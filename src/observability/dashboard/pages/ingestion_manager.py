"""Dashboard ingestion manager page."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any

from core.settings import SettingsError, load_settings
from ingestion.pipeline import IngestionPipeline
from observability.dashboard.services.data_service import DataService


def render(context: dict[str, Any] | None = None) -> None:
    import streamlit as st

    st.title("Ingestion Manager")
    st.info("Upload a PDF, trigger ingestion, watch progress, and delete ingested documents.")

    settings_path = _resolve_settings_path(context)
    service = DataService(settings_path=settings_path)

    upload = st.file_uploader("Upload PDF", type=["pdf"])
    collection_input = _call_st(
        st,
        "text_input",
        "Collection",
        value="default",
        help="Target collection for this ingestion run.",
    )
    force_value = _call_st(
        st,
        "checkbox",
        "Force reingestion",
        value=False,
        help="Ignore SHA256 skip check and ingest anyway.",
    )
    force = bool(force_value) if isinstance(force_value, bool) else False
    progress = st.progress(0.0)

    if st.button("Start Ingestion", type="primary"):
        if upload is None:
            _notify(st, "warning", "Please select a PDF file before ingestion.")
        else:
            _run_ingestion(
                st=st,
                settings_path=settings_path,
                upload=upload,
                collection=collection_input if isinstance(collection_input, str) else "default",
                force=force,
                progress=progress,
            )

    try:
        documents = service.list_documents()
    except SettingsError as exc:
        _notify(st, "error", f"Failed to load settings: {exc}")
        _notify(st, "info", f"Current settings path: `{settings_path}`")
        return

    if not documents:
        _notify(st, "info", "No ingested documents yet.")
        return

    rows = [
        {
            "Collection": doc.collection,
            "Source Path": doc.source_path,
            "Chunks": doc.chunk_count,
            "Images": doc.image_count,
            "Ingested At": doc.ingested_at or "-",
        }
        for doc in documents
    ]
    st.dataframe(rows, use_container_width=True, hide_index=True)

    manager = service.get_document_manager()
    for doc in documents:
        key = f"delete::{doc.doc_id}"
        label = f"Delete [{doc.collection}] {Path(doc.source_path).name}"
        if st.button(label, key=key):
            result = manager.delete_document(doc.source_path, doc.collection)
            if result.deleted:
                _notify(st, "success", f"Deleted document: {doc.source_path}")
            else:
                _notify(st, "warning", f"No records deleted: {doc.source_path}")
            _rerun(st)


def _run_ingestion(
    *,
    st: Any,
    settings_path: str,
    upload: Any,
    collection: str,
    force: bool,
    progress: Any,
) -> None:
    temp_file: Path | None = None
    try:
        settings = load_settings(settings_path)
        pipeline = IngestionPipeline(settings)
        temp_file = _save_uploaded_file(upload)
        target_collection = _normalize_collection(collection)

        def on_progress(stage: str, current: int, total: int) -> None:
            ratio = 0.0 if total <= 0 else max(0.0, min(1.0, float(current) / float(total)))
            _update_progress(progress, ratio, text=f"{stage} ({current}/{total})")

        result = pipeline.run(
            str(temp_file),
            collection=target_collection,
            force=force,
            on_progress=on_progress,
        )
        _update_progress(progress, 1.0, text="ingestion finished")
        _notify(
            st,
            "success",
            f"Ingestion {result.status}: chunks={result.chunk_count}, records={result.record_count}",
        )
    except Exception as exc:
        _notify(st, "error", f"Ingestion failed: {exc}")
    finally:
        if temp_file is not None:
            try:
                temp_file.unlink(missing_ok=True)
            except Exception:
                pass


def _save_uploaded_file(upload: Any) -> Path:
    name = getattr(upload, "name", None)
    suffix = Path(str(name)).suffix if isinstance(name, str) and name.strip() else ".pdf"
    fd, tmp_path = tempfile.mkstemp(prefix="dashboard_ingest_", suffix=suffix or ".pdf")
    path = Path(tmp_path)
    try:
        payload = None
        if hasattr(upload, "getvalue"):
            payload = upload.getvalue()
        elif hasattr(upload, "getbuffer"):
            payload = bytes(upload.getbuffer())
        elif hasattr(upload, "read"):
            payload = upload.read()
        if not isinstance(payload, (bytes, bytearray)):
            raise TypeError("uploaded file payload must be bytes")
        path.write_bytes(bytes(payload))
        return path
    finally:
        try:
            os.close(fd)
        except Exception:
            pass


def _resolve_settings_path(context: dict[str, Any] | None) -> str:
    if isinstance(context, dict):
        value = context.get("settings_path")
        if isinstance(value, str) and value.strip():
            return value.strip()
    return "config/settings.yaml"


def _normalize_collection(value: str) -> str:
    if not isinstance(value, str):
        return "default"
    normalized = value.strip()
    return normalized or "default"


def _update_progress(progress: Any, ratio: float, *, text: str) -> None:
    if progress is None or not hasattr(progress, "progress"):
        return
    try:
        progress.progress(ratio, text=text)
    except TypeError:
        progress.progress(ratio)


def _notify(st: Any, level: str, message: str) -> None:
    fn = getattr(st, level, None)
    if callable(fn):
        fn(message)
        return
    fallback = getattr(st, "info", None) or getattr(st, "warning", None)
    if callable(fallback):
        fallback(message)


def _rerun(st: Any) -> None:
    fn = getattr(st, "rerun", None) or getattr(st, "experimental_rerun", None)
    if callable(fn):
        fn()


def _call_st(st: Any, method: str, *args: Any, **kwargs: Any) -> Any:
    fn = getattr(st, method, None)
    if callable(fn):
        return fn(*args, **kwargs)
    return None
