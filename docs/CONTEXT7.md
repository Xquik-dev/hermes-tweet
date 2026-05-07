# Context7 Guide

Use this page as the compact Context7-facing guide for Hermes Tweet. It focuses
on install, auth, safe tool use, and smoke tests for coding agents.

## Install

Install from the public GitHub repository:

```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
```

Install the published Python package into the Hermes Python environment:

```bash
uv pip install --python ~/.hermes/hermes-agent/venv/bin/python hermes-tweet
hermes plugins enable hermes-tweet
```

Use the PyPI package name `hermes-tweet` and the Hermes toolset name
`hermes-tweet`.

## Configure

Create an API key in the Xquik dashboard and set it in the runtime environment:

```bash
export XQUIK_API_KEY="xq_..."
```

Optional settings:

```bash
export XQUIK_BASE_URL="https://xquik.com"
export HERMES_TWEET_ENABLE_ACTIONS="false"
```

Hermes Tweet never accepts credentials through tool arguments. If
`XQUIK_API_KEY` is missing, Hermes should expose only `tweet_explore`. That is
expected safe gating.

## Tools

| Tool | Use |
| --- | --- |
| `tweet_explore` | Search the bundled Xquik endpoint catalog without an API call. |
| `tweet_read` | Call catalog-listed read-only Xquik API endpoints. |
| `tweet_action` | Call write-like or private endpoints when actions are enabled. |

Use `tweet_explore` first. Then call `tweet_read` with a concrete
`/api/v1/...` path for account checks, tweet search, user lookup, trends,
media reads, monitors, webhooks, draws, or extraction jobs.

Keep `HERMES_TWEET_ENABLE_ACTIONS=false` for unattended sessions. Enable actions
only when the workflow intentionally allows posting, replies, likes, retweets,
follows, DMs, monitor changes, webhook changes, media uploads, or other account
changes.

## Smoke Test

```bash
hermes tools list
hermes -z "Use tweet_explore, then read /api/v1/account. Do not call tweet_action." --toolsets hermes-tweet
```

Expected result:

- `tweet_explore` finds endpoints without using the API key.
- `tweet_read` can read `/api/v1/account` after `XQUIK_API_KEY` is set.
- `tweet_action` stays disabled unless `HERMES_TWEET_ENABLE_ACTIONS=true`.
- `/xstatus` and `/xtrends` are registered slash commands.

If you edit `~/.hermes/.env` during an active Hermes CLI session, run
`/reload`. Gateway and cron sessions need a restart or new session.

## Public Sources

- GitHub: <https://github.com/Xquik-dev/hermes-tweet>
- Xquik guide: <https://docs.xquik.com/guides/hermes-tweet>
- PyPI: <https://pypi.org/project/hermes-tweet/>
- DeepWiki: <https://deepwiki.com/Xquik-dev/hermes-tweet>
- Context7: <https://context7.com/xquik-dev/hermes-tweet>
