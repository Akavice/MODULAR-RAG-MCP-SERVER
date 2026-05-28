"""Build MCP tool response payloads from retrieval results."""

from __future__ import annotations

from typing import Any

from core.response.citation_generator import CitationGenerator
from core.types import RetrievalResult


class ResponseBuilder:
    """Render MCP content + structuredContent payload."""

    def __init__(self, citation_generator: CitationGenerator | None = None) -> None:
        self.citation_generator = citation_generator or CitationGenerator()

    def build(
        self,
        retrieval_results: list[RetrievalResult],
        *,
        query: str,
    ) -> dict[str, Any]:
        if not retrieval_results:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"No results found for query: {query}",
                    }
                ],
                "structuredContent": {
                    "query": query,
                    "results": [],
                    "citations": [],
                },
            }

        citations = self.citation_generator.generate(retrieval_results)
        lines: list[str] = []
        rows: list[dict[str, Any]] = []
        for index, (item, citation) in enumerate(zip(retrieval_results, citations), start=1):
            source = citation.get("source", "")
            score = citation.get("score", 0.0)
            text = item.text.replace("\n", " ").strip()
            lines.append(f"[{index}] {text} (source: {source}, score: {score:.6f})")
            rows.append(
                {
                    "chunk_id": item.chunk_id,
                    "score": float(item.score),
                    "text": item.text,
                    "metadata": dict(item.metadata),
                }
            )

        markdown = "\n\n".join(lines)
        return {
            "content": [{"type": "text", "text": markdown}],
            "structuredContent": {
                "query": query,
                "results": rows,
                "citations": citations,
            },
        }
