"""Azure OpenAI vision-capable LLM backend."""

from __future__ import annotations

import base64
import json
import math
import os
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Callable
from urllib import error as urllib_error
from urllib import request as urllib_request

from libs.llm.base_vision_llm import BaseVisionLLM, ChatResponse


class AzureVisionLLMProviderError(RuntimeError):
    """Provider-scoped error with stable readable formatting."""

    def __init__(self, error_type: str, message: str) -> None:
        super().__init__(f"[azure_vision][{error_type}] {message}")
        self.provider = "azure_vision"
        self.error_type = error_type
        self.message = message


class AzureVisionLLM(BaseVisionLLM):
    """Azure OpenAI vision backend for image understanding."""

    default_model = "gpt-4o-mini"

    def __init__(
        self,
        *,
        model: str | None = None,
        endpoint: str | None = None,
        deployment: str | None = None,
        api_version: str | None = None,
        api_key: str | None = None,
        timeout: float | int | None = None,
        max_image_size: int = 2048,
        detail: str = "auto",
        image_resizer: Callable[[bytes, int], tuple[bytes, dict[str, Any]]] | None = None,
        **options: Any,
    ) -> None:
        endpoint_alias = options.pop("base_url", None)
        azure_endpoint_alias = options.pop("azure_endpoint", None)
        resolved_endpoint = endpoint or endpoint_alias or azure_endpoint_alias
        if isinstance(resolved_endpoint, str):
            resolved_endpoint = resolved_endpoint.rstrip("/")

        resolved_deployment = deployment or options.pop("deployment_name", None) or model
        if not resolved_deployment:
            resolved_deployment = self.default_model

        super().__init__(model=resolved_deployment, **options)
        self.base_url = resolved_endpoint or ""
        self.api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY", "")
        self.api_version = (
            api_version
            or options.get("api_version")
            or os.getenv("AZURE_OPENAI_API_VERSION")
            or "2024-10-21"
        )
        self.timeout = self._normalize_timeout(timeout)
        self.max_image_size = self._normalize_max_image_size(max_image_size)
        self.detail = detail
        self._image_resizer = image_resizer or self._default_resize_image

    def chat_with_image(
        self,
        text: str,
        image_path: str | bytes,
        trace: Any | None = None,
    ) -> ChatResponse:
        _ = trace
        try:
            self.validate_inputs(text=text, image_path=image_path)
            image_bytes, mime_type = self._resolve_image_input(image_path)
            image_bytes, resize_meta = self._image_resizer(image_bytes, self.max_image_size)
            data_url = self._build_data_url(image_bytes=image_bytes, mime_type=mime_type)
            response = self._post_json(
                url=self._build_url(),
                headers=self._build_headers(),
                payload=self._build_payload(text=text, data_url=data_url),
            )
            content = self._extract_content(response)
            return {
                "text": content,
                "metadata": {
                    "provider": "azure_vision",
                    "deployment": self.model or self.default_model,
                    "api_version": self.api_version,
                    **resize_meta,
                },
            }
        except AzureVisionLLMProviderError:
            raise
        except Exception as exc:  # pragma: no cover - defensive fallback
            raise AzureVisionLLMProviderError("RuntimeError", str(exc)) from exc

    def _build_url(self) -> str:
        if not self.base_url:
            raise AzureVisionLLMProviderError("ConfigError", "Missing Azure endpoint")
        return (
            f"{self.base_url}/openai/deployments/{self.model}/chat/completions"
            f"?api-version={self.api_version}"
        )

    def _build_headers(self) -> dict[str, str]:
        api_key = self.api_key.strip()
        if not api_key:
            raise AzureVisionLLMProviderError("ConfigError", "Missing API key")
        return {"Content-Type": "application/json", "api-key": api_key}

    def _build_payload(self, *, text: str, data_url: str) -> dict[str, Any]:
        message = {
            "role": "user",
            "content": [
                {"type": "text", "text": text},
                {
                    "type": "image_url",
                    "image_url": {"url": data_url, "detail": self.detail},
                },
            ],
        }
        payload: dict[str, Any] = {"messages": [message]}
        for key in (
            "temperature",
            "top_p",
            "max_tokens",
            "frequency_penalty",
            "presence_penalty",
            "stop",
            "user",
        ):
            value = self.options.get(key)
            if value is not None:
                payload[key] = value
        return payload

    def _resolve_image_input(self, image_path: str | bytes) -> tuple[bytes, str]:
        if isinstance(image_path, bytes):
            return self._resolve_bytes_input(image_path)

        candidate = image_path.strip()
        path = Path(candidate)
        if path.exists() and path.is_file():
            content = path.read_bytes()
            return content, self._guess_mime_from_path(path)

        if candidate.startswith("data:"):
            return self._parse_data_url(candidate)

        decoded = self._try_decode_base64(candidate.encode("utf-8"))
        if decoded is not None:
            return decoded, self._guess_mime_from_bytes(decoded)

        raise AzureVisionLLMProviderError(
            "ValidationError",
            f"image path does not exist: {candidate}",
        )

    def _resolve_bytes_input(self, content: bytes) -> tuple[bytes, str]:
        decoded = self._try_decode_base64(content)
        if decoded is not None:
            return decoded, self._guess_mime_from_bytes(decoded)
        return content, self._guess_mime_from_bytes(content)

    @staticmethod
    def _try_decode_base64(content: bytes) -> bytes | None:
        try:
            text = content.decode("utf-8").strip()
        except UnicodeDecodeError:
            return None
        if not text:
            return None
        try:
            decoded = base64.b64decode(text, validate=True)
        except Exception:
            return None
        if not decoded:
            return None
        return decoded

    @staticmethod
    def _parse_data_url(value: str) -> tuple[bytes, str]:
        marker = ";base64,"
        if marker not in value:
            raise AzureVisionLLMProviderError(
                "ValidationError",
                "data URL must include ';base64,' marker",
            )
        header, encoded = value.split(marker, 1)
        mime_type = header[5:] or "image/png"
        try:
            decoded = base64.b64decode(encoded, validate=True)
        except Exception as exc:
            raise AzureVisionLLMProviderError(
                "ValidationError",
                "invalid base64 data URL content",
            ) from exc
        if not decoded:
            raise AzureVisionLLMProviderError(
                "ValidationError",
                "data URL image bytes must not be empty",
            )
        return decoded, mime_type

    @staticmethod
    def _guess_mime_from_path(path: Path) -> str:
        suffix = path.suffix.lower()
        if suffix in {".jpg", ".jpeg"}:
            return "image/jpeg"
        if suffix == ".png":
            return "image/png"
        if suffix == ".webp":
            return "image/webp"
        if suffix == ".gif":
            return "image/gif"
        return "image/png"

    @staticmethod
    def _guess_mime_from_bytes(content: bytes) -> str:
        if content.startswith(b"\x89PNG\r\n\x1a\n"):
            return "image/png"
        if content.startswith(b"\xff\xd8\xff"):
            return "image/jpeg"
        if content.startswith(b"GIF87a") or content.startswith(b"GIF89a"):
            return "image/gif"
        if content.startswith(b"RIFF") and b"WEBP" in content[:16]:
            return "image/webp"
        return "image/png"

    @staticmethod
    def _build_data_url(*, image_bytes: bytes, mime_type: str) -> str:
        encoded = base64.b64encode(image_bytes).decode("utf-8")
        return f"data:{mime_type};base64,{encoded}"

    @staticmethod
    def _normalize_max_image_size(value: Any) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("max_image_size must be an integer")
        if value <= 0:
            raise ValueError("max_image_size must be greater than 0")
        return value

    @staticmethod
    def _normalize_timeout(value: Any) -> float:
        if value is None:
            return 30.0
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("timeout must be a number when provided")
        normalized = float(value)
        if not math.isfinite(normalized) or normalized <= 0:
            raise ValueError("timeout must be a finite number greater than 0")
        return normalized

    @staticmethod
    def _default_resize_image(
        image_bytes: bytes,
        max_image_size: int,
    ) -> tuple[bytes, dict[str, Any]]:
        _ = max_image_size
        try:
            from PIL import Image  # type: ignore
        except Exception:
            return image_bytes, {"image_resized": False, "resize_reason": "pillow_unavailable"}

        from io import BytesIO

        try:
            with Image.open(BytesIO(image_bytes)) as img:
                width, height = img.size
                if max(width, height) <= max_image_size:
                    return image_bytes, {
                        "image_resized": False,
                        "image_size": {"width": width, "height": height},
                    }

                img.thumbnail((max_image_size, max_image_size))
                output = BytesIO()
                format_name = (img.format or "PNG").upper()
                img.save(output, format=format_name)
                resized = output.getvalue()
                return resized, {
                    "image_resized": True,
                    "image_size": {"width": img.size[0], "height": img.size[1]},
                    "resize_format": format_name,
                }
        except Exception as exc:
            return image_bytes, {
                "image_resized": False,
                "resize_reason": f"resize_skipped: {exc}",
            }

    def _post_json(
        self,
        *,
        url: str,
        headers: Mapping[str, str],
        payload: Mapping[str, Any],
    ) -> dict[str, Any]:
        body = json.dumps(payload).encode("utf-8")
        req = urllib_request.Request(url=url, data=body, headers=dict(headers), method="POST")
        try:
            with urllib_request.urlopen(req, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
                parsed = json.loads(raw or "{}")
                if not isinstance(parsed, dict):
                    raise AzureVisionLLMProviderError(
                        "ResponseError",
                        "Response body must be a JSON object",
                    )
                return parsed
        except TimeoutError as exc:
            raise AzureVisionLLMProviderError("TimeoutError", str(exc)) from exc
        except urllib_error.HTTPError as exc:
            raw_error = exc.read().decode("utf-8", errors="replace")
            azure_error = self._extract_azure_error(raw_error)
            message = f"{exc.code} {exc.reason}"
            if azure_error:
                message = f"{message} ({azure_error})"
            raise AzureVisionLLMProviderError("HTTPError", message) from exc
        except urllib_error.URLError as exc:
            raise AzureVisionLLMProviderError("ConnectionError", str(exc.reason)) from exc
        except json.JSONDecodeError as exc:
            raise AzureVisionLLMProviderError(
                "ResponseError",
                "Invalid JSON response",
            ) from exc

    @staticmethod
    def _extract_azure_error(raw_error: str) -> str:
        try:
            payload = json.loads(raw_error or "{}")
        except json.JSONDecodeError:
            return raw_error[:200]
        if not isinstance(payload, dict):
            return raw_error[:200]
        error = payload.get("error")
        if not isinstance(error, dict):
            return raw_error[:200]
        code = str(error.get("code", "")).strip()
        message = str(error.get("message", "")).strip()
        if code and message:
            return f"{code}: {message}"
        if code:
            return code
        if message:
            return message
        return raw_error[:200]

    @staticmethod
    def _extract_content(response: Mapping[str, Any]) -> str:
        choices = response.get("choices")
        if not isinstance(choices, list) or not choices:
            raise AzureVisionLLMProviderError(
                "ResponseError",
                "Missing non-empty choices in response",
            )
        first = choices[0]
        if not isinstance(first, Mapping):
            raise AzureVisionLLMProviderError(
                "ResponseError",
                "First choice must be an object",
            )
        message = first.get("message")
        if not isinstance(message, Mapping):
            raise AzureVisionLLMProviderError(
                "ResponseError",
                "Choice message must be an object",
            )
        content = message.get("content")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            text_parts: list[str] = []
            for item in content:
                if isinstance(item, Mapping) and isinstance(item.get("text"), str):
                    text_parts.append(item["text"])
            if text_parts:
                return "\n".join(text_parts)
        raise AzureVisionLLMProviderError(
            "ResponseError",
            "Missing textual content in response",
        )
