"""Dashboard ingestion traces placeholder page."""

from __future__ import annotations

from typing import Any


def render(context: dict[str, Any] | None = None) -> None:
    import streamlit as st

    _ = context
    st.title("Ingestion Traces")
    st.info("Coming in G5: ingestion trace history and stage timing waterfall.")
