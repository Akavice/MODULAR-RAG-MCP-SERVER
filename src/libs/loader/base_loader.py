"""Core abstractions for loader implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from core.types import Document


class BaseLoader(ABC):
    """Abstract loader interface that converts file input into `Document`."""

    @abstractmethod
    def load(self, path: str) -> Document:
        """Load source file and return canonical `Document`."""

    @staticmethod
    def validate_file_path(path: str, *, expected_suffix: str | None = None) -> Path:
        """Validate and normalize input file path."""
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        normalized = path.strip()
        if not normalized:
            raise ValueError("path must not be empty")

        file_path = Path(normalized)
        if not file_path.exists() or not file_path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        if expected_suffix is not None:
            suffix = expected_suffix.lower()
            if file_path.suffix.lower() != suffix:
                raise ValueError(f"path must point to a {suffix} file")
        return file_path
