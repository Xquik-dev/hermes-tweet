# SPDX-FileCopyrightText: 2026 Xquik Contributors
# SPDX-License-Identifier: MIT

from __future__ import annotations

import json
import tomllib
from pathlib import Path
from typing import cast

import pytest
import yaml
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

ROOT = Path(__file__).parents[1]
GUIDE_URL = "https://github.com/Xquik-dev/hermes-tweet#readme"
CLAW_HUB_URL = "https://clawhub.ai/xquik/hermes-tweet"
EXPECTED_TOOLS = ["tweet_explore", "tweet_read", "tweet_action"]
EXPECTED_PUBLIC_PACKAGE_DESCRIPTION = (
    "Hermes Agent plugin for Twitter search, monitoring, follower exports & "
    "approved X actions. Not affiliated with X Corp."
)
EXPECTED_OPTIONAL_ENV = ["XQUIK_BASE_URL", "HERMES_TWEET_ENABLE_ACTIONS"]
EXPECTED_SKILL_CAPABILITY_ENV = [
    "XQUIK_API_KEY",
    "HERMES_TWEET_ENABLE_ACTIONS",
    "HERMES_ENABLE_PROJECT_PLUGINS",
]
EXPECTED_SKILL_TAGS = [
    "hermes-agent",
    "xquik",
    "twitter",
    "x",
    "social-media",
    "automation",
]
EXPECTED_MARKETPLACE_SKILL_AUTHOR = "Burak Bay\u0131r (@burak-bayir), Xquik"
EXPECTED_VERIFIED_SKILL_COMMIT = "c6ebdd7060965dd16a89e8cc12675ff834b5cc94"
EXPECTED_MARKETPLACE_SKILL_FIELDS = {
    "name",
    "description",
    "allowed-tools",
    "version",
    "author",
    "license",
    "compatibility",
    "tags",
}
EXPECTED_MARKETPLACE_SKILL_SECTIONS = (
    "## Overview",
    "## Prerequisites",
    "## Instructions",
    "## Output",
    "## Error handling",
    "## Examples",
    "## Resources",
)
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
EXPECTED_CLAUDE_PLUGIN_DESCRIPTION = (
    "Hermes Agent plugin for Twitter search, monitoring, follower exports & "
    "approved X actions. Not affiliated with X Corp."
)
EXPECTED_CODEX_PLUGIN_KEYWORDS = [*EXPECTED_AGENT_SKILL_MANIFEST_TAGS, "codex-plugin"]
EXPECTED_AGENT_SKILL_INSTALL = "hermes plugins install Xquik-dev/hermes-tweet --enable"
EXPECTED_TOPIC_DISCOVERY_KEYWORD = "agent-skill"
EXPECTED_DASHBOARD_MANIFEST_DESCRIPTION = (
    "Hermes Agent plugin for Twitter search, monitoring, follower exports & "
    "approved X actions. Not affiliated with X Corp."
)
EXPECTED_HERMES_ECO_MANIFEST_NAME = "Hermes Tweet"
EXPECTED_HERMES_ECO_MANIFEST_TYPE = "integration"
EXPECTED_HERMES_ECO_MANIFEST_CATEGORY = "communication"
SUBMISSION_READINESS_PATH = "docs/SUBMISSION_READINESS.md"
EXPECTED_SUBMISSION_READINESS_SURFACES = (
    ROOT / "docs" / "PUBLICATION_CHECKLIST.md",
    ROOT / "docs" / "HERMES_SURFACES.md",
    ROOT / "docs" / "INTEGRATION_PATTERNS.md",
    ROOT / "docs" / "ECOSYSTEM.md",
    ROOT / "docs" / "GITHUB_METADATA.md",
)
EXPECTED_LIVE_ECOSYSTEM_SURFACES = (
    (
        "OpenJarvis Hermes Tweet skill install example",
        "https://github.com/open-jarvis/OpenJarvis/blob/main/docs/user-guide/skills.md",
    ),
    (
        "Claude Skill Registry Data Hermes Tweet archive",
        (
            "https://github.com/majiayu000/claude-skill-registry-data/blob/main/api/"
            "hermes-tweet/SKILL.md"
        ),
    ),
    (
        "Freya Hermes Tweet skill install example",
        "https://github.com/willtanoe/freya/blob/xtr/docs/user-guide/skills.md",
    ),
    (
        "Awesome Skill Forge Hermes Tweet mirror",
        (
            "https://raw.githubusercontent.com/Lord1Egypt/awesome-skill-forge/master/community/"
            "clawhub/h/hermes-tweet/SKILL.md"
        ),
    ),
    (
        "RA-Skills Hermes Tweet mirror",
        (
            "https://github.com/Lord1Egypt/RA-Skills/blob/master/skills/community/"
            "clawhub/h/hermes-tweet/SKILL.md"
        ),
    ),
)
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


