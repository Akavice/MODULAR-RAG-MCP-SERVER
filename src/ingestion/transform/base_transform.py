"""Core abstractions for ingestion transform implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from core.types import Chunk


class BaseTransform(ABC):
    """Abstract transform stage for post-split chunk processing."""

    @abstractmethod
    def transform(self, chunks: list[Chunk], trace: Any | None = None) -> list[Chunk]:
        """Transform chunks and return a new chunk list."""

    @staticmethod
    def validate_chunks(chunks: list[Chunk]) -> None:
        """Validate transform input before processing."""
        if not isinstance(chunks, list):
            raise TypeError("chunks must be a list")

        for index, chunk in enumerate(chunks):
            if not isinstance(chunk, Chunk):
                raise TypeError(f"chunk at index {index} must be a Chunk")
