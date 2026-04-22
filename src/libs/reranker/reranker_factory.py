"""Factory for creating pluggable reranker backends."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from libs.reranker.base_reranker import BaseReranker, RerankCandidate


class NoneReranker(BaseReranker):
    """Fallback reranker that preserves original candidate order."""

    def rerank(
        self,
        query: str,
        candidates: list[dict[str, Any]] | tuple[dict[str, Any], ...],
        trace: Any | None = None,
    ) -> list[RerankCandidate]:
        self.validate_inputs(query=query, candidates=candidates)
        return [dict(candidate) for candidate in candidates]


class RerankerFactory:
    """Provider-based constructor for `BaseReranker` implementations."""

    _registry: dict[str, type[BaseReranker]] = {}
    _builtin_registry: dict[str, type[BaseReranker]] = {"none": NoneReranker}

    @classmethod
    def register(
        cls,
        provider: str,
        reranker_cls: type[BaseReranker],
        *,
        overwrite: bool = False,
    ) -> None:
        """Register a provider implementation for later creation."""
        key = cls._normalize_provider(provider)
        if key in cls._builtin_registry and not overwrite:
            raise ValueError(f"Provider '{provider}' is reserved by built-in rerankers")
        if not overwrite and key in cls._registry:
            raise ValueError(f"Provider '{provider}' is already registered")
        cls._registry[key] = reranker_cls

    @classmethod
    def create(cls, settings: Mapping[str, Any] | Any) -> BaseReranker:
        """Create a reranker from settings containing `rerank.provider`."""
        rerank_settings = cls._extract_rerank_settings(settings)
        provider = rerank_settings.get("provider")
        if not isinstance(provider, str) or not provider.strip():
            raise ValueError("Missing required setting: rerank.provider")

        key = cls._normalize_provider(provider)
        reranker_cls = cls._registry.get(key) or cls._builtin_registry.get(key)
        if reranker_cls is None:
            providers = ", ".join(
                sorted(set(cls._builtin_registry).union(cls._registry))
            ) or "<none>"
            raise ValueError(
                f"Unsupported rerank provider: {provider}. "
                f"Registered providers: {providers}"
            )

        config = dict(rerank_settings)
        config.pop("provider", None)
        return reranker_cls(**config)

    @classmethod
    def clear_registry(cls) -> None:
        """Clear custom providers (mainly for tests)."""
        cls._registry.clear()

    @classmethod
    def registered_providers(cls) -> tuple[str, ...]:
        """Return available providers in deterministic order."""
        return tuple(sorted(set(cls._builtin_registry).union(cls._registry)))

    @staticmethod
    def _normalize_provider(provider: str) -> str:
        key = provider.strip().lower()
        if not key:
            raise ValueError("Provider must not be empty")
        return key

    @staticmethod
    def _extract_rerank_settings(settings: Mapping[str, Any] | Any) -> dict[str, Any]:
        if isinstance(settings, Mapping):
            if "provider" in settings:
                return dict(settings)
            rerank_settings = settings.get("rerank")
        else:
            rerank_settings = getattr(settings, "rerank", None)

        if not isinstance(rerank_settings, Mapping):
            raise ValueError("Missing required setting: rerank")
        return dict(rerank_settings)
