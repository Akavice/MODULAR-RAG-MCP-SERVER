"""Additional contract tests for B8 vision LLM factory behavior."""

from __future__ import annotations

from typing import Any

import pytest

from libs.llm.base_vision_llm import BaseVisionLLM, ChatResponse
from libs.llm.llm_factory import LLMFactory


class VisionA(BaseVisionLLM):
    def chat_with_image(
        self,
        text: str,
        image_path: str | bytes,
        trace: Any | None = None,
    ) -> ChatResponse:
        _ = trace
        self.validate_inputs(text, image_path)
        return {"text": f"A:{self.model}"}


class VisionB(BaseVisionLLM):
    def chat_with_image(
        self,
        text: str,
        image_path: str | bytes,
        trace: Any | None = None,
    ) -> ChatResponse:
        _ = trace
        self.validate_inputs(text, image_path)
        return {"text": f"B:{self.model}"}


@pytest.fixture(autouse=True)
def reset_registry() -> None:
    LLMFactory.clear_registry()
    yield
    LLMFactory.clear_registry()


@pytest.mark.unit
def test_create_vision_llm_normalizes_provider_name() -> None:
    LLMFactory.register_vision("fake_vision", VisionA)

    llm = LLMFactory.create_vision_llm(
        {"provider": "  FAKE_VISION  ", "model": "v1"}
    )

    assert isinstance(llm, VisionA)
    assert llm.model == "v1"


@pytest.mark.unit
def test_register_vision_overwrite_replaces_provider_binding() -> None:
    LLMFactory.register_vision("fake_vision", VisionA)
    LLMFactory.register_vision("fake_vision", VisionB, overwrite=True)

    llm = LLMFactory.create_vision_llm({"provider": "fake_vision", "model": "v2"})

    assert isinstance(llm, VisionB)
    assert llm.chat_with_image("x", "img.png")["text"] == "B:v2"


@pytest.mark.unit
def test_registered_vision_providers_includes_custom_provider() -> None:
    LLMFactory.register_vision("zz_provider", VisionA)

    providers = LLMFactory.registered_vision_providers()

    assert providers == ("zz_provider",)


@pytest.mark.unit
def test_create_vision_llm_raises_for_missing_vision_llm_block() -> None:
    with pytest.raises(ValueError, match="Missing required setting: vision_llm"):
        LLMFactory.create_vision_llm({"llm": {"provider": "openai"}})

