"""Core abstractions for embedding implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any


class BaseEmbedding(ABC):
    """Abstract embedding interface used by ingestion and retrieval."""

    def __init__(self, *, model: str | None = None, **options: Any) -> None:
        self.model = model
        self.options = options

    @abstractmethod
    def embed(
        self,
        texts: Sequence[str],
        trace: Any | None = None,
    ) -> list[list[float]]:
        """Embed texts into vectors with provider-specific implementations."""

    @staticmethod
    def validate_texts(texts: Sequence[str]) -> None:
        """Validate minimal text input contract before provider calls."""
        if not texts:
            raise ValueError("texts must not be empty")

        for index, text in enumerate(texts):
            if not isinstance(text, str):
                raise TypeError(f"text at index {index} must be a string")
