"""Dashboard ingestion manager page."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any

from core.settings import SettingsError, load_settings
from ingestion.pipeline import IngestionPipeline
from observability.dashboard.services.data_service import DataService
from observability.dashboard.services.i18n import locale_from_context, t


def render(context: dict[str, Any] | None = None) -> None:
    import streamlit as st

    locale = locale_from_context(context)
    st.title(t("ingestion_manager.title", locale=locale))
    st.info(t("ingestion_manager.caption", locale=locale))

    settings_path = _resolve_settings_path(context)
    service = DataService(settings_path=settings_path)

    upload = st.file_uploader(t("ingestion_manager.upload_pdf", locale=locale), type=["pdf"])
    collection_input = _call_st(
        st,
        "text_input",
        t("ingestion_manager.collection", locale=locale),
        value="default",
        help=t("ingestion_manager.collection_help", locale=locale),
    )
    force_value = _call_st(
        st,
        "checkbox",
        t("ingestion_manager.force", locale=locale),
        value=False,
        help=t("ingestion_manager.force_help", locale=locale),
    )
    force = bool(force_value) if isinstance(force_value, bool) else False
    progress = st.progress(0.0)

    if st.button(t("ingestion_manager.start", locale=locale), type="primary"):
        if upload is None:
            _notify(st, "warning", t("ingestion_manager.warn.select_pdf", locale=locale))
        else:
            _run_ingestion(
                st=st,
                settings_path=settings_path,
                upload=upload,
                collection=collection_input if isinstance(collection_input, str) else "default",
                force=force,
                progress=progress,
                locale=locale,
            )

    try:
        documents = service.list_documents()
    except SettingsError as exc:
        _notify(st, "error", t("common.failed_load_settings", locale=locale, error=exc))
        _notify(st, "info", t("common.current_settings_path", locale=locale, path=settings_path))
        return

    if not documents:
        _notify(st, "info", t("ingestion_manager.info.no_documents", locale=locale))
        return

    placeholder = t("common.placeholder", locale=locale)
    rows = [
        {
            t("data_browser.table.collection", locale=locale): doc.collection,
            t("data_browser.table.source_path", locale=locale): doc.source_path,
            t("data_browser.table.chunks", locale=locale): doc.chunk_count,
            t("data_browser.table.images", locale=locale): doc.image_count,
            t("data_browser.table.ingested_at", locale=locale): doc.ingested_at or placeholder,
        }
        for doc in documents
    ]
    st.dataframe(rows, use_container_width=True, hide_index=True)

    manager = service.get_document_manager()
    for doc in documents:
        key = f"delete::{doc.doc_id}"
        label = t(
            "ingestion_manager.delete_button",
            locale=locale,
            collection=doc.collection,
            name=Path(doc.source_path).name,
        )
        if st.button(label, key=key):
            result = manager.delete_document(doc.source_path, doc.collection)
            if result.deleted:
                _notify(st, "success", t("ingestion_manager.delete_success", locale=locale, source_path=doc.source_path))
            else:
                _notify(st, "warning", t("ingestion_manager.delete_noop", locale=locale, source_path=doc.source_path))
            _rerun(st)


def _run_ingestion(
    *,
    st: Any,
    settings_path: str,
    upload: Any,
    collection: str,
    force: bool,
    progress: Any,
    locale: str,
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
        _update_progress(progress, 1.0, text=t("ingestion_manager.progress_done", locale=locale))
        _notify(
            st,
            "success",
            t(
                "ingestion_manager.success",
                locale=locale,
                status=result.status,
                chunks=result.chunk_count,
                records=result.record_count,
            ),
        )
    except Exception as exc:
        _notify(st, "error", t("ingestion_manager.error_failed", locale=locale, error=exc))
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
