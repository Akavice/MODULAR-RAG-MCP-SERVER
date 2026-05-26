"""Additional E2E contract tests for query CLI (D7)."""

from __future__ import annotations

from typing import Any

import pytest

from core.types import RetrievalResult
from scripts import query as query_cli


def _r(chunk_id: str, score: float, text: str) -> RetrievalResult:
    return RetrievalResult(
        chunk_id=chunk_id,
        score=score,
        text=text,
        metadata={"source_path": f"docs/{chunk_id}.pdf"},
    )


class _SearchCapture:
    calls: list[dict[str, Any]] = []

    def __init__(self, settings: Any) -> None:
        self.settings = settings

    def search(
        self,
        query: str,
        top_k: int | None = None,
        filters: dict[str, Any] | None = None,
        trace: Any | None = None,
    ) -> list[RetrievalResult]:
        _ = trace
        self.calls.append({"query": query, "top_k": top_k, "filters": filters})
        return [_r("a", 0.9, "A"), _r("b", 0.8, "B"), _r("c", 0.7, "C")]


class _RerankerPassthrough:
    def __init__(self, settings: Any) -> None:
        self.settings = settings

    def rerank(
        self,
        query: str,
        candidates: list[RetrievalResult],
        trace: Any | None = None,
    ) -> list[RetrievalResult]:
        _ = (query, trace)
        return candidates


@pytest.mark.e2e
def test_query_cli_rejects_non_positive_top_k(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(query_cli, "load_settings", lambda _: {"retrieval": {"top_k": 5}})
    monkeypatch.setattr(query_cli, "HybridSearch", _SearchCapture)
    monkeypatch.setattr(query_cli, "Reranker", _RerankerPassthrough)

    code = query_cli.main(["--query", "rag", "--top-k", "0"])
    stdout = capsys.readouterr().out

    assert code == 1
    assert "--top-k must be greater than 0" in stdout


@pytest.mark.e2e
def test_query_cli_normalizes_blank_collection_to_no_filter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _SearchCapture.calls.clear()
    monkeypatch.setattr(query_cli, "load_settings", lambda _: {"retrieval": {"top_k": 5}})
    monkeypatch.setattr(query_cli, "HybridSearch", _SearchCapture)
    monkeypatch.setattr(query_cli, "Reranker", _RerankerPassthrough)

    code = query_cli.main(["--query", "rag", "--collection", "   "])

    assert code == 0
    assert _SearchCapture.calls[-1]["filters"] is None


@pytest.mark.e2e
def test_query_cli_emits_no_results_message(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    class _EmptySearch(_SearchCapture):
        def search(
            self,
            query: str,
            top_k: int | None = None,
            filters: dict[str, Any] | None = None,
            trace: Any | None = None,
        ) -> list[RetrievalResult]:
            _ = (query, top_k, filters, trace)
            return []

    monkeypatch.setattr(query_cli, "load_settings", lambda _: {"retrieval": {"top_k": 5}})
    monkeypatch.setattr(query_cli, "HybridSearch", _EmptySearch)
    monkeypatch.setattr(query_cli, "Reranker", _RerankerPassthrough)

    code = query_cli.main(["--query", "rag"])
    stdout = capsys.readouterr().out

    assert code == 0
    assert "[query] no results" in stdout


@pytest.mark.e2e
def test_query_cli_applies_final_top_k_trim_after_search(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(query_cli, "load_settings", lambda _: {"retrieval": {"top_k": 5}})
    monkeypatch.setattr(query_cli, "HybridSearch", _SearchCapture)
    monkeypatch.setattr(query_cli, "Reranker", _RerankerPassthrough)

    code = query_cli.main(["--query", "rag", "--top-k", "2"])
    stdout = capsys.readouterr().out
    lines = [x for x in stdout.splitlines() if x.strip()]

    assert code == 0
    assert lines[0] == "[query] results=2"
    assert sum(1 for x in lines if x.startswith("[") and " id=" in x) == 2
