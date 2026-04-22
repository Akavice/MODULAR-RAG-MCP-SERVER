"""Core abstractions for evaluation implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from typing import Any


class BaseEvaluator(ABC):
    """Abstract evaluator interface for retrieval quality metrics."""

    def __init__(self, **options: Any) -> None:
        self.options = options

    @abstractmethod
    def evaluate(
        self,
        query: str,
        retrieved_ids: Sequence[str],
        golden_ids: Sequence[str],
        trace: Any | None = None,
    ) -> dict[str, float]:
        """Return deterministic metrics for a single evaluation sample."""

    @staticmethod
    def validate_inputs(
        query: str,
        retrieved_ids: Sequence[str],
        golden_ids: Sequence[str],
    ) -> None:
        """Validate evaluator input payload shape."""
        if not isinstance(query, str):
            raise TypeError("query must be a string")
        if not query.strip():
            raise ValueError("query must not be empty")

        BaseEvaluator._validate_id_sequence("retrieved_ids", retrieved_ids)
        BaseEvaluator._validate_id_sequence("golden_ids", golden_ids)

    @staticmethod
    def _validate_id_sequence(name: str, values: Sequence[str]) -> None:
        if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
            raise TypeError(f"{name} must be a sequence of strings")

        for index, value in enumerate(values):
            if not isinstance(value, str):
                raise TypeError(f"{name}[{index}] must be a string")
