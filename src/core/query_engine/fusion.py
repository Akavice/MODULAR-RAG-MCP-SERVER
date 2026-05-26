"""Rank fusion utilities for hybrid retrieval."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from core.types import RetrievalResult


class Fusion:
    """Fuse dense/sparse ranked lists by Reciprocal Rank Fusion (RRF)."""

    def __init__(self, settings: Any, *, rrf_k: int | None = None) -> None:
        self.settings = settings
        self.rrf_k = self._normalize_rrf_k(rrf_k) if rrf_k is not None else self._resolve_rrf_k(settings)
        self.default_top_k = self._resolve_default_top_k(settings)

    def fuse(
        self,
        dense_results: Sequence[RetrievalResult],
        sparse_results: Sequence[RetrievalResult],
        top_k: int | None = None,
        trace: Any | None = None,
    ) -> list[RetrievalResult]:
        dense = self._normalize_results(dense_results, field_name="dense_results")
        sparse = self._normalize_results(sparse_results, field_name="sparse_results")
        resolved_top_k = self._normalize_top_k(top_k) if top_k is not None else self.default_top_k

        rrf_scores: dict[str, float] = {}
        payload_by_id: dict[str, RetrievalResult] = {}

        self._accumulate_channel(dense, rrf_scores, payload_by_id)
        self._accumulate_channel(sparse, rrf_scores, payload_by_id)

        fused = sorted(rrf_scores.items(), key=lambda item: (-item[1], item[0]))[:resolved_top_k]
        output: list[RetrievalResult] = []
        for chunk_id, score in fused:
            payload = payload_by_id[chunk_id]
            output.append(
                RetrievalResult(
                    chunk_id=chunk_id,
                    score=score,
                    text=payload.text,
                    metadata=dict(payload.metadata),
                )
            )

        if trace is not None and hasattr(trace, "record_stage"):
            trace.record_stage(
                "fusion",
                method="rrf",
                rrf_k=self.rrf_k,
                dense_count=len(dense),
                sparse_count=len(sparse),
                fused_count=len(output),
                top_k=resolved_top_k,
            )
        return output

    def _accumulate_channel(
        self,
        items: list[RetrievalResult],
        rrf_scores: dict[str, float],
        payload_by_id: dict[str, RetrievalResult],
    ) -> None:
        seen_ids: set[str] = set()
        for rank, item in enumerate(items, start=1):
            chunk_id = item.chunk_id
            if chunk_id in seen_ids:
                continue
            seen_ids.add(chunk_id)
            if chunk_id not in payload_by_id:
                payload_by_id[chunk_id] = item
            rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0.0) + (1.0 / (self.rrf_k + rank))

    @staticmethod
    def _normalize_results(value: Sequence[RetrievalResult], *, field_name: str) -> list[RetrievalResult]:
        if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
            raise TypeError(f"{field_name} must be a sequence of RetrievalResult")
        output: list[RetrievalResult] = []
        for index, item in enumerate(value):
            if not isinstance(item, RetrievalResult):
                raise TypeError(f"{field_name}[{index}] must be a RetrievalResult")
            output.append(item)
        return output

    @staticmethod
    def _normalize_top_k(value: Any) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("top_k must be an integer")
        if value <= 0:
            raise ValueError("top_k must be greater than 0")
        return value

    @staticmethod
    def _normalize_rrf_k(value: Any) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("rrf_k must be an integer")
        if value <= 0:
            raise ValueError("rrf_k must be greater than 0")
        return value

    @staticmethod
    def _resolve_default_top_k(settings: Any) -> int:
        if isinstance(settings, Mapping):
            retrieval = settings.get("retrieval")
        else:
            retrieval = getattr(settings, "retrieval", None)
        if isinstance(retrieval, Mapping) and "top_k" in retrieval:
            return Fusion._normalize_top_k(retrieval.get("top_k"))
        return 5

    @staticmethod
    def _resolve_rrf_k(settings: Any) -> int:
        if isinstance(settings, Mapping):
            retrieval = settings.get("retrieval")
        else:
            retrieval = getattr(settings, "retrieval", None)
        if isinstance(retrieval, Mapping):
            fusion_section = retrieval.get("fusion")
            if isinstance(fusion_section, Mapping) and "rrf_k" in fusion_section:
                return Fusion._normalize_rrf_k(fusion_section.get("rrf_k"))
            if "rrf_k" in retrieval:
                return Fusion._normalize_rrf_k(retrieval.get("rrf_k"))
        return 60
