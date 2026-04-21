"""Expose the ``src`` tree for direct local imports during early scaffolding."""

from pathlib import Path
import sys


SRC_PATH = Path(__file__).resolve().parent / "src"

if SRC_PATH.is_dir():
    src_str = str(SRC_PATH)
    if src_str not in sys.path:
        sys.path.insert(0, src_str)
