"""Extra contract tests for Fusion (D4)."""

from __future__ import annotations

import pytest

from core.query_engine.fusion import Fusion
from core.types import RetrievalResult


def _r(chunk_id: str, score: float, text: str, source: str = "docs/x.pdf") -> RetrievalResult:
    return RetrievalResult(chunk_id=chunk_id, score=score, text=text, metadata={"source_path": source})


class _TraceStub:
    def __init__(self) -> None:
        self.events: list[tuple[str, dict[str, object]]] = []

    def record_stage(self, stage: str, **payload: object) -> None:
        self.events.append((stage, payload))


@pytest.mark.unit
def test_fusion_records_trace_payload() -> None:
    fusion = Fusion(settings={"retrieval": {"top_k": 3, "rrf_k": 7}})
    trace = _TraceStub()

    dense = [_r("a", 1.0, "A"), _r("b", 0.8, "B")]
    sparse = [_r("b", 1.0, "B2"), _r("c", 0.9, "C")]
    fused = fusion.fuse(dense, sparse, trace=trace)

    assert len(fused) == 3
    assert len(trace.events) == 1
    stage, payload = trace.events[0]
    assert stage == "fusion"
    assert payload == {
        "method": "rrf",
        "rrf_k": 7,
        "dense_count": 2,
        "sparse_count": 2,
        "fused_count": 3,
        "top_k": 3,
    }


@pytest.mark.unit
def test_fusion_uses_nested_fusion_rrf_k_before_retrieval_rrf_k() -> None:
    fusion = Fusion(settings={"retrieval": {"rrf_k": 99, "fusion": {"rrf_k": 11}}})
    dense = [_r("a", 1.0, "A"), _r("b", 0.5, "B")]
    sparse = [_r("b", 1.0, "B2"), _r("a", 0.4, "A2")]

    fused = fusion.fuse(dense, sparse)

    expected_a = (1.0 / (11 + 1)) + (1.0 / (11 + 2))
    assert fused[0].chunk_id == "a"
    assert fused[0].score == pytest.approx(expected_a)


@pytest.mark.unit
def test_fusion_rejects_invalid_rrf_k_from_settings() -> None:
    with pytest.raises(TypeError, match="rrf_k must be an integer"):
        Fusion(settings={"retrieval": {"rrf_k": True}})
    with pytest.raises(ValueError, match="rrf_k must be greater than 0"):
        Fusion(settings={"retrieval": {"rrf_k": 0}})


@pytest.mark.unit
def test_fusion_rejects_invalid_default_top_k_from_settings() -> None:
    with pytest.raises(TypeError, match="top_k must be an integer"):
        Fusion(settings={"retrieval": {"top_k": "3"}})
    with pytest.raises(ValueError, match="top_k must be greater than 0"):
        Fusion(settings={"retrieval": {"top_k": -1}})


@pytest.mark.unit
def test_fusion_output_metadata_is_defensive_copy() -> None:
    fusion = Fusion(settings={"retrieval": {"top_k": 5}})
    dense = [_r("a", 1.0, "A", source="docs/a.pdf")]
    sparse: list[RetrievalResult] = []

    fused = fusion.fuse(dense, sparse)
    fused[0].metadata["source_path"] = "docs/changed.pdf"

    assert dense[0].metadata["source_path"] == "docs/a.pdf"
