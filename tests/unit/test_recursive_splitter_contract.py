"""Contract tests for RecursiveSplitter behavior beyond smoke paths."""

from __future__ import annotations

import pytest

from libs.splitter.recursive_splitter import RecursiveSplitter


@pytest.mark.unit
def test_recursive_splitter_splits_markdown_headings_into_multiple_chunks() -> None:
    splitter = RecursiveSplitter(chunk_size=20, chunk_overlap=0)
    text = "# H1\n\npara1\n\n## H2\n\npara2\n\n### H3\n\npara3"

    chunks = splitter.split(text)

    assert len(chunks) >= 2
    assert any("# H1" in chunk for chunk in chunks)
    assert any("## H2" in chunk for chunk in chunks)


@pytest.mark.unit
def test_recursive_splitter_preserves_progress_for_long_unbroken_text() -> None:
    splitter = RecursiveSplitter(chunk_size=12, chunk_overlap=5)
    text = "x" * 80

    chunks = splitter.split(text)

    assert len(chunks) > 1
    assert all(chunk.strip() for chunk in chunks)
    assert all(len(chunk) <= 12 for chunk in chunks)


@pytest.mark.unit
def test_recursive_splitter_respects_custom_separators_when_splitting_long_text() -> None:
    splitter = RecursiveSplitter(chunk_size=7, chunk_overlap=0, separators=["@@", ""])
    text = "aa@@bb@@cc@@dd"

    chunks = splitter.split(text)

    # If custom separator is honored, chunks should split at separator boundary
    # and avoid cutting a separator token into a dangling single '@'.
    assert all(not chunk.endswith("@") for chunk in chunks)
    assert all(not chunk.startswith("@") for chunk in chunks)


@pytest.mark.unit
def test_recursive_splitter_custom_separator_produces_expected_chunks() -> None:
    splitter = RecursiveSplitter(chunk_size=7, chunk_overlap=0, separators=["@@", ""])
    text = "aa@@bb@@cc@@dd"

    chunks = splitter.split(text)

    assert chunks == ["aa", "bb", "cc", "dd"]
