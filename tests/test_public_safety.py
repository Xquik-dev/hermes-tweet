from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterable

    import pytest

ROOT = Path(__file__).parents[1]
SCRIPTS_DIR = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


def load_public_safety_module() -> Any:
    module_path = ROOT / "scripts" / "check_public_safety.py"
    spec = importlib.util.spec_from_file_location("check_public_safety", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_public_links_module() -> Any:
    module_path = ROOT / "scripts" / "check_public_links.py"
    spec = importlib.util.spec_from_file_location("check_public_links_for_safety", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


check_public_safety = load_public_safety_module()
check_public_links = load_public_links_module()


def finding_labels(findings: list[Any]) -> list[str]:
    return [finding.label for finding in findings]


def test_scan_line_reports_secret_labels_without_secret_values() -> None:
    token = "ghp_" + ("A" * 24)

    findings = check_public_safety.scan_line(Path("README.md"), 3, f"token={token}")

    assert finding_labels(findings) == ["github-token"]
    rendered_finding = check_public_safety.format_finding(findings[0])
    assert rendered_finding == "README.md:3: github-token"
    assert token not in rendered_finding


def test_scan_line_reports_google_api_key_without_secret_value() -> None:
    token = "AI" + "za" + ("A" * 32)

    findings = check_public_safety.scan_line(Path("README.md"), 4, f"api_key={token}")

    assert finding_labels(findings) == ["google-api-key"]
    rendered_finding = check_public_safety.format_finding(findings[0])
    assert rendered_finding == "README.md:4: google-api-key"
    assert token not in rendered_finding


def test_scan_line_allows_documented_placeholders() -> None:
    placeholder_line = "Set XQUIK_API_KEY=xq_your_key or Authorization: Bearer token."

    findings = check_public_safety.scan_line(Path("README.md"), 8, placeholder_line)

    assert findings == []


def test_scan_line_placeholder_does_not_hide_secret_token() -> None:
    token = "ghp_" + ("A" * 24)
    line = f"Set XQUIK_API_KEY=xq_your_key; never publish token={token}."

    findings = check_public_safety.scan_line(Path("README.md"), 9, line)

    assert finding_labels(findings) == ["github-token"]
    rendered_finding = check_public_safety.format_finding(findings[0])
    assert rendered_finding == "README.md:9: github-token"
    assert token not in rendered_finding


def test_scan_line_placeholder_does_not_hide_private_wording() -> None:
    line = f"Set XQUIK_API_KEY=xq_your_key; never document {'internal'} {'cost'}."

    findings = check_public_safety.scan_line(Path("README.md"), 9, line)

    assert finding_labels(findings) == ["internal-cost"]


def test_scan_line_flags_private_public_wording() -> None:
    line = f"Remove {'internal'} {'cost'} and {'private'} {'vendor'} wording."

    findings = check_public_safety.scan_line(Path("docs/example.md"), 13, line)

    assert finding_labels(findings) == ["internal-cost", "private-vendor"]


def test_scan_line_flags_source_and_pricing_wording() -> None:
    line = f"Remove third-party API source and {'internal'} pricing wording."

    findings = check_public_safety.scan_line(Path("docs/example.md"), 13, line)

    assert finding_labels(findings) == [
        "internal-pricing",
        "third-party-api-source",
    ]


def test_scan_line_flags_runtime_confidentiality_wording() -> None:
    line = (
        "Remove raw session material, provider capacity, and fallback mechanics from public copy."
    )

    findings = check_public_safety.scan_line(Path("docs/example.md"), 17, line)

    assert finding_labels(findings) == [
        "raw-session-material",
        "provider-capacity",
        "fallback-mechanics",
    ]


def test_public_safety_scan_includes_agent_instructions() -> None:
    assert "AGENTS.md" in check_public_safety.PUBLIC_TEXT_FILES


def test_public_safety_scan_includes_github_community_docs() -> None:
    expected_files = {
        ".github/CONTRIBUTING.md",
        ".github/ISSUE_TEMPLATE/bug_report.md",
        ".github/ISSUE_TEMPLATE/feature_request.md",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/SECURITY.md",
        "CODE_OF_CONDUCT.md",
    }

    assert expected_files <= set(check_public_safety.PUBLIC_TEXT_FILES)


def test_public_safety_scan_includes_github_repository_config() -> None:
    expected_files = {
        ".github/FUNDING.yml",
        ".github/dependabot.yml",
        ".github/workflows/ci.yml",
        ".github/workflows/publish.yml",
    }

    assert expected_files <= set(check_public_safety.PUBLIC_TEXT_FILES)


def test_public_safety_scan_includes_skill_cards() -> None:
    expected_files = {
        "skills/hermes-tweet/skill-card.md",
        "hermes_tweet/skills/hermes-tweet/skill-card.md",
    }

    assert expected_files <= set(check_public_safety.PUBLIC_TEXT_FILES)


def test_public_link_and_safety_surfaces_stay_aligned() -> None:
    assert check_public_safety.PUBLIC_TEXT_FILES is check_public_links.PUBLIC_LINK_FILES


def test_public_surface_registry_has_unique_existing_files() -> None:
    files = check_public_safety.PUBLIC_TEXT_FILES
    missing_files = [file_name for file_name in files if not (ROOT / file_name).is_file()]

    assert len(files) == len(set(files))
    assert missing_files == []


def test_copied_catalog_url_rule_stays_in_public_skill_surfaces() -> None:
    expected = "Copied endpoint URLs are accepted only when they resolve to catalog-listed paths."
    readme_expected = (
        "Copied endpoint URLs are accepted, but Hermes Tweet matches only catalog-listed\npaths."
    )
    integration_expected = (
        "Copied endpoint URLs are fine, but Hermes Tweet matches only catalog-listed\n  paths."
    )
    surfaces = {
        "README.md": readme_expected,
        "docs/CONTEXT7.md": (
            "Copied endpoint URLs are accepted only when they resolve to catalog-listed\npaths."
        ),
        "docs/HERMES_SURFACES.md": "copied endpoint URLs must resolve to one",
        "docs/INTEGRATION_PATTERNS.md": integration_expected,
        "docs/OBSERVABILITY.md": (
            "Copied endpoint URLs resolved only to catalog-listed `/api/v1/...` paths."
        ),
        "docs/PUBLICATION_CHECKLIST.md": (
            "Copied endpoint URLs resolve only to catalog-listed `/api/v1/...` paths."
        ),
        "docs/SUBMISSION_READINESS.md": (
            "copied endpoint URLs resolve only to catalog-listed `/api/v1/...` paths"
        ),
        "after-install.md": (
            "Copied endpoint\nURLs are accepted only when they resolve to catalog-listed paths."
        ),
        "skills/hermes-tweet/SKILL.md": expected,
        "hermes_tweet/skills/hermes-tweet/SKILL.md": expected,
        "registries/ask/hermes-tweet/SKILL.md": expected,
    }

    for file_name, text in surfaces.items():
        assert text in (ROOT / file_name).read_text(encoding="utf-8")


def test_scan_public_files_reports_relative_paths(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    public_doc = tmp_path / "docs" / "example.md"
    public_doc.parent.mkdir()
    public_doc.write_text("Authorization: Bearer " + ("B" * 24), encoding="utf-8")
    monkeypatch.setattr(check_public_safety, "ROOT", tmp_path)

    findings = check_public_safety.scan_public_files(("docs/example.md",))

    assert len(findings) == 1
    assert check_public_safety.format_finding(findings[0]) == "docs/example.md:1: bearer-token"


def test_public_safety_main_accepts_targeted_files(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    scanned_files: tuple[str, ...] = ()

    def fake_scan_public_files(files: Iterable[str]) -> list[Any]:
        nonlocal scanned_files
        scanned_files = tuple(files)
        return []

    monkeypatch.setattr(check_public_safety, "scan_public_files", fake_scan_public_files)

    result = check_public_safety.main(("README.md",))
    captured = capsys.readouterr()

    assert result == 0
    assert scanned_files == ("README.md",)
    assert captured.out == "checked=1 findings=0\n"
    assert captured.err == ""


def test_public_safety_main_reports_targeted_findings(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    finding = check_public_safety.PublicSafetyFinding(Path("README.md"), 1, "github-token")

    def fake_scan_public_files(files: Iterable[str]) -> list[Any]:
        assert tuple(files) == ("README.md",)
        return [finding]

    monkeypatch.setattr(check_public_safety, "scan_public_files", fake_scan_public_files)

    result = check_public_safety.main(("README.md",))
    captured = capsys.readouterr()

    assert result == 1
    assert captured.out == "checked=1 findings=1\nREADME.md:1: github-token\n"
    assert captured.err == ""


def test_public_safety_main_rejects_unregistered_targets(
    capsys: pytest.CaptureFixture[str],
) -> None:
    result = check_public_safety.main(("private-notes.md",))
    captured = capsys.readouterr()

    assert result == 1
    assert captured.out == "unregistered public files: private-notes.md\n"
    assert captured.err == ""


def test_public_safety_main_rejects_absolute_targets_outside_repo(
    capsys: pytest.CaptureFixture[str],
) -> None:
    outside_path = ROOT.parent / "private-notes.md"

    result = check_public_safety.main((str(outside_path),))
    captured = capsys.readouterr()

    assert result == 1
    assert captured.out == f"unregistered public files: {outside_path}\n"
    assert captured.err == ""
