"""Unit tests for DocumentChunker adapter behavior."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from core.types import Document
from ingestion.chunking.document_chunker import DocumentChunker
from libs.splitter.base_splitter import BaseSplitter
from libs.splitter.splitter_factory import SplitterFactory


class FakeSplitter(BaseSplitter):
    """Deterministic splitter used to isolate chunker adapter behavior."""

    def split(self, text: str, trace: Any | None = None) -> list[str]:
        _ = trace
        self.validate_text(text)

        predefined = self.options.get("precomputed_chunks")
        if isinstance(predefined, list):
            return [str(item) for item in predefined]

        size = max(1, self.chunk_size)
        return [text[i : i + size] for i in range(0, len(text), size)]


@dataclass(slots=True)
class FakeSettings:
    splitter: dict[str, Any]


@pytest.fixture(autouse=True)
def reset_splitter_registry() -> None:
    SplitterFactory.clear_registry()
    yield
    SplitterFactory.clear_registry()


def _document(text: str) -> Document:
    return Document(
        id="doc_123",
        text=text,
        metadata={
            "source_path": "docs/a.pdf",
            "title": "A",
            "images": [
                {
                    "id": "img_a",
                    "path": "data/images/coll/img_a.png",
                    "page": 1,
                    "text_offset": 0,
                    "text_length": 14,
                    "position": {"x": 0, "y": 0},
                },
                {
                    "id": "img_b",
                    "path": "data/images/coll/img_b.png",
                    "page": 2,
                    "text_offset": 20,
                    "text_length": 14,
                    "position": {"x": 1, "y": 1},
                },
            ],
        },
    )


@pytest.mark.unit
def test_chunk_count_changes_with_splitter_configuration() -> None:
    SplitterFactory.register("fake", FakeSplitter)
    text = "abcdefghij"
    doc = _document(text)

    chunker_small = DocumentChunker(
        {"splitter": {"provider": "fake", "chunk_size": 3, "chunk_overlap": 0}}
    )
    chunker_large = DocumentChunker(
        {"splitter": {"provider": "fake", "chunk_size": 5, "chunk_overlap": 0}}
    )

    chunks_small = chunker_small.split_document(doc)
    chunks_large = chunker_large.split_document(doc)

    assert len(chunks_small) == 4
    assert len(chunks_large) == 2


@pytest.mark.unit
def test_chunk_ids_are_unique_and_deterministic() -> None:
    SplitterFactory.register("fake", FakeSplitter)
    settings = FakeSettings(
        splitter={"provider": "fake", "chunk_size": 4, "chunk_overlap": 0}
    )
    doc = _document("abcdefghij")
    chunker = DocumentChunker(settings)

    first = chunker.split_document(doc)
    second = chunker.split_document(doc)

    first_ids = [chunk.id for chunk in first]
    second_ids = [chunk.id for chunk in second]
    assert len(first_ids) == len(set(first_ids))
    assert first_ids == second_ids


@pytest.mark.unit
def test_chunk_metadata_inherits_document_metadata_and_source_ref() -> None:
    SplitterFactory.register("fake", FakeSplitter)
    chunker = DocumentChunker(
        {"splitter": {"provider": "fake", "chunk_size": 5, "chunk_overlap": 0}}
    )
    doc = _document("abcdefghij")

    chunks = chunker.split_document(doc)

    assert chunks[0].source_ref == doc.id
    assert chunks[0].metadata["source_path"] == "docs/a.pdf"
    assert chunks[0].metadata["title"] == "A"
    assert chunks[0].metadata["chunk_index"] == 0


@pytest.mark.unit
def test_chunk_image_distribution_uses_placeholder_subset() -> None:
    SplitterFactory.register("fake", FakeSplitter)
    chunker = DocumentChunker(
        {
            "splitter": {
                "provider": "fake",
                "chunk_size": 100,
                "chunk_overlap": 0,
                "precomputed_chunks": [
                    "alpha [IMAGE: img_a] beta",
                    "gamma delta",
                    "omega [IMAGE: img_b]",
                ],
            }
        }
    )
    doc = _document("alpha [IMAGE: img_a] beta gamma delta omega [IMAGE: img_b]")

    chunks = chunker.split_document(doc)

    assert chunks[0].metadata["image_refs"] == ["img_a"]
    assert [item["id"] for item in chunks[0].metadata["images"]] == ["img_a"]
    assert "images" not in chunks[1].metadata
    assert "image_refs" not in chunks[1].metadata
    assert chunks[2].metadata["image_refs"] == ["img_b"]
    assert [item["id"] for item in chunks[2].metadata["images"]] == ["img_b"]


@pytest.mark.unit
def test_chunk_output_conforms_to_chunk_contract() -> None:
    SplitterFactory.register("fake", FakeSplitter)
    chunker = DocumentChunker(
        {"splitter": {"provider": "fake", "chunk_size": 5, "chunk_overlap": 0}}
    )
    doc = _document("abcdefghij")

    chunks = chunker.split_document(doc)

    payload = chunks[0].to_dict()
    assert payload["id"]
    assert isinstance(payload["text"], str)
    assert isinstance(payload["metadata"], dict)
    assert isinstance(payload["start_offset"], int)
    assert isinstance(payload["end_offset"], int)
