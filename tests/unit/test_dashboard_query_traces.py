"""Unit tests for dashboard query traces page (G6)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from observability.dashboard.pages import query_traces


class _FakeColumn:
    def __init__(self, calls: list[str]) -> None:
        self._calls = calls
        self.metrics: list[tuple[object, object]] = []

    def metric(self, *args: object, **_kwargs: object) -> None:
        self._calls.append("column.metric")
        if len(args) >= 2:
            self.metrics.append((args[0], args[1]))


class _FakeStreamlit:
    def __init__(self) -> None:
        self.calls: list[str] = []
        self.json_payload: object | None = None
        self.title_text: object | None = None
        self.caption_text: object | None = None
        self.text_input_label: object | None = None
        self.selectbox_label: object | None = None
        self.subheaders: list[object] = []
        self.columns_created: list[_FakeColumn] = []

    def title(self, *args: object, **_kwargs: object) -> None:
        self.calls.append("title")
        if args:
            self.title_text = args[0]

    def caption(self, *args: object, **_kwargs: object) -> None:
        self.calls.append("caption")
        if args:
            self.caption_text = args[0]

    def text_input(self, *args: object, **_kwargs: object) -> str:
        self.calls.append("text_input")
        if args:
            self.text_input_label = args[0]
        return "alpha"

    def metric(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("metric")

    def dataframe(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("dataframe")

    def selectbox(self, label: str, options: list[str], index: int = 0) -> str:
        self.calls.append("selectbox")
        self.selectbox_label = label
        return options[index]

    def subheader(self, *args: object, **_kwargs: object) -> None:
        self.calls.append("subheader")
        if args:
            self.subheaders.append(args[0])

    def bar_chart(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("bar_chart")

    def columns(self, n: int) -> list[_FakeColumn]:
        self.calls.append("columns")
        columns = [_FakeColumn(self.calls) for _ in range(n)]
        self.columns_created.extend(columns)
        return columns

    def json(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("json")
        if _args:
            self.json_payload = _args[0]

    def info(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("info")

    def error(self, *_args: object, **_kwargs: object) -> None:
        self.calls.append("error")


def _write_settings(tmp_path: Path, traces_path: Path) -> Path:
    settings_file = tmp_path / "settings.yaml"
    settings_file.write_text(
        f"""\
project:
  name: test
llm:
  provider: openai
  model: gpt-4o-mini
embedding:
  provider: openai
  model: text-embedding-3-small
vector_store:
  provider: chroma
  persist_directory: {tmp_path.as_posix()}/chroma
retrieval:
  top_k: 5
rerank:
  enabled: false
  provider: none
evaluation:
  provider: custom
observability:
  traces_path: {traces_path.as_posix()}
  app_log_path: {tmp_path.as_posix()}/logs/app.log
ingestion:
  image_storage:
    image_root: {tmp_path.as_posix()}/images
