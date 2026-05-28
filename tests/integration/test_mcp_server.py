"""Integration tests for MCP server stdio workflow."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
from core.types import RetrievalResult
from mcp_server.protocol_handler import ProtocolHandler


def _write_settings(path: Path, persist_directory: Path) -> None:
    payload = f"""
project:
  name: test
  environment: local
llm:
  provider: openai
  model: gpt-4o-mini
embedding:
  provider: openai
  model: text-embedding-3-small
vector_store:
  provider: chroma
  persist_directory: {persist_directory.as_posix()}
retrieval:
  top_k: 5
rerank:
  enabled: false
  provider: none
evaluation:
  provider: custom
observability:
  traces_path: logs/traces.jsonl
  app_log_path: logs/app.log
ingestion:
  bm25_indexer:
    index_dir: data/db/bm25
"""
    path.write_text(payload.strip() + "\n", encoding="utf-8")


def _send_frame(proc: subprocess.Popen[bytes], payload: dict[str, Any]) -> None:
    raw = json.dumps(payload).encode("utf-8")
    frame = f"Content-Length: {len(raw)}\r\n\r\n".encode("ascii") + raw
    assert proc.stdin is not None
    proc.stdin.write(frame)
    proc.stdin.flush()


def _read_frame(proc: subprocess.Popen[bytes]) -> dict[str, Any]:
    assert proc.stdout is not None
    header = proc.stdout.readline()
    assert header.startswith(b"Content-Length:")
    length = int(header.split(b":", 1)[1].strip())
    blank = proc.stdout.readline()
    assert blank in (b"\r\n", b"\n")
    body = proc.stdout.read(length)
    return json.loads(body.decode("utf-8"))


@pytest.mark.integration
def test_mcp_server_initialize_tools_and_stdio_contract(tmp_path: Path) -> None:
    persist_directory = tmp_path / "chroma"
    persist_directory.mkdir(parents=True)
    (persist_directory / "demo.json").write_text("{}", encoding="utf-8")
    settings_path = tmp_path / "settings.yaml"
    _write_settings(settings_path, persist_directory)

    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"src{os.pathsep}{existing}" if existing else "src"

    proc = subprocess.Popen(
        [sys.executable, "-m", "mcp_server.server", "--config", str(settings_path)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(Path(__file__).resolve().parents[2]),
        env=env,
    )
    try:
        _send_frame(
            proc,
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {"protocolVersion": "2025-06-18"},
            },
        )
        resp_init = _read_frame(proc)
        assert resp_init["result"]["serverInfo"]["name"] == "modular-rag-mcp-server"

        _send_frame(
            proc,
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        )
        resp_list = _read_frame(proc)
        names = [item["name"] for item in resp_list["result"]["tools"]]
        assert "query_knowledge_hub" in names
        assert "list_collections" in names
        assert "get_document_summary" in names

        _send_frame(
            proc,
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": "list_collections", "arguments": {}},
            },
        )
        resp_call = _read_frame(proc)
        assert resp_call["result"]["structuredContent"]["collections"] == ["demo"]

        _send_frame(
            proc,
            {"jsonrpc": "2.0", "id": 4, "method": "unknown", "params": {}},
        )
        resp_error = _read_frame(proc)
        assert resp_error["error"]["code"] == -32601
    finally:
        if proc.stdin is not None:
            proc.stdin.close()
        proc.wait(timeout=5)
        stderr_text = (
            proc.stderr.read().decode("utf-8", errors="ignore")
            if proc.stderr is not None
            else ""
        )
        assert "[mcp_server]" in stderr_text


@pytest.mark.integration
def test_mcp_tools_call_query_knowledge_hub_returns_image_content(tmp_path: Path) -> None:
    image_path = tmp_path / "img.png"
    image_path.write_bytes(b"\x89PNG\r\n\x1a\nfake")

    class FakeHybridSearch:
        def search(
            self,
            query: str,
            top_k: int | None = None,
            filters: dict[str, Any] | None = None,
            trace: Any | None = None,
        ) -> list[RetrievalResult]:
            _ = query, top_k, filters, trace
            return [
                RetrievalResult(
                    chunk_id="c1",
                    score=0.9,
                    text="chunk with image",
                    metadata={
                        "source_path": "docs/a.pdf",
                        "images": [{"id": "img1", "path": str(image_path)}],
                    },
                )
            ]

    handler = ProtocolHandler(
        settings={"vector_store": {"persist_directory": str(tmp_path)}},
        context={"hybrid_search": FakeHybridSearch()},
    )

    response = handler.handle_request(
        {
            "jsonrpc": "2.0",
            "id": 10,
            "method": "tools/call",
            "params": {
                "name": "query_knowledge_hub",
                "arguments": {"query": "q", "top_k": 1, "no_rerank": True},
            },
        }
    )

    assert response is not None
    result = response["result"]
    content = result["content"]
    assert content[0]["type"] == "text"
    image_blocks = [item for item in content if item.get("type") == "image"]
    assert len(image_blocks) == 1
    assert image_blocks[0]["mimeType"] == "image/png"
    assert isinstance(image_blocks[0]["data"], str)
