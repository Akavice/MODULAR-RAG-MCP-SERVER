"""CLI entrypoint for offline ingestion workflow."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from core.settings import SettingsError, load_settings
from ingestion.pipeline import IngestionPipeline, IngestionPipelineStageError, IngestionResult


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run offline ingestion for one PDF file.")
    parser.add_argument("--path", required=True, help="Source PDF path to ingest")
    parser.add_argument(
        "--collection",
        default="default",
        help="Target collection name (default: default)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-ingestion even when file hash already exists",
    )
    parser.add_argument(
        "--config",
        default="config/settings.yaml",
        help="Settings file path (default: config/settings.yaml)",
    )
    return parser


def _print_result(result: IngestionResult) -> None:
    if result.status == "skipped":
        print(
            "[ingest] status=skipped"
            f" collection={result.collection}"
            f" reason={result.reason or 'already_ingested'}"
            f" file_hash={result.file_hash}"
        )
        return

    print(
        "[ingest] status=ingested"
        f" collection={result.collection}"
        f" chunks={result.chunk_count}"
        f" records={result.record_count}"
        f" vector_upserted={result.vector_upserted}"
        f" bm25_upserted={result.bm25_upserted}"
        f" images_saved={result.image_saved_count}"
        f" trace_id={result.trace_id or ''}"
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Parse args, execute ingestion pipeline, and return process exit code."""
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        settings = load_settings(args.config)
    except SettingsError as exc:
        print(f"[ingest] configuration error: {exc}")
        return 1

    pipeline = IngestionPipeline(settings)
    try:
        result = pipeline.run(
            args.path,
            collection=args.collection,
            force=bool(args.force),
        )
    except IngestionPipelineStageError as exc:
        print(f"[ingest] pipeline failed at stage={exc.stage}: {exc.cause}")
        return 2
    except Exception as exc:
        print(f"[ingest] pipeline failed: {exc}")
        return 2

    _print_result(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
