"""Contract tests for B7.3 OpenAI/Azure embedding implementations."""

from __future__ import annotations

import io
from urllib import error as urllib_error

import pytest

from libs.embedding.azure_embedding import AzureEmbedding
from libs.embedding.embedding_factory import EmbeddingFactory
from libs.embedding.openai_embedding import EmbeddingProviderError, OpenAIEmbedding


VALID_TEXTS = ["hello", "world"]


class _FakeHTTPResponse:
    """Context-manager response object for monkeypatched urlopen."""

    def __init__(self, payload_text: str) -> None:
        self._payload = payload_text.encode("utf-8")

    def __enter__(self) -> "_FakeHTTPResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:  # type: ignore[no-untyped-def]
        return False

    def read(self) -> bytes:
        return self._payload


@pytest.mark.unit
def test_openai_embedding_normalizes_base_url_and_timeout() -> None:
    emb = OpenAIEmbedding(
        model="text-embedding-3-small",
        api_key="k",
        base_url="https://api.openai.com/v1/",
        timeout=12,
    )

    assert emb.base_url == "https://api.openai.com/v1"
    assert emb.timeout == 12.0


@pytest.mark.unit
def test_openai_embedding_build_headers_requires_api_key() -> None:
    emb = OpenAIEmbedding(model="text-embedding-3-small", api_key="   ")

    with pytest.raises(EmbeddingProviderError, match=r"\[openai\]\[ConfigError\]"):
        emb._build_headers()


@pytest.mark.unit
def test_openai_embedding_extract_embeddings_normalizes_numeric_types() -> None:
    emb = OpenAIEmbedding(model="text-embedding-3-small", api_key="k")

    vectors = emb._extract_embeddings(
        {
            "data": [
                {"embedding": [1, 2.5]},
                {"embedding": [0, -1]},
            ]
        }
    )

    assert vectors == [[1.0, 2.5], [0.0, -1.0]]


@pytest.mark.unit
def test_openai_embedding_extract_embeddings_rejects_boolean_values() -> None:
    emb = OpenAIEmbedding(model="text-embedding-3-small", api_key="k")

    with pytest.raises(EmbeddingProviderError, match=r"\[openai\]\[ResponseError\]"):
        emb._extract_embeddings({"data": [{"embedding": [True, 0.2]}]})


@pytest.mark.unit
def test_openai_embedding_rejects_invalid_max_input_chars_type() -> None:
    emb = OpenAIEmbedding(
        model="text-embedding-3-small",
        api_key="k",
        max_input_chars=True,
    )

    with pytest.raises(EmbeddingProviderError, match=r"\[openai\]\[ValidationError\]"):
        emb.embed(["ok"])


@pytest.mark.unit
def test_openai_embedding_post_json_rejects_invalid_json(monkeypatch: pytest.MonkeyPatch) -> None:
    emb = OpenAIEmbedding(model="text-embedding-3-small", api_key="k")
    monkeypatch.setattr(
        "libs.embedding.openai_embedding.urllib_request.urlopen",
        lambda *args, **kwargs: _FakeHTTPResponse("not-json"),
    )

    with pytest.raises(EmbeddingProviderError, match=r"\[openai\]\[ResponseError\]"):
        emb._post_json(
            url=emb._build_url(),
            headers=emb._build_headers(),
            payload=emb._build_payload(VALID_TEXTS),
        )


@pytest.mark.unit
def test_openai_embedding_post_json_maps_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    emb = OpenAIEmbedding(model="text-embedding-3-small", api_key="k")

    def _raise_http_error(*args, **kwargs):  # type: ignore[no-untyped-def]
        fp = io.BytesIO(b'{"error":"bad-request"}')
        raise urllib_error.HTTPError(
            url="https://api.openai.com/v1/embeddings",
            code=400,
            msg="Bad Request",
            hdrs=None,
            fp=fp,
        )

    monkeypatch.setattr("libs.embedding.openai_embedding.urllib_request.urlopen", _raise_http_error)

    with pytest.raises(EmbeddingProviderError, match=r"\[openai\]\[HTTPError\]"):
        emb._post_json(
            url=emb._build_url(),
            headers=emb._build_headers(),
            payload=emb._build_payload(VALID_TEXTS),
        )


@pytest.mark.unit
def test_azure_embedding_prefers_endpoint_over_base_url_alias() -> None:
    emb = AzureEmbedding(
        model="text-embedding-ada-002",
        api_key="k",
        endpoint="https://endpoint.azure.com",
        base_url="https://alias.azure.com",
        api_version="2024-10-21",
    )

    assert emb._build_url().startswith(
        "https://endpoint.azure.com/openai/deployments/text-embedding-ada-002/embeddings"
    )


@pytest.mark.unit
def test_azure_embedding_payload_is_azure_style_without_model() -> None:
    emb = AzureEmbedding(
        model="text-embedding-ada-002",
        api_key="k",
        endpoint="https://endpoint.azure.com",
    )

    payload = emb._build_payload(["a", "b"])

    assert payload == {"input": ["a", "b"]}


@pytest.mark.unit
def test_embedding_factory_reports_builtin_providers_and_blocks_builtin_override() -> None:
    providers = EmbeddingFactory.registered_providers()
    assert "openai" in providers
    assert "azure" in providers

    with pytest.raises(ValueError, match="reserved by built-in embeddings"):
        EmbeddingFactory.register("openai", OpenAIEmbedding)

