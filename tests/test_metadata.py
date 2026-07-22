from __future__ import annotations

import json
import re
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
    "Native Hermes Agent plugin for X/Twitter automation through Xquik. Not affiliated with X Corp."
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
EXPECTED_MARKETPLACE_SKILL_AUTHOR = "Burak Bay\u0131r (@kriptoburak), Xquik"
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
    "## Error Handling",
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
    "Native Hermes Agent X/Twitter plugin for Xquik automation with read-first "
    "workflows and approval-gated actions. Not affiliated with X Corp."
)
EXPECTED_CODEX_PLUGIN_KEYWORDS = [*EXPECTED_AGENT_SKILL_MANIFEST_TAGS, "codex-plugin"]
EXPECTED_AGENT_SKILL_INSTALL = "hermes plugins install Xquik-dev/hermes-tweet --enable"
EXPECTED_TOPIC_DISCOVERY_KEYWORD = "agent-skill"
EXPECTED_DASHBOARD_MANIFEST_DESCRIPTION = (
    "Hermes Agent X/Twitter plugin for searching tweets, reading replies, "
    "monitoring X, exporting followers, and approval-gated posting through Xquik. "
    "Not affiliated with X Corp."
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
        "Claude Skill Registry Hermes Tweet skill",
        "https://github.com/majiayu000/claude-skill-registry/blob/main/skills/api/"
        "hermes-tweet/SKILL.md",
    ),
    (
        "Claude Skill Registry Data Hermes Tweet archive",
        "https://github.com/majiayu000/claude-skill-registry-data/blob/main/api/"
        "hermes-tweet/SKILL.md",
    ),
    (
        "Freya Hermes Tweet skill install example",
        "https://github.com/willtanoe/freya/blob/xtr/docs/user-guide/skills.md",
    ),
    (
        "Awesome Skill Forge Hermes Tweet mirror",
        "https://raw.githubusercontent.com/Lord1Egypt/awesome-skill-forge/master/community/"
        "clawhub/h/hermes-tweet/SKILL.md",
    ),
    (
        "RA-Skills Hermes Tweet mirror",
        "https://github.com/Lord1Egypt/RA-Skills/blob/master/skills/community/"
        "clawhub/h/hermes-tweet/SKILL.md",
    ),
)
SETUP_UV_ACTION = "astral-sh/setup-uv@11f9893b081a58869d3b5fccaea48c9e9e46f990"
CHECKOUT_ACTION_SHA = "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1"
SETUP_GO_ACTION_SHA = "actions/setup-go@b7ad1dad31e06c5925ef5d2fc7ad053ef454303e"
UPLOAD_ARTIFACT_ACTION_SHA = "actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a"
DOWNLOAD_ARTIFACT_ACTION_SHA = "actions/download-artifact@3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c"
PYPI_PUBLISH_ACTION_SHA = "pypa/gh-action-pypi-publish@cef221092ed1bacb1cc03d23a2d87d1d172e277b"
ATTEST_ACTION_SHA = "actions/attest@f7c74d28b9d84cb8768d0b8ca14a4bac6ef463e6"
CODEQL_ACTION_SHA = "github/codeql-action/{}@7188fc363630916deb702c7fdcf4e481b751f97a"
SCORECARD_ACTION_SHA = "ossf/scorecard-action@4eaacf0543bb3f2c246792bd56e8cdeffafb205a"
CLUSTERFUZZLITE_ACTION_SHA = (
    "google/clusterfuzzlite/actions/{}@884713a6c30a92e5e8544c39945cd7cb630abcd1"
)
HOL_PLUGIN_SCANNER_ACTION_SHA = (
    "hashgraph-online/ai-plugin-scanner-action@a63dd98b7d6497cabad2069e803b450def3b02dc"
)
ACTIONLINT_MODULE = "github.com/rhysd/actionlint/cmd/actionlint@v1.7.12"
BLACKSMITH_RUNNER_LABEL = "blacksmith-2vcpu-ubuntu-2404"
HERMES_AGENT_COMPAT_COMMAND = "uv run python scripts/check_hermes_agent_compat.py"
PUBLIC_SAFETY_COMMAND = "uv run python scripts/check_public_safety.py"
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


def find_step(steps: list[object], name: str) -> dict[str, object]:
    for step in steps:
        step_mapping = require_mapping(step)
        if step_mapping.get("name") == name:
            return step_mapping

    message = f"No workflow step named {name!r}."
    raise AssertionError(message)


