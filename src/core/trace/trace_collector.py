"""In-memory trace collector.

JSON Lines persistence is implemented in the next observability phase; this
collector owns the small F1 contract of accepting finished/unfinished traces and
keeping their serializable snapshots.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from core.trace.trace_context import TraceContext


class TraceCollector:
    """Collect serializable trace snapshots for later persistence."""

    def __init__(self) -> None:
        self._records: list[dict[str, Any]] = []

    def collect(self, trace: TraceContext) -> None:
        if not isinstance(trace, TraceContext):
            raise TypeError("trace must be a TraceContext")
        if trace.finished_at is None:
            trace.finish()
        self._records.append(trace.to_dict())

    def records(self) -> list[dict[str, Any]]:
        return deepcopy(self._records)

    def clear(self) -> None:
        self._records.clear()
