# Submission Readiness

Use this checklist before proposing Hermes Tweet to a skill, plugin, MCP,
catalog, awesome list, or target project. It keeps submissions native,
maintainer-friendly, and easy to merge.

## Fit

Submit Hermes Tweet only when the target has a native route for at least one of
these surfaces:

- Hermes Agent plugins or Hermes skills
- X/Twitter, tweet, social listening, monitoring, digest, or publishing tools
- MCP servers that document optional Hermes Agent backends
- OpenClaw or ClawHub skills that accept complementary backend guidance
- Claude Code plugin catalogs that accept source repositories with
  `.claude-plugin` metadata
- Codex plugin catalogs that accept source repositories with `.codex-plugin`
  metadata, a root security policy, local icon, and scanner evidence
- Skill registries, plugin catalogs, awesome lists, or ecosystem directories

Do not submit when the target is only a browser-cookie workflow, only a
TweetClaw route, a generic Xquik MCP server data entry, unrelated to X/Twitter
or Hermes Agent, archived, or not licensed for contribution. Reject targets
without a detectable contribution license unless a maintainer has already asked
for a Hermes Tweet update on an existing route. Reject personal or
product-owned marketplaces that describe themselves as owner-specific,
team-specific, or closed to random additions unless their docs clearly invite
third-party Hermes Tweet submissions.
Reject branded Claude plugin catalogs that describe themselves as the official
catalog for one vendor, team, or product family. If the catalog says plugin
updates flow from that owner's source repositories, treat it as a compatibility
example, not a third-party submission route, unless the docs explicitly accept
outside source repositories.
A `source.github` or similar repository-pointer schema is not enough by itself:
when the marketplace instructions say it is the canonical hub for the owner's
own skills, reject it unless the contribution docs explicitly invite outside
source repositories.
Reject company engineering hubs, internal workflow marketplaces, and
single-namespace catalogs whose install commands or plugin metadata are scoped
to one organization, team, or owner. Open standards, Agent Skills compatibility,
or Claude marketplace metadata do not make those routes eligible unless the
target explicitly invites third-party source repositories.
Do not treat a `third-party`, `vendor`, `upstream`, or `external` directory name
as an invitation by itself. If the marketplace is branded as one owner's
official catalog, require contribution docs that explicitly accept unrelated
external source repositories before submitting Hermes Tweet.
Treat the contribution license as detectable only after checking both GitHub
metadata and obvious root license files such as `LICENSE`, `LICENSE.md`,
`COPYING`, or `NOTICE`. When metadata is empty but a root license file exists,
read it before rejecting; accept only clear OSI-style permission text.
Reject crawler or indexer directories whose submission path is only a hosted
claim form, upload UI, or account-gated directory unless the repository exposes
a seed, source, catalog, or registry file that can be changed by PR.
Reject prototype marketplace applications whose README documents only API
calls, local server setup, or monetized publish flows without a committed
registry seed, catalog file, or source entry. A `curl` publish example is not a
PR-native submission route.
Reject distro installers, runtime stacks, or bundle repos that only vendor or
symlink local skills/plugins unless they expose a documented external plugin
reference list, package source field, or third-party catalog entry. Do not
vendor Hermes Tweet code into another installer just to create a listing.
Reject runtime bridges or installer extensions that only help another agent
consume Claude plugin marketplaces. Treat them as compatibility surfaces unless
they expose an editable catalog entry for third-party plugins or source
repositories.
Reject generated catalog or marketplace files unless target docs identify them
as the canonical edit surface. When a target builds indexes from another source,
submit only through the documented source file or generator input; skip the
route when that source cannot carry a target-native Hermes Tweet entry.
Reject marketplace contribution workflows that require creating a local
`<plugin>/.claude-plugin/plugin.json` inside the target repository unless they
also document an external source-repository entry for third-party plugins. Do
not copy, vendor, or repackage Hermes Tweet into a local target plugin folder to
satisfy a registry generator.
Reject official-directory snapshot lists whose contribution rules only accept
plugins already published in an upstream official catalog. Treat them as status
mirrors until Hermes Tweet is already listed in that upstream catalog, then
record the live surface instead of opening a speculative PR.
Reject topic-search hits that are only source repositories, standalone
skills/plugins, framework examples, or product implementations unless the target
exposes a documented third-party catalog, registry, marketplace, or showcase
file intended for external additions. Topic metadata such as `agent-skills`,
`claude-code-plugin`, `mcp-server`, or `awesome-list` is discovery evidence
only; it is not a native submission route without an editable third-party entry
surface.
Reject framework-specific plugin marketplaces, IDE agent extension marketplaces,
single-app tool collections, offline marketplace mirrors, or SDK tool packages
such as Dify, LangGraph, LlamaIndex, AutoGen, OpenAI Agents SDK, Cline, Roo
Code, Cursor, Windsurf, Open WebUI, LibreChat, AnythingLLM, BeeAI, Rivet, or
Langroid, AutoGPT Forge, OpenAgents, Agent Zero, SuperAGI, BabyAGI, or
Smolagents, DSPy, Julep, MetaGPT, Qwen-Agent, PraisonAI, Swarms, or
Letta, MemGPT, Griptape, Mirascope, Marvin AI, Agency Swarm, Phidata, Motia, or
product-specific tool adapters unless the target accepts external source
repositories in Hermes Tweet's shipped package format. Do not translate Hermes
Tweet into another runtime package, tool subclass, module, framework tool,
block, extension, or function pack just to satisfy a framework marketplace.
Reject agent-framework runtime toolkits and tool galleries such as AutoGen,
CrewAI, LangGraph, Mastra, Letta, and Semantic Kernel when they require a
runtime-specific tool implementation, adapter class, graph node, agent action,
or plugin function instead of a source-linked Hermes Tweet package entry.
Reject hosted agent builder, assistant builder, toolgroup, and action-group
catalogs such as Chainlit, Microsoft PromptFlow, Llama Stack, CopilotKit, Rasa
CALM, or AWS Bedrock Agents when the route only accepts app-native tools,
workflow nodes, declarative action groups, prompt-flow components, or
runtime-specific tool definitions. Treat these as integration targets, not
Hermes Tweet outreach routes, unless the target exposes a licensed PR-editable
catalog entry that links to Hermes Tweet's shipped source repository package.
Reject hosted AI app directories and assistant action galleries such as ChatGPT
apps, OpenAI Apps SDK examples, GPT action directories, MCP UI registries,
Vercel AI SDK templates, or LangChain Hub snippets when they require app
manifests, UI widgets, action schemas, SDK demos, or hub snippets instead of a
source-linked Hermes Tweet package entry.
Reject browser-automation and computer-use agent toolkits such as Browser Use,
Stagehand, Browserbase, Hyperbrowser, Playwright agent tools, or browser-agent
registries when they require browser task scripts, replay recipes, hosted
browser workflows, DOM automation examples, or computer-use action packs instead
of a source-linked Hermes Tweet package entry.
Reject enterprise hosted-agent surfaces such as Google Vertex AI Agent Builder,
Salesforce Agentforce, ServiceNow AI Agent Studio, Oracle AI Agent Studio,
Slack agent platform tools, and Mistral agent connectors when they only accept
platform-native extensions, connectors, actions, or managed-agent definitions.
Reject code-assistant extension marketplaces and developer-agent tool catalogs
such as Amazon Q Developer, Continue, Sourcegraph Cody, JetBrains Junie, Devin,
or Tabby when they only accept IDE extensions, editor plugins, workspace
automation packs, or assistant-specific tool definitions instead of a
PR-editable Hermes Tweet source package entry.
Reject local coding-agent command packs, workflow recipes, and rule bundles
such as GitHub Copilot Extensions, OpenCode commands, Aider workflows, Goose
extensions, Kiro hooks, or Amp tools when they only accept agent-local prompts,
commands, recipes, hooks, or editor workflows instead of a source-linked Hermes
Tweet package entry.
Reject hosted automation, app-action, and component galleries such as Zapier,
Pipedream, Activepieces, Composio, Arcade, Toolhouse, or Langflow when the
route only accepts workflow templates, provider connectors, hosted app actions,
or framework-native components. Treat those as integration surfaces unless they
expose a PR-editable third-party source repository entry for Hermes Tweet's
shipped package.
Reject embedded `.agents`, `.agent`, `.antigravity`, project-template, and
copied skill directories inside application repositories unless the repository
itself documents a third-party skill catalog, registry, or contribution lane.
Treat those hits as downstream copies or mirrors, not fresh Hermes Tweet
submission routes.
Reject personal agent memory repositories, OpenHands microagent folders, and
hosted MCP directory profile pages such as `.openhands`, Smithery, Glama, or
PulseMCP unless the route exposes a licensed, PR-editable source entry that can
reference Hermes Tweet's shipped package without copying or translating it.
Reject catalogs whose contribution rules require measurable community usage,
maturity, a minimum star count, or a maintainer-curated quality bar until Hermes
Tweet visibly satisfies that target's stated threshold or a maintainer
explicitly asks for another submission. Treat a closed prior Hermes Tweet PR for
maturity, usage, or quality-bar reasons as a target-specific blocker, not as an
invitation to resubmit with the same evidence.
Reject source-packet, evidence-packet, handoff-guide, Xquik toolkit,
xquik-twitter-data, or Xquik API integration submissions when they do not add a
target-native Hermes Tweet entry.

