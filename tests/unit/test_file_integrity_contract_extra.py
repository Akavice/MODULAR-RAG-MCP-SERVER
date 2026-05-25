"""Additional contract tests for SQLiteIntegrityChecker edge behavior."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from libs.loader.file_integrity import SQLiteIntegrityChecker


@pytest.mark.unit
def test_should_skip_is_case_insensitive_for_file_hash(tmp_path: Path) -> None:
    checker = SQLiteIntegrityChecker(db_path=str(tmp_path / "db" / "history.db"))
    checker.mark_success("AbC123", file_path="docs/a.pdf")

    assert checker.should_skip("abc123") is True
    assert checker.should_skip("ABC123") is True


@pytest.mark.unit
def test_mark_success_overrides_previous_failed_status(tmp_path: Path) -> None:
    db_path = tmp_path / "db" / "history.db"
    checker = SQLiteIntegrityChecker(db_path=str(db_path))
    file_hash = "same-hash"

    checker.mark_failed(file_hash, "first error")
    assert checker.should_skip(file_hash) is False

    checker.mark_success(file_hash, file_path="docs/final.pdf")
    assert checker.should_skip(file_hash) is True

    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "SELECT status, file_path, error_msg FROM ingestion_history WHERE file_hash = ?",
            (file_hash,),
        ).fetchone()
    assert row == ("success", "docs/final.pdf", None)


@pytest.mark.unit
@pytest.mark.parametrize("bad_path", ["", "   ", 123])
def test_mark_success_rejects_invalid_file_path(tmp_path: Path, bad_path: object) -> None:
    checker = SQLiteIntegrityChecker(db_path=str(tmp_path / "db" / "history.db"))

    with pytest.raises((TypeError, ValueError), match="file_path"):
        checker.mark_success("hash-1", file_path=bad_path)  # type: ignore[arg-type]


@pytest.mark.unit
@pytest.mark.parametrize("bad_error", ["", "   ", 123])
def test_mark_failed_rejects_invalid_error_message(tmp_path: Path, bad_error: object) -> None:
    checker = SQLiteIntegrityChecker(db_path=str(tmp_path / "db" / "history.db"))

    with pytest.raises((TypeError, ValueError), match="error_msg"):
        checker.mark_failed("hash-1", bad_error)  # type: ignore[arg-type]


@pytest.mark.unit
def test_mark_success_persists_extra_json(tmp_path: Path) -> None:
    db_path = tmp_path / "db" / "history.db"
    checker = SQLiteIntegrityChecker(db_path=str(db_path))
    checker.mark_success(
        "hash-1",
        file_path="docs/a.pdf",
        source_path="docs/a.pdf",
        stage="ingestion",
    )

    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "SELECT extra_json FROM ingestion_history WHERE file_hash = ?",
            ("hash-1",),
        ).fetchone()

    assert row is not None
    payload = json.loads(row[0])
    assert payload["source_path"] == "docs/a.pdf"
    assert payload["stage"] == "ingestion"

