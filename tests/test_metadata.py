from __future__ import annotations

import json
import tomllib
from pathlib import Path
from typing import cast

import pytest
import yaml

ROOT = Path(__file__).parents[1]
GUIDE_URL = "https://github.com/Xquik-dev/hermes-tweet#readme"
EXPECTED_TOOLS = ["tweet_explore", "tweet_read", "tweet_action"]
EXPECTED_PUBLIC_PACKAGE_DESCRIPTION = (
    "Native Hermes Agent plugin for X/Twitter automation through Xquik"
)
EXPECTED_OPTIONAL_ENV = ["XQUIK_BASE_URL", "HERMES_TWEET_ENABLE_ACTIONS"]
EXPECTED_SKILL_TAGS = [
    "hermes-agent",
    "xquik",
    "twitter",
    "x",
    "social-media",
    "automation",
]
EXPECTED_ASK_SKILL_METADATA = {
    "author": "Xquik",
    "repository": "https://github.com/Xquik-dev/hermes-tweet",
    "plugin": "hermes plugins install Xquik-dev/hermes-tweet --enable",
}
EXPECTED_AGENT_SKILL_MANIFEST_TAGS = [
    "hermes-agent",
    "hermes-plugin",
    "xquik",
    "twitter",
    "x",
    "social-media",
    "automation",
]
EXPECTED_AGENT_SKILL_INSTALL = "hermes plugins install Xquik-dev/hermes-tweet --enable"
EXPECTED_DASHBOARD_MANIFEST_DESCRIPTION = (
    "Hermes Agent X/Twitter plugin for searching tweets, reading replies, "
    "monitoring X, exporting followers, and approval-gated posting through Xquik."
)
EXPECTED_HERMES_ECO_MANIFEST_NAME = "Hermes Tweet"
EXPECTED_HERMES_ECO_MANIFEST_TYPE = "integration"
EXPECTED_HERMES_ECO_MANIFEST_CATEGORY = "communication"
SETUP_UV_ACTION = "astral-sh/setup-uv@v8.1.0"
ACTIONLINT_MODULE = "github.com/rhysd/actionlint/cmd/actionlint@v1.7.12"
EXPECTED_PUBLIC_IGNORE_PATTERNS = [
    ".env",
    ".env.*",
    "!.env.example",
    ".envrc",
    ".direnv/",
    ".npmrc",
    ".pypirc",
    "*.pem",
    "*.key",
    "*.token",
    "*.secret",
    ".pytest_cache/",
    ".ruff_cache/",
    ".mypy_cache/",
    ".pyright/",
    ".basedpyright/",
    ".coverage",
    ".coverage.*",
    "coverage.xml",
    "htmlcov/",
    "junit*.xml",
    "*.prof",
    "*.sarif",
    "reports/",
    "build/",
    "dist/",
    "*.egg-info/",
    ".hermes/",
    ".codex/",
    ".agents/",
    ".playwright-cli/",
    "sessions/",
    "logs/",
    "*.log",
    "*.log.*",
    "*.db",
    "*.sqlite",
    "*.sqlite3",
    "*.ipynb",
    ".ipynb_checkpoints/",
    "screenshots/",
]


def load_mapping(path: Path) -> dict[str, object]:
    data = yaml.safe_load(path.read_text())
    assert isinstance(data, dict)
    return cast("dict[str, object]", data)


def load_object_mapping(path: Path) -> dict[object, object]:
    data = yaml.safe_load(path.read_text())
    assert isinstance(data, dict)
    return cast("dict[object, object]", data)


def require_mapping(value: object) -> dict[str, object]:
    assert isinstance(value, dict)
    return cast("dict[str, object]", value)


def require_list(value: object) -> list[object]:
    assert isinstance(value, list)
    return cast("list[object]", value)


def load_skill_frontmatter(path: Path) -> dict[str, object]:
    content = path.read_text()
    assert content.startswith("---\n")
    _, frontmatter, _ = content.split("---", 2)
    data = yaml.safe_load(frontmatter)
    assert isinstance(data, dict)
    return cast("dict[str, object]", data)


def find_step(steps: list[object], name: str) -> dict[str, object]:
    for step in steps:
        step_mapping = require_mapping(step)
        if step_mapping.get("name") == name:
            return step_mapping

    message = f"No workflow step named {name!r}."
    raise AssertionError(message)


def test_find_step_reports_missing_workflow_step() -> None:
    with pytest.raises(AssertionError, match=r"No workflow step named 'Publish'\."):
        find_step([], "Publish")


