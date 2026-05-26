"""Image file storage with SQLite-backed image-id index."""

from __future__ import annotations

import re
import sqlite3
import threading
from pathlib import Path
from typing import Any


class ImageStorage:
    """Persist images to local filesystem and index mapping in SQLite."""

    DEFAULT_IMAGE_ROOT = "data/images"
    DEFAULT_DB_PATH = "data/db/image_index.db"

    def __init__(
        self,
        *,
        image_root: str | None = None,
        db_path: str | None = None,
    ) -> None:
        self.image_root = Path(image_root or self.DEFAULT_IMAGE_ROOT)
        self.db_path = Path(db_path or self.DEFAULT_DB_PATH)
        self.image_root.mkdir(parents=True, exist_ok=True)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._initialize_database()

    def save_image(
        self,
        *,
        image_id: str,
        content: bytes,
        collection: str,
        doc_hash: str | None = None,
        page_num: int | None = None,
        suffix: str = ".png",
    ) -> str:
        """Save image bytes and upsert image_id->path mapping."""
        norm_image_id = self._normalize_non_empty(image_id, field_name="image_id")
        norm_collection = self._normalize_non_empty(collection, field_name="collection")
        norm_doc_hash = self._normalize_optional(doc_hash, field_name="doc_hash")
        norm_suffix = self._normalize_suffix(suffix)
        self._validate_content(content)
        if page_num is not None:
            if isinstance(page_num, bool) or not isinstance(page_num, int):
                raise TypeError("page_num must be an integer when provided")
            if page_num < 0:
                raise ValueError("page_num must be a non-negative integer")

        collection_dir = self.image_root / self._safe_segment(norm_collection)
        collection_dir.mkdir(parents=True, exist_ok=True)
        file_name = f"{self._safe_segment(norm_image_id)}{norm_suffix}"
        target = collection_dir / file_name
        target.write_bytes(content)

        path_value = str(target.resolve())
        old_path: str | None = None
        with self._lock:
            with self._connect() as connection:
                row = connection.execute(
                    "SELECT file_path FROM image_index WHERE image_id = ?",
                    (norm_image_id,),
                ).fetchone()
                if row and isinstance(row[0], str):
                    old_path = row[0]
                connection.execute(
                    """
                    INSERT INTO image_index (
                        image_id, file_path, collection, doc_hash, page_num
                    ) VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(image_id) DO UPDATE SET
                        file_path = excluded.file_path,
                        collection = excluded.collection,
                        doc_hash = excluded.doc_hash,
                        page_num = excluded.page_num
                    """,
                    (norm_image_id, path_value, norm_collection, norm_doc_hash, page_num),
                )
                connection.commit()

        if old_path and old_path != path_value:
            try:
                Path(old_path).unlink(missing_ok=True)
            except Exception:
                pass
        return path_value

    def get_path(self, image_id: str) -> str | None:
        """Get stored file path by image id, or None when not found."""
        norm_image_id = self._normalize_non_empty(image_id, field_name="image_id")
        with self._connect() as connection:
            row = connection.execute(
                "SELECT file_path FROM image_index WHERE image_id = ?",
                (norm_image_id,),
            ).fetchone()
        if not row:
            return None
        return str(row[0])

    def list_images(
        self,
        *,
        collection: str | None = None,
        doc_hash: str | None = None,
    ) -> list[dict[str, Any]]:
        """List image mappings filtered by collection/doc hash."""
        clauses: list[str] = []
        params: list[Any] = []

        if collection is not None:
            clauses.append("collection = ?")
            params.append(self._normalize_non_empty(collection, field_name="collection"))
        if doc_hash is not None:
            clauses.append("doc_hash = ?")
            params.append(self._normalize_non_empty(doc_hash, field_name="doc_hash"))

        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        sql = (
            "SELECT image_id, file_path, collection, doc_hash, page_num, created_at "
            f"FROM image_index {where} ORDER BY image_id"
        )
        with self._connect() as connection:
            rows = connection.execute(sql, tuple(params)).fetchall()

        return [
            {
                "image_id": str(row[0]),
                "file_path": str(row[1]),
                "collection": row[2],
                "doc_hash": row[3],
                "page_num": row[4],
                "created_at": row[5],
            }
            for row in rows
        ]

    def delete_image(self, image_id: str) -> bool:
        """Delete one image mapping and best-effort remove image file."""
        norm_image_id = self._normalize_non_empty(image_id, field_name="image_id")
        file_path = self.get_path(norm_image_id)

        deleted = 0
        with self._lock:
            with self._connect() as connection:
                cursor = connection.execute(
                    "DELETE FROM image_index WHERE image_id = ?",
                    (norm_image_id,),
                )
                deleted = cursor.rowcount
                connection.commit()

        if deleted and file_path:
            try:
                Path(file_path).unlink(missing_ok=True)
            except Exception:
                pass
        return bool(deleted)

    def delete_images(
        self,
        *,
        collection: str | None = None,
        doc_hash: str | None = None,
    ) -> int:
        """Delete image mappings by filters and remove corresponding files."""
        items = self.list_images(collection=collection, doc_hash=doc_hash)
        if not items:
            return 0

        ids = [item["image_id"] for item in items]
        file_paths = [item["file_path"] for item in items]

        placeholders = ",".join("?" for _ in ids)
        with self._lock:
            with self._connect() as connection:
                cursor = connection.execute(
                    f"DELETE FROM image_index WHERE image_id IN ({placeholders})",
                    tuple(ids),
                )
                deleted = cursor.rowcount
                connection.commit()

        for file_path in file_paths:
            try:
                Path(str(file_path)).unlink(missing_ok=True)
            except Exception:
                pass
        return int(deleted)

    def _initialize_database(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS image_index (
                    image_id TEXT PRIMARY KEY,
                    file_path TEXT NOT NULL,
                    collection TEXT,
                    doc_hash TEXT,
                    page_num INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_collection ON image_index(collection)"
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_doc_hash ON image_index(doc_hash)"
            )
            connection.commit()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.db_path,
            timeout=30.0,
            isolation_level=None,
            check_same_thread=False,
        )
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("PRAGMA synchronous=NORMAL")
        connection.execute("PRAGMA busy_timeout=30000")
        return connection

    @staticmethod
    def _safe_segment(value: str) -> str:
        safe = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
        return safe or "item"

    @staticmethod
    def _normalize_non_empty(value: Any, *, field_name: str) -> str:
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string")
        normalized = value.strip()
        if not normalized:
            raise ValueError(f"{field_name} must not be empty")
        return normalized

    @staticmethod
    def _normalize_optional(value: Any, *, field_name: str) -> str | None:
        if value is None:
            return None
        return ImageStorage._normalize_non_empty(value, field_name=field_name)

    @staticmethod
    def _normalize_suffix(value: Any) -> str:
        if not isinstance(value, str):
            raise TypeError("suffix must be a string")
        suffix = value.strip()
        if not suffix:
            raise ValueError("suffix must not be empty")
        if not suffix.startswith("."):
            suffix = f".{suffix}"
        if len(suffix) > 16 or re.search(r"[^A-Za-z0-9.]", suffix):
            raise ValueError("suffix contains invalid characters")
        return suffix.lower()

    @staticmethod
    def _validate_content(content: Any) -> None:
        if not isinstance(content, bytes):
            raise TypeError("content must be bytes")
        if not content:
            raise ValueError("content must not be empty")
