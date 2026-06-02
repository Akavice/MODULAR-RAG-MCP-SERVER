"""Unit tests for CompositeEvaluator (H2)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import pytest

from libs.evaluator.base_evaluator import BaseEvaluator
from libs.evaluator.custom_evaluator import CustomEvaluator
from libs.evaluator.evaluator_factory import EvaluatorFactory
from observability.evaluation import CompositeEvaluator


class StaticEvaluator(BaseEvaluator):
    def __init__(self, metrics: dict[str, float], **options: Any) -> None:
        super().__init__(**options)
        self._metrics = metrics

    def evaluate(
        self,
        query: str,
        retrieved_ids: Sequence[str],
        golden_ids: Sequence[str],
        trace: Any | None = None,
    ) -> dict[str, float]:
        self.validate_inputs(query, retrieved_ids, golden_ids)
        _ = trace
        return dict(self._metrics)


class FakeEvaluator(BaseEvaluator):
    def evaluate(
        self,
        query: str,
        retrieved_ids: Sequence[str],
        golden_ids: Sequence[str],
        trace: Any | None = None,
    ) -> dict[str, float]:
        self.validate_inputs(query, retrieved_ids, golden_ids)
        _ = trace
        return {"faithfulness": 0.75}


class BadResultEvaluator(BaseEvaluator):
    def evaluate(
        self,
        query: str,
        retrieved_ids: Sequence[str],
        golden_ids: Sequence[str],
        trace: Any | None = None,
    ) -> dict[str, float]:
        self.validate_inputs(query, retrieved_ids, golden_ids)
        _ = trace
        return {"bad": "not-numeric"}  # type: ignore[return-value]


@pytest.fixture(autouse=True)
def reset_evaluator_registry() -> None:
    EvaluatorFactory.clear_registry()
    yield
    EvaluatorFactory.clear_registry()


@pytest.mark.unit
def test_composite_evaluator_merges_metrics_from_multiple_evaluators() -> None:
    evaluator = CompositeEvaluator(
        [
            StaticEvaluator({"faithfulness": 0.8, "answer_relevancy": 0.7}),
            StaticEvaluator({"hit_rate": 1.0, "mrr": 0.5}),
        ]
    )

    metrics = evaluator.evaluate(
        query="What is RAG?",
        retrieved_ids=["doc-a", "doc-b"],
        golden_ids=["doc-b"],
    )

    assert metrics == {
        "faithfulness": 0.8,
        "answer_relevancy": 0.7,
        "hit_rate": 1.0,
        "mrr": 0.5,
    }


@pytest.mark.unit
def test_composite_evaluator_prefixes_duplicate_metric_names() -> None:
    evaluator = CompositeEvaluator(
        [
            StaticEvaluator({"score": 0.4}),
            FakeEvaluator(),
            StaticEvaluator({"score": 0.6}),
        ]
    )

    metrics = evaluator.evaluate(
        query="What is RAG?",
        retrieved_ids=["doc-a"],
        golden_ids=["doc-a"],
    )

    assert metrics["score"] == 0.4
    assert metrics["static.score"] == 0.6
    assert metrics["faithfulness"] == 0.75


@pytest.mark.unit
def test_composite_evaluator_rejects_empty_or_invalid_evaluators() -> None:
    with pytest.raises(ValueError, match="evaluators must not be empty"):
        CompositeEvaluator([])

    with pytest.raises(TypeError, match=r"evaluators\[0\]"):
        CompositeEvaluator([object()])  # type: ignore[list-item]


@pytest.mark.unit
def test_composite_evaluator_rejects_non_numeric_metrics() -> None:
    evaluator = CompositeEvaluator([BadResultEvaluator()])

    with pytest.raises(TypeError, match="metric bad must be numeric"):
        evaluator.evaluate(
            query="What is RAG?",
            retrieved_ids=["doc-a"],
            golden_ids=["doc-a"],
        )


@pytest.mark.unit
def test_factory_creates_composite_from_backend_list() -> None:
    EvaluatorFactory.register("fake", FakeEvaluator)

    evaluator = EvaluatorFactory.create(
        {"evaluation": {"backends": ["custom", {"provider": "fake"}]}}
    )

    assert isinstance(evaluator, CompositeEvaluator)
    assert isinstance(evaluator.evaluators[0], CustomEvaluator)
    assert isinstance(evaluator.evaluators[1], FakeEvaluator)

    metrics = evaluator.evaluate(
        query="What is RAG?",
        retrieved_ids=["doc-a", "doc-b"],
        golden_ids=["doc-b"],
    )

    assert metrics["hit_rate"] == 1.0
    assert metrics["mrr"] == 0.5
    assert metrics["faithfulness"] == 0.75


@pytest.mark.unit
def test_factory_rejects_invalid_backends_config() -> None:
    with pytest.raises(ValueError, match="evaluation.backends must be a non-empty list"):
        EvaluatorFactory.create({"evaluation": {"backends": []}})

    with pytest.raises(TypeError, match=r"evaluation.backends\[0\]"):
        EvaluatorFactory.create({"evaluation": {"backends": [123]}})

    with pytest.raises(ValueError, match=r"evaluation.backends\[0\].provider"):
        EvaluatorFactory.create({"evaluation": {"backends": [{"provider": " "}]}})


@pytest.mark.unit
def test_composite_evaluator_preserves_all_duplicate_metric_names() -> None:
    evaluator = CompositeEvaluator(
        [
            StaticEvaluator({"score": 0.1}),
            StaticEvaluator({"score": 0.2}),
            StaticEvaluator({"score": 0.3}),
        ]
    )

    metrics = evaluator.evaluate(
        query="What is RAG?",
        retrieved_ids=["doc-a"],
        golden_ids=["doc-a"],
    )

    assert len(metrics) == 3
    assert sorted(metrics.values()) == [0.1, 0.2, 0.3]
