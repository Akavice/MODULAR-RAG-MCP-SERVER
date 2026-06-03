"""E2E recall regression checks based on the golden test set."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from core.types import RetrievalResult
from libs.evaluator.custom_evaluator import CustomEvaluator
from observability.evaluation.eval_runner import EvalRunner


GOLDEN_TEST_SET = Path("tests/fixtures/golden_test_set.json")
MIN_HIT_RATE = 0.95
MIN_MRR = 0.80


def _result(chunk_id: str, source_path: str, text: str = "") -> RetrievalResult:
    return RetrievalResult(
        chunk_id=chunk_id,
        score=1.0,
        text=text or f"content for {chunk_id}",
        metadata={"source_path": source_path},
    )


class GoldenAwareSearch:
    """Deterministic retrieval fixture that mirrors the golden-set expectations."""

    def __init__(self, *, miss_query: str | None = None) -> None:
        self.miss_query = miss_query
        self.calls: list[dict[str, Any]] = []

    def search(
        self,
        query: str,
        top_k: int | None = None,
        filters: dict[str, Any] | None = None,
    ) -> list[RetrievalResult]:
        self.calls.append({"query": query, "top_k": top_k, "filters": filters})
        if query == self.miss_query:
            return [_result("chunk_unrelated", "docs/unrelated.pdf")]
        if "Azure" in query:
            return [_result("chunk_azure_config", "docs/config_guide.pdf")]
        if "query traces" in query:
            return [_result("chunk_query_trace", "docs/dashboard_guide.pdf")]
        if "recall regression" in query:
            return [_result("chunk_eval_fallback", "docs/evaluation_guide.pdf")]
        return []


@pytest.mark.e2e
def test_golden_set_recall_meets_threshold() -> None:
    search = GoldenAwareSearch()

    report = EvalRunner(
        settings={"retrieval": {"top_k": 5}},
        hybrid_search=search,
        evaluator=CustomEvaluator(),
    ).run(GOLDEN_TEST_SET)

    assert len(report.cases) == _golden_case_count()
    assert report.metrics["hit_rate"] >= MIN_HIT_RATE
    assert report.metrics["mrr"] >= MIN_MRR
    assert all(item.metrics["hit_rate"] == 1.0 for item in report.cases)


@pytest.mark.e2e
def test_recall_threshold_catches_missing_golden_hit() -> None:
    search = GoldenAwareSearch(miss_query="How can I inspect query traces?")

    report = EvalRunner(
        settings={"retrieval": {"top_k": 5}},
        hybrid_search=search,
        evaluator=CustomEvaluator(),
    ).run(GOLDEN_TEST_SET)

    assert report.metrics["hit_rate"] < MIN_HIT_RATE


@pytest.mark.e2e
def test_recall_threshold_catches_missing_source_only_golden_hit() -> None:
    search = GoldenAwareSearch(miss_query="How do I run recall regression?")

    report = EvalRunner(
        settings={"retrieval": {"top_k": 5}},
        hybrid_search=search,
        evaluator=CustomEvaluator(),
    ).run(GOLDEN_TEST_SET)

    assert report.metrics["hit_rate"] < MIN_HIT_RATE


def _golden_case_count() -> int:
    payload = json.loads(GOLDEN_TEST_SET.read_text(encoding="utf-8"))
    return len(payload["test_cases"])
