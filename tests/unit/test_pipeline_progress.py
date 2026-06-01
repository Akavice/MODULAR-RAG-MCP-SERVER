"""Unit tests for ingestion pipeline progress callback contract (F5)."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import pytest

from core.types import Chunk, ChunkRecord, Document
from ingestion.pipeline import IngestionPipeline
from ingestion.storage.image_storage import ImageStorage


class _Integrity:
    def __init__(self, *, should_skip: bool = False) -> None:
        self.should_skip_flag = should_skip

    def compute_sha256(self, path: str) -> str:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()

    def should_skip(self, file_hash: str) -> bool:
        _ = file_hash
        return self.should_skip_flag

    def mark_success(self, file_hash: str, file_path: str, **extra: Any) -> None:
        _ = (file_hash, file_path, extra)

    def mark_failed(self, file_hash: str, error_msg: str, **extra: Any) -> None:
        _ = (file_hash, error_msg, extra)


class _Loader:
    def __init__(self, image_path: Path) -> None:
        self.image_path = image_path

    def load(self, path: str) -> Document:
        return Document(
            id="doc-1",
            text="alpha [IMAGE: img_1] omega",
            metadata={
                "source_path": str(Path(path).resolve()),
                "images": [
                    {
                        "id": "img_1",
                        "path": str(self.image_path.resolve()),
                        "page": 0,
                        "text_offset": 6,
                        "text_length": 14,
                    }
                ],
            },
        )


class _Chunker:
    def split_document(self, document: Document) -> list[Chunk]:
        return [
            Chunk(
                id="chunk-1",
                text=document.text,
                metadata={
                    "source_path": document.metadata["source_path"],
                    "images": [dict(item) for item in document.metadata.get("images", [])],
                },
                start_offset=0,
                end_offset=len(document.text),
                source_ref=document.id,
            )
        ]


class _PassThrough:
    def transform(self, chunks: list[Chunk], trace: Any | None = None) -> list[Chunk]:
        _ = trace
        return list(chunks)


class _Batch:
    def process(self, chunks: list[Chunk], trace: Any | None = None) -> list[ChunkRecord]:
        _ = trace
        return [
            ChunkRecord(
                id=chunk.id,
                text=chunk.text,
                metadata=dict(chunk.metadata),
                dense_vector=[1.0, 0.0, 0.0],
                sparse_vector={"alpha": 1.0},
            )
            for chunk in chunks
        ]


class _Vector:
    def upsert(self, records: list[ChunkRecord], trace: Any | None = None) -> int:
        _ = trace
        return len(records)


class _Bm25:
    def upsert(self, records: list[ChunkRecord], trace: Any | None = None) -> int:
        _ = trace
        return len(records)


def _build_pipeline(tmp_path: Path, *, should_skip: bool) -> IngestionPipeline:
    image_storage = ImageStorage(
        image_root=str(tmp_path / "images"),
        db_path=str(tmp_path / "db" / "image_index.db"),
    )
    return IngestionPipeline(
        settings={},
        integrity_checker=_Integrity(should_skip=should_skip),  # type: ignore[arg-type]
        loader=_Loader(tmp_path / "raw_image.png"),  # type: ignore[arg-type]
        chunker=_Chunker(),  # type: ignore[arg-type]
        chunk_refiner=_PassThrough(),  # type: ignore[arg-type]
        metadata_enricher=_PassThrough(),  # type: ignore[arg-type]
        image_captioner=_PassThrough(),  # type: ignore[arg-type]
        batch_processor=_Batch(),  # type: ignore[arg-type]
        vector_upserter=_Vector(),  # type: ignore[arg-type]
        bm25_indexer=_Bm25(),  # type: ignore[arg-type]
        image_storage=image_storage,
    )


@pytest.mark.unit
def test_pipeline_progress_callback_reports_all_stages_in_order(tmp_path: Path) -> None:
    source_pdf = tmp_path / "doc.pdf"
    source_pdf.write_bytes(b"%PDF-1.4\nfake")
    source_image = tmp_path / "raw_image.png"
    source_image.write_bytes(b"\x89PNG\r\n\x1a\nimg")
    pipeline = _build_pipeline(tmp_path, should_skip=False)
    events: list[tuple[str, int, int]] = []

    result = pipeline.run(
        str(source_pdf),
        collection="kb",
        on_progress=lambda stage, current, total: events.append((stage, current, total)),
    )

    assert result.status == "ingested"
    assert [stage for stage, _, _ in events] == [
        "integrity",
        "load",
        "split",
        "transform",
        "encode",
        "store",
    ]
    assert [current for _, current, _ in events] == [1, 2, 3, 4, 5, 6]
    assert all(total == 6 for _, _, total in events)


@pytest.mark.unit
def test_pipeline_progress_callback_reports_only_integrity_when_skipped(tmp_path: Path) -> None:
    source_pdf = tmp_path / "doc.pdf"
    source_pdf.write_bytes(b"%PDF-1.4\nfake")
    source_image = tmp_path / "raw_image.png"
    source_image.write_bytes(b"\x89PNG\r\n\x1a\nimg")
    pipeline = _build_pipeline(tmp_path, should_skip=True)
    events: list[tuple[str, int, int]] = []

    result = pipeline.run(
        str(source_pdf),
        collection="kb",
        force=False,
        on_progress=lambda stage, current, total: events.append((stage, current, total)),
    )

    assert result.status == "skipped"
    assert events == [("integrity", 1, 6)]


@pytest.mark.unit
def test_pipeline_rejects_non_callable_progress_callback(tmp_path: Path) -> None:
    source_pdf = tmp_path / "doc.pdf"
    source_pdf.write_bytes(b"%PDF-1.4\nfake")
    source_image = tmp_path / "raw_image.png"
    source_image.write_bytes(b"\x89PNG\r\n\x1a\nimg")
    pipeline = _build_pipeline(tmp_path, should_skip=False)

    with pytest.raises(TypeError, match="on_progress must be callable"):
        pipeline.run(str(source_pdf), on_progress="bad")  # type: ignore[arg-type]


@pytest.mark.unit
def test_pipeline_progress_force_true_does_not_short_circuit(tmp_path: Path) -> None:
    source_pdf = tmp_path / "doc.pdf"
    source_pdf.write_bytes(b"%PDF-1.4\nfake")
    source_image = tmp_path / "raw_image.png"
    source_image.write_bytes(b"\x89PNG\r\n\x1a\nimg")
    pipeline = _build_pipeline(tmp_path, should_skip=True)
    events: list[tuple[str, int, int]] = []

    result = pipeline.run(
        str(source_pdf),
        force=True,
        on_progress=lambda stage, current, total: events.append((stage, current, total)),
    )

    assert result.status == "ingested"
    assert [stage for stage, _, _ in events] == [
        "integrity",
        "load",
        "split",
        "transform",
        "encode",
        "store",
    ]
