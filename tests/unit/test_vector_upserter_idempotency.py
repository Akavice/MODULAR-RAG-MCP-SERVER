"""Unit tests for VectorUpserter idempotency behavior."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import pytest

from core.types import ChunkRecord
from ingestion.storage.vector_upserter import VectorUpserter
from libs.vector_store.base_vector_store import BaseVectorStore, QueryMatch


class FakeVectorStore(BaseVectorStore):
    def __init__(self, *, collection_name: str = "default", **options: Any) -> None:
        super().__init__(collection_name=collection_name, **options)
        self._records: dict[str, dict[str, Any]] = {}
        self.calls: list[list[dict[str, Any]]] = []

    def upsert(self, records: list[dict[str, Any]], trace: Any | None = None) -> int:
        _ = trace
        self.calls.append([dict(item) for item in records])
        self.validate_records(records)
        for record in records:
            self._records[record["id"]] = {
                "id": record["id"],
                "vector": list(record["vector"]),
                "text": record.get("text", ""),
                "metadata": dict(record.get("metadata", {})),
            }
        return len(records)

    def query(
        self,
        vector: list[float],
        top_k: int = 5,
        filters: Mapping[str, Any] | None = None,
        trace: Any | None = None,
    ) -> list[QueryMatch]:
        _ = vector, top_k, filters, trace
        return []

    @property
    def record_count(self) -> int:
        return len(self._records)


class TraceStub:
    def __init__(self) -> None:
        self.events: list[tuple[str, dict[str, Any]]] = []

    def record_stage(self, stage: str, **payload: Any) -> None:
        self.events.append((stage, payload))


def _record(chunk_id: str, text: str, source: str, vector: list[float]) -> ChunkRecord:
    return ChunkRecord(
        id=chunk_id,
        text=text,
        metadata={"source_path": source},
        dense_vector=vector,
        sparse_vector=None,
    )


@pytest.mark.unit
def test_upsert_idempotent_for_repeated_calls_with_same_ids() -> None:
    store = FakeVectorStore()
    upserter = VectorUpserter(settings={}, vector_store=store)
    payload = [
        _record("c1", "alpha", "docs/a.pdf", [1.0, 0.0]),
        _record("c2", "beta", "docs/a.pdf", [0.0, 1.0]),
    ]

    first = upserter.upsert(payload)
    second = upserter.upsert(payload)

    assert first == 2
    assert second == 2
    assert store.record_count == 2


@pytest.mark.unit
def test_upsert_deduplicates_duplicate_ids_within_single_call() -> None:
    store = FakeVectorStore()
    upserter = VectorUpserter(settings={}, vector_store=store)
    payload = [
        _record("c1", "alpha-v1", "docs/a.pdf", [1.0, 0.0]),
        _record("c1", "alpha-v2", "docs/a.pdf", [2.0, 0.0]),
        _record("c2", "beta", "docs/a.pdf", [0.0, 1.0]),
    ]

    count = upserter.upsert(payload)

    assert count == 2
    assert store.record_count == 2
    # Keep last duplicate payload for same id.
    assert store._records["c1"]["text"] == "alpha-v2"


@pytest.mark.unit
def test_upsert_rejects_missing_dense_vector() -> None:
    store = FakeVectorStore()
    upserter = VectorUpserter(settings={}, vector_store=store)
    bad = ChunkRecord(
        id="c1",
        text="x",
        metadata={"source_path": "docs/a.pdf"},
        dense_vector=None,
        sparse_vector={"x": 1.0},
    )

    with pytest.raises(ValueError, match="missing dense_vector"):
        upserter.upsert([bad])


@pytest.mark.unit
def test_upsert_validates_record_type_and_empty_input() -> None:
    upserter = VectorUpserter(settings={}, vector_store=FakeVectorStore())
    trace = TraceStub()

    assert upserter.upsert([], trace=trace) == 0
    assert trace.events[-1][0] == "storage_vector_upserter"
    assert trace.events[-1][1]["input_count"] == 0

    with pytest.raises(TypeError, match="ChunkRecord"):
        upserter.upsert([{"id": "x"}])  # type: ignore[list-item]


@pytest.mark.unit
def test_trace_reports_input_unique_and_upsert_counts() -> None:
    store = FakeVectorStore()
    upserter = VectorUpserter(settings={}, vector_store=store)
    trace = TraceStub()

    upserter.upsert(
        [
            _record("c1", "alpha", "docs/a.pdf", [1.0, 0.0]),
            _record("c1", "alpha2", "docs/a.pdf", [2.0, 0.0]),
            _record("c2", "beta", "docs/a.pdf", [0.0, 1.0]),
        ],
        trace=trace,
    )

    stage, payload = trace.events[-1]
    assert stage == "storage_vector_upserter"
    assert payload["input_count"] == 3
    assert payload["unique_count"] == 2
    assert payload["upserted_count"] == 2
