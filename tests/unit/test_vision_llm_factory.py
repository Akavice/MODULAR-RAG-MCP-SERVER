"""Unit tests for vision LLM factory routing and validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from libs.llm.base_vision_llm import BaseVisionLLM, ChatResponse
from libs.llm.llm_factory import LLMFactory


class FakeVisionLLM(BaseVisionLLM):
    """Small fake implementation used in vision factory tests."""

    def chat_with_image(
        self,
        text: str,
        image_path: str | bytes,
        trace: Any | None = None,
    ) -> ChatResponse:
        _ = trace
        self.validate_inputs(text=text, image_path=image_path)
        return {"text": f"{text}|{self.model}"}


@dataclass(slots=True)
class FakeVisionSettings:
    """Minimal settings object exposing `.vision_llm` mapping."""

    vision_llm: dict[str, Any]


@pytest.fixture(autouse=True)
def reset_llm_registry() -> None:
    """Ensure tests do not leak providers across cases."""
    LLMFactory.clear_registry()
    yield
    LLMFactory.clear_registry()


@pytest.mark.unit
def test_create_vision_llm_routes_by_provider_from_nested_mapping() -> None:
    LLMFactory.register_vision("fake_vision", FakeVisionLLM)

    llm = LLMFactory.create_vision_llm(
        {
            "vision_llm": {
                "provider": "fake_vision",
                "model": "vision-v1",
                "temperature": 0.2,
            }
        }
    )

    assert isinstance(llm, FakeVisionLLM)
    assert llm.model == "vision-v1"
    assert llm.options["temperature"] == 0.2


@pytest.mark.unit
def test_create_vision_llm_accepts_direct_mapping() -> None:
    LLMFactory.register_vision("fake_vision", FakeVisionLLM)

    llm = LLMFactory.create_vision_llm({"provider": "fake_vision", "model": "local"})

    assert isinstance(llm, FakeVisionLLM)
    assert llm.model == "local"


@pytest.mark.unit
def test_create_vision_llm_accepts_object_settings() -> None:
    LLMFactory.register_vision("fake_vision", FakeVisionLLM)
    settings = FakeVisionSettings(
        vision_llm={"provider": "fake_vision", "model": "structured"}
    )

    llm = LLMFactory.create_vision_llm(settings)

    assert isinstance(llm, FakeVisionLLM)
    assert llm.model == "structured"


@pytest.mark.unit
def test_create_vision_llm_raises_for_missing_provider() -> None:
    LLMFactory.register_vision("fake_vision", FakeVisionLLM)

    with pytest.raises(ValueError, match="vision_llm.provider"):
        LLMFactory.create_vision_llm({"vision_llm": {}})


@pytest.mark.unit
def test_create_vision_llm_raises_for_unknown_provider() -> None:
    with pytest.raises(ValueError, match="Unsupported vision_llm provider"):
        LLMFactory.create_vision_llm({"vision_llm": {"provider": "unknown-provider"}})


@pytest.mark.unit
def test_register_vision_raises_when_duplicate_provider_without_overwrite() -> None:
    LLMFactory.register_vision("fake_vision", FakeVisionLLM)

    with pytest.raises(ValueError, match="already registered"):
        LLMFactory.register_vision("fake_vision", FakeVisionLLM)


@pytest.mark.unit
@pytest.mark.parametrize(
    ("text", "image_path", "error_type", "message"),
    [
        (123, "image.png", TypeError, "text must be a string"),
        ("prompt", "", ValueError, "image_path must not be empty"),
        ("prompt", b"", ValueError, "image bytes must not be empty"),
        ("prompt", 123, TypeError, "image_path must be a string path or bytes"),
    ],
)
def test_base_vision_llm_validate_inputs(
    text: Any,
    image_path: Any,
    error_type: type[Exception],
    message: str,
) -> None:
    llm = FakeVisionLLM(model="m")

    with pytest.raises(error_type, match=message):
        llm.chat_with_image(text=text, image_path=image_path)
