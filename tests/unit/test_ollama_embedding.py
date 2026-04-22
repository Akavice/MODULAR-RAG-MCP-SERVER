"""Unit tests for OllamaEmbedding provider behavior."""

from __future__ import annotations

import socket
from urllib import error as urllib_error

import pytest

from libs.embedding.embedding_factory import EmbeddingFactory
from libs.embedding.ollama_embedding import OllamaEmbedding
from libs.embedding.openai_embedding import EmbeddingProviderError


VALID_TEXTS = ["hello", "world"]


@pytest.mark.unit
def test_factory_routes_ollama_provider() -> None:
    embedding = EmbeddingFactory.create(
        {
            "embedding": {
                "provider": "ollama",
                "model": "nomic-embed-text",
                "base_url": "http://localhost:11434",
            }
        }
    )

    assert isinstance(embedding, OllamaEmbedding)


@pytest.mark.unit
def test_embed_uses_mocked_http_for_batch_texts(monkeypatch: pytest.MonkeyPatch) -> None:
    embedding = OllamaEmbedding(
        model="nomic-embed-text",
        base_url="http://localhost:11434",
    )
    monkeypatch.setattr(
        OllamaEmbedding,
        "_post_json",
        lambda self, **kwargs: {"embeddings": [[0.1, 0.2], [0.3, 0.4]]},
    )

    vectors = embedding.embed(VALID_TEXTS)

    assert vectors == [[0.1, 0.2], [0.3, 0.4]]


@pytest.mark.unit
def test_embed_validation_error_is_readable() -> None:
    embedding = OllamaEmbedding(model="nomic-embed-text")

    with pytest.raises(EmbeddingProviderError, match=r"\[ollama\]\[ValidationError\]"):
        embedding.embed([])


@pytest.mark.unit
def test_embed_respects_max_input_chars() -> None:
    embedding = OllamaEmbedding(model="nomic-embed-text", max_input_chars=3)

    with pytest.raises(EmbeddingProviderError, match=r"\[ollama\]\[ValidationError\]"):
        embedding.embed(["toolong"])


@pytest.mark.unit
def test_embed_response_error_is_readable(monkeypatch: pytest.MonkeyPatch) -> None:
    embedding = OllamaEmbedding(model="nomic-embed-text")
    monkeypatch.setattr(OllamaEmbedding, "_post_json", lambda self, **kwargs: {"embeddings": []})

    with pytest.raises(EmbeddingProviderError, match=r"\[ollama\]\[ResponseError\]"):
        embedding.embed(["hello"])


@pytest.mark.unit
def test_connection_failure_is_readable_without_sensitive_options(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    embedding = OllamaEmbedding(
        model="nomic-embed-text",
        base_url="http://localhost:11434",
        api_key="super-secret",
    )

    def _raise_connection_error(*args, **kwargs):
        raise urllib_error.URLError("connection refused")

    monkeypatch.setattr(
        "libs.embedding.ollama_embedding.urllib_request.urlopen",
        _raise_connection_error,
    )

    with pytest.raises(EmbeddingProviderError, match=r"\[ollama\]\[ConnectionError\]") as exc_info:
        embedding.embed(["hello"])

    assert "super-secret" not in str(exc_info.value)


@pytest.mark.unit
def test_timeout_is_reported_as_connection_error(monkeypatch: pytest.MonkeyPatch) -> None:
    embedding = OllamaEmbedding(model="nomic-embed-text", base_url="http://localhost:11434")

    def _raise_timeout(*args, **kwargs):
        raise socket.timeout("timed out")

    monkeypatch.setattr("libs.embedding.ollama_embedding.urllib_request.urlopen", _raise_timeout)

    with pytest.raises(EmbeddingProviderError, match=r"\[ollama\]\[ConnectionError\]"):
        embedding.embed(["hello"])
