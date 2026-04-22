"""Unit tests for CustomEvaluator and EvaluatorFactory."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from libs.evaluator.base_evaluator import BaseEvaluator
from libs.evaluator.custom_evaluator import CustomEvaluator
from libs.evaluator.evaluator_factory import EvaluatorFactory


class FakeEvaluator(BaseEvaluator):
    """Simple deterministic evaluator used in factory routing tests."""

    def evaluate(
        self,
        query: str,
        retrieved_ids: list[str],
        golden_ids: list[str],
        trace: Any | None = None,
    ) -> dict[str, float]:
        self.validate_inputs(
            query=query,
            retrieved_ids=retrieved_ids,
            golden_ids=golden_ids,
        )
        return {"hit_rate": 0.5, "mrr": 0.25}


@dataclass(slots=True)
class FakeSettings:
    """Minimal settings object exposing `.evaluation` mapping."""

    evaluation: dict[str, Any]


@pytest.fixture(autouse=True)
def reset_evaluator_registry() -> None:
    """Ensure tests do not leak registered providers across cases."""
    EvaluatorFactory.clear_registry()
    yield
    EvaluatorFactory.clear_registry()


@pytest.mark.unit
def test_custom_evaluator_returns_hit_rate_and_mrr_for_match() -> None:
    evaluator = CustomEvaluator()

    metrics = evaluator.evaluate(
        query="What is RAG?",
        retrieved_ids=["doc-a", "doc-b", "doc-c"],
        golden_ids=["doc-x", "doc-b"],
    )

    assert metrics["hit_rate"] == 1.0
    assert metrics["mrr"] == 0.5


@pytest.mark.unit
def test_custom_evaluator_returns_zero_metrics_when_no_match() -> None:
    evaluator = CustomEvaluator()

    metrics = evaluator.evaluate(
        query="What is RAG?",
        retrieved_ids=["doc-a", "doc-b"],
        golden_ids=["doc-z"],
    )

    assert metrics == {"hit_rate": 0.0, "mrr": 0.0}


@pytest.mark.unit
def test_custom_evaluator_returns_zero_metrics_when_golden_is_empty() -> None:
    evaluator = CustomEvaluator()

    metrics = evaluator.evaluate(
        query="What is RAG?",
        retrieved_ids=["doc-a", "doc-b"],
        golden_ids=[],
    )

    assert metrics == {"hit_rate": 0.0, "mrr": 0.0}


@pytest.mark.unit
def test_custom_evaluator_validates_query() -> None:
    evaluator = CustomEvaluator()

    with pytest.raises(ValueError, match="query must not be empty"):
        evaluator.evaluate(query=" ", retrieved_ids=["doc-a"], golden_ids=["doc-a"])


@pytest.mark.unit
def test_factory_create_returns_builtin_custom_evaluator() -> None:
    evaluator = EvaluatorFactory.create({"evaluation": {"provider": "custom"}})

    assert isinstance(evaluator, CustomEvaluator)


@pytest.mark.unit
def test_factory_create_routes_by_registered_provider() -> None:
    EvaluatorFactory.register("fake", FakeEvaluator)

    evaluator = EvaluatorFactory.create({"evaluation": {"provider": "fake"}})

    assert isinstance(evaluator, FakeEvaluator)


@pytest.mark.unit
def test_factory_create_accepts_object_settings() -> None:
    settings = FakeSettings(evaluation={"provider": "custom"})

    evaluator = EvaluatorFactory.create(settings)

    assert isinstance(evaluator, CustomEvaluator)


@pytest.mark.unit
def test_factory_raises_for_missing_provider() -> None:
    with pytest.raises(ValueError, match="evaluation.provider"):
        EvaluatorFactory.create({"evaluation": {}})


@pytest.mark.unit
def test_factory_raises_for_unknown_provider() -> None:
    with pytest.raises(ValueError, match="Unsupported evaluation provider"):
        EvaluatorFactory.create({"evaluation": {"provider": "unknown"}})
