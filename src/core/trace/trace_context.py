"""Minimal trace context model for ingestion/query instrumentation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


@dataclass(slots=True)
class TraceContext:
    """Lightweight mutable trace context for stage-level records."""

    trace_type: str = "ingestion"
    trace_id: str = field(default_factory=lambda: str(uuid4()))
    stages: list[dict[str, Any]] = field(default_factory=list)
    started_at: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat(timespec="seconds")
    )

    def record_stage(self, stage: str, **payload: Any) -> None:
        """Append a stage event payload into this trace."""
        if not isinstance(stage, str) or not stage.strip():
            raise ValueError("stage must be a non-empty string")
        self.stages.append(
            {
                "stage": stage.strip(),
                "timestamp": datetime.now(UTC).isoformat(timespec="seconds"),
                **payload,
            }
        )
