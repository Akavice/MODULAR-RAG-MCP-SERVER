"""Dashboard data browser page."""

from __future__ import annotations

from typing import Any

from observability.dashboard.services.data_service import DataService, SettingsError


def render(context: dict[str, Any] | None = None) -> None:
    import streamlit as st

    st.title("Data Browser")
    st.caption("Browse ingested documents, chunk details, and linked images.")

    settings_path = "config/settings.yaml"
    if isinstance(context, dict):
        raw_path = context.get("settings_path")
        if isinstance(raw_path, str) and raw_path.strip():
            settings_path = raw_path.strip()

    service = DataService(settings_path=settings_path)
    try:
        collections = service.list_collections()
    except SettingsError as exc:
        st.error(f"Failed to load settings: {exc}")
        st.info(f"Current settings path: `{settings_path}`")
        return

    options = ["All Collections", *collections]
    selected = st.selectbox("Collection", options, index=0)
    selected_collection = None if selected == "All Collections" else selected

    documents = service.list_documents(collection=selected_collection)
    st.metric("Documents", len(documents))
    if not documents:
        st.info("No documents found. Run ingestion first.")
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

    st.subheader("Document Details")
    for doc in documents:
        label = f"{doc.collection} | {doc.source_path}"
        with st.expander(label, expanded=False):
            detail = service.get_document_detail(doc.doc_id)
            meta_cols = st.columns(3)
            meta_cols[0].metric("Chunks", detail.chunk_count)
            meta_cols[1].metric("Images", detail.image_count)
            meta_cols[2].metric("File Hashes", len(detail.file_hashes))
            if detail.file_hashes:
                st.caption("Hashes: " + ", ".join(detail.file_hashes))

            for index, chunk in enumerate(detail.chunks, start=1):
                chunk_id = str(chunk.get("id", f"chunk-{index}"))
                chunk_text = str(chunk.get("text", ""))
                metadata = chunk.get("metadata", {})
                if not isinstance(metadata, dict):
                    metadata = {}

                with st.container(border=True):
                    st.markdown(f"**Chunk {index}**  `{chunk_id}`")
                    st.text(chunk_text)
                    st.json(metadata)

                    images = metadata.get("images")
                    if isinstance(images, list) and images:
                        st.caption("Linked Images")
                        for image_item in images:
                            if not isinstance(image_item, dict):
                                continue
                            image_id = image_item.get("id")
                            image_path = image_item.get("path")
                            if isinstance(image_path, str) and image_path.strip():
                                caption = str(image_id) if isinstance(image_id, str) else "image"
                                st.image(image_path.strip(), caption=caption, width=360)
