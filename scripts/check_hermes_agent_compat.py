# SPDX-FileCopyrightText: 2026 Xquik Contributors
# SPDX-License-Identifier: MIT

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final, cast

import httpx

if TYPE_CHECKING:
    from collections.abc import Sequence

USER_AGENT: Final = "HermesTweetHermesAgentCompat/1.0"
GITHUB_CONTENT_URL: Final = "https://api.github.com/repos/NousResearch/hermes-agent/contents"
DOC_TIMEOUT_SECONDS: Final = 30.0


@dataclass(frozen=True)
class PageCheck:
    name: str
    url: str
    required_terms: tuple[str, ...]


@dataclass(frozen=True)
class SourceCheck:
    path: str
    expected_sha: str
    required_terms: tuple[str, ...]


@dataclass(frozen=True)
class SourceContent:
    sha: str
    text: str


PAGE_CHECKS: Final = (
    PageCheck(
        name="Build a Hermes Plugin",
        url="https://hermes-agent.nousresearch.com/docs/developer-guide/plugins",
        required_terms=(
            "plugin.yaml",
            "requires_env",
            "ctx.register_skill",
            "ctx.register_command",
            "ctx.dispatch_tool",
            "hermes plugins list",
        ),
    ),
    PageCheck(
        name="Plugins guide",
        url="https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins/",
        required_terms=(
            "plugin.yaml",
            "requires_env",
            "ctx.register_skill",
            "hermes plugins",
            "plugins.enabled",
            "HERMES_ENABLE_PROJECT_PLUGINS",
            "hermes_agent.plugins",
        ),
    ),
)

SOURCE_CHECKS: Final = (
    SourceCheck(
        path="hermes_cli/plugins.py",
        expected_sha="2493d8f21eddc0617d04e9ee48812846086eade4",
        required_terms=(
            "ENTRY_POINTS_GROUP",
            "discover_entrypoint_manifests",
            "hermes_agent.plugins",
            "plugins.enabled",
            "HERMES_ENABLE_PROJECT_PLUGINS",
            "HERMES_SAFE_MODE",
            "def register_tool",
            "def register_skill",
            "def register_command",
            "requires_env",
            "check_fn",
        ),
    ),
    SourceCheck(
        path="tools/registry.py",
        expected_sha="081040911499f8bb7e5a947e9c85b5e459fd3dd0",
        required_terms=(
            "check_fn",
            "requires_env",
            "get_definitions",
            "dispatch",
            "json.dumps",
        ),
    ),
    SourceCheck(
        path="hermes_cli/plugins_cmd.py",
        expected_sha="912d93208d2169f2a51bff4dc8b6fed1dfd204c0",
        required_terms=(
            "_resolve_plugin_key",
            "_scan_plugin_tree",
            "_resolve_subdir_within",
            "nested category plugins",
            "requires_env",
            "--enable",
            "--no-enable",
            "plugins.enabled",
            "enable",
            "disable",
            "install",
        ),
    ),
)


def missing_terms(text: str, required_terms: Sequence[str]) -> list[str]:
    return [term for term in required_terms if term not in text]


def github_headers() -> dict[str, str]:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": USER_AGENT}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def check_page(client: httpx.Client, check: PageCheck) -> list[str]:
    try:
        response = client.get(check.url)
        response.raise_for_status()
    except httpx.HTTPError as error:
        return [f"{check.name} check failed. Retry after {error.__class__.__name__}."]

    missing = missing_terms(response.text, check.required_terms)
    if missing:
        return [f"{check.name} is outdated. Add these terms: {', '.join(missing)}"]

    print(f"Docs verified. {check.name} {check.url}")
    return []


def read_source(client: httpx.Client, path: str) -> tuple[SourceContent | None, list[str]]:
    api_url = f"{GITHUB_CONTENT_URL}/{path}?ref=main"
    try:
        response = client.get(api_url)
        response.raise_for_status()
    except httpx.HTTPError as error:
        return None, [f"Metadata fetch failed for {path}. Retry after {error.__class__.__name__}."]

    payload = response.json()
    if not isinstance(payload, dict):
        return None, [f"Invalid GitHub response for {path}. Expected an object."]

    mapping = cast("dict[str, object]", payload)
    sha = mapping.get("sha")
    download_url = mapping.get("download_url")
    if not isinstance(sha, str) or not isinstance(download_url, str):
        return None, [f"Incomplete GitHub response for {path}. Expected sha and download_url."]

    try:
        raw_response = client.get(download_url)
        raw_response.raise_for_status()
    except httpx.HTTPError as error:
        return None, [f"Source fetch failed for {path}. Retry after {error.__class__.__name__}."]

    return SourceContent(sha=sha, text=raw_response.text), []


def check_source(client: httpx.Client, check: SourceCheck) -> list[str]:
    content, errors = read_source(client, check.path)
    if content is None:
        return errors

    if content.sha != check.expected_sha:
        return [
            (
                f"Source changed for {check.path}: {check.expected_sha} to {content.sha}. "
                "Review the official Hermes Agent diff before updating this lock."
            )
        ]

    missing = missing_terms(content.text, check.required_terms)
    if missing:
        return [f"{check.path} is outdated. Add these terms: {', '.join(missing)}"]

    print(f"Source verified. {check.path} {content.sha}")
    return []


def run_checks() -> list[str]:
    timeout = httpx.Timeout(DOC_TIMEOUT_SECONDS)
    errors: list[str] = []

    with httpx.Client(follow_redirects=True, headers=github_headers(), timeout=timeout) as client:
        for page_check in PAGE_CHECKS:
            errors.extend(check_page(client, page_check))
        for source_check in SOURCE_CHECKS:
            errors.extend(check_source(client, source_check))

    return errors


def main() -> int:
    errors = run_checks()
    if errors:
        print("Hermes Agent compatibility failed. Review each item below.")
        for error in errors:
            print(error)
        return 1

    print("Hermes Agent compatibility passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
