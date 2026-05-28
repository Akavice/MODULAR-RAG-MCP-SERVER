"""MCP tool: get summarized metadata for a single document id."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


TOOL_NAME = "get_document_summary"
TOOL_DESCRIPTION = "Return summary metadata for a document id."
TOOL_INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "doc_id": {"type": "string"},
        "collection": {"type": "string", "default": "default"},
    },
    "required": ["doc_id"],
    "additionalProperties": False,
}


def call(arguments: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(arguments, dict):
        raise TypeError("arguments must be a mapping")
    doc_id = arguments.get("doc_id")
    if not isinstance(doc_id, str) or not doc_id.strip():
        raise ValueError("doc_id must be a non-empty string")
    collection = arguments.get("collection", "default")
    if not isinstance(collection, str) or not collection.strip():
        raise ValueError("collection must be a non-empty string")

    settings = context.get("settings")
    if settings is None:
        raise ValueError("tool context missing settings")

    vector_store = settings.get("vector_store") if isinstance(settings, dict) else None
    persist_directory = "data/db/chroma"
    if isinstance(vector_store, dict):
        candidate = vector_store.get("persist_directory")
        if isinstance(candidate, str) and candidate.strip():
            persist_directory = candidate.strip()

    collection_file = Path(persist_directory) / f"{collection.strip()}.json"
    if not collection_file.exists():
        raise ValueError(f"document '{doc_id.strip()}' not found")

    payload = json.loads(collection_file.read_text(encoding="utf-8"))
    records = payload.get("records", {}) if isinstance(payload, dict) else {}
    if not isinstance(records, dict):
        records = {}

    matched: list[dict[str, Any]] = []
    doc_id_norm = doc_id.strip()
    for key, value in records.items():
        if not isinstance(key, str) or not isinstance(value, dict):
            continue
        metadata = value.get("metadata", {})
        source_ref = metadata.get("source_ref") if isinstance(metadata, dict) else None
        if key == doc_id_norm or str(source_ref or "").strip() == doc_id_norm or key.startswith(f"{doc_id_norm}_"):
            matched.append(value)

    if not matched:
        raise ValueError(f"document '{doc_id_norm}' not found")

    first = matched[0]
    first_metadata = first.get("metadata", {})
    title = (
        str(first_metadata.get("title")).strip()
        if isinstance(first_metadata, dict) and first_metadata.get("title") is not None
        else ""
    )
    if not title:
        text = str(first.get("text", "")).strip()
        title = text[:80] if text else doc_id_norm

    all_text = " ".join(str(item.get("text", "")).strip() for item in matched).strip()
    summary = all_text[:280] + ("..." if len(all_text) > 280 else "")

    tags: list[str] = []
    for item in matched:
        metadata = item.get("metadata", {})
        if not isinstance(metadata, dict):
            continue
        raw_tags = metadata.get("tags")
        if isinstance(raw_tags, list):
            for tag in raw_tags:
                if isinstance(tag, str) and tag.strip():
                    normalized = tag.strip().lower()
                    if normalized not in tags:
                        tags.append(normalized)

    doc_summary = {
        "doc_id": doc_id_norm,
        "collection": collection.strip(),
        "title": title,
        "summary": summary or "No summary available.",
        "tags": tags,
        "chunk_count": len(matched),
    }
    return {
        "content": [
            {
                "type": "text",
                "text": (
                    f"Document: {doc_summary['title']}\n"
                    f"Chunks: {doc_summary['chunk_count']}\n"
                    f"Summary: {doc_summary['summary']}"
                ),
            }
        ],
        "structuredContent": doc_summary,
    }
