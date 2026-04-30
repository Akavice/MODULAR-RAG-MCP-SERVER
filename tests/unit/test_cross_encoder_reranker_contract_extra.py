"""Additional contract tests for CrossEncoderReranker edge cases."""

from __future__ import annotations
from typing import Any

import pytest

from libs.reranker.cross_encoder_reranker import (
    CrossEncoderReranker,
    CrossEncoderRerankerError,
)


@pytest.mark.unit
@pytest.mark.parametrize("bad_timeout", [float("nan"), float("inf"), float("-inf")])
def test_init_rejects_non_finite_timeout_values(bad_timeout: float) -> None:
    with pytest.raises(ValueError, match="timeout"):
        CrossEncoderReranker(timeout=bad_timeout)


@pytest.mark.unit
@pytest.mark.parametrize("bad_score", [float("nan"), float("inf"), float("-inf")])
def test_rerank_rejects_non_finite_scores(bad_score: float) -> None:
    def bad_scorer(query: str, candidates: list[dict[str, Any]]) -> list[float]:
        _ = query
        return [bad_score for _ in candidates]

    reranker = CrossEncoderReranker(scorer=bad_scorer)

    with pytest.raises(CrossEncoderRerankerError, match="ResponseError"):
        reranker.rerank(
            query="q",
            candidates=[{"id": "a", "text": "t1"}, {"id": "b", "text": "t2"}],
        )


@pytest.mark.unit
def test_tie_scores_keep_input_order_in_reranked_head() -> None:
    def tie_scorer(query: str, candidates: list[dict[str, Any]]) -> list[float]:
        _ = query
        return [0.7 for _ in candidates]

    reranker = CrossEncoderReranker(top_m=3, scorer=tie_scorer)
    ranked = reranker.rerank(
        query="q",
        candidates=[
            {"id": "a", "text": "a"},
            {"id": "b", "text": "b"},
            {"id": "c", "text": "c"},
            {"id": "tail", "text": "tail"},
        ],
    )

    assert [item["id"] for item in ranked] == ["a", "b", "c", "tail"]
