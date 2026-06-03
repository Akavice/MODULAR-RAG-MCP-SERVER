"""Run golden-set evaluation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run retrieval evaluation.")
    parser.add_argument("--config", default="config/settings.yaml", help="Settings YAML path.")
    parser.add_argument(
        "--test-set",
        default="tests/fixtures/golden_test_set.json",
        help="Golden test set JSON path.",
    )
    parser.add_argument("--top-k", type=int, default=None, help="Override retrieval top_k.")
    parser.add_argument(
        "--live",
        action="store_true",
        help="Use real HybridSearch from settings. Default uses dry-run empty retrieval.",
    )
    args = parser.parse_args(argv)

    _ensure_src_on_path()

    from core.query_engine.hybrid_search import HybridSearch
    from core.settings import load_settings
    from libs.evaluator.evaluator_factory import EvaluatorFactory
    from observability.evaluation.eval_runner import EvalRunner

    try:
        settings = load_settings(args.config)
        evaluator = EvaluatorFactory.create(settings)
        hybrid_search: Any = HybridSearch(settings) if args.live else _DryRunHybridSearch()
        report = EvalRunner(
            settings=settings,
            hybrid_search=hybrid_search,
            evaluator=evaluator,
            top_k=args.top_k,
        ).run(args.test_set)
    except Exception as exc:
        print(f"Evaluation failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    return 0


class _DryRunHybridSearch:
    def search(
        self,
        query: str,
        top_k: int | None = None,
        filters: dict[str, Any] | None = None,
    ) -> list[Any]:
        _ = query, top_k, filters
        return []


def _ensure_src_on_path() -> None:
    root = Path(__file__).resolve().parents[1]
    src = str(root / "src")
    if src not in sys.path:
        sys.path.insert(0, src)


if __name__ == "__main__":
    raise SystemExit(main())
