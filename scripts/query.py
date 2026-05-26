"""CLI entrypoint for online query workflow."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from typing import Any

from core.query_engine.hybrid_search import HybridSearch
from core.query_engine.reranker import Reranker
from core.settings import SettingsError, load_settings
from core.trace.trace_context import TraceContext
from core.types import RetrievalResult


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Query local knowledge index.")
    parser.add_argument("--query", required=True, help="Query text")
    parser.add_argument("--top-k", type=int, default=10, help="Top-K results (default: 10)")
    parser.add_argument("--collection", default=None, help="Optional collection filter")
    parser.add_argument("--verbose", action="store_true", help="Print stage-level trace payloads")
    parser.add_argument("--no-rerank", action="store_true", help="Skip rerank stage")
    parser.add_argument(
        "--config",
        default="config/settings.yaml",
        help="Settings file path (default: config/settings.yaml)",
    )
    return parser


def _format_result_line(index: int, item: RetrievalResult) -> str:
    source = str(item.metadata.get("source_path", ""))
    page = item.metadata.get("page", item.metadata.get("page_num"))
    page_display = f" page={page}" if page is not None else ""
    text = item.text.replace("\n", " ").strip()
    if len(text) > 120:
        text = f"{text[:120].rstrip()}..."
    return (
        f"[{index}] score={item.score:.6f} id={item.chunk_id}{page_display} "
        f"source={source} text={text}"
    )


def _print_results(results: list[RetrievalResult]) -> None:
    if not results:
        print("[query] no results")
        return
    print(f"[query] results={len(results)}")
    for index, item in enumerate(results, start=1):
        print(_format_result_line(index, item))


def _print_verbose_trace(trace: TraceContext) -> None:
    print("[query][verbose] trace stages:")
    for entry in trace.stages:
        stage = entry.get("stage", "")
        payload = {k: v for k, v in entry.items() if k not in {"stage", "timestamp"}}
        print(f"- stage={stage} payload={payload}")


def _normalize_collection(value: str | None) -> str | None:
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    return text


def _build_filters(collection: str | None) -> dict[str, Any] | None:
    if collection is None:
        return None
    return {"collection": collection}


def main(argv: Sequence[str] | None = None) -> int:
    """Parse args, execute query pipeline, and return process exit code."""
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.top_k <= 0:
        print("[query] argument error: --top-k must be greater than 0")
        return 1

    collection = _normalize_collection(args.collection)
    filters = _build_filters(collection)

    try:
        settings = load_settings(args.config)
    except SettingsError as exc:
        print(f"[query] configuration error: {exc}")
        return 1

    trace = TraceContext(trace_type="query")
    search = HybridSearch(settings)
    reranker = Reranker(settings)
    try:
        fused_results = search.search(
            args.query,
            top_k=args.top_k,
            filters=filters,
            trace=trace,
        )
        final_results = (
            fused_results
            if args.no_rerank
            else reranker.rerank(args.query, fused_results, trace=trace)
        )
    except Exception as exc:
        print(f"[query] query failed: {exc}")
        return 2

    _print_results(final_results[: args.top_k])
    if args.verbose:
        _print_verbose_trace(trace)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
