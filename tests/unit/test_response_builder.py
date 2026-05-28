"""Unit tests for MCP response builder."""

from __future__ import annotations

import pytest

from core.response.response_builder import ResponseBuilder
from core.types import RetrievalResult


def _r(chunk_id: str, score: float, text: str) -> RetrievalResult:
    return RetrievalResult(
        chunk_id=chunk_id,
        score=score,
        text=text,
        metadata={"source_path": f"docs/{chunk_id}.pdf", "page": 1},
    )


@pytest.mark.unit
def test_build_includes_markdown_and_citations() -> None:
    builder = ResponseBuilder()

    payload = builder.build([_r("a", 0.9, "alpha"), _r("b", 0.7, "beta")], query="q")

    assert payload["content"][0]["type"] == "text"
    text = payload["content"][0]["text"]
    assert "[1]" in text and "[2]" in text
    citations = payload["structuredContent"]["citations"]
    assert len(citations) == 2
    assert citations[0]["chunk_id"] == "a"


@pytest.mark.unit
def test_build_returns_friendly_message_for_empty_results() -> None:
    builder = ResponseBuilder()

    payload = builder.build([], query="missing")

    assert "No results found" in payload["content"][0]["text"]
    assert payload["structuredContent"]["results"] == []
