"""Unit tests for RagasEvaluator (H1)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import pytest

from libs.evaluator.evaluator_factory import EvaluatorFactory
from libs.evaluator.ragas_evaluator import RagasEvaluator
from observability.evaluation.ragas_evaluator import RagasEvaluator as ObservabilityRagasEvaluator


@pytest.mark.unit
def test_ragas_evaluator_returns_metrics_with_mocked_ragas() -> None:
    captured: dict[str, Any] = {}

    def dataset_factory(samples: list[dict[str, Any]]) -> list[dict[str, Any]]:
        captured["samples"] = samples
        return samples

    def ragas_evaluate(dataset: Sequence[dict[str, Any]], *, metrics: Sequence[str]) -> dict[str, float]:
        captured["dataset"] = dataset
        captured["metrics"] = metrics
        return {
            "faithfulness": 0.8,
            "answer_relevancy": 0.7,
            "context_precision": 0.6,
        }

    evaluator = RagasEvaluator(
        ragas_evaluate=ragas_evaluate,
        dataset_factory=dataset_factory,
        metrics=["faithfulness", "answer_relevancy", "context_precision"],
    )

    metrics = evaluator.evaluate(
        query="How does RAG work?",
        retrieved_ids=["chunk-a", "chunk-b"],
        golden_ids=["chunk-b"],
        trace={
            "answer": "RAG retrieves context before generation.",
            "contexts": ["retrieved context"],
            "ground_truth": "reference answer",
        },
    )

    assert metrics == {
        "faithfulness": 0.8,
        "answer_relevancy": 0.7,
        "context_precision": 0.6,
    }
    assert captured["samples"][0]["question"] == "How does RAG work?"
    assert captured["samples"][0]["answer"] == "RAG retrieves context before generation."
    assert captured["samples"][0]["contexts"] == ["retrieved context"]
    assert captured["samples"][0]["ground_truth"] == "reference answer"
    assert list(captured["metrics"]) == ["faithfulness", "answer_relevancy", "context_precision"]


@pytest.mark.unit
def test_ragas_evaluator_uses_ids_as_fallback_sample_fields() -> None:
    def dataset_factory(samples: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return samples

    def ragas_evaluate(dataset: Sequence[dict[str, Any]], *, metrics: Sequence[str]) -> dict[str, float]:
        _ = metrics
        sample = list(dataset)[0]
        assert sample["contexts"] == ["chunk-a", "chunk-b"]
        assert sample["ground_truth"] == "chunk-b"
        return {"faithfulness": 1.0, "answer_relevancy": 1.0}

    evaluator = RagasEvaluator(
        ragas_evaluate=ragas_evaluate,
        dataset_factory=dataset_factory,
        metrics=["faithfulness", "answer_relevancy"],
    )

    metrics = evaluator.evaluate(
        query="What is configured?",
        retrieved_ids=["chunk-a", "chunk-b"],
        golden_ids=["chunk-b"],
    )

    assert metrics == {"faithfulness": 1.0, "answer_relevancy": 1.0}


@pytest.mark.unit
def test_ragas_evaluator_raises_clear_import_error_when_dependency_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def missing_ragas() -> dict[str, Any]:
        raise ImportError("RagasEvaluator requires optional dependencies `ragas` and `datasets`.")

    monkeypatch.setattr(RagasEvaluator, "_load_ragas", staticmethod(missing_ragas))
    evaluator = RagasEvaluator()

    with pytest.raises(ImportError, match="RagasEvaluator requires optional dependencies"):
        evaluator.evaluate(
            query="What is RAG?",
            retrieved_ids=["chunk-a"],
            golden_ids=["chunk-a"],
        )


@pytest.mark.unit
def test_ragas_evaluator_validates_inputs() -> None:
    evaluator = RagasEvaluator(
        ragas_evaluate=lambda *_args, **_kwargs: {"faithfulness": 1.0},
        dataset_factory=lambda samples: samples,
        metrics=["faithfulness"],
    )

    with pytest.raises(ValueError, match="query must not be empty"):
        evaluator.evaluate(query=" ", retrieved_ids=["chunk-a"], golden_ids=["chunk-a"])


@pytest.mark.unit
def test_evaluator_factory_creates_builtin_ragas_evaluator() -> None:
    evaluator = EvaluatorFactory.create({"evaluation": {"provider": "ragas"}})

    assert isinstance(evaluator, RagasEvaluator)
    assert "ragas" in EvaluatorFactory.registered_providers()


@pytest.mark.unit
def test_observability_ragas_evaluator_exports_libs_implementation() -> None:
    assert ObservabilityRagasEvaluator is RagasEvaluator
