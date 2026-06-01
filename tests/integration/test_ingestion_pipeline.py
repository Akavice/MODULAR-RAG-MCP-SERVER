"""Integration tests for ingestion pipeline orchestration."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import pytest

from core.trace.trace_context import TraceContext
from core.types import Chunk, ChunkRecord, Document
from ingestion.pipeline import IngestionPipeline, IngestionPipelineStageError
from ingestion.storage.image_storage import ImageStorage


class FakeIntegrityChecker:
    def __init__(self, *, should_skip: bool = False) -> None:
        self.should_skip_flag = should_skip
        self.success_calls: list[tuple[str, str, dict[str, Any]]] = []
        self.failed_calls: list[tuple[str, str, dict[str, Any]]] = []

    def compute_sha256(self, path: str) -> str:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()

    def should_skip(self, file_hash: str) -> bool:
        _ = file_hash
        return self.should_skip_flag

    def mark_success(self, file_hash: str, file_path: str, **extra: Any) -> None:
        self.success_calls.append((file_hash, file_path, dict(extra)))

    def mark_failed(self, file_hash: str, error_msg: str, **extra: Any) -> None:
        self.failed_calls.append((file_hash, error_msg, dict(extra)))


class FakeLoader:
    def __init__(self, image_path: Path, *, explode: bool = False) -> None:
        self.image_path = image_path
        self.explode = explode
        self.called = False

    def load(self, path: str) -> Document:
        self.called = True
        if self.explode:
            raise RuntimeError("loader exploded")
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


class FakeChunker:
    def split_document(self, document: Document) -> list[Chunk]:
        return [
            Chunk(
                id="chunk-1",
                text=document.text,
                metadata={
                    "source_path": document.metadata["source_path"],
                    "images": [dict(item) for item in document.metadata.get("images", [])],
                    "image_refs": ["img_1"],
                },
                start_offset=0,
                end_offset=len(document.text),
                source_ref=document.id,
            )
        ]


class PassThroughTransform:
    def __init__(self, marker_key: str) -> None:
        self.marker_key = marker_key

    def transform(self, chunks: list[Chunk], trace: Any | None = None) -> list[Chunk]:
        _ = trace
        output: list[Chunk] = []
        for chunk in chunks:
            metadata = dict(chunk.metadata)
            metadata[self.marker_key] = True
            output.append(
                Chunk(
                    id=chunk.id,
                    text=chunk.text,
                    metadata=metadata,
                    start_offset=chunk.start_offset,
                    end_offset=chunk.end_offset,
                    source_ref=chunk.source_ref,
                )
            )
        return output


class FakeBatchProcessor:
    def process(self, chunks: list[Chunk], trace: Any | None = None) -> list[ChunkRecord]:
        _ = trace
        return [
            ChunkRecord(
                id=chunk.id,
                text=chunk.text,
                metadata=dict(chunk.metadata),
                dense_vector=[1.0, 0.0, 0.0],
                sparse_vector={"alpha": 0.42},
            )
            for chunk in chunks
        ]


class FakeVectorUpserter:
    def __init__(self) -> None:
        self.last_records: list[ChunkRecord] = []

    def upsert(self, records: list[ChunkRecord], trace: Any | None = None) -> int:
        _ = trace
        self.last_records = records
        return len(records)


class FakeBM25Indexer:
    def __init__(self) -> None:
        self.last_records: list[ChunkRecord] = []

    def upsert(self, records: list[ChunkRecord], trace: Any | None = None) -> int:
        _ = trace
        self.last_records = records
        return len(records)


def _build_pipeline(
    *,
    tmp_path: Path,
    integrity_checker: FakeIntegrityChecker,
    loader: FakeLoader,
    vector_upserter: FakeVectorUpserter | None = None,
    bm25_indexer: FakeBM25Indexer | None = None,
) -> tuple[IngestionPipeline, ImageStorage, FakeVectorUpserter]:
    image_storage = ImageStorage(
        image_root=str(tmp_path / "images"),
        db_path=str(tmp_path / "db" / "image_index.db"),
    )
    vector = vector_upserter or FakeVectorUpserter()
    bm25 = bm25_indexer or FakeBM25Indexer()
    pipeline = IngestionPipeline(
        settings={},
        integrity_checker=integrity_checker,
        loader=loader,
        chunker=FakeChunker(),
        chunk_refiner=PassThroughTransform("refined"),
        metadata_enricher=PassThroughTransform("enriched"),
        image_captioner=PassThroughTransform("captioned"),
        batch_processor=FakeBatchProcessor(),
        vector_upserter=vector,
        bm25_indexer=bm25,
        image_storage=image_storage,
    )
    return pipeline, image_storage, vector


@pytest.mark.integration
def test_pipeline_run_ingests_end_to_end_and_updates_image_paths(tmp_path: Path) -> None:
    source_pdf = tmp_path / "doc.pdf"
    source_pdf.write_bytes(b"%PDF-1.4\nfake")
    source_image = tmp_path / "raw_image.png"
    source_image.write_bytes(b"\x89PNG\r\n\x1a\nimg")

    integrity = FakeIntegrityChecker(should_skip=False)
    loader = FakeLoader(source_image)
    pipeline, image_storage, vector_upserter = _build_pipeline(
        tmp_path=tmp_path,
        integrity_checker=integrity,
        loader=loader,
    )
    progress: list[tuple[str, int, int]] = []

    result = pipeline.run(
        str(source_pdf),
        collection="kb",
        on_progress=lambda stage, current, total: progress.append((stage, current, total)),
    )

    assert result.status == "ingested"
    assert result.chunk_count == 1
    assert result.record_count == 1
    assert result.image_saved_count == 1
    assert [item[0] for item in progress] == [
        "integrity",
        "load",
        "split",
        "transform",
        "encode",
        "store",
    ]
    assert [item[1] for item in progress] == [1, 2, 3, 4, 5, 6]
    assert all(item[2] == 6 for item in progress)

    saved_path = image_storage.get_path("img_1")
    assert isinstance(saved_path, str)
    assert Path(saved_path).exists()

    stored_image_path = vector_upserter.last_records[0].metadata["images"][0]["path"]
    assert stored_image_path == saved_path
    assert len(integrity.success_calls) == 1
    assert len(integrity.failed_calls) == 0


@pytest.mark.integration
def test_pipeline_run_skips_when_integrity_checker_reports_seen(tmp_path: Path) -> None:
    source_pdf = tmp_path / "doc.pdf"
    source_pdf.write_bytes(b"%PDF-1.4\nfake")
    source_image = tmp_path / "raw_image.png"
    source_image.write_bytes(b"\x89PNG\r\n\x1a\nimg")

    integrity = FakeIntegrityChecker(should_skip=True)
    loader = FakeLoader(source_image)
    pipeline, _, _ = _build_pipeline(
        tmp_path=tmp_path,
        integrity_checker=integrity,
        loader=loader,
    )
    progress: list[tuple[str, int, int]] = []

    result = pipeline.run(
        str(source_pdf),
        collection="kb",
        force=False,
        on_progress=lambda stage, current, total: progress.append((stage, current, total)),
    )

    assert result.status == "skipped"
    assert result.reason == "already_ingested"
    assert loader.called is False
    assert [item[0] for item in progress] == ["integrity"]
    assert len(integrity.success_calls) == 0
    assert len(integrity.failed_calls) == 0


@pytest.mark.integration
def test_pipeline_run_marks_failed_and_raises_stage_error(tmp_path: Path) -> None:
    source_pdf = tmp_path / "doc.pdf"
    source_pdf.write_bytes(b"%PDF-1.4\nfake")
    source_image = tmp_path / "raw_image.png"
    source_image.write_bytes(b"\x89PNG\r\n\x1a\nimg")

    integrity = FakeIntegrityChecker(should_skip=False)
    loader = FakeLoader(source_image, explode=True)
    pipeline, _, _ = _build_pipeline(
        tmp_path=tmp_path,
        integrity_checker=integrity,
        loader=loader,
    )

    with pytest.raises(IngestionPipelineStageError, match="ingestion stage 'load' failed"):
        pipeline.run(str(source_pdf), collection="kb")

    assert len(integrity.success_calls) == 0
    assert len(integrity.failed_calls) == 1
    assert "load" in integrity.failed_calls[0][1]


@pytest.mark.integration
def test_pipeline_run_force_true_bypasses_skip_check(tmp_path: Path) -> None:
    source_pdf = tmp_path / "doc.pdf"
    source_pdf.write_bytes(b"%PDF-1.4\nfake")
    source_image = tmp_path / "raw_image.png"
    source_image.write_bytes(b"\x89PNG\r\n\x1a\nimg")

    integrity = FakeIntegrityChecker(should_skip=True)
    loader = FakeLoader(source_image)
    pipeline, _, _ = _build_pipeline(
        tmp_path=tmp_path,
        integrity_checker=integrity,
        loader=loader,
    )

    result = pipeline.run(str(source_pdf), collection="kb", force=True)

    assert result.status == "ingested"
    assert loader.called is True
    assert len(integrity.success_calls) == 1
    assert len(integrity.failed_calls) == 0


@pytest.mark.integration
def test_pipeline_run_continues_when_document_image_file_missing(tmp_path: Path) -> None:
    source_pdf = tmp_path / "doc.pdf"
    source_pdf.write_bytes(b"%PDF-1.4\nfake")
    missing_image = tmp_path / "missing_image.png"  # intentionally not created

    integrity = FakeIntegrityChecker(should_skip=False)
    loader = FakeLoader(missing_image)
    pipeline, image_storage, vector_upserter = _build_pipeline(
        tmp_path=tmp_path,
        integrity_checker=integrity,
        loader=loader,
    )

    result = pipeline.run(str(source_pdf), collection="kb")

    assert result.status == "ingested"
    assert result.image_saved_count == 0
    assert image_storage.list_images() == []
    assert vector_upserter.last_records
    # path remains unresolved/original when image persistence is skipped
    assert "missing_image.png" in vector_upserter.last_records[0].metadata["images"][0]["path"]


@pytest.mark.integration
def test_pipeline_run_records_ingestion_trace_stages(tmp_path: Path) -> None:
    source_pdf = tmp_path / "doc.pdf"
    source_pdf.write_bytes(b"%PDF-1.4\nfake")
    source_image = tmp_path / "raw_image.png"
    source_image.write_bytes(b"\x89PNG\r\n\x1a\nimg")

    integrity = FakeIntegrityChecker(should_skip=False)
    loader = FakeLoader(source_image)
    pipeline, _, _ = _build_pipeline(
        tmp_path=tmp_path,
        integrity_checker=integrity,
        loader=loader,
    )
    trace = TraceContext(trace_type="ingestion")

    result = pipeline.run(str(source_pdf), collection="kb", trace=trace)

    assert result.status == "ingested"
    stages = [entry["stage"] for entry in trace.stages]
    for expected in ("load", "split", "transform", "embed", "upsert"):
        assert expected in stages
    payload = trace.to_dict()
    assert payload["trace_type"] == "ingestion"
    assert payload["trace_id"] == trace.trace_id


@pytest.mark.integration
def test_pipeline_run_records_ingestion_trace_stage_payloads(tmp_path: Path) -> None:
    source_pdf = tmp_path / "doc.pdf"
    source_pdf.write_bytes(b"%PDF-1.4\nfake")
    source_image = tmp_path / "raw_image.png"
    source_image.write_bytes(b"\x89PNG\r\n\x1a\nimg")

    integrity = FakeIntegrityChecker(should_skip=False)
    loader = FakeLoader(source_image)
    pipeline, _, _ = _build_pipeline(
        tmp_path=tmp_path,
        integrity_checker=integrity,
        loader=loader,
    )
    trace = TraceContext(trace_type="ingestion")

    result = pipeline.run(str(source_pdf), collection="kb", trace=trace)

    assert result.status == "ingested"
    by_stage = {entry["stage"]: entry for entry in trace.stages}
    for stage in ("load", "split", "transform", "embed", "upsert"):
        assert stage in by_stage
        assert by_stage[stage]["source_path"] == str(source_pdf.resolve())
        assert by_stage[stage]["collection"] == "kb"
        assert by_stage[stage]["document_id"] == "doc-1"

    assert by_stage["split"]["chunk_count"] == 1
    assert by_stage["transform"]["chunk_count"] == 1
    assert by_stage["embed"]["record_count"] == 1
    assert by_stage["upsert"]["vector_upserted"] == 1
    assert by_stage["upsert"]["bm25_upserted"] == 1
    assert by_stage["upsert"]["image_saved_count"] == 1
