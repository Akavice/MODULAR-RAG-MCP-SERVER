"""Factory for creating pluggable evaluator backends."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from libs.evaluator.base_evaluator import BaseEvaluator
from libs.evaluator.custom_evaluator import CustomEvaluator
from libs.evaluator.ragas_evaluator import RagasEvaluator


class EvaluatorFactory:
    """Provider-based constructor for `BaseEvaluator` implementations."""

    _registry: dict[str, type[BaseEvaluator]] = {}
    _builtin_registry: dict[str, type[BaseEvaluator]] = {
        "custom": CustomEvaluator,
        "ragas": RagasEvaluator,
    }

    @classmethod
    def register(
        cls,
        provider: str,
        evaluator_cls: type[BaseEvaluator],
        *,
        overwrite: bool = False,
    ) -> None:
        """Register a provider implementation for later creation."""
        key = cls._normalize_provider(provider)
        if key in cls._builtin_registry and not overwrite:
            raise ValueError(f"Provider '{provider}' is reserved by built-in evaluators")
        if not overwrite and key in cls._registry:
            raise ValueError(f"Provider '{provider}' is already registered")
        cls._registry[key] = evaluator_cls

    @classmethod
    def create(cls, settings: Mapping[str, Any] | Any) -> BaseEvaluator:
        """Create an evaluator from settings containing `evaluation.provider`."""
        evaluation_settings = cls._extract_evaluation_settings(settings)
        provider = evaluation_settings.get("provider")
        if not isinstance(provider, str) or not provider.strip():
            raise ValueError("Missing required setting: evaluation.provider")

        key = cls._normalize_provider(provider)
        evaluator_cls = cls._registry.get(key) or cls._builtin_registry.get(key)
        if evaluator_cls is None:
            providers = ", ".join(
                sorted(set(cls._builtin_registry).union(cls._registry))
            ) or "<none>"
            raise ValueError(
                f"Unsupported evaluation provider: {provider}. "
                f"Registered providers: {providers}"
            )

        config = dict(evaluation_settings)
        config.pop("provider", None)
        return evaluator_cls(**config)

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
    def _extract_evaluation_settings(
        settings: Mapping[str, Any] | Any,
    ) -> dict[str, Any]:
        if isinstance(settings, Mapping):
            if "provider" in settings:
                return dict(settings)
            evaluation_settings = settings.get("evaluation")
        else:
            evaluation_settings = getattr(settings, "evaluation", None)

        if not isinstance(evaluation_settings, Mapping):
            raise ValueError("Missing required setting: evaluation")
        return dict(evaluation_settings)
