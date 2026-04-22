"""Unit tests for reranker factory routing and fallback behavior."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from libs.reranker.base_reranker import BaseReranker, RerankCandidate
from libs.reranker.llm_reranker import LLMReranker
from libs.reranker.reranker_factory import NoneReranker, RerankerFactory


class FakeReranker(BaseReranker):
    """Simple deterministic reranker used in factory tests."""

    def rerank(
        self,
        query: str,
        candidates: list[dict[str, Any]],
        trace: Any | None = None,
    ) -> list[RerankCandidate]:
        self.validate_inputs(query=query, candidates=candidates)
        return sorted(
            (dict(candidate) for candidate in candidates),
            key=lambda item: str(item.get("id", "")),
        )


@dataclass(slots=True)
class FakeSettings:
    """Minimal settings object exposing `.rerank` mapping."""

    rerank: dict[str, Any]


@pytest.fixture(autouse=True)
def reset_reranker_registry() -> None:
    """Ensure tests do not leak registered providers across cases."""
    RerankerFactory.clear_registry()
    yield
    RerankerFactory.clear_registry()


@pytest.mark.unit
def test_create_with_none_provider_returns_none_reranker() -> None:
    reranker = RerankerFactory.create({"rerank": {"provider": "none"}})

    assert isinstance(reranker, NoneReranker)


@pytest.mark.unit
def test_create_with_llm_provider_returns_llm_reranker() -> None:
    reranker = RerankerFactory.create(
        {
            "rerank": {
                "provider": "llm",
                "llm_settings": {"provider": "openai", "model": "gpt-4o-mini"},
            }
        }
    )

    assert isinstance(reranker, LLMReranker)
    assert reranker.llm_settings["provider"] == "openai"


@pytest.mark.unit
def test_create_with_llm_provider_injects_top_level_llm_settings() -> None:
    reranker = RerankerFactory.create(
        {
            "llm": {"provider": "azure", "model": "gpt-4o-mini"},
            "rerank": {"provider": "llm"},
        }
    )

    assert isinstance(reranker, LLMReranker)
    assert reranker.llm_settings["provider"] == "azure"


@pytest.mark.unit
def test_none_reranker_preserves_candidate_order() -> None:
    reranker = RerankerFactory.create({"rerank": {"provider": "none"}})
    candidates = [{"id": "b"}, {"id": "a"}, {"id": "c"}]

    ranked = reranker.rerank(query="test", candidates=candidates)

    assert [item["id"] for item in ranked] == ["b", "a", "c"]


@pytest.mark.unit
def test_create_routes_by_registered_provider() -> None:
    RerankerFactory.register("fake", FakeReranker)

    reranker = RerankerFactory.create({"rerank": {"provider": "fake", "alpha": 0.3}})

    assert isinstance(reranker, FakeReranker)
    assert reranker.options["alpha"] == 0.3


@pytest.mark.unit
def test_create_accepts_object_settings() -> None:
    RerankerFactory.register("fake", FakeReranker)
    settings = FakeSettings(rerank={"provider": "fake"})

    reranker = RerankerFactory.create(settings)

    assert isinstance(reranker, FakeReranker)


@pytest.mark.unit
def test_create_raises_for_missing_provider() -> None:
    with pytest.raises(ValueError, match="rerank.provider"):
        RerankerFactory.create({"rerank": {}})


@pytest.mark.unit
def test_create_raises_for_unknown_provider() -> None:
    with pytest.raises(ValueError, match="Unsupported rerank provider"):
        RerankerFactory.create({"rerank": {"provider": "unknown"}})


@pytest.mark.unit
def test_register_rejects_duplicate_provider_without_overwrite() -> None:
    RerankerFactory.register("fake", FakeReranker)

    with pytest.raises(ValueError, match="already registered"):
        RerankerFactory.register("fake", FakeReranker)
