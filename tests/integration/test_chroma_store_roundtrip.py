"""Integration tests for ChromaStore upsert/query persistence roundtrip."""

from __future__ import annotations

from pathlib import Path

import pytest

from libs.vector_store.chroma_store import ChromaStore
from libs.vector_store.vector_store_factory import VectorStoreFactory


@pytest.mark.integration
def test_factory_create_routes_chroma_provider(tmp_path: Path) -> None:
    store = VectorStoreFactory.create(
        {
            "vector_store": {
                "provider": "chroma",
                "collection_name": "docs",
                "persist_directory": str(tmp_path),
            }
        }
    )

    assert isinstance(store, ChromaStore)


@pytest.mark.integration
def test_chroma_store_upsert_query_roundtrip_with_filters(tmp_path: Path) -> None:
    store = ChromaStore(collection_name="docs", persist_directory=str(tmp_path))
    inserted = store.upsert(
        [
            {
                "id": "d1",
                "vector": [1.0, 0.0, 0.0],
                "text": "first",
                "metadata": {"source": "a"},
            },
            {
                "id": "d2",
                "vector": [0.7, 0.7, 0.0],
                "text": "second",
                "metadata": {"source": "a"},
            },
            {
                "id": "d3",
                "vector": [0.0, 1.0, 0.0],
                "text": "third",
                "metadata": {"source": "b"},
            },
        ]
    )

    assert inserted == 3

    matches = store.query(vector=[1.0, 0.0, 0.0], top_k=2)
    assert len(matches) == 2
    assert matches[0]["id"] == "d1"

    filtered = store.query(vector=[1.0, 0.0, 0.0], top_k=3, filters={"source": "a"})
    assert [item["id"] for item in filtered] == ["d1", "d2"]


@pytest.mark.integration
def test_chroma_store_persistence_across_instances(tmp_path: Path) -> None:
    first = ChromaStore(collection_name="persisted", persist_directory=str(tmp_path))
    first.upsert(
        [
            {"id": "x1", "vector": [0.2, 0.8], "text": "alpha", "metadata": {"k": 1}},
            {"id": "x2", "vector": [0.8, 0.2], "text": "beta", "metadata": {"k": 2}},
        ]
    )

    second = ChromaStore(collection_name="persisted", persist_directory=str(tmp_path))
    matches = second.query(vector=[0.8, 0.2], top_k=1)

    assert len(matches) == 1
    assert matches[0]["id"] == "x2"
