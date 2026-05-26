"""Extra contract/integration coverage for HybridSearch (D5)."""

from __future__ import annotations

from typing import Any

import pytest

from core.query_engine.hybrid_search import HybridSearch
from core.query_engine.query_processor import ProcessedQuery
from core.types import RetrievalResult


def _r(chunk_id: str, score: float, **metadata: Any) -> RetrievalResult:
    payload = {"source_path": f"docs/{chunk_id}.pdf"}
    payload.update(metadata)
    return RetrievalResult(chunk_id=chunk_id, score=score, text=f"text-{chunk_id}", metadata=payload)


class _QP:
    def process(self, query: str, filters: dict[str, Any] | None = None) -> ProcessedQuery:
        _ = query
        return ProcessedQuery(query="normalized q", keywords=["k1"], filters=dict(filters or {}))


class _Dense:
    def __init__(self, rows: list[RetrievalResult]) -> None:
        self.rows = rows

    def retrieve(
        self, query: str, top_k: int | None = None, filters: dict[str, Any] | None = None, trace: Any | None = None
    ) -> list[RetrievalResult]:
        _ = (query, top_k, filters, trace)
        return list(self.rows)


class _Sparse:
    def __init__(self, rows: list[RetrievalResult]) -> None:
        self.rows = rows

    def retrieve(self, keywords: list[str], top_k: int | None = None, trace: Any | None = None) -> list[RetrievalResult]:
        _ = (keywords, top_k, trace)
        return list(self.rows)


class _FusionPassthrough:
    def fuse(
        self,
        dense_results: list[RetrievalResult],
        sparse_results: list[RetrievalResult],
        top_k: int | None = None,
        trace: Any | None = None,
    ) -> list[RetrievalResult]:
        _ = trace
        merged = dense_results + sparse_results
        return merged[: (top_k or len(merged))]


class _FusionAlwaysFail:
    def fuse(
        self,
        dense_results: list[RetrievalResult],
        sparse_results: list[RetrievalResult],
        top_k: int | None = None,
        trace: Any | None = None,
    ) -> list[RetrievalResult]:
        _ = (dense_results, sparse_results, top_k, trace)
        raise RuntimeError("fusion down")


class _Trace:
    def __init__(self) -> None:
        self.events: list[tuple[str, dict[str, Any]]] = []

    def record_stage(self, stage: str, **payload: Any) -> None:
        self.events.append((stage, payload))


@pytest.mark.integration
def test_hybrid_search_applies_filters_before_final_top_k_trim() -> None:
    dense = _Dense([_r("a", 1.0, created_at="2026-01-01", collection="kb"), _r("b", 0.9, created_at="2024-01-01", collection="kb")])
    sparse = _Sparse([_r("c", 1.1, created_at="2026-06-01", collection="kb"), _r("d", 0.8, collection="kb")])
    search = HybridSearch(
        settings={"retrieval": {"top_k": 10}},
        query_processor=_QP(),  # type: ignore[arg-type]
        dense_retriever=dense,  # type: ignore[arg-type]
        sparse_retriever=sparse,  # type: ignore[arg-type]
        fusion=_FusionPassthrough(),  # type: ignore[arg-type]
    )

    out = search.search(
        "q",
        top_k=2,
        filters={"collection": "kb", "time_range": {"from": "2025-01-01", "to": "2026-12-31"}},
    )

    # Expected: filter first => ["a", "c"], then top_k=2 keeps both.
    # Current implementation trims in fusion first and may drop "c" early.
    assert [x.chunk_id for x in out] == ["a", "c"]


@pytest.mark.integration
def test_hybrid_search_records_stage_trace() -> None:
    trace = _Trace()
    search = HybridSearch(
        settings={"retrieval": {"top_k": 3}},
        query_processor=_QP(),  # type: ignore[arg-type]
        dense_retriever=_Dense([_r("a", 1.0, collection="kb")]),  # type: ignore[arg-type]
        sparse_retriever=_Sparse([_r("s", 1.0, collection="kb")]),  # type: ignore[arg-type]
        fusion=_FusionPassthrough(),  # type: ignore[arg-type]
    )

    out = search.search("q", filters={"collection": "kb"}, trace=trace)

    assert len(out) == 2
    assert len(trace.events) >= 1
    stage, payload = trace.events[-1]
    assert stage == "hybrid_search"
    assert payload["dense_failed"] is False
    assert payload["sparse_failed"] is False
    assert payload["result_count"] == 2


@pytest.mark.integration
def test_hybrid_search_when_fusion_fails_with_two_nonempty_channels_raises() -> None:
    search = HybridSearch(
        settings={},
        query_processor=_QP(),  # type: ignore[arg-type]
        dense_retriever=_Dense([_r("d", 1.0)]),  # type: ignore[arg-type]
        sparse_retriever=_Sparse([_r("s", 1.0)]),  # type: ignore[arg-type]
        fusion=_FusionAlwaysFail(),  # type: ignore[arg-type]
    )

    with pytest.raises(RuntimeError, match="fusion down"):
        search.search("q")


@pytest.mark.integration
def test_hybrid_search_rejects_invalid_inputs() -> None:
    with pytest.raises(TypeError, match="top_k must be an integer"):
        HybridSearch(
            settings={"retrieval": {"top_k": "3"}},
            query_processor=_QP(),  # type: ignore[arg-type]
            dense_retriever=_Dense([]),  # type: ignore[arg-type]
            sparse_retriever=_Sparse([]),  # type: ignore[arg-type]
            fusion=_FusionPassthrough(),  # type: ignore[arg-type]
        )

    with pytest.raises(ValueError, match="top_k must be greater than 0"):
        HybridSearch(
            settings={"retrieval": {"top_k": 0}},
            query_processor=_QP(),  # type: ignore[arg-type]
            dense_retriever=_Dense([]),  # type: ignore[arg-type]
            sparse_retriever=_Sparse([]),  # type: ignore[arg-type]
            fusion=_FusionPassthrough(),  # type: ignore[arg-type]
        )

    search = HybridSearch(
        settings={},
        query_processor=_QP(),  # type: ignore[arg-type]
        dense_retriever=_Dense([]),  # type: ignore[arg-type]
        sparse_retriever=_Sparse([]),  # type: ignore[arg-type]
        fusion=_FusionPassthrough(),  # type: ignore[arg-type]
    )
    with pytest.raises(TypeError, match="top_k must be an integer"):
        search.search("q", top_k="2")  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="filters must be a mapping"):
        search.search("q", filters=["bad"])  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="filters keys must be non-empty strings"):
        search.search("q", filters={"   ": 1})
