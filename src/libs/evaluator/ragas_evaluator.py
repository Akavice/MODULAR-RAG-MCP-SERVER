"""Ragas-backed evaluator implementation."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any

from libs.evaluator.base_evaluator import BaseEvaluator


RAGAS_METRIC_NAMES = (
    "faithfulness",
    "answer_relevancy",
    "context_precision",
)


class RagasEvaluator(BaseEvaluator):
    """Evaluator adapter for the optional `ragas` package."""

    def __init__(
        self,
        *,
        ragas_evaluate: Callable[..., Any] | None = None,
        dataset_factory: Callable[..., Any] | None = None,
        metrics: Sequence[Any] | None = None,
        **options: Any,
    ) -> None:
        super().__init__(**options)
        self._ragas_evaluate = ragas_evaluate
        self._dataset_factory = dataset_factory
        self._metrics = list(metrics) if metrics is not None else None

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

        ragas_evaluate = self._ragas_evaluate
        dataset_factory = self._dataset_factory
        metrics = self._metrics
        if ragas_evaluate is None or dataset_factory is None or metrics is None:
            imported = self._load_ragas()
            ragas_evaluate = ragas_evaluate or imported["evaluate"]
            dataset_factory = dataset_factory or imported["dataset_factory"]
            metrics = metrics or imported["metrics"]

        sample = self._build_sample(query, retrieved_ids, golden_ids, trace)
        dataset = dataset_factory([sample])
        raw_result = ragas_evaluate(dataset, metrics=metrics)
        return self._normalize_metrics(raw_result)

    @staticmethod
    def _load_ragas() -> dict[str, Any]:
        try:
            from datasets import Dataset
            from ragas import evaluate
            from ragas.metrics import answer_relevancy, context_precision, faithfulness
        except ImportError as exc:
            raise ImportError(
                "RagasEvaluator requires optional dependencies `ragas` and "
                "`datasets`. Install them before using evaluation.provider=ragas."
            ) from exc

        return {
            "evaluate": evaluate,
            "dataset_factory": Dataset.from_list,
            "metrics": [faithfulness, answer_relevancy, context_precision],
        }

    @staticmethod
    def _build_sample(
        query: str,
        retrieved_ids: Sequence[str],
        golden_ids: Sequence[str],
        trace: Any | None,
    ) -> dict[str, Any]:
        trace_data = RagasEvaluator._trace_to_mapping(trace)
        answer = RagasEvaluator._first_string(
            trace_data,
            ("answer", "response", "output", "generated_answer"),
            default="",
        )
        contexts = RagasEvaluator._extract_contexts(trace_data, retrieved_ids)
        ground_truth = RagasEvaluator._extract_ground_truth(trace_data, golden_ids)

        return {
            "question": query,
            "answer": answer,
            "contexts": contexts,
            "ground_truth": ground_truth,
            "retrieved_ids": list(retrieved_ids),
            "golden_ids": list(golden_ids),
        }

    @staticmethod
    def _trace_to_mapping(trace: Any | None) -> Mapping[str, Any]:
        if isinstance(trace, Mapping):
            return trace
        if trace is not None and hasattr(trace, "to_dict"):
            value = trace.to_dict()
            if isinstance(value, Mapping):
                return value
        return {}

    @staticmethod
    def _first_string(
        values: Mapping[str, Any],
        keys: Sequence[str],
        *,
        default: str,
    ) -> str:
        for key in keys:
            value = values.get(key)
            if isinstance(value, str):
                return value
        return default

    @staticmethod
    def _extract_contexts(
        trace_data: Mapping[str, Any],
        retrieved_ids: Sequence[str],
    ) -> list[str]:
        raw_contexts = trace_data.get("contexts")
        if raw_contexts is None:
            raw_contexts = trace_data.get("retrieved_contexts")
        if isinstance(raw_contexts, Sequence) and not isinstance(raw_contexts, (str, bytes)):
            contexts = [str(item) for item in raw_contexts if item is not None]
            if contexts:
                return contexts
        return list(retrieved_ids)

    @staticmethod
    def _extract_ground_truth(
        trace_data: Mapping[str, Any],
        golden_ids: Sequence[str],
    ) -> str:
        raw_ground_truth = trace_data.get("ground_truth")
        if raw_ground_truth is None:
            raw_ground_truth = trace_data.get("reference")
        if isinstance(raw_ground_truth, str):
            return raw_ground_truth
        if isinstance(raw_ground_truth, Sequence) and not isinstance(raw_ground_truth, (str, bytes)):
            return "\n".join(str(item) for item in raw_ground_truth if item is not None)
        return "\n".join(golden_ids)

    @staticmethod
    def _normalize_metrics(raw_result: Any) -> dict[str, float]:
        if hasattr(raw_result, "to_pandas"):
            frame = raw_result.to_pandas()
            if hasattr(frame, "to_dict"):
                records = frame.to_dict("records")
                if records:
                    return RagasEvaluator._coerce_metric_mapping(records[0])

        if hasattr(raw_result, "to_dict"):
            value = raw_result.to_dict()
            if isinstance(value, Mapping):
                return RagasEvaluator._coerce_metric_mapping(value)

        if isinstance(raw_result, Mapping):
            return RagasEvaluator._coerce_metric_mapping(raw_result)

        raise TypeError("ragas evaluate result must be a mapping-like object")

    @staticmethod
    def _coerce_metric_mapping(values: Mapping[str, Any]) -> dict[str, float]:
        metrics: dict[str, float] = {}
        for name in RAGAS_METRIC_NAMES:
            if name not in values:
                continue
            value = values[name]
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(f"ragas metric {name} must be numeric")
            metrics[name] = float(value)
        if not metrics:
            raise ValueError("ragas evaluate result did not contain supported metrics")
        return metrics
