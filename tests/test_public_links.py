from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import pytest

ROOT = Path(__file__).parents[1]
SCRIPTS_DIR = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


def load_public_links_module() -> Any:
    module_path = ROOT / "scripts" / "check_public_links.py"
    spec = importlib.util.spec_from_file_location("check_public_links", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


check_public_links = load_public_links_module()


@dataclass(frozen=True)
class FakeResponse:
    status_code: int


class FakeClient:
    def __init__(self, status_codes: list[int]) -> None:
        self._status_codes = status_codes
        self.requests: list[tuple[str, str]] = []

    def request(self, method: str, url: str) -> FakeResponse:
        self.requests.append((method, url))
        return FakeResponse(self._status_codes.pop(0))


def test_strip_trailing_url_punctuation_keeps_url_body() -> None:
    url = "https://github.com/Xquik-dev/hermes-tweet#readme)."

    stripped_url = check_public_links.strip_trailing_url_punctuation(url)

    assert stripped_url == "https://github.com/Xquik-dev/hermes-tweet#readme"


def test_collect_public_urls_deduplicates_and_strips_punctuation(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    public_doc = tmp_path / "README.md"
    public_doc.write_text(
        (
            "See https://github.com/Xquik-dev/hermes-tweet#readme).\n"
            "Duplicate https://github.com/Xquik-dev/hermes-tweet#readme\n"
            "Docs https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin/"
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(check_public_links, "ROOT", tmp_path)

    urls = check_public_links.collect_public_urls(("README.md",))

    assert urls == [
        "https://github.com/Xquik-dev/hermes-tweet#readme",
        "https://hermes-agent.nousresearch.com/docs/guides/build-a-hermes-plugin/",
    ]


def test_public_link_scan_includes_github_community_docs() -> None:
    expected_files = {
        ".github/CONTRIBUTING.md",
        ".github/ISSUE_TEMPLATE/bug_report.md",
        ".github/ISSUE_TEMPLATE/feature_request.md",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/SECURITY.md",
        "AGENTS.md",
        "CODE_OF_CONDUCT.md",
    }

    assert expected_files <= set(check_public_links.PUBLIC_LINK_FILES)


def test_public_link_scan_includes_github_repository_config() -> None:
    expected_files = {
        ".github/FUNDING.yml",
        ".github/dependabot.yml",
        ".github/workflows/ci.yml",
        ".github/workflows/publish.yml",
    }

    assert expected_files <= set(check_public_links.PUBLIC_LINK_FILES)


def test_main_accepts_targeted_public_files(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    public_doc = tmp_path / "README.md"
    public_doc.write_text("Docs https://example.com/readme", encoding="utf-8")
    ignored_doc = tmp_path / "after-install.md"
    ignored_doc.write_text("Docs https://example.com/ignored", encoding="utf-8")
    checked_urls: list[str] = []

    def fake_check_public_links(urls: list[str]) -> list[Any]:
        checked_urls.extend(urls)
        return []

    monkeypatch.setattr(check_public_links, "ROOT", tmp_path)
    monkeypatch.setattr(check_public_links, "check_public_links", fake_check_public_links)

    result = check_public_links.main(("README.md",))
    captured = capsys.readouterr()

    assert result == 0
    assert checked_urls == ["https://example.com/readme"]
    assert captured.out == "checked=1 failures=0\n"
    assert captured.err == ""


def test_main_reports_targeted_link_failures(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    public_doc = tmp_path / "README.md"
    public_doc.write_text("Docs https://example.com/missing", encoding="utf-8")

    def fake_check_public_links(urls: list[str]) -> list[Any]:
        assert urls == ["https://example.com/missing"]
        return [
            check_public_links.LinkFailure(
                url="https://example.com/missing",
                reason="HTTP 404",
            ),
        ]

    monkeypatch.setattr(check_public_links, "ROOT", tmp_path)
    monkeypatch.setattr(check_public_links, "check_public_links", fake_check_public_links)

    result = check_public_links.main(("README.md",))
    captured = capsys.readouterr()

    assert result == 1
    assert captured.out == "checked=1 failures=1\nHTTP 404 https://example.com/missing\n"
    assert captured.err == ""


def test_check_public_url_falls_back_from_head_405_to_get_success() -> None:
    client = FakeClient([405, 200])

    failure = check_public_links.check_public_url(client, "https://example.com")

    assert failure is None
    assert client.requests == [("HEAD", "https://example.com"), ("GET", "https://example.com")]


def test_check_public_url_accepts_forbidden_links() -> None:
    client = FakeClient([403])

    failure = check_public_links.check_public_url(client, "https://example.com/private")

    assert failure is None
    assert client.requests == [("HEAD", "https://example.com/private")]


def test_check_public_url_reports_http_failure() -> None:
    client = FakeClient([404])

    failure = check_public_links.check_public_url(client, "https://example.com/missing")

    assert failure == check_public_links.LinkFailure(
        url="https://example.com/missing",
        reason="HTTP 404",
    )
