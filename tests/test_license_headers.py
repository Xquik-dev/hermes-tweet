# SPDX-FileCopyrightText: 2026 Xquik Contributors
# SPDX-License-Identifier: MIT

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import pytest

ROOT = Path(__file__).parents[1]


def load_license_header_module() -> Any:
    module_path = ROOT / "scripts" / "check_license_headers.py"
    spec = importlib.util.spec_from_file_location("check_license_headers", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


check_license_headers = load_license_header_module()


def write_source(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_select_source_files_includes_supported_source_formats(tmp_path: Path) -> None:
    expected_paths = {
        tmp_path / "__init__.py",
        tmp_path / ".clusterfuzzlite" / "Dockerfile",
        tmp_path / ".clusterfuzzlite" / "build.sh",
        tmp_path / ".github" / "workflows" / "ci.yml",
        tmp_path / "MANIFEST.in",
        tmp_path / "docs" / "example.py",
        tmp_path / "hermes_tweet" / "plugin.yaml",
        tmp_path / "pyproject.toml",
    }
    for path in expected_paths:
        write_source(path, "")
    write_source(tmp_path / "README.md", "")
    write_source(tmp_path / "plugin.json", "")
    write_source(tmp_path / "uv.lock", "")
    write_source(tmp_path / ".venv" / "dependency.py", "")
    write_source(tmp_path / "build" / "generated.py", "")

    source_files = check_license_headers.select_source_files(tmp_path)

    assert set(source_files) == expected_paths


def test_scan_source_file_accepts_required_notices(tmp_path: Path) -> None:
    source_path = tmp_path / "hermes_tweet" / "client.py"
    write_source(
        source_path,
        (
            f"{check_license_headers.COPYRIGHT_NOTICE}\n"
            f"{check_license_headers.LICENSE_NOTICE}\n\n"
            "VALUE = 1\n"
        ),
    )

    findings = check_license_headers.scan_source_file(source_path, tmp_path)

    assert findings == []


def test_scan_source_file_reports_each_missing_notice(tmp_path: Path) -> None:
    source_path = tmp_path / "scripts" / "check.py"
    write_source(source_path, "VALUE = 1\n")

    findings = check_license_headers.scan_source_file(source_path, tmp_path)

    assert findings == [
        check_license_headers.LicenseHeaderFinding(
            Path("scripts/check.py"),
            "copyright",
        ),
        check_license_headers.LicenseHeaderFinding(
            Path("scripts/check.py"),
            "license",
        ),
    ]
    assert check_license_headers.format_finding(findings[0]) == (
        "scripts/check.py: missing copyright notice"
    )


def test_scan_source_files_reports_relative_paths(tmp_path: Path) -> None:
    source_path = tmp_path / "fuzz" / "target.py"
    write_source(source_path, f"{check_license_headers.COPYRIGHT_NOTICE}\n")

    findings = check_license_headers.scan_source_files(tmp_path)

    assert findings == [
        check_license_headers.LicenseHeaderFinding(
            Path("fuzz/target.py"),
            "license",
        )
    ]


def test_main_accepts_complete_repository(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(check_license_headers, "select_source_files", lambda: (Path("a.py"),))
    monkeypatch.setattr(check_license_headers, "scan_source_files", list)

    result = check_license_headers.main(())
    captured = capsys.readouterr()

    assert result == 0
    assert captured.out == "checked=1 findings=0\n"
    assert captured.err == ""


def test_main_reports_findings(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    finding = check_license_headers.LicenseHeaderFinding(
        Path("client.py"),
        "license",
    )
    monkeypatch.setattr(check_license_headers, "select_source_files", lambda: (Path("a.py"),))
    monkeypatch.setattr(check_license_headers, "scan_source_files", lambda: [finding])

    result = check_license_headers.main(())
    captured = capsys.readouterr()

    assert result == 1
    assert captured.out == "checked=1 findings=1\nclient.py: missing license notice\n"
    assert captured.err == ""


def test_main_rejects_arguments(capsys: pytest.CaptureFixture[str]) -> None:
    result = check_license_headers.main(("client.py",))
    captured = capsys.readouterr()

    assert result == 1
    assert captured.out == "check_license_headers.py does not accept arguments\n"
    assert captured.err == ""
