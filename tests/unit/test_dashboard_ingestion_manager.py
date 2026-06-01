"""Acceptance-oriented tests for dashboard ingestion manager page (G4)."""

from __future__ import annotations

import sys
from types import SimpleNamespace

import pytest

from observability.dashboard.pages import ingestion_manager


class _FakeStreamlit:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def title(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("title")

    def info(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("info")

    def file_uploader(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("file_uploader")
        return None

    def button(self, *_args: object, **_kwargs: object) -> bool:
        self.calls.append("button")
        return False

    def progress(self, *_args: object, **_kwargs: object) -> SimpleNamespace:
        self.calls.append("progress")
        return SimpleNamespace(progress=lambda *_a, **_k: None)

    def dataframe(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("dataframe")

    def warning(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("warning")


@pytest.mark.unit
def test_ingestion_manager_exposes_g4_operational_controls(monkeypatch: pytest.MonkeyPatch) -> None:
    """G4 page should provide upload/trigger/progress/doc-management interaction points."""
    fake_st = _FakeStreamlit()
    monkeypatch.setitem(sys.modules, "streamlit", fake_st)

    ingestion_manager.render({"settings_path": "config/settings.yaml"})

    assert "file_uploader" in fake_st.calls
    assert "button" in fake_st.calls
    assert "progress" in fake_st.calls
