from __future__ import annotations

import tomllib
from pathlib import Path
from typing import cast

import yaml

ROOT = Path(__file__).parents[1]
GUIDE_URL = "https://docs.xquik.com/guides/hermes-tweet"


def load_mapping(path: Path) -> dict[str, object]:
    data = yaml.safe_load(path.read_text())
    assert isinstance(data, dict)
    return cast("dict[str, object]", data)


def test_release_metadata_surfaces_stay_aligned() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    version = pyproject["project"]["version"]

    assert str(load_mapping(ROOT / "plugin.yaml")["version"]) == version
    assert str(load_mapping(ROOT / "hermes_tweet" / "plugin.yaml")["version"]) == version

    readme = (ROOT / "README.md").read_text()
    assert f"/releases/tag/v{version}" in readme

    urls = pyproject["project"]["urls"]
    assert urls["Homepage"] == GUIDE_URL
    assert urls["Documentation"] == GUIDE_URL
    assert urls["Repository"] == "https://github.com/Xquik-dev/hermes-tweet"
    assert urls["Issues"] == "https://github.com/Xquik-dev/hermes-tweet/issues"
