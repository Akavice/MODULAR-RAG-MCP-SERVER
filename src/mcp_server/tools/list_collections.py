"""MCP tool: list available local vector-store collections."""

from __future__ import annotations

from pathlib import Path
from typing import Any


TOOL_NAME = "list_collections"
TOOL_DESCRIPTION = "List available collections in local vector store."
TOOL_INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {},
    "additionalProperties": False,
}


def call(arguments: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(arguments, dict):
        raise TypeError("arguments must be a mapping")
    if arguments:
        raise ValueError("list_collections does not accept arguments")

    settings = context.get("settings")
    if settings is None:
        raise ValueError("tool context missing settings")

    vector_store = settings.get("vector_store") if isinstance(settings, dict) else None
    persist_directory = "data/db/chroma"
    if isinstance(vector_store, dict):
        candidate = vector_store.get("persist_directory")
        if isinstance(candidate, str) and candidate.strip():
            persist_directory = candidate.strip()

    root = Path(persist_directory)
    collections: list[str] = []
    if root.exists() and root.is_dir():
        for item in root.iterdir():
            if not item.is_file():
                continue
            if item.suffix.lower() != ".json":
                continue
            if item.name.endswith(".tmp"):
                continue
            collections.append(item.stem)

    collections = sorted(dict.fromkeys(collections))
    lines = "\n".join(f"- {name}" for name in collections) or "- <none>"
    return {
        "content": [
            {
                "type": "text",
                "text": f"Available collections:\n{lines}",
            }
        ],
        "structuredContent": {"collections": collections},
    }
