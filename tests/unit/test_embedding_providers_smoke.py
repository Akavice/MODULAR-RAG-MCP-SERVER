"""Smoke tests for OpenAI/Azure embedding providers with mocked HTTP."""

from __future__ import annotations

import pytest

from libs.embedding.azure_embedding import AzureEmbedding
from libs.embedding.embedding_factory import EmbeddingFactory
from libs.embedding.openai_embedding import (
    EmbeddingProviderError,
    OpenAIEmbedding,
)


VALID_TEXTS = ["hello", "world"]


@pytest.mark.unit
def test_factory_routes_openai_provider() -> None:
    embedding = EmbeddingFactory.create(
        {
            "embedding": {
                "provider": "openai",
                "model": "text-embedding-3-small",
                "api_key": "test-key",
            }
        }
    )

    assert isinstance(embedding, OpenAIEmbedding)


@pytest.mark.unit
@pytest.mark.parametrize(
    "azure_kwargs",
    [
        {"endpoint": "https://example.openai.azure.com"},
        {"base_url": "https://example.openai.azure.com"},
    ],
)
def test_factory_routes_azure_provider_with_endpoint_aliases(
    azure_kwargs: dict[str, str],
) -> None:
    embedding = EmbeddingFactory.create(
        {
            "embedding": {
                "provider": "azure",
                "model": "text-embedding-ada-002",
                "api_key": "test-key",
                **azure_kwargs,
            }
        }
    )

    assert isinstance(embedding, AzureEmbedding)


@pytest.mark.unit
def test_openai_embed_uses_mocked_http(monkeypatch: pytest.MonkeyPatch) -> None:
    embedding = OpenAIEmbedding(model="text-embedding-3-small", api_key="test-key")
    monkeypatch.setattr(
        OpenAIEmbedding,
        "_post_json",
        lambda self, **kwargs: {
            "data": [
                {"embedding": [0.1, 0.2], "index": 0},
                {"embedding": [0.3, 0.4], "index": 1},
            ]
        },
    )

    vectors = embedding.embed(VALID_TEXTS)

    assert vectors == [[0.1, 0.2], [0.3, 0.4]]


@pytest.mark.unit
def test_azure_embed_uses_mocked_http(monkeypatch: pytest.MonkeyPatch) -> None:
    embedding = AzureEmbedding(
        model="text-embedding-ada-002",
        api_key="test-key",
        endpoint="https://example.openai.azure.com",
    )
    monkeypatch.setattr(
        AzureEmbedding,
        "_post_json",
        lambda self, **kwargs: {"data": [{"embedding": [0.9, 0.8], "index": 0}]},
    )

    vectors = embedding.embed(["hello"])

    assert vectors == [[0.9, 0.8]]


@pytest.mark.unit
def test_embed_validation_error_is_readable() -> None:
    embedding = OpenAIEmbedding(model="text-embedding-3-small", api_key="test-key")

    with pytest.raises(EmbeddingProviderError, match=r"\[openai\]\[ValidationError\]"):
        embedding.embed([])


@pytest.mark.unit
def test_embed_respects_max_input_chars() -> None:
    embedding = OpenAIEmbedding(
        model="text-embedding-3-small",
        api_key="test-key",
        max_input_chars=5,
    )

    with pytest.raises(EmbeddingProviderError, match=r"\[openai\]\[ValidationError\]"):
        embedding.embed(["123456"])


@pytest.mark.unit
def test_embed_response_error_is_readable(monkeypatch: pytest.MonkeyPatch) -> None:
    embedding = OpenAIEmbedding(model="text-embedding-3-small", api_key="test-key")
    monkeypatch.setattr(OpenAIEmbedding, "_post_json", lambda self, **kwargs: {"data": []})

    with pytest.raises(EmbeddingProviderError, match=r"\[openai\]\[ResponseError\]"):
        embedding.embed(["hello"])


@pytest.mark.unit
def test_azure_missing_endpoint_raises_readable_config_error() -> None:
    embedding = AzureEmbedding(model="text-embedding-ada-002", api_key="test-key")

    with pytest.raises(EmbeddingProviderError, match=r"\[azure\]\[ConfigError\]"):
        embedding.embed(["hello"])
