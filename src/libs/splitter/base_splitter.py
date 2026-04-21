"""Core abstractions for splitter implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseSplitter(ABC):
    """Abstract splitter interface for chunking document text."""

    def __init__(
        self,
        *,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        **options: Any,
    ) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.options = options

    @abstractmethod
    def split(self, text: str, trace: Any | None = None) -> list[str]:
        """Split input text into chunks."""

    @staticmethod
    def validate_text(text: str) -> None:
        """Validate basic text contract before splitting."""
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        if not text.strip():
            raise ValueError("text must not be empty")
