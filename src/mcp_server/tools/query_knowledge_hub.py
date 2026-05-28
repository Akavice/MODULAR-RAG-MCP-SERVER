"""MCP tool: query knowledge hub via hybrid retrieval + optional rerank."""

from __future__ import annotations

from typing import Any

from core.query_engine.hybrid_search import HybridSearch
from core.query_engine.reranker import Reranker
from core.response.multimodal_assembler import MultimodalAssembler
from core.response.response_builder import ResponseBuilder
from core.trace.trace_context import TraceContext


TOOL_NAME = "query_knowledge_hub"
TOOL_DESCRIPTION = "Search the knowledge hub and return ranked results with citations."
TOOL_INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "query": {"type": "string", "description": "User query text"},
        "top_k": {"type": "integer", "minimum": 1, "default": 5},
        "collection": {"type": "string"},
        "no_rerank": {"type": "boolean", "default": False},
    },
    "required": ["query"],
    "additionalProperties": False,
}


def call(arguments: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(arguments, dict):
        raise TypeError("arguments must be a mapping")
    query = arguments.get("query")
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must be a non-empty string")
    top_k = arguments.get("top_k", 5)
    if isinstance(top_k, bool) or not isinstance(top_k, int):
        raise TypeError("top_k must be an integer")
    if top_k <= 0:
        raise ValueError("top_k must be greater than 0")

    collection = arguments.get("collection")
    if collection is not None and (not isinstance(collection, str) or not collection.strip()):
        raise ValueError("collection must be a non-empty string when provided")
    no_rerank = arguments.get("no_rerank", False)
    if not isinstance(no_rerank, bool):
        raise TypeError("no_rerank must be a boolean")

    settings = context.get("settings")
    if settings is None:
        raise ValueError("tool context missing settings")

    hybrid_search = context.get("hybrid_search") or HybridSearch(settings)
    reranker = context.get("reranker") or Reranker(settings)
    response_builder = context.get("response_builder") or ResponseBuilder()
    multimodal_assembler = context.get("multimodal_assembler") or MultimodalAssembler()

    filters = {"collection": collection.strip()} if isinstance(collection, str) else None
    trace = TraceContext(trace_type="query")

    retrieval_results = hybrid_search.search(
        query=query.strip(),
        top_k=top_k,
        filters=filters,
        trace=trace,
    )
    final_results = (
        retrieval_results if no_rerank else reranker.rerank(query.strip(), retrieval_results, trace=trace)
    )
    base_payload = response_builder.build(final_results[:top_k], query=query.strip())
    return multimodal_assembler.assemble(base_payload, final_results[:top_k])
