"""Unit tests for SparseEncoder."""

from __future__ import annotations

from typing import Any

import pytest

from core.types import Chunk
from ingestion.embedding.sparse_encoder import SparseEncoder


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
def test_encode_outputs_chunk_records_with_sparse_vectors() -> None:
    encoder = SparseEncoder(settings={})
    chunks = [_chunk("RAG retrieval with BM25", 0), _chunk("RAG pipeline tuning", 1)]

    records = encoder.encode(chunks)

    assert len(records) == 2
    assert records[0].id == "chunk-0"
    assert isinstance(records[0].sparse_vector, dict)
    assert records[0].sparse_vector
    assert records[0].dense_vector is None


@pytest.mark.unit
def test_unique_term_has_higher_weight_than_shared_term() -> None:
    encoder = SparseEncoder(settings={})
    chunks = [
        _chunk("alpha shared", 0),
        _chunk("beta shared", 1),
        _chunk("gamma shared", 2),
    ]

    records = encoder.encode(chunks)
    vector = records[0].sparse_vector or {}

    assert "alpha" in vector
    assert "shared" in vector
    assert vector["alpha"] > vector["shared"]


@pytest.mark.unit
def test_stopwords_are_filtered_by_default() -> None:
    encoder = SparseEncoder(settings={})
    record = encoder.encode([_chunk("the system and the pipeline", 0)])[0]
    vector = record.sparse_vector or {}

    assert "the" not in vector
    assert "and" not in vector
    assert "system" in vector


@pytest.mark.unit
def test_encode_returns_empty_for_empty_input_and_records_trace() -> None:
    encoder = SparseEncoder(settings={})
    trace = TraceStub()

    records = encoder.encode([], trace=trace)

    assert records == []
    assert trace.events[-1][0] == "embed_sparse_encoder"
    assert trace.events[-1][1]["chunk_count"] == 0


@pytest.mark.unit
def test_encode_rejects_non_chunk_items() -> None:
    encoder = SparseEncoder(settings={})

    with pytest.raises(TypeError, match="must be a Chunk"):
        encoder.encode([{"id": "x"}])  # type: ignore[list-item]


@pytest.mark.unit
def test_trace_stage_reports_vocab_and_avg_len() -> None:
    encoder = SparseEncoder(settings={})
    trace = TraceStub()

    encoder.encode([_chunk("alpha beta", 0), _chunk("beta gamma", 1)], trace=trace)
    stage, payload = trace.events[-1]

    assert stage == "embed_sparse_encoder"
    assert payload["chunk_count"] == 2
    assert payload["vocab_size"] >= 3
    assert payload["avg_doc_len"] > 0


@pytest.mark.unit
def test_settings_override_is_applied() -> None:
    encoder = SparseEncoder(
        settings={
            "ingestion": {
                "sparse_encoder": {
                    "k1": 1.8,
                    "b": 0.6,
                    "min_token_length": 3,
                    "remove_stopwords": False,
                }
            }
        }
    )

    assert encoder.k1 == 1.8
    assert encoder.b == 0.6
    assert encoder.min_token_length == 3
    assert encoder.remove_stopwords is False
