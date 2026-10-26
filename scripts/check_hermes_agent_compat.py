# SPDX-FileCopyrightText: 2026 Xquik Contributors
# SPDX-License-Identifier: MIT

from __future__ import annotations

import hashlib
import json
import os
import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final, Protocol

import httpx

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from hermes_tweet.client import JsonValue

USER_AGENT: Final = "HermesTweetHermesAgentCompat/1.0"
LATEST_RELEASE_URL: Final = "https://api.github.com/repos/NousResearch/hermes-agent/releases/latest"
SOURCE_URL: Final = "https://raw.githubusercontent.com/NousResearch/hermes-agent"
REVIEWED_RELEASE: Final = "v0.22.2"
DEVELOPMENT_BRANCH: Final = "main"
DOC_TIMEOUT_SECONDS: Final = 30.0

_decode_json: Callable[[bytes], JsonValue] = json.loads


class SourceResponse(Protocol):
    @property
    def text(self) -> str: ...

    @property
    def content(self) -> bytes: ...

    def raise_for_status(self) -> object: ...


class SourceClient(Protocol):
    def get(self, url: str, *, headers: dict[str, str] | None = None) -> SourceResponse: ...


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
class CorePinCheck:
    path: str
    required_pin: str
    next_step: str


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
        expected_sha="a652179cd4a7a3ac04fe7eb2a0377de6a6dfbc58",
        required_terms=(
            "ENTRY_POINTS_GROUP",
            "discover_entrypoint_manifests",
            "hermes_agent.plugins",
            "plugins.enabled",
            "HERMES_ENABLE_PROJECT_PLUGINS",
            "HERMES_SAFE_MODE",
            "def register_tool",
            "def register_command",
            "from hermes_cli.plugins_content import",
            "register_skill",
            "requires_env",
            "check_fn",
        ),
    ),
    SourceCheck(
        path="hermes_cli/plugins_content.py",
        expected_sha="92b8d79f5440e58d421a6018d4c6d12e9aef107b",
        required_terms=(
            "def register_skill",
            "SKILL.md not found",
            "skill_namespace",
        ),
    ),
    SourceCheck(
        path="tools/registry.py",
        expected_sha="30ec01a9f31f66ff159024aec3ccc3a57249ba62",
        required_terms=(
            "check_fn",
            "requires_env",
            "get_definitions",
            "dispatch",
            "json.dumps",
            "_kwargs_accepted_by",
        ),
    ),
    SourceCheck(
        path="hermes_cli/plugins_cmd.py",
        expected_sha="ad061ca6772c0f5629d365bb7c406cfb23556f41",
        required_terms=(
            "_resolve_plugin_key",
            "_scan_plugin_tree",
            "_resolve_subdir_within",
            "_tri_state_flag",
            "requires_env",
            "plugins.enabled",
            "enable",
            "disable",
            "install",
        ),
    ),
    SourceCheck(
        path="hermes_cli/plugins_cmd_install.py",
        expected_sha="2aee13fdd3fbfe3b7c3299de4819aa9e114bd3e1",
        required_terms=(
            "def cmd_install",
            "_prompt_plugin_env_vars",
            "_install_plugin_python_deps",
            "declares Python dependencies",
            "yes_deps",
            "no_deps",
        ),
    ),
    SourceCheck(
        path="hermes_cli/subcommands/plugins.py",
        expected_sha="fe703ee56eeee778d14a5ee25401eba1e3f665e3",
        required_terms=(
            "--enable",
            "--no-enable",
            "--force",
            "--yes-deps",
            "--no-deps",
        ),
    ),
    SourceCheck(
        path="pm/plugin_declarations.py",
        expected_sha="210cabe36b29b87272cdda0add85174c17809f6d",
        required_terms=(
            "python_runtime",
            "external",
            "is_member",
            "project.dependencies",
        ),
    ),
)

