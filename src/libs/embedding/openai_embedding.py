"""OpenAI-compatible embedding implementations and shared HTTP logic."""

from __future__ import annotations

import json
import os
from collections.abc import Mapping, Sequence
from typing import Any
from urllib import error as urllib_error
from urllib import request as urllib_request

from libs.embedding.base_embedding import BaseEmbedding


class EmbeddingProviderError(RuntimeError):
    """Provider-scoped error with stable readable formatting."""

    def __init__(self, provider: str, error_type: str, message: str) -> None:
        super().__init__(f"[{provider}][{error_type}] {message}")
        self.provider = provider
        self.error_type = error_type
        self.message = message


class OpenAICompatibleEmbedding(BaseEmbedding):
    """Reusable OpenAI-compatible embedding client."""

    provider_name = "openai"
    default_base_url = "https://api.openai.com/v1"
    api_key_env_name = "OPENAI_API_KEY"
    default_model = "text-embedding-3-small"
    timeout_seconds = 30.0

    def __init__(
        self,
        *,
        model: str | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float | int | None = None,
        max_input_chars: int | None = None,
        **options: Any,
    ) -> None:
        super().__init__(model=model or self.default_model, **options)
        self.base_url = (base_url or self.default_base_url).rstrip("/")
        self.api_key = api_key or os.getenv(self.api_key_env_name, "")
        self.timeout = float(timeout or self.timeout_seconds)
        self.max_input_chars = max_input_chars

    def embed(self, texts: Sequence[str], trace: Any | None = None) -> list[list[float]]:
        try:
            self.validate_texts(texts)
            self._validate_text_lengths(texts)
        except Exception as exc:
            raise EmbeddingProviderError(
                self.provider_name,
                "ValidationError",
                str(exc),
            ) from exc

        try:
            response = self._post_json(
                url=self._build_url(),
                headers=self._build_headers(),
                payload=self._build_payload(texts),
            )
            return self._extract_embeddings(response)
        except EmbeddingProviderError:
            raise
        except Exception as exc:  # pragma: no cover - defensive fallback
            raise EmbeddingProviderError(
                self.provider_name,
                "RuntimeError",
                str(exc),
            ) from exc

    def _build_url(self) -> str:
        return f"{self.base_url}/embeddings"

    def _build_headers(self) -> dict[str, str]:
        api_key = self.api_key.strip()
        if not api_key:
            raise EmbeddingProviderError(
                self.provider_name,
                "ConfigError",
                "Missing API key",
            )
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

    def _build_payload(self, texts: Sequence[str]) -> dict[str, Any]:
        return {"model": self.model, "input": list(texts)}

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
                    raise EmbeddingProviderError(
                        self.provider_name,
                        "ResponseError",
                        "Response body must be a JSON object",
                    )
                return parsed
        except urllib_error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            raise EmbeddingProviderError(
                self.provider_name,
                "HTTPError",
                f"{exc.code} {exc.reason}: {error_body[:300]}",
            ) from exc
        except urllib_error.URLError as exc:
            raise EmbeddingProviderError(
                self.provider_name,
                "ConnectionError",
                str(exc.reason),
            ) from exc
        except json.JSONDecodeError as exc:
            raise EmbeddingProviderError(
                self.provider_name,
                "ResponseError",
                "Invalid JSON response",
            ) from exc

    def _extract_embeddings(self, response: Mapping[str, Any]) -> list[list[float]]:
        data = response.get("data")
        if not isinstance(data, list) or not data:
            raise EmbeddingProviderError(
                self.provider_name,
                "ResponseError",
                "Missing non-empty data list in response",
            )

        embeddings: list[list[float]] = []
        for index, item in enumerate(data):
            if not isinstance(item, Mapping):
                raise EmbeddingProviderError(
                    self.provider_name,
                    "ResponseError",
                    f"Data item at index {index} must be an object",
                )
            vector = item.get("embedding")
            if not isinstance(vector, list) or not vector:
                raise EmbeddingProviderError(
                    self.provider_name,
                    "ResponseError",
                    f"Embedding at index {index} is missing or empty",
                )
            normalized: list[float] = []
            for dim, value in enumerate(vector):
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    raise EmbeddingProviderError(
                        self.provider_name,
                        "ResponseError",
                        f"Embedding value at item {index}, dim {dim} is non-numeric",
                    )
                normalized.append(float(value))
            embeddings.append(normalized)

        return embeddings

    def _validate_text_lengths(self, texts: Sequence[str]) -> None:
        if self.max_input_chars is None:
            return
        if isinstance(self.max_input_chars, bool) or not isinstance(self.max_input_chars, int):
            raise ValueError("max_input_chars must be an integer")
        if self.max_input_chars <= 0:
            raise ValueError("max_input_chars must be greater than 0")

        for index, text in enumerate(texts):
            if len(text) > self.max_input_chars:
                raise ValueError(
                    f"text at index {index} exceeds max_input_chars={self.max_input_chars}"
                )


class OpenAIEmbedding(OpenAICompatibleEmbedding):
    """OpenAI embedding backend."""

    provider_name = "openai"
    default_base_url = "https://api.openai.com/v1"
    api_key_env_name = "OPENAI_API_KEY"
    default_model = "text-embedding-3-small"
