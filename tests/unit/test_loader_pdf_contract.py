"""Contract tests for BaseLoader/PdfLoader."""

from __future__ import annotations

from pathlib import Path

import pytest

from libs.loader.pdf_loader import PdfLoader


def _write_fake_pdf(path: Path) -> None:
    # Minimal bytes with PDF signature for loader contract tests.
    path.write_bytes(b"%PDF-1.4\n%fake\n1 0 obj\n<<>>\nendobj\n")


@pytest.mark.unit
def test_pdf_loader_load_returns_document_with_source_path(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.pdf"
    _write_fake_pdf(file_path)
    loader = PdfLoader(text_extractor=lambda file_path, raw: "hello from pdf")

    document = loader.load(str(file_path))

    assert document.id
    assert document.text == "hello from pdf"
    assert document.metadata["source_path"] == str(file_path.resolve())
    assert document.metadata["images"] == []


@pytest.mark.unit
def test_pdf_loader_rejects_non_pdf_extension(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.txt"
    file_path.write_text("hello", encoding="utf-8")
    loader = PdfLoader()

    with pytest.raises(ValueError, match=r"\.pdf"):
        loader.load(str(file_path))


@pytest.mark.unit
def test_pdf_loader_raises_for_missing_file(tmp_path: Path) -> None:
    loader = PdfLoader()

    with pytest.raises(FileNotFoundError):
        loader.load(str(tmp_path / "missing.pdf"))


@pytest.mark.unit
def test_pdf_loader_inserts_image_placeholders_by_offset(tmp_path: Path) -> None:
    file_path = tmp_path / "with_images.pdf"
    _write_fake_pdf(file_path)

    def image_extractor(file_path: Path, raw: bytes, doc_hash: str) -> list[dict[str, object]]:
        _ = file_path
        _ = raw
        _ = doc_hash
        return [
            {
                "id": "img_1",
                "path": "data/images/test/img_1.png",
                "page": 1,
                "text_offset": 3,
                "text_length_original": 4,
                "position": {"x": 1, "y": 2},
            }
        ]

    loader = PdfLoader(
        text_extractor=lambda file_path, raw: "abcXXXXdef",
        image_extractor=image_extractor,
    )
    document = loader.load(str(file_path))

    assert document.text == "abc[IMAGE: img_1]def"
    assert len(document.metadata["images"]) == 1
    assert document.metadata["images"][0]["text_offset"] == 3


@pytest.mark.unit
def test_pdf_loader_does_not_block_when_image_extraction_fails(tmp_path: Path) -> None:
    file_path = tmp_path / "broken_image_extract.pdf"
    _write_fake_pdf(file_path)

    def broken_image_extractor(file_path: Path, raw: bytes, doc_hash: str) -> list[dict[str, object]]:
        _ = file_path
        _ = raw
        _ = doc_hash
        raise RuntimeError("image parser crashed")

    loader = PdfLoader(
        text_extractor=lambda file_path, raw: "plain text",
        image_extractor=broken_image_extractor,
    )
    document = loader.load(str(file_path))

    assert document.text == "plain text"
    assert document.metadata["images"] == []
    assert "warnings" in document.metadata
