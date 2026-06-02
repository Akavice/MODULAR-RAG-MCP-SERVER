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
from observability.dashboard.services.i18n import (
    SUPPORTED_LOCALES,
    get_locale,
    set_locale,
    t,
)


PageRender = Callable[[dict[str, Any]], None]


def main(settings_path: str = "config/settings.yaml") -> None:
    """Render dashboard with multi-page navigation."""
    import streamlit as st

    locale = get_locale(st.session_state)
    st.set_page_config(
        page_title=t("app.page_title", locale=locale),
        page_icon=":material/analytics:",
        layout="wide",
    )
    locale = _render_locale_switcher(st, locale)
    context = {"settings_path": settings_path, "locale": locale}
    pages: list[tuple[str, str, str, PageRender]] = [
        (t("app.nav.overview", locale=locale), "overview", ":material/home:", overview.render),
        (t("app.nav.data_browser", locale=locale), "data-browser", ":material/folder_open:", data_browser.render),
        (t("app.nav.ingestion_manager", locale=locale), "ingestion-manager", ":material/upload_file:", ingestion_manager.render),
        (t("app.nav.ingestion_traces", locale=locale), "ingestion-traces", ":material/monitoring:", ingestion_traces.render),
        (t("app.nav.query_traces", locale=locale), "query-traces", ":material/search:", query_traces.render),
        (t("app.nav.evaluation_panel", locale=locale), "evaluation-panel", ":material/insights:", evaluation_panel.render),
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
    choice = st.sidebar.radio(t("app.sidebar.pages", locale=locale), labels, index=0)
    label_to_page[choice](context)


def _render_locale_switcher(st: Any, current_locale: str) -> str:
    left, right = st.columns([8, 1])
    with right:
        selected_locale = st.selectbox(
            t("app.language_label", locale=current_locale),
            list(SUPPORTED_LOCALES),
            index=list(SUPPORTED_LOCALES).index(current_locale),
            format_func=lambda code: t("app.language.zh", locale=current_locale)
            if code == "zh-CN"
            else t("app.language.en", locale=current_locale),
            label_visibility="collapsed",
            key="_dashboard_locale_selector",
        )
    with left:
        st.empty()

    return set_locale(st.session_state, selected_locale)


if __name__ == "__main__":
    settings_arg = sys.argv[1] if len(sys.argv) > 1 else "config/settings.yaml"
    main(settings_arg)