def assert_skill_capabilities(frontmatter: dict[str, object]) -> None:
    capabilities = require_mapping(frontmatter["capabilities"])
    shell = require_mapping(capabilities["shell"])
    network = require_mapping(capabilities["network"])
    files = require_mapping(capabilities["files"])
    environment = require_mapping(capabilities["environment"])
    mcp = require_mapping(capabilities["mcp"])

    assert shell["required"] is False
    assert network["required"] is True
    assert files["required"] is False
    assert environment["required"] is True
    assert mcp["required"] is False
    assert require_list(environment["variables"]) == EXPECTED_SKILL_CAPABILITY_ENV
    assert require_list(capabilities["tools"]) == EXPECTED_TOOLS


def normalize_requirement(requirement: str) -> tuple[str, dict[str, object]]:
    parsed = Requirement(requirement)
    return (
        canonicalize_name(parsed.name),
        {"extras": sorted(parsed.extras), "specifier": str(parsed.specifier)},
    )


def normalize_locked_requirement(requirement: object) -> tuple[str, dict[str, object]]:
    requirement_data = require_mapping(requirement)
    extras = require_list(requirement_data.get("extras", []))
    return (
        canonicalize_name(str(requirement_data["name"])),
        {
            "extras": sorted(str(extra) for extra in extras),
            "specifier": str(requirement_data["specifier"]),
        },
    )


def find_locked_package(packages: list[object], name: str) -> dict[str, object]:
    for package in packages:
        package_data = require_mapping(package)
        if package_data["name"] == name:
            return package_data

    message = f"No lockfile package named {name!r}."
    raise AssertionError(message)


def load_skill_frontmatter(path: Path) -> dict[str, object]:
    content = path.read_text()
    assert content.startswith("---\n")
    _, frontmatter, _ = content.split("---", 2)
    data = yaml.safe_load(frontmatter)
    assert isinstance(data, dict)
    return cast("dict[str, object]", data)


def test_find_locked_package_reports_missing_package() -> None:
    with pytest.raises(AssertionError, match=r"No lockfile package named 'hermes-tweet'\."):
        find_locked_package([], "hermes-tweet")


def test_release_metadata_surfaces_stay_aligned() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    version = pyproject["project"]["version"]

    assert pyproject["project"]["description"] == EXPECTED_PUBLIC_PACKAGE_DESCRIPTION
    assert str(load_mapping(ROOT / "plugin.yaml")["version"]) == version
    assert str(load_mapping(ROOT / "hermes_tweet" / "plugin.yaml")["version"]) == version

    for surface in EXPECTED_SUBMISSION_READINESS_SURFACES:
        assert SUBMISSION_READINESS_PATH in surface.read_text(encoding="utf-8")

    urls = pyproject["project"]["urls"]
    assert urls["Homepage"] == GUIDE_URL
    assert urls["Documentation"] == GUIDE_URL
    assert urls["Repository"] == "https://github.com/Xquik-dev/hermes-tweet"
    assert urls["Issues"] == "https://github.com/Xquik-dev/hermes-tweet/issues"


def test_merge_enablement_guide_requires_complete_pr_coverage() -> None:
    guide = (ROOT / "docs" / "MERGE_ENABLEMENT.md").read_text()
    normalized_guide = " ".join(guide.split())

    assert "Enumerate every open in-scope PR before discovery or outreach" in normalized_guide
    assert "A capped GitHub CLI result is incomplete" in normalized_guide
    assert "hermes-tweet-open-prs-<timestamp>.json" in guide
    assert "hermes-tweet-pr-audit-<timestamp>.jsonl" in guide
    assert "author, head owner, base repository" in normalized_guide
    assert "unresolved review threads" in normalized_guide
    assert "verified `burak-bayir` branches" in guide
    assert "aggregate `UNKNOWN` mergeability" in guide
    assert "direct PR read" in guide
    assert "reports `DIRTY` or `CONFLICTING`" in normalized_guide
    assert "prepared fork branch is not outreach" in normalized_guide
    assert "record the API error" in guide
    assert "improve first-party" in guide


