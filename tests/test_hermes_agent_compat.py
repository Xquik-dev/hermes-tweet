# SPDX-FileCopyrightText: 2026 Xquik Contributors
# SPDX-License-Identifier: MIT

from __future__ import annotations

import json
from dataclasses import dataclass

import pytest
from scripts import check_hermes_agent_compat as compat


@dataclass(frozen=True)
class FakeResponse:
    text: str = ""

    @property
    def content(self) -> bytes:
        return self.text.encode()

    def raise_for_status(self) -> None:
        return None


class FakeClient:
    def __init__(self, responses: list[FakeResponse]) -> None:
        self._responses = responses
        self.urls: list[str] = []
        self.authorized_urls: list[str] = []

    def get(self, url: str, headers: dict[str, str] | None = None) -> FakeResponse:
        self.urls.append(url)
        if headers is not None and "Authorization" in headers:
            self.authorized_urls.append(url)
        return self._responses.pop(0)


def test_missing_terms_reports_only_absent_terms() -> None:
    missing = compat.missing_terms(
        "plugin.yaml ctx.register_skill", ("plugin.yaml", "requires_env")
    )

    assert missing == ["requires_env"]


def test_github_headers_adds_optional_token(monkeypatch: pytest.MonkeyPatch) -> None:
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

    assert compat.REVIEWED_RELEASE == "v0.22.5"
    assert locks == {
        "hermes_cli/plugins.py": "14e13ab00e3a289b53b9cc32b813ce120079fc23",
        "hermes_cli/plugins_content.py": "92b8d79f5440e58d421a6018d4c6d12e9aef107b",
        "tools/registry.py": "bc6e1ab7688a17e11d70e1ef992dbf7fb42418c4",
        "hermes_cli/plugins_cmd.py": "d8c3533252807498b790a967f8ffeffc75621b4a",
        "hermes_cli/plugins_cmd_install.py": "ded3fef3d44ec1808d23335e1a5c068add9e4fa8",
        "hermes_cli/subcommands/plugins.py": "26a0eec6469eddeee7dbd331dbd39c02eb103c49",
        "pm/plugin_declarations.py": "9c65c5130e268e41ec65c8d030c8c169007c4277",
    }


HELLO = "hello\n"
HELLO_SHA = "ce013625030ba8dba906f756967f9e9ca394464a"
EMPTY_SHA = "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"
SOURCE = "https://raw.githubusercontent.com/NousResearch/hermes-agent"
LATEST = "https://api.github.com/repos/NousResearch/hermes-agent/releases/latest"
HTTPX_MOVED = (
    "Hermes Agent core no longer pins httpx 0.28. "
    "Review the httpx range in pyproject.toml and python_runtime in plugin.yaml."
)
PIN = '"httpx[socks]==0.28.'


def release(tag: str) -> FakeResponse:
    payload = {"tag_name": tag}
    return FakeResponse(text=json.dumps(payload))


def locked(path: str, expected_sha: str, *terms: str) -> compat.SourceCheck:
    return compat.SourceCheck(path=path, expected_sha=expected_sha, required_terms=terms)


def pin_checks(
    monkeypatch: pytest.MonkeyPatch,
    source_checks: tuple[compat.SourceCheck, ...],
    *,
    core_pins: bool,
) -> None:
    monkeypatch.setattr(compat, "PAGE_CHECKS", ())
    monkeypatch.setattr(compat, "SOURCE_CHECKS", source_checks)
    monkeypatch.setattr(compat, "CORE_PIN_CHECKS", compat.CORE_PIN_CHECKS if core_pins else ())


@pytest.mark.parametrize(("content", "sha"), [(HELLO.encode(), HELLO_SHA), (b"", EMPTY_SHA)])
def test_blob_sha_matches_git(content: bytes, sha: str) -> None:
    assert compat.blob_sha(content) == sha


def test_read_source_fetches_the_file_at_a_ref() -> None:
    client = FakeClient([FakeResponse(text=HELLO)])

    content, errors = compat.read_source(client, "hermes_cli/plugins.py", "v1.2.3")

    assert errors == []
    assert content == compat.SourceContent(sha=HELLO_SHA, text=HELLO)
    assert client.urls == [f"{SOURCE}/v1.2.3/hermes_cli/plugins.py"]


def test_latest_release_reads_the_tag_and_alone_carries_the_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GITHUB_TOKEN", "test-token")
    client = FakeClient([release("v1.2.3"), FakeResponse(text=HELLO)])

    assert compat.latest_release(client) == ("v1.2.3", [])
    compat.read_source(client, "tools/registry.py", "v1.2.3")

    assert client.urls == [LATEST, f"{SOURCE}/v1.2.3/tools/registry.py"]
    assert client.authorized_urls == [LATEST]


