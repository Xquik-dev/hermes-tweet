# SPDX-FileCopyrightText: 2026 Xquik Contributors
# SPDX-License-Identifier: MIT

from __future__ import annotations

import re
from pathlib import Path

import pytest
from scripts import public_surfaces

ROOT = Path(__file__).parents[1]


def test_default_public_surface_selection_uses_registry() -> None:
    files = public_surfaces.select_public_surface_files(None)

    assert files is public_surfaces.PUBLIC_SURFACE_FILES


def test_public_surface_registry_uses_normalized_relative_files() -> None:
    for file_name in public_surfaces.PUBLIC_SURFACE_FILES:
        path = Path(file_name)
        assert not path.is_absolute()
        assert not file_name.startswith("./")
        assert ".." not in path.parts


def test_public_surface_registry_files_exist() -> None:
    for file_name in public_surfaces.PUBLIC_SURFACE_FILES:
        assert (ROOT / file_name).is_file()


def test_public_surface_registry_files_are_utf8_text() -> None:
    for file_name in public_surfaces.PUBLIC_SURFACE_FILES:
        content = (ROOT / file_name).read_text(encoding="utf-8")

        assert "\x00" not in content


def test_public_surface_registry_has_unique_files() -> None:
    files = public_surfaces.PUBLIC_SURFACE_FILES

    assert len(files) == len(set(files))


def test_public_surface_selection_normalizes_dot_slash_targets() -> None:
    files = public_surfaces.select_public_surface_files(
        ("./README.md", "./docs/ECOSYSTEM.md"),
    )

    assert files == ("README.md", "docs/ECOSYSTEM.md")


def test_public_surface_selection_normalizes_absolute_targets() -> None:
    readme_path = ROOT / "README.md"
    ecosystem_path = ROOT / "docs" / "ECOSYSTEM.md"

    files = public_surfaces.select_public_surface_files(
        (str(readme_path), str(ecosystem_path)),
    )

    assert files == ("README.md", "docs/ECOSYSTEM.md")


def test_public_surface_selection_normalizes_relative_parent_segments() -> None:
    files = public_surfaces.select_public_surface_files(
        ("docs/../README.md", "docs/../docs/ECOSYSTEM.md"),
    )

    assert files == ("README.md", "docs/ECOSYSTEM.md")


def test_public_surface_selection_rejects_absolute_targets_outside_repo() -> None:
    outside_path = ROOT.parent / "private-notes.md"

    with pytest.raises(
        ValueError,
        match=rf"unregistered public files: {re.escape(str(outside_path))}",
    ) as exc_info:
        public_surfaces.select_public_surface_files((str(outside_path),))

    assert str(exc_info.value) == f"unregistered public files: {outside_path}"


def test_public_surface_selection_rejects_relative_targets_outside_repo() -> None:
    with pytest.raises(
        ValueError,
        match=r"unregistered public files: \.\./private-notes\.md",
    ):
        public_surfaces.select_public_surface_files(("../private-notes.md",))


def test_public_surface_selection_rejects_unknown_targets() -> None:
    with pytest.raises(
        ValueError,
        match=r"unregistered public files: private-notes\.md, scratch\.md",
    ):
        public_surfaces.select_public_surface_files(
            ("./private-notes.md", "scratch.md"),
        )


def test_public_surface_selection_rejects_duplicate_targets() -> None:
    with pytest.raises(ValueError, match=r"duplicate public files: README\.md"):
        public_surfaces.select_public_surface_files(("README.md", "./README.md"))


def test_public_surface_selection_reports_each_duplicate_once() -> None:
    with pytest.raises(ValueError, match=r"duplicate public files: README\.md") as exc_info:
        public_surfaces.select_public_surface_files(
            ("README.md", "./README.md", "docs/ECOSYSTEM.md", "README.md"),
        )

    assert str(exc_info.value) == "duplicate public files: README.md"