def workflow_job(path: str, job: str) -> dict[str, object]:
    workflow = load_object_mapping(ROOT / ".github" / "workflows" / path)
    jobs = require_mapping(workflow["jobs"])
    return require_mapping(jobs[job])


def test_find_step_reports_missing_workflow_step() -> None:
    with pytest.raises(AssertionError, match=r"No workflow step named 'Publish'\."):
        find_step([], "Publish")


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
    assert "Do not treat a single capped GitHub CLI result as complete" in normalized_guide
    assert "hermes-tweet-open-prs-<timestamp>.json" in guide
    assert "hermes-tweet-pr-audit-<timestamp>.jsonl" in guide
    assert "author, head owner, base repository" in normalized_guide
    assert "unresolved review threads" in normalized_guide
    assert "verified `kriptoburak` branches" in guide
    assert "aggregate `UNKNOWN` mergeability" in guide
    assert "direct PR read" in guide
    assert "direct read reports `DIRTY` or `CONFLICTING`" in normalized_guide
    assert "prepared fork branch as outreach" in guide
    assert "record the API error" in guide
    assert "own-repo fallback PR" in guide


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


def test_docs_track_current_hermes_agent_surface_release() -> None:
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


def test_hermes_surface_guide_keeps_runtime_host_contract_visible() -> None:
    guide = (ROOT / "docs" / "HERMES_SURFACES.md").read_text()

    assert "remote Hermes host" in guide
    assert "host that executes plugin tools" in guide
    assert "HERMES_TWEET_ENABLE_ACTIONS=false" in guide
    assert "HERMES_TWEET_ENABLE_ACTIONS=true" in guide
    assert "hermes plugins install Xquik-dev/hermes-tweet --enable" in guide
    assert 'hermes -z "/xstatus"' in guide


def test_integration_patterns_classify_marketplace_bridges() -> None:
    guide = (ROOT / "docs" / "INTEGRATION_PATTERNS.md").read_text()

    assert "Claude marketplace bridges:" in guide
    assert "compatibility routes, not as catalog targets" in guide
    assert "`hermes plugins install Xquik-dev/hermes-tweet --enable`" in guide
    assert "`.claude-plugin/plugin.json` metadata" in guide
    assert "Codex marketplace bridges:" in guide
    assert "`.codex-plugin/plugin.json` metadata" in guide
    assert "HOL Plugin Scanner evidence" in guide


def test_submission_readiness_rejects_adjacent_duplicate_routes() -> None:
    checklist = (ROOT / "docs" / "SUBMISSION_READINESS.md").read_text()
    normalized_checklist = " ".join(checklist.split())

    assert "`TweetClaw`, `OpenClaw`" in checklist
    assert "`SocialClaw`, `x-twitter-scraper`, and Xquik-only proposals" in checklist
    assert "Treat adjacent-only PR history as a conflict signal" in checklist
    assert "separate native Hermes Tweet route" in checklist
    assert "awesome lists, plugin lists, and topic-search hits" in checklist
    assert "open adjacent X/social submission" in normalized_checklist
    assert "explicit Hermes Tweet or Hermes Agent plugin lane" in normalized_checklist
    assert "generic Claude plugin or agent-skill heading is not enough" in normalized_checklist
    assert "open authored PR in the target" in checklist
    assert "treat the target as saturated" in checklist
    assert "MCP-data-only" in checklist
    assert "Hermes Tweet conversion" in checklist
    assert "generic Xquik MCP server data entry" in checklist
    assert "explicitly incompatible with contribution" in checklist
    assert "license metadata or an absent root license" in checklist
    assert "an absent license alone does not disqualify" in checklist
    assert "product-owned marketplaces" in normalized_checklist
    assert "closed to random additions" in checklist
    assert "branded Claude plugin catalogs" in checklist
    assert "describe themselves as the official catalog" in normalized_checklist
    assert "one vendor, team, or product family" in normalized_checklist
    assert "plugin updates flow from that owner's source repositories" in normalized_checklist
    assert "compatibility example, not a third-party submission route" in normalized_checklist
    assert "explicitly accept outside source repositories" in normalized_checklist
    assert "root license files such as `LICENSE`, `LICENSE.md`" in checklist
    assert "read it before deciding" in checklist
    assert "claim form, upload UI, or account-gated directory" in checklist
    assert "source, catalog, or registry file that can be changed by PR" in checklist
    assert "generated catalog, marketplace" in checklist
    assert "source-registry manifest, or installable catalog manifest files" in normalized_checklist
    assert "canonical edit surface" in normalized_checklist
    assert "documented source file or generator input" in checklist
    assert "source cannot carry a target-native Hermes Tweet entry" in checklist
    assert "topic-search hits that are only source repositories" in checklist
    assert "standalone skills/plugins" in normalized_checklist
    assert "framework examples" in normalized_checklist
    assert "product implementations" in normalized_checklist
    assert "third-party catalog, registry, marketplace, or showcase file" in normalized_checklist
    assert "Topic metadata such as `agent-skills`" in checklist
    assert "discovery evidence only" in normalized_checklist
    assert "Xquik toolkit" in checklist
    assert "xquik-twitter-data" in checklist
    assert "target-native Hermes Tweet entry" in checklist
    assert "`source-packets`" in checklist
    assert "`evidence-packets`" in checklist
    assert "title and summary to name `Hermes Tweet` or" in checklist
    assert "Do not submit or refresh routes titled only for `Xquik`" in checklist
    assert "`TweetClaw`, `OpenClaw`, or other adjacent projects" in checklist


