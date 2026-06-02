"""Dashboard overview page."""

from __future__ import annotations

from typing import Any

from observability.dashboard.services.config_service import ConfigService, SettingsError
from observability.dashboard.services.i18n import locale_from_context, t


def render(context: dict[str, Any] | None = None) -> None:
    """Render dashboard overview with component config and local stats."""
    import streamlit as st

    locale = locale_from_context(context)
    settings_path = "config/settings.yaml"
    if isinstance(context, dict):
        raw_path = context.get("settings_path")
        if isinstance(raw_path, str) and raw_path.strip():
            settings_path = raw_path.strip()

    st.title(t("overview.title", locale=locale))
    st.caption(t("overview.caption", locale=locale))

    service = ConfigService(settings_path=settings_path)
    try:
        overview = service.build_overview()
    except SettingsError as exc:
        st.error(t("common.failed_load_settings", locale=locale, error=exc))
        st.info(t("common.current_settings_path", locale=locale, path=settings_path))
        return

    cols = st.columns(4)
    cols[0].metric(t("overview.metric.collections", locale=locale), overview.stats["collections"])
    cols[1].metric(t("overview.metric.chunks", locale=locale), overview.stats["chunks"])
    cols[2].metric(t("overview.metric.images", locale=locale), overview.stats["images"])
    cols[3].metric(t("overview.metric.traces", locale=locale), overview.stats["traces"])

    st.subheader(t("overview.components", locale=locale))
    for item in overview.components:
        with st.container(border=True):
            st.markdown(
                f"**{item['name']}**  \n"
                f"{t('overview.component.provider', locale=locale)}: `{item['provider']}`  \n"
                f"{t('overview.component.config', locale=locale)}: `{item['model']}`"
            )

    st.subheader(t("overview.settings_summary", locale=locale))
    st.json(
        {
            "project": overview.settings.project,
            "vector_store": overview.settings.vector_store,
            "observability": overview.settings.observability,
        }
    )
