from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, cast

import yaml

METHODS = {"get", "post", "put", "patch", "delete"}
API_PREFIX = "/api/v1"
EXPECTED_ARG_COUNT = 2
OUTPUT = Path(__file__).resolve().parents[1] / "hermes_tweet" / "catalog_data.json"

JsonDict = dict[str, Any]

PROHIBITED_STATIC = {
    ("PATCH", "/api/v1/account"),
    ("PUT", "/api/v1/account/x-identity"),
    ("GET", "/api/v1/api-keys"),
    ("POST", "/api/v1/api-keys"),
    ("POST", "/api/v1/subscribe"),
    ("POST", "/api/v1/credits/topup"),
    ("GET", "/api/v1/credits/topup/status"),
    ("POST", "/api/v1/credits/quick-topup"),
    ("POST", "/api/v1/x/accounts"),
    ("POST", "/api/v1/x/accounts/bulk-retry"),
}

PAID_STATIC = {
    ("POST", "/api/v1/x/media/download"),
}

ACTION_PREFIXES = (
    "/api/v1/events",
    "/api/v1/webhooks",
    "/api/v1/x/accounts",
    "/api/v1/x/bookmarks",
    "/api/v1/x/dm",
    "/api/v1/x/notifications",
    "/api/v1/x/timeline",
)


def _as_dict(value: object) -> JsonDict:
    return cast("JsonDict", value) if isinstance(value, dict) else {}


def _as_list(value: object) -> list[object]:
    return cast("list[object]", value) if isinstance(value, list) else []


def _full_path(path: str) -> str:
    return f"{API_PREFIX}{path}" if path.startswith("/") else f"{API_PREFIX}/{path}"


def _category(tags: object) -> str:
    values = _as_list(tags)
    if values:
        return str(values[0]).lower().replace(" ", "-")
    return "uncategorized"


def _schema_type(schema: JsonDict) -> str:
    value = schema.get("type")
    if isinstance(value, str):
        return value
    if "schema" in schema:
        return _schema_type(_as_dict(schema["schema"]))
    return "unknown"


def _resolve_parameter_ref(parameter: JsonDict, parameter_components: JsonDict) -> JsonDict:
    ref = parameter.get("$ref")
    if not isinstance(ref, str) or not ref.startswith("#/components/parameters/"):
        return parameter
    name = ref.removeprefix("#/components/parameters/")
    return _as_dict(parameter_components.get(name))


def _parameters(
    path_item: JsonDict,
    operation: JsonDict,
    parameter_components: JsonDict,
) -> list[JsonDict]:
    merged: list[JsonDict] = []
    for source in (path_item.get("parameters"), operation.get("parameters")):
        merged.extend(
            _resolve_parameter_ref(_as_dict(item), parameter_components)
            for item in _as_list(source)
        )

    output: list[JsonDict] = []
    for parameter in merged:
        name = str(parameter.get("name", "")).strip()
        if not name:
            continue
        schema = _as_dict(parameter.get("schema"))
        output.append(
            {
                "name": name,
                "in": str(parameter.get("in", "query")),
                "required": bool(parameter.get("required", False)),
                "type": _schema_type(schema),
                "description": str(parameter.get("description", "")).strip(),
            }
        )

    request_body = _as_dict(operation.get("requestBody"))
    if request_body:
        output.append(
            {
                "name": "body",
                "in": "body",
                "required": bool(request_body.get("required", False)),
                "type": "object",
                "description": (
                    str(request_body.get("description", "JSON request body")).strip()
                    or "JSON request body"
                ),
            }
        )

    return output


def _response_shape(operation: JsonDict) -> str:
    responses = _as_dict(operation.get("responses"))
    for status in ("200", "201", "202"):
        response = _as_dict(responses.get(status))
        if response:
            description = str(response.get("description", "")).strip()
            return description[:240]
    return ""


def _mpp(operation: JsonDict) -> dict[str, str] | None:
    info = _as_dict(operation.get("x-payment-info"))
    if not info:
        return None
    amount = info.get("amount")
    try:
        price = int(str(amount)) / 1_000_000
    except ValueError:
        price = 0
    return {
        "intent": str(info.get("intent", "charge")),
        "price": f"${price:.5f}/call",
    }


def _prohibited(method: str, path: str) -> bool:
    if (method, path) in PROHIBITED_STATIC:
        return True
    if path.startswith("/api/v1/support/tickets"):
        return True
    if method == "DELETE" and path.startswith("/api/v1/api-keys/"):
        return True
    if path.startswith("/api/v1/x/accounts/") and method in {"GET", "DELETE"}:
        return True
    return path.startswith("/api/v1/x/accounts/") and path.endswith("/reauth") and method == "POST"


def _action(method: str, path: str) -> bool:
    if method != "GET":
        return True
    return any(path == prefix or path.startswith(f"{prefix}/") for prefix in ACTION_PREFIXES)


def build(source: Path) -> list[JsonDict]:
    spec = _as_dict(cast("object", yaml.safe_load(source.read_text(encoding="utf-8"))))
    paths = _as_dict(spec.get("paths"))
    components = _as_dict(spec.get("components"))
    parameter_components = _as_dict(components.get("parameters"))
    output: list[JsonDict] = []

    for raw_path, path_item in sorted(paths.items()):
        path_item_dict = _as_dict(path_item)
        if not path_item_dict:
            continue

        for raw_method, operation in sorted(path_item_dict.items()):
            method_name = str(raw_method)
            operation_dict = _as_dict(operation)
            if method_name.lower() not in METHODS or not operation_dict:
                continue

            method = method_name.upper()
            path = _full_path(str(raw_path))
            if _prohibited(method, path):
                continue

            output.append(
                {
                    "action": _action(method, path),
                    "category": _category(operation_dict.get("tags")),
                    "free": "x-payment-info" not in operation_dict
                    and (method, path) not in PAID_STATIC,
                    "method": method,
                    "mpp": _mpp(operation_dict),
                    "parameters": _parameters(path_item_dict, operation_dict, parameter_components),
                    "path": path,
                    "responseShape": _response_shape(operation_dict),
                    "summary": str(
                        operation_dict.get("summary") or operation_dict.get("description") or "",
                    ).strip(),
                }
            )

    return output


def main() -> int:
    if len(sys.argv) != EXPECTED_ARG_COUNT:
        print("Usage: python scripts/build_catalog.py /path/to/openapi.yaml", file=sys.stderr)
        return 2
    source = Path(sys.argv[1]).resolve()
    data = build(source)
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(data)} endpoints to {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
