from __future__ import annotations

import json
from typing import TYPE_CHECKING

from hermes_tweet import tools
from hermes_tweet.tools import call_action, call_read, explore

if TYPE_CHECKING:
    import pytest


def test_read_rejects_action_endpoint() -> None:
    result = json.loads(call_read({"path": "/api/v1/x/accounts"}))
    assert result["success"] is False
    assert "tweet_action" in result["error"]


def test_action_is_disabled_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("HERMES_TWEET_ENABLE_ACTIONS", raising=False)
    result = json.loads(
        call_action(
            {
                "path": "/api/v1/x/tweets",
                "method": "POST",
                "body": {"text": "hello"},
                "reason": "test",
            }
        )
    )
    assert result["success"] is False
    assert "disabled" in result["error"]


def test_explore_returns_json_string() -> None:
    result = json.loads(explore({"query": "search"}))
    assert result["success"] is True
    assert result["endpoints"]


def test_explore_returns_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail(_args: dict[str, object]) -> list[dict[str, object]]:
        raise ValueError("broken")

    monkeypatch.setattr(tools, "explore_catalog", fail)

    assert json.loads(explore({})) == {"success": False, "error": "broken"}


def test_handlers_reject_non_object_arguments() -> None:
    error = {"success": False, "error": "Tool arguments must be a JSON object."}

    assert json.loads(explore([])) == error
    assert json.loads(call_read(None)) == error
    assert json.loads(call_action("bad")) == error


def test_read_missing_endpoint() -> None:
    result = json.loads(call_read({"path": "/api/v1/missing"}))
    assert result == {
        "success": False,
        "error": "Endpoint is not in the Hermes Tweet catalog: GET /api/v1/missing",
    }


