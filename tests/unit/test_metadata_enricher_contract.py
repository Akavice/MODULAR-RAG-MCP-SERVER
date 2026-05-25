"""Contract tests for MetadataEnricher."""

from __future__ import annotations

from typing import Any

import pytest

from core.types import Chunk
from ingestion.transform.metadata_enricher import MetadataEnricher
from libs.llm.base_llm import BaseLLM


class FixedReplyLLM(BaseLLM):
    def __init__(self, reply: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.reply = reply
        self.calls: list[list[dict[str, str]]] = []

    def chat(self, messages: Any) -> str:
        self.calls.append(list(messages))
        return self.reply


class RaisingLLM(BaseLLM):
    def chat(self, messages: Any) -> str:
        _ = messages
        raise RuntimeError("provider error")


class TraceStub:
    def __init__(self) -> None:
        self.events: list[tuple[str, dict[str, Any]]] = []

    def record_stage(self, stage: str, **payload: Any) -> None:
        self.events.append((stage, payload))


def _chunk(text: str, idx: int = 0) -> Chunk:
    return Chunk(
        id=f"chunk-{idx}",
        text=text,
        metadata={"source_path": "docs/a.pdf"},
        start_offset=0,
        end_offset=len(text),
        source_ref="doc-1",
    )


@pytest.mark.unit
def test_rule_mode_populates_title_summary_tags() -> None:
    enricher = MetadataEnricher(settings={"ingestion": {"metadata_enricher": {"use_llm": False}}})
    chunks = [_chunk("RAG architecture improves retrieval quality. It combines dense and sparse.")]

    out = enricher.transform(chunks)
    metadata = out[0].metadata

    assert isinstance(metadata.get("title"), str) and metadata["title"].strip()
    assert isinstance(metadata.get("summary"), str) and metadata["summary"].strip()
    assert isinstance(metadata.get("tags"), list) and metadata["tags"]
    assert metadata["metadata_enriched_by"] == "rule"


@pytest.mark.unit
def test_rule_mode_handles_blank_text() -> None:
    enricher = MetadataEnricher(settings={})
    out = enricher.transform([_chunk("   ")])
    metadata = out[0].metadata

    assert metadata["title"] == "Untitled chunk"
    assert metadata["summary"] == "No textual content available."
    assert metadata["tags"] == ["general"]


@pytest.mark.unit
def test_llm_mode_uses_llm_output_when_valid_json() -> None:
    llm = FixedReplyLLM('{"title":"T","summary":"S","tags":["rag","pipeline"]}')
    enricher = MetadataEnricher(
        settings={"ingestion": {"metadata_enricher": {"use_llm": True}}},
        llm=llm,
    )

    out = enricher.transform([_chunk("text")])
    metadata = out[0].metadata

    assert metadata["title"] == "T"
    assert metadata["summary"] == "S"
    assert metadata["tags"] == ["rag", "pipeline"]
    assert metadata["metadata_enriched_by"] == "llm"
    assert len(llm.calls) == 1


@pytest.mark.unit
def test_llm_mode_accepts_json_wrapped_text_response() -> None:
    llm = FixedReplyLLM(
        "Sure:\n```json\n{\"title\":\"A\",\"summary\":\"B\",\"tags\":[\"x\"]}\n```"
    )
    enricher = MetadataEnricher(
        settings={"ingestion": {"metadata_enricher": {"use_llm": True}}},
        llm=llm,
    )

    out = enricher.transform([_chunk("text")])

    assert out[0].metadata["title"] == "A"
    assert out[0].metadata["metadata_enriched_by"] == "llm"


@pytest.mark.unit
def test_llm_invalid_schema_falls_back_to_rule() -> None:
    llm = FixedReplyLLM('{"title":"","summary":"ok","tags":[]}')
    enricher = MetadataEnricher(
        settings={"ingestion": {"metadata_enricher": {"use_llm": True}}},
        llm=llm,
    )

    out = enricher.transform([_chunk("fallback text for tags")])
    metadata = out[0].metadata

    assert metadata["metadata_enriched_by"] == "rule"
    assert "llm_metadata_failed" in metadata["metadata_fallback_reason"]
    assert metadata["tags"]


@pytest.mark.unit
def test_llm_runtime_error_falls_back_without_raising() -> None:
    enricher = MetadataEnricher(
        settings={"ingestion": {"metadata_enricher": {"use_llm": True}}},
        llm=RaisingLLM(),
    )
    trace = TraceStub()

    out = enricher.transform([_chunk("fallback text")], trace=trace)

    assert out[0].metadata["metadata_enriched_by"] == "rule"
    assert "llm_metadata_failed" in out[0].metadata["metadata_fallback_reason"]
    assert any(stage == "transform_metadata_enricher_llm_error" for stage, _ in trace.events)


@pytest.mark.unit
def test_chunk_processing_error_is_isolated() -> None:
    enricher = MetadataEnricher(settings={})

    def broken_rule(_: str) -> dict[str, Any]:
        raise ValueError("broken rule")

    enricher._rule_based_metadata = broken_rule  # type: ignore[method-assign]
    out = enricher.transform([_chunk("a"), _chunk("b", idx=1)])

    assert len(out) == 2
    assert out[0].metadata["metadata_enriched_by"] == "rule"
    assert "chunk_processing_failed" in out[0].metadata["metadata_fallback_reason"]


@pytest.mark.unit
def test_trace_stage_reports_counts() -> None:
    llm = FixedReplyLLM('{"title":"A","summary":"B","tags":["x"]}')
    enricher = MetadataEnricher(
        settings={"ingestion": {"metadata_enricher": {"use_llm": True}}},
        llm=llm,
    )
    trace = TraceStub()

    enricher.transform([_chunk("one"), _chunk("two", idx=1)], trace=trace)
    stage, payload = trace.events[-1]

    assert stage == "transform_metadata_enricher"
    assert payload["chunk_count"] == 2
    assert payload["llm_enriched_count"] == 2
    assert payload["rule_enriched_count"] == 0


@pytest.mark.unit
def test_trace_fallback_count_not_double_counted_on_chunk_exception() -> None:
    enricher = MetadataEnricher(settings={})
    trace = TraceStub()

    def broken_rule(_: str) -> dict[str, Any]:
        raise ValueError("broken rule")

    enricher._rule_based_metadata = broken_rule  # type: ignore[method-assign]
    enricher.transform([_chunk("only")], trace=trace)
    stage, payload = trace.events[-1]

    assert stage == "transform_metadata_enricher"
    assert payload["chunk_count"] == 1
    assert payload["rule_enriched_count"] == 1
    assert payload["fallback_count"] == 1


@pytest.mark.unit
def test_preserves_chunk_identity_and_offsets() -> None:
    chunk = Chunk(
        id="c-1",
        text="Graph index tuning improves recall.",
        metadata={"source_path": "docs/a.pdf"},
        start_offset=5,
        end_offset=25,
        source_ref="doc-a",
    )
    enricher = MetadataEnricher(settings={})

    out = enricher.transform([chunk])[0]

    assert out.id == "c-1"
    assert out.start_offset == 5
    assert out.end_offset == 25
    assert out.source_ref == "doc-a"
