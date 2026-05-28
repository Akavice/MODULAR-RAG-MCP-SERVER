"""JSON-RPC protocol handler for MCP stdio server."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from mcp_server.tools import ToolDefinition, build_tool_registry


JSONRPC_VERSION = "2.0"
SERVER_NAME = "modular-rag-mcp-server"
SERVER_VERSION = "0.1.0"
SUPPORTED_PROTOCOL_VERSION = "2025-06-18"


@dataclass(slots=True)
class ProtocolError(Exception):
    code: int
    message: str
    data: dict[str, Any] | None = None

    def to_error_object(self) -> dict[str, Any]:
        payload = {"code": self.code, "message": self.message}
        if self.data is not None:
            payload["data"] = self.data
        return payload


class ProtocolHandler:
    """Handle JSON-RPC requests and route MCP tool operations."""

    def __init__(
        self,
        *,
        settings: dict[str, Any] | None = None,
        tool_registry: dict[str, ToolDefinition] | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        self.settings = settings or {}
        self.tool_registry = tool_registry or build_tool_registry()
        self.context: dict[str, Any] = {"settings": self.settings}
        if context:
            self.context.update(dict(context))

    def handle_request(self, request: dict[str, Any]) -> dict[str, Any] | None:
        if not isinstance(request, dict):
            raise ProtocolError(-32600, "Invalid Request: request must be an object")

        if request.get("jsonrpc") != JSONRPC_VERSION:
            raise ProtocolError(-32600, "Invalid Request: jsonrpc must be '2.0'")
        method = request.get("method")
        if not isinstance(method, str) or not method.strip():
            raise ProtocolError(-32600, "Invalid Request: method must be a non-empty string")

        request_id = request.get("id")
        params = request.get("params")
        if params is not None and not isinstance(params, dict):
            raise ProtocolError(-32602, "Invalid params: params must be an object")

        try:
            if method == "initialize":
                result = self.handle_initialize(params or {})
            elif method == "tools/list":
                result = self.handle_tools_list()
            elif method == "tools/call":
                result = self.handle_tools_call(params or {})
            else:
                raise ProtocolError(-32601, f"Method not found: {method}")
        except ProtocolError:
            raise
        except Exception as exc:
            raise ProtocolError(-32603, "Internal error", {"reason": str(exc)}) from exc

        # Notification request: no response body.
        if "id" not in request:
            return None
        return {"jsonrpc": JSONRPC_VERSION, "id": request_id, "result": result}

    def handle_initialize(self, params: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(params, dict):
            raise ProtocolError(-32602, "Invalid params: initialize params must be an object")
        requested = params.get("protocolVersion")
        if requested is not None and not isinstance(requested, str):
            raise ProtocolError(-32602, "Invalid params: protocolVersion must be a string")
        protocol_version = requested or SUPPORTED_PROTOCOL_VERSION
        return {
            "protocolVersion": protocol_version,
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            "capabilities": {"tools": {}},
        }

    def handle_tools_list(self) -> dict[str, Any]:
        tools = [
            {
                "name": item.name,
                "description": item.description,
                "inputSchema": item.input_schema,
            }
            for item in sorted(self.tool_registry.values(), key=lambda x: x.name)
        ]
        return {"tools": tools}

    def handle_tools_call(self, params: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(params, dict):
            raise ProtocolError(-32602, "Invalid params: tools/call params must be an object")
        name = params.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ProtocolError(-32602, "Invalid params: tools/call requires non-empty name")
        arguments = params.get("arguments", {})
        if arguments is None:
            arguments = {}
        if not isinstance(arguments, dict):
            raise ProtocolError(-32602, "Invalid params: tools/call arguments must be an object")

        tool = self.tool_registry.get(name.strip())
        if tool is None:
            raise ProtocolError(-32601, f"Tool not found: {name}")
        try:
            result = tool.handler(dict(arguments), self.context)
        except ProtocolError:
            raise
        except (TypeError, ValueError) as exc:
            raise ProtocolError(-32602, f"Invalid params: {exc}") from exc
        except Exception as exc:
            raise ProtocolError(-32603, "Internal error", {"reason": str(exc)}) from exc
        if not isinstance(result, dict):
            raise ProtocolError(-32603, "Internal error", {"reason": "tool must return a mapping"})
        return result


__all__ = [
    "JSONRPC_VERSION",
    "ProtocolError",
    "ProtocolHandler",
    "SERVER_NAME",
    "SERVER_VERSION",
    "SUPPORTED_PROTOCOL_VERSION",
]
