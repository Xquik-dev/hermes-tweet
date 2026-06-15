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
EXPECTED_CLAUDE_PLUGIN_DESCRIPTION = (
    "Native Hermes Agent X/Twitter plugin for Xquik automation with read-first "
    "workflows and approval-gated actions."
)
EXPECTED_CODEX_PLUGIN_KEYWORDS = [*EXPECTED_AGENT_SKILL_MANIFEST_TAGS, "codex-plugin"]
EXPECTED_AGENT_SKILL_INSTALL = "hermes plugins install Xquik-dev/hermes-tweet --enable"
EXPECTED_DASHBOARD_MANIFEST_DESCRIPTION = (
    "Hermes Agent X/Twitter plugin for searching tweets, reading replies, "
    "monitoring X, exporting followers, and approval-gated posting through Xquik."
)
EXPECTED_HERMES_ECO_MANIFEST_NAME = "Hermes Tweet"
EXPECTED_HERMES_ECO_MANIFEST_TYPE = "integration"
EXPECTED_HERMES_ECO_MANIFEST_CATEGORY = "communication"
EXPECTED_SURFACE_GUIDE_LINK = "[`docs/HERMES_SURFACES.md`](docs/HERMES_SURFACES.md)"
EXPECTED_INTEGRATION_PATTERNS_LINK = (
    "[`docs/INTEGRATION_PATTERNS.md`](docs/INTEGRATION_PATTERNS.md)"
)
SUBMISSION_READINESS_PATH = "docs/SUBMISSION_READINESS.md"
EXPECTED_SUBMISSION_READINESS_LINK = f"[`{SUBMISSION_READINESS_PATH}`]({SUBMISSION_READINESS_PATH})"
EXPECTED_SUBMISSION_READINESS_SURFACES = (
    ROOT / "docs" / "PUBLICATION_CHECKLIST.md",
    ROOT / "docs" / "HERMES_SURFACES.md",
    ROOT / "docs" / "INTEGRATION_PATTERNS.md",
    ROOT / "docs" / "ECOSYSTEM.md",
    ROOT / "docs" / "GITHUB_METADATA.md",
)
EXPECTED_LIVE_ECOSYSTEM_SURFACES = (
    (
        "CorpusIQ Hermes skills marketplace X/Twitter skill",
        "https://github.com/CorpusIQ/corpusiq-docs/blob/main/hermes/skills/"
        "marketplace/new-june14-2026/index.md",
    ),
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
        "https://github.com/Lord1Egypt/awesome-skill-forge/blob/master/community/"
        "clawhub/h/hermes-tweet/SKILL.md",
    ),
    (
        "RA-Skills Hermes Tweet mirror",
        "https://github.com/Lord1Egypt/RA-Skills/blob/master/skills/community/"
        "clawhub/h/hermes-tweet/SKILL.md",
    ),
)
SETUP_UV_ACTION = "astral-sh/setup-uv@v8.2.0"
CHECKOUT_ACTION_SHA = "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10"
HOL_PLUGIN_SCANNER_ACTION_SHA = (
    "hashgraph-online/ai-plugin-scanner-action@049f135bbda5f993c3564ce2b97d72ff595c7a1e"
)
ACTIONLINT_MODULE = "github.com/rhysd/actionlint/cmd/actionlint@v1.7.12"
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

    readme = (ROOT / "README.md").read_text()
    assert f"/releases/tag/v{version}" in readme
    assert EXPECTED_PUBLIC_PACKAGE_DESCRIPTION in readme
    assert EXPECTED_SURFACE_GUIDE_LINK in readme
    assert EXPECTED_INTEGRATION_PATTERNS_LINK in readme
    assert EXPECTED_SUBMISSION_READINESS_LINK in readme
    for surface in EXPECTED_SUBMISSION_READINESS_SURFACES:
        assert SUBMISSION_READINESS_PATH in surface.read_text(encoding="utf-8")

    urls = pyproject["project"]["urls"]
    assert urls["Homepage"] == GUIDE_URL
    assert urls["Documentation"] == GUIDE_URL
    assert urls["Repository"] == "https://github.com/Xquik-dev/hermes-tweet"
    assert urls["Issues"] == "https://github.com/Xquik-dev/hermes-tweet/issues"


def test_ecosystem_tracks_validated_live_surfaces() -> None:
    ecosystem = (ROOT / "docs" / "ECOSYSTEM.md").read_text()

    for label, url in EXPECTED_LIVE_ECOSYSTEM_SURFACES:
        assert f"| {label} | <{url}> |" in ecosystem


