"""Unit tests for dashboard config service (G1)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from observability.dashboard.services.config_service import ConfigService, SettingsError


def _settings_yaml(tmp_path: Path) -> str:
    persist_dir = tmp_path / "chroma"
    traces_path = tmp_path / "logs" / "traces.jsonl"
    image_root = tmp_path / "images"
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
  persist_directory: {persist_dir.as_posix()}
retrieval:
  top_k: 5
rerank:
  enabled: false
  provider: none
evaluation:
  provider: custom
observability:
  traces_path: {traces_path.as_posix()}
  app_log_path: {tmp_path.as_posix()}/app.log
ingestion:
  image_storage:
    image_root: {image_root.as_posix()}
"""


@pytest.mark.unit
def test_build_overview_reads_component_and_local_stats(tmp_path: Path) -> None:
    settings_file = tmp_path / "settings.yaml"
    settings_file.write_text(_settings_yaml(tmp_path), encoding="utf-8")

    chroma_dir = tmp_path / "chroma"
    chroma_dir.mkdir(parents=True)
    (chroma_dir / "kb.json").write_text(
        json.dumps({"records": {"a": {"id": "a"}, "b": {"id": "b"}}}),
        encoding="utf-8",
    )
    (tmp_path / "logs").mkdir(parents=True)
    (tmp_path / "logs" / "traces.jsonl").write_text('{"trace_id":"1"}\n{"trace_id":"2"}\n', encoding="utf-8")
    image_dir = tmp_path / "images"
    image_dir.mkdir(parents=True)
    (image_dir / "img1.png").write_bytes(b"img")

    overview = ConfigService(str(settings_file)).build_overview()

    assert overview.stats["collections"] == 1
    assert overview.stats["chunks"] == 2
    assert overview.stats["traces"] == 2
    assert overview.stats["images"] == 1
    assert any(item["name"] == "LLM" for item in overview.components)


@pytest.mark.unit
def test_build_overview_raises_settings_error_for_missing_file(tmp_path: Path) -> None:
    service = ConfigService(str(tmp_path / "missing.yaml"))

    with pytest.raises(SettingsError, match="Settings file not found"):
        service.build_overview()


@pytest.mark.unit
def test_build_overview_ignores_invalid_collection_json(tmp_path: Path) -> None:
    settings_file = tmp_path / "settings.yaml"
    settings_file.write_text(_settings_yaml(tmp_path), encoding="utf-8")

    chroma_dir = tmp_path / "chroma"
    chroma_dir.mkdir(parents=True)
    (chroma_dir / "bad.json").write_text("{not-json", encoding="utf-8")
    (chroma_dir / "ok.json").write_text(
        json.dumps({"records": {"a": {"id": "a"}}}),
        encoding="utf-8",
    )

    overview = ConfigService(str(settings_file)).build_overview()

    assert overview.stats["collections"] == 2
    assert overview.stats["chunks"] == 1


@pytest.mark.unit
def test_build_overview_counts_only_non_empty_trace_lines(tmp_path: Path) -> None:
    settings_file = tmp_path / "settings.yaml"
    settings_file.write_text(_settings_yaml(tmp_path), encoding="utf-8")
    (tmp_path / "logs").mkdir(parents=True)
    (tmp_path / "logs" / "traces.jsonl").write_text("\n{\"trace_id\":\"1\"}\n\n", encoding="utf-8")

    overview = ConfigService(str(settings_file)).build_overview()

    assert overview.stats["traces"] == 1
