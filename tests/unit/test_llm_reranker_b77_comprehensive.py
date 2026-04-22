"""Comprehensive edge-case tests for B7.7 LLM reranker behavior."""

from __future__ import annotations

from typing import Any

import pytest

from libs.llm.base_llm import BaseLLM, ChatMessage
from libs.reranker.llm_reranker import LLMReranker
from libs.reranker.reranker_factory import RerankerFactory


class FixedReplyLLM(BaseLLM):
    """Minimal deterministic LLM fake for reranker tests."""

    def __init__(self, reply: str) -> None:
        super().__init__(model="fixed")
        self.reply = reply

    def chat(self, messages: list[ChatMessage]) -> str:
        self.validate_messages(messages)
        return self.reply


@pytest.mark.unit
def test_b77_preserve_candidates_with_missing_or_blank_id() -> None:
    reranker = LLMReranker(llm=FixedReplyLLM('{"ranked_ids": ["doc-2"]}'))
    candidates = [
        {"id": "", "text": "blank-id"},
        {"text": "missing-id"},
        {"id": "doc-2", "text": "matched"},
    ]

    ranked = reranker.rerank(query="q", candidates=candidates)

    assert len(ranked) == 3
    assert [item.get("text") for item in ranked] == ["matched", "blank-id", "missing-id"]


@pytest.mark.unit
def test_b77_preserve_duplicate_candidate_ids() -> None:
    reranker = LLMReranker(llm=FixedReplyLLM('{"ranked_ids": ["dup"]}'))
    candidates = [
        {"id": "dup", "text": "first-dup"},
        {"id": "dup", "text": "second-dup"},
        {"id": "other", "text": "other"},
    ]

    ranked = reranker.rerank(query="q", candidates=candidates)

    assert len(ranked) == 3
    assert [item["text"] for item in ranked] == ["first-dup", "second-dup", "other"]


@pytest.mark.unit
def test_b77_factory_rejects_non_mapping_llm_settings() -> None:
    with pytest.raises(TypeError, match="rerank.llm_settings"):
        RerankerFactory.create(
            {"rerank": {"provider": "llm", "llm_settings": "openai"}}
        )


@pytest.mark.unit
def test_b77_factory_rejects_non_mapping_rerank_llm_alias() -> None:
    with pytest.raises(TypeError, match="rerank.llm"):
        RerankerFactory.create({"rerank": {"provider": "llm", "llm": 123}})


@pytest.mark.unit
def test_b77_factory_prefers_rerank_llm_over_top_level_llm() -> None:
    reranker = RerankerFactory.create(
        {
            "llm": {"provider": "azure", "model": "gpt-4o-mini"},
            "rerank": {
                "provider": "llm",
                "llm": {"provider": "deepseek", "model": "deepseek-chat"},
            },
        }
    )

    assert reranker.llm_settings["provider"] == "deepseek"


@pytest.mark.unit
def test_b77_invalid_non_object_response_is_rejected() -> None:
    reranker = LLMReranker(llm=FixedReplyLLM('["doc-1"]'))

    with pytest.raises(ValueError, match="JSON object"):
        reranker.rerank(query="q", candidates=[{"id": "doc-1", "text": "a"}])


@pytest.mark.unit
def test_b77_ranked_ids_with_duplicates_do_not_duplicate_output() -> None:
    reranker = LLMReranker(llm=FixedReplyLLM('{"ranked_ids": ["doc-1", "doc-1"]}'))
    candidates = [
        {"id": "doc-1", "text": "first"},
        {"id": "doc-2", "text": "second"},
    ]

    ranked = reranker.rerank(query="q", candidates=candidates)

    assert len(ranked) == 2
    assert [item["id"] for item in ranked] == ["doc-1", "doc-2"]


@pytest.mark.unit
def test_b77_unknown_ranked_id_does_not_drop_candidates() -> None:
    reranker = LLMReranker(llm=FixedReplyLLM('{"ranked_ids": ["unknown"]}'))
    candidates = [
        {"id": "doc-1", "text": "first"},
        {"id": "doc-2", "text": "second"},
    ]

    ranked = reranker.rerank(query="q", candidates=candidates)

    assert len(ranked) == 2
    assert [item["id"] for item in ranked] == ["doc-1", "doc-2"]


@pytest.mark.unit
def test_b77_rerank_returns_copied_candidate_dicts() -> None:
    reranker = LLMReranker(llm=FixedReplyLLM('{"ranked_ids": ["doc-2"]}'))
    candidates = [
        {"id": "doc-1", "text": "first"},
        {"id": "doc-2", "text": "second"},
    ]

    ranked = reranker.rerank(query="q", candidates=candidates)
    ranked[0]["text"] = "changed-in-ranked"

    assert candidates[1]["text"] == "second"