""",
        encoding="utf-8",
    )
    return settings_file


@pytest.mark.unit
def test_query_traces_page_renders_history_timeline_and_comparison(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    traces_path = tmp_path / "logs" / "traces.jsonl"
    traces_path.parent.mkdir(parents=True, exist_ok=True)
    traces_path.write_text(
        json.dumps(
            {
                "trace_id": "q-1",
                "trace_type": "query",
                "started_at": "2026-06-01T10:00:00Z",
                "stages": [
                    {"stage": "query_processing", "query": "alpha test", "elapsed_ms": 1.0},
                    {"stage": "dense_retrieval", "hit_count": 2, "elapsed_ms": 5.0},
                    {"stage": "sparse_retrieval", "hit_count": 3, "elapsed_ms": 6.0},
                    {"stage": "fusion", "fused_count": 2, "elapsed_ms": 2.0},
                    {"stage": "rerank", "input_count": 2, "output_count": 2, "fallback": False, "elapsed_ms": 3.0},
                ],
            }
        ),
        encoding="utf-8",
    )
    settings_file = _write_settings(tmp_path, traces_path)

    fake_st = _FakeStreamlit()
    monkeypatch.setitem(sys.modules, "streamlit", fake_st)

    query_traces.render({"settings_path": str(settings_file)})

    assert "text_input" in fake_st.calls
    assert "metric" in fake_st.calls
    assert "dataframe" in fake_st.calls
    assert "selectbox" in fake_st.calls
    assert "bar_chart" in fake_st.calls
    assert "columns" in fake_st.calls
    assert "json" in fake_st.calls


@pytest.mark.unit
def test_query_traces_page_shows_info_when_no_query_trace(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    traces_path = tmp_path / "logs" / "traces.jsonl"
    traces_path.parent.mkdir(parents=True, exist_ok=True)
    traces_path.write_text("", encoding="utf-8")
    settings_file = _write_settings(tmp_path, traces_path)

    fake_st = _FakeStreamlit()
    monkeypatch.setitem(sys.modules, "streamlit", fake_st)

    query_traces.render({"settings_path": str(settings_file)})

    assert "metric" in fake_st.calls
    assert "info" in fake_st.calls


@pytest.mark.unit
def test_query_traces_page_selectbox_duplicate_labels_should_map_correct_trace(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    traces_path = tmp_path / "logs" / "traces.jsonl"
    traces_path.parent.mkdir(parents=True, exist_ok=True)
    traces_path.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "trace_id": "abcdefgh-1",
                        "trace_type": "query",
                        "started_at": "2026-06-01T10:00:00Z",
                        "stages": [{"stage": "query_processing", "query": "same"}],
                    }
                ),
                json.dumps(
                    {
                        "trace_id": "abcdefgh-2",
                        "trace_type": "query",
                        "started_at": "2026-06-01T10:00:00Z",
                        "stages": [{"stage": "query_processing", "query": "same"}],
                    }
                ),
            ]
        ),
        encoding="utf-8",
    )
    settings_file = _write_settings(tmp_path, traces_path)

    class _SelectSecondFakeStreamlit(_FakeStreamlit):
        def text_input(self, *_args: object, **_kwargs: object) -> str:
            self.calls.append("text_input")
            return ""

        def selectbox(self, _label: str, options: list[str], index: int = 0) -> str:
            self.calls.append("selectbox")
            return options[1]

    fake_st = _SelectSecondFakeStreamlit()
    monkeypatch.setitem(sys.modules, "streamlit", fake_st)

    query_traces.render({"settings_path": str(settings_file)})

    assert isinstance(fake_st.json_payload, dict)
    assert fake_st.json_payload.get("trace_id") == "abcdefgh-2"


@pytest.mark.unit
def test_query_traces_page_renders_zh_cn_labels_and_boolean_text(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    traces_path = tmp_path / "logs" / "traces.jsonl"
    traces_path.parent.mkdir(parents=True, exist_ok=True)
    traces_path.write_text(
        json.dumps(
            {
                "trace_id": "q-zh",
                "trace_type": "query",
                "started_at": "2026-06-02T10:00:00Z",
                "stages": [
                    {"stage": "query_processing", "query": "alpha test", "elapsed_ms": 1.0},
                    {"stage": "dense_retrieval", "hit_count": 2, "elapsed_ms": 5.0},
                    {"stage": "sparse_retrieval", "hit_count": 3, "elapsed_ms": 6.0},
                    {"stage": "fusion", "fused_count": 2, "elapsed_ms": 2.0},
                    {"stage": "rerank", "input_count": 2, "output_count": 1, "fallback": True, "elapsed_ms": 3.0},
                ],
            }
        ),
        encoding="utf-8",
    )
    settings_file = _write_settings(tmp_path, traces_path)

    fake_st = _FakeStreamlit()
    monkeypatch.setitem(sys.modules, "streamlit", fake_st)

    query_traces.render({"settings_path": str(settings_file), "locale": "zh-CN"})

    assert fake_st.title_text == "查询追踪"
    assert fake_st.caption_text == "查看查询历史、阶段耗时和重排效果。"
    assert fake_st.text_input_label == "关键词搜索"
    assert fake_st.selectbox_label == "选择追踪"
    assert "Dense / Sparse 对比" in fake_st.subheaders
    assert "重排前后对比" in fake_st.subheaders
    assert len(fake_st.columns_created) >= 2
    rerank_metrics = [
        metric
        for column in fake_st.columns_created
        for metric in column.metrics
    ]
    assert ("是否降级", "是") in rerank_metrics
