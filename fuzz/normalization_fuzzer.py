from __future__ import annotations

import json
import sys
from typing import Any

import atheris

with atheris.instrument_imports():
    from hermes_tweet.catalog import explore, matches_path, normalize_limit, normalize_method
    from hermes_tweet.client import dumps, normalize_query_params

MAX_NORMALIZED_LIMIT = 100


class InvariantError(RuntimeError):
    """Report a normalization invariant broken by generated input."""


def _require(*, condition: bool, message: str) -> None:
    if not condition:
        raise InvariantError(message)


def _query_value(provider: atheris.FuzzedDataProvider) -> Any:
    return provider.PickValueInList(
        (
            provider.ConsumeBool(),
            provider.ConsumeInt(8),
            provider.ConsumeFloat(),
            provider.ConsumeUnicodeNoSurrogates(64),
            None,
            [provider.ConsumeUnicodeNoSurrogates(16)],
        )
    )


def _safe_segment(provider: atheris.FuzzedDataProvider) -> str:
    segment = provider.ConsumeUnicodeNoSurrogates(32)
    for reserved in "/[]?#":
        segment = segment.replace(reserved, "_")
    return segment or "value"


def test_one_input(data: bytes) -> None:
    provider = atheris.FuzzedDataProvider(data)
    method = provider.ConsumeUnicodeNoSurrogates(32)
    normalized_method = normalize_method(method)
    _require(
        condition=normalized_method == normalized_method.strip().upper(),
        message="normalized methods must be stripped and uppercase",
    )
    _require(
        condition=bool(normalized_method),
        message="normalized methods must not be empty",
    )

    limit_values: tuple[Any, ...] = (
        provider.ConsumeBool(),
        provider.ConsumeInt(8),
        provider.ConsumeFloat(),
        provider.ConsumeUnicodeNoSurrogates(32),
        None,
    )
    normalized_limit = normalize_limit(provider.PickValueInList(limit_values))
    _require(
        condition=1 <= normalized_limit <= MAX_NORMALIZED_LIMIT,
        message="normalized limits must stay inside the documented range",
    )

    template = f"/api/v1/items/{{id}}/{_safe_segment(provider)}"
    concrete = f"/api/v1/items/{_safe_segment(provider)}/{_safe_segment(provider)}"
    _require(
        condition=isinstance(matches_path(template, concrete), bool),
        message="path matching must always return a boolean",
    )

    query = {
        provider.ConsumeUnicodeNoSurrogates(32): _query_value(provider),
        f" {_safe_segment(provider)} ": _query_value(provider),
    }
    normalized_query = normalize_query_params(query)
    if normalized_query is not None:
        _require(
            condition=all(key and key == key.strip() for key in normalized_query),
            message="query keys must be nonempty and stripped",
        )
        _require(
            condition=all(isinstance(value, str) for value in normalized_query.values()),
            message="query values must be normalized to strings",
        )

    explored = explore(
        {
            "query": provider.ConsumeUnicodeNoSurrogates(24),
            "method": method,
            "limit": normalized_limit,
            "include_actions": provider.ConsumeBool(),
        }
    )
    _require(
        condition=len(explored) <= normalized_limit,
        message="catalog exploration must honor the normalized limit",
    )

    payload = {
        "method": normalized_method,
        "query": normalized_query,
        "segments": [template, concrete],
    }
    _require(
        condition=json.loads(dumps(payload)) == payload,
        message="serialized payloads must round-trip without loss",
    )


def main() -> None:
    atheris.Setup(sys.argv, test_one_input)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
