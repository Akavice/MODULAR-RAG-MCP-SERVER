"""Trace context model for ingestion/query instrumentation."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import UTC, datetime
from time import perf_counter
from typing import Any
from uuid import uuid4

_ALLOWED_TRACE_TYPES = frozenset({"query", "ingestion"})


@dataclass(slots=True)
class TraceContext:
    """Lightweight mutable trace context for stage-level records."""

    trace_type: str = "query"
    trace_id: str = field(default_factory=lambda: str(uuid4()))
    stages: list[dict[str, Any]] = field(default_factory=list)
    started_at: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat(timespec="milliseconds")
    )
    finished_at: str | None = None
    total_elapsed_ms: float | None = None
    _started_monotonic: float = field(default_factory=perf_counter, repr=False)
    _last_stage_monotonic: float = field(default_factory=perf_counter, repr=False)

    def __post_init__(self) -> None:
        if self.trace_type not in _ALLOWED_TRACE_TYPES:
            allowed = ", ".join(sorted(_ALLOWED_TRACE_TYPES))
            raise ValueError(f"trace_type must be one of: {allowed}")
        if not isinstance(self.trace_id, str) or not self.trace_id.strip():
            raise ValueError("trace_id must be a non-empty string")

    def record_stage(self, stage: str, **payload: Any) -> None:
        """Append a stage event payload into this trace."""
        if not isinstance(stage, str) or not stage.strip():
            raise ValueError("stage must be a non-empty string")

        now_monotonic = perf_counter()
        stage_elapsed_ms = (now_monotonic - self._last_stage_monotonic) * 1000
        self._last_stage_monotonic = now_monotonic

        stage_payload = dict(payload)
        stage_payload.setdefault("elapsed_ms", round(stage_elapsed_ms, 3))
        self.stages.append(
            {
                "stage": stage.strip(),
                "timestamp": datetime.now(UTC).isoformat(timespec="milliseconds"),
                **stage_payload,
            }
        )

    def finish(self) -> None:
        """Mark this trace as complete and freeze total elapsed time."""
        if self.finished_at is not None:
            return
        now_monotonic = perf_counter()
        self.finished_at = datetime.now(UTC).isoformat(timespec="milliseconds")
        self.total_elapsed_ms = round((now_monotonic - self._started_monotonic) * 1000, 3)

    def elapsed_ms(self, stage_name: str | None = None) -> float:
        """Return total elapsed time or a recorded stage elapsed time."""
        if stage_name is None:
            if self.total_elapsed_ms is not None:
                return self.total_elapsed_ms
            return round((perf_counter() - self._started_monotonic) * 1000, 3)

        if not isinstance(stage_name, str) or not stage_name.strip():
            raise ValueError("stage_name must be a non-empty string")
        target = stage_name.strip()
        for stage in reversed(self.stages):
            if stage.get("stage") == target:
                elapsed = stage.get("elapsed_ms")
                if isinstance(elapsed, bool) or not isinstance(elapsed, int | float):
                    raise ValueError(f"stage {target!r} has no numeric elapsed_ms")
                return float(elapsed)
        raise KeyError(f"stage not found: {target}")

    def to_dict(self) -> dict[str, Any]:
        """Serialize this trace into a JSON-compatible dictionary."""
        return {
            "trace_id": self.trace_id,
            "trace_type": self.trace_type,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "total_elapsed_ms": self.elapsed_ms(),
            "stages": deepcopy(self.stages),
        }
