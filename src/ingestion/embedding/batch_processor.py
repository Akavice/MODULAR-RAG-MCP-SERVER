"""Batch orchestration for dense/sparse ingestion encoders."""

from __future__ import annotations

from math import ceil
from time import perf_counter
from typing import Any

from core.types import Chunk, ChunkRecord
from ingestion.embedding.dense_encoder import DenseEncoder
from ingestion.embedding.sparse_encoder import SparseEncoder


class BatchProcessor:
    """Split chunks into batches and orchestrate dense/sparse encoding."""

    def __init__(
        self,
        settings: Any,
        *,
        dense_encoder: DenseEncoder | None = None,
        sparse_encoder: SparseEncoder | None = None,
        batch_size: int | None = None,
    ) -> None:
        self.settings = settings
        section = self._extract_batch_settings(settings)
        self.enable_dense = self._to_bool(section.get("enable_dense", True))
        self.enable_sparse = self._to_bool(section.get("enable_sparse", True))
        self.batch_size = (
            self._normalize_batch_size(batch_size)
            if batch_size is not None
            else self._normalize_batch_size(section.get("batch_size", 32))
        )

        self.dense_encoder = (
            dense_encoder if dense_encoder is not None else (DenseEncoder(settings) if self.enable_dense else None)
        )
        self.sparse_encoder = (
            sparse_encoder
            if sparse_encoder is not None
            else (SparseEncoder(settings) if self.enable_sparse else None)
        )

    def process(self, chunks: list[Chunk], trace: Any | None = None) -> list[ChunkRecord]:
        self._validate_chunks(chunks)
        if not self.enable_dense and not self.enable_sparse:
            raise ValueError("at least one of dense/sparse encoding must be enabled")

        if not chunks:
            if trace is not None and hasattr(trace, "record_stage"):
                trace.record_stage(
                    "embed_batch_processor",
                    chunk_count=0,
                    batch_count=0,
                    batch_size=self.batch_size,
                    dense_enabled=self.enable_dense,
                    sparse_enabled=self.enable_sparse,
                    total_elapsed_ms=0,
                )
            return []

        merged_records: list[ChunkRecord] = []
        total_elapsed_ms = 0

        for batch_index, start in enumerate(range(0, len(chunks), self.batch_size)):
            batch = chunks[start : start + self.batch_size]
            batch_start = perf_counter()

            if self.enable_dense and self.dense_encoder is None:
                raise RuntimeError("dense encoder is not initialized")
            if self.enable_sparse and self.sparse_encoder is None:
                raise RuntimeError("sparse encoder is not initialized")

            dense_records = (
                self.dense_encoder.encode(batch, trace=trace)
                if self.enable_dense and self.dense_encoder is not None
                else None
            )
            sparse_records = (
                self.sparse_encoder.encode(batch, trace=trace)
                if self.enable_sparse and self.sparse_encoder is not None
                else None
            )
            merged_batch = self._merge_batch(batch, dense_records=dense_records, sparse_records=sparse_records)
            merged_records.extend(merged_batch)

            elapsed_ms = int((perf_counter() - batch_start) * 1000)
            total_elapsed_ms += elapsed_ms
            if trace is not None and hasattr(trace, "record_stage"):
                trace.record_stage(
                    "embed_batch_processor_batch",
                    batch_index=batch_index,
                    batch_size=len(batch),
                    elapsed_ms=elapsed_ms,
                    dense_enabled=self.enable_dense,
                    sparse_enabled=self.enable_sparse,
                )

        if trace is not None and hasattr(trace, "record_stage"):
            trace.record_stage(
                "embed_batch_processor",
                chunk_count=len(chunks),
                batch_count=ceil(len(chunks) / self.batch_size),
                batch_size=self.batch_size,
                dense_enabled=self.enable_dense,
                sparse_enabled=self.enable_sparse,
                total_elapsed_ms=total_elapsed_ms,
            )

        return merged_records

    @staticmethod
    def _merge_batch(
        batch: list[Chunk],
        *,
        dense_records: list[ChunkRecord] | None,
        sparse_records: list[ChunkRecord] | None,
    ) -> list[ChunkRecord]:
        if dense_records is not None and len(dense_records) != len(batch):
            raise ValueError("dense encoder output size must match batch size")
        if sparse_records is not None and len(sparse_records) != len(batch):
            raise ValueError("sparse encoder output size must match batch size")

        merged: list[ChunkRecord] = []
        for index, chunk in enumerate(batch):
            dense = dense_records[index] if dense_records is not None else None
            sparse = sparse_records[index] if sparse_records is not None else None

            if dense is not None and dense.id != chunk.id:
                raise ValueError("dense encoder output id mismatch")
            if sparse is not None and sparse.id != chunk.id:
                raise ValueError("sparse encoder output id mismatch")

            merged.append(
                ChunkRecord(
                    id=chunk.id,
                    text=chunk.text,
                    metadata=dict(chunk.metadata),
                    dense_vector=(list(dense.dense_vector) if dense and dense.dense_vector is not None else None),
                    sparse_vector=(
                        dict(sparse.sparse_vector) if sparse and sparse.sparse_vector is not None else None
                    ),
                )
            )
        return merged

    @staticmethod
    def _validate_chunks(chunks: list[Chunk]) -> None:
        if not isinstance(chunks, list):
            raise TypeError("chunks must be a list")
        for index, chunk in enumerate(chunks):
            if not isinstance(chunk, Chunk):
                raise TypeError(f"chunk at index {index} must be a Chunk")

    @staticmethod
    def _extract_batch_settings(settings: Any) -> dict[str, Any]:
        if isinstance(settings, dict):
            ingestion = settings.get("ingestion")
        else:
            ingestion = getattr(settings, "ingestion", None)
        if isinstance(ingestion, dict):
            section = ingestion.get("batch_processor")
            if isinstance(section, dict):
                return dict(section)
        return {}

    @staticmethod
    def _to_bool(value: Any) -> bool:
        if isinstance(value, bool):
            return value
        return bool(value)

    @staticmethod
    def _normalize_batch_size(value: Any) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("batch_size must be an integer")
        if value <= 0:
            raise ValueError("batch_size must be greater than 0")
        return value
