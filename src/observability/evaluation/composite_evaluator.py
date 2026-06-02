"""Composite evaluator for running multiple evaluation backends."""

from __future__ import annotations

from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from libs.evaluator.base_evaluator import BaseEvaluator


class CompositeEvaluator(BaseEvaluator):
    """Run multiple evaluators and merge their metric outputs."""

    def __init__(self, evaluators: Sequence[BaseEvaluator], **options: Any) -> None:
        super().__init__(**options)
        if not isinstance(evaluators, Sequence) or isinstance(evaluators, (str, bytes)):
            raise TypeError("evaluators must be a sequence of BaseEvaluator instances")
        if not evaluators:
            raise ValueError("evaluators must not be empty")

        self.evaluators: tuple[BaseEvaluator, ...] = tuple(evaluators)
        for index, evaluator in enumerate(self.evaluators):
            if not isinstance(evaluator, BaseEvaluator):
                raise TypeError(f"evaluators[{index}] must be a BaseEvaluator instance")

    def evaluate(
        self,
        query: str,
        retrieved_ids: Sequence[str],
        golden_ids: Sequence[str],
        trace: Any | None = None,
    ) -> dict[str, float]:
        self.validate_inputs(
            query=query,
            retrieved_ids=retrieved_ids,
            golden_ids=golden_ids,
        )

        with ThreadPoolExecutor(max_workers=len(self.evaluators)) as executor:
            futures = [
                executor.submit(
                    evaluator.evaluate,
                    query=query,
                    retrieved_ids=retrieved_ids,
                    golden_ids=golden_ids,
                    trace=trace,
                )
                for evaluator in self.evaluators
            ]

        merged: dict[str, float] = {}
        for evaluator, future in zip(self.evaluators, futures, strict=True):
            metrics = future.result()
            if not isinstance(metrics, dict):
                raise TypeError(f"{type(evaluator).__name__}.evaluate() must return a dict")
            self._merge_metrics(merged, evaluator, metrics)
        return merged

    @staticmethod
    def _merge_metrics(
        target: dict[str, float],
        evaluator: BaseEvaluator,
        metrics: dict[str, Any],
    ) -> None:
        prefix = _metric_prefix(evaluator)
        for name, value in metrics.items():
            if not isinstance(name, str) or not name.strip():
                raise ValueError("metric names must be non-empty strings")
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(f"metric {name} must be numeric")

            key = name.strip()
            if key in target:
                key = f"{prefix}.{key}"
            key = _unique_metric_key(target, key)
            target[key] = float(value)


def _metric_prefix(evaluator: BaseEvaluator) -> str:
    name = type(evaluator).__name__
    if name.endswith("Evaluator"):
        name = name[: -len("Evaluator")]
    normalized = []
    for index, char in enumerate(name):
        if char.isupper() and index > 0:
            normalized.append("_")
        normalized.append(char.lower())
    return "".join(normalized) or "evaluator"


def _unique_metric_key(target: dict[str, float], key: str) -> str:
    if key not in target:
        return key

    suffix = 2
    while f"{key}.{suffix}" in target:
        suffix += 1
    return f"{key}.{suffix}"
