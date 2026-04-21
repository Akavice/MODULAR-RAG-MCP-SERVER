"""Factory for creating pluggable splitter backends."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from libs.splitter.base_splitter import BaseSplitter


class SplitterFactory:
    """Provider-based constructor for `BaseSplitter` implementations."""

    _registry: dict[str, type[BaseSplitter]] = {}

    @classmethod
    def register(
        cls,
        provider: str,
        splitter_cls: type[BaseSplitter],
        *,
        overwrite: bool = False,
    ) -> None:
        """Register a provider implementation for later creation."""
        key = cls._normalize_provider(provider)
        if not overwrite and key in cls._registry:
            raise ValueError(f"Provider '{provider}' is already registered")
        cls._registry[key] = splitter_cls

    @classmethod
    def create(cls, settings: Mapping[str, Any] | Any) -> BaseSplitter:
        """Create a splitter instance from settings containing `splitter.provider`."""
        splitter_settings = cls._extract_splitter_settings(settings)
        provider = splitter_settings.get("provider")
        if not isinstance(provider, str) or not provider.strip():
            raise ValueError("Missing required setting: splitter.provider")

        key = cls._normalize_provider(provider)
        splitter_cls = cls._registry.get(key)
        if splitter_cls is None:
            providers = ", ".join(sorted(cls._registry)) or "<none>"
            raise ValueError(
                f"Unsupported splitter provider: {provider}. "
                f"Registered providers: {providers}"
            )

        config = dict(splitter_settings)
        config.pop("provider", None)
        chunk_size = config.pop("chunk_size", 512)
        chunk_overlap = config.pop("chunk_overlap", 50)
        cls._validate_chunking_settings(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        return splitter_cls(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            **config,
        )

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
    def _validate_chunking_settings(*, chunk_size: Any, chunk_overlap: Any) -> None:
        if isinstance(chunk_size, bool) or not isinstance(chunk_size, int):
            raise TypeError("splitter.chunk_size must be an integer")
        if chunk_size <= 0:
            raise ValueError("splitter.chunk_size must be greater than 0")

        if isinstance(chunk_overlap, bool) or not isinstance(chunk_overlap, int):
            raise TypeError("splitter.chunk_overlap must be an integer")
        if chunk_overlap < 0:
            raise ValueError("splitter.chunk_overlap must be >= 0")
        if chunk_overlap >= chunk_size:
            raise ValueError(
                "splitter.chunk_overlap must be smaller than splitter.chunk_size"
            )

    @staticmethod
    def _extract_splitter_settings(settings: Mapping[str, Any] | Any) -> dict[str, Any]:
        if isinstance(settings, Mapping):
            if "provider" in settings:
                return dict(settings)
            splitter_settings = settings.get("splitter")
        else:
            splitter_settings = getattr(settings, "splitter", None)

        if not isinstance(splitter_settings, Mapping):
            raise ValueError("Missing required setting: splitter")
        return dict(splitter_settings)
