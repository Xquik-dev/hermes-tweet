from __future__ import annotations

from typing import Any, Self

import httpx
import pytest

from hermes_tweet import client
from hermes_tweet.client import build_headers


def test_build_headers_uses_x_api_key_for_xquik_keys() -> None:
    assert build_headers("xq_test", has_body=False) == {"x-api-key": "xq_test"}


def test_build_headers_uses_bearer_for_other_tokens() -> None:
    assert build_headers("token", has_body=True) == {
        "authorization": "Bearer token",
        "content-type": "application/json",
    }


def test_env_helpers(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("XQUIK_BASE_URL", "https://example.com/api")
    monkeypatch.setenv("XQUIK_API_KEY", "xq_test")
    monkeypatch.setenv("HERMES_TWEET_ENABLE_ACTIONS", "true")

    assert client.base_url() == "https://example.com/api/"
    assert client.api_key() == "xq_test"
    assert client.check_api_available() is True
    assert client.action_enabled() is True


def test_env_helpers_normalize_whitespace(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("XQUIK_BASE_URL", "  https://example.com/api/  ")
    monkeypatch.setenv("XQUIK_API_KEY", "  xq_test  ")
    monkeypatch.setenv("HERMES_TWEET_ENABLE_ACTIONS", "  true  ")

    assert client.base_url() == "https://example.com/api/"
    assert client.api_key() == "xq_test"
    assert client.check_api_available() is True
    assert client.action_enabled() is True


def test_env_helpers_use_default_base_url_for_blank_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("XQUIK_BASE_URL", "  ")

    assert client.base_url() == "https://xquik.com/"


def test_env_helpers_when_unconfigured(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("XQUIK_BASE_URL", raising=False)
    monkeypatch.delenv("XQUIK_API_KEY", raising=False)
    monkeypatch.delenv("HERMES_TWEET_ENABLE_ACTIONS", raising=False)

    assert client.base_url() == "https://xquik.com/"
    assert client.api_key() == ""
    assert client.check_api_available() is False
    assert client.action_enabled() is False
    assert build_headers("", has_body=False) == {}


def test_request_validates_path(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("XQUIK_API_KEY", "xq_test")

    assert client.request("GET", "/bad") == {
        "success": False,
        "error": "Path must start with /api/v1/",
    }
    assert client.request("GET", "/api/v1/account?x=1") == {
        "success": False,
        "error": "Pass query parameters through the query object, not in the path.",
    }


def test_request_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("XQUIK_API_KEY", raising=False)

    assert client.request("GET", "/api/v1/account") == {
        "success": False,
        "error": "XQUIK_API_KEY is not configured.",
    }


class FakeClient:
    response: httpx.Response | None = None
    error: httpx.HTTPError | None = None
    last_request: dict[str, Any] | None = None

    def __init__(self, timeout: float) -> None:
        self.timeout = timeout

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def request(self, **kwargs: Any) -> httpx.Response:
        FakeClient.last_request = kwargs
        if FakeClient.error is not None:
            raise FakeClient.error
        if FakeClient.response is None:
            raise AssertionError("FakeClient.response must be set")
        return FakeClient.response


def _response(
    status_code: int, *, json_data: dict[str, Any] | None = None, text: str = ""
) -> httpx.Response:
    request = httpx.Request("GET", "https://xquik.com/api/v1/account")
    if json_data is None:
        return httpx.Response(status_code, content=text.encode(), request=request)
    return httpx.Response(status_code, json=json_data, request=request)


def test_request_returns_json_response(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("XQUIK_API_KEY", "xq_test")
    monkeypatch.setattr(client.httpx, "Client", FakeClient)
    FakeClient.response = _response(200, json_data={"ok": True})
    FakeClient.error = None

    assert client.request("GET", "/api/v1/account", query={"a": "1"}) == {"ok": True}
    assert FakeClient.last_request is not None
    assert FakeClient.last_request["headers"] == {"x-api-key": "xq_test"}


def test_request_ignores_empty_query(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("XQUIK_API_KEY", "xq_test")
    monkeypatch.setattr(client.httpx, "Client", FakeClient)
    FakeClient.response = _response(200, json_data={"ok": True})
    FakeClient.error = None

    assert client.request("GET", "/api/v1/account", query={}) == {"ok": True}
    assert FakeClient.last_request is not None
    assert FakeClient.last_request["params"] is None


def test_request_normalizes_path_whitespace(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("XQUIK_API_KEY", "xq_test")
    monkeypatch.setattr(client.httpx, "Client", FakeClient)
    FakeClient.response = _response(200, json_data={"ok": True})
    FakeClient.error = None

    assert client.request("GET", " /api/v1/account ") == {"ok": True}
    assert FakeClient.last_request is not None
    assert FakeClient.last_request["url"] == "https://xquik.com/api/v1/account"


def test_request_normalizes_method_whitespace(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("XQUIK_API_KEY", "xq_test")
    monkeypatch.setattr(client.httpx, "Client", FakeClient)
    FakeClient.response = _response(200, json_data={"ok": True})
    FakeClient.error = None

    assert client.request(" get ", "/api/v1/account") == {"ok": True}
    assert FakeClient.last_request is not None
    assert FakeClient.last_request["method"] == "GET"


def test_request_defaults_blank_method_to_get(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("XQUIK_API_KEY", "xq_test")
    monkeypatch.setattr(client.httpx, "Client", FakeClient)
    FakeClient.response = _response(200, json_data={"ok": True})
    FakeClient.error = None

    assert client.request("  ", "/api/v1/account") == {"ok": True}
    assert FakeClient.last_request is not None
    assert FakeClient.last_request["method"] == "GET"


def test_request_returns_text_response(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("XQUIK_API_KEY", "token")
    monkeypatch.setattr(client.httpx, "Client", FakeClient)
    FakeClient.response = _response(200, text="plain")
    FakeClient.error = None

    assert client.request("POST", "/api/v1/compose", body={"text": "hello"}) == {"text": "plain"}
    assert FakeClient.last_request is not None
    assert FakeClient.last_request["headers"] == {
        "authorization": "Bearer token",
        "content-type": "application/json",
    }


def test_request_returns_api_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("XQUIK_API_KEY", "xq_test")
    monkeypatch.setattr(client.httpx, "Client", FakeClient)
    FakeClient.response = _response(402, json_data={"error": "insufficient_credits"})
    FakeClient.error = None

    assert client.request("GET", "/api/v1/account") == {
        "success": False,
        "error": "API request failed.",
        "status_code": 402,
        "response": {"error": "insufficient_credits"},
    }


def test_request_returns_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("XQUIK_API_KEY", "xq_test")
    monkeypatch.setattr(client.httpx, "Client", FakeClient)
    FakeClient.response = None
    FakeClient.error = httpx.ConnectError("network down")

    assert client.request("GET", "/api/v1/account") == {
        "success": False,
        "error": "network down",
    }


def test_request_rethrows_unexpected_fake_setup(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("XQUIK_API_KEY", "xq_test")
    monkeypatch.setattr(client.httpx, "Client", FakeClient)
    FakeClient.response = None
    FakeClient.error = None

    with pytest.raises(AssertionError, match=r"FakeClient\.response must be set"):
        client.request("GET", "/api/v1/account")
