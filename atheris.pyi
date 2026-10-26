# SPDX-FileCopyrightText: 2026 Xquik Contributors
# SPDX-License-Identifier: MIT

from collections.abc import Callable, Sequence
from contextlib import AbstractContextManager
from typing import NoReturn

class FuzzedDataProvider:
    ConsumeBool: Callable[[], bool]
    ConsumeFloat: Callable[[], float]
    ConsumeInt: Callable[[int], int]
    ConsumeIntInRange: Callable[[int, int], int]
    ConsumeUnicodeNoSurrogates: Callable[[int], str]
    def __init__(self, data: bytes, /) -> None: ...

Setup: Callable[[Sequence[str], Callable[[bytes], None]], list[str]]
Fuzz: Callable[[], NoReturn]

def instrument_imports() -> AbstractContextManager[object]: ...
