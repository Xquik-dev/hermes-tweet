from __future__ import annotations

import importlib.util
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
