"""Ingestion pipeline orchestration for PDF -> chunk -> embed -> store."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from core.trace.trace_context import TraceContext
from core.types import ChunkRecord, Document
from ingestion.chunking.document_chunker import DocumentChunker
from ingestion.embedding.batch_processor import BatchProcessor
from ingestion.storage.bm25_indexer import BM25Indexer
from ingestion.storage.image_storage import ImageStorage
from ingestion.storage.vector_upserter import VectorUpserter
from ingestion.transform.chunk_refiner import ChunkRefiner
from ingestion.transform.image_captioner import ImageCaptioner
from ingestion.transform.metadata_enricher import MetadataEnricher
from libs.loader.file_integrity import FileIntegrityChecker, SQLiteIntegrityChecker
from libs.loader.pdf_loader import PdfLoader


ProgressCallback = Callable[[str, int, int], None]


class IngestionPipelineStageError(RuntimeError):
    """Raised when one pipeline stage fails."""

    def __init__(self, stage: str, cause: Exception) -> None:
        self.stage = stage
        self.cause = cause
        super().__init__(f"ingestion stage '{stage}' failed: {cause}")


@dataclass(slots=True)
class IngestionResult:
    """Result payload for one ingestion run."""

    status: str
    source_path: str
    collection: str
    file_hash: str
    document_id: str | None
    chunk_count: int
    record_count: int
    vector_upserted: int
    bm25_upserted: int
    image_saved_count: int
    trace_id: str | None = None
    reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "source_path": self.source_path,
            "collection": self.collection,
            "file_hash": self.file_hash,
            "document_id": self.document_id,
            "chunk_count": self.chunk_count,
            "record_count": self.record_count,
            "vector_upserted": self.vector_upserted,
            "bm25_upserted": self.bm25_upserted,
            "image_saved_count": self.image_saved_count,
            "trace_id": self.trace_id,
            "reason": self.reason,
        }


class IngestionPipeline:
    """Serial ingestion orchestration with explicit stage boundaries."""

    _STAGES: tuple[str, ...] = (
        "integrity",
        "load",
        "split",
        "transform",
        "encode",
        "store",
    )

    def __init__(
        self,
        settings: Any,
        *,
        integrity_checker: FileIntegrityChecker | None = None,
        loader: PdfLoader | None = None,
        chunker: DocumentChunker | None = None,
        chunk_refiner: ChunkRefiner | None = None,
        metadata_enricher: MetadataEnricher | None = None,
        image_captioner: ImageCaptioner | None = None,
        batch_processor: BatchProcessor | None = None,
        vector_upserter: VectorUpserter | None = None,
        bm25_indexer: BM25Indexer | None = None,
        image_storage: ImageStorage | None = None,
    ) -> None:
        self.settings = settings
        self.integrity_checker = integrity_checker or SQLiteIntegrityChecker(
            db_path=self._resolve_integrity_db_path(settings)
        )
        self.loader = loader or PdfLoader()
        self.chunker = chunker or DocumentChunker(settings)
        self.chunk_refiner = chunk_refiner or ChunkRefiner(settings)
        self.metadata_enricher = metadata_enricher or MetadataEnricher(settings)
        self.image_captioner = image_captioner or ImageCaptioner(settings)
        self.batch_processor = batch_processor or BatchProcessor(settings)
        self.vector_upserter = vector_upserter or VectorUpserter(settings)
        self.bm25_indexer = bm25_indexer or BM25Indexer(settings)
        self.image_storage = image_storage or ImageStorage(
            image_root=self._resolve_image_root(settings),
            db_path=self._resolve_image_db_path(settings),
        )

    def run(
        self,
        source_path: str,
        *,
        collection: str = "default",
        force: bool = False,
        on_progress: ProgressCallback | None = None,
        trace: TraceContext | None = None,
    ) -> IngestionResult:
        norm_source_path = self._normalize_source_path(source_path)
        norm_collection = self._normalize_collection(collection)
        if not isinstance(force, bool):
            raise TypeError("force must be a boolean")

        trace_ctx = trace or TraceContext(trace_type="ingestion")
        stage_total = len(self._STAGES)

        file_hash = self._run_stage(
            "integrity",
            lambda: self.integrity_checker.compute_sha256(norm_source_path),
        )
        self._notify_progress(on_progress, "integrity", 1, stage_total)

        should_skip = False
        if not force:
            should_skip = self._run_stage(
                "integrity",
                lambda: bool(self.integrity_checker.should_skip(file_hash)),
            )
        if should_skip:
            return IngestionResult(
                status="skipped",
                source_path=norm_source_path,
                collection=norm_collection,
                file_hash=file_hash,
                document_id=None,
                chunk_count=0,
                record_count=0,
                vector_upserted=0,
                bm25_upserted=0,
                image_saved_count=0,
                trace_id=trace_ctx.trace_id,
                reason="already_ingested",
            )

        try:
            document = self._run_stage("load", lambda: self.loader.load(norm_source_path))
            self._notify_progress(on_progress, "load", 2, stage_total)

            chunks = self._run_stage("split", lambda: self.chunker.split_document(document))
            self._notify_progress(on_progress, "split", 3, stage_total)

            transformed_chunks = self._run_stage(
                "transform",
                lambda: self._transform_chunks(chunks, trace=trace_ctx),
            )
            self._notify_progress(on_progress, "transform", 4, stage_total)

            records = self._run_stage(
                "encode",
                lambda: self.batch_processor.process(transformed_chunks, trace=trace_ctx),
            )
            self._notify_progress(on_progress, "encode", 5, stage_total)

            vector_upserted, bm25_upserted, image_saved_count = self._run_stage(
                "store",
                lambda: self._store_outputs(
                    document=document,
                    records=records,
                    collection=norm_collection,
                    doc_hash=file_hash,
                    trace=trace_ctx,
                ),
            )
            self._notify_progress(on_progress, "store", 6, stage_total)

            self.integrity_checker.mark_success(
                file_hash,
                norm_source_path,
                collection=norm_collection,
                chunk_count=len(transformed_chunks),
                record_count=len(records),
                image_saved_count=image_saved_count,
            )
        except Exception as exc:
            try:
                self.integrity_checker.mark_failed(
                    file_hash,
                    str(exc),
                    collection=norm_collection,
                    source_path=norm_source_path,
                )
            except Exception:
                pass
            raise

        return IngestionResult(
            status="ingested",
            source_path=norm_source_path,
            collection=norm_collection,
            file_hash=file_hash,
            document_id=document.id,
            chunk_count=len(transformed_chunks),
            record_count=len(records),
            vector_upserted=vector_upserted,
            bm25_upserted=bm25_upserted,
            image_saved_count=image_saved_count,
            trace_id=trace_ctx.trace_id,
            reason=None,
        )

    def _transform_chunks(self, chunks: list[Any], *, trace: TraceContext | None) -> list[Any]:
        refined = self.chunk_refiner.transform(chunks, trace=trace)
        enriched = self.metadata_enricher.transform(refined, trace=trace)
        return self.image_captioner.transform(enriched, trace=trace)

    def _store_outputs(
        self,
        *,
        document: Document,
        records: list[ChunkRecord],
        collection: str,
        doc_hash: str,
        trace: TraceContext | None,
    ) -> tuple[int, int, int]:
        image_saved_count = self._persist_images_and_patch_metadata(
            document=document,
            records=records,
            collection=collection,
            doc_hash=doc_hash,
        )
        vector_upserted = self.vector_upserter.upsert(records, trace=trace)
        bm25_upserted = self.bm25_indexer.upsert(records, trace=trace)
        return vector_upserted, bm25_upserted, image_saved_count

    def _persist_images_and_patch_metadata(
        self,
        *,
        document: Document,
        records: list[ChunkRecord],
        collection: str,
        doc_hash: str,
    ) -> int:
        images = document.metadata.get("images")
        if not isinstance(images, list) or not images:
            return 0

        saved_paths: dict[str, str] = {}
        saved_count = 0

        for item in images:
            if not isinstance(item, dict):
                continue
            image_id = item.get("id")
            image_path = item.get("path")
            if not isinstance(image_id, str) or not image_id.strip():
                continue
            if not isinstance(image_path, str) or not image_path.strip():
                continue

            source_path = Path(image_path.strip())
            if not source_path.exists() or not source_path.is_file():
                continue

            suffix = source_path.suffix or ".png"
            page_num = item.get("page")
            if isinstance(page_num, bool) or (page_num is not None and not isinstance(page_num, int)):
                page_num = None

            saved_path = self.image_storage.save_image(
                image_id=image_id.strip(),
                content=source_path.read_bytes(),
                collection=collection,
                doc_hash=doc_hash,
                page_num=page_num,
                suffix=suffix,
            )
            saved_paths[image_id.strip()] = saved_path
            item["path"] = saved_path
            saved_count += 1

        if not saved_paths:
            return 0

        for record in records:
            record_images = record.metadata.get("images")
            if not isinstance(record_images, list):
                continue
            for image_item in record_images:
                if not isinstance(image_item, dict):
                    continue
                image_id = image_item.get("id")
                if not isinstance(image_id, str):
                    continue
                saved_path = saved_paths.get(image_id.strip())
                if saved_path:
                    image_item["path"] = saved_path
        return saved_count

    @staticmethod
    def _normalize_source_path(source_path: str) -> str:
        if not isinstance(source_path, str):
            raise TypeError("source_path must be a string")
        normalized = source_path.strip()
        if not normalized:
            raise ValueError("source_path must not be empty")
        return str(Path(normalized).resolve())

    @staticmethod
    def _normalize_collection(collection: str) -> str:
        if not isinstance(collection, str):
            raise TypeError("collection must be a string")
        normalized = collection.strip()
        if not normalized:
            raise ValueError("collection must not be empty")
        return normalized

    @staticmethod
    def _notify_progress(
        callback: ProgressCallback | None,
        stage_name: str,
        current: int,
        total: int,
    ) -> None:
        if callback is None:
            return
        callback(stage_name, current, total)

    @staticmethod
    def _run_stage(stage: str, fn: Callable[[], Any]) -> Any:
        try:
            return fn()
        except IngestionPipelineStageError:
            raise
        except Exception as exc:
            raise IngestionPipelineStageError(stage, exc) from exc

    @staticmethod
    def _resolve_ingestion_section(settings: Any) -> dict[str, Any]:
        if isinstance(settings, dict):
            section = settings.get("ingestion")
        else:
            section = getattr(settings, "ingestion", None)
        if isinstance(section, dict):
            return dict(section)
        return {}

    @staticmethod
    def _resolve_integrity_db_path(settings: Any) -> str | None:
        section = IngestionPipeline._resolve_ingestion_section(settings).get("integrity_checker")
        if isinstance(section, dict):
            value = section.get("db_path")
            if isinstance(value, str) and value.strip():
                return value.strip()
        return None

    @staticmethod
    def _resolve_image_root(settings: Any) -> str | None:
        section = IngestionPipeline._resolve_ingestion_section(settings).get("image_storage")
        if isinstance(section, dict):
            value = section.get("image_root")
            if isinstance(value, str) and value.strip():
                return value.strip()
        return None

    @staticmethod
    def _resolve_image_db_path(settings: Any) -> str | None:
        section = IngestionPipeline._resolve_ingestion_section(settings).get("image_storage")
        if isinstance(section, dict):
            value = section.get("db_path")
            if isinstance(value, str) and value.strip():
                return value.strip()
        return None
