"""Unit tests for MCP protocol handler behavior."""

from __future__ import annotations

import pytest

from mcp_server.protocol_handler import ProtocolError, ProtocolHandler
from mcp_server.tools import ToolDefinition


def _handler_with_fake_tool() -> ProtocolHandler:
    def fake_tool(arguments: dict[str, object], context: dict[str, object]) -> dict[str, object]:
        _ = context
        return {"echo": arguments}

    registry = {
        "fake": ToolDefinition(
            name="fake",
            description="fake tool",
            input_schema={"type": "object", "properties": {}},
            handler=fake_tool,
        )
    }
    return ProtocolHandler(settings={"vector_store": {}}, tool_registry=registry)


@pytest.mark.unit
def test_handle_initialize_returns_server_info_and_capabilities() -> None:
    handler = _handler_with_fake_tool()

    response = handler.handle_request(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"protocolVersion": "2025-06-18"},
        }
    )

    assert response is not None
    result = response["result"]
    assert result["serverInfo"]["name"] == "modular-rag-mcp-server"
    assert "tools" in result["capabilities"]


@pytest.mark.unit
def test_handle_tools_list_returns_registered_tool_schema() -> None:
    handler = _handler_with_fake_tool()

    response = handler.handle_request(
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
    )

    tools = response["result"]["tools"]
    assert len(tools) == 1
    assert tools[0]["name"] == "fake"
    assert tools[0]["description"] == "fake tool"


@pytest.mark.unit
def test_handle_tools_call_routes_to_handler() -> None:
    handler = _handler_with_fake_tool()

    response = handler.handle_request(
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "fake", "arguments": {"x": 1}},
        }
    )

    assert response["result"]["echo"] == {"x": 1}


@pytest.mark.unit
def test_invalid_method_raises_protocol_error() -> None:
    handler = _handler_with_fake_tool()
    with pytest.raises(ProtocolError) as exc_info:
        handler.handle_request(
            {"jsonrpc": "2.0", "id": 4, "method": "unknown", "params": {}}
        )
    assert exc_info.value.code == -32601


@pytest.mark.unit
def test_invalid_tools_call_params_raises_protocol_error() -> None:
    handler = _handler_with_fake_tool()
    with pytest.raises(ProtocolError) as exc_info:
        handler.handle_request(
            {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "tools/call",
                "params": {"name": "fake", "arguments": "bad"},
            }
        )
    assert exc_info.value.code == -32602
