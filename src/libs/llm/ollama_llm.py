"""Ollama LLM backend implementation."""

from __future__ import annotations

import json
import socket
from collections.abc import Mapping, Sequence
from typing import Any
from urllib import error as urllib_error
from urllib import request as urllib_request

from libs.llm.base_llm import BaseLLM, ChatMessage
from libs.llm.openai_llm import LLMProviderError


class OllamaLLM(BaseLLM):
    """Ollama chat backend via local HTTP endpoint."""

    provider_name = "ollama"
    default_base_url = "http://localhost:11434"
    default_model = "llama3.1"
    timeout_seconds = 30.0

    def __init__(
        self,
        *,
        model: str | None = None,
        base_url: str | None = None,
        timeout: float | int | None = None,
        **options: Any,
    ) -> None:
        super().__init__(model=model or self.default_model, **options)
        self.base_url = (base_url or self.default_base_url).rstrip("/")
        self.timeout = float(timeout or self.timeout_seconds)

    def chat(self, messages: Sequence[ChatMessage]) -> str:
        try:
            self.validate_messages(messages)
        except Exception as exc:
            raise LLMProviderError(self.provider_name, "ValidationError", str(exc)) from exc

        if not isinstance(self.base_url, str) or not self.base_url.strip():
            raise LLMProviderError(
                self.provider_name,
                "ConfigError",
                "Missing Ollama base_url",
            )

        try:
            response = self._post_json(
                url=self._build_url(),
                payload=self._build_payload(messages),
            )
            return self._extract_content(response)
        except LLMProviderError:
            raise
        except Exception as exc:  # pragma: no cover - defensive fallback
            raise LLMProviderError(self.provider_name, "RuntimeError", str(exc)) from exc

    def _build_url(self) -> str:
        return f"{self.base_url}/api/chat"

    def _build_payload(self, messages: Sequence[ChatMessage]) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [dict(msg) for msg in messages],
            "stream": False,
        }
        if "temperature" in self.options:
            payload["options"] = {"temperature": self.options["temperature"]}
        return payload

    def _post_json(self, *, url: str, payload: Mapping[str, Any]) -> dict[str, Any]:
        body = json.dumps(payload).encode("utf-8")
        req = urllib_request.Request(
            url=url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib_request.urlopen(req, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
                parsed = json.loads(raw or "{}")
                if not isinstance(parsed, dict):
                    raise LLMProviderError(
                        self.provider_name,
                        "ResponseError",
                        "Response body must be a JSON object",
                    )
                return parsed
        except urllib_error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            raise LLMProviderError(
                self.provider_name,
                "HTTPError",
                f"{exc.code} {exc.reason}: {error_body[:300]}",
            ) from exc
        except urllib_error.URLError as exc:
            reason = getattr(exc, "reason", exc)
            raise LLMProviderError(
                self.provider_name,
                "ConnectionError",
                str(reason),
            ) from exc
        except (TimeoutError, socket.timeout) as exc:
            raise LLMProviderError(
                self.provider_name,
                "ConnectionError",
                "Request timeout",
            ) from exc
        except json.JSONDecodeError as exc:
            raise LLMProviderError(
                self.provider_name,
                "ResponseError",
                "Invalid JSON response",
            ) from exc

    def _extract_content(self, response: Mapping[str, Any]) -> str:
        message = response.get("message")
        if not isinstance(message, Mapping):
            raise LLMProviderError(
                self.provider_name,
                "ResponseError",
                "Missing message object in response",
            )
        content = message.get("content")
        if not isinstance(content, str):
            raise LLMProviderError(
                self.provider_name,
                "ResponseError",
                "Missing textual content in response",
            )
        return content
