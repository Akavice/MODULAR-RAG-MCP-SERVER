"""Dashboard evaluation panel placeholder page."""

from __future__ import annotations

from typing import Any

from observability.dashboard.services.i18n import locale_from_context, t


def render(context: dict[str, Any] | None = None) -> None:
    import streamlit as st

    locale = locale_from_context(context)
    st.title(t("evaluation_panel.title", locale=locale))
    st.info(t("evaluation_panel.placeholder", locale=locale))
