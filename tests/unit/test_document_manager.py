"""Unit tests for cross-storage DocumentManager lifecycle operations (G2)."""

from __future__ import annotations

from pathlib import Path

import pytest

from core.types import ChunkRecord
from ingestion.document_manager import DocumentManager
from ingestion.storage.bm25_indexer import BM25Indexer
from ingestion.storage.image_storage import ImageStorage
from libs.loader.file_integrity import SQLiteIntegrityChecker
from libs.vector_store.chroma_store import ChromaStore


def _build_manager(tmp_path: Path) -> tuple[DocumentManager, ChromaStore, BM25Indexer]:
    settings = {
        "ingestion": {
            "bm25_indexer": {"index_dir": str(tmp_path / "bm25")},
        }
    }
    chroma = ChromaStore(
        collection_name="kb",
        persist_directory=str(tmp_path / "chroma"),
    )
    bm25 = BM25Indexer(settings=settings)
    image_storage = ImageStorage(
        image_root=str(tmp_path / "images"),
        db_path=str(tmp_path / "db" / "image.db"),
    )
    integrity = SQLiteIntegrityChecker(db_path=str(tmp_path / "db" / "integrity.db"))
    manager = DocumentManager(
        chroma_store=chroma,
        bm25_indexer=bm25,
        image_storage=image_storage,
        file_integrity=integrity,
    )
    return manager, chroma, bm25


@pytest.mark.unit
def test_list_documents_merges_vector_and_integrity_sources(tmp_path: Path) -> None:
    manager, chroma, bm25 = _build_manager(tmp_path)
    source_a = str((tmp_path / "a.pdf").resolve())
    source_b = str((tmp_path / "b.pdf").resolve())

    manager.file_integrity.mark_success(
        "hash-a",
        source_a,
        source_path=source_a,
        collection="kb",
    )
    manager.file_integrity.mark_success(
        "hash-b",
        source_b,
        source_path=source_b,
        collection="kb",
    )

    chroma.upsert(
        [
            {
                "id": "c1",
                "vector": [1.0, 0.0, 0.0],
                "text": "chunk one",
                "metadata": {
                    "source_path": source_a,
                    "chunk_index": 0,
                    "images": [{"id": "img-a-1", "path": "/tmp/a1.png"}],
                },
            },
            {
                "id": "c2",
                "vector": [0.0, 1.0, 0.0],
                "text": "chunk two",
                "metadata": {
                    "source_path": source_a,
                    "chunk_index": 1,
                    "images": [{"id": "img-a-2", "path": "/tmp/a2.png"}],
                },
            },
        ]
    )
    bm25.upsert(
        [
            ChunkRecord(
                id="c1",
                text="chunk one",
                metadata={"source_path": source_a},
                sparse_vector={"chunk": 1.0},
            ),
            ChunkRecord(
                id="c2",
                text="chunk two",
                metadata={"source_path": source_a},
                sparse_vector={"chunk": 1.0},
            ),
        ]
    )
    manager.image_storage.save_image(
        image_id="img-a-1",
        content=b"img-a-1",
        collection="kb",
        doc_hash="hash-a",
    )
    manager.image_storage.save_image(
        image_id="img-b-1",
        content=b"img-b-1",
        collection="kb",
        doc_hash="hash-b",
    )

    docs = manager.list_documents(collection="kb")

    assert len(docs) == 2
    by_source = {item.source_path: item for item in docs}
    assert by_source[source_a].chunk_count == 2
    assert by_source[source_a].image_count == 2
    assert by_source[source_b].chunk_count == 0
    assert by_source[source_b].image_count == 1


@pytest.mark.unit
def test_get_document_detail_returns_sorted_chunks_and_file_hashes(tmp_path: Path) -> None:
    manager, chroma, bm25 = _build_manager(tmp_path)
    source = str((tmp_path / "doc.pdf").resolve())
    manager.file_integrity.mark_success(
        "hash-doc",
        source,
        source_path=source,
        collection="kb",
    )

    chroma.upsert(
        [
            {
                "id": "chunk-2",
                "vector": [0.1, 0.2],
                "text": "second",
                "metadata": {"source_path": source, "chunk_index": 2},
            },
            {
                "id": "chunk-1",
                "vector": [0.2, 0.1],
                "text": "first",
                "metadata": {"source_path": source, "chunk_index": 1},
            },
        ]
    )
    bm25.upsert(
        [
            ChunkRecord(
                id="chunk-2",
                text="second",
                metadata={"source_path": source},
                sparse_vector={"x": 1.0},
            )
        ]
    )

    doc_id = manager.list_documents(collection="kb")[0].doc_id
    detail = manager.get_document_detail(doc_id)

    assert detail.source_path == source
    assert [item["id"] for item in detail.chunks] == ["chunk-1", "chunk-2"]
    assert detail.file_hashes == ["hash-doc"]


@pytest.mark.unit
def test_delete_document_removes_all_related_storage_entries(tmp_path: Path) -> None:
    manager, chroma, bm25 = _build_manager(tmp_path)
    source = str((tmp_path / "doc.pdf").resolve())
    manager.file_integrity.mark_success(
        "hash-doc",
        source,
        source_path=source,
        collection="kb",
    )
    chroma.upsert(
        [
            {
                "id": "chunk-1",
                "vector": [1.0, 0.0],
                "text": "hello",
                "metadata": {"source_path": source},
            }
        ]
    )
    bm25.upsert(
        [
            ChunkRecord(
                id="chunk-1",
                text="hello",
                metadata={"source_path": source},
                sparse_vector={"hello": 1.0},
            )
        ]
    )
    manager.image_storage.save_image(
        image_id="img-1",
        content=b"img",
        collection="kb",
        doc_hash="hash-doc",
    )

    result = manager.delete_document(source, "kb")

    assert result.deleted is True
    assert result.removed_chunks == 1
    assert result.removed_bm25 == 1
    assert result.removed_images == 1
    assert result.removed_integrity_records == 1
    assert manager.file_integrity.should_skip("hash-doc") is False
    assert bm25.query(["hello"], top_k=5) == []
    assert chroma.query(vector=[1.0, 0.0], top_k=5) == []


@pytest.mark.unit
def test_get_collection_stats_aggregates_counts(tmp_path: Path) -> None:
    manager, chroma, _ = _build_manager(tmp_path)
    source = str((tmp_path / "doc.pdf").resolve())
    manager.file_integrity.mark_success(
        "hash-doc",
        source,
        source_path=source,
        collection="kb",
    )
    chroma.upsert(
        [
            {
                "id": "chunk-1",
                "vector": [1.0, 0.0],
                "text": "hello",
                "metadata": {"source_path": source},
            }
        ]
    )

    stats = manager.get_collection_stats("kb")

    assert stats.collection == "kb"
    assert stats.document_count == 1
    assert stats.chunk_count == 1
    assert stats.image_count == 0


@pytest.mark.unit
def test_get_document_detail_raises_for_unknown_doc_id(tmp_path: Path) -> None:
    manager, _, _ = _build_manager(tmp_path)

    with pytest.raises(ValueError, match="document not found"):
        manager.get_document_detail("doc_missing")


@pytest.mark.unit
def test_delete_document_returns_not_deleted_when_no_match(tmp_path: Path) -> None:
    manager, _, _ = _build_manager(tmp_path)
    source = str((tmp_path / "none.pdf").resolve())

    result = manager.delete_document(source, "kb")

    assert result.deleted is False
    assert result.removed_chunks == 0
    assert result.removed_bm25 == 0
    assert result.removed_images == 0
    assert result.removed_integrity_records == 0
