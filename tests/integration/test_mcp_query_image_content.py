"""Integration test for MCP tools/call image content path (E6 acceptance)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from core.types import RetrievalResult
from mcp_server.protocol_handler import ProtocolHandler
from mcp_server.tools import build_tool_registry


class _FakeHybridSearch:
    def __init__(self, image_path: Path) -> None:
        self.image_path = image_path

    def search(
        self,
        query: str,
        top_k: int | None = None,
        filters: dict[str, Any] | None = None,
        trace: Any | None = None,
    ) -> list[RetrievalResult]:
        _ = (query, top_k, filters, trace)
        return [
            RetrievalResult(
                chunk_id="chunk-1",
                score=0.91,
                text="answer with image",
                metadata={
                    "source_path": "docs/a.pdf",
                    "images": [{"id": "img-1", "path": str(self.image_path)}],
                },
            )
        ]


class _FakeReranker:
    def rerank(
        self,
        query: str,
        candidates: list[RetrievalResult],
        trace: Any | None = None,
    ) -> list[RetrievalResult]:
        _ = (query, trace)
        return candidates


@pytest.mark.integration
def test_tools_call_query_knowledge_hub_returns_text_and_image_content(tmp_path: Path) -> None:
    image_path = tmp_path / "a.png"
    image_path.write_bytes(b"\x89PNG\r\n\x1a\nfake")

    handler = ProtocolHandler(
        settings={"vector_store": {"persist_directory": str(tmp_path)}},
        tool_registry=build_tool_registry(),
    )
    handler.context["hybrid_search"] = _FakeHybridSearch(image_path)
    handler.context["reranker"] = _FakeReranker()

    response = handler.handle_request(
        {
            "jsonrpc": "2.0",
            "id": 100,
            "method": "tools/call",
            "params": {
                "name": "query_knowledge_hub",
                "arguments": {"query": "what is this", "top_k": 1},
            },
        }
    )

    assert response is not None
    result = response["result"]
    content = result["content"]
    assert any(item.get("type") == "text" for item in content)
    images = [item for item in content if item.get("type") == "image"]
    assert len(images) == 1
    assert images[0]["mimeType"] == "image/png"
    assert isinstance(images[0]["data"], str) and len(images[0]["data"]) > 0
