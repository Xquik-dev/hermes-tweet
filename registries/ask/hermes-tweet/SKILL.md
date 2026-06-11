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
