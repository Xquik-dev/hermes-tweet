from __future__ import annotations

import json
import os
from typing import Any
from urllib.parse import urljoin

import httpx

API_V1_PREFIX = "/api/v1/"
DEFAULT_BASE_URL = "https://xquik.com"
TIMEOUT_SECONDS = 30.0


def base_url() -> str:
    return os.getenv("XQUIK_BASE_URL", DEFAULT_BASE_URL).rstrip("/") + "/"


def api_key() -> str:
    return os.getenv("XQUIK_API_KEY", "")


def check_api_available() -> bool:
    return bool(api_key())


def action_enabled() -> bool:
    return check_api_available() and os.getenv("HERMES_TWEET_ENABLE_ACTIONS", "").lower() == "true"


def build_headers(key: str, *, has_body: bool) -> dict[str, str]:
    headers: dict[str, str] = {}
    if key.startswith("xq_"):
        headers["x-api-key"] = key
    elif key:
        headers["authorization"] = f"Bearer {key}"
    if has_body:
        headers["content-type"] = "application/json"
    return headers


def request(
    method: str,
    path: str,
    query: dict[str, str] | None = None,
    body: Any | None = None,
) -> Any:
    if not path.startswith(API_V1_PREFIX):
        return {"success": False, "error": f"Path must start with {API_V1_PREFIX}"}
    if "?" in path or "#" in path:
        return {
            "success": False,
            "error": "Pass query parameters through the query object, not in the path.",
        }

    key = api_key()
    if not key:
        return {"success": False, "error": "XQUIK_API_KEY is not configured."}

    url = urljoin(base_url(), path.lstrip("/"))
    try:
        with httpx.Client(timeout=TIMEOUT_SECONDS) as client:
            response = client.request(
                method=method,
                url=url,
                params=query,
                json=body,
                headers=build_headers(key, has_body=body is not None),
            )
        try:
            payload = response.json()
        except ValueError:
            payload = {"text": response.text}
        if not response.is_success:
            return {
                "success": False,
                "error": "API request failed.",
                "status_code": response.status_code,
                "response": payload,
            }
        return payload
    except httpx.HTTPError as exc:
        return {"success": False, "error": str(exc)}


def dumps(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))
