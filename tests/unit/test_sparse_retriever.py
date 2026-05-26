"""Unit tests for SparseRetriever orchestration and contracts."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import pytest

from core.query_engine.sparse_retriever import SparseRetriever
from core.types import RetrievalResult
from libs.vector_store.base_vector_store import BaseVectorStore, QueryMatch


class FakeBM25Indexer:
    def __init__(self) -> None:
        self.loaded = False
        self.query_calls: list[dict[str, Any]] = []

    def load(self) -> None:
        self.loaded = True

    def query(self, keywords: list[str], top_k: int = 5) -> list[dict[str, Any]]:
        self.query_calls.append({"keywords": list(keywords), "top_k": top_k})
        return [
            {"chunk_id": "c2", "score": 2.0},
            {"chunk_id": "c1", "score": 1.5},
        ][:top_k]


class FakeVectorStore(BaseVectorStore):
    def __init__(self) -> None:
        super().__init__(collection_name="kb")
        self.get_by_ids_calls: list[list[str]] = []

    def upsert(self, records: list[dict[str, Any]], trace: Any | None = None) -> int:
        _ = records, trace
        return 0

    def query(
        self,
        vector: list[float],
        top_k: int = 5,
        filters: Mapping[str, Any] | None = None,
        trace: Any | None = None,
    ) -> list[QueryMatch]:
        _ = vector, top_k, filters, trace
        return []

    def get_by_ids(self, ids: list[str]) -> list[dict[str, Any]]:
        self.get_by_ids_calls.append(list(ids))
        payload = {
            "c1": {"id": "c1", "text": "alpha", "metadata": {"source_path": "docs/a.pdf"}},
            "c2": {"id": "c2", "text": "beta", "metadata": {"source_path": "docs/b.pdf"}},
        }
        return [payload[item_id] for item_id in ids if item_id in payload]


@pytest.mark.unit
def test_retrieve_calls_bm25_and_hydrates_by_ids() -> None:
    bm25 = FakeBM25Indexer()
    vector_store = FakeVectorStore()
    retriever = SparseRetriever(
        settings={"retrieval": {"top_k": 3}},
        bm25_indexer=bm25,  # type: ignore[arg-type]
        vector_store=vector_store,
    )

    results = retriever.retrieve(["RAG", "retrieval"])

    assert bm25.loaded is True
    assert bm25.query_calls[-1] == {"keywords": ["rag", "retrieval"], "top_k": 3}
    assert vector_store.get_by_ids_calls[-1] == ["c2", "c1"]
    assert len(results) == 2
    assert isinstance(results[0], RetrievalResult)
    assert results[0].chunk_id == "c2"
    assert results[0].text == "beta"
    assert results[0].score == 2.0


@pytest.mark.unit
def test_retrieve_respects_explicit_top_k() -> None:
    bm25 = FakeBM25Indexer()
    retriever = SparseRetriever(
        settings={"retrieval": {"top_k": 5}},
        bm25_indexer=bm25,  # type: ignore[arg-type]
        vector_store=FakeVectorStore(),
    )

    retriever.retrieve(["rag"], top_k=1)

    assert bm25.query_calls[-1]["top_k"] == 1


@pytest.mark.unit
def test_retrieve_rejects_invalid_inputs() -> None:
    retriever = SparseRetriever(
        settings={},
        bm25_indexer=FakeBM25Indexer(),  # type: ignore[arg-type]
        vector_store=FakeVectorStore(),
    )

    with pytest.raises(TypeError, match="keywords must be a sequence of strings"):
        retriever.retrieve("rag")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="keywords must not be empty"):
        retriever.retrieve(["  ", "\n"])
    with pytest.raises(TypeError, match="keywords\\[0\\] must be a string"):
        retriever.retrieve([1])  # type: ignore[list-item]
    with pytest.raises(TypeError, match="top_k must be an integer"):
        retriever.retrieve(["rag"], top_k="3")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="top_k must be greater than 0"):
        retriever.retrieve(["rag"], top_k=0)


@pytest.mark.unit
def test_retrieve_uses_empty_text_when_id_not_found() -> None:
    class MissingVectorStore(FakeVectorStore):
        def get_by_ids(self, ids: list[str]) -> list[dict[str, Any]]:
            self.get_by_ids_calls.append(list(ids))
            return []

    retriever = SparseRetriever(
        settings={},
        bm25_indexer=FakeBM25Indexer(),  # type: ignore[arg-type]
        vector_store=MissingVectorStore(),
    )

    results = retriever.retrieve(["rag"])

    assert results[0].chunk_id == "c2"
    assert results[0].text == ""
    assert results[0].metadata == {}
