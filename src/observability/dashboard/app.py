"""Streamlit dashboard entrypoint."""

from __future__ import annotations

import sys
from typing import Any, Callable

from observability.dashboard.pages import (
    data_browser,
    evaluation_panel,
    ingestion_manager,
    ingestion_traces,
    overview,
    query_traces,
)


PageRender = Callable[[dict[str, Any]], None]


def main(settings_path: str = "config/settings.yaml") -> None:
    """Render dashboard with multi-page navigation."""
    import streamlit as st

    st.set_page_config(
        page_title="Modular RAG Dashboard",
        page_icon=":material/analytics:",
        layout="wide",
    )
    context = {"settings_path": settings_path}
    pages: list[tuple[str, str, str, PageRender]] = [
        ("System Overview", "overview", ":material/home:", overview.render),
        ("Data Browser", "data-browser", ":material/folder_open:", data_browser.render),
        ("Ingestion Manager", "ingestion-manager", ":material/upload_file:", ingestion_manager.render),
        ("Ingestion Traces", "ingestion-traces", ":material/monitoring:", ingestion_traces.render),
        ("Query Traces", "query-traces", ":material/search:", query_traces.render),
        ("Evaluation Panel", "evaluation-panel", ":material/insights:", evaluation_panel.render),
    ]

    if hasattr(st, "navigation") and hasattr(st, "Page"):
        st_pages = [
            st.Page(
                lambda page=render_fn: page(context),
                title=title,
                icon=icon,
                url_path=url_path,
            )
            for title, url_path, icon, render_fn in pages
        ]
        st.navigation(st_pages).run()
        return

    # Backward compatible fallback for older Streamlit versions.
    labels = [title for title, _, _, _ in pages]
    label_to_page = {title: render_fn for title, _, _, render_fn in pages}
    choice = st.sidebar.radio("Pages", labels, index=0)
    label_to_page[choice](context)


if __name__ == "__main__":
    settings_arg = sys.argv[1] if len(sys.argv) > 1 else "config/settings.yaml"
    main(settings_arg)
