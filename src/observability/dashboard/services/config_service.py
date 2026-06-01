"""Dashboard config/data summary service."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from core.settings import Settings, SettingsError, load_settings


@dataclass(slots=True)
class OverviewSnapshot:
    """Config and local data summary payload for dashboard overview."""

    settings: Settings
    components: list[dict[str, str]]
    stats: dict[str, int]


class ConfigService:
    """Load settings and derive lightweight local overview statistics."""

    def __init__(self, settings_path: str = "config/settings.yaml") -> None:
        self.settings_path = settings_path

    def build_overview(self) -> OverviewSnapshot:
        settings = load_settings(self.settings_path)
        return OverviewSnapshot(
            settings=settings,
            components=self._build_components(settings),
            stats=self._build_stats(settings),
        )

    @staticmethod
    def _build_components(settings: Settings) -> list[dict[str, str]]:
        return [
            {
                "name": "LLM",
                "provider": str(settings.llm.get("provider", "unknown")),
                "model": str(settings.llm.get("model", "unknown")),
            },
            {
                "name": "Embedding",
                "provider": str(settings.embedding.get("provider", "unknown")),
                "model": str(settings.embedding.get("model", "unknown")),
            },
            {
                "name": "Vector Store",
                "provider": str(settings.vector_store.get("provider", "unknown")),
                "model": str(settings.vector_store.get("collection_name", "default")),
            },
            {
                "name": "Rerank",
                "provider": str(settings.rerank.get("provider", "none")),
                "model": str(settings.rerank.get("enabled", False)),
            },
        ]

    @staticmethod
    def _build_stats(settings: Settings) -> dict[str, int]:
        persist_dir = Path(str(settings.vector_store.get("persist_directory", "data/db/chroma")))
        traces_path = Path(str(settings.observability.get("traces_path", "logs/traces.jsonl")))
        image_root = Path(
            str(
                settings.ingestion.get("image_storage", {}).get(
                    "image_root",
                    "data/images",
                )
            )
        )

        collection_count = 0
        chunk_count = 0
        if persist_dir.exists():
            for item in sorted(persist_dir.glob("*.json")):
                collection_count += 1
                try:
                    payload = json.loads(item.read_text(encoding="utf-8"))
                except Exception:
                    continue
                records = payload.get("records")
                if isinstance(records, dict):
                    chunk_count += len(records)

        trace_count = 0
        if traces_path.exists():
            try:
                with traces_path.open("r", encoding="utf-8") as handle:
                    trace_count = sum(1 for line in handle if line.strip())
            except Exception:
                trace_count = 0

        image_count = 0
        if image_root.exists():
            image_count = sum(1 for path in image_root.rglob("*") if path.is_file())

        return {
            "collections": collection_count,
            "chunks": chunk_count,
            "traces": trace_count,
            "images": image_count,
        }


__all__ = ["ConfigService", "OverviewSnapshot", "SettingsError"]
