"""Additional contract tests for DenseRetriever edge behavior."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import pytest

from core.query_engine.dense_retriever import DenseRetriever
from libs.embedding.base_embedding import BaseEmbedding
from libs.vector_store.base_vector_store import BaseVectorStore, QueryMatch


class FakeEmbedding(BaseEmbedding):
    def __init__(self) -> None:
        super().__init__(model="fake")

    def embed(self, texts: list[str], trace: Any | None = None) -> list[list[float]]:
        _ = texts, trace
        return [[0.1, 0.2, 0.3]]


class BadVectorStoreOutputType(BaseVectorStore):
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
        return "bad"  # type: ignore[return-value]


class BadVectorStoreItemType(BaseVectorStore):
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
        return ["bad"]  # type: ignore[list-item]


class BadScoreVectorStore(BaseVectorStore):
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
        return [{"id": "c1", "score": True, "text": "x", "metadata": {"source_path": "d"}}]  # type: ignore[dict-item]


@pytest.mark.unit
def test_retrieve_rejects_non_list_vector_store_output() -> None:
    retriever = DenseRetriever(
        settings={},
        embedding_client=FakeEmbedding(),
        vector_store=BadVectorStoreOutputType(),
    )

    with pytest.raises(TypeError, match="vector_store.query output must be a list"):
        retriever.retrieve("q")


@pytest.mark.unit
def test_retrieve_rejects_non_mapping_vector_store_items() -> None:
    retriever = DenseRetriever(
        settings={},
        embedding_client=FakeEmbedding(),
        vector_store=BadVectorStoreItemType(),
    )

    with pytest.raises(TypeError, match="must be a mapping"):
        retriever.retrieve("q")


@pytest.mark.unit
def test_retrieve_rejects_boolean_score_in_result() -> None:
    retriever = DenseRetriever(
        settings={},
        embedding_client=FakeEmbedding(),
        vector_store=BadScoreVectorStore(),
    )

    with pytest.raises(TypeError, match="score must be numeric"):
        retriever.retrieve("q")
