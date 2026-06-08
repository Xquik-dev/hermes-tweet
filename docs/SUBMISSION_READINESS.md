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
- Skill registries, plugin catalogs, awesome lists, or ecosystem directories

Do not submit when the target is only a browser-cookie workflow, only a
TweetClaw route, unrelated to X/Twitter or Hermes Agent, archived, or not
licensed for contribution.

## Duplicate Gate

Before opening or refreshing a submission:

- Search the target README, docs, manifests, examples, skills, and indexes for
  `Hermes Tweet`, `hermes-tweet`, `Xquik`, and the repository URL.
- Check open and closed PRs and issues for prior Hermes Tweet proposals.
- Check accepted examples so the wording, file layout, and validation match the
  target's own format.
- Trace fork parents before using a personal fork, and use a renamed fork only
  when the normal fork name is already occupied by another parent.

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
- complementary to local browser-cookie or direct OAuth examples

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