## Duplicate Gate

Before opening or refreshing a submission:

- Search the target README, docs, manifests, examples, skills, and indexes for
  `Hermes Tweet`, `hermes-tweet`, `Xquik`, and the repository URL.
- Run a public GitHub code search for live `Hermes Tweet`, `hermes-tweet`, and
  repository URL mentions before treating a target as fresh. If the hit is an
  accepted default-branch listing, record it in `docs/ECOSYSTEM.md` instead of
  opening a duplicate submission.
- Check open and closed PRs and issues for prior Hermes Tweet proposals.
- Treat a closed prior Hermes Tweet issue as a completed or rejected submission
  route. Do not reopen the same target with a PR unless a maintainer asks for a
  new PR, conversion, or updated evidence.
- Search open and closed PRs and issues for adjacent `TweetClaw`, `OpenClaw`,
  `SocialClaw`, `x-twitter-scraper`, and Xquik-only proposals before treating a
  target as fresh.
- Treat adjacent-only PR history as a conflict signal unless the target docs
  show a separate native Hermes Tweet route.
- Treat accepted adjacent entries as saturation too. If the target already has
  a live Xquik, TweetClaw, OpenClaw, SocialClaw, or x-twitter-scraper entry in
  the same catalog, tool list, or awesome-list section, reject another Hermes
  Tweet submission unless the target has a distinct Hermes Agent plugin lane.
