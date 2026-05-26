"""Integration tests for HybridSearch orchestration behavior."""

from __future__ import annotations

from typing import Any

import pytest

from core.query_engine.hybrid_search import HybridSearch
from core.query_engine.query_processor import ProcessedQuery
from core.types import RetrievalResult


def _r(chunk_id: str, score: float, text: str, **metadata: Any) -> RetrievalResult:
    payload = {"source_path": f"docs/{chunk_id}.pdf"}
    payload.update(metadata)
    return RetrievalResult(chunk_id=chunk_id, score=score, text=text, metadata=payload)


class FakeQueryProcessor:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any] | None]] = []

    def process(self, query: str, filters: dict[str, Any] | None = None) -> ProcessedQuery:
        self.calls.append((query, filters))
        return ProcessedQuery(
            query=query.strip(),
            keywords=["rag", "retrieval"],
            filters=dict(filters or {}),
        )


class FakeDenseRetriever:
    def __init__(self, *, explode: bool = False) -> None:
        self.explode = explode
        self.calls: list[dict[str, Any]] = []

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
        filters: dict[str, Any] | None = None,
        trace: Any | None = None,
    ) -> list[RetrievalResult]:
        _ = trace
        self.calls.append({"query": query, "top_k": top_k, "filters": filters})
        if self.explode:
            raise RuntimeError("dense unavailable")
        return [
            _r("d1", 0.9, "dense-a", collection="kb", doc_type="pdf"),
            _r("d2", 0.7, "dense-b", collection="other", doc_type="md"),
        ]


class FakeSparseRetriever:
    def __init__(self, *, explode: bool = False) -> None:
        self.explode = explode
        self.calls: list[dict[str, Any]] = []

    def retrieve(
        self,
        keywords: list[str],
        top_k: int | None = None,
        trace: Any | None = None,
    ) -> list[RetrievalResult]:
        _ = trace
        self.calls.append({"keywords": list(keywords), "top_k": top_k})
        if self.explode:
            raise RuntimeError("sparse unavailable")
        return [
            _r("s1", 2.0, "sparse-a", collection="kb", doc_type="pdf"),
            _r("d2", 1.8, "sparse-b", collection="other", doc_type="md"),
        ]


class FakeFusion:
    def __init__(self, *, explode: bool = False) -> None:
        self.explode = explode
        self.calls: list[dict[str, Any]] = []

    def fuse(
        self,
        dense_results: list[RetrievalResult],
        sparse_results: list[RetrievalResult],
        top_k: int | None = None,
        trace: Any | None = None,
    ) -> list[RetrievalResult]:
        _ = trace
        self.calls.append(
            {
                "dense_count": len(dense_results),
                "sparse_count": len(sparse_results),
                "top_k": top_k,
            }
        )
        if self.explode:
            raise RuntimeError("fusion failed")
        seen: set[str] = set()
        merged: list[RetrievalResult] = []
        for item in dense_results + sparse_results:
            if item.chunk_id in seen:
                continue
            seen.add(item.chunk_id)
            merged.append(item)
        return merged[: (top_k or len(merged))]


@pytest.mark.integration
def test_search_runs_full_pipeline_and_applies_metadata_filters() -> None:
    qp = FakeQueryProcessor()
    dense = FakeDenseRetriever()
    sparse = FakeSparseRetriever()
    fusion = FakeFusion()
    searcher = HybridSearch(
        settings={"retrieval": {"top_k": 5}},
        query_processor=qp,  # type: ignore[arg-type]
        dense_retriever=dense,  # type: ignore[arg-type]
        sparse_retriever=sparse,  # type: ignore[arg-type]
        fusion=fusion,  # type: ignore[arg-type]
    )

    results = searcher.search("  rag retrieval  ", top_k=3, filters={"collection": "kb"})

    assert qp.calls[-1] == ("  rag retrieval  ", {"collection": "kb"})
    assert dense.calls[-1]["query"] == "rag retrieval"
    assert dense.calls[-1]["filters"] == {"collection": "kb"}
    assert sparse.calls[-1]["keywords"] == ["rag", "retrieval"]
    assert fusion.calls[-1]["top_k"] == 4
    assert [item.chunk_id for item in results] == ["d1", "s1"]
    assert all(item.metadata["collection"] == "kb" for item in results)


@pytest.mark.integration
def test_search_falls_back_to_sparse_when_dense_fails() -> None:
    searcher = HybridSearch(
        settings={},
        query_processor=FakeQueryProcessor(),  # type: ignore[arg-type]
        dense_retriever=FakeDenseRetriever(explode=True),  # type: ignore[arg-type]
        sparse_retriever=FakeSparseRetriever(),  # type: ignore[arg-type]
        fusion=FakeFusion(),
    )

    results = searcher.search("q")

    assert results
    assert any(item.chunk_id.startswith("s") for item in results)


@pytest.mark.integration
def test_search_raises_when_both_dense_and_sparse_fail() -> None:
    searcher = HybridSearch(
        settings={},
        query_processor=FakeQueryProcessor(),  # type: ignore[arg-type]
        dense_retriever=FakeDenseRetriever(explode=True),  # type: ignore[arg-type]
        sparse_retriever=FakeSparseRetriever(explode=True),  # type: ignore[arg-type]
        fusion=FakeFusion(),
    )

    with pytest.raises(RuntimeError, match="both dense and sparse retrieval failed"):
        searcher.search("q")


@pytest.mark.integration
def test_search_fusion_failure_falls_back_to_single_path_results() -> None:
    searcher = HybridSearch(
        settings={},
        query_processor=FakeQueryProcessor(),  # type: ignore[arg-type]
        dense_retriever=FakeDenseRetriever(explode=True),  # type: ignore[arg-type]
        sparse_retriever=FakeSparseRetriever(),  # type: ignore[arg-type]
        fusion=FakeFusion(explode=True),  # type: ignore[arg-type]
    )

    results = searcher.search("q", top_k=1)

    assert len(results) == 1
    assert results[0].chunk_id == "s1"