def test_release_metadata_surfaces_stay_aligned() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    version = pyproject["project"]["version"]

    assert pyproject["project"]["description"] == EXPECTED_PUBLIC_PACKAGE_DESCRIPTION
    assert str(load_mapping(ROOT / "plugin.yaml")["version"]) == version
    assert str(load_mapping(ROOT / "hermes_tweet" / "plugin.yaml")["version"]) == version

    readme = (ROOT / "README.md").read_text()
    assert f"/releases/tag/v{version}" in readme
    assert EXPECTED_PUBLIC_PACKAGE_DESCRIPTION in readme

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
    assert root_manifest["description"] == EXPECTED_PUBLIC_PACKAGE_DESCRIPTION
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


def test_registry_skill_mirrors_bundled_skill() -> None:
    bundled_skill = ROOT / "hermes_tweet" / "skills" / "hermes-tweet" / "SKILL.md"
    registry_skill = ROOT / "skills" / "hermes-tweet" / "SKILL.md"
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    version = pyproject["project"]["version"]

    assert registry_skill.read_text().rstrip() == bundled_skill.read_text().rstrip()

    frontmatter = load_skill_frontmatter(bundled_skill)
    assert frontmatter["name"] == "hermes-tweet"
    assert str(frontmatter["version"]) == version
    assert frontmatter["author"] == "Xquik"
    assert frontmatter["tags"] == EXPECTED_SKILL_TAGS

    marketplace_metadata = require_mapping(frontmatter["metadata"])
    assert str(marketplace_metadata["version"]) == version
    assert marketplace_metadata["author"] == "Xquik"
    assert marketplace_metadata["tags"] == EXPECTED_SKILL_TAGS


def test_ask_wrapper_skill_matches_public_package_metadata() -> None:
    ask_skill = ROOT / "registries" / "ask" / "hermes-tweet" / "SKILL.md"
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    version = pyproject["project"]["version"]

    frontmatter = load_skill_frontmatter(ask_skill)
    assert frontmatter["name"] == "hermes-tweet"
    assert str(frontmatter["version"]) == version
    assert frontmatter["author"] == "Xquik"
    assert frontmatter["description"] == (
        "Search Twitter/X, read tweet replies, look up users, monitor tweets, "
        "export followers, and gate X actions through Xquik."
    )
    assert frontmatter["tags"] == EXPECTED_SKILL_TAGS

    ask_metadata = require_mapping(frontmatter["metadata"])
    assert ask_metadata == EXPECTED_ASK_SKILL_METADATA | {"version": version}


def test_agent_skill_manifest_matches_public_package_metadata() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    project = pyproject["project"]
    manifest = json.loads((ROOT / "skill.json").read_text())

    assert manifest["name"] == project["name"]
    assert manifest["version"] == project["version"]
    assert manifest["author"] == "Xquik"
    assert manifest["description"] == "Hermes Agent X/Twitter plugin for Xquik automation"
    assert manifest["tags"] == EXPECTED_AGENT_SKILL_MANIFEST_TAGS
    assert manifest["dependencies"] == []
    assert manifest["conflicts"] == []
    assert manifest["install"] == {"openclaw": EXPECTED_AGENT_SKILL_INSTALL}
    assert manifest["homepage"] == GUIDE_URL
    assert manifest["repository"] == project["urls"]["Repository"]
    assert set(manifest["keywords"]).issubset(project["keywords"])
    assert "include skill.json" in (ROOT / "MANIFEST.in").read_text().splitlines()


def test_plugin_hub_manifest_matches_public_package_metadata() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    project = pyproject["project"]
    manifest = json.loads((ROOT / "dashboard" / "manifest.json").read_text())

    assert manifest["name"] == project["name"]
    assert manifest["label"] == "Hermes Tweet"
    assert manifest["version"] == project["version"]
    assert manifest["description"] == EXPECTED_DASHBOARD_MANIFEST_DESCRIPTION
    assert manifest["slots"] == ["tools"]
    assert "include dashboard/manifest.json" in (ROOT / "MANIFEST.in").read_text().splitlines()


