from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

PUBLIC_SURFACE_FILES = (
    ".github/CONTRIBUTING.md",
    ".github/FUNDING.yml",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/SECURITY.md",
    ".github/dependabot.yml",
    ".github/workflows/ci.yml",
    ".github/workflows/publish.yml",
    "AGENTS.md",
    "CODE_OF_CONDUCT.md",
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


def select_public_surface_files(argv: Sequence[str] | None) -> tuple[str, ...]:
    if not argv:
        return PUBLIC_SURFACE_FILES

    public_files = set(PUBLIC_SURFACE_FILES)
    unknown_files = tuple(file_name for file_name in argv if file_name not in public_files)
    if unknown_files:
        unknown_list = ", ".join(unknown_files)
        message = f"unregistered public files: {unknown_list}"
        raise ValueError(message)

    return tuple(argv)
