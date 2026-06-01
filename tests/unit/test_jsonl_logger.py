from __future__ import annotations

import json
from pathlib import Path

import pytest

from observability.logger import get_trace_logger, write_trace


@pytest.mark.unit
def test_write_trace_appends_single_json_line(tmp_path: Path) -> None:
    trace_path = tmp_path / "logs" / "traces.jsonl"

    write_trace({"trace_id": "t1", "trace_type": "query"}, traces_path=trace_path)

    raw = trace_path.read_text(encoding="utf-8").strip()
    payload = json.loads(raw)
    assert payload["trace_id"] == "t1"
    assert payload["trace_type"] == "query"
    assert payload["level"] == "INFO"
    assert "timestamp" in payload


@pytest.mark.unit
def test_get_trace_logger_reuses_same_instance_for_same_path(tmp_path: Path) -> None:
    trace_path = tmp_path / "trace.jsonl"

    first = get_trace_logger(trace_path)
    second = get_trace_logger(str(trace_path))

    assert first is second


@pytest.mark.unit
def test_write_trace_rejects_non_mapping(tmp_path: Path) -> None:
    trace_path = tmp_path / "trace.jsonl"

    with pytest.raises(TypeError, match="trace_dict"):
        write_trace("bad", traces_path=trace_path)  # type: ignore[arg-type]


@pytest.mark.unit
def test_get_trace_logger_rejects_blank_path() -> None:
    with pytest.raises(ValueError, match="log path"):
        get_trace_logger("   ")


@pytest.mark.unit
def test_write_trace_appends_multiple_lines(tmp_path: Path) -> None:
    trace_path = tmp_path / "logs" / "traces.jsonl"

    write_trace({"trace_id": "t1"}, traces_path=trace_path)
    write_trace({"trace_id": "t2"}, traces_path=trace_path)

    lines = [line for line in trace_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(lines) == 2
    assert json.loads(lines[0])["trace_id"] == "t1"
    assert json.loads(lines[1])["trace_id"] == "t2"


@pytest.mark.unit
def test_get_trace_logger_rejects_invalid_path_type() -> None:
    with pytest.raises(TypeError, match="log path"):
        get_trace_logger(123)  # type: ignore[arg-type]
