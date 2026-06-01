"""Dashboard data browser service."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from core.settings import SettingsError, load_settings
from ingestion.document_manager import DocumentDetail, DocumentInfo, DocumentManager
from ingestion.storage.bm25_indexer import BM25Indexer
from ingestion.storage.image_storage import ImageStorage
from libs.loader.file_integrity import SQLiteIntegrityChecker
from libs.vector_store.chroma_store import ChromaStore


@dataclass(slots=True)
class BrowserDocument:
    """Dashboard-facing document row payload."""

    doc_id: str
    source_path: str
    collection: str
    chunk_count: int
    image_count: int
    ingested_at: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "source_path": self.source_path,
            "collection": self.collection,
            "chunk_count": self.chunk_count,
            "image_count": self.image_count,
            "ingested_at": self.ingested_at,
        }


class DataService:
    """Provide document/chunk/image browse data for dashboard pages."""

    def __init__(
        self,
        settings_path: str = "config/settings.yaml",
        *,
        document_manager: DocumentManager | None = None,
    ) -> None:
        self.settings_path = settings_path
        self._document_manager = document_manager

    def list_collections(self) -> list[str]:
        docs = self.list_documents()
        values = sorted({item.collection for item in docs})
        return values

    def list_documents(self, collection: str | None = None) -> list[BrowserDocument]:
        manager = self._get_manager()
        rows = manager.list_documents(collection=collection)
        lookup = self._build_ingested_time_lookup()
        output: list[BrowserDocument] = []
        for item in rows:
            key = self._document_key(item.collection, item.source_path)
            output.append(
                BrowserDocument(
                    doc_id=item.doc_id,
                    source_path=item.source_path,
                    collection=item.collection,
                    chunk_count=item.chunk_count,
                    image_count=item.image_count,
                    ingested_at=lookup.get(key),
                )
            )
        return output

    def get_document_detail(self, doc_id: str) -> DocumentDetail:
        manager = self._get_manager()
        return manager.get_document_detail(doc_id)

    def get_document_manager(self) -> DocumentManager:
        return self._get_manager()

    def _get_manager(self) -> DocumentManager:
        if self._document_manager is not None:
            return self._document_manager

        settings = load_settings(self.settings_path)
        vector_store = ChromaStore(
            collection_name=self._resolve_collection_name(settings),
            persist_directory=str(settings.vector_store.get("persist_directory", "data/db/chroma")),
            embedding_provider=self._resolve_embedding_provider(settings),
            embedding_model=self._resolve_embedding_model(settings),
            embedding_dimension=self._resolve_embedding_dimension(settings),
        )
        bm25 = BM25Indexer(settings=settings)

        image_section = settings.ingestion.get("image_storage", {})
        image_storage = ImageStorage(
            image_root=str(image_section.get("image_root", "data/images")),
            db_path=str(image_section.get("db_path", "data/db/image_index.db")),
        )
        integrity = SQLiteIntegrityChecker(db_path=self._resolve_integrity_db_path(settings))
        self._document_manager = DocumentManager(
            chroma_store=vector_store,
            bm25_indexer=bm25,
            image_storage=image_storage,
            file_integrity=integrity,
        )
        return self._document_manager

    def _build_ingested_time_lookup(self) -> dict[str, str]:
        manager = self._get_manager()
        rows = manager.file_integrity.list_processed()
        output: dict[str, str] = {}
        for item in rows:
            if item.get("status") != "success":
                continue
            source_path = item.get("source_path")
            if not isinstance(source_path, str) or not source_path.strip():
                continue
            collection = item.get("collection")
            if not isinstance(collection, str) or not collection.strip():
                collection = getattr(manager.chroma_store, "collection_name", "default")
            if not isinstance(collection, str) or not collection.strip():
                collection = "default"
            ingested_at = item.get("created_at")
            if not isinstance(ingested_at, str) or not ingested_at.strip():
                continue
            key = self._document_key(collection.strip(), source_path)
            output[key] = ingested_at.strip()
        return output

    @staticmethod
    def _resolve_collection_name(settings: Any) -> str:
        value = settings.vector_store.get("collection_name", "default")
        if isinstance(value, str) and value.strip():
            return value.strip()
        return "default"

    @staticmethod
    def _resolve_embedding_provider(settings: Any) -> str | None:
        value = settings.embedding.get("provider")
        if isinstance(value, str) and value.strip():
            return value.strip()
        return None

    @staticmethod
    def _resolve_embedding_model(settings: Any) -> str | None:
        value = settings.embedding.get("model")
        if isinstance(value, str) and value.strip():
            return value.strip()
        return None

    @staticmethod
    def _resolve_embedding_dimension(settings: Any) -> int | None:
        value = settings.embedding.get("dimension")
        if isinstance(value, int) and not isinstance(value, bool) and value > 0:
            return value
        return None

    @staticmethod
    def _resolve_integrity_db_path(settings: Any) -> str:
        section = settings.ingestion.get("integrity_checker", {})
        if isinstance(section, dict):
            value = section.get("db_path")
            if isinstance(value, str) and value.strip():
                return value.strip()
        return SQLiteIntegrityChecker.DEFAULT_DB_PATH

    @staticmethod
    def _document_key(collection: str, source_path: str) -> str:
        normalized_source = str(Path(source_path).resolve())
        return f"{collection}\n{normalized_source}"


__all__ = ["DataService", "BrowserDocument", "SettingsError"]
