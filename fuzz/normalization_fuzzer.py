# SPDX-FileCopyrightText: 2026 Xquik Contributors
# SPDX-License-Identifier: MIT

from __future__ import annotations

import json
import sys
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable
    from contextlib import AbstractContextManager

    class _FuzzedDataProvider:
        ConsumeBool: Callable[[], bool]
        ConsumeFloat: Callable[[], float]
        ConsumeInt: Callable[[int], int]
        ConsumeIntInRange: Callable[[int, int], int]
        ConsumeUnicodeNoSurrogates: Callable[[int], str]

    class _Atheris:
        FuzzedDataProvider: Callable[[bytes], _FuzzedDataProvider]
        Fuzz: Callable[[], None]
        Setup: Callable[[list[str], Callable[[bytes], None]], list[str]]
        instrument_imports: Callable[[], AbstractContextManager[object, None]]

    atheris = _Atheris()
else:
    import atheris

with atheris.instrument_imports():
    from hermes_tweet.catalog import explore, matches_path, normalize_limit, normalize_method
    from hermes_tweet.client import dumps, normalize_query_params

MAX_NORMALIZED_LIMIT = 100

_T = TypeVar("_T")
_decode_json: Callable[[str], object] = json.loads


class InvariantError(RuntimeError):
    pass


def _require(*, condition: bool, message: str) -> None:
    if not condition:
        raise InvariantError(message)


def _pick_value(
    provider: _FuzzedDataProvider,
    values: tuple[_T, ...],
) -> _T:
    index = provider.ConsumeIntInRange(0, len(values) - 1)
    return values[index]


def _query_value(provider: _FuzzedDataProvider) -> object:
    return _pick_value(
        provider,
        (
            provider.ConsumeBool(),
            provider.ConsumeInt(8),
            provider.ConsumeFloat(),
            provider.ConsumeUnicodeNoSurrogates(64),
            None,
            [provider.ConsumeUnicodeNoSurrogates(16)],
        ),
    )


def _safe_segment(provider: _FuzzedDataProvider) -> str:
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
        message="Normalized methods must be stripped and uppercase.",
    )
    _require(
        condition=bool(normalized_method),
        message="Normalized methods must not be empty.",
    )

    limit_values: tuple[object, ...] = (
        provider.ConsumeBool(),
        provider.ConsumeInt(8),
        provider.ConsumeFloat(),
        provider.ConsumeUnicodeNoSurrogates(32),
        None,
    )
    normalized_limit = normalize_limit(_pick_value(provider, limit_values))
    _require(
        condition=1 <= normalized_limit <= MAX_NORMALIZED_LIMIT,
        message="Normalized limits must stay inside the documented range.",
    )

    template = f"/api/v1/items/{{id}}/{_safe_segment(provider)}"
    concrete = f"/api/v1/items/{_safe_segment(provider)}/{_safe_segment(provider)}"
    _require(
        condition=type(matches_path(template, concrete)) is bool,
        message="Path matching must always return a boolean.",
    )

    query = {
        provider.ConsumeUnicodeNoSurrogates(32): _query_value(provider),
        f" {_safe_segment(provider)} ": _query_value(provider),
    }
    normalized_query = normalize_query_params(query)
    if normalized_query is not None:
        _require(
            condition=all(key and key == key.strip() for key in normalized_query),
            message="Query keys must be nonempty and stripped.",
        )
        _require(
            condition=all(type(value) is str for value in normalized_query.values()),
            message="Query values must be normalized to strings.",
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
        message="Catalog exploration must honor the normalized limit.",
    )

    payload = {
        "method": normalized_method,
        "query": normalized_query,
        "segments": [template, concrete],
    }
    _require(
        condition=_decode_json(dumps(payload)) == payload,
        message="Serialized payloads must round-trip without loss.",
    )


def main() -> None:
    atheris.Setup(sys.argv, test_one_input)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
