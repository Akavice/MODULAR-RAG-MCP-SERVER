"""Run golden-set retrieval evaluation."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from libs.evaluator.base_evaluator import BaseEvaluator


@dataclass(slots=True)
class EvalCase:
    query: str
    expected_chunk_ids: list[str]
    expected_sources: list[str]
    filters: dict[str, Any] | None = None


@dataclass(slots=True)
class EvalCaseResult:
    query: str
    expected_chunk_ids: list[str]
    expected_sources: list[str]
    retrieved_ids: list[str]
    retrieved_sources: list[str]
    metrics: dict[str, float]

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "expected_chunk_ids": list(self.expected_chunk_ids),
            "expected_sources": list(self.expected_sources),
            "retrieved_ids": list(self.retrieved_ids),
            "retrieved_sources": list(self.retrieved_sources),
            "metrics": dict(self.metrics),
        }


@dataclass(slots=True)
class EvalReport:
    metrics: dict[str, float]
    cases: list[EvalCaseResult]

    def to_dict(self) -> dict[str, Any]:
        return {
            "metrics": dict(self.metrics),
            "cases": [item.to_dict() for item in self.cases],
        }


class EvalRunner:
    """Run retrieval against a golden test set and aggregate evaluator metrics."""

    def __init__(
        self,
        settings: Any,
        hybrid_search: Any,
        evaluator: BaseEvaluator,
        *,
        top_k: int | None = None,
    ) -> None:
        self.settings = settings
        self.hybrid_search = hybrid_search
        if not isinstance(evaluator, BaseEvaluator):
            raise TypeError("evaluator must be a BaseEvaluator instance")
        self.evaluator = evaluator
        self.top_k = self._normalize_top_k(top_k) if top_k is not None else self._resolve_top_k(settings)

    def run(self, test_set_path: str | Path) -> EvalReport:
        cases = self._load_cases(test_set_path)
        results: list[EvalCaseResult] = []
        for case in cases:
            retrieved = self.hybrid_search.search(
                case.query,
                top_k=self.top_k,
                filters=case.filters,
            )
            retrieved_ids = [_extract_result_id(item, index) for index, item in enumerate(retrieved)]
            retrieved_sources = [_extract_source(item) for item in retrieved]
            evaluator_metrics = self.evaluator.evaluate(
                query=case.query,
                retrieved_ids=retrieved_ids,
                golden_ids=case.expected_chunk_ids or case.expected_sources,
                trace={
                    "contexts": [_extract_text(item) for item in retrieved],
                    "ground_truth": "\n".join(case.expected_chunk_ids or case.expected_sources),
                },
            )
            case_metrics = {
                "hit_rate": _hit_rate(
                    retrieved_ids=retrieved_ids,
                    retrieved_sources=retrieved_sources,
                    expected_ids=case.expected_chunk_ids,
                    expected_sources=case.expected_sources,
                ),
                "mrr": _mrr(
                    retrieved_ids=retrieved_ids,
                    retrieved_sources=retrieved_sources,
                    expected_ids=case.expected_chunk_ids,
                    expected_sources=case.expected_sources,
                ),
            }
            case_metrics.update(
                _coerce_metrics(
                    evaluator_metrics,
                    reserved_names=set(case_metrics),
                    prefix="evaluator",
                )
            )
            results.append(
                EvalCaseResult(
                    query=case.query,
                    expected_chunk_ids=case.expected_chunk_ids,
                    expected_sources=case.expected_sources,
                    retrieved_ids=retrieved_ids,
                    retrieved_sources=retrieved_sources,
                    metrics=case_metrics,
                )
            )

        return EvalReport(metrics=_aggregate_metrics(results), cases=results)

    @staticmethod
    def _load_cases(test_set_path: str | Path) -> list[EvalCase]:
        path = Path(test_set_path)
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, Mapping):
            raise TypeError("golden test set must be a JSON object")
        raw_cases = payload.get("test_cases")
        if not isinstance(raw_cases, list) or not raw_cases:
            raise ValueError("golden test set must contain non-empty test_cases")

        cases: list[EvalCase] = []
        for index, item in enumerate(raw_cases):
            if not isinstance(item, Mapping):
                raise TypeError(f"test_cases[{index}] must be a mapping")
            query = item.get("query")
            if not isinstance(query, str) or not query.strip():
                raise ValueError(f"test_cases[{index}].query must be a non-empty string")
            expected_chunk_ids = _string_list(item.get("expected_chunk_ids", []), f"test_cases[{index}].expected_chunk_ids")
            expected_sources = _string_list(item.get("expected_sources", []), f"test_cases[{index}].expected_sources")
            if not expected_chunk_ids and not expected_sources:
                raise ValueError(
                    f"test_cases[{index}] must define expected_chunk_ids or expected_sources"
                )
            filters = item.get("filters")
            if filters is not None and not isinstance(filters, Mapping):
                raise TypeError(f"test_cases[{index}].filters must be a mapping when provided")
            cases.append(
                EvalCase(
                    query=query.strip(),
                    expected_chunk_ids=expected_chunk_ids,
                    expected_sources=expected_sources,
                    filters=dict(filters) if isinstance(filters, Mapping) else None,
                )
            )
        return cases

    @staticmethod
    def _normalize_top_k(value: Any) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("top_k must be an integer")
        if value <= 0:
            raise ValueError("top_k must be greater than 0")
        return value

    @classmethod
    def _resolve_top_k(cls, settings: Any) -> int:
        retrieval = settings.get("retrieval") if isinstance(settings, Mapping) else getattr(settings, "retrieval", None)
        if isinstance(retrieval, Mapping) and "top_k" in retrieval:
            return cls._normalize_top_k(retrieval.get("top_k"))
        return 5


def _string_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise TypeError(f"{field_name} must be a list of strings")
    output: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str):
            raise TypeError(f"{field_name}[{index}] must be a string")
        normalized = item.strip()
        if normalized:
            output.append(normalized)
    return output


def _extract_result_id(item: Any, index: int) -> str:
    value = getattr(item, "chunk_id", None)
    if value is None and isinstance(item, Mapping):
        value = item.get("chunk_id") or item.get("id")
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"retrieval result at index {index} has invalid chunk_id")
    return value.strip()


def _extract_text(item: Any) -> str:
    value = getattr(item, "text", None)
    if value is None and isinstance(item, Mapping):
        value = item.get("text")
    return value if isinstance(value, str) else ""


def _extract_source(item: Any) -> str:
    metadata = getattr(item, "metadata", None)
    if metadata is None and isinstance(item, Mapping):
        metadata = item.get("metadata")
    if not isinstance(metadata, Mapping):
        return ""
    value = metadata.get("source_path") or metadata.get("source") or metadata.get("file_name")
    return value.strip() if isinstance(value, str) else ""


def _coerce_metrics(
    metrics: Any,
    *,
    reserved_names: set[str] | None = None,
    prefix: str = "metric",
) -> dict[str, float]:
    if not isinstance(metrics, Mapping):
        raise TypeError("evaluator.evaluate() must return a mapping")
    output: dict[str, float] = {}
    reserved = set(reserved_names or set())
    for name, value in metrics.items():
        if not isinstance(name, str) or not name.strip():
            raise ValueError("metric names must be non-empty strings")
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"metric {name} must be numeric")
        key = name.strip()
        if key in reserved:
            key = f"{prefix}.{key}"
        key = _unique_metric_key(reserved.union(output), key)
        output[key] = float(value)
    return output


def _unique_metric_key(existing: set[str], key: str) -> str:
    if key not in existing:
        return key
    suffix = 2
    while f"{key}.{suffix}" in existing:
        suffix += 1
    return f"{key}.{suffix}"


def _hit_rate(
    *,
    retrieved_ids: list[str],
    retrieved_sources: list[str],
    expected_ids: list[str],
    expected_sources: list[str],
) -> float:
    return 1.0 if _first_match_rank(retrieved_ids, retrieved_sources, expected_ids, expected_sources) else 0.0


def _mrr(
    *,
    retrieved_ids: list[str],
    retrieved_sources: list[str],
    expected_ids: list[str],
    expected_sources: list[str],
) -> float:
    rank = _first_match_rank(retrieved_ids, retrieved_sources, expected_ids, expected_sources)
    return 0.0 if rank is None else 1.0 / float(rank)


def _first_match_rank(
    retrieved_ids: list[str],
    retrieved_sources: list[str],
    expected_ids: list[str],
    expected_sources: list[str],
) -> int | None:
    expected_id_set = set(expected_ids)
    expected_source_set = {Path(item).name for item in expected_sources}
    for index, chunk_id in enumerate(retrieved_ids, start=1):
        if expected_id_set and chunk_id in expected_id_set:
            return index
        if expected_source_set:
            source_name = Path(retrieved_sources[index - 1]).name
            if source_name in expected_source_set:
                return index
    return None


def _aggregate_metrics(results: list[EvalCaseResult]) -> dict[str, float]:
    if not results:
        return {}
    totals: dict[str, float] = {}
    counts: dict[str, int] = {}
    for result in results:
        for name, value in result.metrics.items():
            totals[name] = totals.get(name, 0.0) + value
            counts[name] = counts.get(name, 0) + 1
    return {name: totals[name] / float(counts[name]) for name in sorted(totals)}
