"""Unit tests for query preprocessing behavior."""

from __future__ import annotations

import pytest

from core.query_engine.query_processor import ProcessedQuery, QueryProcessor


@pytest.mark.unit
def test_process_extracts_keywords_and_filters() -> None:
    processor = QueryProcessor(settings={})

    result = processor.process(
        "collection:kb doc_type:pdf language:en how to tune rag retrieval",
    )

    assert isinstance(result, ProcessedQuery)
    assert result.filters["collection"] == "kb"
    assert result.filters["doc_type"] == "pdf"
    assert result.filters["language"] == "en"
    assert "rag" in result.keywords
    assert "retrieval" in result.keywords


@pytest.mark.unit
def test_process_parses_time_range_and_merges_explicit_filters() -> None:
    processor = QueryProcessor(settings={})

    result = processor.process(
        "from:2024-01-01 to:2024-12-31 policy changes",
        filters={"collection": "legal", "access_level": "internal"},
    )

    assert result.filters["time_range"] == {
        "from": "2024-01-01",
        "to": "2024-12-31",
    }
    assert result.filters["collection"] == "legal"
    assert result.filters["access_level"] == "internal"


@pytest.mark.unit
def test_process_keywords_never_empty_for_valid_query() -> None:
    processor = QueryProcessor(settings={})

    result = processor.process("the and of")

    assert result.keywords
    assert result.keywords[0] == "the and of"


@pytest.mark.unit
def test_process_rejects_invalid_query_input() -> None:
    processor = QueryProcessor(settings={})

    with pytest.raises(TypeError, match="query must be a string"):
        processor.process(123)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="query must not be empty"):
        processor.process("   ")


@pytest.mark.unit
def test_process_rejects_invalid_filters_argument() -> None:
    processor = QueryProcessor(settings={})

    with pytest.raises(TypeError, match="filters must be a mapping"):
        processor.process("rag query", filters="collection:kb")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="filters keys must be non-empty strings"):
        processor.process("rag query", filters={"": "x"})