def test_read_success(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_request(
        method: str,
        path: str,
        query: dict[str, str] | None = None,
        body: object | None = None,
    ) -> dict[str, object]:
        return {"method": method, "path": path, "query": query, "body": body}

    monkeypatch.setattr(tools, "request", fake_request)

    result = json.loads(
        call_read(
            {
                "path": "/api/v1/x/tweets/search",
                "query": {
                    1: "ignored",
                    "  ": "ignored",
                    "bad": [],
                    "bad_inf": float("inf"),
                    "bad_nan": float("nan"),
                    "include": True,
                    "limit": 2,
                    " q ": "ai",
                    "ratio": 1.5,
                    "verified": False,
                },
            }
        )
    )

    assert result == {
        "body": None,
        "method": "GET",
        "path": "/api/v1/x/tweets/search",
        "query": {
            "include": "true",
            "limit": "2",
            "q": "ai",
            "ratio": "1.5",
            "verified": "false",
        },
    }


def test_read_normalizes_path_values(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_request(
        method: str,
        path: str,
        query: dict[str, str] | None = None,
        body: object | None = None,
    ) -> dict[str, object]:
        return {"method": method, "path": path, "query": query, "body": body}

    monkeypatch.setattr(tools, "request", fake_request)

    assert json.loads(call_read({"path": " /api/v1/account "})) == {
        "body": None,
        "method": "GET",
        "path": "/api/v1/account",
        "query": None,
    }
    assert json.loads(call_read({"path": None})) == {
        "success": False,
        "error": "Endpoint is not in the Hermes Tweet catalog: GET ",
    }


def test_read_normalizes_copied_endpoint_url_before_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_request(
        method: str,
        path: str,
        query: dict[str, str] | None = None,
        body: object | None = None,
    ) -> dict[str, object]:
        return {"method": method, "path": path, "query": query, "body": body}

    monkeypatch.setattr(tools, "request", fake_request)

    assert json.loads(call_read({"path": "https://xquik.com/api/v1/account"})) == {
        "body": None,
        "method": "GET",
        "path": "/api/v1/account",
        "query": None,
    }


def test_read_rejects_query_or_fragment_in_path(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(tools, "request", None)

    expected = {
        "success": False,
        "error": "Pass query parameters through the query object, not in path.",
    }
    assert (
        json.loads(call_read({"path": "https://xquik.com/api/v1/account?ignored=true"})) == expected
    )
    assert json.loads(call_read({"path": "/api/v1/account#section"})) == expected


def test_read_rejects_non_catalog_copied_url_before_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(tools, "request", None)

    assert json.loads(call_read({"path": "https://xquik.com/not-api/account"})) == {
        "success": False,
        "error": "Endpoint is not in the Hermes Tweet catalog: GET https://xquik.com/not-api/account",
    }


def test_read_success_without_query_dict(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_request(
        method: str,
        path: str,
        query: dict[str, str] | None = None,
        body: object | None = None,
    ) -> dict[str, object]:
        return {"method": method, "path": path, "query": query, "body": body}

    monkeypatch.setattr(tools, "request", fake_request)

    assert json.loads(call_read({"path": "/api/v1/account", "query": []})) == {
        "body": None,
        "method": "GET",
        "path": "/api/v1/account",
        "query": None,
    }


def test_read_ignores_empty_query_after_normalization(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_request(
        method: str,
        path: str,
        query: dict[str, str] | None = None,
        body: object | None = None,
    ) -> dict[str, object]:
        return {"method": method, "path": path, "query": query, "body": body}

    monkeypatch.setattr(tools, "request", fake_request)

    assert json.loads(
        call_read(
            {
                "path": "/api/v1/account",
                "query": {
                    1: "ignored",
                    "  ": "ignored",
                    "bad": [],
                    "bad_inf": float("inf"),
                    "bad_nan": float("nan"),
                },
            }
        )
    ) == {
        "body": None,
        "method": "GET",
        "path": "/api/v1/account",
        "query": None,
    }


def test_read_returns_handler_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail(_method: str, _path: str) -> object:
        raise ValueError("catalog failed")

    monkeypatch.setattr(tools, "find_endpoint", fail)

    assert json.loads(call_read({"path": "/api/v1/account"})) == {
        "success": False,
        "error": "catalog failed",
    }


def test_action_missing_endpoint(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(tools, "action_enabled", lambda: True)

    result = json.loads(
        call_action(
            {
                "method": "POST",
                "path": "/api/v1/missing",
                "reason": "test",
            }
        )
    )

    assert result == {
        "success": False,
        "error": "Endpoint is not in the Hermes Tweet catalog: POST /api/v1/missing",
    }


def test_action_rejects_query_or_fragment_in_path(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(tools, "action_enabled", lambda: True)
    monkeypatch.setattr(tools, "request", None)

    expected = {
        "success": False,
        "error": "Pass query parameters through the query object, not in path.",
    }
    assert (
        json.loads(
            call_action(
                {
                    "method": "POST",
                    "path": "https://xquik.com/api/v1/x/tweets?debug=true",
                    "reason": "test",
                }
            )
        )
        == expected
    )
    assert (
        json.loads(
            call_action(
                {
                    "method": "POST",
                    "path": "/api/v1/x/tweets#section",
                    "reason": "test",
                }
            )
        )
        == expected
    )


def test_action_blocks_account_connection_challenge(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(tools, "action_enabled", lambda: True)
    monkeypatch.setattr(tools, "request", None)

    result = json.loads(
        call_action(
            {
                "method": "POST",
                "path": "/api/v1/x/account-connection-challenges/abc/submit",
                "body": {"code": "123456"},
                "reason": "connect account",
            }
        )
    )

    assert result == {
        "success": False,
        "error": tools.BLOCKED_ACTION_ERROR,
    }


def test_action_requires_reason_when_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(tools, "action_enabled", lambda: True)

    error = {"success": False, "error": "Action reason is required."}

    assert json.loads(call_action({"path": "/api/v1/x/tweets", "method": "POST"})) == error
    assert (
        json.loads(call_action({"path": "/api/v1/x/tweets", "method": "POST", "reason": "  "}))
        == error
    )
    assert (
        json.loads(call_action({"path": "/api/v1/x/tweets", "method": "POST", "reason": None}))
        == error
    )


def test_action_success(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_request(
        method: str,
        path: str,
        query: dict[str, str] | None = None,
        body: object | None = None,
    ) -> dict[str, object]:
        return {"method": method, "path": path, "query": query, "body": body}

    monkeypatch.setattr(tools, "action_enabled", lambda: True)
    monkeypatch.setattr(tools, "request", fake_request)

    result = json.loads(
        call_action(
            {
                "body": {"text": "hello"},
                "method": "POST",
                "path": "/api/v1/x/tweets",
                "query": {"dry": True, "preview": False},
                "reason": "test",
            }
        )
    )

    assert result == {
        "body": {"text": "hello"},
        "method": "POST",
        "path": "/api/v1/x/tweets",
        "query": {"dry": "true", "preview": "false"},
    }


def test_action_defaults_missing_or_malformed_method_to_post(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_request(
        method: str,
        path: str,
        query: dict[str, str] | None = None,
        body: object | None = None,
    ) -> dict[str, object]:
        return {"method": method, "path": path, "query": query, "body": body}

    monkeypatch.setattr(tools, "action_enabled", lambda: True)
    monkeypatch.setattr(tools, "request", fake_request)

    assert json.loads(
        call_action(
            {
                "body": {"text": "hello"},
                "path": "/api/v1/compose",
                "reason": "test",
            }
        )
    ) == {
        "body": {"text": "hello"},
        "method": "POST",
        "path": "/api/v1/compose",
        "query": None,
    }

    result = json.loads(
        call_action(
            {
                "body": {"text": "hello"},
                "method": None,
                "path": "/api/v1/compose",
                "reason": "test",
            }
        )
    )

    assert result == {
        "body": {"text": "hello"},
        "method": "POST",
        "path": "/api/v1/compose",
        "query": None,
    }


def test_action_normalizes_path_values(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_request(
        method: str,
        path: str,
        query: dict[str, str] | None = None,
        body: object | None = None,
    ) -> dict[str, object]:
        return {"method": method, "path": path, "query": query, "body": body}

    monkeypatch.setattr(tools, "action_enabled", lambda: True)
    monkeypatch.setattr(tools, "request", fake_request)

    result = json.loads(
        call_action(
            {
                "body": {"text": "hello"},
                "method": "POST",
                "path": " /api/v1/x/tweets ",
                "reason": "test",
            }
        )
    )

    assert result == {
        "body": {"text": "hello"},
        "method": "POST",
        "path": "/api/v1/x/tweets",
        "query": None,
    }


def test_action_normalizes_copied_endpoint_url_before_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_request(
        method: str,
        path: str,
        query: dict[str, str] | None = None,
        body: object | None = None,
    ) -> dict[str, object]:
        return {"method": method, "path": path, "query": query, "body": body}

    monkeypatch.setattr(tools, "action_enabled", lambda: True)
    monkeypatch.setattr(tools, "request", fake_request)

    assert json.loads(
        call_action(
            {
                "body": {"text": "hello"},
                "method": "POST",
                "path": "https://dashboard.xquik.com/api/v1/x/tweets",
                "reason": "test",
            }
        )
    ) == {
        "body": {"text": "hello"},
        "method": "POST",
        "path": "/api/v1/x/tweets",
        "query": None,
    }


def test_action_rejects_non_catalog_copied_url_before_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(tools, "action_enabled", lambda: True)
    monkeypatch.setattr(tools, "request", None)

    assert json.loads(
        call_action(
            {
                "method": "POST",
                "path": "https://dashboard.xquik.com/not-api/tweet",
                "reason": "test",
            }
        )
    ) == {
        "success": False,
        "error": (
            "Endpoint is not in the Hermes Tweet catalog: "
            "POST https://dashboard.xquik.com/not-api/tweet"
        ),
    }


def test_action_returns_handler_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail() -> bool:
        raise ValueError("env failed")

    monkeypatch.setattr(tools, "action_enabled", fail)

    assert json.loads(call_action({"path": "/api/v1/x/tweets", "method": "POST"})) == {
        "success": False,
        "error": "env failed",
    }


def test_slash_commands(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[dict[str, object]] = []

    def fake_call_read(args: dict[str, object]) -> str:
        calls.append(args)
        return json.dumps({"ok": True})

    monkeypatch.setattr(tools, "call_read", fake_call_read)

    assert tools.xstatus(None) == '{"ok": true}'
    assert tools.xtrends(" tech ") == '{"ok": true}'
    assert tools.xtrends(None) == '{"ok": true}'
    assert calls == [
        {"path": "/api/v1/account"},
        {"path": "/api/v1/x/trends", "query": {"category": "tech"}},
        {"path": "/api/v1/x/trends", "query": None},
    ]
