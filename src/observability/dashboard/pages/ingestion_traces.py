"""Dashboard ingestion traces page."""

from __future__ import annotations

from typing import Any

from observability.dashboard.services.trace_service import SettingsError, TraceService


def render(context: dict[str, Any] | None = None) -> None:
    import streamlit as st

    st.title("Ingestion Traces")
    st.caption("Browse ingestion history and stage elapsed-time waterfall.")

    settings_path = "config/settings.yaml"
    if isinstance(context, dict):
        value = context.get("settings_path")
        if isinstance(value, str) and value.strip():
            settings_path = value.strip()

    service = TraceService(settings_path=settings_path)
    try:
        traces = service.list_ingestion_traces(limit=500)
    except SettingsError as exc:
        st.error(f"Failed to load settings: {exc}")
        st.info(f"Current settings path: `{settings_path}`")
        return

    st.metric("Ingestion Traces", len(traces))
    if not traces:
        st.info("No ingestion traces found. Run ingestion first.")
        return

    list_rows = [
        {
            "Trace ID": item.trace_id,
            "Started At": item.started_at,
            "Finished At": item.finished_at or "-",
            "Elapsed (ms)": item.total_elapsed_ms if item.total_elapsed_ms is not None else "-",
            "Stages": item.stage_count,
            "Collection": item.collection or "-",
            "Source Path": item.source_path or "-",
        }
        for item in traces
    ]
    st.dataframe(list_rows, use_container_width=True, hide_index=True)

    labels = [
        f"{item.started_at} | {item.trace_id[:8]} | {item.collection or 'unknown'}"
        for item in traces
    ]
    selected_label = st.selectbox("Select Trace", labels, index=0)
    selected_index = labels.index(selected_label)
    selected_trace = traces[selected_index]

    st.subheader("Stage Timing Waterfall")
    timeline = TraceService.build_stage_timeline(selected_trace)
    if not timeline:
        st.info("No stage timing data found for this trace.")
    else:
        chart_rows = [
            {"stage": row["stage"], "elapsed_ms": row["elapsed_ms"]}
            for row in timeline
        ]
        st.bar_chart(chart_rows, x="stage", y="elapsed_ms")
        st.dataframe(chart_rows, use_container_width=True, hide_index=True)

    st.subheader("Trace Payload")
    st.json(selected_trace.to_dict())
