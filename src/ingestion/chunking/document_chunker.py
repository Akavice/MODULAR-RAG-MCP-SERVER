"""Document-to-chunk adapter built on top of pluggable splitter backends."""

from __future__ import annotations

import hashlib
import re
from typing import Any

from core.types import Chunk, Document
from libs.splitter.splitter_factory import SplitterFactory


_IMAGE_PLACEHOLDER_PATTERN = re.compile(r"\[IMAGE:\s*([^\]]+?)\]")


class DocumentChunker:
    """Adapt `Document` objects into typed `Chunk` objects."""

    def __init__(self, settings: Any) -> None:
        self.settings = settings
        self.splitter = SplitterFactory.create(settings)

    def split_document(self, document: Document) -> list[Chunk]:
        if not isinstance(document, Document):
            raise TypeError("document must be a Document")

        if not document.text.strip():
            return []

        raw_chunks = self.splitter.split(document.text)
        if not isinstance(raw_chunks, list):
            raise TypeError("splitter output must be a list")

        chunks: list[Chunk] = []
        search_cursor = 0

        for chunk_text in raw_chunks:
            if not isinstance(chunk_text, str) or not chunk_text.strip():
                continue
            chunk_index = len(chunks)

            start_offset, end_offset, search_cursor = self._compute_offsets(
                document_text=document.text,
                chunk_text=chunk_text,
                search_cursor=search_cursor,
            )
            metadata = self._inherit_metadata(
                document=document,
                chunk_index=chunk_index,
                chunk_text=chunk_text,
            )
            chunk = Chunk(
                id=self._generate_chunk_id(document.id, chunk_index, chunk_text),
                text=chunk_text,
                metadata=metadata,
                start_offset=start_offset,
                end_offset=end_offset,
                source_ref=document.id,
            )
            chunks.append(chunk)
        return chunks

    @staticmethod
    def _generate_chunk_id(doc_id: str, index: int, text: str) -> str:
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]
        return f"{doc_id}_{index:04d}_{digest}"

    @staticmethod
    def _inherit_metadata(
        document: Document,
        chunk_index: int,
        chunk_text: str,
    ) -> dict[str, Any]:
        metadata = dict(document.metadata)
        metadata["chunk_index"] = chunk_index

        image_catalog = document.metadata.get("images")
        image_by_id: dict[str, dict[str, Any]] = {}
        if isinstance(image_catalog, list):
            for item in image_catalog:
                if not isinstance(item, dict):
                    continue
                image_id = item.get("id")
                if isinstance(image_id, str) and image_id.strip():
                    image_by_id[image_id.strip()] = dict(item)

        refs = [
            match.group(1).strip()
            for match in _IMAGE_PLACEHOLDER_PATTERN.finditer(chunk_text)
            if match.group(1).strip()
        ]

        metadata.pop("images", None)
        metadata.pop("image_refs", None)
        if refs:
            metadata["image_refs"] = refs
            subset = [image_by_id[image_id] for image_id in refs if image_id in image_by_id]
            if subset:
                metadata["images"] = subset

        return metadata

    @staticmethod
    def _compute_offsets(
        *,
        document_text: str,
        chunk_text: str,
        search_cursor: int,
    ) -> tuple[int, int, int]:
        start = document_text.find(chunk_text, max(0, search_cursor))
        if start == -1:
            start = max(0, search_cursor)
        end = start + len(chunk_text)
        next_cursor = max(search_cursor, end)
        return start, end, next_cursor
