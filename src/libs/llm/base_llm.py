"""Core abstractions for LLM implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from typing import Any


ChatMessage = Mapping[str, Any]


class BaseLLM(ABC):
    """Abstract LLM interface used by the core pipeline."""

    def __init__(self, *, model: str | None = None, **options: Any) -> None:
        self.model = model
        self.options = options

    @abstractmethod
    def chat(self, messages: Sequence[ChatMessage]) -> str:
        """Generate a single text response from a chat-style message list."""

    @staticmethod
    def validate_messages(messages: Sequence[ChatMessage]) -> None:
        """Validate minimal message structure before provider calls."""
        if not messages:
            raise ValueError("messages must not be empty")

        for index, message in enumerate(messages):
            if not isinstance(message, Mapping):
                raise TypeError(f"message at index {index} must be a mapping")

            role = message.get("role")
            content = message.get("content")

            if not isinstance(role, str) or not role.strip():
                raise ValueError(f"message at index {index} is missing a valid role")

            if content is None:
                raise ValueError(f"message at index {index} is missing content")