CORE_PIN_CHECKS: Final = (
    CorePinCheck(
        path="pyproject.toml",
        required_pin='"httpx[socks]==0.28.',
        next_step=(
            "Hermes Agent core no longer pins httpx 0.28. "
            "Review the httpx range in pyproject.toml and python_runtime in plugin.yaml."
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


def check_page(client: SourceClient, check: PageCheck) -> list[str]:
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


def blob_sha(content: bytes) -> str:
    header = f"blob {len(content)}\0".encode()
    return hashlib.sha1(header + content, usedforsecurity=False).hexdigest()


def latest_release(client: SourceClient) -> tuple[str | None, list[str]]:
    try:
        response = client.get(LATEST_RELEASE_URL, headers=github_headers())
        response.raise_for_status()
    except httpx.HTTPError as error:
        return None, [f"Release lookup failed. Retry after {error.__class__.__name__}."]

    payload = _decode_json(response.content)
    tag = payload.get("tag_name") if isinstance(payload, dict) else None
    if not isinstance(tag, str) or not tag:
        return None, ["Invalid GitHub response for the latest release. Expected tag_name."]

    return tag, []


def read_source(
    client: SourceClient, path: str, ref: str
) -> tuple[SourceContent | None, list[str]]:
    try:
        response = client.get(f"{SOURCE_URL}/{ref}/{path}")
        response.raise_for_status()
    except httpx.HTTPError as error:
        return None, [
            f"Source fetch failed for {path} at {ref}. Retry after {error.__class__.__name__}."
        ]

    return SourceContent(sha=blob_sha(response.content), text=response.text), []


def check_source(client: SourceClient, check: SourceCheck, release: str) -> list[str]:
    content, errors = read_source(client, check.path, release)
    if content is None:
        return errors

    if content.sha != check.expected_sha:
        return [
            (
                f"Source changed for {check.path} in Hermes Agent {release}: "
                f"{check.expected_sha} to {content.sha}. "
                "Review the official Hermes Agent diff before updating this lock."
            )
        ]

    missing = missing_terms(content.text, check.required_terms)
    if missing:
        return [f"{check.path} is outdated. Add these terms: {', '.join(missing)}"]

    print(f"Source verified. {check.path} {release} {content.sha}")
    return []


def check_core_pin(client: SourceClient, check: CorePinCheck, release: str) -> list[str]:
    content, errors = read_source(client, check.path, release)
    if content is None:
        return errors

    if check.required_pin not in content.text:
        return [check.next_step]

    print(f"Core pin verified. {check.path} {release} {check.required_pin}")
    return []


def development_warnings(client: SourceClient) -> list[str]:
    warnings: list[str] = []
    for source_check in SOURCE_CHECKS:
        content, errors = read_source(client, source_check.path, DEVELOPMENT_BRANCH)
        if content is None:
            warnings.extend(errors)
        elif content.sha != source_check.expected_sha:
            warnings.append(
                f"Upstream {DEVELOPMENT_BRANCH} changed {source_check.path} to {content.sha}. "
                "The next Hermes Agent release may need a review."
            )
    for core_pin_check in CORE_PIN_CHECKS:
        content, errors = read_source(client, core_pin_check.path, DEVELOPMENT_BRANCH)
        if content is None:
            warnings.extend(errors)
        elif core_pin_check.required_pin not in content.text:
            warnings.append(
                f"Upstream {DEVELOPMENT_BRANCH} dropped the pin {core_pin_check.required_pin}. "
                "The next Hermes Agent release may need a review."
            )
    return warnings


def run_checks(client: SourceClient) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    for page_check in PAGE_CHECKS:
        errors.extend(check_page(client, page_check))

    release, release_errors = latest_release(client)
    if release is None:
        return [*errors, *release_errors], []

    if release != REVIEWED_RELEASE:
        print(f"Hermes Agent {release} is newer than the reviewed {REVIEWED_RELEASE}.")
    for source_check in SOURCE_CHECKS:
        errors.extend(check_source(client, source_check, release))
    for core_pin_check in CORE_PIN_CHECKS:
        errors.extend(check_core_pin(client, core_pin_check, release))

    return errors, development_warnings(client)


def main() -> int:
    timeout = httpx.Timeout(DOC_TIMEOUT_SECONDS)
    with httpx.Client(
        follow_redirects=True, headers={"User-Agent": USER_AGENT}, timeout=timeout
    ) as client:
        errors, warnings = run_checks(client)

    for warning in warnings:
        print(f"Warning. {warning}")
    if errors:
        print("Hermes Agent compatibility failed. Review each item below.")
        for error in errors:
            print(error)
        return 1

    print("Hermes Agent compatibility passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
