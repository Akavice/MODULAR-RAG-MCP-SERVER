"""Unit tests for LLMReranker behavior and schema contract."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from libs.llm.base_llm import BaseLLM, ChatMessage
from libs.reranker.llm_reranker import LLMReranker


class StaticResponseLLM(BaseLLM):
    """Fake LLM that returns a predefined response and captures messages."""

    def __init__(
        self,
        *,
        response_text: str,
        capture: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(model="fake-llm")
        self.response_text = response_text
        self.capture = capture

    def chat(self, messages: list[ChatMessage]) -> str:
        self.validate_messages(messages)
        if self.capture is not None:
            self.capture["messages"] = list(messages)
        return self.response_text


@pytest.mark.unit
def test_rerank_reorders_by_ranked_ids_and_keeps_remaining_order() -> None:
    llm = StaticResponseLLM(response_text='{"ranked_ids":["c2","c1"]}')
    reranker = LLMReranker(llm=llm)
    candidates = [
        {"id": "c1", "text": "first"},
        {"id": "c2", "text": "second"},
        {"id": "c3", "text": "third"},
    ]

    ranked = reranker.rerank(query="test query", candidates=candidates)

    assert [item["id"] for item in ranked] == ["c2", "c1", "c3"]


@pytest.mark.unit
def test_rerank_reads_prompt_from_file(tmp_path: Path) -> None:
    prompt_file = tmp_path / "rerank.txt"
    prompt_file.write_text("CUSTOM RERANK PROMPT", encoding="utf-8")
    captured: dict[str, Any] = {}
    llm = StaticResponseLLM(
        response_text='{"ranked_ids":["doc-1"]}',
        capture=captured,
    )
    reranker = LLMReranker(llm=llm, prompt_path=str(prompt_file))

    reranker.rerank(
        query="where is the answer",
        candidates=[{"id": "doc-1", "text": "answer"}],
    )

    sent_prompt = str(captured["messages"][-1]["content"])
    assert "CUSTOM RERANK PROMPT" in sent_prompt
    assert "Query:\nwhere is the answer" in sent_prompt
    assert "- id=doc-1 text=answer" in sent_prompt


@pytest.mark.unit
def test_rerank_accepts_json_object_extracted_from_wrapped_text() -> None:
    llm = StaticResponseLLM(
        response_text='result:\n{"ranked_ids":["c1"]}\nthanks',
    )
    reranker = LLMReranker(llm=llm)

    ranked = reranker.rerank(
        query="test query",
        candidates=[{"id": "c1", "text": "first"}, {"id": "c2", "text": "second"}],
    )

    assert [item["id"] for item in ranked] == ["c1", "c2"]


@pytest.mark.unit
def test_rerank_raises_readable_error_for_invalid_schema() -> None:
    llm = StaticResponseLLM(response_text='{"ids":["c1"]}')
    reranker = LLMReranker(llm=llm)

    with pytest.raises(ValueError, match="ranked_ids"):
        reranker.rerank(
            query="test query",
            candidates=[{"id": "c1", "text": "first"}],
        )


@pytest.mark.unit
def test_rerank_preserves_candidates_with_blank_or_missing_id() -> None:
    llm = StaticResponseLLM(response_text='{"ranked_ids":["doc-2"]}')
    reranker = LLMReranker(llm=llm)
    candidates = [
        {"id": "", "text": "blank-id"},
        {"text": "missing-id"},
        {"id": "doc-2", "text": "matched"},
    ]

    ranked = reranker.rerank(query="test query", candidates=candidates)

    assert len(ranked) == 3
    assert [item.get("text") for item in ranked] == ["matched", "blank-id", "missing-id"]


@pytest.mark.unit
def test_rerank_preserves_duplicate_ids_without_dropping() -> None:
    llm = StaticResponseLLM(response_text='{"ranked_ids":["dup"]}')
    reranker = LLMReranker(llm=llm)
    candidates = [
        {"id": "dup", "text": "first-dup"},
        {"id": "dup", "text": "second-dup"},
        {"id": "other", "text": "other"},
    ]

    ranked = reranker.rerank(query="test query", candidates=candidates)

    assert len(ranked) == 3
    assert [item["text"] for item in ranked] == ["first-dup", "second-dup", "other"]
