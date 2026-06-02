"""Dashboard ingestion traces page."""

from __future__ import annotations

from typing import Any

from observability.dashboard.services.i18n import locale_from_context, t
from observability.dashboard.services.trace_service import SettingsError, TraceService


def render(context: dict[str, Any] | None = None) -> None:
    import streamlit as st

    locale = locale_from_context(context)
    st.title(t("ingestion_traces.title", locale=locale))
    st.caption(t("ingestion_traces.caption", locale=locale))

    settings_path = "config/settings.yaml"
    if isinstance(context, dict):
        value = context.get("settings_path")
        if isinstance(value, str) and value.strip():
            settings_path = value.strip()

    service = TraceService(settings_path=settings_path)
    try:
        traces = service.list_ingestion_traces(limit=500)
    except SettingsError as exc:
        st.error(t("common.failed_load_settings", locale=locale, error=exc))
        st.info(t("common.current_settings_path", locale=locale, path=settings_path))
        return

    st.metric(t("ingestion_traces.metric.count", locale=locale), len(traces))
    if not traces:
        st.info(t("ingestion_traces.info.no_traces", locale=locale))
        return

    placeholder = t("common.placeholder", locale=locale)
    list_rows = [
        {
            t("ingestion_traces.table.trace_id", locale=locale): item.trace_id,
            t("ingestion_traces.table.started_at", locale=locale): item.started_at,
            t("ingestion_traces.table.finished_at", locale=locale): item.finished_at or placeholder,
            t("ingestion_traces.table.elapsed_ms", locale=locale): (
                item.total_elapsed_ms if item.total_elapsed_ms is not None else placeholder
            ),
            t("ingestion_traces.table.stages", locale=locale): item.stage_count,
            t("ingestion_traces.table.collection", locale=locale): item.collection or placeholder,
            t("ingestion_traces.table.source_path", locale=locale): item.source_path or placeholder,
        }
        for item in traces
    ]
    st.dataframe(list_rows, use_container_width=True, hide_index=True)

    options_by_label = {
        f"{index:04d} | {item.started_at} | {item.trace_id} | {item.collection or t('ingestion_traces.unknown_collection', locale=locale)}": item
        for index, item in enumerate(traces)
    }
    selected_label = st.selectbox(
        t("ingestion_traces.select_trace", locale=locale),
        list(options_by_label),
        index=0,
    )
    selected_trace = options_by_label[selected_label]

    st.subheader(t("ingestion_traces.stage_waterfall", locale=locale))
    timeline = TraceService.build_stage_timeline(selected_trace)
    if not timeline:
        st.info(t("ingestion_traces.info.no_timeline", locale=locale))
    else:
        chart_rows = [
            {"stage": row["stage"], "elapsed_ms": row["elapsed_ms"]}
            for row in timeline
        ]
        st.bar_chart(chart_rows, x="stage", y="elapsed_ms")
        st.dataframe(chart_rows, use_container_width=True, hide_index=True)

    st.subheader(t("ingestion_traces.payload", locale=locale))
    st.json(selected_trace.to_dict())
