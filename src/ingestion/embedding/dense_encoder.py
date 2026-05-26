"""Dense embedding encoder for ingestion chunks."""

from __future__ import annotations

from math import ceil
from typing import Any

from core.types import Chunk, ChunkRecord
from libs.embedding.base_embedding import BaseEmbedding
from libs.embedding.embedding_factory import EmbeddingFactory


class DenseEncoder:
    """Encode chunk text into dense vectors via pluggable embedding backends."""

    def __init__(
        self,
        settings: Any,
        embedding_client: BaseEmbedding | None = None,
        *,
        batch_size: int | None = None,
    ) -> None:
        self.settings = settings
        self.embedding_client = embedding_client or EmbeddingFactory.create(settings)
        self.batch_size = (
            self._normalize_batch_size(batch_size)
            if batch_size is not None
            else self._resolve_batch_size(settings)
        )

    def encode(self, chunks: list[Chunk], trace: Any | None = None) -> list[ChunkRecord]:
        self._validate_chunks(chunks)
        if not chunks:
            if trace is not None and hasattr(trace, "record_stage"):
                trace.record_stage(
                    "embed_dense_encoder",
                    chunk_count=0,
                    batch_size=self.batch_size,
                    batch_count=0,
                    vector_dim=0,
                )
            return []

        chunk_records: list[ChunkRecord] = []
        vector_dim = 0

        for start in range(0, len(chunks), self.batch_size):
            batch = chunks[start : start + self.batch_size]
            texts = [item.text for item in batch]
            vectors = self.embedding_client.embed(texts, trace=trace)
            if not isinstance(vectors, list):
                raise TypeError("embedding output must be a list of vectors")
            if len(vectors) != len(batch):
                raise ValueError("embedding output size must match input chunk size")

            for chunk, vector in zip(batch, vectors):
                record = ChunkRecord(
                    id=chunk.id,
                    text=chunk.text,
                    metadata=dict(chunk.metadata),
                    dense_vector=vector,
                    sparse_vector=None,
                )
                if record.dense_vector is not None and not vector_dim:
                    vector_dim = len(record.dense_vector)
                if record.dense_vector is not None and len(record.dense_vector) != vector_dim:
                    raise ValueError(
                        "embedding output dimension mismatch: "
                        f"expected {vector_dim}, got {len(record.dense_vector)}"
                    )
                chunk_records.append(record)

        if trace is not None and hasattr(trace, "record_stage"):
            trace.record_stage(
                "embed_dense_encoder",
                chunk_count=len(chunks),
                batch_size=self.batch_size,
                batch_count=ceil(len(chunks) / self.batch_size),
                vector_dim=vector_dim,
            )

        return chunk_records

    @staticmethod
    def _validate_chunks(chunks: list[Chunk]) -> None:
        if not isinstance(chunks, list):
            raise TypeError("chunks must be a list")
        for index, chunk in enumerate(chunks):
            if not isinstance(chunk, Chunk):
                raise TypeError(f"chunk at index {index} must be a Chunk")

    @staticmethod
    def _normalize_batch_size(value: Any) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("batch_size must be an integer")
        if value <= 0:
            raise ValueError("batch_size must be greater than 0")
        return value

    @staticmethod
    def _resolve_batch_size(settings: Any) -> int:
        if isinstance(settings, dict):
            ingestion = settings.get("ingestion")
        else:
            ingestion = getattr(settings, "ingestion", None)

        if isinstance(ingestion, dict):
            dense = ingestion.get("dense_encoder")
            if isinstance(dense, dict) and "batch_size" in dense:
                return DenseEncoder._normalize_batch_size(dense.get("batch_size"))
        return 32
