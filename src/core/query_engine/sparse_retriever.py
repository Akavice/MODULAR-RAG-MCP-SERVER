"""Sparse retriever backed by BM25 index and vector-store id lookup."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from core.types import RetrievalResult
from ingestion.storage.bm25_indexer import BM25Indexer
from libs.vector_store.base_vector_store import BaseVectorStore
from libs.vector_store.vector_store_factory import VectorStoreFactory


class SparseRetriever:
    """Perform lexical retrieval using BM25 and hydrate chunk payloads by ids."""

    def __init__(
        self,
        settings: Any,
        *,
        bm25_indexer: BM25Indexer | None = None,
        vector_store: BaseVectorStore | None = None,
    ) -> None:
        self.settings = settings
        self.bm25_indexer = bm25_indexer or BM25Indexer(settings)
        self.vector_store = vector_store or VectorStoreFactory.create(settings)
        self.default_top_k = self._resolve_default_top_k(settings)
        self._load_bm25_once()

    def retrieve(
        self,
        keywords: Sequence[str],
        top_k: int | None = None,
        trace: Any | None = None,
    ) -> list[RetrievalResult]:
        normalized_keywords = self._normalize_keywords(keywords)
        resolved_top_k = self._normalize_top_k(top_k) if top_k is not None else self.default_top_k

        bm25_hits = self.bm25_indexer.query(normalized_keywords, top_k=resolved_top_k)
        if not isinstance(bm25_hits, list):
            raise TypeError("bm25_indexer.query output must be a list")
        if not bm25_hits:
            if trace is not None and hasattr(trace, "record_stage"):
                trace.record_stage(
                    "sparse_retrieval",
                    keyword_count=len(normalized_keywords),
                    top_k=resolved_top_k,
                    hit_count=0,
                )
            return []

        rank_items: list[tuple[str, float]] = []
        for index, item in enumerate(bm25_hits):
            if not isinstance(item, Mapping):
                raise TypeError(f"bm25_indexer.query result at index {index} must be a mapping")
            chunk_id = item.get("chunk_id")
            score = item.get("score")
            if not isinstance(chunk_id, str) or not chunk_id.strip():
                raise ValueError(f"bm25_indexer.query result at index {index} has invalid chunk_id")
            if isinstance(score, bool) or not isinstance(score, (int, float)):
                raise TypeError(f"bm25_indexer.query result at index {index} has invalid score")
            rank_items.append((chunk_id.strip(), float(score)))

        ids = [chunk_id for chunk_id, _ in rank_items]
        records = self.vector_store.get_by_ids(ids)
        if not isinstance(records, list):
            raise TypeError("vector_store.get_by_ids output must be a list")
        payload_by_id = self._index_records_by_id(records)

        results: list[RetrievalResult] = []
        for chunk_id, score in rank_items:
            record = payload_by_id.get(chunk_id, {})
            text_value = record.get("text", "")
            metadata_value = record.get("metadata", {})
            metadata = dict(metadata_value) if isinstance(metadata_value, Mapping) else {}
            results.append(
                RetrievalResult(
                    chunk_id=chunk_id,
                    score=score,
                    text=text_value if isinstance(text_value, str) else str(text_value),
                    metadata=metadata,
                )
            )

        if trace is not None and hasattr(trace, "record_stage"):
            trace.record_stage(
                "sparse_retrieval",
                keyword_count=len(normalized_keywords),
                top_k=resolved_top_k,
                hit_count=len(results),
            )
        return results

    def _load_bm25_once(self) -> None:
        load_fn = getattr(self.bm25_indexer, "load", None)
        if callable(load_fn):
            load_fn()

    @staticmethod
    def _index_records_by_id(records: list[Any]) -> dict[str, Mapping[str, Any]]:
        by_id: dict[str, Mapping[str, Any]] = {}
        for index, item in enumerate(records):
            if not isinstance(item, Mapping):
                raise TypeError(
                    f"vector_store.get_by_ids result at index {index} must be a mapping"
                )
            item_id = item.get("id")
            if not isinstance(item_id, str) or not item_id.strip():
                raise ValueError(
                    f"vector_store.get_by_ids result at index {index} has invalid id"
                )
            by_id[item_id.strip()] = item
        return by_id

    @staticmethod
    def _normalize_keywords(keywords: Sequence[str]) -> list[str]:
        if not isinstance(keywords, Sequence) or isinstance(keywords, (str, bytes)):
            raise TypeError("keywords must be a sequence of strings")
        output: list[str] = []
        seen: set[str] = set()
        for index, item in enumerate(keywords):
            if not isinstance(item, str):
                raise TypeError(f"keywords[{index}] must be a string")
            token = item.strip().lower()
            if not token:
                continue
            if token not in seen:
                output.append(token)
                seen.add(token)
        if not output:
            raise ValueError("keywords must not be empty")
        return output

    @staticmethod
    def _normalize_top_k(top_k: Any) -> int:
        if isinstance(top_k, bool) or not isinstance(top_k, int):
            raise TypeError("top_k must be an integer")
        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")
        return top_k

    @staticmethod
    def _resolve_default_top_k(settings: Any) -> int:
        if isinstance(settings, Mapping):
            retrieval = settings.get("retrieval")
        else:
            retrieval = getattr(settings, "retrieval", None)
        if isinstance(retrieval, Mapping) and "top_k" in retrieval:
            return SparseRetriever._normalize_top_k(retrieval.get("top_k"))
        return 5
