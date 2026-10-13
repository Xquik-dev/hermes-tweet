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
# The uv stub records each call. It builds a scanner that records its own call.
# The uname stub reports macOS, so the fuzz script never starts a fuzzer here.
# The ssh stub records the remote command and discards the source it is sent.
STUB = r"""uv() {
 case "$1 $2" in
  'venv --quiet')
   mkdir -p "$5/bin"
   printf '#!/bin/sh\necho "scanner $*" >> "%s"\nenv >> "%s"\nexit %s\n' \
    "$EVENTS" "$SCANNER_ENVIRONMENT" "$SCAN_EXIT" > "$5/bin/plugin-scanner"
   chmod +x "$5/bin/plugin-scanner"
   echo "venv $3 $4" >> "$EVENTS";;
  'pip install')
   shift 5
   case "$*" in
    '--no-deps --require-hashes --requirement '*) echo "pinned $(cat "$4")" >> "$EVENTS";;
    *) echo "dependencies $*" >> "$EVENTS";;
   esac;;
  *) exit 99;;
 esac
}
uname() { if [ "$1" = -s ]; then echo Darwin; else echo arm64; fi; }
ssh() {
 cat > /dev/null
 echo "ssh $*" >> "$EVENTS"
}
export -f uv uname ssh
runner=$1; shift
bash "$runner" "$@"
"""
SCANNER = "plugin-scanner==2.0.1116"
DIGEST = "40d40308484e49b438c6ef47a7794ab6aac617914447174f80fe4578911cdcb3"
SCANNED = (
    "scanner scan . --format text --profile default "
    "--min-score 80 --fail-on-severity high --cisco-skill-scan auto"
)
SCAN = [
    "venv --python 3.12",
    f"pinned {SCANNER} --hash=sha256:{DIGEST}",
    f"dependencies {SCANNER}",
    SCANNED,
]
NOT_LINUX = "Use Linux x86_64 or set XQUIK_FUZZ_HOST to an authorized Linux SSH runner."
BAD_HOST = "Invalid SSH host. Set XQUIK_FUZZ_HOST to a host name or user@host."
BAD_DURATION = "Invalid duration. Pass a whole number of seconds, such as 600."


def run_script(
    tmp_path: Path, script: str, arguments: list[str], host: str, scan_exit: str = "0"
) -> tuple[int, list[str], str]:
    events = tmp_path / "events"
    events.touch()
    result = subprocess.run(
        [BASH, "-c", STUB, "script-test", str(ROOT / script), *arguments],
        env={
            **os.environ,
            "EVENTS": str(events),
            "SCAN_EXIT": scan_exit,
            "SCANNER_ENVIRONMENT": str(tmp_path / "scanner-environment"),
            "GITHUB_TOKEN": "isolated-fixture-token",
            "TMPDIR": str(tmp_path),
            "XQUIK_FUZZ_HOST": host,
        },
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode, events.read_text().splitlines(), result.stderr


@pytest.mark.parametrize("scan_exit", ["0", "1"])
def test_plugin_scan_pins_the_scanner_and_returns_its_result(
    tmp_path: Path, scan_exit: str
) -> None:
    status, events, _ = run_script(tmp_path, "scripts/plugin-scan", [], "", scan_exit)
    assert status == int(scan_exit)
    assert events == SCAN
    names = {
        line.partition("=")[0]
        for line in (tmp_path / "scanner-environment").read_text().splitlines()
    }
    assert names - {"PWD", "SHLVL", "_", "OLDPWD"} == {"HOME", "PATH", "TMPDIR"}


@pytest.mark.parametrize(
    ("arguments", "host", "expected"),
    [
        ([], "", (1, NOT_LINUX)),
        (["600"], "", (1, NOT_LINUX)),
        ([], "-oProxyCommand=id", (2, BAD_HOST)),
        ([], "runner;id", (2, BAD_HOST)),
        (["soon"], "", (2, BAD_DURATION)),
        (["0"], "runner", (2, BAD_DURATION)),
    ],
)
def test_fuzz_refuses_before_it_starts(
    tmp_path: Path, arguments: list[str], host: str, expected: tuple[int, str]
) -> None:
    status, events, errors = run_script(tmp_path, "scripts/fuzz", arguments, host)
    assert (status, errors) == (expected[0], f"{expected[1]}\n")
    assert events == []


def test_fuzz_sends_the_source_and_the_duration_to_the_runner(tmp_path: Path) -> None:
    status, events, errors = run_script(tmp_path, "scripts/fuzz", ["600"], "fuzz@runner")
    assert (status, errors) == (0, "")
    assert len(events) == 1
    assert events[0].startswith("ssh -- fuzz@runner set -eu; umask 077; ")
    assert events[0].endswith("; unset XQUIK_FUZZ_HOST; bash scripts/fuzz 600")
