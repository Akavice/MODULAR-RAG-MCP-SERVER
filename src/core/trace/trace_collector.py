"""Trace collector with optional persistence writer."""

from __future__ import annotations

from collections.abc import Callable
from copy import deepcopy
from typing import Any

from core.trace.trace_context import TraceContext
from observability.logger import write_trace


class TraceCollector:
    """Collect serializable trace snapshots for later persistence."""

    def __init__(self, writer: Callable[[dict[str, Any]], None] | None = None) -> None:
        self._records: list[dict[str, Any]] = []
        self._writer = writer or write_trace

    def collect(self, trace: TraceContext) -> None:
        if not isinstance(trace, TraceContext):
            raise TypeError("trace must be a TraceContext")
        if trace.finished_at is None:
            trace.finish()
        payload = trace.to_dict()
        self._records.append(payload)
        self._writer(payload)

    def records(self) -> list[dict[str, Any]]:
        return deepcopy(self._records)

    def clear(self) -> None:
        self._records.clear()
