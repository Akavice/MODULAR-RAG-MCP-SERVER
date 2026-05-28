"""Unit tests for list_collections MCP tool."""

from __future__ import annotations

from pathlib import Path

import pytest

from mcp_server.tools import list_collections


@pytest.mark.unit
def test_list_collections_returns_sorted_collection_names(tmp_path: Path) -> None:
    persist = tmp_path / "chroma"
    persist.mkdir(parents=True)
    (persist / "zeta.json").write_text("{}", encoding="utf-8")
    (persist / "alpha.json").write_text("{}", encoding="utf-8")
    (persist / "ignore.tmp").write_text("{}", encoding="utf-8")

    payload = list_collections.call(
        {},
        {"settings": {"vector_store": {"persist_directory": str(persist)}}},
    )

    assert payload["structuredContent"]["collections"] == ["alpha", "zeta"]


@pytest.mark.unit
def test_list_collections_rejects_arguments(tmp_path: Path) -> None:
    persist = tmp_path / "chroma"
    persist.mkdir(parents=True)
    with pytest.raises(ValueError, match="does not accept arguments"):
        list_collections.call(
            {"x": 1},
            {"settings": {"vector_store": {"persist_directory": str(persist)}}},
        )
