"""Additional contract tests for ChromaStore edge behavior."""

from __future__ import annotations

from pathlib import Path

import pytest

from libs.vector_store.chroma_store import ChromaStore


@pytest.mark.integration
def test_chroma_store_rejects_query_dimension_mismatch(tmp_path: Path) -> None:
    store = ChromaStore(collection_name="dims", persist_directory=str(tmp_path))
    store.upsert(
        [
            {"id": "v1", "vector": [1.0, 0.0, 0.0], "metadata": {"group": "a"}},
            {"id": "v2", "vector": [0.0, 1.0, 0.0], "metadata": {"group": "b"}},
        ]
    )

    with pytest.raises(ValueError, match="dimension"):
        store.query(vector=[1.0, 0.0], top_k=2)


@pytest.mark.integration
def test_chroma_store_ignores_corrupted_collection_file(tmp_path: Path) -> None:
    collection_file = tmp_path / "broken.json"
    collection_file.write_text("{invalid json", encoding="utf-8")

    store = ChromaStore(collection_name="broken", persist_directory=str(tmp_path))
    matches = store.query(vector=[1.0], top_k=1)

    assert matches == []


@pytest.mark.integration
def test_chroma_store_sanitizes_collection_filename(tmp_path: Path) -> None:
    store = ChromaStore(collection_name="A/B:C*D?", persist_directory=str(tmp_path))
    store.upsert([{"id": "id-1", "vector": [1.0], "text": "x", "metadata": {"k": 1}}])

    files = {p.name for p in tmp_path.iterdir() if p.is_file()}
    assert "A_B_C_D_.json" in files

