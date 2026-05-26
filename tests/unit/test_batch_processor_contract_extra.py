"""Extra contract tests for BatchProcessor initialization and config behavior."""

from __future__ import annotations

from typing import Any

import pytest

from core.types import Chunk, ChunkRecord
from ingestion.embedding.batch_processor import BatchProcessor


class FakeDenseEncoder:
    def encode(self, chunks: list[Chunk], trace: Any | None = None) -> list[ChunkRecord]:
        _ = trace
        return [
            ChunkRecord(
                id=c.id,
                text=c.text,
                metadata=dict(c.metadata),
                dense_vector=[1.0],
                sparse_vector=None,
            )
            for c in chunks
        ]


class FakeSparseEncoder:
    def encode(self, chunks: list[Chunk], trace: Any | None = None) -> list[ChunkRecord]:
        _ = trace
        return [
            ChunkRecord(
                id=c.id,
                text=c.text,
                metadata=dict(c.metadata),
                dense_vector=None,
                sparse_vector={"t": 1.0},
            )
            for c in chunks
        ]


def _chunk(idx: int) -> Chunk:
    text = f"chunk-{idx}"
    return Chunk(
        id=f"chunk-{idx}",
        text=text,
        metadata={"source_path": "docs/a.pdf"},
        start_offset=0,
        end_offset=len(text),
        source_ref="doc-1",
    )


@pytest.mark.unit
def test_init_does_not_require_sparse_encoder_when_sparse_disabled() -> None:
    processor = BatchProcessor(
        settings={"ingestion": {"batch_processor": {"enable_dense": True, "enable_sparse": False}}},
        dense_encoder=FakeDenseEncoder(),
        sparse_encoder=None,
    )

    records = processor.process([_chunk(0), _chunk(1)])

    assert len(records) == 2
    assert all(r.dense_vector is not None for r in records)
    assert all(r.sparse_vector is None for r in records)


@pytest.mark.unit
def test_init_rejects_invalid_batch_size_from_settings() -> None:
    with pytest.raises(TypeError, match="batch_size must be an integer"):
        BatchProcessor(
            settings={"ingestion": {"batch_processor": {"batch_size": "32"}}},
            dense_encoder=FakeDenseEncoder(),
            sparse_encoder=FakeSparseEncoder(),
        )

