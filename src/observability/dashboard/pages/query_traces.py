"""Dashboard query traces page."""

from __future__ import annotations

from typing import Any

from observability.dashboard.services.i18n import locale_from_context, t
from observability.dashboard.services.trace_service import SettingsError, TraceService


def render(context: dict[str, Any] | None = None) -> None:
    import streamlit as st

    locale = locale_from_context(context)
    st.title(t("query_traces.title", locale=locale))
    st.caption(t("query_traces.caption", locale=locale))

    settings_path = "config/settings.yaml"
    if isinstance(context, dict):
        value = context.get("settings_path")
        if isinstance(value, str) and value.strip():
            settings_path = value.strip()

    service = TraceService(settings_path=settings_path)
    keyword = st.text_input(t("query_traces.search_keyword", locale=locale), value="")

    try:
        traces = service.list_query_traces(keyword=keyword, limit=500)
    except SettingsError as exc:
        st.error(t("common.failed_load_settings", locale=locale, error=exc))
        st.info(t("common.current_settings_path", locale=locale, path=settings_path))
        return

    st.metric(t("query_traces.metric.count", locale=locale), len(traces))
    if not traces:
        st.info(t("query_traces.info.no_traces", locale=locale))
        return

    placeholder = t("common.placeholder", locale=locale)
    table_rows = [
        {
            t("query_traces.table.trace_id", locale=locale): item.trace_id,
            t("query_traces.table.started_at", locale=locale): item.started_at,
            t("query_traces.table.elapsed_ms", locale=locale): (
                item.total_elapsed_ms if item.total_elapsed_ms is not None else placeholder
            ),
            t("query_traces.table.query", locale=locale): item.query_text or placeholder,
            t("query_traces.table.stages", locale=locale): item.stage_count,
            t("query_traces.table.collection", locale=locale): item.collection or placeholder,
        }
        for item in traces
    ]
    st.dataframe(table_rows, use_container_width=True, hide_index=True)

    # Use stable unique option keys to avoid wrong mapping when display text duplicates.
    options_by_label = {
        f"{index:04d} | {item.started_at} | {item.trace_id} | {item.query_text or t('query_traces.no_query', locale=locale)}": item
        for index, item in enumerate(traces)
    }
    selected_label = st.selectbox(t("query_traces.select_trace", locale=locale), list(options_by_label), index=0)
    selected_trace = options_by_label[selected_label]

    st.subheader(t("query_traces.stage_waterfall", locale=locale))
    timeline = TraceService.build_stage_timeline(selected_trace)
    if timeline:
        st.bar_chart(
            [{"stage": row["stage"], "elapsed_ms": row["elapsed_ms"]} for row in timeline],
            x="stage",
            y="elapsed_ms",
        )
    else:
        st.info(t("query_traces.info.no_timeline", locale=locale))

    st.subheader(t("query_traces.section.dense_sparse", locale=locale))
    summary = TraceService.summarize_query_channels(selected_trace)
    cols = st.columns(3)
    cols[0].metric(t("query_traces.metric.dense_hits", locale=locale), _display_int(summary["dense_hit_count"], locale=locale))
    cols[1].metric(t("query_traces.metric.sparse_hits", locale=locale), _display_int(summary["sparse_hit_count"], locale=locale))
    cols[2].metric(t("query_traces.metric.fused_count", locale=locale), _display_int(summary["fused_count"], locale=locale))

    st.subheader(t("query_traces.section.rerank", locale=locale))
    rerank_cols = st.columns(3)
    rerank_cols[0].metric(t("query_traces.metric.before_rerank", locale=locale), _display_int(summary["rerank_input"], locale=locale))
    rerank_cols[1].metric(t("query_traces.metric.after_rerank", locale=locale), _display_int(summary["rerank_output"], locale=locale))
    rerank_cols[2].metric(t("query_traces.metric.fallback", locale=locale), _display_bool(summary["rerank_fallback"], locale=locale))

    st.subheader(t("query_traces.section.payload", locale=locale))
    st.json(selected_trace.to_dict())


def _display_int(value: int | None, *, locale: str) -> str:
    if value is None:
        return t("common.placeholder", locale=locale)
    return str(value)


def _display_bool(value: bool | None, *, locale: str) -> str:
    if value is None:
        return t("common.placeholder", locale=locale)
    return t("query_traces.bool.yes", locale=locale) if value else t("query_traces.bool.no", locale=locale)
