"""Lightweight evaluator with deterministic retrieval metrics."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from libs.evaluator.base_evaluator import BaseEvaluator


class CustomEvaluator(BaseEvaluator):
    """Minimal evaluator that reports hit_rate and mrr."""

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

        golden_set = {item for item in golden_ids if item}
        if not golden_set:
            return {"hit_rate": 0.0, "mrr": 0.0}

        reciprocal_rank = 0.0
        for index, doc_id in enumerate(retrieved_ids, start=1):
            if doc_id in golden_set:
                reciprocal_rank = 1.0 / float(index)
                break

        hit_rate = 1.0 if reciprocal_rank > 0.0 else 0.0
        return {"hit_rate": hit_rate, "mrr": reciprocal_rank}
