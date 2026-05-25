"""Unit tests for ImageCaptioner fallback and happy-path behavior."""

from __future__ import annotations

from typing import Any

import pytest

from core.types import Chunk
from ingestion.transform.image_captioner import ImageCaptioner
from libs.llm.base_vision_llm import BaseVisionLLM


class FakeVisionLLM(BaseVisionLLM):
    def __init__(self, *, reply: str = "caption", **options: Any) -> None:
        super().__init__(**options)
        self.reply = reply
        self.calls: list[tuple[str, str | bytes]] = []

    def chat_with_image(
        self,
        text: str,
        image_path: str | bytes,
        trace: Any | None = None,
    ) -> dict[str, Any]:
        _ = trace
        self.calls.append((text, image_path))
        return {"text": self.reply, "metadata": {"provider": "fake_vision"}}


class RaisingVisionLLM(BaseVisionLLM):
    def chat_with_image(
        self,
        text: str,
        image_path: str | bytes,
        trace: Any | None = None,
    ) -> dict[str, Any]:
        _ = text, image_path, trace
        raise RuntimeError("vision down")


class TraceStub:
    def __init__(self) -> None:
        self.events: list[tuple[str, dict[str, Any]]] = []

    def record_stage(self, stage: str, **payload: Any) -> None:
        self.events.append((stage, payload))


def _chunk_with_image() -> Chunk:
    return Chunk(
        id="c1",
        text="The chart below explains growth [IMAGE: img_1]",
        metadata={
            "source_path": "docs/a.pdf",
            "image_refs": ["img_1"],
            "images": [{"id": "img_1", "path": "data/images/a/img_1.png"}],
        },
        start_offset=0,
        end_offset=40,
        source_ref="doc-1",
    )


def _chunk_without_image() -> Chunk:
    return Chunk(
        id="c2",
        text="No image refs here.",
        metadata={"source_path": "docs/a.pdf"},
        start_offset=0,
        end_offset=18,
        source_ref="doc-1",
    )


@pytest.mark.unit
def test_disabled_mode_marks_unprocessed_and_does_not_call_llm() -> None:
    llm = FakeVisionLLM(reply="never used")
    captioner = ImageCaptioner(
        settings={"ingestion": {"image_captioner": {"use_vision_llm": False}}},
        vision_llm=llm,
    )

    out = captioner.transform([_chunk_with_image()])

    assert out[0].metadata["has_unprocessed_images"] is True
    assert out[0].metadata["image_caption_fallback_reason"] == "captioning_disabled"
    assert "image_captions" not in out[0].metadata
    assert len(llm.calls) == 0


@pytest.mark.unit
def test_no_image_refs_returns_chunk_unchanged() -> None:
    captioner = ImageCaptioner(
        settings={"ingestion": {"image_captioner": {"use_vision_llm": True}}},
        vision_llm=FakeVisionLLM(),
    )
    chunk = _chunk_without_image()

    out = captioner.transform([chunk])[0]

    assert out.metadata == chunk.metadata
    assert out.text == chunk.text


@pytest.mark.unit
def test_enabled_mode_generates_caption_and_writes_metadata() -> None:
    llm = FakeVisionLLM(reply="A line chart showing quarterly growth.")
    captioner = ImageCaptioner(
        settings={"ingestion": {"image_captioner": {"use_vision_llm": True}}},
        vision_llm=llm,
    )

    out = captioner.transform([_chunk_with_image()])[0]

    assert out.metadata["captioned_by"] == "vision_llm"
    assert out.metadata["image_captions"]["img_1"] == "A line chart showing quarterly growth."
    assert "has_unprocessed_images" not in out.metadata
    assert len(llm.calls) == 1


@pytest.mark.unit
def test_vision_llm_error_falls_back_without_crash() -> None:
    captioner = ImageCaptioner(
        settings={"ingestion": {"image_captioner": {"use_vision_llm": True}}},
        vision_llm=RaisingVisionLLM(),
    )

    out = captioner.transform([_chunk_with_image()])[0]

    assert out.metadata["has_unprocessed_images"] is True
    assert "captioning_failed" in out.metadata["image_caption_fallback_reason"]
    assert "image_captions" not in out.metadata


@pytest.mark.unit
def test_missing_image_path_marks_unprocessed() -> None:
    chunk = Chunk(
        id="c3",
        text="A ref with missing path [IMAGE: img_2]",
        metadata={
            "source_path": "docs/a.pdf",
            "image_refs": ["img_2"],
            "images": [],
        },
        start_offset=0,
        end_offset=30,
        source_ref="doc-1",
    )
    captioner = ImageCaptioner(
        settings={"ingestion": {"image_captioner": {"use_vision_llm": True}}},
        vision_llm=FakeVisionLLM(),
    )

    out = captioner.transform([chunk])[0]

    assert out.metadata["has_unprocessed_images"] is True
    assert out.metadata["image_caption_fallback_reason"] == "no_caption_generated"


@pytest.mark.unit
def test_trace_counts_captioned_and_unprocessed() -> None:
    trace = TraceStub()
    llm = FakeVisionLLM(reply="caption")
    captioner = ImageCaptioner(
        settings={"ingestion": {"image_captioner": {"use_vision_llm": True}}},
        vision_llm=llm,
    )
    bad_chunk = Chunk(
        id="c4",
        text="bad image item",
        metadata={
            "source_path": "docs/a.pdf",
            "image_refs": ["img_x"],
            "images": [],
        },
        start_offset=0,
        end_offset=10,
        source_ref="doc-1",
    )

    captioner.transform([_chunk_with_image(), bad_chunk, _chunk_without_image()], trace=trace)
    stage, payload = trace.events[-1]

    assert stage == "transform_image_captioner"
    assert payload["chunk_count"] == 3
    assert payload["captioned_count"] == 1
    assert payload["unprocessed_count"] == 1
