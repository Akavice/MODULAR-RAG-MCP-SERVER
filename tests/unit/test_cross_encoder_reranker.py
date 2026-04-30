"""Unit tests for CrossEncoderReranker behavior and error signals."""

from __future__ import annotations

import time
from typing import Any

import pytest

from libs.reranker.cross_encoder_reranker import (
    CrossEncoderReranker,
    CrossEncoderRerankerError,
)


@pytest.mark.unit
def test_rerank_sorts_top_m_by_scorer_and_preserves_tail_order() -> None:
    def fake_scorer(query: str, candidates: list[dict[str, Any]]) -> list[float]:
        _ = query
        _ = candidates
        return [0.2, 0.9, 0.5]

    reranker = CrossEncoderReranker(top_m=3, scorer=fake_scorer)
    candidates = [
        {"id": "a", "text": "a"},
        {"id": "b", "text": "b"},
        {"id": "c", "text": "c"},
        {"id": "tail-1", "text": "tail-1"},
        {"id": "tail-2", "text": "tail-2"},
    ]

    ranked = reranker.rerank(query="q", candidates=candidates)

    assert [item["id"] for item in ranked] == ["b", "c", "a", "tail-1", "tail-2"]
    assert ranked[0]["score"] == pytest.approx(0.9)
    assert ranked[1]["score"] == pytest.approx(0.5)
    assert ranked[2]["score"] == pytest.approx(0.2)
    assert "score" not in ranked[3]


@pytest.mark.unit
def test_rerank_uses_default_scorer_without_external_dependencies() -> None:
    reranker = CrossEncoderReranker()
    candidates = [
        {"id": "low", "text": "alpha"},
        {"id": "high", "text": "alpha beta"},
        {"id": "none", "text": "gamma"},
    ]

    ranked = reranker.rerank(query="alpha beta", candidates=candidates)

    assert [item["id"] for item in ranked][:2] == ["high", "low"]
    assert ranked[0]["score"] > ranked[1]["score"] > ranked[2]["score"]


@pytest.mark.unit
def test_rerank_raises_timeout_signal_when_scorer_raises_timeout() -> None:
    def timeout_scorer(query: str, candidates: list[dict[str, Any]]) -> list[float]:
        _ = query
        _ = candidates
        raise TimeoutError("scorer timeout")

    reranker = CrossEncoderReranker(scorer=timeout_scorer)

    with pytest.raises(CrossEncoderRerankerError, match=r"\[cross_encoder\]\[TimeoutError\]"):
        reranker.rerank(query="q", candidates=[{"id": "a", "text": "x"}])


@pytest.mark.unit
def test_rerank_raises_backend_signal_when_scorer_fails() -> None:
    def broken_scorer(query: str, candidates: list[dict[str, Any]]) -> list[float]:
        _ = query
        _ = candidates
        raise RuntimeError("backend failed")

    reranker = CrossEncoderReranker(scorer=broken_scorer)

    with pytest.raises(CrossEncoderRerankerError, match=r"\[cross_encoder\]\[BackendError\]"):
        reranker.rerank(query="q", candidates=[{"id": "a", "text": "x"}])


@pytest.mark.unit
def test_rerank_raises_timeout_signal_when_execution_exceeds_timeout() -> None:
    def slow_scorer(query: str, candidates: list[dict[str, Any]]) -> list[float]:
        _ = query
        time.sleep(0.02)
        return [0.1 for _ in candidates]

    reranker = CrossEncoderReranker(timeout=0.001, scorer=slow_scorer)

    with pytest.raises(CrossEncoderRerankerError, match=r"\[cross_encoder\]\[TimeoutError\]"):
        reranker.rerank(query="q", candidates=[{"id": "a", "text": "x"}])


@pytest.mark.unit
@pytest.mark.parametrize("bad_top_m", [0, -1, "3"])
def test_init_rejects_invalid_top_m(bad_top_m: Any) -> None:
    with pytest.raises((TypeError, ValueError), match="top_m"):
        CrossEncoderReranker(top_m=bad_top_m)
