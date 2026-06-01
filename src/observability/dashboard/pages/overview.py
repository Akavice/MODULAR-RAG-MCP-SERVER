"""Dashboard overview page."""

from __future__ import annotations

from typing import Any

from observability.dashboard.services.config_service import ConfigService, SettingsError


def render(context: dict[str, Any] | None = None) -> None:
    """Render dashboard overview with component config and local stats."""
    import streamlit as st

    settings_path = "config/settings.yaml"
    if isinstance(context, dict):
        raw_path = context.get("settings_path")
        if isinstance(raw_path, str) and raw_path.strip():
            settings_path = raw_path.strip()

    st.title("System Overview")
    st.caption("Component configuration and local data status.")

    service = ConfigService(settings_path=settings_path)
    try:
        overview = service.build_overview()
    except SettingsError as exc:
        st.error(f"Failed to load settings: {exc}")
        st.info(f"Current settings path: `{settings_path}`")
        return

    cols = st.columns(4)
    cols[0].metric("Collections", overview.stats["collections"])
    cols[1].metric("Chunks", overview.stats["chunks"])
    cols[2].metric("Images", overview.stats["images"])
    cols[3].metric("Traces", overview.stats["traces"])

    st.subheader("Components")
    for item in overview.components:
        with st.container(border=True):
            st.markdown(
                f"**{item['name']}**  \n"
                f"Provider: `{item['provider']}`  \n"
                f"Config: `{item['model']}`"
            )

    st.subheader("Settings Summary")
    st.json(
        {
            "project": overview.settings.project,
            "vector_store": overview.settings.vector_store,
            "observability": overview.settings.observability,
        }
    )
