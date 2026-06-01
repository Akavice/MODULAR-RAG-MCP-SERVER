"""Cross-storage document lifecycle manager for Dashboard and admin operations."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class DocumentInfo:
    """List-view payload for one ingested document."""

    doc_id: str
    source_path: str
    collection: str
    chunk_count: int
    image_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "source_path": self.source_path,
            "collection": self.collection,
            "chunk_count": self.chunk_count,
            "image_count": self.image_count,
        }


@dataclass(slots=True)
class DocumentDetail(DocumentInfo):
    """Detail-view payload with chunk-level records and file-hash bindings."""

    chunks: list[dict[str, Any]]
    file_hashes: list[str]

    def to_dict(self) -> dict[str, Any]:
        payload = super().to_dict()
        payload["chunks"] = [dict(item) for item in self.chunks]
        payload["file_hashes"] = list(self.file_hashes)
        return payload


@dataclass(slots=True)
class DeleteResult:
    """Deletion result for one source+collection document."""

    source_path: str
    collection: str
    removed_chunks: int
    removed_bm25: int
    removed_images: int
    removed_integrity_records: int

    @property
    def deleted(self) -> bool:
        return (
            self.removed_chunks > 0
            or self.removed_bm25 > 0
            or self.removed_images > 0
            or self.removed_integrity_records > 0
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_path": self.source_path,
            "collection": self.collection,
            "removed_chunks": self.removed_chunks,
            "removed_bm25": self.removed_bm25,
            "removed_images": self.removed_images,
            "removed_integrity_records": self.removed_integrity_records,
            "deleted": self.deleted,
        }


@dataclass(slots=True)
class CollectionStats:
    """Aggregated document/chunk/image counters."""

    collection: str
    document_count: int
    chunk_count: int
    image_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "collection": self.collection,
            "document_count": self.document_count,
            "chunk_count": self.chunk_count,
            "image_count": self.image_count,
        }


class DocumentManager:
    """Coordinate document management across vector/BM25/image/integrity stores."""

    def __init__(
        self,
        chroma_store: Any,
        bm25_indexer: Any,
        image_storage: Any,
        file_integrity: Any,
    ) -> None:
        self.chroma_store = chroma_store
        self.bm25_indexer = bm25_indexer
        self.image_storage = image_storage
        self.file_integrity = file_integrity

    def list_documents(self, collection: str | None = None) -> list[DocumentInfo]:
        normalized_collection = self._normalize_optional_collection(collection)
        grouped: dict[tuple[str, str], dict[str, Any]] = {}
        image_ids_by_key: dict[tuple[str, str], set[str]] = {}

        for record in self._iter_vector_records():
            metadata = record["metadata"]
            source_path = metadata.get("source_path")
            if not isinstance(source_path, str) or not source_path.strip():
                continue
            source_path = source_path.strip()
            record_collection = self._record_collection(metadata)
            if normalized_collection and record_collection != normalized_collection:
                continue
            key = (record_collection, source_path)

            item = grouped.setdefault(
                key,
                {
                    "collection": record_collection,
                    "source_path": source_path,
                    "chunk_count": 0,
                    "image_count": 0,
                },
            )
            item["chunk_count"] += 1
            image_ids = image_ids_by_key.setdefault(key, set())
            for image_id in self._extract_image_ids(metadata):
                image_ids.add(image_id)

        for integrity_item in self.file_integrity.list_processed():
            if integrity_item.get("status") != "success":
                continue
            source_path = integrity_item.get("source_path")
            if not isinstance(source_path, str) or not source_path.strip():
                continue
            source_path = source_path.strip()
            record_collection = self._resolve_integrity_collection(integrity_item)
            if normalized_collection and record_collection != normalized_collection:
                continue

            key = (record_collection, source_path)
            grouped.setdefault(
                key,
                {
                    "collection": record_collection,
                    "source_path": source_path,
                    "chunk_count": 0,
                },
            )

            file_hash = integrity_item.get("file_hash")
            if isinstance(file_hash, str) and file_hash.strip():
                images = self.image_storage.list_images(
                    collection=record_collection,
                    doc_hash=file_hash.strip(),
                )
                image_ids = image_ids_by_key.setdefault(key, set())
                for image_item in images:
                    image_id = image_item.get("image_id")
                    if isinstance(image_id, str) and image_id.strip():
                        image_ids.add(image_id.strip())

        for key, image_ids in image_ids_by_key.items():
            grouped[key]["image_count"] = len(image_ids)

        rows = sorted(
            grouped.values(),
            key=lambda item: (item["collection"], item["source_path"]),
        )
        return [
            DocumentInfo(
                doc_id=self._doc_id(item["collection"], item["source_path"]),
                source_path=item["source_path"],
                collection=item["collection"],
                chunk_count=int(item["chunk_count"]),
                image_count=int(item.get("image_count", 0)),
            )
            for item in rows
        ]

    def get_document_detail(self, doc_id: str) -> DocumentDetail:
        normalized_doc_id = self._normalize_non_empty(doc_id, field_name="doc_id")
        target: DocumentInfo | None = None
        for item in self.list_documents():
            if item.doc_id == normalized_doc_id:
                target = item
                break
        if target is None:
            raise ValueError(f"document not found: {normalized_doc_id}")

        chunks: list[dict[str, Any]] = []
        for record in self._iter_vector_records():
            metadata = record["metadata"]
            source_path = metadata.get("source_path")
            if not isinstance(source_path, str):
                continue
            if source_path.strip() != target.source_path:
                continue
            if self._record_collection(metadata) != target.collection:
                continue
            chunks.append(
                {
                    "id": record["id"],
                    "text": record["text"],
                    "metadata": dict(metadata),
                }
            )

        chunks.sort(
            key=lambda item: (
                int(item["metadata"].get("chunk_index", 0))
                if isinstance(item["metadata"].get("chunk_index"), int)
                else 0,
                str(item["id"]),
            )
        )
        file_hashes = self._find_file_hashes(
            source_path=target.source_path,
            collection=target.collection,
        )
        return DocumentDetail(
            doc_id=target.doc_id,
            source_path=target.source_path,
            collection=target.collection,
            chunk_count=target.chunk_count,
            image_count=target.image_count,
            chunks=chunks,
            file_hashes=file_hashes,
        )

    def delete_document(self, source_path: str, collection: str) -> DeleteResult:
        normalized_source = self._normalize_source_path(source_path)
        normalized_collection = self._normalize_non_empty(collection, field_name="collection")
        file_hashes = self._find_file_hashes(
            source_path=normalized_source,
            collection=normalized_collection,
        )

        removed_chunks = int(
            self.chroma_store.delete_by_metadata(
                {"source_path": normalized_source, "collection": normalized_collection}
            )
        )
        removed_bm25 = int(self.bm25_indexer.remove_document(normalized_source))

        removed_images = 0
        for file_hash in file_hashes:
            removed_images += int(
                self.image_storage.delete_images(
                    collection=normalized_collection,
                    doc_hash=file_hash,
                )
            )

        removed_integrity_records = 0
        for file_hash in file_hashes:
            if self.file_integrity.remove_record(file_hash):
                removed_integrity_records += 1

        return DeleteResult(
            source_path=normalized_source,
            collection=normalized_collection,
            removed_chunks=removed_chunks,
            removed_bm25=removed_bm25,
            removed_images=removed_images,
            removed_integrity_records=removed_integrity_records,
        )

    def get_collection_stats(self, collection: str | None = None) -> CollectionStats:
        docs = self.list_documents(collection=collection)
        return CollectionStats(
            collection=self._normalize_optional_collection(collection) or "all",
            document_count=len(docs),
            chunk_count=sum(item.chunk_count for item in docs),
            image_count=sum(item.image_count for item in docs),
        )

    def _iter_vector_records(self) -> list[dict[str, Any]]:
        raw = getattr(self.chroma_store, "_records", None)
        if not isinstance(raw, dict):
            return []
        records: list[dict[str, Any]] = []
        for item_id, item in raw.items():
            if not isinstance(item, dict):
                continue
            metadata = item.get("metadata", {})
            if not isinstance(metadata, dict):
                metadata = {}
            records.append(
                {
                    "id": str(item.get("id", item_id)),
                    "text": str(item.get("text", "")),
                    "metadata": dict(metadata),
                }
            )
        return records

    def _record_collection(self, metadata: dict[str, Any]) -> str:
        value = metadata.get("collection")
        if isinstance(value, str) and value.strip():
            return value.strip()
        fallback = getattr(self.chroma_store, "collection_name", "default")
        if isinstance(fallback, str) and fallback.strip():
            return fallback.strip()
        return "default"

    def _resolve_integrity_collection(self, row: dict[str, Any]) -> str:
        value = row.get("collection")
        if isinstance(value, str) and value.strip():
            return value.strip()
        fallback = getattr(self.chroma_store, "collection_name", "default")
        if isinstance(fallback, str) and fallback.strip():
            return fallback.strip()
        return "default"

    def _find_file_hashes(self, *, source_path: str, collection: str) -> list[str]:
        hashes: list[str] = []
        for item in self.file_integrity.list_processed():
            if item.get("status") != "success":
                continue
            row_source = item.get("source_path")
            if not isinstance(row_source, str):
                continue
            if self._normalize_source_path(row_source) != source_path:
                continue
            row_collection = self._resolve_integrity_collection(item)
            if row_collection != collection:
                continue
            file_hash = item.get("file_hash")
            if isinstance(file_hash, str) and file_hash.strip():
                hashes.append(file_hash.strip())
        return sorted(set(hashes))

    @staticmethod
    def _extract_image_ids(metadata: dict[str, Any]) -> list[str]:
        images = metadata.get("images")
        if not isinstance(images, list):
            return []
        output: list[str] = []
        for item in images:
            if not isinstance(item, dict):
                continue
            image_id = item.get("id")
            if isinstance(image_id, str) and image_id.strip():
                output.append(image_id.strip())
        return output

    @staticmethod
    def _doc_id(collection: str, source_path: str) -> str:
        digest = hashlib.sha256(f"{collection}\n{source_path}".encode("utf-8")).hexdigest()[:16]
        return f"doc_{digest}"

    @staticmethod
    def _normalize_non_empty(value: Any, *, field_name: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string")
        normalized = value.strip()
        if not normalized:
            raise ValueError(f"{field_name} must not be empty")
        return normalized

    @staticmethod
    def _normalize_optional_collection(value: str | None) -> str | None:
        if value is None:
            return None
        return DocumentManager._normalize_non_empty(value, field_name="collection")

    @staticmethod
    def _normalize_source_path(source_path: str) -> str:
        normalized = DocumentManager._normalize_non_empty(source_path, field_name="source_path")
        return str(Path(normalized).resolve())
