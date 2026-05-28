"""MCP stdio server entrypoint."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Any, BinaryIO

from core.settings import SettingsError, load_settings
from mcp_server.protocol_handler import JSONRPC_VERSION, ProtocolError, ProtocolHandler


@dataclass(slots=True)
class StdioMessageIO:
    """Read/write MCP messages over stdio with Content-Length framing."""

    reader: BinaryIO
    writer: BinaryIO
    err: Any

    def read_message(self) -> dict[str, Any] | None:
        while True:
            first_line = self.reader.readline()
            if first_line == b"":
                return None
            if not first_line.strip():
                continue

            if first_line.lower().startswith(b"content-length:"):
                content_length = self._parse_content_length(first_line)
                # Consume remaining headers until blank line.
                while True:
                    header_line = self.reader.readline()
                    if header_line == b"":
                        return None
                    if header_line in (b"\r\n", b"\n"):
                        break
                payload = self.reader.read(content_length)
                if len(payload) != content_length:
                    return None
                return json.loads(payload.decode("utf-8"))

            # Fallback mode for newline-delimited JSON used in local tests.
            return json.loads(first_line.decode("utf-8"))

    def write_message(self, payload: dict[str, Any]) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        header = f"Content-Length: {len(raw)}\r\n\r\n".encode("ascii")
        self.writer.write(header)
        self.writer.write(raw)
        self.writer.flush()

    @staticmethod
    def _parse_content_length(line: bytes) -> int:
        text = line.decode("ascii", errors="ignore")
        _, _, raw = text.partition(":")
        length_text = raw.strip()
        if not length_text.isdigit():
            raise ValueError("invalid Content-Length header")
        length = int(length_text)
        if length < 0:
            raise ValueError("invalid negative Content-Length")
        return length


class MCPServer:
    """Minimal MCP server loop over stdio transport."""

    def __init__(self, handler: ProtocolHandler, io: StdioMessageIO) -> None:
        self.handler = handler
        self.io = io

    def run(self) -> int:
        self._log("server started")
        while True:
            try:
                request = self.io.read_message()
            except json.JSONDecodeError as exc:
                self._write_error(
                    request_id=None,
                    code=-32600,
                    message="Invalid Request: malformed JSON",
                    data={"reason": str(exc)},
                )
                continue
            except Exception as exc:
                self._write_error(
                    request_id=None,
                    code=-32600,
                    message="Invalid Request",
                    data={"reason": str(exc)},
                )
                continue

            if request is None:
                self._log("stdin closed")
                return 0

            try:
                response = self.handler.handle_request(request)
            except ProtocolError as exc:
                request_id = request.get("id") if isinstance(request, dict) else None
                self._write_error(
                    request_id=request_id,
                    code=exc.code,
                    message=exc.message,
                    data=exc.data,
                )
                continue

            if response is not None:
                self.io.write_message(response)

    def _write_error(
        self,
        *,
        request_id: Any,
        code: int,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> None:
        error_obj: dict[str, Any] = {"code": code, "message": message}
        if data is not None:
            error_obj["data"] = data
        self.io.write_message(
            {"jsonrpc": JSONRPC_VERSION, "id": request_id, "error": error_obj}
        )

    def _log(self, message: str) -> None:
        self.io.err.write(f"[mcp_server] {message}\n")
        self.io.err.flush()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run MCP server on stdio.")
    parser.add_argument(
        "--config",
        default="config/settings.yaml",
        help="Settings file path (default: config/settings.yaml)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        settings_obj = load_settings(args.config)
    except SettingsError as exc:
        sys.stderr.write(f"[mcp_server] configuration error: {exc}\n")
        sys.stderr.flush()
        return 1

    settings = {
        "project": settings_obj.project,
        "ingestion": settings_obj.ingestion,
        "llm": settings_obj.llm,
        "embedding": settings_obj.embedding,
        "vector_store": settings_obj.vector_store,
        "retrieval": settings_obj.retrieval,
        "rerank": settings_obj.rerank,
        "evaluation": settings_obj.evaluation,
        "observability": settings_obj.observability,
    }
    handler = ProtocolHandler(settings=settings)
    io = StdioMessageIO(
        reader=sys.stdin.buffer,
        writer=sys.stdout.buffer,
        err=sys.stderr,
    )
    server = MCPServer(handler=handler, io=io)
    return server.run()


if __name__ == "__main__":
    raise SystemExit(main())