def test_submission_readiness_blocks_disabled_pr_routes() -> None:
    checklist = (ROOT / "docs" / "SUBMISSION_READINESS.md").read_text()
    normalized_checklist = " ".join(checklist.split())

    assert "Before preparing a patch" in normalized_checklist
    assert "pull-request surface is enabled" in normalized_checklist
    assert "accepts external fork heads" in normalized_checklist
    assert "repository's pull-request endpoint" in normalized_checklist
    assert "fork creation and branch push succeed" in normalized_checklist
    assert "continue with another eligible target" in normalized_checklist


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
    bundled_text = bundled_skill.read_text()
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    version = pyproject["project"]["version"]

    assert registry_skill.read_text().rstrip() == bundled_text.rstrip()
    assert "## Permissions and Capabilities" in bundled_text
    assert "## Known Risks and Mitigations" in bundled_text
    assert "## Output" in bundled_text
    assert "## Error Handling" in bundled_text
    assert "## Resources" in bundled_text
    assert "## Release Trust Gate" in bundled_text
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
    assert "## Tool Matrix" in reference_text
    assert "## Approval Checklist" in reference_text
    assert "HERMES_TWEET_ENABLE_ACTIONS=true" in reference_text

    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    package_data = pyproject["tool"]["setuptools"]["package-data"]["hermes_tweet"]
    assert "skills/hermes-tweet/references/*.md" in package_data


def test_skill_card_mirrors_bundled_skill_card() -> None:
    registry_card = ROOT / "skills" / "hermes-tweet" / "skill-card.md"
    bundled_card = ROOT / "hermes_tweet" / "skills" / "hermes-tweet" / "skill-card.md"
    card_text = bundled_card.read_text()
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    version = pyproject["project"]["version"]

    assert registry_card.read_text().rstrip() == card_text.rstrip()
    assert f"- Version: {version}" in card_text
    assert "Status: public self-assessment. Not NVIDIA-verified." in card_text
    assert "## Owner" in card_text
    assert "## Use Case" in card_text
    assert "## Inputs and Configuration" in card_text
    assert "## Capabilities" in card_text
    assert "## Outputs" in card_text
    assert "## Side Effects" in card_text
    assert "## Known Risks and Mitigations" in card_text
    assert "## Release Trust Gate" in card_text
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
        "Search Twitter/X, read tweet replies, look up users, monitor tweets, "
        "export followers, and gate X actions through Xquik. Not affiliated with X Corp."
    )
    assert frontmatter["tags"] == EXPECTED_SKILL_TAGS
    assert_skill_capabilities(frontmatter)

    ask_metadata = require_mapping(frontmatter["metadata"])
    assert ask_metadata == EXPECTED_ASK_SKILL_METADATA | {"version": version}
    assert "## Permissions and Trust" in ask_text
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
        "Hermes Agent X/Twitter plugin for Xquik automation. Not affiliated with X Corp."
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


