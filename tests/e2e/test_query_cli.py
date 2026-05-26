"""E2E-style tests for query CLI behavior."""

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


class FakeSearch:
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
        self.calls.append(
            {"query": query, "top_k": top_k, "filters": dict(filters or {})}
        )
        if trace is not None and hasattr(trace, "record_stage"):
            trace.record_stage("dense_retrieval", hit_count=2)
        return [_r("a", 0.9, "alpha"), _r("b", 0.8, "beta")]


class FakeReranker:
    calls: list[dict[str, Any]] = []

    def __init__(self, settings: Any) -> None:
        self.settings = settings

    def rerank(
        self,
        query: str,
        candidates: list[RetrievalResult],
        trace: Any | None = None,
    ) -> list[RetrievalResult]:
        self.calls.append({"query": query, "count": len(candidates)})
        if trace is not None and hasattr(trace, "record_stage"):
            trace.record_stage("rerank", fallback=False)
        return list(reversed(candidates))


@pytest.mark.e2e
def test_query_cli_runs_search_and_rerank(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    FakeSearch.calls.clear()
    FakeReranker.calls.clear()
    monkeypatch.setattr(query_cli, "load_settings", lambda path: {"retrieval": {"top_k": 5}})
    monkeypatch.setattr(query_cli, "HybridSearch", FakeSearch)
    monkeypatch.setattr(query_cli, "Reranker", FakeReranker)

    code = query_cli.main(["--query", "rag", "--top-k", "2", "--collection", "kb"])
    stdout = capsys.readouterr().out

    assert code == 0
    assert FakeSearch.calls[-1]["query"] == "rag"
    assert FakeSearch.calls[-1]["top_k"] == 2
    assert FakeSearch.calls[-1]["filters"] == {"collection": "kb"}
    assert FakeReranker.calls[-1]["query"] == "rag"
    assert "[query] results=2" in stdout
    # Reranked order should be reversed by FakeReranker.
    assert "id=b" in stdout.splitlines()[1]


@pytest.mark.e2e
def test_query_cli_no_rerank_skips_reranker(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    FakeSearch.calls.clear()
    FakeReranker.calls.clear()
    monkeypatch.setattr(query_cli, "load_settings", lambda path: {"retrieval": {"top_k": 5}})
    monkeypatch.setattr(query_cli, "HybridSearch", FakeSearch)
    monkeypatch.setattr(query_cli, "Reranker", FakeReranker)

    code = query_cli.main(["--query", "rag", "--no-rerank"])
    stdout = capsys.readouterr().out

    assert code == 0
    assert len(FakeReranker.calls) == 0
    assert "[query] results=2" in stdout
    assert "id=a" in stdout.splitlines()[1]


@pytest.mark.e2e
def test_query_cli_verbose_prints_trace(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    FakeSearch.calls.clear()
    FakeReranker.calls.clear()
    monkeypatch.setattr(query_cli, "load_settings", lambda path: {"retrieval": {"top_k": 5}})
    monkeypatch.setattr(query_cli, "HybridSearch", FakeSearch)
    monkeypatch.setattr(query_cli, "Reranker", FakeReranker)

    code = query_cli.main(["--query", "rag", "--verbose"])
    stdout = capsys.readouterr().out

    assert code == 0
    assert "[query][verbose] trace stages:" in stdout
    assert "stage=dense_retrieval" in stdout
    assert "stage=rerank" in stdout


@pytest.mark.e2e
def test_query_cli_returns_1_on_settings_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def _raise(_: str) -> dict[str, Any]:
        raise query_cli.SettingsError("bad config")

    monkeypatch.setattr(query_cli, "load_settings", _raise)
    code = query_cli.main(["--query", "rag"])
    stdout = capsys.readouterr().out

    assert code == 1
    assert "configuration error" in stdout


@pytest.mark.e2e
def test_query_cli_returns_2_on_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    class FailingSearch(FakeSearch):
        def search(
            self,
            query: str,
            top_k: int | None = None,
            filters: dict[str, Any] | None = None,
            trace: Any | None = None,
        ) -> list[RetrievalResult]:
            _ = query, top_k, filters, trace
            raise RuntimeError("boom")

    monkeypatch.setattr(query_cli, "load_settings", lambda path: {"retrieval": {"top_k": 5}})
    monkeypatch.setattr(query_cli, "HybridSearch", FailingSearch)
    monkeypatch.setattr(query_cli, "Reranker", FakeReranker)

    code = query_cli.main(["--query", "rag"])
    stdout = capsys.readouterr().out

    assert code == 2
    assert "query failed" in stdout
