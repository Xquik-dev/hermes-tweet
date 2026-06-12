from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).parents[1]


def load_public_surfaces_module() -> Any:
    module_path = ROOT / "scripts" / "public_surfaces.py"
    spec = importlib.util.spec_from_file_location("public_surfaces", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


public_surfaces = load_public_surfaces_module()


def test_default_public_surface_selection_uses_registry() -> None:
    files = public_surfaces.select_public_surface_files(None)

    assert files is public_surfaces.PUBLIC_SURFACE_FILES


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
