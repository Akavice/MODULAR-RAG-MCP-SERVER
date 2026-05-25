"""Additional contract tests for DocumentChunker edge behavior."""

from __future__ import annotations

from typing import Any

import pytest

from core.types import Document
from ingestion.chunking.document_chunker import DocumentChunker
from libs.splitter.base_splitter import BaseSplitter
from libs.splitter.splitter_factory import SplitterFactory


class FakeSplitter(BaseSplitter):
    def split(self, text: str, trace: Any | None = None) -> list[str]:
        _ = trace
        self.validate_text(text)
        predefined = self.options.get("precomputed_chunks")
        if isinstance(predefined, list):
            return [str(item) for item in predefined]
        return [text]


class BadSplitter(BaseSplitter):
    def split(self, text: str, trace: Any | None = None) -> list[str]:  # type: ignore[override]
        _ = trace
        self.validate_text(text)
        return "not-a-list"  # type: ignore[return-value]


@pytest.fixture(autouse=True)
def reset_splitter_registry() -> None:
    SplitterFactory.clear_registry()
    yield
    SplitterFactory.clear_registry()


def _document(text: str) -> Document:
    return Document(id="doc_1", text=text, metadata={"source_path": "docs/a.pdf"})


@pytest.mark.unit
def test_split_document_rejects_non_document_input() -> None:
    SplitterFactory.register("fake", FakeSplitter)
    chunker = DocumentChunker({"splitter": {"provider": "fake"}})

    with pytest.raises(TypeError, match="document must be a Document"):
        chunker.split_document({"id": "x"})  # type: ignore[arg-type]


@pytest.mark.unit
def test_split_document_returns_empty_for_blank_text() -> None:
    SplitterFactory.register("fake", FakeSplitter)
    chunker = DocumentChunker({"splitter": {"provider": "fake"}})
    doc = _document("   \n")

    assert chunker.split_document(doc) == []


@pytest.mark.unit
def test_chunk_index_is_sequential_after_skipping_empty_chunks() -> None:
    SplitterFactory.register("fake", FakeSplitter)
    chunker = DocumentChunker(
        {
            "splitter": {
                "provider": "fake",
                "precomputed_chunks": ["first", "   ", "", "second"],
            }
        }
    )
    doc = _document("first second")

    chunks = chunker.split_document(doc)

    assert [c.metadata["chunk_index"] for c in chunks] == [0, 1]


@pytest.mark.unit
def test_split_document_rejects_non_list_splitter_output() -> None:
    SplitterFactory.register("bad", BadSplitter)
    chunker = DocumentChunker({"splitter": {"provider": "bad"}})
    doc = _document("abc")

    with pytest.raises(TypeError, match="splitter output"):
        chunker.split_document(doc)


@pytest.mark.unit
def test_offsets_are_monotonic_for_repeated_chunk_texts() -> None:
    SplitterFactory.register("fake", FakeSplitter)
    chunker = DocumentChunker(
        {
            "splitter": {
                "provider": "fake",
                "precomputed_chunks": ["abc", "abc", "abc"],
            }
        }
    )
    doc = _document("abc abc abc")

    chunks = chunker.split_document(doc)

    starts = [c.start_offset for c in chunks]
    assert starts == sorted(starts)
    assert starts == [0, 4, 8]


@pytest.mark.unit
def test_duplicate_image_placeholders_keep_refs_and_images_in_sync() -> None:
    SplitterFactory.register("fake", FakeSplitter)
    chunker = DocumentChunker(
        {
            "splitter": {
                "provider": "fake",
                "precomputed_chunks": ["x [IMAGE: img_a] y [IMAGE: img_a]"],
            }
        }
    )
    doc = Document(
        id="doc_dup",
        text="x [IMAGE: img_a] y [IMAGE: img_a]",
        metadata={
            "source_path": "docs/a.pdf",
            "images": [{"id": "img_a", "path": "data/images/a.png", "page": 1}],
        },
    )

    chunks = chunker.split_document(doc)

    assert chunks[0].metadata["image_refs"] == ["img_a", "img_a"]
    assert [item["id"] for item in chunks[0].metadata["images"]] == ["img_a", "img_a"]
