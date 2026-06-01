"""Application and trace logging helpers."""

from __future__ import annotations

import json
import logging
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


_LOGGER_CONFIGURED = False
_TRACE_LOGGERS: dict[Path, logging.Logger] = {}


def get_logger(name: str | None = None) -> logging.Logger:
    """Return a stderr logger with a minimal shared configuration."""
    global _LOGGER_CONFIGURED

    if not _LOGGER_CONFIGURED:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))

        root_logger = logging.getLogger("modular_rag")
        root_logger.setLevel(logging.INFO)
        root_logger.handlers.clear()
        root_logger.addHandler(handler)
        root_logger.propagate = False
        _LOGGER_CONFIGURED = True

    logger_name = "modular_rag" if name is None else f"modular_rag.{name}"
    return logging.getLogger(logger_name)


class _JsonLinesFormatter(logging.Formatter):
    """Formatter that writes one compact JSON object per line."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(timespec="milliseconds"),
            "level": record.levelname,
            "logger": record.name,
        }
        if isinstance(record.msg, dict):
            payload.update(record.msg)
        else:
            payload["message"] = record.getMessage()
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def get_trace_logger(traces_path: str | Path = "logs/traces.jsonl") -> logging.Logger:
    """Return a JSONL trace logger that appends records to the target file."""
    path = _normalize_log_path(traces_path)
    cached = _TRACE_LOGGERS.get(path)
    if cached is not None:
        return cached

    path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(f"modular_rag.trace.{path.as_posix()}")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.propagate = False

    handler = logging.FileHandler(path, encoding="utf-8")
    handler.setFormatter(_JsonLinesFormatter())
    logger.addHandler(handler)

    _TRACE_LOGGERS[path] = logger
    return logger


def write_trace(trace_dict: dict[str, Any], *, traces_path: str | Path = "logs/traces.jsonl") -> None:
    """Append one trace dictionary as a single JSON line."""
    if not isinstance(trace_dict, dict):
        raise TypeError("trace_dict must be a mapping")
    get_trace_logger(traces_path).info(trace_dict)


def _normalize_log_path(path: str | Path) -> Path:
    if isinstance(path, Path):
        norm = path
    elif isinstance(path, str):
        if not path.strip():
            raise ValueError("log path must be a non-empty string")
        norm = Path(path.strip())
    else:
        raise TypeError("log path must be a string or Path")
    return norm