- For awesome lists, plugin lists, and topic-search hits, treat an open
  adjacent X/social submission in the same target as saturation when the target
  has no explicit Hermes Tweet or Hermes Agent plugin lane. A generic Claude
  plugin or agent-skill heading is not enough by itself when the adjacent entry
  would occupy the same list slot.
- If any open authored PR in the target is Xquik-only, TweetClaw-only,
  OpenClaw-only, source-packet-only, evidence-packet-only, MCP-data-only, or
  otherwise adjacent-only, treat the target as saturated. Do not open another
  submission there unless a maintainer explicitly asks for a target-specific
  Hermes Tweet conversion or separate native Hermes Tweet entry.
- Require the PR or issue title and summary to name `Hermes Tweet` or
  `hermes-tweet`. Do not submit or refresh routes titled only for `Xquik`,
  `TweetClaw`, `OpenClaw`, or other adjacent projects.
- Before waiting on checks, reread the outbound title, summary, and added
  lines. If the branch or PR is Xquik-only, TweetClaw-only, OpenClaw-only, or
  otherwise adjacent-only, close it immediately with a short scope comment
  instead of leaving off-scope outreach open.
- Reject slugs, package names, plugin names, or catalog keys centered on
  `xquik-*`, `tweetclaw-*`, `openclaw-*`, `source-packets`, or
  `evidence-packets` unless the same submission clearly installs or indexes
  Hermes Tweet as the native entry.
- Check accepted examples so the wording, file layout, and validation match the
  target's own format.
- For translated or mirrored awesome lists, check the upstream source list and
  translation issue tracker. If either already has a live Hermes Tweet entry,
  open Hermes Tweet PR, or open Hermes Tweet issue, treat the mirror as
  duplicate unless the maintainer asks for an independent localized submission.
- Trace fork parents before using a personal fork, and use a renamed fork only
  when the normal fork name is already occupied by another parent.
- Respect target contribution docs. If a target requires issue-first
  submissions or maintainer-curated additions, update the existing issue or
  open a new issue instead of opening a direct PR.

If a target already has a live Hermes Tweet entry, do not open another one.
Refresh only when it fixes a concrete merge blocker, stale target-native
wording, or broken validation evidence.

## Native Wording

Prefer concise wording that explains where Hermes Tweet fits:

- native Hermes Agent X/Twitter plugin
- optional Hermes Agent backend for X/Twitter reads
- read-only by default, with explicit action gating
- compatible with Hermes Desktop, remote gateway, TUI, CLI, dashboard, cron, and
  CI smoke-test surfaces
- source-native `.claude-plugin/plugin.json` metadata for catalogs that install
  plugins directly from a repository
- source-native `.codex-plugin/plugin.json` metadata with HOL Plugin Scanner
  evidence for Codex plugin catalogs
- complementary to local browser-cookie or direct OAuth examples
- copied endpoint URLs resolve only to catalog-listed `/api/v1/...` paths

Avoid wording that implies Hermes Tweet replaces the target project, fixes a
target bug, bypasses platform rules, removes user approval, or requires secrets
inside docs, prompts, issues, or PR comments.

## Validation

Every submission should include target-native validation when feasible:

- target tests, linters, manifest checks, catalog generators, or README
  generators
- `git diff --check`
- exact conflict-marker scan
- added-line public-safety scan for secrets and private implementation details
- live link checks for Hermes Tweet, Xquik, and target-owned links touched by
  the change

If the target has no CI and the submission repairs a conflict or review
request, leave at most one concise validation comment. Do not repeat comments
when the PR already has current validation evidence.

When creating PRs or issues from a shell, write Markdown bodies through a
reviewed file or another non-interpolating path. Verify the rendered body keeps
repository names, backticked literals, and validation commands intact before
waiting on checks or asking maintainers to review.

## Public-Safety Gate

Public submissions must not include:

- API keys, cookies, tokens, screenshots, logs, or private runtime artifacts
- nonpublic service names, restricted provider names, nonpublic pricing units,
  or private implementation details
- commands that require production SSH, browser login, manual legal acceptance,
  payment, or secret retrieval

Keep public examples to placeholder environment variable names and documented
Hermes Tweet settings: `XQUIK_API_KEY`, `XQUIK_BASE_URL`, and
`HERMES_TWEET_ENABLE_ACTIONS`.
