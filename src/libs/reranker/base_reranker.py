"""Core abstractions for reranker implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from typing import Any, TypedDict


class RerankCandidate(TypedDict, total=False):
    """Canonical reranker input/output candidate shape."""

    id: str
    text: str
    score: float
    metadata: dict[str, Any]


class BaseReranker(ABC):
    """Abstract reranker interface used by query-time ranking."""

    def __init__(self, **options: Any) -> None:
        self.options = options

    @abstractmethod
    def rerank(
        self,
        query: str,
        candidates: Sequence[Mapping[str, Any]],
        trace: Any | None = None,
    ) -> list[RerankCandidate]:
        """Re-rank candidates for the given query."""

    @staticmethod
    def validate_inputs(query: str, candidates: Sequence[Mapping[str, Any]]) -> None:
        """Validate rerank input payload shape before provider calls."""
        if not isinstance(query, str):
            raise TypeError("query must be a string")
        if not query.strip():
            raise ValueError("query must not be empty")

        if not isinstance(candidates, Sequence) or isinstance(candidates, (str, bytes)):
            raise TypeError("candidates must be a sequence")

        for index, candidate in enumerate(candidates):
            if not isinstance(candidate, Mapping):
                raise TypeError(f"candidate at index {index} must be a mapping")
