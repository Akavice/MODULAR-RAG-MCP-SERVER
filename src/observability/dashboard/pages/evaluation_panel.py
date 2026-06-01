"""Dashboard evaluation panel placeholder page."""

from __future__ import annotations

from typing import Any


def render(context: dict[str, Any] | None = None) -> None:
    import streamlit as st

    _ = context
    st.title("Evaluation Panel")
    st.info("Coming in H4: run evaluation jobs and inspect metrics.")