def test_hol_plugin_scanner_workflow_matches_codex_catalog_requirements() -> None:
    workflow = load_object_mapping(ROOT / ".github" / "workflows" / "hol-plugin-scanner.yml")

    on_config = require_mapping(workflow[True])
    assert "pull_request" in on_config
    assert require_mapping(on_config["push"])["branches"] == ["master", "main"]
    assert on_config["workflow_dispatch"] is None
    assert require_mapping(workflow["permissions"]) == {"contents": "read"}

    jobs = require_mapping(workflow["jobs"])
    scan = require_mapping(jobs["scan"])
    assert require_mapping(scan["permissions"]) == {
        "contents": "read",
        "security-events": "write",
    }
    assert scan["runs-on"] == BLACKSMITH_RUNNER_LABEL
    steps = require_list(scan["steps"])
    checkout = find_step(steps, "Checkout")
    assert checkout["uses"] == CHECKOUT_ACTION_SHA
    assert require_mapping(checkout["with"])["persist-credentials"] is False

    scanner = find_step(steps, "HOL Plugin Scanner")
    assert scanner["uses"] == HOL_PLUGIN_SCANNER_ACTION_SHA
    assert require_mapping(scanner["with"]) == {
        "plugin_dir": ".",
        "mode": "scan",
        "min_score": 80,
        "fail_on_severity": "high",
        "format": "sarif",
        "upload_sarif": True,
    }


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


@pytest.mark.parametrize(
    ("workflow_path", "job_name"),
    [("ci.yml", "check"), ("hol-plugin-scanner.yml", "scan")],
)
def test_validation_workflows_run_on_blacksmith_runner(
    workflow_path: str,
    job_name: str,
) -> None:
    assert workflow_job(workflow_path, job_name)["runs-on"] == BLACKSMITH_RUNNER_LABEL


@pytest.mark.parametrize("job_name", ["build", "publish"])
def test_publish_workflow_runs_on_github_hosted_runner(job_name: str) -> None:
    assert workflow_job("publish.yml", job_name)["runs-on"] == "ubuntu-24.04"


def test_actionlint_allows_blacksmith_runner_label() -> None:
    config = load_object_mapping(ROOT / ".github" / "actionlint.yaml")
    self_hosted_runner = require_mapping(config["self-hosted-runner"])

    assert self_hosted_runner["labels"] == [BLACKSMITH_RUNNER_LABEL]


def test_all_workflow_actions_are_pinned_to_commit_shas() -> None:
    action_reference = re.compile(r"[^@\s]+@[0-9a-f]{40}")

    for workflow_path in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
        action_lines = [
            line.strip()
            for line in workflow_path.read_text().splitlines()
            if line.strip().startswith("uses:")
        ]
        assert action_lines
        for action_line in action_lines:
            action = action_line.removeprefix("uses:").partition("#")[0].strip()
            assert action_reference.fullmatch(action), (
                f"Unpinned action in {workflow_path}: {action}"
            )


def test_codeql_workflow_analyzes_python_with_restricted_permissions() -> None:
    workflow = load_object_mapping(ROOT / ".github" / "workflows" / "codeql.yml")
    analyze = require_mapping(require_mapping(workflow["jobs"])["analyze"])

    assert require_mapping(workflow[True])["push"] == {"branches": ["master"]}
    assert require_mapping(analyze["permissions"]) == {
        "contents": "read",
        "security-events": "write",
    }
    steps = require_list(analyze["steps"])
    assert find_step(steps, "Check out source")["uses"] == CHECKOUT_ACTION_SHA
    initialize = find_step(steps, "Initialize CodeQL")
    assert initialize["uses"] == CODEQL_ACTION_SHA.format("init")
    assert require_mapping(initialize["with"]) == {
        "languages": "python",
        "build-mode": "none",
        "queries": "security-extended",
    }
    assert find_step(steps, "Analyze")["uses"] == CODEQL_ACTION_SHA.format("analyze")


def test_scorecard_workflow_publishes_results_with_restricted_permissions() -> None:
    workflow = load_object_mapping(ROOT / ".github" / "workflows" / "scorecard.yml")
    analysis = require_mapping(require_mapping(workflow["jobs"])["analysis"])

    assert workflow["permissions"] == "read-all"
    assert require_mapping(analysis["permissions"]) == {
        "contents": "read",
        "security-events": "write",
        "id-token": "write",
    }
    steps = require_list(analysis["steps"])
    assert find_step(steps, "Check out source")["uses"] == CHECKOUT_ACTION_SHA
    scorecard = find_step(steps, "Run analysis")
    assert scorecard["uses"] == SCORECARD_ACTION_SHA
    assert require_mapping(scorecard["with"])["publish_results"] is True
    upload = find_step(steps, "Upload to code scanning")
    assert upload["uses"] == CODEQL_ACTION_SHA.format("upload-sarif")


