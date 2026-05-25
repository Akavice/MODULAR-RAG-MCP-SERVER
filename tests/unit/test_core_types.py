"""Unit tests for core shared data contracts."""

from __future__ import annotations

import json

import pytest

from core.types import (
    IMAGE_PLACEHOLDER_TEMPLATE,
    Chunk,
    ChunkRecord,
    Document,
    make_image_placeholder,
)


def _metadata() -> dict[str, object]:
    return {
        "source_path": "docs/sample.pdf",
        "collection": "knowledge",
        "images": [
            {
                "id": "dochash_1_0",
                "path": "data/images/knowledge/dochash_1_0.png",
                "page": 1,
                "text_offset": 15,
                "text_length": 21,
                "position": {"x": 10, "y": 20, "w": 80, "h": 60},
            }
        ],
    }


@pytest.mark.unit
def test_document_to_dict_from_dict_roundtrip_is_json_serializable() -> None:
    document = Document(
        id="doc-1",
        text="hello\n[IMAGE: dochash_1_0]",
        metadata=_metadata(),
    )

    payload = document.to_dict()
    encoded = json.dumps(payload)
    decoded = json.loads(encoded)
    restored = Document.from_dict(decoded)

    assert restored.to_dict() == payload


@pytest.mark.unit
def test_document_requires_metadata_source_path() -> None:
    with pytest.raises(ValueError, match="metadata.source_path"):
        Document(id="doc-1", text="hello", metadata={})


@pytest.mark.unit
def test_document_rejects_invalid_images_schema() -> None:
    with pytest.raises(ValueError, match=r"metadata.images\[0\]\.id"):
        Document(
            id="doc-1",
            text="hello",
            metadata={"source_path": "a.pdf", "images": [{"path": "x.png"}]},
        )


@pytest.mark.unit
def test_chunk_serialization_with_source_ref() -> None:
    chunk = Chunk(
        id="chunk-1",
        text="chunk text",
        metadata=_metadata(),
        start_offset=10,
        end_offset=42,
        source_ref="doc-1",
    )

    restored = Chunk.from_dict(chunk.to_dict())

    assert restored.to_dict() == chunk.to_dict()


@pytest.mark.unit
def test_chunk_rejects_invalid_offsets() -> None:
    with pytest.raises(ValueError, match="end_offset"):
        Chunk(
            id="chunk-1",
            text="chunk text",
            metadata=_metadata(),
            start_offset=8,
            end_offset=5,
        )


@pytest.mark.unit
def test_chunk_record_roundtrip_and_optional_vectors() -> None:
    record = ChunkRecord(
        id="record-1",
        text="chunk text",
        metadata=_metadata(),
        dense_vector=[0.1, 0.2, 0.3],
        sparse_vector={"token_a": 1.2, "token_b": 0.7},
    )

    restored = ChunkRecord.from_dict(record.to_dict())

    assert restored.to_dict() == record.to_dict()


@pytest.mark.unit
def test_chunk_record_rejects_non_finite_dense_vector() -> None:
    with pytest.raises(ValueError, match="dense_vector\\[0\\]"):
        ChunkRecord(
            id="record-1",
            text="chunk text",
            metadata=_metadata(),
            dense_vector=[float("nan")],
        )


@pytest.mark.unit
def test_make_image_placeholder_uses_spec_format() -> None:
    image_id = "doc_hash_2_1"

    placeholder = make_image_placeholder(image_id)

    assert placeholder == "[IMAGE: doc_hash_2_1]"
    assert placeholder == IMAGE_PLACEHOLDER_TEMPLATE.format(image_id=image_id)