def test_uv_lock_tracks_dev_dependency_constraints() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    lockfile = tomllib.loads((ROOT / "uv.lock").read_text())

    expected = dict(
        normalize_requirement(requirement)
        for requirement in pyproject["project"]["optional-dependencies"]["dev"]
    )
    packages = require_list(lockfile["package"])
    package = find_locked_package(packages, "hermes-tweet")
    requires_dist = require_list(require_mapping(package["metadata"])["requires-dist"])
    locked: dict[str, dict[str, object]] = {}
    for requirement in requires_dist:
        requirement_data = require_mapping(requirement)
        if requirement_data.get("marker") == "extra == 'dev'":
            name, metadata = normalize_locked_requirement(requirement_data)
            locked[name] = metadata

    assert locked == expected


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
    assert "without a detectable contribution license" in checklist
    assert "maintainer has already asked" in checklist
    assert "product-owned marketplaces" in checklist
    assert "closed to random additions" in checklist
    assert "branded Claude plugin catalogs" in checklist
    assert "describe themselves as the official catalog" in normalized_checklist
    assert "one vendor, team, or product family" in normalized_checklist
    assert "plugin updates flow from that owner's source repositories" in normalized_checklist
    assert "compatibility example, not a third-party submission route" in normalized_checklist
    assert "explicitly accept outside source repositories" in normalized_checklist
    assert "root license files such as `LICENSE`, `LICENSE.md`" in checklist
    assert "read it before rejecting" in checklist
    assert "claim form, upload UI, or account-gated directory" in checklist
    assert "source, catalog, or registry file that can be changed by PR" in checklist
    assert "generated catalog or marketplace files" in checklist
    assert "canonical edit surface" in checklist
    assert "documented source file or generator input" in checklist
    assert "source cannot carry a target-native Hermes Tweet entry" in checklist
    assert "topic-search hits that are only source repositories" in checklist
    assert "standalone skills/plugins" in normalized_checklist
    assert "framework examples" in normalized_checklist
    assert "product implementations" in normalized_checklist
    assert "third-party catalog, registry, marketplace, or showcase file" in normalized_checklist
    assert "Topic metadata such as `agent-skills`" in checklist
    assert "discovery evidence only" in normalized_checklist
    assert "editable third-party entry surface" in normalized_checklist
    for phrase in (
        "framework-specific plugin marketplaces, IDE agent extension marketplaces",
        "single-app tool collections, offline marketplace mirrors",
        "Dify, LangGraph, LlamaIndex, AutoGen, OpenAI Agents SDK",
        "Cline, Roo Code, Cursor, Windsurf",
        "Open WebUI, LibreChat, AnythingLLM, BeeAI, Rivet",
        "Langroid, AutoGPT Forge, OpenAgents, Agent Zero, SuperAGI, BabyAGI",
        "Smolagents, DSPy, Julep, MetaGPT, Qwen-Agent, PraisonAI, Swarms",
        "Letta, MemGPT, Griptape, Mirascope, Marvin AI, Agency Swarm, Phidata, Motia",
        "Hermes Tweet's shipped package format",
        "tool subclass, module, framework tool",
        "hosted agent builder, assistant builder, toolgroup, and action-group",
        "Chainlit, Microsoft PromptFlow, Llama Stack, CopilotKit, Rasa",
        "CALM, or AWS Bedrock Agents",
        "app-native tools",
        "declarative action groups",
        "prompt-flow components",
        "runtime-specific tool definitions",
        "integration targets, not Hermes Tweet outreach routes",
        "licensed PR-editable catalog entry",
        "Hermes Tweet's shipped source repository package",
        "enterprise hosted-agent surfaces",
        "Google Vertex AI Agent Builder",
        "Salesforce Agentforce",
        "ServiceNow AI Agent Studio",
        "Oracle AI Agent Studio",
        "Slack agent platform tools",
        "Mistral agent connectors",
        "platform-native extensions",
        "managed-agent definitions",
        "code-assistant extension marketplaces",
        "developer-agent tool catalogs",
        "Amazon Q Developer, Continue, Sourcegraph Cody",
        "JetBrains Junie, Devin",
        "IDE extensions, editor plugins",
        "workspace automation packs",
        "assistant-specific tool definitions",
        "PR-editable Hermes Tweet source package entry",
        "local coding-agent command packs",
        "workflow recipes, and rule bundles",
        "GitHub Copilot Extensions, OpenCode commands",
        "Aider workflows, Goose",
        "Kiro hooks, or Amp tools",
        "agent-local prompts",
        "commands, recipes, hooks, or editor workflows",
        "source-linked Hermes Tweet package entry",
        "hosted automation, app-action, and component galleries",
        "Zapier, Pipedream, Activepieces, Composio, Arcade, Toolhouse, or Langflow",
        "workflow templates, provider connectors, hosted app actions",
        "PR-editable third-party source repository entry",
        "embedded `.agents`, `.agent`, `.antigravity`",
        "project-template",
        "copied skill directories inside application repositories",
        "downstream copies or mirrors",
        "fresh Hermes Tweet submission routes",
        "personal agent memory repositories",
        "OpenHands microagent folders",
        "hosted MCP directory profile pages",
        "`.openhands`, Smithery, Glama, or PulseMCP",
        "licensed, PR-editable source entry",
        "contribution rules require measurable community usage",
        "minimum star count",
        "maintainer-curated quality bar",
        "target's stated threshold",
        "closed prior Hermes Tweet PR",
        "target-specific blocker",
        "resubmit with the same evidence",
        "write Markdown bodies through a reviewed file",
        "non-interpolating path",
        "repository names, backticked literals, and validation commands",
        "`source.github` or similar repository-pointer schema",
        "canonical hub for the owner's own skills",
        "prototype marketplace applications",
        "README documents only API calls",
        "`curl` publish example is not a PR-native submission route",
        "company engineering hubs",
        "internal workflow marketplaces",
        "single-namespace catalogs",
        "Open standards, Agent Skills compatibility",
        "`third-party`, `vendor`, `upstream`, or `external` directory name",
        "branded as one owner's official catalog",
        "explicitly accept unrelated external source repositories",
        "distro installers, runtime stacks, or bundle repos",
        "external plugin reference list",
        "vendor Hermes Tweet code into another installer",
        "runtime bridges or installer extensions",
        "only help another agent consume Claude plugin marketplaces",
        "compatibility surfaces",
        "editable catalog entry for third-party plugins or source repositories",
        "translated or mirrored awesome lists",
        "translation issue tracker",
        "independent localized submission",
        "accepted adjacent entries as saturation",
        "a live Xquik, TweetClaw, OpenClaw, SocialClaw, or x-twitter-scraper entry",
        "same catalog, tool list, or awesome-list section",
        "distinct Hermes Agent plugin lane",
        "closed prior Hermes Tweet issue",
        "completed or rejected submission route",
        "unless a maintainer asks for a new PR",
        "public GitHub code search for live `Hermes Tweet`, `hermes-tweet`",
        "accepted default-branch listing",
        "record it in `docs/ECOSYSTEM.md`",
        "opening a duplicate submission",
        "local `<plugin>/.claude-plugin/plugin.json` inside the target repository",
        "external source-repository entry for third-party plugins",
        "copy, vendor, or repackage Hermes Tweet",
        "local target plugin folder",
        "official-directory snapshot lists",
        "plugins already published in an upstream official catalog",
        "status mirrors",
        "already listed in that upstream catalog",
        "Before waiting on checks, reread the outbound title, summary, and added lines",
        "close it immediately with a short scope comment",
        "off-scope outreach open",
    ):
        assert phrase in normalized_checklist
    assert "Xquik toolkit" in checklist
    assert "xquik-twitter-data" in checklist
    assert "target-native Hermes Tweet entry" in checklist
    assert "`source-packets`" in checklist
    assert "`evidence-packets`" in checklist
    assert "title and summary to name `Hermes Tweet` or" in checklist
    assert "Do not submit or refresh routes titled only for `Xquik`" in checklist
    assert "`TweetClaw`, `OpenClaw`, or other adjacent projects" in checklist


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

    manifest_lines = (ROOT / "MANIFEST.in").read_text().splitlines()
    assert "include .codex-plugin/plugin.json" in manifest_lines
    assert "include SECURITY.md" in manifest_lines
    assert "include assets/icon.svg" in manifest_lines


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
    assert require_mapping(workflow["permissions"]) == {
        "contents": "read",
        "security-events": "write",
    }

    jobs = require_mapping(workflow["jobs"])
    scan = require_mapping(jobs["scan"])
    assert scan["runs-on"] == "ubuntu-latest"
    steps = require_list(scan["steps"])
    assert find_step(steps, "Checkout")["uses"] == CHECKOUT_ACTION_SHA

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

    public_safety_step = find_step(build_steps, "Public safety scan")
    assert public_safety_step["run"] == PUBLIC_SAFETY_COMMAND

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
    assert step_names.index("Hermes Agent compatibility") < step_names.index("Test with coverage")
    assert step_names.index("Public safety scan") < step_names.index("Test with coverage")

    setup_go_step = find_step(steps, "Set up Go")
    assert setup_go_step["uses"] == "actions/setup-go@v6"
    setup_go_config = require_mapping(setup_go_step["with"])
    assert setup_go_config["go-version"] == "stable"
    assert setup_go_config["cache"] is False

    workflow_lint_step = find_step(steps, "Workflow lint")
    assert workflow_lint_step["run"] == f"go run {ACTIONLINT_MODULE}"

    install_uv_step = find_step(steps, "Install uv")
    assert install_uv_step["uses"] == SETUP_UV_ACTION

    hermes_agent_compat_step = find_step(steps, "Hermes Agent compatibility")
    assert hermes_agent_compat_step["run"] == HERMES_AGENT_COMPAT_COMMAND

    public_safety_step = find_step(steps, "Public safety scan")
    assert public_safety_step["run"] == PUBLIC_SAFETY_COMMAND


def test_release_gate_runs_hermes_agent_compatibility_checker() -> None:
    checklist = (ROOT / "docs" / "PUBLICATION_CHECKLIST.md").read_text()
    agents = (ROOT / "AGENTS.md").read_text()

    assert (
        "uv run --python 3.12 --extra dev python scripts/check_hermes_agent_compat.py" in checklist
    )
    assert "uv run --python 3.12 --extra dev python scripts/check_public_safety.py" in checklist
    assert "source SHA changes" in checklist
    assert "uv run --python 3.12 --extra dev python scripts/check_hermes_agent_compat.py" in agents
    assert "uv run --python 3.12 --extra dev python scripts/check_public_safety.py" in agents
