"""Additional contract tests for PdfLoader edge cases."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from libs.loader.pdf_loader import PdfLoader


def _write_fake_pdf(path: Path) -> None:
    path.write_bytes(b"%PDF-1.4\n%fake\n1 0 obj\n<<>>\nendobj\n")


@pytest.mark.unit
def test_pdf_loader_rejects_non_string_path() -> None:
    loader = PdfLoader(text_extractor=lambda file_path, raw: "ok")

    with pytest.raises(TypeError, match="path must be a string"):
        loader.load(123)  # type: ignore[arg-type]


@pytest.mark.unit
def test_pdf_loader_rejects_empty_string_path() -> None:
    loader = PdfLoader(text_extractor=lambda file_path, raw: "ok")

    with pytest.raises(ValueError, match="path must not be empty"):
        loader.load("   ")


@pytest.mark.unit
def test_pdf_loader_rejects_non_string_text_extractor_output(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.pdf"
    _write_fake_pdf(file_path)
    loader = PdfLoader(text_extractor=lambda file_path, raw: None)  # type: ignore[return-value]

    with pytest.raises(TypeError, match="text extractor"):
        loader.load(str(file_path))


@pytest.mark.unit
def test_pdf_loader_ignores_invalid_image_items_without_crashing(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.pdf"
    _write_fake_pdf(file_path)

    def image_extractor(file_path: Path, raw: bytes, doc_hash: str) -> list[dict[str, Any]]:
        _ = file_path
        _ = raw
        _ = doc_hash
        return [
            "not-a-dict",  # invalid
            {"id": "img_valid", "path": "x.png", "text_offset": 1},  # valid
            {"id": "", "path": "x.png", "text_offset": 2},  # invalid id
            {"id": "img_bad_offset", "path": "x.png", "text_offset": "2"},  # invalid offset
        ]  # type: ignore[list-item]

    loader = PdfLoader(
        text_extractor=lambda file_path, raw: "abcd",
        image_extractor=image_extractor,
    )

    document = loader.load(str(file_path))

    assert "[IMAGE: img_valid]" in document.text
    assert len(document.metadata["images"]) == 1
    assert document.metadata["images"][0]["id"] == "img_valid"


@pytest.mark.unit
def test_pdf_loader_appends_placeholder_when_offset_is_invalid(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.pdf"
    _write_fake_pdf(file_path)

    def image_extractor(file_path: Path, raw: bytes, doc_hash: str) -> list[dict[str, Any]]:
        _ = file_path
        _ = raw
        _ = doc_hash
        return [{"id": "img1", "path": "x.png", "text_offset": -3}]

    loader = PdfLoader(
        text_extractor=lambda file_path, raw: "abcdef",
        image_extractor=image_extractor,
    )

    document = loader.load(str(file_path))

    assert document.text == "abcdef\n[IMAGE: img1]"


@pytest.mark.unit
def test_pdf_loader_handles_non_list_image_extractor_output(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.pdf"
    _write_fake_pdf(file_path)

    loader = PdfLoader(
        text_extractor=lambda file_path, raw: "plain",
        image_extractor=lambda file_path, raw, doc_hash: "bad"  # type: ignore[return-value]
    )

    document = loader.load(str(file_path))

    assert document.metadata["images"] == []
    assert "warnings" in document.metadata
    assert "extractor must return a list" in "\n".join(document.metadata["warnings"])


@pytest.mark.unit
def test_pdf_loader_records_warning_for_dropped_invalid_image_items(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.pdf"
    _write_fake_pdf(file_path)

    def image_extractor(file_path: Path, raw: bytes, doc_hash: str) -> list[dict[str, Any]]:
        _ = file_path
        _ = raw
        _ = doc_hash
        return [
            {"id": "", "path": "x.png"},
            {"id": "x", "path": ""},
            {"id": "x2", "path": "x2.png", "text_offset": "abc"},
        ]

    loader = PdfLoader(
        text_extractor=lambda file_path, raw: "plain",
        image_extractor=image_extractor,
    )
    document = loader.load(str(file_path))

    assert document.metadata["images"] == []
    warnings = "\n".join(document.metadata.get("warnings", []))
    assert "invalid id" in warnings
    assert "invalid path" in warnings
    assert "invalid text_offset" in warnings


@pytest.mark.unit
def test_pdf_loader_replaces_multiple_images_by_descending_offsets(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.pdf"
    _write_fake_pdf(file_path)

    def image_extractor(file_path: Path, raw: bytes, doc_hash: str) -> list[dict[str, Any]]:
        _ = file_path
        _ = raw
        _ = doc_hash
        return [
            {"id": "img_b", "path": "b.png", "text_offset": 4, "text_length_original": 4},
            {"id": "img_a", "path": "a.png", "text_offset": 0, "text_length_original": 4},
        ]

    loader = PdfLoader(
        text_extractor=lambda file_path, raw: "AAAABBBB",
        image_extractor=image_extractor,
    )
    document = loader.load(str(file_path))

    assert document.text == "[IMAGE: img_a][IMAGE: img_b]"


@pytest.mark.unit
def test_pdf_loader_appends_when_original_text_length_is_invalid(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.pdf"
    _write_fake_pdf(file_path)

    def image_extractor(file_path: Path, raw: bytes, doc_hash: str) -> list[dict[str, Any]]:
        _ = file_path
        _ = raw
        _ = doc_hash
        return [{"id": "img1", "path": "x.png", "text_offset": 1, "text_length_original": -2}]

    loader = PdfLoader(
        text_extractor=lambda file_path, raw: "abc",
        image_extractor=image_extractor,
    )
    document = loader.load(str(file_path))

    assert document.text.endswith("[IMAGE: img1]")
