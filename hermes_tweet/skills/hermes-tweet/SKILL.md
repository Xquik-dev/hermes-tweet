---
name: hermes-tweet
description: Use Xquik from Hermes Agent for X search, posting, replies, likes, retweets, follows, DMs, monitors, extraction jobs, draws, media, and trends.
---

# Hermes Tweet

Use Hermes Tweet when the user wants to automate or inspect X through Xquik.

## Workflow

1. Use `tweet_explore` to find the endpoint.
2. Use `tweet_read` for public read-only endpoints.
3. Use `tweet_action` only for writes or private reads after stating the exact endpoint and payload.

## Safety

- Never ask for or reveal API keys, signing keys, passwords, cookies, or TOTP secrets.
- Never pass credentials in tool arguments.
- Use only catalog-listed `/api/v1/...` endpoints.
- Do not use account connection, re-authentication, API key, billing, credit top-up, or support-ticket endpoints.
- For posting, deleting, following, DMs, profile changes, monitors, webhooks, extraction jobs, and draws, summarize the action before calling `tweet_action`.

## Examples

Search tweets:

```json
{"query":"tweet search","method":"GET"}
```

Then call:

```json
{"path":"/api/v1/x/tweets/search","query":{"q":"AI agents","limit":25}}
```

Post a tweet:

```json
{"query":"post tweet","include_actions":true}
```

Then call `tweet_action` with:

```json
{"path":"/api/v1/x/tweets","method":"POST","body":{"account":"@example","text":"Hello from Hermes Tweet"},"reason":"Post the user-approved tweet."}
```