def test_ecosystem_tracks_validated_live_surfaces() -> None:
    ecosystem = (ROOT / "docs" / "ECOSYSTEM.md").read_text()

    for label, url in EXPECTED_LIVE_ECOSYSTEM_SURFACES:
        assert f"| {label} | <{url}> |" in ecosystem


def test_uv_lock_separates_dev_dependency_constraints() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    lockfile = tomllib.loads((ROOT / "uv.lock").read_text())

    expected = dict(
        normalize_requirement(requirement) for requirement in pyproject["dependency-groups"]["dev"]
    )
    packages = require_list(lockfile["package"])
    package = find_locked_package(packages, "hermes-tweet")
    metadata = require_mapping(package["metadata"])
    requires_dev = require_list(require_mapping(metadata["requires-dev"])["dev"])
    locked = dict(normalize_locked_requirement(require_mapping(item)) for item in requires_dev)

    assert locked == expected
    assert metadata["requires-dist"] == [{"name": "httpx", "specifier": ">=0.28.1,<0.29"}]
    assert "provides-extras" not in metadata


def test_docs_track_current_hermes_agent_release() -> None:
    docs = "\n".join(
        [
            (ROOT / "README.md").read_text(),
            (ROOT / "docs" / "CONTEXT7.md").read_text(),
            (ROOT / "docs" / "HERMES_SURFACES.md").read_text(),
            (ROOT / "docs" / "OBSERVABILITY.md").read_text(),
            (ROOT / "hermes_tweet" / "skills" / "hermes-tweet" / "SKILL.md").read_text(),
        ],
    )

    assert "Hermes Agent v0.16.0" in docs
    assert "remote gateway" in docs
    assert "Hermes Desktop" in docs
    assert "Hermes v0.12.0" not in docs


def test_hermes_host_guide_keeps_runtime_contract_visible() -> None:
    guide = (ROOT / "docs" / "HERMES_SURFACES.md").read_text()

    assert "remote Hermes host" in guide
    assert "host that executes plugin tools" in guide
    assert "HERMES_TWEET_ENABLE_ACTIONS=false" in guide
    assert "HERMES_TWEET_ENABLE_ACTIONS=true" in guide
    assert "hermes plugins install Xquik-dev/hermes-tweet --enable" in guide
    assert 'hermes -z "/xstatus"' in guide


def test_integration_patterns_classify_marketplace_bridges() -> None:
    guide = (ROOT / "docs" / "INTEGRATION_PATTERNS.md").read_text()

    assert "**Claude marketplace bridges.**" in guide
    assert "compatibility routes, not as catalog targets" in guide
    assert "`hermes plugins install Xquik-dev/hermes-tweet --enable`" in guide
    assert "`.claude-plugin/plugin.json` metadata" in guide
    assert "**Codex marketplace bridges.**" in guide
    assert "`.codex-plugin/plugin.json` metadata" in guide
    assert "HOL Plugin Scanner evidence" in guide


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


def test_plugin_needs_nothing_installed_by_hermes() -> None:
    project = require_mapping(tomllib.loads((ROOT / "pyproject.toml").read_text())["project"])

    assert load_mapping(ROOT / "plugin.yaml")["python_runtime"] == "external"
    assert project["dependencies"] == ["httpx>=0.28.1,<0.29"]


def test_registry_skill_mirrors_bundled_skill() -> None:
    bundled_skill = ROOT / "hermes_tweet" / "skills" / "hermes-tweet" / "SKILL.md"
    registry_skill = ROOT / "skills" / "hermes-tweet" / "SKILL.md"
    bundled_text = bundled_skill.read_text()
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    version = pyproject["project"]["version"]

    assert registry_skill.read_text().rstrip() == bundled_text.rstrip()
    assert "## Permissions and capabilities" in bundled_text
    assert "## Known risks and mitigations" in bundled_text
    assert "## Output" in bundled_text
    assert "## Error handling" in bundled_text
    assert "## Resources" in bundled_text
    assert "## Release trust gate" in bundled_text
    assert "SkillSpector" in bundled_text
    assert "skill-card.md" in bundled_text
    assert "skill.oms.sig" in bundled_text

    frontmatter = load_skill_frontmatter(bundled_skill)
    assert frontmatter["name"] == "hermes-tweet"
    assert str(frontmatter["version"]) == version
    assert frontmatter["author"] == EXPECTED_MARKETPLACE_SKILL_AUTHOR
    assert frontmatter["allowed-tools"] == EXPECTED_TOOLS
    assert frontmatter["license"] == "MIT"
    assert frontmatter["compatibility"] == (
        "Requires Hermes Agent plugin support and Xquik API access."
    )
    assert frontmatter["repo"] == "https://github.com/Xquik-dev/hermes-tweet"
    assert frontmatter["homepage"] == GUIDE_URL
    assert frontmatter["commit"] == EXPECTED_VERIFIED_SKILL_COMMIT
    assert frontmatter["languages"] == ["en"]
    assert len(str(frontmatter["description"])) >= 160
    assert frontmatter["tags"] == EXPECTED_SKILL_TAGS
    assert_skill_capabilities(frontmatter)

    marketplace_metadata = require_mapping(frontmatter["metadata"])
    assert str(marketplace_metadata["version"]) == version
    assert marketplace_metadata["author"] == "Xquik"
    assert marketplace_metadata["tags"] == EXPECTED_SKILL_TAGS


