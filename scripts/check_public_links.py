from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import httpx

from public_surfaces import PUBLIC_SURFACE_FILES, select_public_surface_files

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

ROOT = Path(__file__).parents[1]
HTTP_BAD_REQUEST = 400
HTTP_FORBIDDEN = 403
HTTP_METHOD_NOT_ALLOWED = 405
HTTP_UNAUTHORIZED = 401
PUBLIC_LINK_FILES = PUBLIC_SURFACE_FILES
AUTHENTICATED_PUBLIC_URLS = frozenset({"https://xquik.com/mcp"})
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
        if status_code == HTTP_UNAUTHORIZED and url in AUTHENTICATED_PUBLIC_URLS:
            challenge = response.headers.get("www-authenticate", "")
            if challenge.lower().startswith("bearer "):
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


def main(argv: Sequence[str] | None = None) -> int:
    try:
        files = select_public_surface_files(argv)
    except ValueError as error:
        print(error)
        return 1

    urls = collect_public_urls(files)
    failures = check_public_links(urls)

    print(f"checked={len(urls)} failures={len(failures)}")
    for failure in failures:
        print(f"{failure.reason} {failure.url}")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
