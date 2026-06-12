# Integration Patterns

Use this guide when deciding how Hermes Tweet fits with browser-cookie skills,
official API examples, OpenClaw skills, MCP servers, and catalog listings. The
goal is to keep Hermes Tweet positioned as the Hermes Agent runtime path, not as
a replacement for every local X/Twitter tool.

## Positioning

Hermes Tweet is the native Hermes Agent plugin for X/Twitter work through
Xquik. It is best when the workflow needs:

- a Hermes plugin entry point from PyPI or GitHub
- `tweet_explore` catalog discovery before tool calls
- API-key managed reads through `tweet_read`
- explicit action gating through `tweet_action`
- the same toolset across Desktop, remote gateway, dashboard, TUI, CLI, cron,
  and CI smoke-test surfaces

Keep local browser-cookie skills as the local account/session path. Keep direct
official API examples as implementation references. Keep Hermes Tweet as the
managed Hermes Agent path for reads, monitoring, support triage, research,
launch checks, and approval-gated account actions.

## Complementary Routes

Browser-cookie skills:
Keep them for local browser sessions, media download, archive jobs, and
account-specific local state. Add Hermes Tweet when the workflow should run from
Hermes Desktop, a remote gateway, a dashboard-managed runtime, or unattended
cron without relying on a laptop Chrome session.

Official X API examples:
Keep them for direct OAuth or API implementation details. Add Hermes Tweet when
the agent should avoid raw OAuth handling and call managed Hermes tools through
`XQUIK_API_KEY`.

OpenClaw skills:
Keep them for OpenClaw-native browser workflows and SKILL.md discovery. Add
Hermes Tweet when a Hermes Agent user needs the same X/Twitter read or action
capability from a Hermes runtime.

MCP servers:
Keep them for MCP-native clients and tool schemas. Add Hermes Tweet when the
user wants a native Hermes plugin with slash commands, bundled skill guidance,
and Hermes plugin enablement.

Skill catalogs and awesome lists:
Keep them for discovery and comparison. Add Hermes Tweet when the listing
accepts Hermes Agent plugins, X/Twitter skills, social automation tools, or
optional backend notes. Before opening a public submission, use
`docs/SUBMISSION_READINESS.md` to check fit, duplicates, wording, validation,
and public-safety requirements.

## Tool Choice

- Use `tweet_explore` first when a user asks what Hermes Tweet can do.
- Use `tweet_read` for public or account read routes that the catalog marks as
  read-safe.
- Copied endpoint URLs are fine, but Hermes Tweet matches only catalog-listed
  paths.
- Use `tweet_action` only when the user asks for posting, replies, DMs,
  follows, monitor changes, webhook changes, media changes, extraction jobs, or
  draw actions and actions are explicitly enabled.
- Keep `HERMES_TWEET_ENABLE_ACTIONS=false` for cron, gateway, research,
  monitoring, support triage, and other unattended sessions unless the workflow
  includes an explicit approval step.

## Outreach Copy

Use wording like:

- optional Hermes Agent backend for X/Twitter reads
- managed Hermes Agent X/Twitter toolset
- Hermes Desktop and remote gateway compatible X/Twitter plugin
- read-only by default, with explicit action gating
- complementary to local browser-cookie workflows

Avoid wording that implies Hermes Tweet replaces a target project, fixes a
target bug, bypasses platform rules, or removes the need for user approval on
account actions.
