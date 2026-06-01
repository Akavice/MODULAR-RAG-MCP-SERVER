"""Unit tests for dashboard ingestion traces page (G5)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from observability.dashboard.pages import ingestion_traces


class _FakeStreamlit:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def title(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("title")

    def caption(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("caption")

    def metric(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("metric")

    def dataframe(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("dataframe")

    def selectbox(self, _label: str, options: list[str], index: int = 0) -> str:
        self.calls.append("selectbox")
        return options[index]

    def subheader(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("subheader")

    def bar_chart(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("bar_chart")

    def json(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("json")

    def info(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("info")

    def error(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("error")


def _write_settings(tmp_path: Path, traces_path: Path) -> Path:
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
  persist_directory: {tmp_path.as_posix()}/chroma
retrieval:
  top_k: 5
rerank:
  enabled: false
  provider: none
evaluation:
  provider: custom
observability:
  traces_path: {traces_path.as_posix()}
  app_log_path: {tmp_path.as_posix()}/logs/app.log
ingestion:
  image_storage:
    image_root: {tmp_path.as_posix()}/images
""",
        encoding="utf-8",
    )
    return settings_file


@pytest.mark.unit
def test_ingestion_traces_page_renders_history_and_waterfall(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    traces_path = tmp_path / "logs" / "traces.jsonl"
    traces_path.parent.mkdir(parents=True, exist_ok=True)
    traces_path.write_text(
        json.dumps(
            {
                "trace_id": "i-1",
                "trace_type": "ingestion",
                "started_at": "2026-06-01T10:00:00Z",
                "stages": [
                    {"stage": "load", "elapsed_ms": 12.0},
                    {"stage": "upsert", "elapsed_ms": 18.5},
                ],
            }
        ),
        encoding="utf-8",
    )
    settings_file = _write_settings(tmp_path, traces_path)

    fake_st = _FakeStreamlit()
    monkeypatch.setitem(sys.modules, "streamlit", fake_st)

    ingestion_traces.render({"settings_path": str(settings_file)})

    assert "metric" in fake_st.calls
    assert "dataframe" in fake_st.calls
    assert "selectbox" in fake_st.calls
    assert "bar_chart" in fake_st.calls
    assert "json" in fake_st.calls


@pytest.mark.unit
def test_ingestion_traces_page_shows_info_when_no_traces(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    traces_path = tmp_path / "logs" / "traces.jsonl"
    traces_path.parent.mkdir(parents=True, exist_ok=True)
    traces_path.write_text("", encoding="utf-8")
    settings_file = _write_settings(tmp_path, traces_path)

    fake_st = _FakeStreamlit()
    monkeypatch.setitem(sys.modules, "streamlit", fake_st)

    ingestion_traces.render({"settings_path": str(settings_file)})

    assert "metric" in fake_st.calls
    assert "info" in fake_st.calls


@pytest.mark.unit
def test_ingestion_traces_page_shows_error_when_settings_invalid(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_st = _FakeStreamlit()
    monkeypatch.setitem(sys.modules, "streamlit", fake_st)

    ingestion_traces.render({"settings_path": str(tmp_path / "missing.yaml")})

    assert "error" in fake_st.calls
    assert "info" in fake_st.calls
