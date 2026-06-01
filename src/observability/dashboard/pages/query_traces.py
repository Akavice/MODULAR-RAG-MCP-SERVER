"""Dashboard query traces page."""

from __future__ import annotations

from typing import Any

from observability.dashboard.services.trace_service import SettingsError, TraceService


def render(context: dict[str, Any] | None = None) -> None:
    import streamlit as st

    st.title("Query Traces")
    st.caption("Browse query history with stage timing and rerank effects.")

    settings_path = "config/settings.yaml"
    if isinstance(context, dict):
        value = context.get("settings_path")
        if isinstance(value, str) and value.strip():
            settings_path = value.strip()

    service = TraceService(settings_path=settings_path)
    keyword = st.text_input("Search keyword", value="")

    try:
        traces = service.list_query_traces(keyword=keyword, limit=500)
    except SettingsError as exc:
        st.error(f"Failed to load settings: {exc}")
        st.info(f"Current settings path: `{settings_path}`")
        return

    st.metric("Query Traces", len(traces))
    if not traces:
        st.info("No query traces found. Run query first.")
        return

    table_rows = [
        {
            "Trace ID": item.trace_id,
            "Started At": item.started_at,
            "Elapsed (ms)": item.total_elapsed_ms if item.total_elapsed_ms is not None else "-",
            "Query": item.query_text or "-",
            "Stages": item.stage_count,
            "Collection": item.collection or "-",
        }
        for item in traces
    ]
    st.dataframe(table_rows, use_container_width=True, hide_index=True)

    # Use stable unique option keys to avoid wrong mapping when display text duplicates.
    options_by_label = {
        f"{index:04d} | {item.started_at} | {item.trace_id} | {item.query_text or 'no-query'}": item
        for index, item in enumerate(traces)
    }
    selected_label = st.selectbox("Select Trace", list(options_by_label), index=0)
    selected_trace = options_by_label[selected_label]

    st.subheader("Stage Timing Waterfall")
    timeline = TraceService.build_stage_timeline(selected_trace)
    if timeline:
        st.bar_chart(
            [{"stage": row["stage"], "elapsed_ms": row["elapsed_ms"]} for row in timeline],
            x="stage",
            y="elapsed_ms",
        )
    else:
        st.info("No stage timing data found for this trace.")

    st.subheader("Dense vs Sparse")
    summary = TraceService.summarize_query_channels(selected_trace)
    cols = st.columns(3)
    cols[0].metric("Dense Hits", _display_int(summary["dense_hit_count"]))
    cols[1].metric("Sparse Hits", _display_int(summary["sparse_hit_count"]))
    cols[2].metric("Fused Count", _display_int(summary["fused_count"]))

    st.subheader("Rerank Delta")
    rerank_cols = st.columns(3)
    rerank_cols[0].metric("Before Rerank", _display_int(summary["rerank_input"]))
    rerank_cols[1].metric("After Rerank", _display_int(summary["rerank_output"]))
    rerank_cols[2].metric("Fallback", _display_bool(summary["rerank_fallback"]))

    st.subheader("Trace Payload")
    st.json(selected_trace.to_dict())


def _display_int(value: int | None) -> str:
    if value is None:
        return "-"
    return str(value)


def _display_bool(value: bool | None) -> str:
    if value is None:
        return "-"
    return "yes" if value else "no"
