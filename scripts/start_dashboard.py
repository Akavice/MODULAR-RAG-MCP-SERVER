"""CLI helper to start Streamlit dashboard."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Start Modular RAG dashboard.")
    parser.add_argument(
        "--settings",
        default="config/settings.yaml",
        help="Settings file path (default: config/settings.yaml)",
    )
    parser.add_argument(
        "--server-port",
        default="8501",
        help="Streamlit server port (default: 8501)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Start Streamlit dashboard app process."""
    parser = _build_parser()
    args = parser.parse_args(argv)
    app_path = Path("src/observability/dashboard/app.py").resolve()

    command = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app_path),
        "--server.port",
        str(args.server_port),
        "--",
        args.settings,
    ]
    try:
        completed = subprocess.run(command, check=False)
    except Exception as exc:
        print(f"Failed to start dashboard: {exc}")
        return 1
    return int(completed.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