@pytest.mark.parametrize(
    "relative_path",
    [
        "skills/hermes-tweet/SKILL.md",
        "hermes_tweet/skills/hermes-tweet/SKILL.md",
    ],
)
def test_marketplace_skill_contract(relative_path: str) -> None:
    skill_path = ROOT / relative_path
    skill_text = skill_path.read_text(encoding="utf-8")
    frontmatter = load_skill_frontmatter(skill_path)

    assert set(frontmatter) >= EXPECTED_MARKETPLACE_SKILL_FIELDS
    assert frontmatter["allowed-tools"] == EXPECTED_TOOLS
    assert frontmatter["author"] == EXPECTED_MARKETPLACE_SKILL_AUTHOR
    assert "Use when" in str(frontmatter["description"])
    assert "Trigger with" in str(frontmatter["description"])

    section_positions = [
        skill_text.index(section) for section in EXPECTED_MARKETPLACE_SKILL_SECTIONS
    ]
    assert section_positions == sorted(section_positions)

    required_environment_variables = require_list(frontmatter["required_environment_variables"])
    assert required_environment_variables == [
        {
            "name": "XQUIK_API_KEY",
            "prompt": "Xquik API key",
            "help": "Create an API key at https://dashboard.xquik.com",
            "required_for": ("tweet_read, /xstatus, /xtrends, and authenticated Xquik API calls"),
        }
    ]


def test_skill_reference_mirrors_bundled_reference() -> None:
    relative_reference = Path("references") / "endpoint-contract.md"
    registry_reference = ROOT / "skills" / "hermes-tweet" / relative_reference
    bundled_reference = ROOT / "hermes_tweet" / "skills" / "hermes-tweet" / relative_reference
    reference_text = registry_reference.read_text(encoding="utf-8")

    assert bundled_reference.read_text(encoding="utf-8") == reference_text
    assert "## Tool matrix" in reference_text
    assert "## Approval checklist" in reference_text
    assert "HERMES_TWEET_ENABLE_ACTIONS=true" in reference_text

    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    wheel_packages = pyproject["tool"]["hatch"]["build"]["targets"]["wheel"]["packages"]
    assert wheel_packages == ["hermes_tweet"]


def test_skill_card_mirrors_bundled_skill_card() -> None:
    registry_card = ROOT / "skills" / "hermes-tweet" / "skill-card.md"
    bundled_card = ROOT / "hermes_tweet" / "skills" / "hermes-tweet" / "skill-card.md"
    card_text = bundled_card.read_text()
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    version = pyproject["project"]["version"]

    assert registry_card.read_text().rstrip() == card_text.rstrip()
    assert f"- **Version.** {version}" in card_text
    assert "public self-assessment, not NVIDIA verification" in card_text
    assert "## Owner" in card_text
    assert "## Use case" in card_text
    assert "## Inputs and configuration" in card_text
    assert "## Capabilities" in card_text
    assert "## Outputs" in card_text
    assert "## Side effects" in card_text
    assert "## Known risks and mitigations" in card_text
    assert "## Release trust gate" in card_text
    assert "SkillSpector scan report" in card_text
    assert "Tier-3 eval data" in card_text
    assert "skill.oms.sig" in card_text
    assert "XQUIK_API_KEY" in card_text
    assert "HERMES_TWEET_ENABLE_ACTIONS=true" in card_text
    assert "tweet_explore" in card_text
    assert "tweet_read" in card_text
    assert "tweet_action" in card_text


