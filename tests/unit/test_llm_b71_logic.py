"""Focused logic tests for B7.1 OpenAI-compatible LLM providers."""

from __future__ import annotations

import io
from urllib import error as urllib_error

import pytest

from libs.llm.azure_llm import AzureLLM
from libs.llm.openai_llm import LLMProviderError, OpenAILLM


VALID_MESSAGES = [{"role": "user", "content": "hello"}]


@pytest.mark.unit
def test_openai_chat_supports_list_content_blocks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    llm = OpenAILLM(model="gpt-4o-mini", api_key="test-key")
    monkeypatch.setattr(
        OpenAILLM,
        "_post_json",
        lambda self, **kwargs: {
            "choices": [
                {
                    "message": {
                        "content": [
                            {"type": "output_text", "text": "line-1"},
                            {"text": "line-2"},
                        ]
                    }
                }
            ]
        },
    )

    result = llm.chat(VALID_MESSAGES)

    assert result == "line-1\nline-2"


@pytest.mark.unit
def test_openai_http_error_is_wrapped_as_provider_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    llm = OpenAILLM(model="gpt-4o-mini", api_key="test-key")

    def raise_http_error(*args, **kwargs):  # type: ignore[no-untyped-def]
        fp = io.BytesIO(b'{"error":"bad-request"}')
        raise urllib_error.HTTPError(
            url="https://api.openai.com/v1/chat/completions",
            code=400,
            msg="Bad Request",
            hdrs=None,
            fp=fp,
        )

    monkeypatch.setattr("libs.llm.openai_llm.urllib_request.urlopen", raise_http_error)

    with pytest.raises(LLMProviderError, match=r"\[openai\]\[HTTPError\]"):
        llm.chat(VALID_MESSAGES)


@pytest.mark.unit
def test_azure_endpoint_has_priority_over_base_url_alias(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    llm = AzureLLM(
        model="gpt-4o-mini",
        api_key="test-key",
        endpoint="https://endpoint.openai.azure.com",
        base_url="https://alias.openai.azure.com",
    )
    captured: dict[str, str] = {}

    def fake_post_json(self, **kwargs):  # type: ignore[no-untyped-def]
        captured["url"] = kwargs["url"]
        return {"choices": [{"message": {"content": "ok"}}]}

    monkeypatch.setattr(AzureLLM, "_post_json", fake_post_json)

    result = llm.chat(VALID_MESSAGES)

    assert result == "ok"
    assert captured["url"].startswith(
        "https://endpoint.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions"
    )

