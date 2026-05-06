from __future__ import annotations

import tomllib
from pathlib import Path
from typing import cast

import yaml

ROOT = Path(__file__).parents[1]
GUIDE_URL = "https://docs.xquik.com/guides/hermes-tweet"
EXPECTED_TOOLS = ["tweet_explore", "tweet_read", "tweet_action"]
EXPECTED_OPTIONAL_ENV = ["XQUIK_BASE_URL", "HERMES_TWEET_ENABLE_ACTIONS"]


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


def test_plugin_manifests_keep_install_prompt_contract() -> None:
    root_manifest = load_mapping(ROOT / "plugin.yaml")
    package_manifest = load_mapping(ROOT / "hermes_tweet" / "plugin.yaml")

    assert root_manifest == package_manifest
    assert root_manifest["name"] == "hermes-tweet"
    assert root_manifest["provides_tools"] == EXPECTED_TOOLS
    assert root_manifest["optional_env"] == EXPECTED_OPTIONAL_ENV

    requires_env = root_manifest["requires_env"]
    assert isinstance(requires_env, list)
    assert requires_env == [
        {
            "name": "XQUIK_API_KEY",
            "description": "Xquik API key. Create one in the Xquik dashboard.",
            "url": "https://dashboard.xquik.com",
            "secret": True,
        }
    ]
