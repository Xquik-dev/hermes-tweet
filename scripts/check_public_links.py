from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    from collections.abc import Iterable

ROOT = Path(__file__).parents[1]
HTTP_BAD_REQUEST = 400
HTTP_FORBIDDEN = 403
HTTP_METHOD_NOT_ALLOWED = 405
PUBLIC_LINK_FILES = (
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
    "docs/ECOSYSTEM.md",
    "docs/CONTEXT7.md",
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
TRAILING_URL_PUNCTUATION = ".,;:!?)'"
URL_PATTERN = re.compile(r'https?://[^\s\]\\)<>"`]+')
USER_AGENT = "HermesTweetLinkCheck/1.0"


@dataclass(frozen=True)
class LinkFailure:
    url: str
    reason: str


def strip_trailing_url_punctuation(url: str) -> str:
    return url.rstrip(TRAILING_URL_PUNCTUATION)


def collect_public_urls(files: Iterable[str] = PUBLIC_LINK_FILES) -> list[str]:
    urls: list[str] = []
    seen_urls: set[str] = set()

    for file_name in files:
        text = (ROOT / file_name).read_text(encoding="utf-8")
        for match in URL_PATTERN.findall(text):
            url = strip_trailing_url_punctuation(match)
            if url in seen_urls:
                continue
            seen_urls.add(url)
            urls.append(url)

    return urls


def check_public_url(client: httpx.Client, url: str) -> LinkFailure | None:
    last_reason = "not checked"

    for method in ("HEAD", "GET"):
        try:
            response = client.request(method, url)
        except httpx.HTTPError as error:
            last_reason = error.__class__.__name__
            continue

        status_code = response.status_code
        if status_code < HTTP_BAD_REQUEST or status_code == HTTP_FORBIDDEN:
            return None
        if method == "HEAD" and status_code == HTTP_METHOD_NOT_ALLOWED:
            last_reason = f"HTTP {status_code}"
            continue
        return LinkFailure(url=url, reason=f"HTTP {status_code}")

    return LinkFailure(url=url, reason=last_reason)


def check_public_links(urls: Iterable[str]) -> list[LinkFailure]:
    failures: list[LinkFailure] = []
    headers = {"User-Agent": USER_AGENT}
    timeout = httpx.Timeout(20.0)

    with httpx.Client(follow_redirects=True, headers=headers, timeout=timeout) as client:
        for url in urls:
            failure = check_public_url(client, url)
            if failure is not None:
                failures.append(failure)

    return failures


def main() -> int:
    urls = collect_public_urls()
    failures = check_public_links(urls)

    print(f"checked={len(urls)} failures={len(failures)}")
    for failure in failures:
        print(f"{failure.reason} {failure.url}")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
