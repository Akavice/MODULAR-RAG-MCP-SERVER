"""Roundtrip tests for BM25Indexer."""

from __future__ import annotations

from pathlib import Path

import pytest

from core.types import ChunkRecord
from ingestion.storage.bm25_indexer import BM25Indexer


def _record(chunk_id: str, text: str, source: str, sparse: dict[str, float]) -> ChunkRecord:
    return ChunkRecord(
        id=chunk_id,
        text=text,
        metadata={"source_path": source},
        dense_vector=None,
        sparse_vector=sparse,
    )


@pytest.mark.unit
def test_roundtrip_persist_load_query_remove(tmp_path: Path) -> None:
    index_dir = tmp_path / "bm25"
    indexer = BM25Indexer(settings={}, index_dir=str(index_dir))
    records = [
        _record("c1", "alpha chunk", "docs/a.pdf", {"alpha": 1.0, "shared": 0.2}),
        _record("c2", "beta chunk", "docs/b.pdf", {"beta": 1.0, "shared": 0.2}),
        _record("c3", "alpha beta", "docs/a.pdf", {"alpha": 0.3, "beta": 0.4}),
    ]

    upserted = indexer.upsert(records)
    assert upserted == 3
    assert (index_dir / "index.json").exists()
    assert indexer.doc_count == 3
    assert "alpha" in indexer.idf
    assert "shared" in indexer.inverted_index

    reloaded = BM25Indexer(settings={}, index_dir=str(index_dir))
    reloaded.load()
    assert reloaded.doc_count == 3
    assert "alpha" in reloaded.inverted_index

    results = reloaded.query(["alpha"], top_k=2)
    assert len(results) == 2
    assert results[0]["chunk_id"] in {"c1", "c3"}
    assert results[0]["score"] >= results[1]["score"]

    removed = reloaded.remove_document("docs/a.pdf")
    assert removed == 2
    assert reloaded.doc_count == 1
    after = reloaded.query(["alpha"], top_k=5)
    assert after == []


@pytest.mark.unit
def test_load_missing_file_is_noop(tmp_path: Path) -> None:
    indexer = BM25Indexer(settings={}, index_dir=str(tmp_path / "missing"))

    indexer.load()

    assert indexer.doc_count == 0
    assert indexer.inverted_index == {}


@pytest.mark.unit
def test_query_and_remove_validate_inputs(tmp_path: Path) -> None:
    indexer = BM25Indexer(settings={}, index_dir=str(tmp_path / "bm25"))
    indexer.upsert([_record("c1", "x", "docs/a.pdf", {"x": 1.0})])

    with pytest.raises(TypeError, match="keywords must be a list"):
        indexer.query("x")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="top_k must be greater than 0"):
        indexer.query(["x"], top_k=0)
    with pytest.raises(ValueError, match="source must be a non-empty string"):
        indexer.remove_document("   ")


@pytest.mark.unit
def test_upsert_validates_record_type(tmp_path: Path) -> None:
    indexer = BM25Indexer(settings={}, index_dir=str(tmp_path / "bm25"))

    with pytest.raises(TypeError, match="ChunkRecord"):
        indexer.upsert([{"id": "x"}])  # type: ignore[list-item]
