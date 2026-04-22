"""Factory for creating pluggable LLM backends."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from libs.llm.base_llm import BaseLLM
from libs.llm.azure_llm import AzureLLM
from libs.llm.deepseek_llm import DeepSeekLLM
from libs.llm.ollama_llm import OllamaLLM
from libs.llm.openai_llm import OpenAILLM


class LLMFactory:
    """Provider-based constructor for `BaseLLM` implementations."""

    _registry: dict[str, type[BaseLLM]] = {}
    _builtin_registry: dict[str, type[BaseLLM]] = {
        "openai": OpenAILLM,
        "azure": AzureLLM,
        "deepseek": DeepSeekLLM,
        "ollama": OllamaLLM,
    }

    @classmethod
    def register(
        cls,
        provider: str,
        llm_cls: type[BaseLLM],
        *,
        overwrite: bool = False,
    ) -> None:
        """Register a provider implementation for later creation."""
        key = cls._normalize_provider(provider)
        if key in cls._builtin_registry and not overwrite:
            raise ValueError(f"Provider '{provider}' is reserved by built-in llms")
        if not overwrite and key in cls._registry:
            raise ValueError(f"Provider '{provider}' is already registered")
        cls._registry[key] = llm_cls

    @classmethod
    def create(cls, settings: Mapping[str, Any] | Any) -> BaseLLM:
        """Create an LLM instance from settings containing `llm.provider`."""
        llm_settings = cls._extract_llm_settings(settings)
        provider = llm_settings.get("provider")
        if not isinstance(provider, str) or not provider.strip():
            raise ValueError("Missing required setting: llm.provider")

        key = cls._normalize_provider(provider)
        llm_cls = cls._registry.get(key) or cls._builtin_registry.get(key)
        if llm_cls is None:
            providers = ", ".join(
                sorted(set(cls._builtin_registry).union(cls._registry))
            ) or "<none>"
            raise ValueError(
                f"Unsupported llm provider: {provider}. Registered providers: {providers}"
            )

        config = dict(llm_settings)
        config.pop("provider", None)
        model = config.pop("model", None)
        return llm_cls(model=model, **config)

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
    def _extract_llm_settings(settings: Mapping[str, Any] | Any) -> dict[str, Any]:
        if isinstance(settings, Mapping):
            if "provider" in settings:
                return dict(settings)
            llm_settings = settings.get("llm")
        else:
            llm_settings = getattr(settings, "llm", None)

        if not isinstance(llm_settings, Mapping):
            raise ValueError("Missing required setting: llm")
        return dict(llm_settings)