def test_ask_wrapper_skill_matches_public_package_metadata() -> None:
    ask_skill = ROOT / "registries" / "ask" / "hermes-tweet" / "SKILL.md"
    ask_text = ask_skill.read_text()
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    version = pyproject["project"]["version"]

    frontmatter = load_skill_frontmatter(ask_skill)
    assert frontmatter["name"] == "hermes-tweet"
    assert str(frontmatter["version"]) == version
    assert frontmatter["author"] == "Xquik"
    assert frontmatter["description"] == (
        "Search Twitter/X, read replies, find users, monitor accounts, export "
        "followers & gate X actions through Xquik. Not affiliated with X Corp."
    )
    assert frontmatter["tags"] == EXPECTED_SKILL_TAGS
    assert_skill_capabilities(frontmatter)

    ask_metadata = require_mapping(frontmatter["metadata"])
    assert ask_metadata == EXPECTED_ASK_SKILL_METADATA | {"version": version}
    assert "## Permissions and trust" in ask_text
    assert "SkillSpector" in ask_text
    assert "skill-card.md" in ask_text
    assert "skill.oms.sig" in ask_text


def test_agent_skill_manifest_matches_public_package_metadata() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    project = pyproject["project"]
    manifest = json.loads((ROOT / "skill.json").read_text())

    assert manifest["name"] == project["name"]
    assert manifest["version"] == project["version"]
    assert manifest["author"] == "Xquik"
    assert manifest["description"] == (
        "Hermes Agent plugin for Twitter search, monitoring, follower exports & "
        "approved X actions. Not affiliated with X Corp."
    )
    assert manifest["tags"] == EXPECTED_AGENT_SKILL_MANIFEST_TAGS
    assert manifest["dependencies"] == []
    assert manifest["conflicts"] == []
    assert manifest["install"] == {"openclaw": EXPECTED_AGENT_SKILL_INSTALL}
    assert manifest["homepage"] == GUIDE_URL
    assert manifest["repository"] == project["urls"]["Repository"]
    assert set(manifest["keywords"]).issubset(project["keywords"])
    assert "include skill.json" in (ROOT / "MANIFEST.in").read_text().splitlines()


def test_agent_skill_manifest_advertises_topic_based_registry_metadata() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    manifest = json.loads((ROOT / "skill.json").read_text())
    metadata = (ROOT / "docs" / "GITHUB_METADATA.md").read_text()

    assert EXPECTED_TOPIC_DISCOVERY_KEYWORD in pyproject["project"]["keywords"]
    assert EXPECTED_TOPIC_DISCOVERY_KEYWORD in manifest["keywords"]
    assert EXPECTED_TOPIC_DISCOVERY_KEYWORD in metadata


def test_claude_plugin_manifest_matches_public_package_metadata() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    project = pyproject["project"]
    manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())

    assert manifest["name"] == project["name"]
    assert manifest["version"] == project["version"]
    assert manifest["description"] == EXPECTED_CLAUDE_PLUGIN_DESCRIPTION
    assert manifest["author"] == {"name": "Xquik", "url": "https://github.com/Xquik-dev"}
    assert manifest["license"] == project["license"]
    assert manifest["homepage"] == GUIDE_URL
    assert manifest["repository"] == project["urls"]["Repository"]
    assert manifest["keywords"] == EXPECTED_AGENT_SKILL_MANIFEST_TAGS
    assert "include .claude-plugin/plugin.json" in (ROOT / "MANIFEST.in").read_text().splitlines()


