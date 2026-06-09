from __future__ import annotations

from typing import Any, cast

from .catalog import explore as explore_catalog
from .catalog import find_endpoint, normalize_method
from .client import action_enabled, check_api_available, dumps, request


def _query(value: Any) -> dict[str, str] | None:
    if not isinstance(value, dict):
        return None
    output: dict[str, str] = {}
    for key, item in cast("dict[object, object]", value).items():
        if not isinstance(key, str):
            continue
        if isinstance(item, bool):
            output[key] = str(item).lower()
        elif isinstance(item, (str, int, float)):
            output[key] = str(item)
    return output


def _path(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip()


def explore(args: dict[str, Any], **_: Any) -> str:
    try:
        return dumps({"success": True, "endpoints": explore_catalog(args)})
    except Exception as exc:
        return dumps({"success": False, "error": str(exc)})


def call_read(args: dict[str, Any], **_: Any) -> str:
    try:
        path = _path(args.get("path"))
        endpoint = find_endpoint("GET", path)
        if endpoint is None:
            return dumps(
                {
                    "success": False,
                    "error": f"Endpoint is not in the Hermes Tweet catalog: GET {path}",
                }
            )
        if endpoint.action:
            return dumps(
                {
                    "success": False,
                    "error": "Use tweet_action for private or write-like endpoints.",
                }
            )
        return dumps(request("GET", path, query=_query(args.get("query"))))
    except Exception as exc:
        return dumps({"success": False, "error": str(exc)})


def call_action(args: dict[str, Any], **_: Any) -> str:
    try:
        if not action_enabled():
            return dumps(
                {
                    "success": False,
                    "error": (
                        "tweet_action is disabled. Set HERMES_TWEET_ENABLE_ACTIONS=true "
                        "to enable it."
                    ),
                }
            )
        method = normalize_method(args.get("method"), default="POST")
        path = _path(args.get("path"))
        endpoint = find_endpoint(method, path)
        if endpoint is None:
            return dumps(
                {
                    "success": False,
                    "error": f"Endpoint is not in the Hermes Tweet catalog: {method} {path}",
                }
            )
        return dumps(
            request(
                method,
                path,
                query=_query(args.get("query")),
                body=args.get("body"),
            )
        )
    except Exception as exc:
        return dumps({"success": False, "error": str(exc)})


def xstatus(raw_args: str = "") -> str:
    _ = raw_args
    return call_read({"path": "/api/v1/account"})


def xtrends(raw_args: str = "") -> str:
    category = raw_args.strip()
    query = {"category": category} if category else None
    return call_read({"path": "/api/v1/x/trends", "query": query})


__all__ = [
    "action_enabled",
    "call_action",
    "call_read",
    "check_api_available",
    "explore",
    "xstatus",
    "xtrends",
]
