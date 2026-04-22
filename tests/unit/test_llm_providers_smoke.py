"""Smoke tests for OpenAI-compatible LLM providers with mocked HTTP."""

from __future__ import annotations

import pytest

from libs.llm.azure_llm import AzureLLM
from libs.llm.deepseek_llm import DeepSeekLLM
from libs.llm.llm_factory import LLMFactory
from libs.llm.openai_llm import LLMProviderError, OpenAILLM


VALID_MESSAGES = [{"role": "user", "content": "hello"}]


@pytest.mark.unit
def test_factory_routes_openai_provider() -> None:
    llm = LLMFactory.create(
        {"llm": {"provider": "openai", "model": "gpt-4o-mini", "api_key": "test-key"}}
    )

    assert isinstance(llm, OpenAILLM)


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
    llm = LLMFactory.create(
        {
            "llm": {
                "provider": "azure",
                "model": "gpt-4o-mini",
                "api_key": "test-key",
                **azure_kwargs,
            }
        }
    )

    assert isinstance(llm, AzureLLM)


@pytest.mark.unit
def test_factory_routes_deepseek_provider() -> None:
    llm = LLMFactory.create(
        {
            "llm": {
                "provider": "deepseek",
                "model": "deepseek-chat",
                "api_key": "test-key",
            }
        }
    )

    assert isinstance(llm, DeepSeekLLM)


@pytest.mark.unit
def test_openai_chat_uses_mocked_http(monkeypatch: pytest.MonkeyPatch) -> None:
    llm = OpenAILLM(model="gpt-4o-mini", api_key="test-key")
    monkeypatch.setattr(
        OpenAILLM,
        "_post_json",
        lambda self, **kwargs: {"choices": [{"message": {"content": "openai-ok"}}]},
    )

    result = llm.chat(VALID_MESSAGES)

    assert result == "openai-ok"


@pytest.mark.unit
def test_azure_chat_uses_mocked_http(monkeypatch: pytest.MonkeyPatch) -> None:
    llm = AzureLLM(
        model="gpt-4o-mini",
        api_key="test-key",
        endpoint="https://example.openai.azure.com",
    )
    monkeypatch.setattr(
        AzureLLM,
        "_post_json",
        lambda self, **kwargs: {"choices": [{"message": {"content": "azure-ok"}}]},
    )

    result = llm.chat(VALID_MESSAGES)

    assert result == "azure-ok"


@pytest.mark.unit
def test_azure_chat_uses_mocked_http_with_base_url_alias(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    llm = AzureLLM(
        model="gpt-4o-mini",
        api_key="test-key",
        base_url="https://example.openai.azure.com",
    )
    monkeypatch.setattr(
        AzureLLM,
        "_post_json",
        lambda self, **kwargs: {"choices": [{"message": {"content": "azure-ok"}}]},
    )

    result = llm.chat(VALID_MESSAGES)

    assert result == "azure-ok"


@pytest.mark.unit
def test_deepseek_chat_uses_mocked_http(monkeypatch: pytest.MonkeyPatch) -> None:
    llm = DeepSeekLLM(model="deepseek-chat", api_key="test-key")
    monkeypatch.setattr(
        DeepSeekLLM,
        "_post_json",
        lambda self, **kwargs: {"choices": [{"message": {"content": "deepseek-ok"}}]},
    )

    result = llm.chat(VALID_MESSAGES)

    assert result == "deepseek-ok"


@pytest.mark.unit
def test_chat_validation_error_is_readable_with_provider_and_error_type() -> None:
    llm = OpenAILLM(model="gpt-4o-mini", api_key="test-key")

    with pytest.raises(LLMProviderError, match=r"\[openai\]\[ValidationError\]"):
        llm.chat([])


@pytest.mark.unit
def test_chat_response_error_is_readable_with_provider_and_error_type(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    llm = OpenAILLM(model="gpt-4o-mini", api_key="test-key")
    monkeypatch.setattr(OpenAILLM, "_post_json", lambda self, **kwargs: {"choices": []})

    with pytest.raises(LLMProviderError, match=r"\[openai\]\[ResponseError\]"):
        llm.chat(VALID_MESSAGES)


@pytest.mark.unit
def test_azure_missing_endpoint_raises_readable_config_error() -> None:
    llm = AzureLLM(model="gpt-4o-mini", api_key="test-key", endpoint=None)

    with pytest.raises(LLMProviderError, match=r"\[azure\]\[ConfigError\]"):
        llm.chat(VALID_MESSAGES)
