"""Additional contract tests for SparseRetriever edge behavior."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import pytest

from core.query_engine.sparse_retriever import SparseRetriever
from libs.vector_store.base_vector_store import BaseVectorStore, QueryMatch


class FakeVectorStore(BaseVectorStore):
    def __init__(self) -> None:
        super().__init__(collection_name="kb")

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
        _ = ids
        return [{"id": "c1", "text": "x", "metadata": {"source_path": "docs/a.pdf"}}]


class BadBm25OutputType:
    def load(self) -> None:
        return None

    def query(self, keywords: list[str], top_k: int = 5) -> Any:
        _ = keywords, top_k
        return "bad"


class BadBm25ItemType:
    def load(self) -> None:
        return None

    def query(self, keywords: list[str], top_k: int = 5) -> Any:
        _ = keywords, top_k
        return ["bad"]


class BadBm25Score:
    def load(self) -> None:
        return None

    def query(self, keywords: list[str], top_k: int = 5) -> Any:
        _ = keywords, top_k
        return [{"chunk_id": "c1", "score": True}]


class BadGetByIdsOutput(FakeVectorStore):
    def get_by_ids(self, ids: list[str]) -> Any:
        _ = ids
        return "bad"


class BadGetByIdsItem(FakeVectorStore):
    def get_by_ids(self, ids: list[str]) -> Any:
        _ = ids
        return ["bad"]


@pytest.mark.unit
def test_retrieve_rejects_non_list_bm25_output() -> None:
    retriever = SparseRetriever(
        settings={},
        bm25_indexer=BadBm25OutputType(),  # type: ignore[arg-type]
        vector_store=FakeVectorStore(),
    )
    with pytest.raises(TypeError, match="bm25_indexer.query output must be a list"):
        retriever.retrieve(["rag"])


@pytest.mark.unit
def test_retrieve_rejects_non_mapping_bm25_item() -> None:
    retriever = SparseRetriever(
        settings={},
        bm25_indexer=BadBm25ItemType(),  # type: ignore[arg-type]
        vector_store=FakeVectorStore(),
    )
    with pytest.raises(TypeError, match="must be a mapping"):
        retriever.retrieve(["rag"])


@pytest.mark.unit
def test_retrieve_rejects_boolean_bm25_score() -> None:
    retriever = SparseRetriever(
        settings={},
        bm25_indexer=BadBm25Score(),  # type: ignore[arg-type]
        vector_store=FakeVectorStore(),
    )
    with pytest.raises(TypeError, match="invalid score"):
        retriever.retrieve(["rag"])


@pytest.mark.unit
def test_retrieve_rejects_non_list_get_by_ids_output() -> None:
    class GoodBm25:
        def load(self) -> None:
            return None

        def query(self, keywords: list[str], top_k: int = 5) -> Any:
            _ = keywords, top_k
            return [{"chunk_id": "c1", "score": 1.0}]

    retriever = SparseRetriever(
        settings={},
        bm25_indexer=GoodBm25(),  # type: ignore[arg-type]
        vector_store=BadGetByIdsOutput(),
    )
    with pytest.raises(TypeError, match="vector_store.get_by_ids output must be a list"):
        retriever.retrieve(["rag"])


@pytest.mark.unit
def test_retrieve_rejects_non_mapping_get_by_ids_item() -> None:
    class GoodBm25:
        def load(self) -> None:
            return None

        def query(self, keywords: list[str], top_k: int = 5) -> Any:
            _ = keywords, top_k
            return [{"chunk_id": "c1", "score": 1.0}]

    retriever = SparseRetriever(
        settings={},
        bm25_indexer=GoodBm25(),  # type: ignore[arg-type]
        vector_store=BadGetByIdsItem(),
    )
    with pytest.raises(TypeError, match="must be a mapping"):
        retriever.retrieve(["rag"])
