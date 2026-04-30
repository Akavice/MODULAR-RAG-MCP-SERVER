"""Core abstractions for vision-capable LLM implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, TypedDict


class ChatResponse(TypedDict, total=False):
    """Canonical vision response payload."""

    text: str
    metadata: dict[str, Any]


class BaseVisionLLM(ABC):
    """Abstract vision LLM interface used by multimodal transforms."""

    def __init__(self, *, model: str | None = None, **options: Any) -> None:
        self.model = model
        self.options = options

    @abstractmethod
    def chat_with_image(
        self,
        text: str,
        image_path: str | bytes,
        trace: Any | None = None,
    ) -> ChatResponse:
        """Generate a text response from prompt text and one image input."""

    @staticmethod
    def validate_inputs(text: str, image_path: str | bytes) -> None:
        """Validate minimal multimodal request shape before provider calls."""
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        if isinstance(image_path, str):
            if not image_path.strip():
                raise ValueError("image_path must not be empty")
            return

        if isinstance(image_path, bytes):
            if not image_path:
                raise ValueError("image bytes must not be empty")
            return

        raise TypeError("image_path must be a string path or bytes")
