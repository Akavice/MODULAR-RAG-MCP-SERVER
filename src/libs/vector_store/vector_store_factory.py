"""Factory for creating pluggable vector store backends."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from libs.vector_store.base_vector_store import BaseVectorStore


class VectorStoreFactory:
    """Provider-based constructor for `BaseVectorStore` implementations."""

    _registry: dict[str, type[BaseVectorStore]] = {}

    @classmethod
    def register(
        cls,
        provider: str,
        vector_store_cls: type[BaseVectorStore],
        *,
        overwrite: bool = False,
    ) -> None:
        """Register a provider implementation for later creation."""
        key = cls._normalize_provider(provider)
        if not overwrite and key in cls._registry:
            raise ValueError(f"Provider '{provider}' is already registered")
        cls._registry[key] = vector_store_cls

    @classmethod
    def create(cls, settings: Mapping[str, Any] | Any) -> BaseVectorStore:
        """Create a vector store from settings containing `vector_store.provider`."""
        vector_store_settings = cls._extract_vector_store_settings(settings)
        provider = vector_store_settings.get("provider")
        if not isinstance(provider, str) or not provider.strip():
            raise ValueError("Missing required setting: vector_store.provider")

        key = cls._normalize_provider(provider)
        vector_store_cls = cls._registry.get(key)
        if vector_store_cls is None:
            providers = ", ".join(sorted(cls._registry)) or "<none>"
            raise ValueError(
                f"Unsupported vector_store provider: {provider}. "
                f"Registered providers: {providers}"
            )

        config = dict(vector_store_settings)
        config.pop("provider", None)
        collection_name = config.pop("collection_name", "default")
        collection_name = cls._validate_collection_name(collection_name)
        return vector_store_cls(collection_name=collection_name, **config)

    @classmethod
    def clear_registry(cls) -> None:
        """Clear all providers (mainly for tests)."""
        cls._registry.clear()

    @classmethod
    def registered_providers(cls) -> tuple[str, ...]:
        """Return currently registered providers in deterministic order."""
        return tuple(sorted(cls._registry))

    @staticmethod
    def _normalize_provider(provider: str) -> str:
        key = provider.strip().lower()
        if not key:
            raise ValueError("Provider must not be empty")
        return key

    @staticmethod
    def _validate_collection_name(value: Any) -> str:
        if not isinstance(value, str):
            raise TypeError("vector_store.collection_name must be a string")
        name = value.strip()
        if not name:
            raise ValueError("vector_store.collection_name must not be empty")
        return name

    @staticmethod
    def _extract_vector_store_settings(
        settings: Mapping[str, Any] | Any,
    ) -> dict[str, Any]:
        if isinstance(settings, Mapping):
            if "provider" in settings:
                return dict(settings)
            vector_store_settings = settings.get("vector_store")
        else:
            vector_store_settings = getattr(settings, "vector_store", None)

        if not isinstance(vector_store_settings, Mapping):
            raise ValueError("Missing required setting: vector_store")
        return dict(vector_store_settings)
