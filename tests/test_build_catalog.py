from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).parents[1]


def load_build_catalog_module() -> Any:
    module_path = ROOT / "scripts" / "build_catalog.py"
    spec = importlib.util.spec_from_file_location("build_catalog", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


build_catalog = load_build_catalog_module()


def write_openapi(tmp_path: Path, paths: dict[str, object]) -> Path:
    source = tmp_path / "openapi.yaml"
    source.write_text(yaml.safe_dump({"paths": paths}), encoding="utf-8")
    return source


def test_build_skips_prohibited_account_and_support_endpoints(tmp_path: Path) -> None:
    source = write_openapi(
        tmp_path,
        {
            "/account": {"patch": {"summary": "Update account"}},
            "/support/tickets": {"get": {"summary": "List tickets"}},
            "/x/tweets/search": {"get": {"summary": "Search tweets"}},
        },
    )

    endpoints = build_catalog.build(source)

    assert [endpoint["path"] for endpoint in endpoints] == ["/api/v1/x/tweets/search"]


def test_build_marks_non_get_and_action_prefix_gets_as_actions(tmp_path: Path) -> None:
    source = write_openapi(
        tmp_path,
        {
            "/events": {"get": {"summary": "List events"}},
            "/x/tweets": {"post": {"summary": "Create tweet"}},
            "/x/tweets/search": {"get": {"summary": "Search tweets"}},
        },
    )

    endpoints = build_catalog.build(source)
    actions_by_path = {endpoint["path"]: endpoint["action"] for endpoint in endpoints}

    assert actions_by_path == {
        "/api/v1/events": True,
        "/api/v1/x/tweets": True,
        "/api/v1/x/tweets/search": False,
    }


def test_build_extracts_parameters_request_body_response_and_payment(
    tmp_path: Path,
) -> None:
    source = write_openapi(
        tmp_path,
        {
            "/x/tweets/search": {
                "parameters": [
                    {
                        "name": "cursor",
                        "in": "query",
                        "schema": {"type": "string"},
                    }
                ],
                "get": {
                    "summary": "Search tweets",
                    "tags": ["Tweets"],
                    "parameters": [
                        {
                            "name": "q",
                            "in": "query",
                            "required": True,
                            "description": "Search query",
                            "schema": {"type": "string"},
                        }
                    ],
                    "requestBody": {"required": True, "description": "Optional JSON body"},
                    "responses": {"200": {"description": "Search result contract"}},
                    "x-payment-info": {"amount": "150", "intent": "charge"},
                },
            }
        },
    )

    [endpoint] = build_catalog.build(source)

    assert endpoint == {
        "action": False,
        "category": "tweets",
        "free": False,
        "method": "GET",
        "mpp": {"intent": "charge", "price": "$0.00015/call"},
        "parameters": [
            {
                "name": "cursor",
                "in": "query",
                "required": False,
                "type": "string",
                "description": "",
            },
            {
                "name": "q",
                "in": "query",
                "required": True,
                "type": "string",
                "description": "Search query",
            },
            {
                "name": "body",
                "in": "body",
                "required": True,
                "type": "object",
                "description": "Optional JSON body",
            },
        ],
        "path": "/api/v1/x/tweets/search",
        "responseShape": "Search result contract",
        "summary": "Search tweets",
    }


def test_build_defaults_empty_metadata(tmp_path: Path) -> None:
    source = write_openapi(
        tmp_path,
        {
            "x/trends": {
                "get": {
                    "description": "Trend lookup",
                    "parameters": [{"name": "limit", "schema": {"schema": {"type": "integer"}}}],
                }
            }
        },
    )

    [endpoint] = build_catalog.build(source)

    assert endpoint["category"] == "uncategorized"
    assert endpoint["free"] is True
    assert endpoint["method"] == "GET"
    assert endpoint["mpp"] is None
    assert endpoint["parameters"] == [
        {
            "name": "limit",
            "in": "query",
            "required": False,
            "type": "integer",
            "description": "",
        }
    ]
    assert endpoint["path"] == "/api/v1/x/trends"
    assert endpoint["responseShape"] == ""
    assert endpoint["summary"] == "Trend lookup"
