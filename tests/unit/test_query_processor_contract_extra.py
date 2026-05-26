"""Additional contract tests for QueryProcessor edge behavior."""

from __future__ import annotations

import pytest

from core.query_engine.query_processor import QueryProcessor


@pytest.mark.unit
def test_explicit_filters_override_inline_filters() -> None:
    processor = QueryProcessor(settings={})

    result = processor.process(
        "collection:kb doc_type:pdf rag retrieval",
        filters={"collection": "legal"},
    )

    assert result.filters["collection"] == "legal"
    assert result.filters["doc_type"] == "pdf"


@pytest.mark.unit
def test_filter_prefix_inside_word_must_not_be_parsed_as_filter() -> None:
    processor = QueryProcessor(settings={})

    result = processor.process("mycollection:kb rag")

    assert "collection" not in result.filters
    assert "mycollection" in result.keywords


@pytest.mark.unit
def test_keywords_do_not_contain_inline_filter_values() -> None:
    processor = QueryProcessor(settings={})

    result = processor.process("collection:kb language:en rag retrieval")

    assert "kb" not in result.keywords
    assert "en" not in result.keywords
    assert "rag" in result.keywords
    assert "retrieval" in result.keywords
