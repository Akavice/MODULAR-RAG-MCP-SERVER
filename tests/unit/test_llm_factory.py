"""Unit tests for LLM factory routing and validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from libs.llm.base_llm import BaseLLM, ChatMessage
from libs.llm.llm_factory import LLMFactory


class FakeLLM(BaseLLM):
    """Small fake implementation used in factory tests."""

    def chat(self, messages: list[ChatMessage]) -> str:
        self.validate_messages(messages)
        return str(messages[-1]["content"])


@dataclass(slots=True)
class FakeSettings:
    """Minimal settings object exposing `.llm` mapping."""

    llm: dict[str, Any]


@pytest.fixture(autouse=True)
def reset_llm_registry() -> None:
    """Ensure tests do not leak registered providers across cases."""
    LLMFactory.clear_registry()
    yield
    LLMFactory.clear_registry()


@pytest.mark.unit
def test_create_routes_by_provider_from_nested_mapping() -> None:
    LLMFactory.register("fake", FakeLLM)

    llm = LLMFactory.create(
        {"llm": {"provider": "fake", "model": "fake-model", "temperature": 0.1}}
    )

    assert isinstance(llm, FakeLLM)
    assert llm.model == "fake-model"
    assert llm.options["temperature"] == 0.1


@pytest.mark.unit
def test_create_accepts_direct_llm_mapping() -> None:
    LLMFactory.register("fake", FakeLLM)

    llm = LLMFactory.create({"provider": "fake", "model": "local"})

    assert isinstance(llm, FakeLLM)
    assert llm.model == "local"


@pytest.mark.unit
def test_create_accepts_object_settings() -> None:
    LLMFactory.register("fake", FakeLLM)
    settings = FakeSettings(llm={"provider": "fake", "model": "structured"})

    llm = LLMFactory.create(settings)

    assert isinstance(llm, FakeLLM)
    assert llm.model == "structured"


@pytest.mark.unit
def test_create_raises_for_missing_provider() -> None:
    LLMFactory.register("fake", FakeLLM)

    with pytest.raises(ValueError, match="llm.provider"):
        LLMFactory.create({"llm": {}})


@pytest.mark.unit
def test_create_raises_for_unknown_provider() -> None:
    LLMFactory.register("fake", FakeLLM)

    with pytest.raises(ValueError, match="Unsupported llm provider"):
        LLMFactory.create({"llm": {"provider": "unknown-provider"}})


@pytest.mark.unit
def test_register_raises_when_duplicate_provider_without_overwrite() -> None:
    LLMFactory.register("fake", FakeLLM)

    with pytest.raises(ValueError, match="already registered"):
        LLMFactory.register("fake", FakeLLM)


@pytest.mark.unit
def test_register_raises_for_builtin_provider_without_overwrite() -> None:
    with pytest.raises(ValueError, match="reserved by built-in llms"):
        LLMFactory.register("openai", FakeLLM)