def test_hermes_eco_manifest_matches_public_package_metadata() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    project = pyproject["project"]
    manifest = json.loads((ROOT / ".hermes-eco.json").read_text())

    assert manifest["name"] == EXPECTED_HERMES_ECO_MANIFEST_NAME
    assert manifest["resource_type"] == EXPECTED_HERMES_ECO_MANIFEST_TYPE
    assert manifest["type"] == EXPECTED_HERMES_ECO_MANIFEST_TYPE
    assert manifest["primary_category"] == EXPECTED_HERMES_ECO_MANIFEST_CATEGORY
    assert manifest["description"] == EXPECTED_DASHBOARD_MANIFEST_DESCRIPTION
    assert manifest["author"] == "Xquik"
    assert manifest["repository"] == project["urls"]["Repository"]
    assert manifest["homepage"] == GUIDE_URL
    assert manifest["license"] == project["license"]
    assert manifest["tags"] == EXPECTED_AGENT_SKILL_MANIFEST_TAGS
    assert manifest["tools_used"] == EXPECTED_TOOLS
    assert "include .hermes-eco.json" in (ROOT / "MANIFEST.in").read_text().splitlines()


def test_public_repo_ignore_rules_cover_local_artifacts() -> None:
    ignore_patterns = set((ROOT / ".gitignore").read_text().splitlines())
    missing_patterns = sorted(set(EXPECTED_PUBLIC_IGNORE_PATTERNS) - ignore_patterns)

    assert missing_patterns == []


def test_publish_workflow_requires_version_matched_release_tag() -> None:
    workflow = load_object_mapping(ROOT / ".github" / "workflows" / "publish.yml")
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    version = pyproject["project"]["version"]

    # PyYAML 1.1 treats the GitHub Actions "on" key as boolean true.
    on_config = require_mapping(workflow[True])
    release = require_mapping(on_config["release"])
    assert release["types"] == ["published"]

    workflow_dispatch = require_mapping(on_config["workflow_dispatch"])
    inputs = require_mapping(workflow_dispatch["inputs"])
    ref_input = require_mapping(inputs["ref"])
    assert ref_input["required"] is True
    assert ref_input["description"] == f"Release tag to publish, such as v{version}"
    assert "default" not in ref_input

    jobs = require_mapping(workflow["jobs"])
    build = require_mapping(jobs["build"])
    build_steps = require_list(build["steps"])

    install_uv_step = find_step(build_steps, "Install uv")
    assert install_uv_step["uses"] == SETUP_UV_ACTION

    checkout_step = find_step(build_steps, "Checkout")
    checkout_config = require_mapping(checkout_step["with"])
    assert checkout_config["ref"] == "${{ github.event.inputs.ref || github.ref_name }}"

    validate_step = find_step(build_steps, "Validate release tag")
    validate_env = require_mapping(validate_step["env"])
    assert validate_env["RELEASE_REF"] == "${{ github.event.inputs.ref || github.ref_name }}"

    validate_script = validate_step["run"]
    assert isinstance(validate_script, str)
    assert "pyproject.toml" in validate_script
    assert 'expected_ref = f"v{version}"' in validate_script
    assert 'actual_ref = os.environ["RELEASE_REF"]' in validate_script
    assert "pyproject version tag" in validate_script

    publish = require_mapping(jobs["publish"])
    publish_permissions = require_mapping(publish["permissions"])
    assert publish_permissions == {"contents": "read", "id-token": "write"}


def test_ci_workflow_runs_actionlint_before_python_checks() -> None:
    workflow = load_object_mapping(ROOT / ".github" / "workflows" / "ci.yml")

    # PyYAML 1.1 treats the GitHub Actions "on" key as boolean true.
    on_config = require_mapping(workflow[True])
    assert "pull_request" in on_config
    assert "workflow_dispatch" in on_config

    jobs = require_mapping(workflow["jobs"])
    check = require_mapping(jobs["check"])
    steps = require_list(check["steps"])

    step_names = [require_mapping(step)["name"] for step in steps]
    assert step_names.index("Workflow lint") < step_names.index("Install uv")
    assert step_names.index("Workflow lint") < step_names.index("Test with coverage")

    setup_go_step = find_step(steps, "Set up Go")
    assert setup_go_step["uses"] == "actions/setup-go@v6"
    setup_go_config = require_mapping(setup_go_step["with"])
    assert setup_go_config["go-version"] == "stable"
    assert setup_go_config["cache"] is False

    workflow_lint_step = find_step(steps, "Workflow lint")
    assert workflow_lint_step["run"] == f"go run {ACTIONLINT_MODULE}"

    install_uv_step = find_step(steps, "Install uv")
    assert install_uv_step["uses"] == SETUP_UV_ACTION
