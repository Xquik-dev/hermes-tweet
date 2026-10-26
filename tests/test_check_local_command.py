# SPDX-FileCopyrightText: 2026 Xquik Contributors
# SPDX-License-Identifier: MIT

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
BASH = shutil.which("bash") or "/bin/bash"
GIT = shutil.which("git") or "/usr/bin/git"
SCRIPT = r"""#!/usr/bin/env bash
name=$(basename "$0")
if [ "${1:-}" = --version ]; then
 [ "$CHECK_CASE" != no-codeql ] || exit 1
 echo 2.27.2
 exit
fi
printf '%s\n' "$name" >> "$CHECK_EVENTS"
[ "$CHECK_CASE$name" != changedcodeql-security ] || touch "$CHECK_DIRTY"
[ "$CHECK_CASE" != "$name" ]
"""
STUB = r"""record() {
 printf '%s\n' "$1" >> "$CHECK_EVENTS"
 [ "$CHECK_CASE" != "$1" ]
}
dirty() { [ "$CHECK_CASE" = dirty ] || [ -e "$CHECK_DIRTY" ]; }
git() {
 case "$1 $2" in
  'rev-parse HEAD') echo abc123;;
  'status --porcelain') if dirty; then echo ' M README.md'; fi;;
  'grep -nP')
   printf '%s\n' ignores >> "$CHECK_EVENTS"
   command git "$@";;
  *) exit 99;;
 esac
}
gh() {
 [ "$1 $2" = 'api --silent' ] || exit 99
 case "$3" in
  repos/Xquik-dev/hermes-tweet/commits/abc123) [ "$CHECK_CASE" != unpushed ];;
  repos/Xquik-dev/hermes-tweet/statuses/abc123)
   [ "$4 $6 $7 $8" = '-f -f context=xquik-local-checks -f' ] || exit 99
   [ "$#" = 9 ] || exit 99
   printf '%s: %s\n' "${5#state=}" "${9#description=}" >> "$CHECK_STATUSES";;
  *) exit 99;;
 esac
}
uv() {
 [ "$UV_PYTHON" = 3.12 ] && [ "${UV_PROJECT_ENVIRONMENT##*/}" = venv ] || exit 99
 case "$*" in
  'sync --locked --group dev') record sync;;
  'run --no-sync ruff format --check .') record format;;
  'run --no-sync ruff check --ignore-noqa .') record lint;;
  'run --no-sync basedpyright') record types;;
  'run --no-sync mypy --any-exprs-report '*)
   mkdir -p "$5"
   anys=0
   [ "$CHECK_CASE" != any ] || anys=1
   printf 'Total %s 10 90.00%%\n' "$anys" > "$5/any-exprs.txt"
   record mypy;;
  'run --no-sync python scripts/check_hermes_agent_compat.py')
   record "compatibility with token ${GITHUB_TOKEN:-none} ${GH_TOKEN:-none}";;
  'run --no-sync python scripts/check_public_safety.py') record safety;;
  'run --no-sync python scripts/check_license_headers.py') record licenses;;
  "run --no-sync pytest $COVERAGE")
   echo "===== 183 passed in 1.00s ====="
   record tests;;
  'run --no-sync bandit -c pyproject.toml -r hermes_tweet scripts fuzz') record bandit;;
  'run --no-sync pip-audit') record audit;;
  'run --no-sync python -m build --outdir '*) record "build at $SOURCE_DATE_EPOCH";;
  'run --no-sync twine check '*) record metadata;;
  *) exit 99;;
 esac
}
export -f record dirty git gh uv
runner=$1; shift
bash "$runner" "$@"
"""
COVERAGE = "--cov=hermes_tweet --cov=tests --cov-report=term-missing --cov-fail-under=100"
COMPATIBILITY = "compatibility with token none none"
CHECKS = [
    "sync",
    "format",
    "lint",
    "ignores",
    "types",
    "mypy",
    COMPATIBILITY,
    "safety",
    "licenses",
    "tests",
    "bandit",
    "audit",
    "check_reproducible.sh",
    "build at 946684800",
    "metadata",
    "plugin-scan",
    "codeql-security",
]
FAILURES = [
    ("sync", "Install locked dependencies on Python 3.12"),
    ("format", "Format check"),
    ("lint", "Lint"),
    ("types", "Type check"),
    ("mypy", "Type check with mypy"),
    (COMPATIBILITY, "Hermes Agent compatibility"),
    ("safety", "Public safety scan"),
    ("licenses", "License header check"),
    ("tests", "Tests with 100% coverage"),
    ("bandit", "Security scan with Bandit"),
    ("audit", "Dependency audit"),
    ("check_reproducible.sh", "Reproducible package"),
    ("build at 946684800", "Package build and metadata"),
    ("metadata", "Package build and metadata"),
    ("plugin-scan", "Plugin scan with a minimum score of 80"),
    ("codeql-security", "Static analysis with CodeQL 2.27.2 security-extended queries"),
]
PENDING = "pending: Running lint, types, safety, tests, audit, build, plugin scan & CodeQL."
PASSED = (
    "format, lint, types, compatibility, safety, licenses, tests (183 passed), Bandit, audit, "
    "build, plugin scan, CodeQL 2.27.2."
)
INHERITED = ("UV_PYTHON", "UV_PROJECT_ENVIRONMENT")


