"""Vector store upsert adapter with idempotent chunk-record handling."""

from __future__ import annotations

from typing import Any

from core.types import ChunkRecord
from libs.vector_store.base_vector_store import BaseVectorStore
from libs.vector_store.vector_store_factory import VectorStoreFactory


class VectorUpserter:
    """Upsert dense chunk vectors into the configured vector store."""

    def __init__(
        self,
        settings: Any,
        *,
        vector_store: BaseVectorStore | None = None,
    ) -> None:
        self.settings = settings
        self.vector_store = vector_store or VectorStoreFactory.create(settings)

    def upsert(self, records: list[ChunkRecord], trace: Any | None = None) -> int:
        """Upsert chunk records and return processed unique-record count."""
        self._validate_records(records)
        if not records:
            if trace is not None and hasattr(trace, "record_stage"):
                trace.record_stage(
                    "storage_vector_upserter",
                    input_count=0,
                    unique_count=0,
                    upserted_count=0,
                )
            return 0

        # Idempotency within one call: keep only last value for duplicate chunk ids.
        deduped_by_id: dict[str, ChunkRecord] = {}
        for record in records:
            deduped_by_id[self._stable_chunk_id(record)] = record

        payload: list[dict[str, Any]] = []
        for stable_id, record in deduped_by_id.items():
            dense_vector = record.dense_vector
            if dense_vector is None:
                raise ValueError(f"record '{record.id}' missing dense_vector")
            payload.append(
                {
                    "id": stable_id,
                    "vector": list(dense_vector),
                    "text": record.text,
                    "metadata": dict(record.metadata),
                }
            )

        upserted_count = self.vector_store.upsert(payload, trace=trace)
        if trace is not None and hasattr(trace, "record_stage"):
            trace.record_stage(
                "storage_vector_upserter",
                input_count=len(records),
                unique_count=len(payload),
                upserted_count=upserted_count,
                collection_name=getattr(self.vector_store, "collection_name", ""),
            )
        return upserted_count

    @staticmethod
    def _stable_chunk_id(record: ChunkRecord) -> str:
        # DenseEncoder already emits deterministic chunk ids; keep them unchanged.
        return record.id.strip()

    @staticmethod
    def _validate_records(records: list[ChunkRecord]) -> None:
        if not isinstance(records, list):
            raise TypeError("records must be a list")
        for index, record in enumerate(records):
            if not isinstance(record, ChunkRecord):
                raise TypeError(f"record at index {index} must be a ChunkRecord")
