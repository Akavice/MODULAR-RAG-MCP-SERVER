"""Dense retriever built on embedding + vector store providers."""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any

from core.types import RetrievalResult
from libs.embedding.base_embedding import BaseEmbedding
from libs.embedding.embedding_factory import EmbeddingFactory
from libs.vector_store.base_vector_store import BaseVectorStore
from libs.vector_store.vector_store_factory import VectorStoreFactory


class DenseRetriever:
    """Perform semantic retrieval by embedding a query then querying vector store."""

    def __init__(
        self,
        settings: Any,
        *,
        embedding_client: BaseEmbedding | None = None,
        vector_store: BaseVectorStore | None = None,
    ) -> None:
        self.settings = settings
        self.embedding_client = embedding_client or EmbeddingFactory.create(settings)
        self.vector_store = vector_store or VectorStoreFactory.create(settings)
        self.default_top_k = self._resolve_default_top_k(settings)

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
        filters: Mapping[str, Any] | None = None,
        trace: Any | None = None,
    ) -> list[RetrievalResult]:
        normalized_query = self._normalize_query(query)
        resolved_top_k = self._normalize_top_k(top_k) if top_k is not None else self.default_top_k
        normalized_filters = self._normalize_filters(filters)

        vectors = self.embedding_client.embed([normalized_query], trace=trace)
        query_vector = self._extract_query_vector(vectors)
        matches = self.vector_store.query(
            vector=query_vector,
            top_k=resolved_top_k,
            filters=normalized_filters,
            trace=trace,
        )
        results = self._normalize_matches(matches)

        if trace is not None and hasattr(trace, "record_stage"):
            trace.record_stage(
                "dense_retrieval",
                query=normalized_query,
                top_k=resolved_top_k,
                filter_count=len(normalized_filters or {}),
                hit_count=len(results),
                provider=getattr(self.vector_store, "__class__", type(self.vector_store)).__name__,
            )
        return results

    @staticmethod
    def _normalize_query(query: Any) -> str:
        if not isinstance(query, str):
            raise TypeError("query must be a string")
        normalized = query.strip()
        if not normalized:
            raise ValueError("query must not be empty")
        return normalized

    @staticmethod
    def _normalize_top_k(top_k: Any) -> int:
        if isinstance(top_k, bool) or not isinstance(top_k, int):
            raise TypeError("top_k must be an integer")
        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")
        return top_k

    @staticmethod
    def _normalize_filters(filters: Mapping[str, Any] | None) -> dict[str, Any] | None:
        if filters is None:
            return None
        if not isinstance(filters, Mapping):
            raise TypeError("filters must be a mapping when provided")
        return {str(key): value for key, value in filters.items()}

    @staticmethod
    def _extract_query_vector(vectors: Any) -> list[float]:
        if not isinstance(vectors, list):
            raise TypeError("embedding output must be a list")
        if len(vectors) != 1:
            raise ValueError("embedding output size must be 1 for single query")
        vector = vectors[0]
        if not isinstance(vector, list) or not vector:
            raise ValueError("query embedding vector must be a non-empty list")
        normalized: list[float] = []
        for index, value in enumerate(vector):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(f"query embedding vector[{index}] must be numeric")
            numeric = float(value)
            if not math.isfinite(numeric):
                raise ValueError(f"query embedding vector[{index}] must be finite")
            normalized.append(numeric)
        return normalized

    @staticmethod
    def _normalize_matches(matches: Any) -> list[RetrievalResult]:
        if not isinstance(matches, list):
            raise TypeError("vector_store.query output must be a list")
        results: list[RetrievalResult] = []
        for index, item in enumerate(matches):
            if not isinstance(item, Mapping):
                raise TypeError(f"vector_store.query result at index {index} must be a mapping")
            chunk_id = item.get("id")
            score = item.get("score")
            text = item.get("text", "")
            metadata_raw = item.get("metadata", {})
            metadata = dict(metadata_raw) if isinstance(metadata_raw, Mapping) else {}
            results.append(
                RetrievalResult(
                    chunk_id=chunk_id,
                    score=score,
                    text=text if isinstance(text, str) else str(text),
                    metadata=metadata,
                )
            )
        return results

    @staticmethod
    def _resolve_default_top_k(settings: Any) -> int:
        if isinstance(settings, Mapping):
            retrieval = settings.get("retrieval")
        else:
            retrieval = getattr(settings, "retrieval", None)
        if isinstance(retrieval, Mapping):
            if "top_k" in retrieval:
                return DenseRetriever._normalize_top_k(retrieval.get("top_k"))
        return 5
