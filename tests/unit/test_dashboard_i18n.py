"""Unit tests for dashboard i18n wiring (G7)."""

from __future__ import annotations

import sys
from typing import Any

import pytest

from observability.dashboard import app as dashboard_app
from observability.dashboard.services import i18n


class _FakeColumn:
    def __enter__(self) -> "_FakeColumn":
        return self

    def __exit__(self, *_args: object) -> None:
        return None


class _FakeSidebar:
    def __init__(self, owner: "_FakeStreamlit") -> None:
        self.owner = owner

    def radio(self, label: str, options: list[str], index: int = 0) -> str:
        self.owner.sidebar_label = label
        self.owner.sidebar_options = list(options)
        return options[index]


class _FakeStreamlit:
    def __init__(self) -> None:
        self.session_state: dict[str, Any] = {}
        self.sidebar = _FakeSidebar(self)
        self.sidebar_label = ""
        self.sidebar_options: list[str] = []
        self.selectbox_calls: list[dict[str, Any]] = []

    def set_page_config(self, **_kwargs: Any) -> None:
        return None

    def columns(self, _spec: list[int]) -> list[_FakeColumn]:
        return [_FakeColumn(), _FakeColumn()]

    def selectbox(self, label: str, options: list[str], index: int = 0, **_kwargs: Any) -> str:
        self.selectbox_calls.append({"label": label, "options": list(options), "index": index})
        if len(options) > 1:
            return options[1]
        return options[index]

    def empty(self) -> None:
        return None


@pytest.mark.unit
def test_dashboard_app_switches_locale_and_passes_context(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_st = _FakeStreamlit()
    monkeypatch.setitem(sys.modules, "streamlit", fake_st)

    captured: dict[str, Any] = {}

    def _capture(context: dict[str, Any]) -> None:
        captured.update(context)

    monkeypatch.setattr(dashboard_app.overview, "render", _capture)

    dashboard_app.main("config/settings.yaml")

    assert captured["locale"] == "zh-CN"
    assert captured["settings_path"] == "config/settings.yaml"
    assert fake_st.sidebar_label == i18n.t("app.sidebar.pages", locale="zh-CN")
    assert fake_st.session_state[i18n.LOCALE_STATE_KEY] == "zh-CN"


@pytest.mark.unit
def test_i18n_translate_fallback_and_formatting() -> None:
    assert i18n.normalize_locale("xx") == i18n.DEFAULT_LOCALE
    assert i18n.t("query_traces.metric.count", locale="zh-CN") == "\u67e5\u8be2\u8ffd\u8e2a\u6570"
    assert i18n.t("missing.key", locale="zh-CN") == "missing.key"
    message = i18n.t("common.current_settings_path", locale="en-US", path="cfg.yaml")
    assert "cfg.yaml" in message


@pytest.mark.unit
def test_i18n_falls_back_to_en_us_when_locale_entry_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    patched = {
        locale: dict(messages)
        for locale, messages in i18n._MESSAGES.items()
    }
    patched["zh-CN"].pop("query_traces.metric.count", None)
    monkeypatch.setattr(i18n, "_MESSAGES", patched)

    assert i18n.t("query_traces.metric.count", locale="zh-CN") == "Query Traces"
