"""Unit tests for SQLite-backed file integrity checker."""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

import pytest

from libs.loader.file_integrity import SQLiteIntegrityChecker


@pytest.mark.unit
def test_compute_sha256_is_deterministic(tmp_path: Path) -> None:
    sample = tmp_path / "doc.txt"
    sample.write_text("same-content", encoding="utf-8")
    checker = SQLiteIntegrityChecker(db_path=str(tmp_path / "db" / "history.db"))

    hash_1 = checker.compute_sha256(str(sample))
    hash_2 = checker.compute_sha256(str(sample))

    assert hash_1 == hash_2
    assert len(hash_1) == 64


@pytest.mark.unit
def test_should_skip_true_after_mark_success(tmp_path: Path) -> None:
    db_path = tmp_path / "db" / "history.db"
    checker = SQLiteIntegrityChecker(db_path=str(db_path))
    file_hash = "abc123"

    assert checker.should_skip(file_hash) is False
    checker.mark_success(file_hash, file_path="docs/a.pdf", source_path="docs/a.pdf")
    assert checker.should_skip(file_hash) is True


@pytest.mark.unit
def test_default_db_path_created_under_cwd(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)

    checker = SQLiteIntegrityChecker()

    assert checker.db_path == Path("data/db/ingestion_history.db")
    assert (tmp_path / "data" / "db" / "ingestion_history.db").exists()


@pytest.mark.unit
def test_sqlite_wal_mode_enabled(tmp_path: Path) -> None:
    db_path = tmp_path / "db" / "history.db"
    checker = SQLiteIntegrityChecker(db_path=str(db_path))

    with sqlite3.connect(db_path) as connection:
        mode = connection.execute("PRAGMA journal_mode").fetchone()

    assert mode is not None
    assert str(mode[0]).lower() == "wal"


@pytest.mark.unit
def test_mark_failed_does_not_trigger_skip(tmp_path: Path) -> None:
    checker = SQLiteIntegrityChecker(db_path=str(tmp_path / "db" / "history.db"))
    file_hash = "failed-hash"

    checker.mark_failed(file_hash, "parse error")

    assert checker.should_skip(file_hash) is False
