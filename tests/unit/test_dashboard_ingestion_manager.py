"""Acceptance-oriented tests for dashboard ingestion manager page (G4)."""

from __future__ import annotations

import sys
from types import SimpleNamespace
from pathlib import Path

import pytest

from observability.dashboard.pages import ingestion_manager
from observability.dashboard.services.data_service import BrowserDocument


class _FakeStreamlit:
    def __init__(self) -> None:
        self.calls: list[str] = []
        self.messages: list[tuple[str, str]] = []
        self._button_results: dict[str, bool] = {}
        self._upload: object | None = None

    def title(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("title")

    def info(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("info")
        if _args:
            self.messages.append(("info", str(_args[0])))

    def file_uploader(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("file_uploader")
        return self._upload

    def button(self, label: str, *_args: object, **_kwargs: object) -> bool:
        self.calls.append("button")
        return self._button_results.get(label, False)

    def progress(self, *_args: object, **_kwargs: object) -> SimpleNamespace:
        self.calls.append("progress")
        return SimpleNamespace(progress=lambda *_a, **_k: self.calls.append("progress.update"))

    def dataframe(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("dataframe")

    def success(self, message: str) -> None:
        self.calls.append("success")
        self.messages.append(("success", message))

    def error(self, message: str) -> None:
        self.calls.append("error")
        self.messages.append(("error", message))

    def warning(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("warning")
        if _args:
            self.messages.append(("warning", str(_args[0])))

    def rerun(self) -> None:
        self.calls.append("rerun")


class _Upload:
    def __init__(self, name: str, payload: bytes) -> None:
        self.name = name
        self._payload = payload

    def getvalue(self) -> bytes:
        return self._payload


@pytest.mark.unit
def test_ingestion_manager_exposes_g4_operational_controls(monkeypatch: pytest.MonkeyPatch) -> None:
    """G4 page should provide upload/trigger/progress/doc-management interaction points."""
    fake_st = _FakeStreamlit()
    monkeypatch.setitem(sys.modules, "streamlit", fake_st)

    ingestion_manager.render({"settings_path": "config/settings.yaml"})

    assert "file_uploader" in fake_st.calls
    assert "button" in fake_st.calls
    assert "progress" in fake_st.calls


@pytest.mark.unit
def test_ingestion_manager_start_ingestion_triggers_pipeline(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    fake_st = _FakeStreamlit()
    fake_st._upload = _Upload("demo.pdf", b"%PDF-1.4\nfake")
    fake_st._button_results["Start Ingestion"] = True
    monkeypatch.setitem(sys.modules, "streamlit", fake_st)

    class _DocManager:
        def delete_document(self, source_path: str, collection: str) -> object:
            _ = source_path, collection
            return SimpleNamespace(deleted=False)

    class _Service:
        def __init__(self, settings_path: str) -> None:
            _ = settings_path

        def list_documents(self) -> list[BrowserDocument]:
            return []

        def get_document_manager(self) -> _DocManager:
            return _DocManager()

    run_calls: list[dict[str, object]] = []

    class _Pipeline:
        def __init__(self, settings: object) -> None:
            _ = settings

        def run(self, source_path: str, *, collection: str, force: bool, on_progress: object) -> object:
            run_calls.append({"source_path": source_path, "collection": collection, "force": force})
            assert callable(on_progress)
            on_progress("load", 2, 6)  # type: ignore[misc]
            return SimpleNamespace(status="ingested", chunk_count=1, record_count=1)

    monkeypatch.setattr(ingestion_manager, "DataService", _Service)
    monkeypatch.setattr(ingestion_manager, "load_settings", lambda _: {"x": 1})
    monkeypatch.setattr(ingestion_manager, "IngestionPipeline", _Pipeline)

    ingestion_manager.render({"settings_path": str(tmp_path / "settings.yaml")})

    assert run_calls
    assert run_calls[0]["collection"] == "default"
    assert any(level == "success" and "Ingestion ingested" in msg for level, msg in fake_st.messages)
    assert "progress.update" in fake_st.calls


@pytest.mark.unit
def test_ingestion_manager_delete_button_calls_document_manager(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_st = _FakeStreamlit()
    delete_label = "Delete [kb] a.pdf"
    fake_st._button_results[delete_label] = True
    monkeypatch.setitem(sys.modules, "streamlit", fake_st)

    calls: list[tuple[str, str]] = []

    class _DocManager:
        def delete_document(self, source_path: str, collection: str) -> object:
            calls.append((source_path, collection))
            return SimpleNamespace(deleted=True)

    class _Service:
        def __init__(self, settings_path: str) -> None:
            _ = settings_path

        def list_documents(self) -> list[BrowserDocument]:
            return [BrowserDocument("doc1", str(Path("/tmp/a.pdf")), "kb", 1, 0, None)]

        def get_document_manager(self) -> _DocManager:
            return _DocManager()

    monkeypatch.setattr(ingestion_manager, "DataService", _Service)
    monkeypatch.setattr(ingestion_manager, "load_settings", lambda _: {"x": 1})

    ingestion_manager.render({"settings_path": "config/settings.yaml"})

    assert calls == [(str(Path("/tmp/a.pdf")), "kb")]
    assert "rerun" in fake_st.calls
