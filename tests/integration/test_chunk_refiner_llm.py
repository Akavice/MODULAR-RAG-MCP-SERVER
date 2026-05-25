"""Integration tests for ChunkRefiner with real LLM providers."""

from __future__ import annotations

import os

import pytest

from core.trace.trace_context import TraceContext
from core.types import Chunk
from ingestion.transform.chunk_refiner import ChunkRefiner


def _build_openai_settings(*, model: str) -> dict[str, object]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY is required for real LLM integration test")

    return {
        "llm": {
            "provider": "openai",
            "model": model,
            "api_key": api_key,
        },
        "ingestion": {
            "chunk_refiner": {
                "use_llm": True,
            }
        },
    }


def _chunk(text: str) -> Chunk:
    return Chunk(
        id="c1",
        text=text,
        metadata={"source_path": "docs/integration.pdf"},
        start_offset=0,
        end_offset=len(text),
        source_ref="doc-i",
    )


@pytest.mark.integration
def test_chunk_refiner_real_llm_refine_succeeds() -> None:
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    settings = _build_openai_settings(model=model)
    refiner = ChunkRefiner(settings=settings)
    trace = TraceContext()

    output = refiner.transform([_chunk("Page 1 of 3\nhello     world\n---")], trace=trace)

    assert len(output) == 1
    assert isinstance(output[0].text, str)
    assert output[0].text.strip()
    assert output[0].metadata["refined_by"] in {"llm", "rule"}
    assert trace.stages


@pytest.mark.integration
def test_chunk_refiner_real_llm_invalid_model_fallbacks_to_rule() -> None:
    settings = _build_openai_settings(model="non-existent-model-for-fallback-check")
    refiner = ChunkRefiner(settings=settings)

    output = refiner.transform([_chunk("A    B")])

    assert output[0].metadata["refined_by"] == "rule"
    assert "llm_" in output[0].metadata.get("refine_fallback_reason", "")
    assert output[0].text == "A B"
