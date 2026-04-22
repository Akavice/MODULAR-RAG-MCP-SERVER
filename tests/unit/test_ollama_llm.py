"""Unit tests for OllamaLLM provider behavior."""

from __future__ import annotations

import socket
from urllib import error as urllib_error

import pytest

from libs.llm.llm_factory import LLMFactory
from libs.llm.ollama_llm import OllamaLLM
from libs.llm.openai_llm import LLMProviderError


VALID_MESSAGES = [{"role": "user", "content": "hello"}]


@pytest.mark.unit
def test_factory_routes_ollama_provider() -> None:
    llm = LLMFactory.create(
        {"llm": {"provider": "ollama", "model": "llama3.1", "base_url": "http://host"}}
    )

    assert isinstance(llm, OllamaLLM)


@pytest.mark.unit
def test_chat_uses_mocked_http(monkeypatch: pytest.MonkeyPatch) -> None:
    llm = OllamaLLM(model="llama3.1", base_url="http://localhost:11434")
    monkeypatch.setattr(
        OllamaLLM,
        "_post_json",
        lambda self, **kwargs: {"message": {"content": "ollama-ok"}},
    )

    result = llm.chat(VALID_MESSAGES)

    assert result == "ollama-ok"


@pytest.mark.unit
def test_chat_validation_error_is_readable() -> None:
    llm = OllamaLLM(model="llama3.1")

    with pytest.raises(LLMProviderError, match=r"\[ollama\]\[ValidationError\]"):
        llm.chat([])


@pytest.mark.unit
def test_chat_response_error_is_readable(monkeypatch: pytest.MonkeyPatch) -> None:
    llm = OllamaLLM(model="llama3.1")
    monkeypatch.setattr(OllamaLLM, "_post_json", lambda self, **kwargs: {"message": {}})

    with pytest.raises(LLMProviderError, match=r"\[ollama\]\[ResponseError\]"):
        llm.chat(VALID_MESSAGES)


@pytest.mark.unit
def test_connection_failure_is_readable_without_sensitive_options(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    llm = OllamaLLM(
        model="llama3.1",
        base_url="http://localhost:11434",
        api_key="super-secret",
    )

    def _raise_connection_error(*args, **kwargs):
        raise urllib_error.URLError("connection refused")

    monkeypatch.setattr("libs.llm.ollama_llm.urllib_request.urlopen", _raise_connection_error)

    with pytest.raises(LLMProviderError, match=r"\[ollama\]\[ConnectionError\]") as exc_info:
        llm.chat(VALID_MESSAGES)

    assert "super-secret" not in str(exc_info.value)


@pytest.mark.unit
def test_timeout_is_reported_as_connection_error(monkeypatch: pytest.MonkeyPatch) -> None:
    llm = OllamaLLM(model="llama3.1", base_url="http://localhost:11434")

    def _raise_timeout(*args, **kwargs):
        raise socket.timeout("timed out")

    monkeypatch.setattr("libs.llm.ollama_llm.urllib_request.urlopen", _raise_timeout)

    with pytest.raises(LLMProviderError, match=r"\[ollama\]\[ConnectionError\]"):
        llm.chat(VALID_MESSAGES)
