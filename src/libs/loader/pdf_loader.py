"""PDF loader implementation."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Callable

from core.types import Document, make_image_placeholder
from libs.loader.base_loader import BaseLoader


TextExtractor = Callable[[Path, bytes], str]
ImageExtractor = Callable[[Path, bytes, str], list[dict[str, Any]]]


class PdfLoader(BaseLoader):
    """Load PDF files into canonical `Document` objects."""

    def __init__(
        self,
        *,
        text_extractor: TextExtractor | None = None,
        image_extractor: ImageExtractor | None = None,
    ) -> None:
        self._text_extractor = text_extractor or self._default_text_extractor
        self._image_extractor = image_extractor or self._default_image_extractor

    def load(self, path: str) -> Document:
        file_path = self.validate_file_path(path, expected_suffix=".pdf")
        raw_bytes = file_path.read_bytes()
        doc_hash = hashlib.sha256(raw_bytes).hexdigest()

        text = self._extract_text(file_path, raw_bytes)
        images, warnings = self._extract_images(file_path, raw_bytes, doc_hash)
        text, images = self._merge_image_placeholders(text=text, images=images)

        metadata: dict[str, Any] = {
            "source_path": str(file_path.resolve()),
            "file_name": file_path.name,
            "file_size": len(raw_bytes),
            "images": images,
        }
        if warnings:
            metadata["warnings"] = warnings

        return Document(id=doc_hash, text=text, metadata=metadata)

    def _extract_text(self, file_path: Path, raw_bytes: bytes) -> str:
        try:
            extracted = self._text_extractor(file_path, raw_bytes)
        except Exception:
            return ""
        if not isinstance(extracted, str):
            raise TypeError("text extractor must return a string")
        return extracted

    def _extract_images(
        self,
        file_path: Path,
        raw_bytes: bytes,
        doc_hash: str,
    ) -> tuple[list[dict[str, Any]], list[str]]:
        try:
            images = self._image_extractor(file_path, raw_bytes, doc_hash)
        except Exception as exc:
            return [], [f"image_extraction_failed: {exc}"]

        if not isinstance(images, list):
            return [], ["image_extraction_failed: extractor must return a list"]

        normalized: list[dict[str, Any]] = []
        warnings: list[str] = []
        for index, item in enumerate(images):
            if not isinstance(item, dict):
                warnings.append(f"image_item_dropped[{index}]: not a mapping")
                continue

            image_id = item.get("id")
            image_path = item.get("path")
            text_offset = item.get("text_offset")
            if not isinstance(image_id, str) or not image_id.strip():
                warnings.append(f"image_item_dropped[{index}]: invalid id")
                continue
            if not isinstance(image_path, str) or not image_path.strip():
                warnings.append(f"image_item_dropped[{index}]: invalid path")
                continue
            if text_offset is not None and (
                not isinstance(text_offset, int) or isinstance(text_offset, bool)
            ):
                warnings.append(f"image_item_dropped[{index}]: invalid text_offset")
                continue

            normalized.append(dict(item))
        return normalized, warnings

    @staticmethod
    def _merge_image_placeholders(
        *,
        text: str,
        images: list[dict[str, Any]],
    ) -> tuple[str, list[dict[str, Any]]]:
        if not text:
            text = ""

        # Apply replacements in reverse order to keep offsets stable.
        replace_items: list[tuple[int, int, int]] = []
        for index, image in enumerate(images):
            image_id = image.get("id")
            if not isinstance(image_id, str) or not image_id.strip():
                continue
            placeholder = make_image_placeholder(image_id)
            placeholder_length = len(placeholder)

            text_offset = image.get("text_offset")
            original_text_length = image.get(
                "text_length_original",
                image.get("text_length", placeholder_length),
            )
            if (
                isinstance(text_offset, int)
                and not isinstance(text_offset, bool)
                and text_offset >= 0
                and isinstance(original_text_length, int)
                and not isinstance(original_text_length, bool)
                and original_text_length >= 0
                and text_offset <= len(text)
                and text_offset + original_text_length <= len(text)
            ):
                replace_items.append((text_offset, original_text_length, index))
            else:
                if text:
                    text = f"{text}\n{placeholder}"
                else:
                    text = placeholder
                image["text_offset"] = max(0, len(text) - len(placeholder))
            image["text_length"] = placeholder_length

        for text_offset, original_length, index in sorted(
            replace_items,
            key=lambda item: item[0],
            reverse=True,
        ):
            placeholder = make_image_placeholder(str(images[index]["id"]))
            text = (
                text[:text_offset]
                + placeholder
                + text[text_offset + original_length :]
            )
            images[index]["text_offset"] = text_offset
            images[index]["text_length"] = len(placeholder)

        return text, images

    @staticmethod
    def _default_text_extractor(file_path: Path, raw_bytes: bytes) -> str:
        del raw_bytes
        try:
            from pypdf import PdfReader  # type: ignore
        except Exception:
            return ""

        try:
            reader = PdfReader(str(file_path))
            return "\n".join((page.extract_text() or "") for page in reader.pages).strip()
        except Exception:
            return ""

    @staticmethod
    def _default_image_extractor(
        file_path: Path,
        raw_bytes: bytes,
        doc_hash: str,
    ) -> list[dict[str, Any]]:
        del file_path
        del raw_bytes
        del doc_hash
        return []
