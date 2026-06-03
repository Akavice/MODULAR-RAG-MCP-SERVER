"""Unit tests for EvalRunner (H3)."""

from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import pytest

from core.types import RetrievalResult
from libs.evaluator.base_evaluator import BaseEvaluator
from libs.evaluator.custom_evaluator import CustomEvaluator
from observability.evaluation.eval_runner import EvalRunner
from scripts import evaluate as evaluate_cli


class StaticEvaluator(BaseEvaluator):
    def evaluate(
        self,
        query: str,
        retrieved_ids: Sequence[str],
        golden_ids: Sequence[str],
        trace: Any | None = None,
    ) -> dict[str, float]:
        self.validate_inputs(query, retrieved_ids, golden_ids)
        assert trace is not None
        return {"custom_score": 1.0 if retrieved_ids else 0.0}


class FakeHybridSearch:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def search(
        self,
        query: str,
        top_k: int | None = None,
        filters: dict[str, Any] | None = None,
    ) -> list[RetrievalResult]:
        self.calls.append({"query": query, "top_k": top_k, "filters": filters})
        if "Azure" in query:
            return [
                _result("chunk-other", "docs/other.pdf"),
                _result("chunk_azure_config", "docs/config_guide.pdf"),
            ]
        return [_result("chunk-x", "docs/dashboard_guide.pdf")]


def _result(chunk_id: str, source_path: str) -> RetrievalResult:
    return RetrievalResult(
        chunk_id=chunk_id,
        score=1.0,
        text=f"text for {chunk_id}",
        metadata={"source_path": source_path},
    )


def _write_test_set(tmp_path: Path, payload: dict[str, Any]) -> Path:
    path = tmp_path / "golden.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


@pytest.mark.unit
def test_eval_runner_runs_retrieval_and_aggregates_metrics(tmp_path: Path) -> None:
    test_set = _write_test_set(
        tmp_path,
        {
            "test_cases": [
                {
                    "query": "How do I configure Azure OpenAI?",
                    "expected_chunk_ids": ["chunk_azure_config"],
                    "expected_sources": ["config_guide.pdf"],
                    "filters": {"collection": "docs"},
                },
                {
                    "query": "How can I inspect query traces?",
                    "expected_chunk_ids": [],
                    "expected_sources": ["dashboard_guide.pdf"],
                },
            ]
        },
    )
    searcher = FakeHybridSearch()

    report = EvalRunner(
        settings={"retrieval": {"top_k": 3}},
        hybrid_search=searcher,
        evaluator=StaticEvaluator(),
    ).run(test_set)

    assert report.metrics["hit_rate"] == 1.0
    assert report.metrics["mrr"] == pytest.approx((0.5 + 1.0) / 2.0)
    assert report.metrics["custom_score"] == 1.0
    assert len(report.cases) == 2
    assert searcher.calls[0] == {
        "query": "How do I configure Azure OpenAI?",
        "top_k": 3,
        "filters": {"collection": "docs"},
    }
    assert report.to_dict()["cases"][0]["retrieved_ids"] == [
        "chunk-other",
        "chunk_azure_config",
    ]


@pytest.mark.unit
def test_eval_runner_rejects_invalid_golden_set(tmp_path: Path) -> None:
    test_set = _write_test_set(tmp_path, {"test_cases": [{"query": "q"}]})

    with pytest.raises(ValueError, match="expected_chunk_ids or expected_sources"):
        EvalRunner(
            settings={},
            hybrid_search=FakeHybridSearch(),
            evaluator=StaticEvaluator(),
        ).run(test_set)


@pytest.mark.unit
def test_eval_runner_validates_top_k() -> None:
    with pytest.raises(ValueError, match="top_k must be greater than 0"):
        EvalRunner(
            settings={},
            hybrid_search=FakeHybridSearch(),
            evaluator=StaticEvaluator(),
            top_k=0,
        )


@pytest.mark.unit
def test_evaluate_cli_dry_run_outputs_json(capsys: pytest.CaptureFixture[str]) -> None:
    code = evaluate_cli.main(["--test-set", "tests/fixtures/golden_test_set.json"])

    assert code == 0
    output = json.loads(capsys.readouterr().out)
    assert "metrics" in output
    assert len(output["cases"]) == 2


@pytest.mark.unit
def test_eval_runner_preserves_source_fallback_hit_rate_with_custom_evaluator(
    tmp_path: Path,
) -> None:
    test_set = _write_test_set(
        tmp_path,
        {
            "test_cases": [
                {
                    "query": "How can I inspect query traces?",
                    "expected_chunk_ids": [],
                    "expected_sources": ["dashboard_guide.pdf"],
                }
            ]
        },
    )

    report = EvalRunner(
        settings={"retrieval": {"top_k": 3}},
        hybrid_search=FakeHybridSearch(),
        evaluator=CustomEvaluator(),
    ).run(test_set)

    assert report.cases[0].retrieved_sources == ["docs/dashboard_guide.pdf"]
    assert report.cases[0].metrics["hit_rate"] == 1.0
    assert report.cases[0].metrics["mrr"] == 1.0
