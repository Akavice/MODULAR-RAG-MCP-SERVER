"""Unit tests for AzureVisionLLM with mocked HTTP transport."""

from __future__ import annotations

import base64
import io
import json
import socket
from pathlib import Path
from urllib import error as urllib_error

import pytest

from libs.llm.azure_vision_llm import AzureVisionLLM, AzureVisionLLMProviderError


class _DummyResponse:
    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def __enter__(self) -> "_DummyResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # type: ignore[no-untyped-def]
        _ = exc_type
        _ = exc
        _ = tb

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")


def _decode_data_url(data_url: str) -> bytes:
    assert ";base64," in data_url
    encoded = data_url.split(";base64,", 1)[1]
    return base64.b64decode(encoded)


@pytest.mark.unit
def test_chat_with_image_path_uses_mocked_http_and_returns_text(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    image_bytes = b"\x89PNG\r\n\x1a\nfake-png-bytes"
    image_path = tmp_path / "sample.png"
    image_path.write_bytes(image_bytes)
    captured: dict[str, object] = {}

    def fake_urlopen(request, timeout):  # type: ignore[no-untyped-def]
        captured["url"] = request.full_url
        captured["timeout"] = timeout
        captured["payload"] = json.loads(request.data.decode("utf-8"))
        return _DummyResponse({"choices": [{"message": {"content": "vision-ok"}}]})

    monkeypatch.setattr("libs.llm.azure_vision_llm.urllib_request.urlopen", fake_urlopen)

    llm = AzureVisionLLM(
        model="gpt-4o-mini",
        endpoint="https://example.openai.azure.com",
        api_key="test-key",
    )

    response = llm.chat_with_image(text="describe image", image_path=str(image_path))

    assert response["text"] == "vision-ok"
    assert str(captured["url"]).startswith(
        "https://example.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions"
    )
    payload = captured["payload"]
    assert isinstance(payload, dict)
    message = payload["messages"][0]
    data_url = message["content"][1]["image_url"]["url"]
    assert _decode_data_url(data_url) == image_bytes


@pytest.mark.unit
def test_chat_with_image_supports_base64_bytes_input() -> None:
    image_bytes = b"\xff\xd8\xffjpeg-bytes"
    encoded = base64.b64encode(image_bytes)
    captured_payload: dict[str, object] = {}

    class TestableAzureVisionLLM(AzureVisionLLM):
        def _post_json(self, *, url, headers, payload):  # type: ignore[override]
            _ = url
            _ = headers
            captured_payload["payload"] = dict(payload)
            return {"choices": [{"message": {"content": "ok"}}]}

    llm = TestableAzureVisionLLM(
        model="gpt-4o-mini",
        endpoint="https://example.openai.azure.com",
        api_key="test-key",
    )

    response = llm.chat_with_image(text="describe", image_path=encoded)

    assert response["text"] == "ok"
    payload = captured_payload["payload"]
    assert isinstance(payload, dict)
    data_url = payload["messages"][0]["content"][1]["image_url"]["url"]
    assert _decode_data_url(data_url) == image_bytes


@pytest.mark.unit
def test_chat_with_image_applies_custom_resize_hook() -> None:
    captured_payload: dict[str, object] = {}

    def fake_resize(raw: bytes, max_image_size: int) -> tuple[bytes, dict[str, object]]:
        assert raw == b"\x89PNG\r\n\x1a\nraw-image"
        assert max_image_size == 1024
        return b"\x89PNG\r\n\x1a\ncompressed", {"image_resized": True}

    class TestableAzureVisionLLM(AzureVisionLLM):
        def _post_json(self, *, url, headers, payload):  # type: ignore[override]
            _ = url
            _ = headers
            captured_payload["payload"] = dict(payload)
            return {"choices": [{"message": {"content": "ok"}}]}

    llm = TestableAzureVisionLLM(
        model="gpt-4o-mini",
        endpoint="https://example.openai.azure.com",
        api_key="test-key",
        max_image_size=1024,
        image_resizer=fake_resize,
    )

    response = llm.chat_with_image(text="describe", image_path=b"\x89PNG\r\n\x1a\nraw-image")

    payload = captured_payload["payload"]
    assert isinstance(payload, dict)
    data_url = payload["messages"][0]["content"][1]["image_url"]["url"]
    assert _decode_data_url(data_url) == b"\x89PNG\r\n\x1a\ncompressed"
    assert response["metadata"]["image_resized"] is True


@pytest.mark.unit
def test_chat_with_image_wraps_timeout_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def raise_timeout(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise TimeoutError("request timed out")

    monkeypatch.setattr("libs.llm.azure_vision_llm.urllib_request.urlopen", raise_timeout)

    llm = AzureVisionLLM(
        model="gpt-4o-mini",
        endpoint="https://example.openai.azure.com",
        api_key="test-key",
        timeout=1,
    )

    with pytest.raises(AzureVisionLLMProviderError, match=r"\[azure_vision\]\[TimeoutError\]"):
        llm.chat_with_image(text="describe", image_path=b"\x89PNG\r\n\x1a\nbytes")


@pytest.mark.unit
def test_chat_with_image_wraps_401_with_azure_error_code(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def raise_401(*args, **kwargs):  # type: ignore[no-untyped-def]
        fp = io.BytesIO(
            b'{"error":{"code":"invalid_api_key","message":"API key is invalid"}}'
        )
        raise urllib_error.HTTPError(
            url="https://example.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions",
            code=401,
            msg="Unauthorized",
            hdrs=None,
            fp=fp,
        )

    monkeypatch.setattr("libs.llm.azure_vision_llm.urllib_request.urlopen", raise_401)

    llm = AzureVisionLLM(
        model="gpt-4o-mini",
        endpoint="https://example.openai.azure.com",
        api_key="bad-key",
    )

    with pytest.raises(
        AzureVisionLLMProviderError,
        match=r"\[azure_vision\]\[HTTPError\].*invalid_api_key",
    ):
        llm.chat_with_image(text="describe", image_path=b"\x89PNG\r\n\x1a\nbytes")


@pytest.mark.unit
@pytest.mark.parametrize("bad_timeout", [0, -1, "3", float("nan"), float("inf")])
def test_init_rejects_invalid_timeout(bad_timeout: object) -> None:
    with pytest.raises((TypeError, ValueError), match="timeout"):
        AzureVisionLLM(
            model="gpt-4o-mini",
            endpoint="https://example.openai.azure.com",
            api_key="test-key",
            timeout=bad_timeout,  # type: ignore[arg-type]
        )


@pytest.mark.unit
def test_init_supports_endpoint_and_deployment_aliases() -> None:
    llm = AzureVisionLLM(
        base_url="https://alias.openai.azure.com/",
        deployment_name="vision-deploy",
        api_key="k",
    )

    assert llm.base_url == "https://alias.openai.azure.com"
    assert llm.model == "vision-deploy"


@pytest.mark.unit
def test_init_reads_api_key_and_version_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "env-key")
    monkeypatch.setenv("AZURE_OPENAI_API_VERSION", "2099-01-01")

    llm = AzureVisionLLM(endpoint="https://example.openai.azure.com")

    assert llm.api_key == "env-key"
    assert llm.api_version == "2099-01-01"


@pytest.mark.unit
def test_chat_with_image_rejects_data_url_without_base64_marker() -> None:
    llm = AzureVisionLLM(
        model="gpt-4o-mini",
        endpoint="https://example.openai.azure.com",
        api_key="test-key",
    )

    with pytest.raises(AzureVisionLLMProviderError, match="data URL must include ';base64,'"):
        llm.chat_with_image(text="describe", image_path="data:image/png,abcd")


@pytest.mark.unit
def test_chat_with_image_wraps_non_json_http_error_body(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def raise_500(*args, **kwargs):  # type: ignore[no-untyped-def]
        fp = io.BytesIO(b"upstream exploded in plain text")
        raise urllib_error.HTTPError(
            url="https://example.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions",
            code=500,
            msg="Server Error",
            hdrs=None,
            fp=fp,
        )

    monkeypatch.setattr("libs.llm.azure_vision_llm.urllib_request.urlopen", raise_500)
    llm = AzureVisionLLM(
        model="gpt-4o-mini",
        endpoint="https://example.openai.azure.com",
        api_key="k",
    )

    with pytest.raises(AzureVisionLLMProviderError, match=r"\[azure_vision\]\[HTTPError\].*Server Error"):
        llm.chat_with_image(text="describe", image_path=b"\x89PNG\r\n\x1a\nbytes")


@pytest.mark.unit
def test_chat_with_image_wraps_urLError_as_connection_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def raise_url_error(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise urllib_error.URLError(socket.gaierror("name resolution failed"))

    monkeypatch.setattr("libs.llm.azure_vision_llm.urllib_request.urlopen", raise_url_error)
    llm = AzureVisionLLM(
        model="gpt-4o-mini",
        endpoint="https://example.openai.azure.com",
        api_key="k",
    )

    with pytest.raises(AzureVisionLLMProviderError, match=r"\[azure_vision\]\[ConnectionError\]"):
        llm.chat_with_image(text="describe", image_path=b"\x89PNG\r\n\x1a\nbytes")
