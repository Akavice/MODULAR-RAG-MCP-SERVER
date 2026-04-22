"""Core abstractions for vector store implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from typing import Any, TypedDict


class VectorRecord(TypedDict, total=False):
    """Canonical record shape for vector upsert."""

    id: str
    vector: list[float]
    text: str
    metadata: dict[str, Any]


class QueryMatch(TypedDict, total=False):
    """Canonical query result shape returned by vector stores."""

    id: str
    score: float
    text: str
    metadata: dict[str, Any]


class BaseVectorStore(ABC):
    """Abstract vector store interface for upsert and retrieval."""

    def __init__(self, *, collection_name: str = "default", **options: Any) -> None:
        self.collection_name = collection_name
        self.options = options

    @abstractmethod
    def upsert(
        self,
        records: Sequence[Mapping[str, Any]],
        trace: Any | None = None,
    ) -> int:
        """Upsert vector records and return the number of processed items."""

    @abstractmethod
    def query(
        self,
        vector: Sequence[float],
        top_k: int = 5,
        filters: Mapping[str, Any] | None = None,
        trace: Any | None = None,
    ) -> list[QueryMatch]:
        """Query nearest matches by input vector."""

    @staticmethod
    def validate_records(records: Sequence[Mapping[str, Any]]) -> None:
        """Validate upsert payload shape before provider calls."""
        if not records:
            raise ValueError("records must not be empty")

        for index, record in enumerate(records):
            if not isinstance(record, Mapping):
                raise TypeError(f"record at index {index} must be a mapping")

            record_id = record.get("id")
            if not isinstance(record_id, str) or not record_id.strip():
                raise ValueError(f"record at index {index} is missing a valid id")

            vector = record.get("vector")
            if not isinstance(vector, Sequence) or isinstance(vector, (str, bytes)):
                raise TypeError(f"record at index {index} has invalid vector")
            if len(vector) == 0:
                raise ValueError(f"record at index {index} has empty vector")

            for dim, value in enumerate(vector):
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    raise TypeError(
                        f"record at index {index} has non-numeric vector value at {dim}"
                    )

            metadata = record.get("metadata")
            if metadata is not None and not isinstance(metadata, Mapping):
                raise TypeError(f"record at index {index} has invalid metadata")

    @staticmethod
    def validate_query_inputs(
        vector: Sequence[float],
        top_k: int,
        filters: Mapping[str, Any] | None,
    ) -> None:
        """Validate query payload shape before provider calls."""
        if not isinstance(vector, Sequence) or isinstance(vector, (str, bytes)):
            raise TypeError("query vector must be a sequence of numeric values")
        if len(vector) == 0:
            raise ValueError("query vector must not be empty")
        for dim, value in enumerate(vector):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(f"query vector has non-numeric value at index {dim}")

        if isinstance(top_k, bool) or not isinstance(top_k, int):
            raise TypeError("top_k must be an integer")
        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")

        if filters is not None and not isinstance(filters, Mapping):
            raise TypeError("filters must be a mapping")