@pytest.mark.parametrize("payload", [[], {}, {"tag_name": ""}, {"tag_name": 7}])
def test_latest_release_reports_an_unusable_answer(payload: object) -> None:
    client = FakeClient([FakeResponse(text=json.dumps(payload))])

    assert compat.latest_release(client) == (
        None,
        ["Invalid GitHub response for the latest release. Expected tag_name."],
    )


def test_check_source_reports_sha_drift() -> None:
    client = FakeClient([FakeResponse(text=HELLO)])

    errors = compat.check_source(client, locked("tools/registry.py", "old-sha"), "v1.2.3")

    assert errors == [
        (
            f"Source changed for tools/registry.py in Hermes Agent v1.2.3: old-sha to {HELLO_SHA}. "
            "Review the official Hermes Agent diff before updating this lock."
        )
    ]


def test_check_source_reports_missing_terms_after_sha_match() -> None:
    client = FakeClient([FakeResponse(text=HELLO)])
    check = locked("tools/registry.py", HELLO_SHA, "hello", "check_fn")

    errors = compat.check_source(client, check, "v1.2.3")

    assert errors == ["tools/registry.py is outdated. Add these terms: check_fn"]


def test_core_pin_check_passes_while_hermes_ships_the_httpx_line(
    capsys: pytest.CaptureFixture[str],
) -> None:
    client = FakeClient([FakeResponse(text='dependencies = ["httpx[socks]==0.28.1"]')])

    assert compat.check_core_pin(client, compat.CORE_PIN_CHECKS[0], "v1.2.3") == []
    assert capsys.readouterr().out == f"Core pin verified. pyproject.toml v1.2.3 {PIN}\n"
    assert client.urls == [f"{SOURCE}/v1.2.3/pyproject.toml"]


def test_core_pin_check_fails_when_hermes_moves_httpx() -> None:
    client = FakeClient([FakeResponse(text='dependencies = ["httpx[socks]==0.29.0"]')])

    assert compat.check_core_pin(client, compat.CORE_PIN_CHECKS[0], "v1.2.3") == [HTTPX_MOVED]


def test_run_checks_gates_on_the_latest_release_and_only_warns_about_main(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    pin_checks(monkeypatch, (locked("tools/registry.py", HELLO_SHA, "hello"),), core_pins=True)
    client = FakeClient(
        [
            release("v9.9.9"),
            FakeResponse(text=HELLO),
            FakeResponse(text=f'dependencies = [{PIN}1"]'),
            FakeResponse(text="changed after the release\n"),
            FakeResponse(text='dependencies = ["httpx[socks]==0.29.0"]'),
        ]
    )

    errors, warnings = compat.run_checks(client)

    assert errors == []
    assert warnings == [
        (
            "Upstream main changed tools/registry.py to "
            "746c21705532133a692d4a96009362b31b4612e7. "
            "The next Hermes Agent release may need a review."
        ),
        (f"Upstream main dropped the pin {PIN}. The next Hermes Agent release may need a review."),
    ]
    assert client.urls == [
        LATEST,
        f"{SOURCE}/v9.9.9/tools/registry.py",
        f"{SOURCE}/v9.9.9/pyproject.toml",
        f"{SOURCE}/main/tools/registry.py",
        f"{SOURCE}/main/pyproject.toml",
    ]
    assert capsys.readouterr().out.splitlines()[0] == (
        "Hermes Agent v9.9.9 is newer than the reviewed v0.22.5."
    )


def test_run_checks_fails_when_the_latest_release_changes_a_locked_file(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pin_checks(monkeypatch, (locked("tools/registry.py", HELLO_SHA, "hello"),), core_pins=False)
    client = FakeClient([release("v0.22.0"), FakeResponse(text=""), FakeResponse(text=HELLO)])

    errors, warnings = compat.run_checks(client)

    assert errors == [
        (
            f"Source changed for tools/registry.py in Hermes Agent v0.22.0: {HELLO_SHA} to "
            f"{EMPTY_SHA}. Review the official Hermes Agent diff before updating this lock."
        )
    ]
    assert warnings == []


def test_run_checks_stops_when_the_release_lookup_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    pin_checks(monkeypatch, (locked("tools/registry.py", HELLO_SHA),), core_pins=False)
    client = FakeClient([FakeResponse(text="[]")])

    assert compat.run_checks(client) == (
        ["Invalid GitHub response for the latest release. Expected tag_name."],
        [],
    )
    assert client.urls == [LATEST]
