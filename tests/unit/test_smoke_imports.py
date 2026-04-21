"""Smoke tests for the initial project scaffold."""

import importlib

import pytest


MODULES = (
    "mcp_server",
    "core",
    "ingestion",
    "libs",
    "observability",
    "mcp_server.server",
    "core.settings",
    "observability.logger",
)


@pytest.mark.unit
@pytest.mark.parametrize("module_name", MODULES)
def test_scaffold_modules_import(module_name: str) -> None:
    """Ensure the initial scaffold can be imported from the repo root."""
    module = importlib.import_module(module_name)
    assert module is not None
