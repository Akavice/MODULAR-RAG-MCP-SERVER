"""Dashboard ingestion manager placeholder page."""

from __future__ import annotations

from typing import Any


def render(context: dict[str, Any] | None = None) -> None:
    import streamlit as st

    _ = context
    st.title("Ingestion Manager")
    st.info("Coming in G4: upload files, trigger ingestion, and manage documents.")
