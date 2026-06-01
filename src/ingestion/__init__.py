"""Ingestion pipeline package."""

from ingestion.document_manager import (
    CollectionStats,
    DeleteResult,
    DocumentDetail,
    DocumentInfo,
    DocumentManager,
)
from ingestion.pipeline import (
    IngestionPipeline,
    IngestionPipelineStageError,
    IngestionResult,
)

__all__ = [
    "IngestionPipeline",
    "IngestionResult",
    "IngestionPipelineStageError",
    "DocumentManager",
    "DocumentInfo",
    "DocumentDetail",
    "DeleteResult",
    "CollectionStats",
]
