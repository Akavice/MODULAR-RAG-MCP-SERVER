"""Unit tests for DenseEncoder."""

from __future__ import annotations

from typing import Any

import pytest

from core.types import Chunk
from ingestion.embedding.dense_encoder import DenseEncoder
from libs.embedding.base_embedding import BaseEmbedding


class FakeEmbedding(BaseEmbedding):
    def __init__(self, *, vectors: list[list[float]] | None = None, **options: Any) -> None:
        super().__init__(**options)
        self.vectors = vectors
        self.calls: list[list[str]] = []

    def embed(self, texts: list[str], trace: Any | None = None) -> list[list[float]]:
        _ = trace
        self.calls.append(list(texts))
        if self.vectors is not None:
            return [list(item) for item in self.vectors]
        return [[float(len(text)), 1.0] for text in texts]


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
def test_encode_builds_chunk_records_with_dense_vectors() -> None:
    encoder = DenseEncoder(settings={}, embedding_client=FakeEmbedding(), batch_size=4)
    chunks = [_chunk("alpha", 0), _chunk("beta", 1)]

    records = encoder.encode(chunks)

    assert len(records) == 2
    assert records[0].id == "chunk-0"
    assert records[0].dense_vector == [5.0, 1.0]
    assert records[1].dense_vector == [4.0, 1.0]
    assert records[0].metadata["source_path"] == "docs/a.pdf"


@pytest.mark.unit
def test_encode_uses_batching() -> None:
    fake = FakeEmbedding()
    encoder = DenseEncoder(settings={}, embedding_client=fake, batch_size=2)
    chunks = [_chunk("a", 0), _chunk("bb", 1), _chunk("ccc", 2), _chunk("dddd", 3), _chunk("eeeee", 4)]

    encoder.encode(chunks)

    assert len(fake.calls) == 3
    assert fake.calls[0] == ["a", "bb"]
    assert fake.calls[1] == ["ccc", "dddd"]
    assert fake.calls[2] == ["eeeee"]


@pytest.mark.unit
def test_encode_returns_empty_for_empty_chunks() -> None:
    fake = FakeEmbedding()
    encoder = DenseEncoder(settings={}, embedding_client=fake)
    trace = TraceStub()

    records = encoder.encode([], trace=trace)

    assert records == []
    assert fake.calls == []
    assert trace.events[-1][0] == "embed_dense_encoder"
    assert trace.events[-1][1]["chunk_count"] == 0


@pytest.mark.unit
def test_encode_rejects_non_chunk_items() -> None:
    encoder = DenseEncoder(settings={}, embedding_client=FakeEmbedding())

    with pytest.raises(TypeError, match="must be a Chunk"):
        encoder.encode([{"id": "x"}])  # type: ignore[list-item]


@pytest.mark.unit
def test_encode_rejects_embedding_count_mismatch() -> None:
    fake = FakeEmbedding(vectors=[[1.0, 2.0]])
    encoder = DenseEncoder(settings={}, embedding_client=fake, batch_size=8)
    chunks = [_chunk("x", 0), _chunk("y", 1)]

    with pytest.raises(ValueError, match="output size must match"):
        encoder.encode(chunks)


@pytest.mark.unit
def test_trace_stage_reports_batch_and_vector_dim() -> None:
    encoder = DenseEncoder(settings={}, embedding_client=FakeEmbedding(), batch_size=2)
    trace = TraceStub()

    encoder.encode([_chunk("x", 0), _chunk("yy", 1), _chunk("zzz", 2)], trace=trace)
    stage, payload = trace.events[-1]

    assert stage == "embed_dense_encoder"
    assert payload["chunk_count"] == 3
    assert payload["batch_count"] == 2
    assert payload["batch_size"] == 2
    assert payload["vector_dim"] == 2


@pytest.mark.unit
def test_batch_size_can_be_loaded_from_settings() -> None:
    encoder = DenseEncoder(
        settings={"ingestion": {"dense_encoder": {"batch_size": 7}}},
        embedding_client=FakeEmbedding(),
    )
    assert encoder.batch_size == 7
