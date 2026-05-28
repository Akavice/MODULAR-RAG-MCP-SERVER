"""Unit tests for get_document_summary MCP tool."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mcp_server.tools import get_document_summary


def _write_collection(path: Path) -> None:
    payload = {
        "collection_name": "default",
        "records": {
            "doc1_0000_x": {
                "id": "doc1_0000_x",
                "text": "First chunk content",
                "metadata": {
                    "source_path": "docs/a.pdf",
                    "source_ref": "doc1",
                    "title": "Doc One",
                    "tags": ["rag", "intro"],
                },
            },
            "doc1_0001_y": {
                "id": "doc1_0001_y",
                "text": "Second chunk content",
                "metadata": {"source_path": "docs/a.pdf", "source_ref": "doc1"},
            },
        },
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


@pytest.mark.unit
def test_get_document_summary_returns_structured_payload(tmp_path: Path) -> None:
    persist = tmp_path / "chroma"
    persist.mkdir(parents=True)
    _write_collection(persist / "default.json")

    payload = get_document_summary.call(
        {"doc_id": "doc1"},
        {"settings": {"vector_store": {"persist_directory": str(persist)}}},
    )

    summary = payload["structuredContent"]
    assert summary["doc_id"] == "doc1"
    assert summary["title"] == "Doc One"
    assert summary["chunk_count"] == 2
    assert "rag" in summary["tags"]


@pytest.mark.unit
def test_get_document_summary_raises_for_missing_doc(tmp_path: Path) -> None:
    persist = tmp_path / "chroma"
    persist.mkdir(parents=True)
    _write_collection(persist / "default.json")

    with pytest.raises(ValueError, match="not found"):
        get_document_summary.call(
            {"doc_id": "missing"},
            {"settings": {"vector_store": {"persist_directory": str(persist)}}},
        )
