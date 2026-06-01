"""Trace parsing service for dashboard pages."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from core.settings import SettingsError, load_settings


@dataclass(slots=True)
class TraceSummary:
    """Normalized trace summary for dashboard list view."""

    trace_id: str
    trace_type: str
    started_at: str
    finished_at: str | None
    total_elapsed_ms: float | None
    stage_count: int
    source_path: str | None
    collection: str | None
    stages: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "trace_type": self.trace_type,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "total_elapsed_ms": self.total_elapsed_ms,
            "stage_count": self.stage_count,
            "source_path": self.source_path,
            "collection": self.collection,
            "stages": [dict(item) for item in self.stages],
        }


class TraceService:
    """Read and normalize JSONL traces produced by observability logger."""

    def __init__(self, settings_path: str = "config/settings.yaml") -> None:
        self.settings_path = settings_path

    def list_ingestion_traces(self, limit: int = 200) -> list[TraceSummary]:
        return self.list_traces(trace_type="ingestion", limit=limit)

    def list_traces(
        self,
        *,
        trace_type: str | None = None,
        limit: int = 200,
    ) -> list[TraceSummary]:
        if isinstance(limit, bool) or not isinstance(limit, int):
            raise TypeError("limit must be an integer")
        if limit <= 0:
            raise ValueError("limit must be greater than 0")

        traces_path = self._resolve_traces_path()
        if not traces_path.exists():
            return []

        summaries: list[TraceSummary] = []
        with traces_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                raw = line.strip()
                if not raw:
                    continue
                try:
                    item = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                if not isinstance(item, dict):
                    continue
                summary = self._to_summary(item)
                if summary is None:
                    continue
                if trace_type is not None and summary.trace_type != trace_type:
                    continue
                summaries.append(summary)

        summaries.sort(key=lambda item: item.started_at, reverse=True)
        return summaries[:limit]

    @staticmethod
    def build_stage_timeline(trace: TraceSummary) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for stage in trace.stages:
            if not isinstance(stage, dict):
                continue
            stage_name = stage.get("stage")
            elapsed = stage.get("elapsed_ms")
            if not isinstance(stage_name, str) or not stage_name.strip():
                continue
            if isinstance(elapsed, bool) or not isinstance(elapsed, (int, float)):
                continue
            rows.append({"stage": stage_name.strip(), "elapsed_ms": float(elapsed)})
        return rows

    def _resolve_traces_path(self) -> Path:
        settings = load_settings(self.settings_path)
        value = settings.observability.get("traces_path", "logs/traces.jsonl")
        if not isinstance(value, str) or not value.strip():
            raise SettingsError("observability.traces_path must be a non-empty string")
        return Path(value.strip())

    def _to_summary(self, payload: dict[str, Any]) -> TraceSummary | None:
        trace_id = payload.get("trace_id")
        trace_type = payload.get("trace_type")
        if not isinstance(trace_id, str) or not trace_id.strip():
            return None
        if not isinstance(trace_type, str) or not trace_type.strip():
            return None

        started_at = payload.get("started_at")
        if not isinstance(started_at, str) or not started_at.strip():
            timestamp = payload.get("timestamp")
            if isinstance(timestamp, str) and timestamp.strip():
                started_at = timestamp.strip()
            else:
                started_at = ""
        if not started_at:
            return None

        finished_at = payload.get("finished_at")
        if not isinstance(finished_at, str) or not finished_at.strip():
            finished_at = None

        total_elapsed_ms = payload.get("total_elapsed_ms")
        if isinstance(total_elapsed_ms, bool) or not isinstance(total_elapsed_ms, (int, float)):
            total_elapsed_ms = None
        else:
            total_elapsed_ms = float(total_elapsed_ms)

        stages = payload.get("stages")
        if not isinstance(stages, list):
            stages = []

        source_path: str | None = None
        collection: str | None = None
        for stage in stages:
            if not isinstance(stage, dict):
                continue
            if source_path is None:
                value = stage.get("source_path")
                if isinstance(value, str) and value.strip():
                    source_path = value.strip()
            if collection is None:
                value = stage.get("collection")
                if isinstance(value, str) and value.strip():
                    collection = value.strip()
            if source_path and collection:
                break

        return TraceSummary(
            trace_id=trace_id.strip(),
            trace_type=trace_type.strip(),
            started_at=started_at,
            finished_at=finished_at,
            total_elapsed_ms=total_elapsed_ms,
            stage_count=len(stages),
            source_path=source_path,
            collection=collection,
            stages=[dict(item) for item in stages if isinstance(item, dict)],
        )


__all__ = ["TraceService", "TraceSummary", "SettingsError"]
