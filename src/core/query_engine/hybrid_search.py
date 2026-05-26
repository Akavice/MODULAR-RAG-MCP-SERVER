"""Hybrid retrieval orchestration: query processing + dense/sparse + fusion."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from core.query_engine.dense_retriever import DenseRetriever
from core.query_engine.fusion import Fusion
from core.query_engine.query_processor import QueryProcessor
from core.query_engine.sparse_retriever import SparseRetriever
from core.types import RetrievalResult


class HybridSearch:
    """Coordinate dense/sparse retrieval with deterministic fusion and fallback."""

    def __init__(
        self,
        settings: Any,
        *,
        query_processor: QueryProcessor | None = None,
        dense_retriever: DenseRetriever | None = None,
        sparse_retriever: SparseRetriever | None = None,
        fusion: Fusion | None = None,
    ) -> None:
        self.settings = settings
        self.query_processor = query_processor or QueryProcessor(settings)
        self.dense_retriever = dense_retriever or DenseRetriever(settings)
        self.sparse_retriever = sparse_retriever or SparseRetriever(settings)
        self.fusion = fusion or Fusion(settings)
        self.default_top_k = self._resolve_default_top_k(settings)

    def search(
        self,
        query: str,
        top_k: int | None = None,
        filters: Mapping[str, Any] | None = None,
        trace: Any | None = None,
    ) -> list[RetrievalResult]:
        resolved_top_k = self._normalize_top_k(top_k) if top_k is not None else self.default_top_k
        normalized_filters = self._normalize_filters(filters)
        processed = self.query_processor.process(query, filters=normalized_filters)

        dense_results: list[RetrievalResult] = []
        sparse_results: list[RetrievalResult] = []
        dense_error: Exception | None = None
        sparse_error: Exception | None = None

        try:
            dense_results = self.dense_retriever.retrieve(
                processed.query,
                top_k=resolved_top_k,
                filters=processed.filters,
                trace=trace,
            )
        except Exception as exc:
            dense_error = exc

        try:
            sparse_results = self.sparse_retriever.retrieve(
                processed.keywords,
                top_k=resolved_top_k,
                trace=trace,
            )
        except Exception as exc:
            sparse_error = exc

        if dense_error is not None and sparse_error is not None:
            raise RuntimeError(
                "both dense and sparse retrieval failed: "
                f"dense={dense_error}; sparse={sparse_error}"
            ) from sparse_error

        fusion_top_k = self._resolve_fusion_top_k(
            dense_results=dense_results,
            sparse_results=sparse_results,
            requested_top_k=resolved_top_k,
        )
        fused = self._fuse_with_fallback(
            dense_results=dense_results,
            sparse_results=sparse_results,
            top_k=fusion_top_k,
            trace=trace,
        )
        filtered = self._apply_metadata_filters(fused, processed.filters)
        output = filtered[:resolved_top_k]

        if trace is not None and hasattr(trace, "record_stage"):
            trace.record_stage(
                "hybrid_search",
                top_k=resolved_top_k,
                query=processed.query,
                keyword_count=len(processed.keywords),
                filter_count=len(processed.filters),
                fusion_top_k=fusion_top_k,
                dense_count=len(dense_results),
                sparse_count=len(sparse_results),
                result_count=len(output),
                dense_failed=dense_error is not None,
                sparse_failed=sparse_error is not None,
            )
        return output

    def _fuse_with_fallback(
        self,
        *,
        dense_results: list[RetrievalResult],
        sparse_results: list[RetrievalResult],
        top_k: int,
        trace: Any | None,
    ) -> list[RetrievalResult]:
        try:
            return self.fusion.fuse(
                dense_results,
                sparse_results,
                top_k=top_k,
                trace=trace,
            )
        except Exception:
            if dense_results and sparse_results:
                raise
            fallback = dense_results if dense_results else sparse_results
            return fallback[:top_k]

    @staticmethod
    def _resolve_fusion_top_k(
        *,
        dense_results: list[RetrievalResult],
        sparse_results: list[RetrievalResult],
        requested_top_k: int,
    ) -> int:
        # Fuse a superset first, then apply metadata filters and final top_k trim.
        candidate_count = len(dense_results) + len(sparse_results)
        return max(requested_top_k, candidate_count)

    def _apply_metadata_filters(
        self,
        candidates: list[RetrievalResult],
        filters: Mapping[str, Any] | None,
    ) -> list[RetrievalResult]:
        if not filters:
            return list(candidates)

        output: list[RetrievalResult] = []
        for item in candidates:
            if self._matches_filters(item, filters):
                output.append(item)
        return output

    @staticmethod
    def _matches_filters(item: RetrievalResult, filters: Mapping[str, Any]) -> bool:
        metadata = item.metadata
        for key, expected in filters.items():
            if key == "time_range":
                if not HybridSearch._matches_time_range(metadata, expected):
                    return False
                continue
            if metadata.get(key) != expected:
                return False
        return True

    @staticmethod
    def _matches_time_range(metadata: Mapping[str, Any], expected: Any) -> bool:
        if not isinstance(expected, Mapping):
            return True
        candidate = None
        for key in ("created_at", "updated_at", "timestamp", "date"):
            value = metadata.get(key)
            if isinstance(value, str) and value.strip():
                candidate = value.strip()
                break
        if candidate is None:
            return False
        range_from = expected.get("from")
        if isinstance(range_from, str) and range_from.strip() and candidate < range_from.strip():
            return False
        range_to = expected.get("to")
        if isinstance(range_to, str) and range_to.strip() and candidate > range_to.strip():
            return False
        return True

    @staticmethod
    def _normalize_top_k(value: Any) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("top_k must be an integer")
        if value <= 0:
            raise ValueError("top_k must be greater than 0")
        return value

    @staticmethod
    def _normalize_filters(filters: Mapping[str, Any] | None) -> dict[str, Any] | None:
        if filters is None:
            return None
        if not isinstance(filters, Mapping):
            raise TypeError("filters must be a mapping when provided")
        normalized: dict[str, Any] = {}
        for key, value in filters.items():
            if not isinstance(key, str) or not key.strip():
                raise ValueError("filters keys must be non-empty strings")
            normalized[key.strip()] = value
        return normalized

    @staticmethod
    def _resolve_default_top_k(settings: Any) -> int:
        if isinstance(settings, Mapping):
            retrieval = settings.get("retrieval")
        else:
            retrieval = getattr(settings, "retrieval", None)
        if isinstance(retrieval, Mapping) and "top_k" in retrieval:
            return HybridSearch._normalize_top_k(retrieval.get("top_k"))
        return 5
