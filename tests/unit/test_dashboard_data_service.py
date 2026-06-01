"""Unit tests for dashboard DataService (G3)."""

from __future__ import annotations

from pathlib import Path

import pytest

from core.settings import SettingsError
from observability.dashboard.services.data_service import DataService
from observability.dashboard.services.data_service import BrowserDocument
from ingestion.storage.image_storage import ImageStorage
from libs.loader.file_integrity import SQLiteIntegrityChecker
from libs.vector_store.chroma_store import ChromaStore


def _write_settings(tmp_path: Path) -> Path:
    settings_file = tmp_path / "settings.yaml"
    settings_file.write_text(
        f"""\
project:
  name: test
llm:
  provider: openai
  model: gpt-4o-mini
embedding:
  provider: openai
  model: text-embedding-3-small
vector_store:
  provider: chroma
  collection_name: kb
  persist_directory: {tmp_path.as_posix()}/chroma
retrieval:
  top_k: 5
rerank:
  enabled: false
  provider: none
evaluation:
  provider: custom
observability:
  traces_path: {tmp_path.as_posix()}/logs/traces.jsonl
  app_log_path: {tmp_path.as_posix()}/logs/app.log
ingestion:
  integrity_checker:
    db_path: {tmp_path.as_posix()}/db/integrity.db
  image_storage:
    image_root: {tmp_path.as_posix()}/images
    db_path: {tmp_path.as_posix()}/db/image_index.db
  bm25_indexer:
    index_dir: {tmp_path.as_posix()}/db/bm25
""",
        encoding="utf-8",
    )
    return settings_file


@pytest.mark.unit
def test_data_service_lists_documents_and_detail(tmp_path: Path) -> None:
    settings_file = _write_settings(tmp_path)
    source_path = str((tmp_path / "sample.pdf").resolve())

    chroma = ChromaStore(
        collection_name="kb",
        persist_directory=str(tmp_path / "chroma"),
        embedding_provider="openai",
        embedding_model="text-embedding-3-small",
    )
    chroma.upsert(
        [
            {
                "id": "chunk-2",
                "vector": [0.2, 0.8],
                "text": "second",
                "metadata": {
                    "source_path": source_path,
                    "chunk_index": 2,
                    "images": [{"id": "img-1", "path": "/fake/a.png"}],
                },
            },
            {
                "id": "chunk-1",
                "vector": [0.8, 0.2],
                "text": "first",
                "metadata": {"source_path": source_path, "chunk_index": 1},
            },
        ]
    )

    integrity = SQLiteIntegrityChecker(db_path=str(tmp_path / "db" / "integrity.db"))
    integrity.mark_success(
        "hash-1",
        source_path,
        source_path=source_path,
        collection="kb",
    )

    image_storage = ImageStorage(
        image_root=str(tmp_path / "images"),
        db_path=str(tmp_path / "db" / "image_index.db"),
    )
    image_storage.save_image(
        image_id="img-1",
        content=b"image",
        collection="kb",
        doc_hash="hash-1",
    )

    service = DataService(settings_path=str(settings_file))
    docs = service.list_documents(collection="kb")

    assert len(docs) == 1
    assert docs[0].source_path == source_path
    assert docs[0].chunk_count == 2
    assert docs[0].image_count == 1
    assert docs[0].ingested_at is not None
    assert service.list_collections() == ["kb"]

    detail = service.get_document_detail(docs[0].doc_id)
    assert [item["id"] for item in detail.chunks] == ["chunk-1", "chunk-2"]
    assert detail.file_hashes == ["hash-1"]


@pytest.mark.unit
def test_data_service_raises_settings_error_for_missing_file(tmp_path: Path) -> None:
    service = DataService(settings_path=str(tmp_path / "missing.yaml"))

    with pytest.raises(SettingsError, match="Settings file not found"):
        service.list_documents()


@pytest.mark.unit
def test_list_collections_is_sorted_and_unique_with_injected_manager() -> None:
    class _Manager:
        def list_documents(self, collection: str | None = None) -> list[object]:
            _ = collection
            return [
                BrowserDocument("1", "/a", "kb", 1, 0, None),
                BrowserDocument("2", "/b", "zeta", 1, 0, None),
                BrowserDocument("3", "/c", "kb", 1, 0, None),
            ]

        @property
        def file_integrity(self) -> object:
            class _Integrity:
                @staticmethod
                def list_processed() -> list[dict[str, str]]:
                    return []

            return _Integrity()

    service = DataService(document_manager=_Manager())  # type: ignore[arg-type]

    assert service.list_collections() == ["kb", "zeta"]


@pytest.mark.unit
def test_list_documents_passes_collection_filter_to_manager() -> None:
    class _Manager:
        def __init__(self) -> None:
            self.last_collection: str | None = None

        def list_documents(self, collection: str | None = None) -> list[object]:
            self.last_collection = collection
            return [BrowserDocument("1", "/a", "kb", 1, 0, None)]

        @property
        def file_integrity(self) -> object:
            class _Integrity:
                @staticmethod
                def list_processed() -> list[dict[str, str]]:
                    return []

            return _Integrity()

    manager = _Manager()
    service = DataService(document_manager=manager)  # type: ignore[arg-type]

    _ = service.list_documents(collection="kb")

    assert manager.last_collection == "kb"
