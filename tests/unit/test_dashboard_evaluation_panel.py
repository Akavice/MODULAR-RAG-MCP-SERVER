"""Unit tests for dashboard evaluation panel (H4)."""

from __future__ import annotations

import sys
from types import SimpleNamespace
from typing import Any

import pytest

from observability.dashboard.pages import evaluation_panel
from observability.evaluation.eval_runner import EvalCaseResult, EvalReport


class _FakeColumn:
    def __init__(self, calls: list[str]) -> None:
        self.calls = calls
        self.metrics: list[tuple[str, str]] = []

    def metric(self, label: str, value: str) -> None:
        self.calls.append("column.metric")
        self.metrics.append((label, value))


class _FakeStreamlit:
    def __init__(self, *, run_button: bool) -> None:
        self.calls: list[str] = []
        self.messages: list[tuple[str, str]] = []
        self.json_payload: object | None = None
        self.dataframe_payload: object | None = None
        self.columns_payload: list[_FakeColumn] = []
        self.run_button = run_button
        self.selectbox_label: str | None = None
        self.text_input_label: str | None = None
        self.number_input_label: str | None = None
        self.checkbox_label: str | None = None

    def title(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("title")

    def caption(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("caption")

    def selectbox(self, *args: object, **_kwargs: object) -> str:
        self.calls.append("selectbox")
        if args:
            self.selectbox_label = str(args[0])
        return "custom"

    def text_input(self, *args: object, **_kwargs: object) -> str:
        self.calls.append("text_input")
        if args:
            self.text_input_label = str(args[0])
        return "tests/fixtures/golden_test_set.json"

    def number_input(self, *args: object, **_kwargs: object) -> int:
        self.calls.append("number_input")
        if args:
            self.number_input_label = str(args[0])
        return 3

    def checkbox(self, *args: object, **_kwargs: object) -> bool:
        self.calls.append("checkbox")
        if args:
            self.checkbox_label = str(args[0])
        return True

    def button(self, *_args: object, **_kwargs: object) -> bool:
        self.calls.append("button")
        return self.run_button

    def success(self, message: str) -> None:
        self.calls.append("success")
        self.messages.append(("success", message))

    def error(self, message: str) -> None:
        self.calls.append("error")
        self.messages.append(("error", message))

    def subheader(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("subheader")

    def columns(self, count: int) -> list[_FakeColumn]:
        self.calls.append("columns")
        self.columns_payload = [_FakeColumn(self.calls) for _ in range(count)]
        return self.columns_payload

    def dataframe(self, payload: object, *_args: object, **_kwargs: object) -> None:
        self.calls.append("dataframe")
        self.dataframe_payload = payload

    def json(self, payload: object) -> None:
        self.calls.append("json")
        self.json_payload = payload


@pytest.mark.unit
def test_evaluation_panel_exposes_controls_without_running(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_st = _FakeStreamlit(run_button=False)
    monkeypatch.setitem(sys.modules, "streamlit", fake_st)

    evaluation_panel.render({"settings_path": "config/settings.yaml"})

    assert "selectbox" in fake_st.calls
    assert "text_input" in fake_st.calls
    assert "number_input" in fake_st.calls
    assert "checkbox" in fake_st.calls
    assert "button" in fake_st.calls
    assert "json" not in fake_st.calls


@pytest.mark.unit
def test_evaluation_panel_runs_eval_and_renders_metrics(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_st = _FakeStreamlit(run_button=True)
    monkeypatch.setitem(sys.modules, "streamlit", fake_st)

    captured: dict[str, object] = {}
    report = EvalReport(
        metrics={"hit_rate": 1.0, "mrr": 0.5},
        cases=[
            EvalCaseResult(
                query="q",
                expected_chunk_ids=["a"],
                expected_sources=[],
                retrieved_ids=["a"],
                retrieved_sources=["docs/a.pdf"],
                metrics={"hit_rate": 1.0, "mrr": 0.5},
            )
        ],
    )

    def fake_run_evaluation(**kwargs: object) -> EvalReport:
        captured.update(kwargs)
        return report

    monkeypatch.setattr(evaluation_panel, "_run_evaluation", fake_run_evaluation)

    evaluation_panel.render({"settings_path": "cfg.yaml", "locale": "en-US"})

    assert captured == {
        "settings_path": "cfg.yaml",
        "backend": "custom",
        "test_set_path": "tests/fixtures/golden_test_set.json",
        "top_k": 3,
        "dry_run": True,
    }
    assert "success" in fake_st.calls
    assert "dataframe" in fake_st.calls
    assert "json" in fake_st.calls
    assert isinstance(fake_st.json_payload, dict)
    assert fake_st.json_payload["metrics"]["hit_rate"] == 1.0  # type: ignore[index]


@pytest.mark.unit
def test_evaluation_panel_shows_error_on_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_st = _FakeStreamlit(run_button=True)
    monkeypatch.setitem(sys.modules, "streamlit", fake_st)

    def fail_run(**_kwargs: object) -> EvalReport:
        raise RuntimeError("boom")

    monkeypatch.setattr(evaluation_panel, "_run_evaluation", fail_run)

    evaluation_panel.render({"settings_path": "cfg.yaml", "locale": "en-US"})

    assert "error" in fake_st.calls
    assert fake_st.messages[-1] == ("error", "Evaluation failed: boom")


@pytest.mark.unit
def test_evaluation_panel_renders_zh_cn_labels_for_case_table(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_st = _FakeStreamlit(run_button=True)
    monkeypatch.setitem(sys.modules, "streamlit", fake_st)

    report = EvalReport(
        metrics={"hit_rate": 1.0, "mrr": 0.5},
        cases=[
            EvalCaseResult(
                query="q",
                expected_chunk_ids=[],
                expected_sources=["docs/a.pdf"],
                retrieved_ids=["a"],
                retrieved_sources=["docs/a.pdf"],
                metrics={"hit_rate": 1.0, "mrr": 0.5},
            )
        ],
    )

    monkeypatch.setattr(evaluation_panel, "_run_evaluation", lambda **_kwargs: report)

    evaluation_panel.render({"settings_path": "cfg.yaml", "locale": "zh-CN"})

    assert fake_st.selectbox_label == "评估后端"
    assert fake_st.text_input_label == "Golden Test Set"
    assert fake_st.number_input_label == "Top K"
    assert fake_st.checkbox_label == "空跑模式"
    assert isinstance(fake_st.dataframe_payload, list)
    assert fake_st.dataframe_payload
    row = fake_st.dataframe_payload[0]
    assert "查询" in row
    assert "期望命中" in row
    assert "实际命中" in row
    assert "命中率" in row
    assert "倒数排名均值" in row
