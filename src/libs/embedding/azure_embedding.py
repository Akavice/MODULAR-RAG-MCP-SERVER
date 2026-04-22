"""Azure OpenAI-compatible embedding backend."""

from __future__ import annotations

import os
from collections.abc import Sequence
from typing import Any

from libs.embedding.openai_embedding import (
    EmbeddingProviderError,
    OpenAICompatibleEmbedding,
)


class AzureEmbedding(OpenAICompatibleEmbedding):
    """Azure OpenAI embedding backend."""

    provider_name = "azure"
    default_base_url = ""
    api_key_env_name = "AZURE_OPENAI_API_KEY"
    default_model = "text-embedding-ada-002"

    def __init__(
        self,
        *,
        model: str | None = None,
        endpoint: str | None = None,
        deployment: str | None = None,
        api_version: str | None = None,
        api_key: str | None = None,
        timeout: float | int | None = None,
        max_input_chars: int | None = None,
        **options: Any,
    ) -> None:
        endpoint_alias = options.pop("base_url", None)
        azure_endpoint_alias = options.pop("azure_endpoint", None)
        resolved_endpoint = endpoint or endpoint_alias or azure_endpoint_alias

        resolved_deployment = deployment or options.pop("deployment_name", None) or model
        if not resolved_deployment:
            resolved_deployment = self.default_model

        super().__init__(
            model=resolved_deployment,
            base_url=resolved_endpoint,
            api_key=api_key,
            timeout=timeout,
            max_input_chars=max_input_chars,
            **options,
        )
        self.api_version = (
            api_version
            or options.get("api_version")
            or os.getenv("AZURE_OPENAI_API_VERSION")
            or "2024-10-21"
        )

    def _build_url(self) -> str:
        if not self.base_url:
            raise EmbeddingProviderError(
                self.provider_name,
                "ConfigError",
                "Missing Azure endpoint",
            )
        endpoint = self.base_url.rstrip("/")
        return (
            f"{endpoint}/openai/deployments/{self.model}/embeddings"
            f"?api-version={self.api_version}"
        )

    def _build_headers(self) -> dict[str, str]:
        api_key = self.api_key.strip()
        if not api_key:
            raise EmbeddingProviderError(
                self.provider_name,
                "ConfigError",
                "Missing API key",
            )
        return {"Content-Type": "application/json", "api-key": api_key}

    def _build_payload(self, texts: Sequence[str]) -> dict[str, Any]:
        return {"input": list(texts)}
