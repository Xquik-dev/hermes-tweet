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
# The stubs record each release step as an event.
# RELEASE_CASE picks the state they report.
STUB = r"""record() { printf '%s\n' "$1" >> "$RELEASE_EVENTS"; }
git() {
 case "$1" in
  remote) echo git@github.com:Xquik-dev/hermes-tweet.git;;
  status) [ "$RELEASE_CASE" != dirty ] || echo ' M README.md';;
  symbolic-ref) if [ "$RELEASE_CASE" = branch ]; then echo topic; else echo master; fi;;
  fetch) [ "$*" = 'fetch --quiet origin master' ] || exit 99;;
  rev-parse)
   case "$*" in
    *refs/tags/*) return 1;;
    *origin/master*) if [ "$RELEASE_CASE" = behind ]; then echo def; else echo abc; fi;;
    *) echo abc;;
   esac;;
  ls-remote) [ "$RELEASE_CASE" = tagged ] || return 2;;
  tag) record "tag $3 $6";;
  push) record "push $3";;
  *) exit 99;;
 esac
}
uv() {
 case "$*" in
  'version --short') echo 1.2.3;;
  'run --locked --group dev python scripts/check_public_links.py') record links;;
  'run --locked --group dev python -m build --outdir '*)
   record "build at $SOURCE_DATE_EPOCH"
   mkdir -p "$9"
   for suffix in -py3-none-any.whl .tar.gz; do
    echo fixture > "$9/hermes_tweet-1.2.3$suffix"
   done;;
  'run --locked --group dev twine check '*) record metadata;;
  'publish '*)
   [ "$UV_PUBLISH_TOKEN" = isolated-fixture-token ] && [ "$#" = 7 ] || exit 99
   [ "$2 $3" = '--publish-url https://upload.pypi.org/legacy/' ] || exit 99
   [ "$4 $5" = '--check-url https://pypi.org/simple/' ] || exit 99
   record publish;;
  *) exit 99;;
 esac
}
gh() {
 case "$1 $2" in
  'auth status') :;;
  'release create')
   [ "$3 ${4##*/} ${5##*/}" = "v1.2.3 $RELEASE_FILES" ] || exit 99
   shift 5
   [ "$*" = "--repo Xquik-dev/hermes-tweet $RELEASE_OPTIONS" ] || exit 99
   record "release v1.2.3";;
  *) exit 99;;
 esac
}
curl() {
 case "$*" in
  *--write-out*) printf '%s' "$RELEASE_PYPI";;
  *)
   record verify
   digest=$(echo "$RELEASE_UPLOADED" | shasum -a 256 | cut -d ' ' -f 1)
   echo "{\"sha256\":\"$digest\"}";;
 esac
 while [ "$#" -gt 1 ]; do shift; done
 [ "$1" = https://pypi.org/pypi/hermes-tweet/1.2.3/json ] || exit 99
}
security() {
 [ -n "${PYPI_KEYCHAIN_SERVICE:-}" ] || exit 99
 [ "$1 $2 $3" = "find-generic-password -s $PYPI_KEYCHAIN_SERVICE" ] || exit 99
 [ "$RELEASE_CASE" != keychain ] || return 44
 [ "${4:-}" != -w ] || echo isolated-fixture-token
}
sleep() { record "sleep $1"; }
export -f record git uv gh curl security sleep
runner=$1; shift
bash "$runner" "$@"
"""
CHECKS = "#!/usr/bin/env bash\nprintf 'checks\\n' >> \"$RELEASE_EVENTS\"\n"
CHECKED = ["checks", "links", "build at 946684800", "metadata"]
RELEASED = ["tag v1.2.3 abc", "push refs/tags/v1.2.3", "release v1.2.3"]
PUBLISHER = "test-publisher"
DRY_RUN_END = "Dry run finished for hermes-tweet 1.2.3. Nothing was uploaded, tagged, or released."
DIFFERENT = (
    "release-local: PyPI files differ from this build or are not visible yet. "
    "Compare them before tagging."
)
TAGGED = (
    "release-local: Tag v1.2.3 already exists on origin. "
    "Bump the version in pyproject.toml, then rerun."
)
NO_KEYCHAIN_ITEM = (
    "release-local: The Keychain has no item named by PYPI_KEYCHAIN_SERVICE. "
    "Add the PyPI token under that name, then run bin/release-local again."
)
NO_ITEM_NAME = (
    "release-local: PYPI_KEYCHAIN_SERVICE is unset. "
    "Set it to the Keychain item that holds the PyPI token, then run bin/release-local again."
)
REFUSALS: list[tuple[list[str], str, str, tuple[int, str]]] = [
    ([], "dirty", "404", (1, "release-local: Commit or remove local changes, then rerun.")),
    (
        ["--dry-run"],
        "dirty",
        "404",
        (1, "release-local: Commit or remove local changes, then rerun."),
    ),
    ([], "branch", "404", (1, "release-local: Switch to master, then rerun.")),
    ([], "behind", "404", (1, "release-local: Make master equal to origin/master, then rerun.")),
    ([], "tagged", "404", (1, TAGGED)),
    ([], "keychain", "404", (1, NO_KEYCHAIN_ITEM)),
    ([], "ready", "503", (1, "release-local: PyPI returned HTTP 503. Retry later.")),
    (
        ["--publish"],
        "ready",
        "404",
        (2, "release-local: unknown option --publish. Use --dry-run or no option."),
    ),
]


