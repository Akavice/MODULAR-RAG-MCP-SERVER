"""Unit tests for core query-engine reranker fallback behavior."""

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
        metadata={"source_path": f"docs/{chunk_id}.pdf"},
    )


class TraceStub:
    def __init__(self) -> None:
        self.events: list[tuple[str, dict[str, Any]]] = []

    def record_stage(self, stage: str, **payload: Any) -> None:
        self.events.append((stage, payload))


class FakeBackend:
    def __init__(self, *, explode: bool = False) -> None:
        self.explode = explode
        self.calls: list[dict[str, Any]] = []

    def rerank(
        self,
        query: str,
        candidates: list[dict[str, Any]],
        trace: Any | None = None,
    ) -> list[dict[str, Any]]:
        _ = trace
        self.calls.append({"query": query, "candidate_count": len(candidates)})
        if self.explode:
            raise RuntimeError("backend down")
        return [candidates[1], candidates[0], *candidates[2:]]


@pytest.mark.unit
def test_reranker_returns_original_order_when_disabled() -> None:
    reranker = Reranker(settings={"rerank": {"enabled": False}})
    candidates = [_r("a", 1.0, "A"), _r("b", 0.8, "B")]

    out = reranker.rerank("q", candidates)

    assert [x.chunk_id for x in out] == ["a", "b"]


@pytest.mark.unit
def test_reranker_reorders_when_backend_succeeds() -> None:
    backend = FakeBackend()
    reranker = Reranker(settings={"rerank": {"enabled": True}}, reranker=backend)  # type: ignore[arg-type]
    candidates = [_r("a", 1.0, "A"), _r("b", 0.8, "B"), _r("c", 0.7, "C")]

    out = reranker.rerank("q", candidates)

    assert backend.calls[-1]["query"] == "q"
    assert [x.chunk_id for x in out] == ["b", "a", "c"]


@pytest.mark.unit
def test_reranker_fallbacks_when_backend_raises_and_marks_trace() -> None:
    trace = TraceStub()
    backend = FakeBackend(explode=True)
    reranker = Reranker(settings={"rerank": {"enabled": True}}, reranker=backend)  # type: ignore[arg-type]
    candidates = [_r("a", 1.0, "A"), _r("b", 0.8, "B")]

    out = reranker.rerank("q", candidates, trace=trace)

    assert [x.chunk_id for x in out] == ["a", "b"]
    stage, payload = trace.events[-1]
    assert stage == "rerank"
    assert payload["enabled"] is True
    assert payload["fallback"] is True
    assert str(payload["reason"]).startswith("rerank_failed:")


@pytest.mark.unit
def test_reranker_validates_inputs() -> None:
    reranker = Reranker(settings={"rerank": {"enabled": False}})
    with pytest.raises(TypeError, match="query must be a string"):
        reranker.rerank(123, [])  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="query must not be empty"):
        reranker.rerank(" ", [])
    with pytest.raises(TypeError, match="candidates must be a sequence"):
        reranker.rerank("q", "bad")  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="candidates\\[0\\] must be a RetrievalResult"):
        reranker.rerank("q", [{"id": "x"}])  # type: ignore[list-item]


@pytest.mark.unit
def test_reranker_fallbacks_when_backend_init_fails() -> None:
    trace = TraceStub()
    reranker = Reranker(
        settings={"rerank": {"enabled": True, "provider": "not_exists"}},
        reranker=None,
    )
    candidates = [_r("a", 1.0, "A")]

    out = reranker.rerank("q", candidates, trace=trace)

    assert [x.chunk_id for x in out] == ["a"]
    stage, payload = trace.events[-1]
    assert stage == "rerank"
    assert payload["fallback"] is True
