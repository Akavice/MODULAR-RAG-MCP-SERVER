"""Unit tests for ChunkRefiner transform behavior."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from core.types import Chunk
from ingestion.transform.base_transform import BaseTransform
from ingestion.transform.chunk_refiner import ChunkRefiner
from libs.llm.base_llm import BaseLLM


class DummyTransform(BaseTransform):
    def transform(self, chunks: list[Chunk], trace: Any | None = None) -> list[Chunk]:
        _ = trace
        self.validate_chunks(chunks)
        return chunks


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
        raise RuntimeError("boom")


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


def _load_noisy_fixture() -> dict[str, dict[str, str]]:
    path = Path("tests/fixtures/noisy_chunks.json")
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.unit
def test_base_transform_validate_chunks_rejects_non_list() -> None:
    transform = DummyTransform()

    with pytest.raises(TypeError, match="chunks must be a list"):
        transform.transform("bad")  # type: ignore[arg-type]


@pytest.mark.unit
def test_base_transform_validate_chunks_rejects_non_chunk_items() -> None:
    transform = DummyTransform()

    with pytest.raises(TypeError, match="must be a Chunk"):
        transform.transform([{"id": "x"}])  # type: ignore[list-item]


@pytest.mark.unit
def test_rule_based_refine_matches_fixture_examples() -> None:
    fixture = _load_noisy_fixture()
    refiner = ChunkRefiner(settings={})

    for scenario in fixture.values():
        assert refiner._rule_based_refine(scenario["input"]) == scenario["expected"]


@pytest.mark.unit
def test_transform_returns_empty_when_input_is_empty() -> None:
    refiner = ChunkRefiner(settings={"ingestion": {"chunk_refiner": {"use_llm": False}}})
    trace = TraceStub()

    output = refiner.transform([], trace=trace)

    assert output == []
    assert trace.events[0][0] == "transform_chunk_refiner"
    assert trace.events[0][1]["chunk_count"] == 0


@pytest.mark.unit
def test_transform_rule_mode_sets_refined_by_rule() -> None:
    refiner = ChunkRefiner(settings={"ingestion": {"chunk_refiner": {"use_llm": False}}})
    chunks = [_chunk("Page 1 of 3\nhello   world", idx=0)]

    output = refiner.transform(chunks)

    assert output[0].text == "hello world"
    assert output[0].metadata["refined_by"] == "rule"


@pytest.mark.unit
def test_transform_llm_mode_uses_llm_response_and_marks_metadata() -> None:
    llm = FixedReplyLLM("llm polished text")
    refiner = ChunkRefiner(
        settings={"ingestion": {"chunk_refiner": {"use_llm": True}}},
        llm=llm,
    )
    chunks = [_chunk("hello", idx=0)]

    output = refiner.transform(chunks)

    assert output[0].text == "llm polished text"
    assert output[0].metadata["refined_by"] == "llm"
    assert len(llm.calls) == 1


@pytest.mark.unit
def test_transform_llm_failure_falls_back_to_rule_and_sets_reason() -> None:
    refiner = ChunkRefiner(
        settings={"ingestion": {"chunk_refiner": {"use_llm": True}}},
        llm=RaisingLLM(),
    )
    chunks = [_chunk("A   B", idx=0)]
    trace = TraceStub()

    output = refiner.transform(chunks, trace=trace)

    assert output[0].text == "A B"
    assert output[0].metadata["refined_by"] == "rule"
    assert "llm_refine_failed" in output[0].metadata["refine_fallback_reason"]
    assert any(stage == "transform_chunk_refiner_llm_error" for stage, _ in trace.events)


@pytest.mark.unit
def test_transform_llm_empty_response_falls_back_to_rule() -> None:
    refiner = ChunkRefiner(
        settings={"ingestion": {"chunk_refiner": {"use_llm": True}}},
        llm=FixedReplyLLM("   "),
    )
    chunks = [_chunk("foo", idx=0)]

    output = refiner.transform(chunks)

    assert output[0].text == "foo"
    assert output[0].metadata["refined_by"] == "rule"
    assert output[0].metadata["refine_fallback_reason"] == "llm_response_empty"


@pytest.mark.unit
def test_transform_llm_init_failure_falls_back_without_crash() -> None:
    refiner = ChunkRefiner(
        settings={"ingestion": {"chunk_refiner": {"use_llm": True}}},
        llm=None,
    )
    chunks = [_chunk("foo", idx=0)]

    output = refiner.transform(chunks)

    assert output[0].text == "foo"
    assert output[0].metadata["refined_by"] == "rule"
    assert "llm_init_failed" in output[0].metadata["refine_fallback_reason"]


@pytest.mark.unit
def test_prompt_loader_falls_back_when_file_missing(tmp_path: Path) -> None:
    missing = tmp_path / "missing_prompt.txt"
    refiner = ChunkRefiner(settings={}, prompt_path=str(missing))

    rendered = refiner._render_prompt("abc")

    assert "abc" in rendered
    assert "Clean and refine the following text" in rendered


@pytest.mark.unit
def test_prompt_loader_uses_file_content_when_present(tmp_path: Path) -> None:
    prompt_file = tmp_path / "chunk_refine_prompt.txt"
    prompt_file.write_text("Rewrite:\n{text}", encoding="utf-8")
    llm = FixedReplyLLM("ok")
    refiner = ChunkRefiner(
        settings={"ingestion": {"chunk_refiner": {"use_llm": True}}},
        llm=llm,
        prompt_path=str(prompt_file),
    )

    refiner.transform([_chunk("raw text")])

    assert "Rewrite:\nraw text" in llm.calls[0][0]["content"]


@pytest.mark.unit
def test_prompt_without_placeholder_appends_text(tmp_path: Path) -> None:
    prompt_file = tmp_path / "chunk_refine_prompt.txt"
    prompt_file.write_text("Only clean this", encoding="utf-8")
    llm = FixedReplyLLM("ok")
    refiner = ChunkRefiner(
        settings={"ingestion": {"chunk_refiner": {"use_llm": True}}},
        llm=llm,
        prompt_path=str(prompt_file),
    )

    refiner.transform([_chunk("payload")])

    assert llm.calls[0][0]["content"].endswith("payload")


@pytest.mark.unit
def test_transform_preserves_chunk_offsets_and_source_ref() -> None:
    chunk = Chunk(
        id="c-1",
        text="A    B",
        metadata={"source_path": "docs/a.pdf"},
        start_offset=7,
        end_offset=20,
        source_ref="doc-x",
    )
    refiner = ChunkRefiner(settings={})

    output = refiner.transform([chunk])[0]

    assert output.start_offset == 7
    assert output.end_offset == 20
    assert output.source_ref == "doc-x"


@pytest.mark.unit
def test_transform_isolates_per_chunk_failures(monkeypatch: pytest.MonkeyPatch) -> None:
    refiner = ChunkRefiner(settings={})

    def flaky_rule(text: str) -> str:
        if text == "bad":
            raise ValueError("bad chunk")
        return text

    monkeypatch.setattr(refiner, "_rule_based_refine", flaky_rule)
    chunks = [_chunk("ok", idx=0), _chunk("bad", idx=1), _chunk("ok2", idx=2)]

    output = refiner.transform(chunks)

    assert [c.text for c in output] == ["ok", "bad", "ok2"]
    assert output[1].metadata["refined_by"] == "rule"
    assert "chunk_processing_failed" in output[1].metadata["refine_fallback_reason"]


@pytest.mark.unit
def test_trace_stage_contains_refine_counters() -> None:
    llm = FixedReplyLLM("llm")
    refiner = ChunkRefiner(
        settings={"ingestion": {"chunk_refiner": {"use_llm": True}}},
        llm=llm,
    )
    trace = TraceStub()
    chunks = [_chunk("a", idx=0), _chunk("b", idx=1)]

    refiner.transform(chunks, trace=trace)

    stage_name, payload = trace.events[-1]
    assert stage_name == "transform_chunk_refiner"
    assert payload["chunk_count"] == 2
    assert payload["llm_refined_count"] == 2
    assert payload["rule_refined_count"] == 0
