"""Cross-encoder reranker implementation with pluggable scoring backend."""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from libs.reranker.base_reranker import BaseReranker, RerankCandidate


class CrossEncoderRerankerError(RuntimeError):
    """Stable provider-scoped error signal for fallback handling."""

    def __init__(self, error_type: str, message: str) -> None:
        super().__init__(f"[cross_encoder][{error_type}] {message}")
        self.provider = "cross_encoder"
        self.error_type = error_type
        self.message = message


class CrossEncoderReranker(BaseReranker):
    """Rerank candidates with a cross-encoder style scoring function."""

    def __init__(
        self,
        *,
        model: str | None = None,
        top_m: int | None = None,
        timeout: float | int | None = None,
        scorer: Callable[[str, list[dict[str, Any]]], list[float]] | None = None,
        **options: Any,
    ) -> None:
        super().__init__(**options)
        self.model = model or "cross-encoder-placeholder"
        self.top_m = self._normalize_top_m(top_m)
        self.timeout_seconds = self._normalize_timeout(timeout)
        self._scorer = scorer or self._default_scorer

    def rerank(
        self,
        query: str,
        candidates: list[dict[str, Any]],
        trace: Any | None = None,
    ) -> list[RerankCandidate]:
        self.validate_inputs(query=query, candidates=candidates)
        if not candidates:
            return []

        rerank_count = len(candidates)
        if self.top_m is not None:
            rerank_count = min(rerank_count, self.top_m)

        head_candidates = candidates[:rerank_count]
        tail_candidates = candidates[rerank_count:]

        scores = self._score(query=query, candidates=head_candidates)
        scored_indices = [
            (index, score) for index, score in enumerate(scores)
        ]
        scored_indices.sort(key=lambda item: (-item[1], item[0]))

        ranked: list[RerankCandidate] = []
        for index, score in scored_indices:
            item = dict(head_candidates[index])
            item["score"] = float(score)
            ranked.append(item)

        ranked.extend(dict(item) for item in tail_candidates)
        return ranked

    def _score(self, *, query: str, candidates: list[dict[str, Any]]) -> list[float]:
        started_at = time.monotonic()
        try:
            scores = self._scorer(query, candidates)
        except TimeoutError as exc:
            raise CrossEncoderRerankerError("TimeoutError", str(exc)) from exc
        except CrossEncoderRerankerError:
            raise
        except Exception as exc:
            raise CrossEncoderRerankerError("BackendError", str(exc)) from exc

        elapsed = time.monotonic() - started_at
        if elapsed > self.timeout_seconds:
            raise CrossEncoderRerankerError(
                "TimeoutError",
                f"Reranker request exceeded timeout ({elapsed:.2f}s > {self.timeout_seconds:.2f}s)",
            )

        if not isinstance(scores, list):
            raise CrossEncoderRerankerError(
                "ResponseError",
                "Scorer must return a list of float scores",
            )
        if len(scores) != len(candidates):
            raise CrossEncoderRerankerError(
                "ResponseError",
                f"Scorer returned {len(scores)} scores for {len(candidates)} candidates",
            )

        normalized: list[float] = []
        for index, score in enumerate(scores):
            if isinstance(score, bool) or not isinstance(score, (int, float)):
                raise CrossEncoderRerankerError(
                    "ResponseError",
                    f"Score at index {index} must be numeric",
                )
            normalized.append(float(score))
        return normalized

    @staticmethod
    def _normalize_top_m(value: Any) -> int | None:
        if value is None:
            return None
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("top_m must be an integer when provided")
        if value <= 0:
            raise ValueError("top_m must be greater than 0")
        return value

    @staticmethod
    def _normalize_timeout(value: Any) -> float:
        if value is None:
            return 10.0
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("timeout must be a number when provided")
        normalized = float(value)
        if normalized <= 0:
            raise ValueError("timeout must be greater than 0")
        return normalized

    @staticmethod
    def _default_scorer(query: str, candidates: list[dict[str, Any]]) -> list[float]:
        query_tokens = set(query.lower().split())
        if not query_tokens:
            return [0.0 for _ in candidates]

        scores: list[float] = []
        for candidate in candidates:
            text = str(candidate.get("text", ""))
            candidate_tokens = set(text.lower().split())
            overlap = len(query_tokens.intersection(candidate_tokens))
            scores.append(overlap / float(len(query_tokens)))
        return scores
