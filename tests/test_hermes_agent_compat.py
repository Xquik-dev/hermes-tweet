from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parents[1]


def load_compat_module() -> Any:
    module_path = ROOT / "scripts" / "check_hermes_agent_compat.py"
    spec = importlib.util.spec_from_file_location("check_hermes_agent_compat", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


compat = load_compat_module()


@dataclass(frozen=True)
class FakeResponse:
    text: str = ""
    payload: object | None = None

    def raise_for_status(self) -> None:
        return None

    def json(self) -> object:
        return self.payload


class FakeClient:
    def __init__(self, responses: list[FakeResponse]) -> None:
        self._responses = responses
        self.urls: list[str] = []

    def get(self, url: str) -> FakeResponse:
        self.urls.append(url)
        return self._responses.pop(0)


def test_missing_terms_reports_only_absent_terms() -> None:
    missing = compat.missing_terms(
        "plugin.yaml ctx.register_skill", ("plugin.yaml", "requires_env")
    )

    assert missing == ["requires_env"]


def test_github_headers_adds_optional_token(monkeypatch: Any) -> None:
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setenv("GH_TOKEN", "test-token")

    headers = compat.github_headers()

    assert headers == {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer test-token",
        "User-Agent": compat.USER_AGENT,
    }


def test_source_checks_track_reviewed_hermes_agent_locks() -> None:
    locks = {check.path: check.expected_sha for check in compat.SOURCE_CHECKS}

    assert locks == {
        "hermes_cli/plugins.py": "6ca393fca53c1fd2b3479bed72180fedcc848c88",
        "tools/registry.py": "9b6611fb407dd17da5aa4ae2ba6a39498af830da",
        "hermes_cli/plugins_cmd.py": "6a7c39f3e4e014f98201766e980d19c696e1c545",
    }


def test_check_page_reports_missing_terms() -> None:
    client = FakeClient([FakeResponse(text="plugin.yaml")])
    check = compat.PageCheck(
        name="Plugin docs",
        url="https://example.com/docs",
        required_terms=("plugin.yaml", "requires_env"),
    )

    errors = compat.check_page(client, check)

    assert errors == ["Plugin docs: missing terms requires_env"]
    assert client.urls == ["https://example.com/docs"]


def test_read_source_fetches_metadata_and_source_text() -> None:
    client = FakeClient(
        [
            FakeResponse(payload={"sha": "abc123", "download_url": "https://example.com/raw.py"}),
            FakeResponse(text="requires_env check_fn"),
        ],
    )

    content, errors = compat.read_source(client, "hermes_cli/plugins.py")

    assert errors == []
    assert content == compat.SourceContent(sha="abc123", text="requires_env check_fn")
    assert client.urls == [
        f"{compat.GITHUB_CONTENT_URL}/hermes_cli/plugins.py?ref=main",
        "https://example.com/raw.py",
    ]


def test_check_source_reports_sha_drift() -> None:
    client = FakeClient(
        [
            FakeResponse(payload={"sha": "new-sha", "download_url": "https://example.com/raw.py"}),
            FakeResponse(text="requires_env"),
        ],
    )
    check = compat.SourceCheck(
        path="tools/registry.py",
        expected_sha="old-sha",
        required_terms=("requires_env",),
    )

    errors = compat.check_source(client, check)

    assert errors == [
        (
            "tools/registry.py: source sha changed from old-sha to new-sha. "
            "Review official Hermes Agent changes before updating this lock."
        )
    ]


def test_check_source_reports_missing_terms_after_sha_match() -> None:
    client = FakeClient(
        [
            FakeResponse(
                payload={"sha": "locked-sha", "download_url": "https://example.com/raw.py"}
            ),
            FakeResponse(text="requires_env"),
        ],
    )
    check = compat.SourceCheck(
        path="tools/registry.py",
        expected_sha="locked-sha",
        required_terms=("requires_env", "check_fn"),
    )

    errors = compat.check_source(client, check)

    assert errors == ["tools/registry.py: missing terms check_fn"]
