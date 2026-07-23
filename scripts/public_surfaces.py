# SPDX-FileCopyrightText: 2026 Xquik Contributors
# SPDX-License-Identifier: MIT

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

ROOT = Path(__file__).parents[1]
PUBLIC_SURFACE_FILES = (
    ".github/CONTRIBUTING.md",
    ".github/FUNDING.yml",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/SECURITY.md",
    ".github/dependabot.yml",
    ".github/workflows/ci.yml",
    ".github/workflows/clusterfuzzlite.yml",
    ".github/workflows/hol-plugin-scanner.yml",
    ".github/workflows/publish.yml",
    ".clusterfuzzlite/Dockerfile",
    ".clusterfuzzlite/build.sh",
    ".clusterfuzzlite/project.yaml",
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
    ".codexignore",
    ".dockerignore",
    "AGENTS.md",
    "CODE_OF_CONDUCT.md",
    "README.md",
    "SECURITY.md",
    "after-install.md",
    "assets/icon.svg",
    "assets/screenshot.svg",
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
    "skills/hermes-tweet/skill-card.md",
    "skills/hermes-tweet/references/endpoint-contract.md",
    "hermes_tweet/skills/hermes-tweet/SKILL.md",
    "hermes_tweet/skills/hermes-tweet/skill-card.md",
    "hermes_tweet/skills/hermes-tweet/references/endpoint-contract.md",
    "registries/ask/hermes-tweet/SKILL.md",
)


def normalize_public_surface_file(file_name: str) -> str:
    path = Path(file_name)
    root = ROOT.resolve()
    candidate = path if path.is_absolute() else ROOT / path
    try:
        return candidate.resolve(strict=False).relative_to(root).as_posix()
    except ValueError:
        normalized = file_name

    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def find_duplicate_files(files: Sequence[str]) -> tuple[str, ...]:
    seen_files: set[str] = set()
    reported_files: set[str] = set()
    duplicate_files: list[str] = []
    for file_name in files:
        if file_name in seen_files:
            if file_name in reported_files:
                continue
            reported_files.add(file_name)
            duplicate_files.append(file_name)
            continue
        seen_files.add(file_name)
    return tuple(duplicate_files)


def select_public_surface_files(argv: Sequence[str] | None) -> tuple[str, ...]:
    if not argv:
        return PUBLIC_SURFACE_FILES

    requested_files = tuple(normalize_public_surface_file(file_name) for file_name in argv)
    public_files = set(PUBLIC_SURFACE_FILES)
    unknown_files = tuple(
        file_name for file_name in requested_files if file_name not in public_files
    )
    if unknown_files:
        unknown_list = ", ".join(unknown_files)
        message = f"unregistered public files: {unknown_list}"
        raise ValueError(message)

    duplicate_files = find_duplicate_files(requested_files)
    if duplicate_files:
        duplicate_list = ", ".join(duplicate_files)
        message = f"duplicate public files: {duplicate_list}"
        raise ValueError(message)

    return requested_files
