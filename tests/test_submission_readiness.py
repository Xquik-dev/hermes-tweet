# SPDX-FileCopyrightText: 2026 Xquik Contributors
# SPDX-License-Identifier: MIT

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).parents[1]
SUBMISSION_READINESS_PATH = ROOT / "docs" / "SUBMISSION_READINESS.md"
MAX_SUBMISSION_READINESS_LINES = 180
REQUIRED_RULES = (
    "without copying, translating, or repackaging it",
    "pull-request feature is enabled and accepts external fork heads",
    "canonical, PR-editable source",
    "explicit incompatible license or unsigned legal agreement blocks submission",
    "live listing, open proposal, closed submission, duplicate head branch",
    "adjacent Xquik entry saturates a generic catalog lane",
    "must name `Hermes Tweet` or `hermes-tweet`",
    "copied endpoint URLs resolve only to catalog-listed `/api/v1/...` paths",
    "Run every target-required check",
    "Never publish",
)


def test_submission_readiness_keeps_each_gate() -> None:
    checklist = " ".join(SUBMISSION_READINESS_PATH.read_text().split())

    for rule in REQUIRED_RULES:
        assert rule in checklist


def test_submission_readiness_stays_concise() -> None:
    line_count = len(SUBMISSION_READINESS_PATH.read_text().splitlines())

    assert line_count <= MAX_SUBMISSION_READINESS_LINES
