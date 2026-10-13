# SPDX-FileCopyrightText: 2026 Xquik Contributors
# SPDX-License-Identifier: MIT

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
BASH = shutil.which("bash") or "/bin/bash"
FAKE_CODEQL = """#!/usr/bin/env bash
[ "$*" = 'version --format=terse' ] || exit 99
echo {version}
"""
MISSING = "CodeQL CLI is missing. Install it with brew install --cask codeql, then rerun."
OUTDATED = "CodeQL CLI 2.26.9 is older than 2.27.0. Run brew upgrade --cask codeql."
EXTRACTED: dict[str, object] = {
    "descriptor": {"id": "py/diagnostics/successfully-extracted-files"},
    "level": "none",
}
FINDING: dict[str, object] = {
    "locations": [
        {
            "physicalLocation": {
                "artifactLocation": {"uri": "hermes_tweet/a.py"},
                "region": {"startLine": 7},
            }
        }
    ],
    "message": {"text": "Unsafe value."},
    "ruleId": "py/x",
}


def check_version(tmp_path: Path, version: str | None) -> subprocess.CompletedProcess[str]:
    codeql = tmp_path / "codeql"
    if version is not None:
        codeql.write_text(FAKE_CODEQL.format(version=version))
        codeql.chmod(0o755)
    return subprocess.run(
        [BASH, str(ROOT / "scripts/codeql-security"), "--version"],
        env={**os.environ, "XQUIK_CODEQL_BIN": str(codeql)},
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.parametrize("version", ["2.27.0", "2.27.2", "2.100.0", "3.0.0"])
def test_supported_codeql_prints_its_version_without_analyzing(
    tmp_path: Path, version: str
) -> None:
    result = check_version(tmp_path, version)
    assert result.returncode == 0, result.stderr
    assert result.stdout == f"{version}\n"
    assert result.stderr == ""


@pytest.mark.parametrize(("version", "message"), [(None, MISSING), ("2.26.9", OUTDATED)])
def test_unusable_codeql_fails_with_the_next_step(
    tmp_path: Path, version: str | None, message: str
) -> None:
    result = check_version(tmp_path, version)
    assert result.returncode == 1
    assert result.stderr == f"{message}\n"
    assert result.stdout == ""


def invocation(notification: dict[str, object], *, successful: bool = True) -> dict[str, object]:
    return {"executionSuccessful": successful, "toolExecutionNotifications": [notification]}


def report(**change: object) -> dict[str, object]:
    run = {"invocations": [invocation(EXTRACTED)], "results": [], **change}
    return {"runs": [run], "version": "2.1.0"}


def verify(tmp_path: Path, sarif: dict[str, object]) -> subprocess.CompletedProcess[str]:
    path = tmp_path / "report.sarif"
    path.write_text(json.dumps(sarif))
    return subprocess.run(
        [BASH, str(ROOT / "scripts/verify-codeql"), str(path)],
        capture_output=True,
        text=True,
        check=False,
    )


def test_complete_run_with_no_findings_passes(tmp_path: Path) -> None:
    result = verify(tmp_path, report())
    assert result.returncode == 0, result.stderr
    assert result.stdout == "CodeQL finished with no findings. Extracted Python entries 1.\n"


@pytest.mark.parametrize("level", ["error", "warning", "note", "none"])
def test_finding_of_any_level_fails_and_names_its_place(tmp_path: Path, level: str) -> None:
    result = verify(tmp_path, report(results=[{**FINDING, "level": level}]))
    assert result.returncode == 1
    assert result.stderr == (
        "py/x hermes_tweet/a.py:7 Unsafe value.\nCodeQL found 1 finding(s). Fix each one.\n"
    )


@pytest.mark.parametrize(
    ("sarif", "message"),
    [
        ({"runs": [], "version": "2.1.0"}, "Expected 1 SARIF 2.1.0 run."),
        ({**report(), "version": "2.0.0"}, "Expected 1 SARIF 2.1.0 run."),
        (report(results=None), "CodeQL report lacks results."),
        (report(invocations=[]), "CodeQL report lacks invocations."),
        (
            report(invocations=[invocation(EXTRACTED, successful=False)]),
            "CodeQL invocation failed.",
        ),
        (
            report(invocations=[{"executionSuccessful": True}]),
            "CodeQL report lacks diagnostics.",
        ),
        (report(invocations=[invocation({"level": "error"})]), "CodeQL diagnostic needs review."),
        (
            report(invocations=[invocation({"level": "note"})]),
            "CodeQL did not confirm extracted Python files.",
        ),
    ],
)
def test_incomplete_report_fails(tmp_path: Path, sarif: dict[str, object], message: str) -> None:
    result = verify(tmp_path, sarif)
    assert result.returncode == 1
    assert result.stderr == f"{message}\n"
