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


@pytest.mark.integration
def test_chroma_store_rejects_signature_mismatch_on_reopen(tmp_path: Path) -> None:
    store = ChromaStore(
        collection_name="sig",
        persist_directory=str(tmp_path),
        embedding_provider="openai",
        embedding_model="text-embedding-3-small",
    )
    store.upsert([{"id": "id-1", "vector": [0.1, 0.2, 0.3], "metadata": {"k": 1}}])

    with pytest.raises(ValueError, match="embedding signature mismatch"):
        ChromaStore(
            collection_name="sig",
            persist_directory=str(tmp_path),
            embedding_provider="azure",
            embedding_model="text-embedding-ada-002",
        )


@pytest.mark.integration
def test_chroma_store_rejects_first_upsert_when_configured_dimension_differs(tmp_path: Path) -> None:
    store = ChromaStore(
        collection_name="sig_dim",
        persist_directory=str(tmp_path),
        embedding_dimension=4,
    )

    with pytest.raises(ValueError, match="dimension"):
        store.upsert([{"id": "id-1", "vector": [0.1, 0.2], "metadata": {"k": 1}}])


@pytest.mark.integration
def test_chroma_store_persists_dimension_signature_and_enforces_after_reopen(
    tmp_path: Path,
) -> None:
    first = ChromaStore(
        collection_name="persist_sig",
        persist_directory=str(tmp_path),
        embedding_dimension=3,
    )
    first.upsert([{"id": "p1", "vector": [0.1, 0.2, 0.3], "metadata": {"k": 1}}])

    # Reopen without explicit embedding signature config; stored signature should still apply.
    second = ChromaStore(collection_name="persist_sig", persist_directory=str(tmp_path))
    with pytest.raises(ValueError, match="dimension"):
        second.query(vector=[0.1, 0.2], top_k=1)