def test_clusterfuzzlite_runs_python_fuzzers_with_restricted_permissions() -> None:
    workflow = load_object_mapping(ROOT / ".github" / "workflows" / "clusterfuzzlite.yml")
    on_config = require_mapping(workflow[True])

    assert "pull_request" in on_config
    assert "schedule" in on_config
    assert "workflow_dispatch" in on_config
    assert workflow["permissions"] == "read-all"

    fuzz = require_mapping(require_mapping(workflow["jobs"])["fuzz"])
    assert fuzz["runs-on"] == "ubuntu-24.04"
    assert fuzz["timeout-minutes"] == 30
    steps = require_list(fuzz["steps"])

    build = find_step(steps, "Build fuzzers")
    assert build["uses"] == CLUSTERFUZZLITE_ACTION_SHA.format("build_fuzzers")
    assert require_mapping(build["with"]) == {
        "language": "python",
        "github-token": "${{ github.token }}",
        "sanitizer": "address",
    }

    run = find_step(steps, "Run fuzzers")
    assert run["uses"] == CLUSTERFUZZLITE_ACTION_SHA.format("run_fuzzers")
    assert require_mapping(run["with"]) == {
        "language": "python",
        "github-token": "${{ github.token }}",
        "sanitizer": "address",
        "fuzz-seconds": "${{ github.event_name == 'pull_request' && '60' || '600' }}",
        "mode": "${{ github.event_name == 'pull_request' && 'code-change' || 'batch' }}",
        "output-sarif": False,
    }

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


def test_publish_workflow_requires_version_matched_release_tag() -> None:
    workflow = load_object_mapping(ROOT / ".github" / "workflows" / "publish.yml")

    # PyYAML 1.1 treats the GitHub Actions "on" key as boolean true.
    on_config = require_mapping(workflow[True])
    release = require_mapping(on_config["release"])
    assert release["types"] == ["published"]
    assert "workflow_dispatch" not in on_config

    jobs = require_mapping(workflow["jobs"])
    build = require_mapping(jobs["build"])
    assert build["timeout-minutes"] == 30
    build_steps = require_list(build["steps"])

    install_uv_step = find_step(build_steps, "Install uv")
    assert install_uv_step["uses"] == SETUP_UV_ACTION
    assert require_mapping(install_uv_step["with"])["enable-cache"] is False

    public_safety_step = find_step(build_steps, "Public safety scan")
    assert public_safety_step["run"] == PUBLIC_SAFETY_COMMAND

    checkout_step = find_step(build_steps, "Checkout")
    assert checkout_step["uses"] == CHECKOUT_ACTION_SHA
    checkout_config = require_mapping(checkout_step["with"])
    assert checkout_config == {
        "fetch-depth": 0,
        "persist-credentials": False,
        "ref": "${{ github.event.release.tag_name }}",
    }

    validate_step = find_step(build_steps, "Validate release tag")
    validate_env = require_mapping(validate_step["env"])
    assert validate_env["RELEASE_TAG"] == "${{ github.event.release.tag_name }}"

    validate_script = validate_step["run"]
    assert isinstance(validate_script, str)
    assert "pyproject.toml" in validate_script
    assert 'expected_ref = f"v{version}"' in validate_script
    assert 'actual_ref = os.environ["RELEASE_TAG"]' in validate_script
    assert "pyproject version tag" in validate_script
    assert "refs/tags/${RELEASE_TAG}^{commit}" in validate_script
    assert "refs/remotes/origin/master" in validate_script
    assert "protected master tip" in validate_script

    assert find_step(build_steps, "Set up Go")["uses"] == SETUP_GO_ACTION_SHA
    assert find_step(build_steps, "Workflow lint")["run"] == f"go run {ACTIONLINT_MODULE}"
    assert find_step(build_steps, "Public link scan")["run"] == (
        "uv run python scripts/check_public_links.py"
    )
    assert find_step(build_steps, "Hermes Agent compatibility")["run"] == (
        HERMES_AGENT_COMPAT_COMMAND
    )
    assert find_step(build_steps, "Upload distributions")["uses"] == (UPLOAD_ARTIFACT_ACTION_SHA)

    publish = require_mapping(jobs["publish"])
    assert publish["timeout-minutes"] == 10
    publish_permissions = require_mapping(publish["permissions"])
    assert publish_permissions == {"contents": "read", "id-token": "write"}
    publish_steps = require_list(publish["steps"])
    assert find_step(publish_steps, "Download distributions")["uses"] == (
        DOWNLOAD_ARTIFACT_ACTION_SHA
    )
    publish_step = find_step(publish_steps, "Publish distributions")
    assert publish_step["uses"] == PYPI_PUBLISH_ACTION_SHA
    assert require_mapping(publish_step["with"]) == {
        "attestations": True,
        "packages-dir": "dist/",
    }


