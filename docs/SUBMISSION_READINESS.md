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
Treat the contribution license as detectable only after checking both GitHub
metadata and obvious root license files such as `LICENSE`, `LICENSE.md`,
`COPYING`, or `NOTICE`. When metadata is empty but a root license file exists,
read it before rejecting; accept only clear OSI-style permission text.
Reject crawler or indexer directories whose submission path is only a hosted
claim form, upload UI, or account-gated directory unless the repository exposes
a seed, source, catalog, or registry file that can be changed by PR.
Reject generated catalog or marketplace files unless target docs identify them
as the canonical edit surface. When a target builds indexes from another source,
submit only through the documented source file or generator input; skip the
route when that source cannot carry a target-native Hermes Tweet entry.
Reject source-packet, evidence-packet, handoff-guide, Xquik toolkit,
xquik-twitter-data, or Xquik API integration submissions when they do not add a
target-native Hermes Tweet entry.

## Duplicate Gate

Before opening or refreshing a submission:

- Search the target README, docs, manifests, examples, skills, and indexes for
  `Hermes Tweet`, `hermes-tweet`, `Xquik`, and the repository URL.
- Check open and closed PRs and issues for prior Hermes Tweet proposals.
- Search open and closed PRs and issues for adjacent `TweetClaw`, `OpenClaw`,
  `SocialClaw`, `x-twitter-scraper`, and Xquik-only proposals before treating a
  target as fresh.
- Treat adjacent-only PR history as a conflict signal unless the target docs
  show a separate native Hermes Tweet route.
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
- Reject slugs, package names, plugin names, or catalog keys centered on
  `xquik-*`, `tweetclaw-*`, `openclaw-*`, `source-packets`, or
  `evidence-packets` unless the same submission clearly installs or indexes
  Hermes Tweet as the native entry.
- Check accepted examples so the wording, file layout, and validation match the
  target's own format.
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
