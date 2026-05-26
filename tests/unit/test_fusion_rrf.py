"""Unit tests for reciprocal-rank-fusion behavior."""

from __future__ import annotations

import pytest

from core.query_engine.fusion import Fusion
from core.types import RetrievalResult


def _r(chunk_id: str, score: float, text: str) -> RetrievalResult:
    return RetrievalResult(
        chunk_id=chunk_id,
        score=score,
        text=text,
        metadata={"source_path": f"docs/{chunk_id}.pdf"},
    )


@pytest.mark.unit
def test_fuse_rrf_merges_dense_sparse_deterministically() -> None:
    fusion = Fusion(settings={"retrieval": {"top_k": 5, "rrf_k": 10}})
    dense = [_r("a", 0.9, "A"), _r("b", 0.8, "B"), _r("c", 0.7, "C")]
    sparse = [_r("b", 2.0, "B2"), _r("d", 1.5, "D"), _r("a", 1.0, "A2")]

    fused = fusion.fuse(dense, sparse)

    assert [item.chunk_id for item in fused] == ["b", "a", "d", "c"]
    # Keep payload from first seen channel (dense first).
    assert fused[0].text == "B"
    assert fused[1].text == "A"


@pytest.mark.unit
def test_fuse_respects_top_k_override() -> None:
    fusion = Fusion(settings={"retrieval": {"top_k": 5}})
    dense = [_r("a", 1.0, "A"), _r("b", 0.5, "B"), _r("c", 0.4, "C")]
    sparse = [_r("c", 2.0, "C2"), _r("a", 1.0, "A2"), _r("d", 0.9, "D")]

    fused = fusion.fuse(dense, sparse, top_k=2)

    assert len(fused) == 2


@pytest.mark.unit
def test_fuse_deduplicates_duplicate_ids_within_each_channel() -> None:
    fusion = Fusion(settings={"retrieval": {"rrf_k": 5}})
    dense = [_r("a", 1.0, "A"), _r("a", 0.9, "A2"), _r("b", 0.8, "B")]
    sparse = [_r("b", 1.0, "B2"), _r("c", 0.9, "C")]

    fused = fusion.fuse(dense, sparse)

    assert [item.chunk_id for item in fused][:3] == ["b", "a", "c"]


@pytest.mark.unit
def test_fuse_rejects_invalid_inputs() -> None:
    fusion = Fusion(settings={})
    with pytest.raises(TypeError, match="dense_results must be a sequence"):
        fusion.fuse("x", [])  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="sparse_results\\[0\\] must be a RetrievalResult"):
        fusion.fuse([], ["x"])  # type: ignore[list-item]
    with pytest.raises(TypeError, match="top_k must be an integer"):
        fusion.fuse([], [], top_k="2")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="top_k must be greater than 0"):
        fusion.fuse([], [], top_k=0)


@pytest.mark.unit
def test_rrf_k_config_is_respected() -> None:
    dense = [_r("a", 1.0, "A"), _r("b", 0.9, "B")]
    sparse = [_r("b", 1.0, "B2"), _r("a", 0.8, "A2")]

    small_k = Fusion(settings={"retrieval": {"rrf_k": 1}})
    large_k = Fusion(settings={"retrieval": {"rrf_k": 100}})

    fused_small = small_k.fuse(dense, sparse)
    fused_large = large_k.fuse(dense, sparse)

    assert [item.chunk_id for item in fused_small] == [item.chunk_id for item in fused_large]
    assert fused_small[0].score != fused_large[0].score
