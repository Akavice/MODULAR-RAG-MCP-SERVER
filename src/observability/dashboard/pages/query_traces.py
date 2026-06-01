"""Dashboard query traces placeholder page."""

from __future__ import annotations

from typing import Any


def render(context: dict[str, Any] | None = None) -> None:
    import streamlit as st

    _ = context
    st.title("Query Traces")
    st.info("Coming in G6: query trace history and dense/sparse/rerank comparison.")
