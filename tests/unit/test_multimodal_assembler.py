"""Unit tests for multimodal payload assembly."""

from __future__ import annotations

from pathlib import Path

import pytest

from core.response.multimodal_assembler import MultimodalAssembler
from core.types import RetrievalResult


@pytest.mark.unit
def test_assemble_appends_image_blocks_when_image_exists(tmp_path: Path) -> None:
    image_path = tmp_path / "img.png"
    image_path.write_bytes(b"\x89PNG\r\n\x1a\nfake")
    result = RetrievalResult(
        chunk_id="c1",
        score=0.9,
        text="with image",
        metadata={"source_path": "docs/a.pdf", "images": [{"id": "img1", "path": str(image_path)}]},
    )
    assembler = MultimodalAssembler()

    payload = assembler.assemble({"content": [{"type": "text", "text": "x"}]}, [result])

    assert len(payload["content"]) == 2
    assert payload["content"][1]["type"] == "image"
    assert payload["content"][1]["mimeType"] == "image/png"
    assert isinstance(payload["content"][1]["data"], str)


@pytest.mark.unit
def test_assemble_skips_missing_image_paths(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.png"
    result = RetrievalResult(
        chunk_id="c1",
        score=0.9,
        text="with missing image",
        metadata={"source_path": "docs/a.pdf", "images": [{"id": "img1", "path": str(missing_path)}]},
    )
    assembler = MultimodalAssembler()

    payload = assembler.assemble({"content": [{"type": "text", "text": "x"}]}, [result])

    assert len(payload["content"]) == 1
    assert payload["content"][0]["type"] == "text"


@pytest.mark.unit
def test_assemble_uses_octet_stream_for_unknown_suffix(tmp_path: Path) -> None:
    image_path = tmp_path / "img.bin"
    image_path.write_bytes(b"raw")
    result = RetrievalResult(
        chunk_id="c1",
        score=0.9,
        text="with unknown image type",
        metadata={"source_path": "docs/a.pdf", "images": [{"id": "img1", "path": str(image_path)}]},
    )
    assembler = MultimodalAssembler()

    payload = assembler.assemble({"content": [{"type": "text", "text": "x"}]}, [result])

    assert len(payload["content"]) == 2
    assert payload["content"][1]["type"] == "image"
    assert payload["content"][1]["mimeType"] == "application/octet-stream"
