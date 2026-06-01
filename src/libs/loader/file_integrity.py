"""File integrity checker implementations for ingestion deduplication."""

from __future__ import annotations

import hashlib
import json
import sqlite3
import threading
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class FileIntegrityChecker(ABC):
    """Abstract file integrity checker interface."""

    @abstractmethod
    def compute_sha256(self, path: str) -> str:
        """Compute deterministic file hash for ingestion deduplication."""

    @abstractmethod
    def should_skip(self, file_hash: str) -> bool:
        """Return True when this hash has already been processed successfully."""

    @abstractmethod
    def mark_success(self, file_hash: str, file_path: str, **extra: Any) -> None:
        """Mark a file hash as processed successfully."""

    @abstractmethod
    def mark_failed(self, file_hash: str, error_msg: str, **extra: Any) -> None:
        """Mark a file hash as failed with a readable error message."""

    @abstractmethod
    def remove_record(self, file_hash: str) -> bool:
        """Remove one file-hash record and return True when deleted."""

    @abstractmethod
    def list_processed(self) -> list[dict[str, Any]]:
        """List persisted ingestion records for management operations."""


class SQLiteIntegrityChecker(FileIntegrityChecker):
    """SQLite-backed integrity checker with WAL mode for concurrent writes."""

    DEFAULT_DB_PATH = "data/db/ingestion_history.db"

    def __init__(self, db_path: str | None = None) -> None:
        target = Path(db_path or self.DEFAULT_DB_PATH)
        self.db_path = target
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._initialize_database()

    def compute_sha256(self, path: str) -> str:
        file_path = Path(path)
        if not file_path.exists() or not file_path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        digest = hashlib.sha256()
        with file_path.open("rb") as handle:
            while True:
                chunk = handle.read(1024 * 1024)
                if not chunk:
                    break
                digest.update(chunk)
        return digest.hexdigest()

    def should_skip(self, file_hash: str) -> bool:
        normalized = self._normalize_file_hash(file_hash)
        with self._connect() as connection:
            row = connection.execute(
                "SELECT status FROM ingestion_history WHERE file_hash = ?",
                (normalized,),
            ).fetchone()
        return bool(row and row[0] == "success")

    def mark_success(self, file_hash: str, file_path: str, **extra: Any) -> None:
        normalized = self._normalize_file_hash(file_hash)
        normalized_path = self._normalize_file_path(file_path)
        self._upsert(
            file_hash=normalized,
            status="success",
            file_path=normalized_path,
            error_msg=None,
            extra=extra,
        )

    def mark_failed(self, file_hash: str, error_msg: str, **extra: Any) -> None:
        normalized = self._normalize_file_hash(file_hash)
        if not isinstance(error_msg, str) or not error_msg.strip():
            raise ValueError("error_msg must be a non-empty string")
        self._upsert(
            file_hash=normalized,
            status="failed",
            file_path=None,
            error_msg=error_msg.strip(),
            extra=extra,
        )

    def remove_record(self, file_hash: str) -> bool:
        normalized = self._normalize_file_hash(file_hash)
        with self._lock:
            with self._connect() as connection:
                cursor = connection.execute(
                    "DELETE FROM ingestion_history WHERE file_hash = ?",
                    (normalized,),
                )
                deleted = cursor.rowcount
                connection.commit()
        return bool(deleted)

    def list_processed(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT file_hash, status, file_path, error_msg, extra_json, created_at, updated_at
                FROM ingestion_history
                ORDER BY updated_at DESC, file_hash ASC
                """
            ).fetchall()

        output: list[dict[str, Any]] = []
        for row in rows:
            extra: dict[str, Any] = {}
            raw_extra = row[4]
            if isinstance(raw_extra, str) and raw_extra.strip():
                try:
                    parsed = json.loads(raw_extra)
                    if isinstance(parsed, dict):
                        extra = parsed
                except json.JSONDecodeError:
                    extra = {}

            source_path = extra.get("source_path")
            if not isinstance(source_path, str) or not source_path.strip():
                source_path = row[2] if isinstance(row[2], str) else None

            collection = extra.get("collection")
            if not isinstance(collection, str) or not collection.strip():
                collection = None

            output.append(
                {
                    "file_hash": row[0],
                    "status": row[1],
                    "file_path": row[2],
                    "error_msg": row[3],
                    "source_path": source_path,
                    "collection": collection,
                    "extra": extra,
                    "created_at": row[5],
                    "updated_at": row[6],
                }
            )
        return output

    def _initialize_database(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS ingestion_history (
                    file_hash TEXT PRIMARY KEY,
                    status TEXT NOT NULL CHECK (status IN ('success', 'failed')),
                    file_path TEXT,
                    error_msg TEXT,
                    extra_json TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            connection.execute(
                """
                CREATE TRIGGER IF NOT EXISTS trg_ingestion_history_updated_at
                AFTER UPDATE ON ingestion_history
                FOR EACH ROW
                BEGIN
                    UPDATE ingestion_history
                    SET updated_at = CURRENT_TIMESTAMP
                    WHERE file_hash = OLD.file_hash;
                END;
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_ingestion_history_status
                ON ingestion_history(status)
                """
            )
            connection.commit()

    def _upsert(
        self,
        *,
        file_hash: str,
        status: str,
        file_path: str | None,
        error_msg: str | None,
        extra: dict[str, Any],
    ) -> None:
        extra_json = None
        if extra:
            extra_json = json.dumps(extra, ensure_ascii=False, sort_keys=True)

        with self._lock:
            with self._connect() as connection:
                connection.execute(
                    """
                    INSERT INTO ingestion_history (
                        file_hash,
                        status,
                        file_path,
                        error_msg,
                        extra_json
                    ) VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(file_hash) DO UPDATE SET
                        status = excluded.status,
                        file_path = excluded.file_path,
                        error_msg = excluded.error_msg,
                        extra_json = excluded.extra_json
                    """,
                    (file_hash, status, file_path, error_msg, extra_json),
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
    def _normalize_file_hash(file_hash: str) -> str:
        if not isinstance(file_hash, str):
            raise TypeError("file_hash must be a string")
        normalized = file_hash.strip().lower()
        if not normalized:
            raise ValueError("file_hash must not be empty")
        return normalized

    @staticmethod
    def _normalize_file_path(file_path: str) -> str:
        if not isinstance(file_path, str):
            raise TypeError("file_path must be a string")
        normalized = file_path.strip()
        if not normalized:
            raise ValueError("file_path must not be empty")
        return normalized
