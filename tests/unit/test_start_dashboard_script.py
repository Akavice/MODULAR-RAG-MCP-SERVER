"""Unit tests for dashboard start script (G1)."""

from __future__ import annotations

import subprocess

import pytest

from scripts import start_dashboard


@pytest.mark.unit
def test_start_dashboard_builds_streamlit_command(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    def _fake_run(command: list[str], check: bool = False) -> subprocess.CompletedProcess[str]:
        captured["command"] = command
        captured["check"] = check
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(start_dashboard.subprocess, "run", _fake_run)

    code = start_dashboard.main(["--settings", "cfg.yaml", "--server-port", "9999"])

    assert code == 0
    command = captured["command"]
    assert isinstance(command, list)
    assert command[:4] == [start_dashboard.sys.executable, "-m", "streamlit", "run"]
    assert "--server.port" in command
    assert "9999" in command
    assert "--" in command
    assert command[-1] == "cfg.yaml"
    assert captured["check"] is False


@pytest.mark.unit
def test_start_dashboard_returns_1_when_subprocess_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    def _boom(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        raise RuntimeError("boom")

    monkeypatch.setattr(start_dashboard.subprocess, "run", _boom)

    code = start_dashboard.main([])

    assert code == 1
