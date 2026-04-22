"""OpenAI-compatible LLM implementations and shared HTTP logic."""

from __future__ import annotations

import json
import os
from collections.abc import Mapping, Sequence
from typing import Any
from urllib import error as urllib_error
from urllib import request as urllib_request

from libs.llm.base_llm import BaseLLM, ChatMessage


class LLMProviderError(RuntimeError):
    """Provider-scoped error with stable readable formatting."""

    def __init__(self, provider: str, error_type: str, message: str) -> None:
        super().__init__(f"[{provider}][{error_type}] {message}")
        self.provider = provider
        self.error_type = error_type
        self.message = message


class OpenAICompatibleLLM(BaseLLM):
    """Reusable OpenAI-compatible chat completion client."""

    provider_name = "openai"
    default_base_url = "https://api.openai.com/v1"
    api_key_env_name = "OPENAI_API_KEY"
    default_model = "gpt-4o-mini"
    timeout_seconds = 30.0

    def __init__(
        self,
        *,
        model: str | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float | int | None = None,
        **options: Any,
    ) -> None:
        super().__init__(model=model or self.default_model, **options)
        self.base_url = (base_url or self.default_base_url).rstrip("/")
        self.api_key = api_key or os.getenv(self.api_key_env_name, "")
        self.timeout = float(timeout or self.timeout_seconds)

    def chat(self, messages: Sequence[ChatMessage]) -> str:
        try:
            self.validate_messages(messages)
        except Exception as exc:  # pragma: no cover - covered by tests
            raise LLMProviderError(
                self.provider_name,
                "ValidationError",
                str(exc),
            ) from exc

        try:
            response = self._post_json(
                url=self._build_url(),
                headers=self._build_headers(),
                payload=self._build_payload(messages),
            )
            return self._extract_content(response)
        except LLMProviderError:
            raise
        except Exception as exc:  # pragma: no cover - defensive fallback
            raise LLMProviderError(self.provider_name, "RuntimeError", str(exc)) from exc

    def _build_url(self) -> str:
        return f"{self.base_url}/chat/completions"

    def _build_headers(self) -> dict[str, str]:
        api_key = self.api_key.strip()
        if not api_key:
            raise LLMProviderError(
                self.provider_name,
                "ConfigError",
                "Missing API key",
            )
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

    def _build_payload(self, messages: Sequence[ChatMessage]) -> dict[str, Any]:
        return {"model": self.model, "messages": [dict(msg) for msg in messages]}

    def _post_json(
        self,
        *,
        url: str,
        headers: Mapping[str, str],
        payload: Mapping[str, Any],
    ) -> dict[str, Any]:
        body = json.dumps(payload).encode("utf-8")
        req = urllib_request.Request(
            url=url,
            data=body,
            headers=dict(headers),
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
            raise LLMProviderError(
                self.provider_name,
                "ConnectionError",
                str(exc.reason),
            ) from exc
        except json.JSONDecodeError as exc:
            raise LLMProviderError(
                self.provider_name,
                "ResponseError",
                "Invalid JSON response",
            ) from exc

    def _extract_content(self, response: Mapping[str, Any]) -> str:
        choices = response.get("choices")
        if not isinstance(choices, list) or not choices:
            raise LLMProviderError(
                self.provider_name,
                "ResponseError",
                "Missing non-empty choices in response",
            )

        first = choices[0]
        if not isinstance(first, Mapping):
            raise LLMProviderError(
                self.provider_name,
                "ResponseError",
                "First choice must be an object",
            )
        message = first.get("message")
        if not isinstance(message, Mapping):
            raise LLMProviderError(
                self.provider_name,
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
        raise LLMProviderError(
            self.provider_name,
            "ResponseError",
            "Missing textual content in response",
        )


class OpenAILLM(OpenAICompatibleLLM):
    """OpenAI chat completion backend."""

    provider_name = "openai"
    default_base_url = "https://api.openai.com/v1"
    api_key_env_name = "OPENAI_API_KEY"
    default_model = "gpt-4o-mini"