def run_checks(
    tmp_path: Path, case: str, *arguments: str, source: str = ""
) -> tuple[int, list[str], list[str]]:
    project = tmp_path / "project"
    for folder in ("bin", "scripts"):
        (project / folder).mkdir(parents=True)
    subprocess.run([GIT, "init", "-q", str(project)], check=True)
    if source:
        (project / "probe.py").write_text(source)
    runner = project / "bin/check-local"
    runner.write_bytes((ROOT / "bin/check-local").read_bytes())
    for name in ("codeql-security", "plugin-scan", "check_reproducible.sh"):
        (project / "scripts" / name).write_text(SCRIPT)
    events, statuses = tmp_path / "events", tmp_path / "statuses"
    events.touch()
    statuses.touch()
    result = subprocess.run(
        [BASH, "-c", STUB, "check-local-test", str(runner), *arguments],
        env={
            **{key: value for key, value in os.environ.items() if key not in INHERITED},
            "CHECK_CASE": case,
            "CHECK_EVENTS": str(events),
            "CHECK_STATUSES": str(statuses),
            "CHECK_DIRTY": str(tmp_path / "dirty"),
            "COVERAGE": COVERAGE,
            "GITHUB_TOKEN": "isolated-fixture-token",
            "GH_TOKEN": "isolated-fixture-token",
        },
        capture_output=True,
        text=True,
        check=False,
    )
    output = (result.stdout + result.stderr).splitlines()
    return (
        result.returncode,
        events.read_text().splitlines(),
        [*statuses.read_text().splitlines(), *output],
    )


def test_success_status_lists_the_checks_that_passed(tmp_path: Path) -> None:
    status, events, report = run_checks(tmp_path, "ready")
    assert status == 0, report
    assert events == CHECKS
    assert report[:2] == [PENDING, f"success: Passed {PASSED}"]
    assert len(f"Passed {PASSED}") < 139
    assert report[-1] == f"All local checks passed. They were {PASSED}"


def test_any_expression_fails_the_mypy_step(tmp_path: Path) -> None:
    status, events, report = run_checks(tmp_path, "any")
    assert status != 0
    assert events == CHECKS[: CHECKS.index("mypy") + 1]
    assert report[:2] == [PENDING, "failure: Failed at Type check with mypy."]
    assert "Total 1 10 90.00%" in report


@pytest.mark.parametrize(
    "comment",
    [
        "type: ignore[assignment]",
        "pyright: ignore[reportAssignmentType]",
        "mypy: ignore-errors",
        "pyright: basic",
    ],
)
def test_type_checker_comments_fail_the_build(tmp_path: Path, comment: str) -> None:
    line = f'x: int = "a"  # {comment}'
    status, events, report = run_checks(tmp_path, "ready", source=f"{line}\n")
    assert status == 1
    assert events == CHECKS[: CHECKS.index("ignores") + 1]
    assert report[:2] == [PENDING, "failure: Failed at Type checker comments."]
    assert f"probe.py:1:{line}" in report


@pytest.mark.parametrize("failure", FAILURES)
def test_failed_check_posts_failure_and_stops(tmp_path: Path, failure: tuple[str, str]) -> None:
    status, events, report = run_checks(tmp_path, failure[0])
    assert status != 0
    assert events == CHECKS[: CHECKS.index(failure[0]) + 1]
    assert report[:2] == [PENDING, f"failure: Failed at {failure[1]}."]


@pytest.mark.parametrize(
    ("case", "status", "events", "failed"),
    [("no-codeql", 1, [], "CodeQL CLI"), ("changed", 1, CHECKS, "Final tree check")],
)
def test_failure_outside_a_check_posts_failure(
    tmp_path: Path, case: str, status: int, events: list[str], failed: str
) -> None:
    observed_status, observed, report = run_checks(tmp_path, case)
    assert observed_status == status
    assert observed == events
    assert report[:2] == [PENDING, f"failure: Failed at {failed}."]


@pytest.mark.parametrize(
    ("case", "arguments", "reason"),
    [
        ("ready", ["--no-status"], "--no-status was passed."),
        ("dirty", [], "the tree has uncommitted changes."),
        ("unpushed", [], "GitHub does not have HEAD, or gh is signed out. Push first."),
    ],
)
def test_status_is_posted_only_for_a_clean_pushed_commit(
    tmp_path: Path, case: str, arguments: list[str], reason: str
) -> None:
    status, events, report = run_checks(tmp_path, case, *arguments)
    assert status == 0, report
    assert events == CHECKS
    assert report[0] == f"==> Commit status not posted because {reason}"


def test_unknown_option_stops_before_any_check(tmp_path: Path) -> None:
    status, events, report = run_checks(tmp_path, "ready", "--skip")
    assert status == 2
    assert events == []
    assert report == ["check-local: unknown option --skip. Use --no-status or no option."]
