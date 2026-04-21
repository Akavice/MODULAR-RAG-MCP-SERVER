"""Configuration loading and validation helpers."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


class SettingsError(ValueError):
    """Raised when the project configuration is missing required fields."""


@dataclass(slots=True)
class Settings:
    """Minimal structured settings container for early project phases."""

    llm: dict[str, Any]
    embedding: dict[str, Any]
    vector_store: dict[str, Any]
    retrieval: dict[str, Any]
    rerank: dict[str, Any]
    evaluation: dict[str, Any]
    observability: dict[str, Any]
    project: dict[str, Any] = field(default_factory=dict)


def load_settings(path: str) -> Settings:
    """Load YAML settings from disk and validate required fields."""
    config_path = Path(path)
    if not config_path.exists():
        raise SettingsError(f"Settings file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as handle:
        raw_settings = yaml.safe_load(handle) or {}

    if not isinstance(raw_settings, dict):
        raise SettingsError("Settings root must be a mapping")

    settings = Settings(
        project=_get_mapping(raw_settings, "project", required=False),
        llm=_get_mapping(raw_settings, "llm"),
        embedding=_get_mapping(raw_settings, "embedding"),
        vector_store=_get_mapping(raw_settings, "vector_store"),
        retrieval=_get_mapping(raw_settings, "retrieval"),
        rerank=_get_mapping(raw_settings, "rerank"),
        evaluation=_get_mapping(raw_settings, "evaluation"),
        observability=_get_mapping(raw_settings, "observability"),
    )
    validate_settings(settings)
    return settings


def validate_settings(settings: Settings) -> None:
    """Validate required settings fields with readable path-based errors."""
    required_fields = (
        ("llm.provider", settings.llm.get("provider")),
        ("embedding.provider", settings.embedding.get("provider")),
        ("vector_store.provider", settings.vector_store.get("provider")),
        ("retrieval.top_k", settings.retrieval.get("top_k")),
        ("rerank.enabled", settings.rerank.get("enabled")),
        ("evaluation.provider", settings.evaluation.get("provider")),
        ("observability.traces_path", settings.observability.get("traces_path")),
        ("observability.app_log_path", settings.observability.get("app_log_path")),
    )

    for field_path, value in required_fields:
        if value is None or value == "":
            raise SettingsError(f"Missing required setting: {field_path}")


def _get_mapping(
    raw_settings: dict[str, Any],
    key: str,
    *,
    required: bool = True,
) -> dict[str, Any]:
    """Return a mapping section or raise a readable configuration error."""
    value = raw_settings.get(key)
    if value is None:
        if required:
            raise SettingsError(f"Missing required setting: {key}")
        return {}
    if not isinstance(value, dict):
        raise SettingsError(f"Setting '{key}' must be a mapping")
    return value
