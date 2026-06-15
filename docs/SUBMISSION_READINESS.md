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
Flowise, Haystack, Sema4.ai, MindsDB, or product-specific tool adapters unless
the target accepts external source repositories in Hermes Tweet's shipped
package format. Do not translate Hermes Tweet into another runtime package,
tool subclass, module, framework tool, block, extension, action, pipeline, or
function pack just to satisfy a framework marketplace.
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
Reject prompt, evaluation, and observability hubs such as LangSmith Hub,
PromptLayer, Langfuse, Braintrust, promptfoo, or OpenPipe when they only accept
prompt templates, eval datasets, trace dashboards, eval configs, SDK snippets,
or experiment recipes instead of a source-linked Hermes Tweet package entry.
Reject RAG, retrieval, and vector-store integration catalogs such as LlamaHub,
Pinecone Assistant, Weaviate, Qdrant, Chroma, or retriever plugin galleries
when they only accept data loaders, vector indexes, retriever classes, ingestion
pipelines, or demo notebooks instead of a source-linked Hermes Tweet package
entry.
Reject notebook, data-app, and BI assistant galleries such as Jupyter AI,
NotebookLM, marimo, Hex, Deepnote, Observable Framework, or Databricks Apps when
they only accept notebooks, magic commands, app templates, dashboards,
workspace recipes, or data-app examples instead of a source-linked Hermes Tweet
package entry.
Reject browser-automation and computer-use agent toolkits such as Browser Use,
Stagehand, Browserbase, Hyperbrowser, Playwright agent tools, or browser-agent
registries when they require browser task scripts, replay recipes, hosted
browser workflows, DOM automation examples, or computer-use action packs instead
of a source-linked Hermes Tweet package entry.
Reject enterprise hosted-agent surfaces such as Google Vertex AI Agent Builder,
Salesforce Agentforce, ServiceNow AI Agent Studio, Oracle AI Agent Studio,
Slack agent platform tools, and Mistral agent connectors when they only accept
platform-native extensions, connectors, actions, or managed-agent definitions.
Reject productivity and workspace app directories such as Google Workspace
Marketplace, Microsoft Teams apps, Slack App Directory, Notion, Airtable,
monday.com, or Asana when they only accept app add-ons, workspace bots,
slash-command apps, database blocks, workspace automations, or product-specific
integrations instead of a source-linked Hermes Tweet package entry.
Reject CRM, support, and commerce app marketplaces such as HubSpot Marketplace,
Salesforce AppExchange, Zendesk Marketplace, Intercom App Store, Freshworks
Marketplace, Pipedrive Marketplace, Zoho Marketplace, or Shopify App Store when
they only accept CRM apps, support widgets, sales automations, helpdesk macros,
commerce app packages, or storefront integrations instead of a source-linked
Hermes Tweet package entry.
Reject community chat and bot directories such as Discord App Directory,
Discord bot lists, Telegram bot catalogs, Matrix bot directories, Mastodon app
directories, Reddit app directories, or Twitch Extension Marketplace when they
only accept chat bots, server apps, slash commands, moderation workflows, social
feed relays, or extension packages instead of a source-linked Hermes Tweet
package entry.
Reject CMS, content publishing, and creator platform marketplaces such as
WordPress Plugin Directory, Drupal module directory, Ghost integrations,
Webflow App Marketplace, Wix App Market, or Squarespace Extensions when they
only accept CMS plugins, theme extensions, site widgets, publishing
automations, form handlers, or website-builder app packages instead of a
source-linked Hermes Tweet package entry.
Reject social listening, brand monitoring, and marketing analytics app
directories such as Hootsuite App Directory, Buffer integrations, Sprout Social
app directory, Semrush App Center, brand-monitoring integration galleries, or
martech app marketplaces when they only accept dashboards, analytics connectors,
reporting widgets, campaign automations, social inbox apps, or
platform-specific integrations instead of a source-linked Hermes Tweet package
entry.
Reject LMS, documentation, and knowledge-base marketplaces such as Moodle
Plugin Directory, Canvas LMS integrations, Blackboard app catalog, Confluence
Marketplace, GitBook integrations, or knowledge-base app marketplaces when they
only accept course plugins, learning-tool integrations, documentation widgets,
space macros, help-center automations, or knowledge-base connectors instead of
a source-linked Hermes Tweet package entry.
Reject API marketplaces, public API networks, and developer portal catalogs
such as RapidAPI, Postman Public API Network, SwaggerHub, Stoplight, ReadMe,
Kong Plugin Hub, or API gateway marketplaces when they only accept API specs,
hosted API listings, request collections, docs workspaces, gateway plugins, or
API management connectors instead of a source-linked Hermes Tweet package
entry.
Reject finance, accounting, payroll, procurement, and ERP app marketplaces
such as QuickBooks App Store, Xero App Store, NetSuite SuiteApps, SAP Store,
Workday Marketplace, ADP Marketplace, Stripe App Marketplace, or procurement
app marketplaces when they only accept accounting connectors, billing apps,
payroll automations, procurement workflows, ERP extensions, or
platform-native financial integration packages instead of a source-linked
Hermes Tweet package entry.
Reject HR, recruiting, talent, benefits, and workforce app marketplaces such as
Greenhouse integrations, Lever integrations, Ashby marketplace, Workable app
marketplace, BambooHR app marketplace, Gusto integrations, LinkedIn Talent
Solutions partner apps, or recruiting app marketplaces when they only accept
ATS connectors, candidate-source automations, job board integrations,
interview workflows, employee-directory apps, benefits connectors, onboarding
tasks, or workforce platform packages instead of a source-linked Hermes Tweet
package entry.
Reject healthcare, EHR, FHIR, telehealth, wellness, and fitness app
marketplaces such as Epic App Orchard, Oracle Health App Gallery, SMART App
Gallery, FHIR app galleries, athenahealth Marketplace, telehealth app
marketplaces, wellness app marketplaces, or fitness app marketplaces when they
only accept EHR integrations, clinical apps, FHIR launch apps, patient portal
widgets, care workflows, wellness programs, device integrations, or
platform-native health app packages instead of a source-linked Hermes Tweet
package entry.
Reject legal, compliance, e-signature, identity, and KYC app marketplaces such
as DocuSign App Center, Adobe Acrobat Sign integrations, Okta Integration
Network, Auth0 Marketplace, OneTrust app catalogs, Vanta integrations, Drata
integrations, or compliance automation marketplaces when they only accept
e-signature connectors, identity integrations, compliance controls, audit
workflows, trust-center automations, KYC checks, or platform-native governance
apps instead of a source-linked Hermes Tweet package entry.
Reject security operations, SIEM, SOAR, and observability integration catalogs
such as Splunkbase, Elastic integrations, Datadog integrations, Grafana plugin
catalog, New Relic Instant Observability, Sumo Logic app catalog, or Cortex
XSOAR content packs when they only accept dashboards, detection rules, log
parsers, alert connectors, runbooks, incident workflows, or platform-specific
integration packages instead of a source-linked Hermes Tweet package entry.
Reject CI/CD, DevOps automation, and pipeline extension marketplaces such as
GitHub Marketplace Actions, GitLab CI/CD Catalog, CircleCI orb registry,
Jenkins plugin index, Buildkite plugins, Travis CI add-ons, or pipeline
automation marketplaces when they only accept workflow actions, CI templates,
orb packages, build plugins, deployment automations, or source-control
workflows instead of a source-linked Hermes Tweet package entry.
Reject container, cloud-native, and infrastructure packaging registries such as
Docker Hub extensions, Kubernetes operator catalogs, Helm chart repositories,
Artifact Hub, Terraform Registry, Pulumi Registry, Crossplane package registry,
or Backstage plugin catalogs when they only accept container images, operators,
charts, infrastructure providers, platform plugins, or deployment packages
instead of a source-linked Hermes Tweet package entry.
Reject browser, desktop, launcher, shortcut, and mobile app extension stores
such as Chrome Web Store, Firefox Add-ons, Microsoft Edge Add-ons, Raycast
extensions, Alfred workflows, Setapp, iOS Shortcuts galleries, or Android app
marketplaces when they only accept browser extensions, desktop launcher
commands, packaged apps, mobile intents, automation shortcuts, or app-store
listings instead of a source-linked Hermes Tweet package entry.
Reject design, creative, whiteboard, and knowledge-app plugin marketplaces such
as Figma Community plugins, Canva Apps Marketplace, Miro Marketplace, FigJam
widgets, Adobe Express add-ons, Framer Marketplace, Obsidian community plugins,
or Blender extensions when they only accept design plugins, canvas widgets,
creative app add-ons, personal knowledge plugins, scene extensions, or
product-native UI integrations instead of a source-linked Hermes Tweet package
entry.
Reject game engine, AR/VR, 3D asset, and creator gaming marketplaces such as
Unity Asset Store, Unreal Engine Marketplace, Roblox Creator Store, Godot Asset
Library, Steamworks tools, itch.io tool marketplaces, Meta Quest App Lab, or
VRChat marketplaces when they only accept engine plugins, editor extensions,
game assets, scripts, SDK integrations, creator tools, avatar or world
packages, or app-store listings instead of a source-linked Hermes Tweet package
entry.
Reject voice assistant, speech, meeting, and real-time communications app
marketplaces such as Alexa Skills Store, Google Assistant Actions, Bixby
capsules, Zoom App Marketplace, Microsoft Teams meeting apps, Slack huddle app
surfaces, or conferencing integration catalogs when they only accept voice
skills, assistant actions, meeting bots, call workflows, transcript tools, or
communications app packages instead of a source-linked Hermes Tweet package
entry.
Reject email marketing, newsletter, scheduling, event, form, and survey app
marketplaces such as Mailchimp integrations, SendGrid integrations, Brevo app
store, Substack app directories, Calendly integrations, Eventbrite app
marketplace, Typeform app marketplace, or SurveyMonkey app directories when
they only accept email automations, newsletter connectors, booking workflows,
event listings, form widgets, survey templates, or platform-native integration
packages instead of a source-linked Hermes Tweet package entry.
Reject maps, geospatial, travel, mobility, logistics, and fleet app
marketplaces such as Google Maps Platform integrations, Mapbox plugin catalog,
ArcGIS Marketplace, QGIS plugin repository, travel booking marketplaces,
Expedia app marketplace, Uber developer app marketplaces, or logistics and
fleet app marketplaces when they only accept map plugins, GIS extensions,
geospatial data connectors, travel booking widgets, ride-hailing workflows,
fleet automations, or route-optimization packages instead of a source-linked
Hermes Tweet package entry.
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
Reject RPA and no-code automation marketplaces such as UiPath, Robocorp, n8n,
Make, or Workato when they only accept bots, community nodes, workflow exports,
automation recipes, or task templates instead of a source-linked Hermes Tweet
package entry.
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
