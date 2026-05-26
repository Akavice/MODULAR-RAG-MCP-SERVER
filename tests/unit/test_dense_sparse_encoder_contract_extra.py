"""Extra contract tests for DenseEncoder and SparseEncoder."""

from __future__ import annotations

from typing import Any

import pytest

from core.types import Chunk
from ingestion.embedding.dense_encoder import DenseEncoder
from ingestion.embedding.sparse_encoder import SparseEncoder
from libs.embedding.base_embedding import BaseEmbedding


class FakeEmbedding(BaseEmbedding):
    def __init__(self, vectors: list[list[float]], **options: Any) -> None:
        super().__init__(**options)
        self.vectors = vectors

    def embed(self, texts: list[str], trace: Any | None = None) -> list[list[float]]:
        _ = texts, trace
        return [list(v) for v in self.vectors]


def _chunk(text: str, idx: int) -> Chunk:
    return Chunk(
        id=f"chunk-{idx}",
        text=text,
        metadata={"source_path": "docs/a.pdf"},
        start_offset=0,
        end_offset=len(text),
        source_ref="doc-1",
    )


@pytest.mark.unit
def test_dense_encoder_rejects_inconsistent_vector_dimensions() -> None:
    encoder = DenseEncoder(
        settings={},
        embedding_client=FakeEmbedding(vectors=[[1.0, 2.0], [3.0]]),
        batch_size=8,
    )

    with pytest.raises(ValueError, match="dimension"):
        encoder.encode([_chunk("alpha", 0), _chunk("beta", 1)])


@pytest.mark.unit
def test_dense_encoder_rejects_invalid_batch_size_from_settings() -> None:
    with pytest.raises(TypeError, match="batch_size must be an integer"):
        DenseEncoder(
            settings={"ingestion": {"dense_encoder": {"batch_size": "32"}}},
            embedding_client=FakeEmbedding(vectors=[[1.0]]),
        )


@pytest.mark.unit
def test_sparse_encoder_rejects_invalid_numeric_params() -> None:
    with pytest.raises(ValueError, match="k1 must be a finite number > 0"):
        SparseEncoder(settings={"ingestion": {"sparse_encoder": {"k1": 0}}})

    with pytest.raises(ValueError, match="b must be a finite number in \\[0, 1\\]"):
        SparseEncoder(settings={"ingestion": {"sparse_encoder": {"b": 1.5}}})

    with pytest.raises(ValueError, match="min_token_length must be greater than 0"):
        SparseEncoder(settings={"ingestion": {"sparse_encoder": {"min_token_length": 0}}})