def test_publish_workflow_attests_and_attaches_release_artifacts() -> None:
    build = workflow_job("publish.yml", "build")
    assert require_mapping(build["permissions"]) == {
        "attestations": "write",
        "contents": "write",
        "id-token": "write",
    }
    build_steps = require_list(build["steps"])

    attest_step = find_step(build_steps, "Attest distributions")
    assert attest_step["uses"] == ATTEST_ACTION_SHA
    assert require_mapping(attest_step["with"])["subject-path"] == ("dist/*.whl\ndist/*.tar.gz\n")

    attach_step = find_step(build_steps, "Attach release provenance")
    assert require_mapping(attach_step["env"]) == {
        "ATTESTATION_BUNDLE": "${{ steps.attest.outputs.bundle-path }}",
        "GH_TOKEN": "${{ github.token }}",
        "RELEASE_TAG": "${{ github.event.release.tag_name }}",
    }
    attach_script = attach_step["run"]
    assert isinstance(attach_script, str)
    assert "provenance.intoto.jsonl" in attach_script
    assert "gh release upload" in attach_script

    upload_step = find_step(build_steps, "Upload distributions")
    assert upload_step["uses"] == UPLOAD_ARTIFACT_ACTION_SHA
    assert require_mapping(upload_step["with"])["path"] == ("dist/*.whl\ndist/*.tar.gz\n")


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
    assert step_names.index("Hermes Agent compatibility") < step_names.index("Test with coverage")
    assert step_names.index("Public safety scan") < step_names.index("Test with coverage")

    setup_go_step = find_step(steps, "Set up Go")
    assert setup_go_step["uses"] == SETUP_GO_ACTION_SHA
    setup_go_config = require_mapping(setup_go_step["with"])
    assert setup_go_config["go-version"] == "stable"
    assert setup_go_config["cache"] is False

    workflow_lint_step = find_step(steps, "Workflow lint")
    assert workflow_lint_step["run"] == f"go run {ACTIONLINT_MODULE}"

    install_uv_step = find_step(steps, "Install uv")
    assert install_uv_step["uses"] == SETUP_UV_ACTION

    checkout_step = find_step(steps, "Checkout")
    assert checkout_step["uses"] == CHECKOUT_ACTION_SHA
    assert require_mapping(checkout_step["with"])["persist-credentials"] is False

    hermes_agent_compat_step = find_step(steps, "Hermes Agent compatibility")
    assert hermes_agent_compat_step["run"] == HERMES_AGENT_COMPAT_COMMAND
    assert require_mapping(hermes_agent_compat_step["env"]) == {
        "GITHUB_TOKEN": "${{ github.token }}"
    }

    public_safety_step = find_step(steps, "Public safety scan")
    assert public_safety_step["run"] == PUBLIC_SAFETY_COMMAND


def test_release_gate_runs_hermes_agent_compatibility_checker() -> None:
    checklist = (ROOT / "docs" / "PUBLICATION_CHECKLIST.md").read_text()
    agents = (ROOT / "AGENTS.md").read_text()

    assert (
        "uv run --python 3.12 --group dev python scripts/check_hermes_agent_compat.py" in checklist
    )
    assert "uv run --python 3.12 --group dev python scripts/check_public_safety.py" in checklist
    assert "source SHA changes" in checklist
    assert "uv run --python 3.12 --group dev python scripts/check_hermes_agent_compat.py" in agents
    assert "uv run --python 3.12 --group dev python scripts/check_public_safety.py" in agents
