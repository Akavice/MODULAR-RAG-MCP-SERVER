"""Contract-style tests for OllamaLLM internals and error mapping."""

from __future__ import annotations

import io
from urllib import error as urllib_error

import pytest

from libs.llm.ollama_llm import OllamaLLM
from libs.llm.openai_llm import LLMProviderError


VALID_MESSAGES = [{"role": "user", "content": "hello"}]


class _FakeHTTPResponse:
    """Small context-manager response object for urlopen monkeypatching."""

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
        ("http://localhost:11434/", 15, "http://localhost:11434", 15.0),
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
    llm = OllamaLLM(model="llama3.1", base_url=base_url, timeout=timeout)

    assert llm.base_url == expected_base_url
    assert llm.timeout == expected_timeout


@pytest.mark.unit
def test_build_url_appends_api_chat_path() -> None:
    llm = OllamaLLM(model="llama3.1", base_url="http://127.0.0.1:11434")

    assert llm._build_url() == "http://127.0.0.1:11434/api/chat"


@pytest.mark.unit
@pytest.mark.parametrize(
    ("temperature", "expected_options"),
    [
        (0.2, {"temperature": 0.2}),
        (1, {"temperature": 1}),
    ],
)
def test_build_payload_temperature_options_matrix(
    temperature: float | int,
    expected_options: dict[str, float | int],
) -> None:
    llm = OllamaLLM(model="llama3.1", temperature=temperature)

    payload = llm._build_payload(VALID_MESSAGES)

    assert payload["model"] == "llama3.1"
    assert payload["stream"] is False
    assert payload["messages"] == VALID_MESSAGES
    assert payload["options"] == expected_options


@pytest.mark.unit
def test_build_payload_omits_options_without_temperature() -> None:
    llm = OllamaLLM(model="llama3.1")

    payload = llm._build_payload(VALID_MESSAGES)

    assert "options" not in payload


@pytest.mark.unit
def test_extract_content_rejects_missing_message_object() -> None:
    llm = OllamaLLM(model="llama3.1")

    with pytest.raises(LLMProviderError, match=r"\[ollama\]\[ResponseError\]"):
        llm._extract_content({})


@pytest.mark.unit
def test_extract_content_rejects_non_string_content() -> None:
    llm = OllamaLLM(model="llama3.1")

    with pytest.raises(LLMProviderError, match=r"\[ollama\]\[ResponseError\]"):
        llm._extract_content({"message": {"content": 123}})


@pytest.mark.unit
def test_post_json_rejects_non_object_json(monkeypatch: pytest.MonkeyPatch) -> None:
    llm = OllamaLLM(model="llama3.1")
    monkeypatch.setattr(
        "libs.llm.ollama_llm.urllib_request.urlopen",
        lambda *args, **kwargs: _FakeHTTPResponse("[]"),
    )

    with pytest.raises(LLMProviderError, match=r"\[ollama\]\[ResponseError\]"):
        llm._post_json(url=llm._build_url(), payload=llm._build_payload(VALID_MESSAGES))


@pytest.mark.unit
def test_post_json_rejects_invalid_json(monkeypatch: pytest.MonkeyPatch) -> None:
    llm = OllamaLLM(model="llama3.1")
    monkeypatch.setattr(
        "libs.llm.ollama_llm.urllib_request.urlopen",
        lambda *args, **kwargs: _FakeHTTPResponse("not-json"),
    )

    with pytest.raises(LLMProviderError, match=r"\[ollama\]\[ResponseError\]"):
        llm._post_json(url=llm._build_url(), payload=llm._build_payload(VALID_MESSAGES))


@pytest.mark.unit
def test_post_json_maps_http_error_to_provider_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    llm = OllamaLLM(model="llama3.1")

    def _raise_http_error(*args, **kwargs):  # type: ignore[no-untyped-def]
        fp = io.BytesIO(b'{"error":"bad-request"}')
        raise urllib_error.HTTPError(
            url="http://localhost:11434/api/chat",
            code=400,
            msg="Bad Request",
            hdrs=None,
            fp=fp,
        )

    monkeypatch.setattr("libs.llm.ollama_llm.urllib_request.urlopen", _raise_http_error)

    with pytest.raises(LLMProviderError, match=r"\[ollama\]\[HTTPError\]"):
        llm._post_json(url=llm._build_url(), payload=llm._build_payload(VALID_MESSAGES))


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
    llm = OllamaLLM(model="llama3.1")
    monkeypatch.setattr(
        "libs.llm.ollama_llm.urllib_request.urlopen",
        lambda *args, **kwargs: (_ for _ in ()).throw(raised_error),
    )

    with pytest.raises(LLMProviderError, match=r"\[ollama\]\[ConnectionError\]"):
        llm._post_json(url=llm._build_url(), payload=llm._build_payload(VALID_MESSAGES))


@pytest.mark.unit
def test_chat_rejects_blank_base_url_before_network_call() -> None:
    llm = OllamaLLM(model="llama3.1", base_url="   ")

    with pytest.raises(LLMProviderError, match=r"\[ollama\]\[ConfigError\]"):
        llm.chat(VALID_MESSAGES)
