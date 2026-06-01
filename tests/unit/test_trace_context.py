from __future__ import annotations

import json
from time import sleep

import pytest

from core.trace import TraceCollector, TraceContext


def test_trace_context_defaults_to_query_trace_type() -> None:
    trace = TraceContext()

    assert trace.trace_type == "query"
    assert trace.trace_id
    assert trace.finished_at is None
    assert trace.total_elapsed_ms is None


def test_trace_context_rejects_invalid_trace_type() -> None:
    with pytest.raises(ValueError, match="trace_type"):
        TraceContext(trace_type="invalid")


def test_trace_context_rejects_blank_trace_id() -> None:
    with pytest.raises(ValueError, match="trace_id"):
        TraceContext(trace_id="   ")


def test_record_stage_adds_timestamp_and_elapsed_ms() -> None:
    trace = TraceContext(trace_type="ingestion")

    trace.record_stage("load", chunk_count=2)

    assert trace.stages[0]["stage"] == "load"
    assert trace.stages[0]["chunk_count"] == 2
    assert isinstance(trace.stages[0]["timestamp"], str)
    assert trace.stages[0]["elapsed_ms"] >= 0


def test_record_stage_preserves_explicit_elapsed_ms() -> None:
    trace = TraceContext()

    trace.record_stage("dense", elapsed_ms=12.5)

    assert trace.elapsed_ms("dense") == 12.5


def test_record_stage_rejects_blank_stage_name() -> None:
    trace = TraceContext()

    with pytest.raises(ValueError, match="stage"):
        trace.record_stage(" ")


def test_finish_freezes_total_elapsed_and_is_idempotent() -> None:
    trace = TraceContext()
    sleep(0.001)

    trace.finish()
    first_finished_at = trace.finished_at
    first_elapsed = trace.total_elapsed_ms
    sleep(0.001)
    trace.finish()

    assert trace.finished_at == first_finished_at
    assert trace.total_elapsed_ms == first_elapsed
    assert first_elapsed is not None
    assert first_elapsed > 0


def test_to_dict_is_json_serializable_after_finish() -> None:
    trace = TraceContext(trace_type="query", trace_id="trace-1")
    trace.record_stage("query_processing", input_count=1)
    trace.finish()

    payload = trace.to_dict()

    assert payload["trace_id"] == "trace-1"
    assert payload["trace_type"] == "query"
    assert payload["started_at"]
    assert payload["finished_at"]
    assert payload["total_elapsed_ms"] >= 0
    assert payload["stages"][0]["stage"] == "query_processing"
    json.dumps(payload)


def test_to_dict_returns_stage_copy() -> None:
    trace = TraceContext()
    trace.record_stage("rerank", output_count=1)

    payload = trace.to_dict()
    payload["stages"][0]["output_count"] = 99

    assert trace.stages[0]["output_count"] == 1


def test_elapsed_ms_rejects_unknown_stage() -> None:
    trace = TraceContext()

    with pytest.raises(KeyError, match="missing"):
        trace.elapsed_ms("missing")


def test_elapsed_ms_rejects_blank_stage_name() -> None:
    trace = TraceContext()

    with pytest.raises(ValueError, match="stage_name"):
        trace.elapsed_ms(" ")


def test_trace_collector_finishes_and_collects_trace_snapshot() -> None:
    trace = TraceContext(trace_id="trace-collector")
    trace.record_stage("fusion")
    collector = TraceCollector()

    collector.collect(trace)
    records = collector.records()
    records[0]["trace_id"] = "mutated"

    assert trace.finished_at is not None
    assert collector.records()[0]["trace_id"] == "trace-collector"


def test_trace_collector_rejects_non_trace_context() -> None:
    collector = TraceCollector()

    with pytest.raises(TypeError, match="TraceContext"):
        collector.collect(object())  # type: ignore[arg-type]


def test_trace_collector_clear_empties_records_snapshot() -> None:
    trace = TraceContext(trace_id="trace-clear")
    collector = TraceCollector()

    collector.collect(trace)
    assert collector.records()
    collector.clear()
    assert collector.records() == []
