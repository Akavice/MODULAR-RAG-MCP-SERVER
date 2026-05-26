"""E2E-style tests for ingest CLI behavior."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import pytest

from ingestion.pipeline import IngestionResult
from scripts import ingest as ingest_cli


class FakePipeline:
    """Stateful fake ingestion pipeline used to exercise CLI control flow."""

    seen_hashes: set[str] = set()

    def __init__(self, settings: Any) -> None:
        self.settings = settings

    def run(
        self,
        source_path: str,
        *,
        collection: str = "default",
        force: bool = False,
    ) -> IngestionResult:
        source = Path(source_path).resolve()
        file_hash = hashlib.sha256(source.read_bytes()).hexdigest()
        db_dir = Path(self.settings["vector_store"]["persist_directory"])
        bm25_dir = Path(self.settings["ingestion"]["bm25_indexer"]["index_dir"])
        db_dir.mkdir(parents=True, exist_ok=True)
        bm25_dir.mkdir(parents=True, exist_ok=True)

        if not force and file_hash in self.seen_hashes:
            return IngestionResult(
                status="skipped",
                source_path=str(source),
                collection=collection,
                file_hash=file_hash,
                document_id=None,
                chunk_count=0,
                record_count=0,
                vector_upserted=0,
                bm25_upserted=0,
                image_saved_count=0,
                trace_id="trace-skip",
                reason="already_ingested",
            )

        self.seen_hashes.add(file_hash)
        (db_dir / "default.json").write_text("{}", encoding="utf-8")
        (bm25_dir / "index.json").write_text("{}", encoding="utf-8")
        return IngestionResult(
            status="ingested",
            source_path=str(source),
            collection=collection,
            file_hash=file_hash,
            document_id="doc-1",
            chunk_count=1,
            record_count=1,
            vector_upserted=1,
            bm25_upserted=1,
            image_saved_count=0,
            trace_id="trace-ok",
            reason=None,
        )


def _settings_for(tmp_path: Path) -> dict[str, Any]:
    return {
        "vector_store": {"persist_directory": str(tmp_path / "data" / "db" / "chroma")},
        "ingestion": {
            "bm25_indexer": {"index_dir": str(tmp_path / "data" / "db" / "bm25")}
        },
    }


@pytest.mark.e2e
def test_ingest_cli_creates_db_artifacts_and_reports_ingested(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    FakePipeline.seen_hashes.clear()
    sample = tmp_path / "simple.pdf"
    sample.write_bytes(b"%PDF-1.4\nfake")

    monkeypatch.setattr(ingest_cli, "load_settings", lambda path: _settings_for(tmp_path))
    monkeypatch.setattr(ingest_cli, "IngestionPipeline", FakePipeline)

    code = ingest_cli.main(
        [
            "--path",
            str(sample),
            "--collection",
            "kb",
            "--config",
            str(tmp_path / "settings.yaml"),
        ]
    )

    stdout = capsys.readouterr().out
    assert code == 0
    assert "status=ingested" in stdout
    assert (tmp_path / "data" / "db" / "chroma" / "default.json").exists()
    assert (tmp_path / "data" / "db" / "bm25" / "index.json").exists()


@pytest.mark.e2e
def test_ingest_cli_skips_repeated_run_when_not_forced(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    FakePipeline.seen_hashes.clear()
    sample = tmp_path / "simple.pdf"
    sample.write_bytes(b"%PDF-1.4\nfake")
    settings = _settings_for(tmp_path)

    monkeypatch.setattr(ingest_cli, "load_settings", lambda path: settings)
    monkeypatch.setattr(ingest_cli, "IngestionPipeline", FakePipeline)

    first = ingest_cli.main(["--path", str(sample), "--config", str(tmp_path / "settings.yaml")])
    second = ingest_cli.main(["--path", str(sample), "--config", str(tmp_path / "settings.yaml")])
    stdout = capsys.readouterr().out

    assert first == 0
    assert second == 0
    assert stdout.count("status=ingested") == 1
    assert stdout.count("status=skipped") == 1


@pytest.mark.e2e
def test_ingest_cli_force_true_reingests_instead_of_skipping(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    FakePipeline.seen_hashes.clear()
    sample = tmp_path / "simple.pdf"
    sample.write_bytes(b"%PDF-1.4\nfake")
    settings = _settings_for(tmp_path)

    monkeypatch.setattr(ingest_cli, "load_settings", lambda path: settings)
    monkeypatch.setattr(ingest_cli, "IngestionPipeline", FakePipeline)

    first = ingest_cli.main(["--path", str(sample), "--config", str(tmp_path / "settings.yaml")])
    second = ingest_cli.main(
        ["--path", str(sample), "--force", "--config", str(tmp_path / "settings.yaml")]
    )
    stdout = capsys.readouterr().out

    assert first == 0
    assert second == 0
    assert stdout.count("status=ingested") == 2
    assert "status=skipped" not in stdout


@pytest.mark.e2e
def test_ingest_cli_returns_1_on_settings_error(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    sample = tmp_path / "simple.pdf"
    sample.write_bytes(b"%PDF-1.4\nfake")

    def _raise_settings_error(_: str) -> dict[str, Any]:
        raise ingest_cli.SettingsError("bad config")

    monkeypatch.setattr(ingest_cli, "load_settings", _raise_settings_error)

    code = ingest_cli.main(["--path", str(sample), "--config", str(tmp_path / "settings.yaml")])
    stdout = capsys.readouterr().out

    assert code == 1
    assert "configuration error" in stdout


@pytest.mark.e2e
def test_ingest_cli_returns_2_on_stage_error(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    sample = tmp_path / "simple.pdf"
    sample.write_bytes(b"%PDF-1.4\nfake")

    class FailingPipeline:
        def __init__(self, settings: Any) -> None:
            self.settings = settings

        def run(
            self,
            source_path: str,
            *,
            collection: str = "default",
            force: bool = False,
        ) -> IngestionResult:
            _ = source_path, collection, force
            raise ingest_cli.IngestionPipelineStageError("store", RuntimeError("boom"))

    monkeypatch.setattr(ingest_cli, "load_settings", lambda path: _settings_for(tmp_path))
    monkeypatch.setattr(ingest_cli, "IngestionPipeline", FailingPipeline)

    code = ingest_cli.main(["--path", str(sample), "--config", str(tmp_path / "settings.yaml")])
    stdout = capsys.readouterr().out

    assert code == 2
    assert "stage=store" in stdout
