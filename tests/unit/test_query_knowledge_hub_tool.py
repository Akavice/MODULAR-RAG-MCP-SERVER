"""Unit tests for query_knowledge_hub MCP tool."""

from __future__ import annotations

from typing import Any

import pytest

from core.types import RetrievalResult
from mcp_server.tools import query_knowledge_hub


def _r(chunk_id: str, score: float, text: str) -> RetrievalResult:
    return RetrievalResult(
        chunk_id=chunk_id,
        score=score,
        text=text,
        metadata={"source_path": f"docs/{chunk_id}.pdf"},
    )


class FakeHybridSearch:
    def search(
        self,
        query: str,
        top_k: int | None = None,
        filters: dict[str, Any] | None = None,
        trace: Any | None = None,
    ) -> list[RetrievalResult]:
        _ = query, top_k, filters, trace
        return [_r("a", 0.9, "alpha"), _r("b", 0.8, "beta")]


class FakeReranker:
    def rerank(
        self,
        query: str,
        candidates: list[RetrievalResult],
        trace: Any | None = None,
    ) -> list[RetrievalResult]:
        _ = query, trace
        return list(reversed(candidates))


@pytest.mark.unit
def test_query_knowledge_hub_returns_content_and_structured_payload() -> None:
    payload = query_knowledge_hub.call(
        {"query": "rag", "top_k": 2},
        {
            "settings": {"vector_store": {}},
            "hybrid_search": FakeHybridSearch(),
            "reranker": FakeReranker(),
        },
    )

    assert payload["content"][0]["type"] == "text"
    assert payload["structuredContent"]["query"] == "rag"
    assert len(payload["structuredContent"]["results"]) == 2
    # Reranked reverse order.
    assert payload["structuredContent"]["results"][0]["chunk_id"] == "b"


@pytest.mark.unit
def test_query_knowledge_hub_validates_arguments() -> None:
    with pytest.raises(ValueError, match="query must be a non-empty string"):
        query_knowledge_hub.call({"query": ""}, {"settings": {}})
    with pytest.raises(TypeError, match="top_k must be an integer"):
        query_knowledge_hub.call({"query": "x", "top_k": "2"}, {"settings": {}})
