"""Unit tests for embedding factory routing and validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from libs.embedding.base_embedding import BaseEmbedding
from libs.embedding.embedding_factory import EmbeddingFactory


class FakeEmbedding(BaseEmbedding):
    """Small fake embedding implementation used in factory tests."""

    def embed(self, texts: list[str], trace: Any | None = None) -> list[list[float]]:
        self.validate_texts(texts)
        return [[float(len(text))] for text in texts]


@dataclass(slots=True)
class FakeSettings:
    """Minimal settings object exposing `.embedding` mapping."""

    embedding: dict[str, Any]


@pytest.fixture(autouse=True)
def reset_embedding_registry() -> None:
    """Ensure tests do not leak registered providers across cases."""
    EmbeddingFactory.clear_registry()
    yield
    EmbeddingFactory.clear_registry()


@pytest.mark.unit
def test_create_routes_by_provider_from_nested_mapping() -> None:
    EmbeddingFactory.register("fake", FakeEmbedding)

    embedding = EmbeddingFactory.create(
        {"embedding": {"provider": "fake", "model": "fake-v1", "batch_size": 16}}
    )

    assert isinstance(embedding, FakeEmbedding)
    assert embedding.model == "fake-v1"
    assert embedding.options["batch_size"] == 16


@pytest.mark.unit
def test_create_accepts_direct_embedding_mapping() -> None:
    EmbeddingFactory.register("fake", FakeEmbedding)

    embedding = EmbeddingFactory.create({"provider": "fake", "model": "local"})

    assert isinstance(embedding, FakeEmbedding)
    assert embedding.model == "local"


@pytest.mark.unit
def test_create_accepts_object_settings() -> None:
    EmbeddingFactory.register("fake", FakeEmbedding)
    settings = FakeSettings(embedding={"provider": "fake", "model": "structured"})

    embedding = EmbeddingFactory.create(settings)

    assert isinstance(embedding, FakeEmbedding)
    assert embedding.model == "structured"


@pytest.mark.unit
def test_create_raises_for_missing_provider() -> None:
    EmbeddingFactory.register("fake", FakeEmbedding)

    with pytest.raises(ValueError, match="embedding.provider"):
        EmbeddingFactory.create({"embedding": {}})


@pytest.mark.unit
def test_create_raises_for_unregistered_provider() -> None:
    EmbeddingFactory.register("fake", FakeEmbedding)

    with pytest.raises(ValueError, match="Registered providers: fake"):
        EmbeddingFactory.create({"embedding": {"provider": "openai"}})


@pytest.mark.unit
def test_register_raises_when_duplicate_provider_without_overwrite() -> None:
    EmbeddingFactory.register("fake", FakeEmbedding)

    with pytest.raises(ValueError, match="already registered"):
        EmbeddingFactory.register("fake", FakeEmbedding)

