"""Contract-focused tests for OllamaEmbedding internals."""

from __future__ import annotations

import io
from urllib import error as urllib_error

import pytest

from libs.embedding.embedding_factory import EmbeddingFactory
from libs.embedding.ollama_embedding import OllamaEmbedding
from libs.embedding.openai_embedding import EmbeddingProviderError


VALID_TEXTS = ["hello", "world"]


class _FakeHTTPResponse:
    """Tiny context-manager response for monkeypatched urlopen."""

    def __init__(self, payload_text: str) -> None:
        self._payload = payload_text.encode("utf-8")

    def __enter__(self) -> "_FakeHTTPResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:  # type: ignore[no-untyped-def]
        return False

    def read(self) -> bytes:
        return self._payload


@pytest.mark.unit
@pytest.mark.parametrize(
    ("base_url", "timeout", "expected_base_url", "expected_timeout"),
    [
        ("http://localhost:11434/", 10, "http://localhost:11434", 10.0),
        ("http://127.0.0.1:11434", 7.5, "http://127.0.0.1:11434", 7.5),
        (None, None, "http://localhost:11434", 30.0),
    ],
)
def test_init_normalizes_base_url_and_timeout_matrix(
    base_url: str | None,
    timeout: float | int | None,
    expected_base_url: str,
    expected_timeout: float,
) -> None:
    emb = OllamaEmbedding(model="nomic-embed-text", base_url=base_url, timeout=timeout)

    assert emb.base_url == expected_base_url
    assert emb.timeout == expected_timeout


@pytest.mark.unit
def test_build_url_uses_embed_endpoint() -> None:
    emb = OllamaEmbedding(model="nomic-embed-text", base_url="http://localhost:11434")

    assert emb._build_url() == "http://localhost:11434/api/embed"


@pytest.mark.unit
def test_build_payload_keeps_model_and_input_order() -> None:
    emb = OllamaEmbedding(model="nomic-embed-text")

    payload = emb._build_payload(["a", "b", "c"])

    assert payload["model"] == "nomic-embed-text"
    assert payload["input"] == ["a", "b", "c"]


@pytest.mark.unit
def test_extract_embeddings_normalizes_int_to_float() -> None:
    emb = OllamaEmbedding(model="nomic-embed-text")

    vectors = emb._extract_embeddings({"embeddings": [[1, 2.5], [0, -3]]})

    assert vectors == [[1.0, 2.5], [0.0, -3.0]]


@pytest.mark.unit
def test_extract_embeddings_rejects_bool_dimension_values() -> None:
    emb = OllamaEmbedding(model="nomic-embed-text")

    with pytest.raises(EmbeddingProviderError, match=r"\[ollama\]\[ResponseError\]"):
        emb._extract_embeddings({"embeddings": [[True, 0.1]]})


@pytest.mark.unit
def test_post_json_rejects_invalid_json_body(monkeypatch: pytest.MonkeyPatch) -> None:
    emb = OllamaEmbedding(model="nomic-embed-text")
    monkeypatch.setattr(
        "libs.embedding.ollama_embedding.urllib_request.urlopen",
        lambda *args, **kwargs: _FakeHTTPResponse("not-json"),
    )

    with pytest.raises(EmbeddingProviderError, match=r"\[ollama\]\[ResponseError\]"):
        emb._post_json(url=emb._build_url(), payload=emb._build_payload(VALID_TEXTS))


@pytest.mark.unit
def test_post_json_maps_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    emb = OllamaEmbedding(model="nomic-embed-text")

    def _raise_http_error(*args, **kwargs):  # type: ignore[no-untyped-def]
        fp = io.BytesIO(b'{"error":"bad-request"}')
        raise urllib_error.HTTPError(
            url="http://localhost:11434/api/embed",
            code=500,
            msg="Internal Server Error",
            hdrs=None,
            fp=fp,
        )

    monkeypatch.setattr("libs.embedding.ollama_embedding.urllib_request.urlopen", _raise_http_error)

    with pytest.raises(EmbeddingProviderError, match=r"\[ollama\]\[HTTPError\]"):
        emb._post_json(url=emb._build_url(), payload=emb._build_payload(VALID_TEXTS))


@pytest.mark.unit
@pytest.mark.parametrize(
    "raised_error",
    [
        TimeoutError("timed out"),
        urllib_error.URLError("connection refused"),
    ],
)
def test_post_json_maps_network_errors_to_connection_error(
    monkeypatch: pytest.MonkeyPatch,
    raised_error: Exception,
) -> None:
    emb = OllamaEmbedding(model="nomic-embed-text")
    monkeypatch.setattr(
        "libs.embedding.ollama_embedding.urllib_request.urlopen",
        lambda *args, **kwargs: (_ for _ in ()).throw(raised_error),
    )

    with pytest.raises(EmbeddingProviderError, match=r"\[ollama\]\[ConnectionError\]"):
        emb._post_json(url=emb._build_url(), payload=emb._build_payload(VALID_TEXTS))


@pytest.mark.unit
def test_embed_rejects_blank_base_url_before_network_call() -> None:
    emb = OllamaEmbedding(model="nomic-embed-text", base_url="   ")

    with pytest.raises(EmbeddingProviderError, match=r"\[ollama\]\[ConfigError\]"):
        emb.embed(["hello"])


@pytest.mark.unit
def test_embedding_factory_exposes_and_protects_ollama_builtin() -> None:
    providers = EmbeddingFactory.registered_providers()
    assert "ollama" in providers

    with pytest.raises(ValueError, match="reserved by built-in embeddings"):
        EmbeddingFactory.register("ollama", OllamaEmbedding)

