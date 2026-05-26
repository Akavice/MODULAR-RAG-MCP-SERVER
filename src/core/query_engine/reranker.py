"""Core-layer reranker orchestration with graceful fallback."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from core.types import RetrievalResult
from libs.reranker.base_reranker import BaseReranker
from libs.reranker.reranker_factory import RerankerFactory


class Reranker:
    """Apply optional reranking on fused retrieval results."""

    def __init__(
        self,
        settings: Any,
        *,
        reranker: BaseReranker | None = None,
    ) -> None:
        self.settings = settings
        self.enabled = self._resolve_enabled(settings)
        self._reranker = reranker
        self._init_error: str | None = None

    def rerank(
        self,
        query: str,
        candidates: Sequence[RetrievalResult],
        trace: Any | None = None,
    ) -> list[RetrievalResult]:
        normalized_query = self._normalize_query(query)
        normalized_candidates = self._normalize_candidates(candidates)

        if not normalized_candidates:
            self._record_trace(
                trace,
                input_count=0,
                output_count=0,
                enabled=self.enabled,
                fallback=False,
                reason="no_candidates",
            )
            return []

        if not self.enabled:
            self._record_trace(
                trace,
                input_count=len(normalized_candidates),
                output_count=len(normalized_candidates),
                enabled=False,
                fallback=False,
                reason="disabled",
            )
            return list(normalized_candidates)

        backend = self._resolve_backend()
        if backend is None:
            self._record_trace(
                trace,
                input_count=len(normalized_candidates),
                output_count=len(normalized_candidates),
                enabled=True,
                fallback=True,
                reason=self._init_error or "reranker_init_failed",
            )
            return list(normalized_candidates)

        payload = [self._to_candidate_payload(item) for item in normalized_candidates]
        try:
            ranked_payload = backend.rerank(normalized_query, payload, trace=trace)
            output = self._from_ranked_payload(
                original=normalized_candidates,
                ranked_payload=ranked_payload,
            )
            self._record_trace(
                trace,
                input_count=len(normalized_candidates),
                output_count=len(output),
                enabled=True,
                fallback=False,
                reason="ok",
            )
            return output
        except Exception as exc:
            self._record_trace(
                trace,
                input_count=len(normalized_candidates),
                output_count=len(normalized_candidates),
                enabled=True,
                fallback=True,
                reason=f"rerank_failed: {exc}",
            )
            return list(normalized_candidates)

    def _resolve_backend(self) -> BaseReranker | None:
        if self._reranker is not None:
            return self._reranker
        if self._init_error is not None:
            return None
        try:
            self._reranker = RerankerFactory.create(self.settings)
            return self._reranker
        except Exception as exc:
            self._init_error = str(exc)
            return None

    @staticmethod
    def _to_candidate_payload(item: RetrievalResult) -> dict[str, Any]:
        return {
            "id": item.chunk_id,
            "text": item.text,
            "score": item.score,
            "metadata": dict(item.metadata),
        }

    @staticmethod
    def _from_ranked_payload(
        *,
        original: list[RetrievalResult],
        ranked_payload: Any,
    ) -> list[RetrievalResult]:
        if not isinstance(ranked_payload, Sequence) or isinstance(ranked_payload, (str, bytes)):
            raise TypeError("reranker output must be a sequence")

        result: list[RetrievalResult] = []
        used_indices: set[int] = set()
        id_to_indices: dict[str, list[int]] = {}
        for index, item in enumerate(original):
            id_to_indices.setdefault(item.chunk_id, []).append(index)

        for index, candidate in enumerate(ranked_payload):
            if not isinstance(candidate, Mapping):
                raise TypeError(f"reranker output item at index {index} must be a mapping")

            candidate_id_raw = candidate.get("id")
            if isinstance(candidate_id_raw, str) and candidate_id_raw.strip():
                candidate_id = candidate_id_raw.strip()
                matched = False
                for original_index in id_to_indices.get(candidate_id, []):
                    if original_index in used_indices:
                        continue
                    source = original[original_index]
                    used_indices.add(original_index)
                    result.append(
                        RetrievalResult(
                            chunk_id=source.chunk_id,
                            score=Reranker._coalesce_score(candidate.get("score"), source.score),
                            text=Reranker._coalesce_text(candidate.get("text"), source.text),
                            metadata=Reranker._coalesce_metadata(candidate.get("metadata"), source.metadata),
                        )
                    )
                    matched = True
                    break
                if matched:
                    continue

            # Ignore unmatched rows and keep original fallback ordering below.
            continue

        # Ensure no original candidate is lost due to malformed backend output.
        for index, item in enumerate(original):
            if index not in used_indices:
                result.append(item)

        return result

    @staticmethod
    def _coalesce_score(value: Any, fallback: float) -> float:
        if value is None:
            return fallback
        return Reranker._coerce_score(value, default=fallback)

    @staticmethod
    def _coerce_score(value: Any, *, default: float) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return float(default)
        numeric = float(value)
        if numeric != numeric or numeric in (float("inf"), float("-inf")):
            return float(default)
        return numeric

    @staticmethod
    def _coalesce_text(value: Any, fallback: str) -> str:
        if isinstance(value, str):
            return value
        if value is None:
            return fallback
        return str(value)

    @staticmethod
    def _coalesce_metadata(value: Any, fallback: Mapping[str, Any]) -> dict[str, Any]:
        if isinstance(value, Mapping):
            return dict(value)
        return dict(fallback)

    @staticmethod
    def _normalize_query(query: Any) -> str:
        if not isinstance(query, str):
            raise TypeError("query must be a string")
        normalized = query.strip()
        if not normalized:
            raise ValueError("query must not be empty")
        return normalized

    @staticmethod
    def _normalize_candidates(candidates: Sequence[RetrievalResult]) -> list[RetrievalResult]:
        if not isinstance(candidates, Sequence) or isinstance(candidates, (str, bytes)):
            raise TypeError("candidates must be a sequence of RetrievalResult")
        output: list[RetrievalResult] = []
        for index, item in enumerate(candidates):
            if not isinstance(item, RetrievalResult):
                raise TypeError(f"candidates[{index}] must be a RetrievalResult")
            output.append(item)
        return output

    @staticmethod
    def _resolve_enabled(settings: Any) -> bool:
        if isinstance(settings, Mapping):
            rerank = settings.get("rerank")
        else:
            rerank = getattr(settings, "rerank", None)
        if isinstance(rerank, Mapping):
            value = rerank.get("enabled", False)
            if isinstance(value, bool):
                return value
            return bool(value)
        return False

    @staticmethod
    def _record_trace(
        trace: Any | None,
        *,
        input_count: int,
        output_count: int,
        enabled: bool,
        fallback: bool,
        reason: str,
    ) -> None:
        if trace is None or not hasattr(trace, "record_stage"):
            return
        trace.record_stage(
            "rerank",
            enabled=enabled,
            fallback=fallback,
            reason=reason,
            input_count=input_count,
            output_count=output_count,
        )
