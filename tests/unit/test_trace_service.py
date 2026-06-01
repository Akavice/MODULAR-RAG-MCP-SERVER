"""Unit tests for dashboard trace service (G5)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from core.settings import SettingsError
from observability.dashboard.services.trace_service import TraceService


def _settings_yaml(tmp_path: Path, traces_path: Path) -> str:
    return f"""\
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
"""


@pytest.mark.unit
def test_list_ingestion_traces_filters_sorts_and_skips_invalid_lines(tmp_path: Path) -> None:
    traces_path = tmp_path / "logs" / "traces.jsonl"
    traces_path.parent.mkdir(parents=True, exist_ok=True)
    traces_path.write_text(
        "\n".join(
            [
                json.dumps({"trace_id": "q-1", "trace_type": "query", "started_at": "2026-06-01T10:00:00Z"}),
                "not-json",
                json.dumps(
                    {
                        "trace_id": "i-1",
                        "trace_type": "ingestion",
                        "started_at": "2026-06-01T10:00:00Z",
                        "total_elapsed_ms": 42.5,
                        "stages": [
                            {"stage": "load", "elapsed_ms": 12.0, "source_path": "/a.pdf", "collection": "kb"},
                            {"stage": "upsert", "elapsed_ms": 30.5},
                        ],
                    }
                ),
                json.dumps(
                    {
                        "trace_id": "i-2",
                        "trace_type": "ingestion",
                        "started_at": "2026-06-01T11:00:00Z",
                        "stages": [],
                    }
                ),
            ]
        ),
        encoding="utf-8",
    )
    settings_file = tmp_path / "settings.yaml"
    settings_file.write_text(_settings_yaml(tmp_path, traces_path), encoding="utf-8")

    traces = TraceService(settings_path=str(settings_file)).list_ingestion_traces()

    assert [item.trace_id for item in traces] == ["i-2", "i-1"]
    assert traces[1].source_path == "/a.pdf"
    assert traces[1].collection == "kb"
    assert traces[1].stage_count == 2


@pytest.mark.unit
def test_build_stage_timeline_keeps_only_numeric_stage_elapsed(tmp_path: Path) -> None:
    traces_path = tmp_path / "logs" / "traces.jsonl"
    traces_path.parent.mkdir(parents=True, exist_ok=True)
    traces_path.write_text(
        json.dumps(
            {
                "trace_id": "i-1",
                "trace_type": "ingestion",
                "started_at": "2026-06-01T10:00:00Z",
                "stages": [
                    {"stage": "load", "elapsed_ms": 10.0},
                    {"stage": "split", "elapsed_ms": "x"},
                    {"stage": "", "elapsed_ms": 5.0},
                    {"stage": "upsert", "elapsed_ms": 20},
                ],
            }
        ),
        encoding="utf-8",
    )
    settings_file = tmp_path / "settings.yaml"
    settings_file.write_text(_settings_yaml(tmp_path, traces_path), encoding="utf-8")

    trace = TraceService(settings_path=str(settings_file)).list_ingestion_traces()[0]
    timeline = TraceService.build_stage_timeline(trace)

    assert timeline == [
        {"stage": "load", "elapsed_ms": 10.0},
        {"stage": "upsert", "elapsed_ms": 20.0},
    ]


@pytest.mark.unit
def test_list_traces_raises_settings_error_for_missing_file(tmp_path: Path) -> None:
    service = TraceService(settings_path=str(tmp_path / "missing.yaml"))

    with pytest.raises(SettingsError, match="Settings file not found"):
        service.list_ingestion_traces()


@pytest.mark.unit
def test_list_traces_rejects_invalid_limit_types(tmp_path: Path) -> None:
    traces_path = tmp_path / "logs" / "traces.jsonl"
    traces_path.parent.mkdir(parents=True, exist_ok=True)
    traces_path.write_text("", encoding="utf-8")
    settings_file = tmp_path / "settings.yaml"
    settings_file.write_text(_settings_yaml(tmp_path, traces_path), encoding="utf-8")
    service = TraceService(settings_path=str(settings_file))

    with pytest.raises(TypeError, match="limit must be an integer"):
        service.list_traces(limit="10")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="limit must be greater than 0"):
        service.list_traces(limit=0)
