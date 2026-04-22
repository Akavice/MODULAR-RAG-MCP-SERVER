"""Unit tests for RecursiveSplitter default implementation."""

from __future__ import annotations

import pytest

from libs.splitter.recursive_splitter import RecursiveSplitter
from libs.splitter.splitter_factory import SplitterFactory


@pytest.mark.unit
def test_factory_routes_recursive_provider() -> None:
    splitter = SplitterFactory.create(
        {"splitter": {"provider": "recursive", "chunk_size": 120, "chunk_overlap": 20}}
    )

    assert isinstance(splitter, RecursiveSplitter)


@pytest.mark.unit
def test_recursive_splitter_keeps_small_code_block_intact() -> None:
    splitter = RecursiveSplitter(chunk_size=50, chunk_overlap=10)
    markdown = (
        "# Title\n\n"
        "Intro paragraph.\n\n"
        "```python\n"
        "print('hello')\n"
        "print('world')\n"
        "```\n\n"
        "Outro paragraph."
    )

    chunks = splitter.split(markdown)

    assert len(chunks) >= 2
    code_chunks = [chunk for chunk in chunks if "```python" in chunk]
    assert code_chunks
    assert "```" in code_chunks[0]


@pytest.mark.unit
def test_recursive_splitter_splits_long_plain_text_with_overlap() -> None:
    splitter = RecursiveSplitter(chunk_size=30, chunk_overlap=5)
    text = "abcdefghijklmnopqrstuvwxyz1234567890"

    chunks = splitter.split(text)

    assert len(chunks) >= 2
    assert all(len(chunk) <= 30 for chunk in chunks)
    assert chunks[0][-5:] in chunks[1]


@pytest.mark.unit
def test_recursive_splitter_rejects_empty_text() -> None:
    splitter = RecursiveSplitter(chunk_size=100, chunk_overlap=10)

    with pytest.raises(ValueError, match="text must not be empty"):
        splitter.split("   ")
