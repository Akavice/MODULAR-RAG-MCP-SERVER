"""Citation generation for MCP tool responses."""

from __future__ import annotations

from typing import Any

from core.types import RetrievalResult


class CitationGenerator:
    """Generate structured citations from retrieval results."""

    def generate(self, retrieval_results: list[RetrievalResult]) -> list[dict[str, Any]]:
        citations: list[dict[str, Any]] = []
        for item in retrieval_results:
            metadata = dict(item.metadata)
            citations.append(
                {
                    "source": str(metadata.get("source_path", "")),
                    "page": metadata.get("page", metadata.get("page_num")),
                    "chunk_id": item.chunk_id,
                    "score": float(item.score),
                }
            )
        return citations
