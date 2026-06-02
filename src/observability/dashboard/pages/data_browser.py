"""Dashboard data browser page."""

from __future__ import annotations

from typing import Any

from observability.dashboard.services.data_service import DataService, SettingsError
from observability.dashboard.services.i18n import locale_from_context, t


def render(context: dict[str, Any] | None = None) -> None:
    import streamlit as st

    locale = locale_from_context(context)
    st.title(t("data_browser.title", locale=locale))
    st.caption(t("data_browser.caption", locale=locale))

    settings_path = "config/settings.yaml"
    if isinstance(context, dict):
        raw_path = context.get("settings_path")
        if isinstance(raw_path, str) and raw_path.strip():
            settings_path = raw_path.strip()

    service = DataService(settings_path=settings_path)
    try:
        collections = service.list_collections()
    except SettingsError as exc:
        st.error(t("common.failed_load_settings", locale=locale, error=exc))
        st.info(t("common.current_settings_path", locale=locale, path=settings_path))
        return

    all_collections = t("data_browser.collection.all", locale=locale)
    options = [all_collections, *collections]
    selected = st.selectbox(t("data_browser.select.collection", locale=locale), options, index=0)
    selected_collection = None if selected == all_collections else selected

    documents = service.list_documents(collection=selected_collection)
    st.metric(t("data_browser.metric.documents", locale=locale), len(documents))
    if not documents:
        st.info(t("data_browser.info.no_documents", locale=locale))
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

    st.subheader(t("data_browser.details", locale=locale))
    for doc in documents:
        label = f"{doc.collection} | {doc.source_path}"
        with st.expander(label, expanded=False):
            detail = service.get_document_detail(doc.doc_id)
            meta_cols = st.columns(3)
            meta_cols[0].metric(t("data_browser.table.chunks", locale=locale), detail.chunk_count)
            meta_cols[1].metric(t("data_browser.table.images", locale=locale), detail.image_count)
            meta_cols[2].metric(t("data_browser.metric.file_hashes", locale=locale), len(detail.file_hashes))
            if detail.file_hashes:
                st.caption(f"{t('data_browser.hashes_prefix', locale=locale)}: " + ", ".join(detail.file_hashes))

            for index, chunk in enumerate(detail.chunks, start=1):
                chunk_id = str(chunk.get("id", f"chunk-{index}"))
                chunk_text = str(chunk.get("text", ""))
                metadata = chunk.get("metadata", {})
                if not isinstance(metadata, dict):
                    metadata = {}

                with st.container(border=True):
                    st.markdown(f"**{t('data_browser.chunk_prefix', locale=locale)} {index}**  `{chunk_id}`")
                    st.text(chunk_text)
                    st.json(metadata)

                    images = metadata.get("images")
                    if isinstance(images, list) and images:
                        st.caption(t("data_browser.linked_images", locale=locale))
                        for image_item in images:
                            if not isinstance(image_item, dict):
                                continue
                            image_id = image_item.get("id")
                            image_path = image_item.get("path")
                            if isinstance(image_path, str) and image_path.strip():
                                caption = str(image_id) if isinstance(image_id, str) else t(
                                    "data_browser.image_fallback",
                                    locale=locale,
                                )
                                st.image(image_path.strip(), caption=caption, width=360)
