"""Tool definitions exposed by the MCP server."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from mcp_server.tools.get_document_summary import (
    TOOL_DESCRIPTION as GET_DOCUMENT_SUMMARY_DESCRIPTION,
)
from mcp_server.tools.get_document_summary import TOOL_INPUT_SCHEMA as GET_DOCUMENT_SUMMARY_INPUT_SCHEMA
from mcp_server.tools.get_document_summary import TOOL_NAME as GET_DOCUMENT_SUMMARY_NAME
from mcp_server.tools.get_document_summary import call as get_document_summary_call
from mcp_server.tools.list_collections import TOOL_DESCRIPTION as LIST_COLLECTIONS_DESCRIPTION
from mcp_server.tools.list_collections import TOOL_INPUT_SCHEMA as LIST_COLLECTIONS_INPUT_SCHEMA
from mcp_server.tools.list_collections import TOOL_NAME as LIST_COLLECTIONS_NAME
from mcp_server.tools.list_collections import call as list_collections_call
from mcp_server.tools.query_knowledge_hub import TOOL_DESCRIPTION as QUERY_KNOWLEDGE_HUB_DESCRIPTION
from mcp_server.tools.query_knowledge_hub import TOOL_INPUT_SCHEMA as QUERY_KNOWLEDGE_HUB_INPUT_SCHEMA
from mcp_server.tools.query_knowledge_hub import TOOL_NAME as QUERY_KNOWLEDGE_HUB_NAME
from mcp_server.tools.query_knowledge_hub import call as query_knowledge_hub_call


@dataclass(slots=True)
class ToolDefinition:
    name: str
    description: str
    input_schema: dict[str, Any]
    handler: Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]


TOOL_DEFINITIONS: tuple[ToolDefinition, ...] = (
    ToolDefinition(
        name=QUERY_KNOWLEDGE_HUB_NAME,
        description=QUERY_KNOWLEDGE_HUB_DESCRIPTION,
        input_schema=QUERY_KNOWLEDGE_HUB_INPUT_SCHEMA,
        handler=query_knowledge_hub_call,
    ),
    ToolDefinition(
        name=LIST_COLLECTIONS_NAME,
        description=LIST_COLLECTIONS_DESCRIPTION,
        input_schema=LIST_COLLECTIONS_INPUT_SCHEMA,
        handler=list_collections_call,
    ),
    ToolDefinition(
        name=GET_DOCUMENT_SUMMARY_NAME,
        description=GET_DOCUMENT_SUMMARY_DESCRIPTION,
        input_schema=GET_DOCUMENT_SUMMARY_INPUT_SCHEMA,
        handler=get_document_summary_call,
    ),
)


def build_tool_registry() -> dict[str, ToolDefinition]:
    return {item.name: item for item in TOOL_DEFINITIONS}


__all__ = ["ToolDefinition", "TOOL_DEFINITIONS", "build_tool_registry"]
