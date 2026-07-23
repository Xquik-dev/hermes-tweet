# SPDX-FileCopyrightText: 2026 Xquik Contributors
# SPDX-License-Identifier: MIT

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

ROOT = Path(__file__).parents[1]
COPYRIGHT_NOTICE = "# SPDX-FileCopyrightText: 2026 Xquik Contributors"
LICENSE_NOTICE = "# SPDX-License-Identifier: MIT"
SOURCE_SUFFIXES = frozenset({".in", ".py", ".sh", ".toml", ".yaml", ".yml"})
SOURCE_NAMES = frozenset({"Dockerfile"})
IGNORED_DIRECTORY_NAMES = frozenset(
    {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        "__pycache__",
        "build",
        "dist",
    }
)


@dataclass(frozen=True)
class LicenseHeaderFinding:
    path: Path
    missing_notice: str


def select_source_files(root: Path = ROOT) -> tuple[Path, ...]:
    return tuple(
        sorted(
            path
            for path in root.rglob("*")
            if path.is_file()
            and not IGNORED_DIRECTORY_NAMES.intersection(path.relative_to(root).parts)
            and (path.suffix in SOURCE_SUFFIXES or path.name in SOURCE_NAMES)
        )
    )


def scan_source_file(path: Path, root: Path = ROOT) -> list[LicenseHeaderFinding]:
    header = path.read_text(encoding="utf-8").splitlines()[:5]
    relative_path = path.relative_to(root)
    findings: list[LicenseHeaderFinding] = []
    if COPYRIGHT_NOTICE not in header:
        findings.append(LicenseHeaderFinding(relative_path, "copyright"))
    if LICENSE_NOTICE not in header:
        findings.append(LicenseHeaderFinding(relative_path, "license"))
    return findings


def scan_source_files(root: Path = ROOT) -> list[LicenseHeaderFinding]:
    return [
        finding for path in select_source_files(root) for finding in scan_source_file(path, root)
    ]


def format_finding(finding: LicenseHeaderFinding) -> str:
    return f"{finding.path}: missing {finding.missing_notice} notice"


def main(argv: Sequence[str] | None = None) -> int:
    if argv:
        print("check_license_headers.py does not accept arguments")
        return 1

    source_files = select_source_files()
    findings = scan_source_files()
    print(f"checked={len(source_files)} findings={len(findings)}")
    for finding in findings:
        print(format_finding(finding))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
