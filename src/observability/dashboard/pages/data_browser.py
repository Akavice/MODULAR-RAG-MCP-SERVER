"""Dashboard data browser placeholder page."""

from __future__ import annotations

from typing import Any


def render(context: dict[str, Any] | None = None) -> None:
    import streamlit as st

    _ = context
    st.title("Data Browser")
    st.info("Coming in G3: browse documents, chunks, and linked images.")
