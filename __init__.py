# SPDX-FileCopyrightText: 2026 Xquik Contributors
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING

if __package__ and not TYPE_CHECKING:
    from .hermes_tweet import register
else:
    from hermes_tweet import register

__all__ = ["register"]
