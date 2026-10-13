# SPDX-FileCopyrightText: 2026 Xquik Contributors
# SPDX-License-Identifier: MIT

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
        "hermes_cli/plugins.py": "a652179cd4a7a3ac04fe7eb2a0377de6a6dfbc58",
        "hermes_cli/plugins_content.py": "92b8d79f5440e58d421a6018d4c6d12e9aef107b",
        "tools/registry.py": "30ec01a9f31f66ff159024aec3ccc3a57249ba62",
        "hermes_cli/plugins_cmd.py": "ad061ca6772c0f5629d365bb7c406cfb23556f41",
        "hermes_cli/plugins_cmd_install.py": "2aee13fdd3fbfe3b7c3299de4819aa9e114bd3e1",
        "hermes_cli/subcommands/plugins.py": "fe703ee56eeee778d14a5ee25401eba1e3f665e3",
        "pm/plugin_declarations.py": "210cabe36b29b87272cdda0add85174c17809f6d",
    }


HTTPX_MOVED = (
    "Hermes Agent core no longer pins httpx 0.28. "
    "Review the httpx range in pyproject.toml and python_runtime in plugin.yaml."
)


def core_pin_responses(text: str) -> list[FakeResponse]:
    payload = {"sha": "any-sha", "download_url": "https://raw.example.test/pyproject.toml"}
    return [FakeResponse(payload=payload), FakeResponse(text=text)]


def test_core_pin_check_passes_while_hermes_ships_the_httpx_line(capsys: Any) -> None:
    client = FakeClient(core_pin_responses('dependencies = ["httpx[socks]==0.28.1"]'))

    assert compat.check_core_pin(client, compat.CORE_PIN_CHECKS[0]) == []
    assert capsys.readouterr().out == 'Core pin verified. pyproject.toml "httpx[socks]==0.28.\n'
    assert client.urls[0].endswith("/contents/pyproject.toml?ref=main")


def test_core_pin_check_fails_when_hermes_moves_httpx() -> None:
    client = FakeClient(core_pin_responses('dependencies = ["httpx[socks]==0.29.0"]'))

    assert compat.check_core_pin(client, compat.CORE_PIN_CHECKS[0]) == [HTTPX_MOVED]


def test_core_pin_check_reports_an_unreadable_file() -> None:
    client = FakeClient([FakeResponse(payload=[])])

    assert compat.check_core_pin(client, compat.CORE_PIN_CHECKS[0]) == [
        "Invalid GitHub response for pyproject.toml. Expected an object."
    ]


def test_check_page_reports_missing_terms() -> None:
    client = FakeClient([FakeResponse(text="plugin.yaml")])
    check = compat.PageCheck(
        name="Plugin docs",
        url="https://example.com/docs",
        required_terms=("plugin.yaml", "requires_env"),
    )

    errors = compat.check_page(client, check)

    assert errors == ["Plugin docs is outdated. Add these terms: requires_env"]
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
            "Source changed for tools/registry.py: old-sha to new-sha. "
            "Review the official Hermes Agent diff before updating this lock."
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

    assert errors == ["tools/registry.py is outdated. Add these terms: check_fn"]
