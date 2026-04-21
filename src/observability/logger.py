"""Logging helpers for early scaffolding."""

import logging
import sys


_LOGGER_CONFIGURED = False


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
