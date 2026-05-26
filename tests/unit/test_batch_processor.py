"""Unit tests for BatchProcessor orchestration."""

from __future__ import annotations

from typing import Any

import pytest

from core.types import Chunk, ChunkRecord
from ingestion.embedding.batch_processor import BatchProcessor


class FakeDenseEncoder:
    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    def encode(self, chunks: list[Chunk], trace: Any | None = None) -> list[ChunkRecord]:
        _ = trace
        self.calls.append([c.id for c in chunks])
        return [
            ChunkRecord(
                id=c.id,
                text=c.text,
                metadata=dict(c.metadata),
                dense_vector=[float(len(c.text)), 1.0],
                sparse_vector=None,
            )
            for c in chunks
        ]


class FakeSparseEncoder:
    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    def encode(self, chunks: list[Chunk], trace: Any | None = None) -> list[ChunkRecord]:
        _ = trace
        self.calls.append([c.id for c in chunks])
        return [
            ChunkRecord(
                id=c.id,
                text=c.text,
                metadata=dict(c.metadata),
                dense_vector=None,
                sparse_vector={"token": float(index + 1)},
            )
            for index, c in enumerate(chunks)
        ]


class WrongSizeDenseEncoder(FakeDenseEncoder):
    def encode(self, chunks: list[Chunk], trace: Any | None = None) -> list[ChunkRecord]:
        records = super().encode(chunks, trace=trace)
        return records[:-1]


class WrongIdSparseEncoder(FakeSparseEncoder):
    def encode(self, chunks: list[Chunk], trace: Any | None = None) -> list[ChunkRecord]:
        records = super().encode(chunks, trace=trace)
        if records:
            records[0] = ChunkRecord(
                id="wrong-id",
                text=records[0].text,
                metadata=records[0].metadata,
                dense_vector=None,
                sparse_vector=records[0].sparse_vector,
            )
        return records


class TraceStub:
    def __init__(self) -> None:
        self.events: list[tuple[str, dict[str, Any]]] = []

    def record_stage(self, stage: str, **payload: Any) -> None:
        self.events.append((stage, payload))


def _chunk(text: str, idx: int) -> Chunk:
    return Chunk(
        id=f"chunk-{idx}",
        text=text,
        metadata={"source_path": "docs/a.pdf"},
        start_offset=0,
        end_offset=len(text),
        source_ref="doc-1",
    )


@pytest.mark.unit
def test_process_batches_and_merges_dense_sparse_vectors() -> None:
    dense = FakeDenseEncoder()
    sparse = FakeSparseEncoder()
    processor = BatchProcessor(
        settings={"ingestion": {"batch_processor": {"batch_size": 2}}},
        dense_encoder=dense,
        sparse_encoder=sparse,
    )
    chunks = [_chunk("a", 0), _chunk("bb", 1), _chunk("ccc", 2)]

    records = processor.process(chunks)

    assert len(records) == 3
    assert records[0].dense_vector == [1.0, 1.0]
    assert records[0].sparse_vector == {"token": 1.0}
    assert len(dense.calls) == 2
    assert len(sparse.calls) == 2


@pytest.mark.unit
def test_process_can_disable_sparse_path() -> None:
    dense = FakeDenseEncoder()
    sparse = FakeSparseEncoder()
    processor = BatchProcessor(
        settings={"ingestion": {"batch_processor": {"batch_size": 2, "enable_sparse": False}}},
        dense_encoder=dense,
        sparse_encoder=sparse,
    )

    records = processor.process([_chunk("x", 0), _chunk("y", 1)])

    assert all(r.dense_vector is not None for r in records)
    assert all(r.sparse_vector is None for r in records)
    assert len(dense.calls) == 1
    assert len(sparse.calls) == 0


@pytest.mark.unit
def test_process_can_disable_dense_path() -> None:
    dense = FakeDenseEncoder()
    sparse = FakeSparseEncoder()
    processor = BatchProcessor(
        settings={"ingestion": {"batch_processor": {"batch_size": 2, "enable_dense": False}}},
        dense_encoder=dense,
        sparse_encoder=sparse,
    )

    records = processor.process([_chunk("x", 0), _chunk("y", 1)])

    assert all(r.dense_vector is None for r in records)
    assert all(r.sparse_vector is not None for r in records)
    assert len(dense.calls) == 0
    assert len(sparse.calls) == 1


@pytest.mark.unit
def test_process_rejects_when_both_paths_disabled() -> None:
    processor = BatchProcessor(
        settings={
            "ingestion": {
                "batch_processor": {"enable_dense": False, "enable_sparse": False}
            }
        },
        dense_encoder=FakeDenseEncoder(),
        sparse_encoder=FakeSparseEncoder(),
    )

    with pytest.raises(ValueError, match="at least one of dense/sparse"):
        processor.process([_chunk("x", 0)])


@pytest.mark.unit
def test_process_rejects_encoder_size_mismatch() -> None:
    processor = BatchProcessor(
        settings={"ingestion": {"batch_processor": {"batch_size": 4}}},
        dense_encoder=WrongSizeDenseEncoder(),
        sparse_encoder=FakeSparseEncoder(),
    )

    with pytest.raises(ValueError, match="dense encoder output size"):
        processor.process([_chunk("a", 0), _chunk("b", 1)])


@pytest.mark.unit
def test_process_rejects_encoder_id_mismatch() -> None:
    processor = BatchProcessor(
        settings={"ingestion": {"batch_processor": {"batch_size": 4}}},
        dense_encoder=FakeDenseEncoder(),
        sparse_encoder=WrongIdSparseEncoder(),
    )

    with pytest.raises(ValueError, match="sparse encoder output id mismatch"):
        processor.process([_chunk("a", 0)])


@pytest.mark.unit
def test_trace_records_batch_and_summary_events() -> None:
    trace = TraceStub()
    processor = BatchProcessor(
        settings={"ingestion": {"batch_processor": {"batch_size": 2}}},
        dense_encoder=FakeDenseEncoder(),
        sparse_encoder=FakeSparseEncoder(),
    )

    processor.process([_chunk("a", 0), _chunk("bb", 1), _chunk("ccc", 2)], trace=trace)

    stages = [name for name, _ in trace.events]
    assert "embed_batch_processor_batch" in stages
    assert stages[-1] == "embed_batch_processor"
    assert trace.events[-1][1]["chunk_count"] == 3
    assert trace.events[-1][1]["batch_count"] == 2


@pytest.mark.unit
def test_empty_input_returns_empty_and_records_summary() -> None:
    trace = TraceStub()
    processor = BatchProcessor(
        settings={},
        dense_encoder=FakeDenseEncoder(),
        sparse_encoder=FakeSparseEncoder(),
    )

    records = processor.process([], trace=trace)

    assert records == []
    assert trace.events[-1][0] == "embed_batch_processor"
    assert trace.events[-1][1]["chunk_count"] == 0


@pytest.mark.unit
def test_init_does_not_require_dense_encoder_when_dense_disabled() -> None:
    processor = BatchProcessor(
        settings={
            "ingestion": {"batch_processor": {"enable_dense": False, "enable_sparse": True}},
        },
        dense_encoder=None,
        sparse_encoder=FakeSparseEncoder(),
    )

    records = processor.process([_chunk("x", 0)])

    assert len(records) == 1
    assert records[0].dense_vector is None
    assert records[0].sparse_vector is not None
