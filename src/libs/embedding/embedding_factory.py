"""Factory for creating pluggable embedding backends."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from libs.embedding.azure_embedding import AzureEmbedding
from libs.embedding.base_embedding import BaseEmbedding
from libs.embedding.openai_embedding import OpenAIEmbedding


class EmbeddingFactory:
    """Provider-based constructor for `BaseEmbedding` implementations."""

    _registry: dict[str, type[BaseEmbedding]] = {}
    _builtin_registry: dict[str, type[BaseEmbedding]] = {
        "openai": OpenAIEmbedding,
        "azure": AzureEmbedding,
    }

    @classmethod
    def register(
        cls,
        provider: str,
        embedding_cls: type[BaseEmbedding],
        *,
        overwrite: bool = False,
    ) -> None:
        """Register a provider implementation for later creation."""
        key = cls._normalize_provider(provider)
        if key in cls._builtin_registry and not overwrite:
            raise ValueError(f"Provider '{provider}' is reserved by built-in embeddings")
        if not overwrite and key in cls._registry:
            raise ValueError(f"Provider '{provider}' is already registered")
        cls._registry[key] = embedding_cls

    @classmethod
    def create(cls, settings: Mapping[str, Any] | Any) -> BaseEmbedding:
        """Create an embedding instance from settings containing `embedding.provider`."""
        embedding_settings = cls._extract_embedding_settings(settings)
        provider = embedding_settings.get("provider")
        if not isinstance(provider, str) or not provider.strip():
            raise ValueError("Missing required setting: embedding.provider")

        key = cls._normalize_provider(provider)
        embedding_cls = cls._registry.get(key) or cls._builtin_registry.get(key)
        if embedding_cls is None:
            providers = ", ".join(
                sorted(set(cls._builtin_registry).union(cls._registry))
            ) or "<none>"
            raise ValueError(
                f"Unsupported embedding provider: {provider}. "
                f"Registered providers: {providers}"
            )

        config = dict(embedding_settings)
        config.pop("provider", None)
        model = config.pop("model", None)
        return embedding_cls(model=model, **config)

    @classmethod
    def clear_registry(cls) -> None:
        """Clear all providers (mainly for tests)."""
        cls._registry.clear()

    @classmethod
    def registered_providers(cls) -> tuple[str, ...]:
        """Return currently registered providers in deterministic order."""
        return tuple(sorted(set(cls._builtin_registry).union(cls._registry)))

    @staticmethod
    def _normalize_provider(provider: str) -> str:
        key = provider.strip().lower()
        if not key:
            raise ValueError("Provider must not be empty")
        return key

    @staticmethod
    def _extract_embedding_settings(
        settings: Mapping[str, Any] | Any,
    ) -> dict[str, Any]:
        if isinstance(settings, Mapping):
            if "provider" in settings:
                return dict(settings)
            embedding_settings = settings.get("embedding")
        else:
            embedding_settings = getattr(settings, "embedding", None)

        if not isinstance(embedding_settings, Mapping):
            raise ValueError("Missing required setting: embedding")
        return dict(embedding_settings)
