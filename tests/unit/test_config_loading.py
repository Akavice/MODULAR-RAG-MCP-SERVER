"""Unit tests for configuration loading."""

from pathlib import Path

import pytest

from core.settings import Settings, SettingsError, load_settings


VALID_SETTINGS = """\
llm:
  provider: openai
embedding:
  provider: openai
vector_store:
  provider: chroma
retrieval:
  top_k: 5
rerank:
  enabled: false
evaluation:
  provider: custom
observability:
  traces_path: logs/traces.jsonl
  app_log_path: logs/app.log
"""


def test_load_settings_returns_settings(tmp_path: Path) -> None:
    """Loading a valid YAML file should return a Settings object."""
    settings_file = tmp_path / "settings.yaml"
    settings_file.write_text(VALID_SETTINGS, encoding="utf-8")

    settings = load_settings(str(settings_file))

    assert isinstance(settings, Settings)
    assert settings.embedding["provider"] == "openai"
    assert settings.vector_store["provider"] == "chroma"


def test_load_settings_reports_missing_required_field(tmp_path: Path) -> None:
    """Missing nested required fields should raise a readable error."""
    settings_file = tmp_path / "settings.yaml"
    settings_file.write_text(
        """\
llm:
  provider: openai
embedding: {}
vector_store:
  provider: chroma
retrieval:
  top_k: 5
rerank:
  enabled: false
evaluation:
  provider: custom
observability:
  traces_path: logs/traces.jsonl
  app_log_path: logs/app.log
""",
        encoding="utf-8",
    )

    with pytest.raises(SettingsError, match="embedding.provider"):
        load_settings(str(settings_file))
