"""Additional contract tests for core Reranker fallback behavior."""

from __future__ import annotations

from typing import Any

import pytest

from core.query_engine.reranker import Reranker
from core.types import RetrievalResult


def _r(chunk_id: str, score: float, text: str) -> RetrievalResult:
    return RetrievalResult(
        chunk_id=chunk_id,
        score=score,
        text=text,
        metadata={"source_path": f"docs/{chunk_id}.pdf", "tag": chunk_id},
    )


class _Backend:
    def __init__(self, response: Any) -> None:
        self.response = response

    def rerank(self, query: str, candidates: list[dict[str, Any]], trace: Any | None = None) -> Any:
        _ = (query, candidates, trace)
        return self.response


@pytest.mark.unit
def test_reranker_fallbacks_when_backend_returns_non_sequence() -> None:
    reranker = Reranker(
        settings={"rerank": {"enabled": True}},
        reranker=_Backend(response={"id": "b"}),  # type: ignore[arg-type]
    )
    candidates = [_r("a", 0.9, "A"), _r("b", 0.8, "B")]

    out = reranker.rerank("q", candidates)

    assert [x.chunk_id for x in out] == ["a", "b"]


@pytest.mark.unit
def test_reranker_ignores_unmatched_rows_and_keeps_remaining_order() -> None:
    reranker = Reranker(
        settings={"rerank": {"enabled": True}},
        reranker=_Backend(response=[{"id": "missing"}, {"id": "b"}]),  # type: ignore[arg-type]
    )
    candidates = [_r("a", 0.9, "A"), _r("b", 0.8, "B"), _r("c", 0.7, "C")]

    out = reranker.rerank("q", candidates)

    assert [x.chunk_id for x in out] == ["b", "a", "c"]


@pytest.mark.unit
def test_reranker_deduplicates_duplicate_backend_ids() -> None:
    reranker = Reranker(
        settings={"rerank": {"enabled": True}},
        reranker=_Backend(response=[{"id": "b"}, {"id": "b"}, {"id": "a"}]),  # type: ignore[arg-type]
    )
    candidates = [_r("a", 0.9, "A"), _r("b", 0.8, "B"), _r("c", 0.7, "C")]

    out = reranker.rerank("q", candidates)

    assert [x.chunk_id for x in out] == ["b", "a", "c"]


@pytest.mark.unit
def test_reranker_coalesces_invalid_backend_fields_to_source_values() -> None:
    reranker = Reranker(
        settings={"rerank": {"enabled": True}},
        reranker=_Backend(
            response=[
                {"id": "b", "score": "bad", "text": 123, "metadata": "bad"},
                {"id": "a", "score": 0.123, "text": "A-new", "metadata": {"source_path": "docs/new.pdf"}},
            ]
        ),  # type: ignore[arg-type]
    )
    candidates = [_r("a", 0.9, "A"), _r("b", 0.8, "B")]

    out = reranker.rerank("q", candidates)

    assert [x.chunk_id for x in out] == ["b", "a"]
    assert out[0].score == pytest.approx(0.8)
    assert out[0].text == "123"
    assert out[0].metadata["tag"] == "b"
    assert out[1].score == pytest.approx(0.123)
    assert out[1].text == "A-new"
    assert out[1].metadata["source_path"] == "docs/new.pdf"
