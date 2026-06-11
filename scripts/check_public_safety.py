from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

ROOT = Path(__file__).parents[1]
PUBLIC_TEXT_FILES = (
    "AGENTS.md",
    "README.md",
    "after-install.md",
    "docs/CONTEXT7.md",
    "docs/ECOSYSTEM.md",
    "docs/GITHUB_METADATA.md",
    "docs/HERMES_SURFACES.md",
    "docs/INTEGRATION_PATTERNS.md",
    "docs/OBSERVABILITY.md",
    "docs/PUBLICATION_CHECKLIST.md",
    "docs/SUBMISSION_READINESS.md",
    "pyproject.toml",
    "plugin.yaml",
    "hermes_tweet/plugin.yaml",
    "skill.json",
    "dashboard/manifest.json",
    ".hermes-eco.json",
    "skills/hermes-tweet/SKILL.md",
    "hermes_tweet/skills/hermes-tweet/SKILL.md",
    "registries/ask/hermes-tweet/SKILL.md",
)
SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("github-token", re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}")),
    ("openai-key", re.compile(r"sk-[A-Za-z0-9_-]{20,}")),
    ("aws-access-key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("xquik-api-key", re.compile(r"xq_[A-Za-z0-9_-]{12,}")),
    ("bearer-token", re.compile(r"Bearer\s+[A-Za-z0-9._~+/-]{20,}")),
)
SAFE_PLACEHOLDERS = (
    "xq_...",
    "xq_your_key",
    "xq_test",
    "Bearer token",
)
PRIVATE_TEXT_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("internal-cost", re.compile(r"\binternal cost\b", re.IGNORECASE)),
    ("private-vendor", re.compile(r"\bprivate vendor\b", re.IGNORECASE)),
    ("runtime-artifact", re.compile(r"\b(login|write) screenshots?\b", re.IGNORECASE)),
)


@dataclass(frozen=True)
class PublicSafetyFinding:
    path: Path
    line_number: int
    label: str


def is_safe_placeholder(line: str) -> bool:
    return any(placeholder in line for placeholder in SAFE_PLACEHOLDERS)


def scan_line(path: Path, line_number: int, line: str) -> list[PublicSafetyFinding]:
    findings: list[PublicSafetyFinding] = []
    if not is_safe_placeholder(line):
        findings.extend(
            PublicSafetyFinding(path, line_number, label)
            for label, pattern in SECRET_PATTERNS
            if pattern.search(line)
        )

    findings.extend(
        PublicSafetyFinding(path, line_number, label)
        for label, pattern in PRIVATE_TEXT_PATTERNS
        if pattern.search(line)
    )
    return findings


def scan_public_files(files: Iterable[str] = PUBLIC_TEXT_FILES) -> list[PublicSafetyFinding]:
    findings: list[PublicSafetyFinding] = []
    for file_name in files:
        path = ROOT / file_name
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            findings.extend(scan_line(path.relative_to(ROOT), line_number, line))
    return findings


def format_finding(finding: PublicSafetyFinding) -> str:
    return f"{finding.path}:{finding.line_number}: {finding.label}"


def main(argv: Sequence[str] | None = None) -> int:
    files = tuple(argv) if argv else PUBLIC_TEXT_FILES
    findings = scan_public_files(files)
    print(f"checked={len(files)} findings={len(findings)}")
    for finding in findings:
        print(format_finding(finding))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