def test_codex_plugin_manifest_matches_public_package_metadata() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    project = pyproject["project"]
    manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text())

    assert manifest["name"] == project["name"]
    assert manifest["version"] == project["version"]
    assert manifest["description"] == EXPECTED_CLAUDE_PLUGIN_DESCRIPTION
    assert manifest["author"] == {"name": "Xquik", "url": "https://github.com/Xquik-dev"}
    assert manifest["license"] == project["license"]
    assert manifest["homepage"] == GUIDE_URL
    assert manifest["repository"] == project["urls"]["Repository"]
    assert manifest["commit"] == EXPECTED_VERIFIED_SKILL_COMMIT
    assert manifest["verified"] is True
    assert manifest["keywords"] == EXPECTED_CODEX_PLUGIN_KEYWORDS
    assert manifest["skills"] == "./skills/"

    interface = require_mapping(manifest["interface"])
    assert interface["displayName"] == "Hermes Tweet"
    assert interface["developerName"] == "Xquik"
    assert interface["category"] == "Productivity"
    assert interface["capabilities"] == ["Interactive", "Read", "Write"]
    assert interface["websiteURL"] == GUIDE_URL
    assert (
        interface["privacyPolicyURL"] == "https://github.com/Xquik-dev/hermes-tweet/security/policy"
    )
    assert interface["termsOfServiceURL"] == (
        "https://github.com/Xquik-dev/hermes-tweet/blob/master/LICENSE"
    )
    assert interface["composerIcon"] == "./assets/icon.svg"
    assert interface["logo"] == "./assets/icon.svg"
    assert interface["screenshots"] == ["./assets/screenshot.svg"]

    manifest_lines = (ROOT / "MANIFEST.in").read_text().splitlines()
    assert "include .codex-plugin/plugin.json" in manifest_lines
    assert "include .codexignore" in manifest_lines
    assert "include SECURITY.md" in manifest_lines
    assert "include assets/icon.svg" in manifest_lines
    assert "include assets/screenshot.svg" in manifest_lines


def test_codexignore_blocks_local_and_sensitive_artifacts() -> None:
    ignored_paths = (ROOT / ".codexignore").read_text().splitlines()

    assert ".env.*" in ignored_paths
    assert ".venv/" in ignored_paths
    assert "*.pem" in ignored_paths
    assert "*.token" in ignored_paths
    assert "dist/" in ignored_paths


def test_root_security_policy_matches_github_security_policy() -> None:
    assert (ROOT / "SECURITY.md").read_text().rstrip() == (
        ROOT / ".github" / "SECURITY.md"
    ).read_text().rstrip()


def test_clawhub_metadata_uses_live_canonical_route() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
    ecosystem = (ROOT / "docs" / "ECOSYSTEM.md").read_text()

    assert project["urls"]["ClawHub"] == CLAW_HUB_URL
    assert f"<{CLAW_HUB_URL}>" in ecosystem
    assert "clawhub.ai/skills/hermes-tweet" not in ecosystem


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


def test_repository_has_no_github_actions_workflows() -> None:
    assert not (ROOT / ".github" / "workflows").exists()


def test_fuzz_harness_builds_from_pinned_dependencies() -> None:
    project = load_object_mapping(ROOT / ".clusterfuzzlite" / "project.yaml")
    assert project == {"language": "python"}
    dockerfile = (ROOT / ".clusterfuzzlite" / "Dockerfile").read_text()
    assert "base-builder-python@sha256:" in dockerfile
    dockerignore = (ROOT / ".dockerignore").read_text().splitlines()
    assert dockerignore[0] == "**"
    assert "!hermes_tweet/**" in dockerignore
    assert "!fuzz/**" in dockerignore
    assert "!.clusterfuzzlite/**" in dockerignore
    build_script = (ROOT / ".clusterfuzzlite" / "build.sh").read_text()
    assert "--require-hashes" in build_script
    assert "--no-deps" in build_script
    assert "--only-binary=:all:" in build_script
    assert "requirements.txt" in build_script
    fuzz_requirements = (ROOT / ".clusterfuzzlite" / "requirements.txt").read_text()
    assert "httpx==0.28.1" in fuzz_requirements
    assert "--hash=sha256:" in fuzz_requirements
    assert "pyinstaller" in build_script
    assert (
        '--add-data "${SRC}/hermes-tweet/hermes_tweet/catalog_data.json:hermes_tweet"'
        in build_script
    )
    assert '--paths "${SRC}/hermes-tweet"' in build_script
    assert "LLVMFuzzerTestOneInput" in build_script
    fuzzer = (ROOT / "fuzz" / "normalization_fuzzer.py").read_text()
    compile(fuzzer, "normalization_fuzzer.py", "exec")
    assert "atheris.Setup" in fuzzer
    assert "atheris.Fuzz" in fuzzer


def test_release_gate_runs_hermes_agent_compatibility_checker() -> None:
    checklist = (ROOT / "docs" / "PUBLICATION_CHECKLIST.md").read_text()

    assert (
        "uv run --python 3.12 --group dev python scripts/check_hermes_agent_compat.py" in checklist
    )
    assert "uv run --python 3.12 --group dev python scripts/check_public_safety.py" in checklist
    assert "source SHA changes" in checklist
    reproducible_command = "uv run --python 3.12 --group dev bash scripts/check_reproducible.sh"
    assert reproducible_command in checklist
