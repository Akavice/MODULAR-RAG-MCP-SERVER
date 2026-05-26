"""Additional contract tests for BM25Indexer behavior."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from core.types import ChunkRecord
from ingestion.storage.bm25_indexer import BM25Indexer


def _record(chunk_id: str, source: str, sparse: dict[str, float]) -> ChunkRecord:
    return ChunkRecord(
        id=chunk_id,
        text=chunk_id,
        metadata={"source_path": source},
        dense_vector=None,
        sparse_vector=sparse,
    )


@pytest.mark.unit
def test_upsert_same_chunk_id_overwrites_instead_of_duplicating(tmp_path: Path) -> None:
    indexer = BM25Indexer(settings={}, index_dir=str(tmp_path / "bm25"))
    indexer.upsert([_record("c1", "docs/a.pdf", {"alpha": 1.0})])
    indexer.upsert([_record("c1", "docs/a.pdf", {"beta": 2.0})])

    assert indexer.doc_count == 1
    assert "alpha" not in indexer.inverted_index
    assert "beta" in indexer.inverted_index


@pytest.mark.unit
def test_remove_document_persists_after_reload(tmp_path: Path) -> None:
    index_dir = tmp_path / "bm25"
    indexer = BM25Indexer(settings={}, index_dir=str(index_dir))
    indexer.upsert(
        [
            _record("c1", "docs/a.pdf", {"alpha": 1.0}),
            _record("c2", "docs/b.pdf", {"beta": 1.0}),
        ]
    )
    removed = indexer.remove_document("docs/a.pdf")
    assert removed == 1

    reloaded = BM25Indexer(settings={}, index_dir=str(index_dir))
    reloaded.load()
    assert reloaded.doc_count == 1
    assert all(item["chunk_id"] != "c1" for item in reloaded.query(["alpha"], top_k=5))


@pytest.mark.unit
def test_query_order_tie_breaks_by_chunk_id(tmp_path: Path) -> None:
    indexer = BM25Indexer(settings={}, index_dir=str(tmp_path / "bm25"))
    indexer.upsert(
        [
            _record("c2", "docs/a.pdf", {"shared": 1.0}),
            _record("c1", "docs/b.pdf", {"shared": 1.0}),
        ]
    )

    results = indexer.query(["shared"], top_k=2)
    assert [row["chunk_id"] for row in results] == ["c1", "c2"]


@pytest.mark.unit
def test_settings_index_dir_is_resolved(tmp_path: Path) -> None:
    configured = tmp_path / "custom_bm25"
    indexer = BM25Indexer(
        settings={"ingestion": {"bm25_indexer": {"index_dir": str(configured)}}}
    )
    indexer.upsert([_record("c1", "docs/a.pdf", {"alpha": 1.0})])

    assert (configured / "index.json").exists()


@pytest.mark.unit
def test_load_rejects_invalid_payload_shape(tmp_path: Path) -> None:
    index_dir = tmp_path / "bm25"
    index_dir.mkdir(parents=True, exist_ok=True)
    (index_dir / "index.json").write_text(
        json.dumps({"doc_vectors": [], "doc_sources": {}}),
        encoding="utf-8",
    )
    indexer = BM25Indexer(settings={}, index_dir=str(index_dir))

    with pytest.raises(ValueError, match="missing required mappings"):
        indexer.load()

