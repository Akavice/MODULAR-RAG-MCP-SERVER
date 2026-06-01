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
    query_text: str | None
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
            "query_text": self.query_text,
            "stages": [dict(item) for item in self.stages],
        }


class TraceService:
    """Read and normalize JSONL traces produced by observability logger."""

    def __init__(self, settings_path: str = "config/settings.yaml") -> None:
        self.settings_path = settings_path

    def list_ingestion_traces(self, limit: int = 200) -> list[TraceSummary]:
        return self.list_traces(trace_type="ingestion", limit=limit)

    def list_query_traces(
        self,
        *,
        keyword: str | None = None,
        limit: int = 200,
    ) -> list[TraceSummary]:
        traces = self.list_traces(trace_type="query", limit=limit)
        normalized = self._normalize_keyword(keyword)
        if normalized is None:
            return traces
        return [
            item
            for item in traces
            if self._trace_matches_keyword(item, normalized)
        ]

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

    @staticmethod
    def summarize_query_channels(trace: TraceSummary) -> dict[str, Any]:
        dense_hit_count = None
        sparse_hit_count = None
        fused_count = None
        rerank_input = None
        rerank_output = None
        rerank_fallback = None

        for stage in trace.stages:
            if not isinstance(stage, dict):
                continue
            stage_name = stage.get("stage")
            if stage_name == "dense_retrieval":
                value = stage.get("hit_count")
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    dense_hit_count = int(value)
            elif stage_name == "sparse_retrieval":
                value = stage.get("hit_count")
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    sparse_hit_count = int(value)
            elif stage_name == "fusion":
                value = stage.get("fused_count")
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    fused_count = int(value)
            elif stage_name == "rerank":
                input_value = stage.get("input_count")
                output_value = stage.get("output_count")
                fallback_value = stage.get("fallback")
                if isinstance(input_value, (int, float)) and not isinstance(input_value, bool):
                    rerank_input = int(input_value)
                if isinstance(output_value, (int, float)) and not isinstance(output_value, bool):
                    rerank_output = int(output_value)
                if isinstance(fallback_value, bool):
                    rerank_fallback = fallback_value

        return {
            "dense_hit_count": dense_hit_count,
            "sparse_hit_count": sparse_hit_count,
            "fused_count": fused_count,
            "rerank_input": rerank_input,
            "rerank_output": rerank_output,
            "rerank_fallback": rerank_fallback,
        }

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
        query_text: str | None = None
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
            if query_text is None:
                value = stage.get("query")
                if isinstance(value, str) and value.strip():
                    query_text = value.strip()

        return TraceSummary(
            trace_id=trace_id.strip(),
            trace_type=trace_type.strip(),
            started_at=started_at,
            finished_at=finished_at,
            total_elapsed_ms=total_elapsed_ms,
            stage_count=len(stages),
            source_path=source_path,
            collection=collection,
            query_text=query_text,
            stages=[dict(item) for item in stages if isinstance(item, dict)],
        )

    @staticmethod
    def _normalize_keyword(keyword: str | None) -> str | None:
        if keyword is None:
            return None
        if not isinstance(keyword, str):
            raise TypeError("keyword must be a string when provided")
        normalized = keyword.strip().lower()
        if not normalized:
            return None
        return normalized

    @staticmethod
    def _trace_matches_keyword(trace: TraceSummary, keyword: str) -> bool:
        if keyword in trace.trace_id.lower():
            return True
        if trace.query_text and keyword in trace.query_text.lower():
            return True
        if trace.source_path and keyword in trace.source_path.lower():
            return True
        return False


__all__ = ["TraceService", "TraceSummary", "SettingsError"]
