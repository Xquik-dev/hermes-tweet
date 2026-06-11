from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import pytest

ROOT = Path(__file__).parents[1]


def load_public_safety_module() -> Any:
    module_path = ROOT / "scripts" / "check_public_safety.py"
    spec = importlib.util.spec_from_file_location("check_public_safety", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


check_public_safety = load_public_safety_module()


def finding_labels(findings: list[Any]) -> list[str]:
    return [finding.label for finding in findings]


def test_scan_line_reports_secret_labels_without_secret_values() -> None:
    token = "ghp_" + ("A" * 24)

    findings = check_public_safety.scan_line(Path("README.md"), 3, f"token={token}")

    assert finding_labels(findings) == ["github-token"]
    rendered_finding = check_public_safety.format_finding(findings[0])
    assert rendered_finding == "README.md:3: github-token"
    assert token not in rendered_finding


def test_scan_line_allows_documented_placeholders() -> None:
    placeholder_line = "Set XQUIK_API_KEY=xq_your_key or Authorization: Bearer token."

    findings = check_public_safety.scan_line(Path("README.md"), 8, placeholder_line)

    assert findings == []


def test_scan_line_flags_private_public_wording() -> None:
    line = f"Remove {'internal'} {'cost'} and {'private'} {'vendor'} wording."

    findings = check_public_safety.scan_line(Path("docs/example.md"), 13, line)

    assert finding_labels(findings) == ["internal-cost", "private-vendor"]


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