def run_release(
    tmp_path: Path, arguments: list[str], case: str, pypi: str, service: str | None = PUBLISHER
) -> tuple[int, list[str], str]:
    project = tmp_path / "project"
    (project / "bin").mkdir(parents=True)
    runner = project / "bin/release-local"
    runner.write_bytes((ROOT / "bin/release-local").read_bytes())
    checks = project / "bin/check-local"
    checks.write_text(CHECKS)
    checks.chmod(0o755)
    events = tmp_path / "events"
    events.touch()
    environment = {
        key: value for key, value in os.environ.items() if key != "PYPI_KEYCHAIN_SERVICE"
    }
    environment.update(
        RELEASE_CASE=case,
        RELEASE_PYPI=pypi,
        RELEASE_EVENTS=str(events),
        RELEASE_UPLOADED="other" if case == "mismatch" else "fixture",
        RELEASE_RETRY_SECONDS="0",
        RELEASE_FILES="hermes_tweet-1.2.3-py3-none-any.whl hermes_tweet-1.2.3.tar.gz",
        RELEASE_OPTIONS="--verify-tag --title v1.2.3 --generate-notes --latest",
    )
    if service is not None:
        environment["PYPI_KEYCHAIN_SERVICE"] = service
    result = subprocess.run(
        [BASH, "-c", STUB, "release-local-test", str(runner), *arguments],
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    output = result.stdout + result.stderr
    assert "isolated-fixture-token" not in output
    assert PUBLISHER not in output
    return result.returncode, events.read_text().splitlines(), output.splitlines()[-1]


@pytest.mark.parametrize(
    ("pypi", "events"),
    [("404", [*CHECKED, "publish", "verify", *RELEASED]), ("200", [*CHECKED, "verify", *RELEASED])],
)
def test_release_uploads_once_then_tags_and_releases(
    tmp_path: Path, pypi: str, events: list[str]
) -> None:
    status, observed, last_line = run_release(tmp_path, [], "ready", pypi)
    assert status == 0, last_line
    assert observed == events
    assert last_line == "Released hermes-tweet 1.2.3 as v1.2.3."


@pytest.mark.parametrize(
    ("case", "pypi", "events"),
    [("ready", "404", CHECKED), ("ready", "200", [*CHECKED, "verify"]), ("branch", "404", CHECKED)],
)
def test_dry_run_needs_no_token_and_releases_nothing(
    tmp_path: Path, case: str, pypi: str, events: list[str]
) -> None:
    status, observed, last_line = run_release(tmp_path, ["--dry-run"], case, pypi, service=None)
    assert status == 0, last_line
    assert observed == events
    assert last_line == DRY_RUN_END


def test_release_never_tags_files_that_differ_from_pypi(tmp_path: Path) -> None:
    status, observed, last_line = run_release(tmp_path, [], "mismatch", "200")
    assert status == 1
    assert observed == [*CHECKED, *["verify", "sleep 0"] * 4, "verify"]
    assert last_line == DIFFERENT


@pytest.mark.parametrize(("arguments", "case", "pypi", "expected"), REFUSALS)
def test_release_refuses_before_any_upload(
    tmp_path: Path, arguments: list[str], case: str, pypi: str, expected: tuple[int, str]
) -> None:
    status, observed, last_line = run_release(tmp_path, arguments, case, pypi)
    assert (status, last_line) == expected
    assert not {"publish", "verify", *RELEASED} & set(observed)


@pytest.mark.parametrize("service", [None, ""])
def test_release_stops_when_the_token_item_is_not_named(
    tmp_path: Path, service: str | None
) -> None:
    status, observed, last_line = run_release(tmp_path, [], "ready", "404", service=service)
    assert status == 1
    assert last_line == NO_ITEM_NAME
    assert observed == []
