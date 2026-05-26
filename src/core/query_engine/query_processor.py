"""Query preprocessing for keyword extraction and lightweight filter parsing."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


_TOKEN_PATTERN = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_-]*")
_FILTER_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_-])(?P<key>collection|doc_type|language|access_level|from|to)"
    r"\s*:\s*(?P<value>[^\s]+)",
    flags=re.IGNORECASE,
)
_STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "with",
}
_ALIAS_TO_FILTER_KEY = {
    "collection": "collection",
    "doc_type": "doc_type",
    "language": "language",
    "access_level": "access_level",
}


@dataclass(slots=True)
class ProcessedQuery:
    """Canonical query payload passed to downstream retrievers."""

    query: str
    keywords: list[str]
    filters: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "keywords": list(self.keywords),
            "filters": dict(self.filters),
        }


class QueryProcessor:
    """Parse a query string into retrieval keywords and generic filters."""

    def __init__(self, settings: Any) -> None:
        self.settings = settings

    def process(
        self,
        query: str,
        filters: dict[str, Any] | None = None,
    ) -> ProcessedQuery:
        normalized_query = self._normalize_query(query)
        extracted_filters, residual_text = self._extract_filters(normalized_query)
        merged_filters = self._merge_filters(
            query_filters=extracted_filters,
            provided_filters=filters,
        )
        keywords = self._extract_keywords(residual_text)
        if not keywords:
            # Ensure downstream retrieval always has at least one query signal.
            keywords = [normalized_query.lower()]
        return ProcessedQuery(
            query=normalized_query,
            keywords=keywords,
            filters=merged_filters,
        )

    @staticmethod
    def _normalize_query(query: Any) -> str:
        if not isinstance(query, str):
            raise TypeError("query must be a string")
        normalized = query.strip()
        if not normalized:
            raise ValueError("query must not be empty")
        return normalized

    @staticmethod
    def _extract_filters(query: str) -> tuple[dict[str, Any], str]:
        filters: dict[str, Any] = {}
        time_range: dict[str, str] = {}

        def replace_match(match: re.Match[str]) -> str:
            key_raw = match.group("key").strip().lower()
            value = match.group("value").strip()
            if not value:
                return " "

            if key_raw in ("from", "to"):
                time_range[key_raw] = value
            else:
                filter_key = _ALIAS_TO_FILTER_KEY[key_raw]
                filters[filter_key] = value
            return " "

        residual = _FILTER_PATTERN.sub(replace_match, query)
        if time_range:
            filters["time_range"] = dict(time_range)
        return filters, residual

    @staticmethod
    def _merge_filters(
        *,
        query_filters: dict[str, Any],
        provided_filters: dict[str, Any] | None,
    ) -> dict[str, Any]:
        if provided_filters is None:
            return dict(query_filters)
        if not isinstance(provided_filters, dict):
            raise TypeError("filters must be a mapping when provided")

        merged = dict(query_filters)
        for key, value in provided_filters.items():
            if not isinstance(key, str) or not key.strip():
                raise ValueError("filters keys must be non-empty strings")
            merged[key.strip()] = value
        return merged

    @staticmethod
    def _extract_keywords(text: str) -> list[str]:
        keywords: list[str] = []
        seen: set[str] = set()

        for token in _TOKEN_PATTERN.findall(text.lower()):
            if token in _STOP_WORDS:
                continue
            if token in seen:
                continue
            seen.add(token)
            keywords.append(token)
        return keywords
