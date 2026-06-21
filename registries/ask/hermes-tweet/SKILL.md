---
name: hermes-tweet
description: Search Twitter/X, read tweet replies, look up users, monitor tweets, export followers, and gate X actions through Xquik.
version: 0.1.6
author: Xquik
license: MIT
tags:
  - hermes-agent
  - xquik
  - twitter
  - x
  - social-media
  - automation
metadata:
  version: 0.1.6
  author: Xquik
  repository: https://github.com/Xquik-dev/hermes-tweet
  plugin: hermes plugins install Xquik-dev/hermes-tweet --enable
capabilities:
  shell:
    required: false
    justification: Optional Hermes CLI checks are used only for installation and registry diagnostics.
  network:
    required: true
    justification: Hermes Tweet tools call Xquik API routes for X/Twitter reads and approved actions.
  files:
    required: false
    justification: Normal use does not require local file reads or writes.
  environment:
    required: true
    variables:
      - XQUIK_API_KEY
      - HERMES_TWEET_ENABLE_ACTIONS
      - HERMES_ENABLE_PROJECT_PLUGINS
    justification: Runtime configuration controls authenticated reads, gated actions, and trusted project-local plugin loading.
  mcp:
    required: false
    justification: No MCP server access is required.
  tools:
    - tweet_explore
    - tweet_read
    - tweet_action
---

# Hermes Tweet

Use this ASK-compatible wrapper when a Hermes Agent user needs the native Hermes
Tweet plugin for X/Twitter automation through Xquik.

## Install

Install the native plugin in Hermes Agent:

```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
hermes tools list
```

Set `XQUIK_API_KEY` in the Hermes runtime environment before using authenticated
read or action tools. Do not paste the key into chat.

## When to Use

Use Hermes Tweet for:

- scrape/search tweets or search Twitter/X
- read tweet replies and tweet details
- look up users and public profiles
- monitor tweets or accounts
- export followers and following lists
- post tweets/replies, send DMs, or automate X actions after explicit approval

## Tool Flow

1. Use `tweet_explore` to find the catalog endpoint.
2. Use `tweet_read` for public read-only endpoints.
3. Use `tweet_action` only for approved writes, private reads, monitors,
   webhooks, extraction jobs, giveaway draws, or media operations.

## Safety

- Never ask for API keys, passwords, cookies, or TOTP secrets.
- Never pass credentials in tool arguments.
- Use only catalog-listed `/api/v1/...` endpoints.
- Copied endpoint URLs are accepted only when they resolve to catalog-listed paths.
- Keep write actions gated behind `HERMES_TWEET_ENABLE_ACTIONS=true`.
- Summarize the exact action before posting, replying, sending DMs, or changing
  account state.

## Permissions and Trust

- Tool scope: use only `tweet_explore`, `tweet_read`, and `tweet_action` through
  the enabled Hermes Tweet toolset.
- Network scope: call only catalog-listed Xquik API routes through those tools.
  Do not create direct HTTP fallbacks.
- File scope: do not write files, logs, screenshots, cached payloads, or
  credentials unless the user asks for an explicit export workflow.
- Environment scope: check only whether `XQUIK_API_KEY`,
  `HERMES_TWEET_ENABLE_ACTIONS`, and `HERMES_ENABLE_PROJECT_PLUGINS` are
  configured. Never request or echo values.
- Output: return concise Markdown summaries, action previews, or JSON-like tool
  payloads. `tweet_action` may change account or workflow state only after
  explicit approval.
- Release gate: do not present this skill as NVIDIA-verified unless the release
  includes a clean SkillSpector review, `skill-card.md`, Tier-3 eval data,
  `BENCHMARK.md`, `skill.oms.sig`, and signature verification instructions.
