"""Recursive splitter for markdown-aware chunking."""

from __future__ import annotations

import re
from collections.abc import Sequence
from typing import Any

from libs.splitter.base_splitter import BaseSplitter


class RecursiveSplitter(BaseSplitter):
    """Lightweight markdown-aware recursive splitter."""

    def __init__(
        self,
        *,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        separators: Sequence[str] | None = None,
        **options: Any,
    ) -> None:
        super().__init__(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            **options,
        )
        self.separators = list(separators or ["\n\n", "\n", " ", ""])

    def split(self, text: str, trace: Any | None = None) -> list[str]:
        self.validate_text(text)
        blocks = self._split_markdown_blocks(text)
        merged = self._merge_blocks(blocks)
        return merged

    def _split_markdown_blocks(self, text: str) -> list[str]:
        code_pattern = re.compile(r"(```[\s\S]*?```)", re.MULTILINE)
        parts = code_pattern.split(text)
        blocks: list[str] = []

        for part in parts:
            if not part or not part.strip():
                continue

            if part.startswith("```") and part.endswith("```"):
                blocks.append(part.strip())
                continue

            heading_splits = re.split(r"(?m)(?=^#{1,6}\s)", part)
            for section in heading_splits:
                section = section.strip()
                if not section:
                    continue
                paragraph_splits = [p.strip() for p in section.split("\n\n") if p.strip()]
                blocks.extend(paragraph_splits if paragraph_splits else [section])

        return blocks

    def _merge_blocks(self, blocks: list[str]) -> list[str]:
        if not blocks:
            return []

        chunks: list[str] = []
        current = ""

        for block in blocks:
            candidate = f"{current}\n\n{block}".strip() if current else block
            if len(candidate) <= self.chunk_size:
                current = candidate
                continue

            if current:
                chunks.append(current)
                current = ""

            if len(block) <= self.chunk_size:
                current = block
                continue

            chunks.extend(self._split_long_text(block))

        if current:
            chunks.append(current)

        return [chunk for chunk in chunks if chunk.strip()]

    def _split_long_text(self, text: str) -> list[str]:
        slices: list[str] = []
        start = 0
        length = len(text)

        while start < length:
            start = self._skip_leading_separators(text=text, start=start)
            if start >= length:
                break

            end = min(start + self.chunk_size, length)
            split_at = self._find_split_boundary(text=text, start=start, end=end)
            if split_at is None or split_at <= start:
                split_at = end

            chunk = text[start:split_at].strip()
            if not chunk and split_at < length:
                split_at = end
                chunk = text[start:split_at].strip()
            if chunk:
                slices.append(chunk)

            if split_at >= length:
                break

            next_start = max(0, split_at - self.chunk_overlap)
            if next_start <= start:
                next_start = split_at
            start = next_start

        return slices

    def _find_split_boundary(self, *, text: str, start: int, end: int) -> int | None:
        """Find the best split boundary within [start, end)."""
        if end <= start:
            return None

        for separator in self.separators:
            if not separator:
                continue
            pos = text.rfind(separator, start, end)
            if pos > start:
                return pos

        return None

    def _skip_leading_separators(self, *, text: str, start: int) -> int:
        """Advance start if it lands on one of the configured separators."""
        cursor = start
        while cursor < len(text):
            advanced = False
            for separator in self.separators:
                if not separator:
                    continue
                if text.startswith(separator, cursor):
                    cursor += len(separator)
                    advanced = True
                    break
            if not advanced:
                break
        return cursor
