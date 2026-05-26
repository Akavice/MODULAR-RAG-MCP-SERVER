"""Unit tests for DenseRetriever orchestration and contracts."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import pytest

from core.query_engine.dense_retriever import DenseRetriever
from core.types import RetrievalResult
from libs.embedding.base_embedding import BaseEmbedding
from libs.vector_store.base_vector_store import BaseVectorStore, QueryMatch


class FakeEmbedding(BaseEmbedding):
    def __init__(self) -> None:
        super().__init__(model="fake")
        self.calls: list[list[str]] = []

    def embed(
        self,
        texts: list[str],
        trace: Any | None = None,
    ) -> list[list[float]]:
        _ = trace
        self.calls.append(list(texts))
        return [[0.1, 0.2, 0.3]]


class FakeVectorStore(BaseVectorStore):
    def __init__(self) -> None:
        super().__init__(collection_name="kb")
        self.calls: list[dict[str, Any]] = []

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
        _ = trace
        self.calls.append({"vector": list(vector), "top_k": top_k, "filters": filters})
        return [
            {
                "id": "chunk-1",
                "score": 0.88,
                "text": "dense match",
                "metadata": {"source_path": "docs/a.pdf"},
            }
        ]


@pytest.mark.unit
def test_retrieve_calls_embedding_and_vector_store() -> None:
    embedding = FakeEmbedding()
    vector_store = FakeVectorStore()
    retriever = DenseRetriever(
        settings={"retrieval": {"top_k": 3}},
        embedding_client=embedding,
        vector_store=vector_store,
    )

    results = retriever.retrieve("rag retrieval", filters={"collection": "kb"})

    assert embedding.calls == [["rag retrieval"]]
    assert vector_store.calls[-1]["top_k"] == 3
    assert vector_store.calls[-1]["filters"] == {"collection": "kb"}
    assert len(results) == 1
    assert isinstance(results[0], RetrievalResult)
    assert results[0].chunk_id == "chunk-1"
    assert results[0].text == "dense match"


@pytest.mark.unit
def test_retrieve_respects_explicit_top_k_override() -> None:
    retriever = DenseRetriever(
        settings={"retrieval": {"top_k": 5}},
        embedding_client=FakeEmbedding(),
        vector_store=FakeVectorStore(),
    )

    retriever.retrieve("query", top_k=2)

    assert retriever.vector_store.calls[-1]["top_k"] == 2  # type: ignore[attr-defined]


@pytest.mark.unit
def test_retrieve_rejects_invalid_inputs() -> None:
    retriever = DenseRetriever(
        settings={},
        embedding_client=FakeEmbedding(),
        vector_store=FakeVectorStore(),
    )

    with pytest.raises(TypeError, match="query must be a string"):
        retriever.retrieve(123)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="query must not be empty"):
        retriever.retrieve(" ")
    with pytest.raises(TypeError, match="top_k must be an integer"):
        retriever.retrieve("q", top_k="3")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="top_k must be greater than 0"):
        retriever.retrieve("q", top_k=0)
    with pytest.raises(TypeError, match="filters must be a mapping"):
        retriever.retrieve("q", filters="x")  # type: ignore[arg-type]


@pytest.mark.unit
def test_retrieve_validates_embedding_output_shape() -> None:
    class BadEmbedding(FakeEmbedding):
        def embed(self, texts: list[str], trace: Any | None = None) -> list[list[float]]:
            _ = texts, trace
            return []

    retriever = DenseRetriever(
        settings={},
        embedding_client=BadEmbedding(),
        vector_store=FakeVectorStore(),
    )
    with pytest.raises(ValueError, match="embedding output size must be 1"):
        retriever.retrieve("q")


@pytest.mark.unit
def test_retrieve_result_to_dict_roundtrip() -> None:
    result = RetrievalResult(
        chunk_id="c1",
        score=0.5,
        text="hello",
        metadata={"source_path": "docs/a.pdf"},
    )

    payload = result.to_dict()
    restored = RetrievalResult.from_dict(payload)

    assert restored.to_dict() == payload
