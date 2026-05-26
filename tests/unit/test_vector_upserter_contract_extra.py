"""Additional contract tests for VectorUpserter behavior."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import pytest

from core.types import ChunkRecord
from ingestion.storage.vector_upserter import VectorUpserter
from libs.vector_store.base_vector_store import BaseVectorStore, QueryMatch


class FakeVectorStore(BaseVectorStore):
    def __init__(self, *, collection_name: str = "test-coll", **options: Any) -> None:
        super().__init__(collection_name=collection_name, **options)
        self.calls: list[list[dict[str, Any]]] = []
        self.return_count = 0

    def upsert(self, records: list[dict[str, Any]], trace: Any | None = None) -> int:
        _ = trace
        self.calls.append([dict(item) for item in records])
        self.return_count = len(records)
        return self.return_count

    def query(
        self,
        vector: list[float],
        top_k: int = 5,
        filters: Mapping[str, Any] | None = None,
        trace: Any | None = None,
    ) -> list[QueryMatch]:
        _ = vector, top_k, filters, trace
        return []


class TraceStub:
    def __init__(self) -> None:
        self.events: list[tuple[str, dict[str, Any]]] = []

    def record_stage(self, stage: str, **payload: Any) -> None:
        self.events.append((stage, payload))


def _record(chunk_id: str, text: str, vector: list[float]) -> ChunkRecord:
    return ChunkRecord(
        id=chunk_id,
        text=text,
        metadata={"source_path": "docs/a.pdf"},
        dense_vector=vector,
        sparse_vector=None,
    )


@pytest.mark.unit
def test_upsert_keeps_unique_id_order_and_last_duplicate_value() -> None:
    store = FakeVectorStore()
    upserter = VectorUpserter(settings={}, vector_store=store)

    upserter.upsert(
        [
            _record("c1", "v1", [1.0, 0.0]),
            _record("c2", "b", [0.0, 1.0]),
            _record("c1", "v2", [2.0, 0.0]),
            _record("c3", "c", [0.5, 0.5]),
        ]
    )

    payload = store.calls[-1]
    assert [item["id"] for item in payload] == ["c1", "c2", "c3"]
    assert payload[0]["text"] == "v2"
    assert payload[0]["vector"] == [2.0, 0.0]


@pytest.mark.unit
def test_trace_reports_vector_store_return_count_and_collection_name() -> None:
    store = FakeVectorStore(collection_name="kb-prod")
    upserter = VectorUpserter(settings={}, vector_store=store)
    trace = TraceStub()

    result = upserter.upsert([_record("c1", "x", [1.0])], trace=trace)

    assert result == 1
    stage, payload = trace.events[-1]
    assert stage == "storage_vector_upserter"
    assert payload["upserted_count"] == 1
    assert payload["collection_name"] == "kb-prod"

