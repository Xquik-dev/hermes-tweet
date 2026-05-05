# Hermes Tweet

[![CI](https://github.com/Xquik-dev/hermes-tweet/actions/workflows/ci.yml/badge.svg)](https://github.com/Xquik-dev/hermes-tweet/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/hermes-tweet.svg)](https://pypi.org/project/hermes-tweet/)
[![Python](https://img.shields.io/pypi/pyversions/hermes-tweet.svg)](https://pypi.org/project/hermes-tweet/)
[![Apify Actor](https://apify.com/actor-badge?actor=xquik/x-tweet-scraper)](https://apify.com/xquik/x-tweet-scraper)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Native [Hermes Agent](https://github.com/NousResearch/hermes-agent) plugin for
X automation through [Xquik](https://xquik.com).

Hermes Tweet brings X search, account reads, tweet posting, replies, likes,
retweets, follows, DMs, monitors, webhooks, draws, extraction jobs, media, and
trend reads into Hermes as structured tools.

Use it when you need a Hermes Agent Twitter plugin, Hermes X automation, social
media automation for agents, or a native Hermes toolset for X/Twitter.

## Highlights

- Native Hermes plugin with `plugin.yaml` and pip entry point.
- 99 agent-callable Xquik endpoints generated from OpenAPI.
- 32 MPP-tagged read endpoints in the bundled catalog.
- Read and action tools are split for least-privilege operation.
- Action endpoints are disabled by default.
- Bundled Hermes skill for agent-facing usage guidance.
- Slash commands for account status and trends.
- Strict CI with formatting, linting, type checking, tests, coverage, security
  scan, dependency audit, and package build checks.

## Install

From a local checkout:

```bash
pip install -e .
hermes plugins enable hermes-tweet
```

For public distribution:

```bash
pip install hermes-tweet
hermes plugins enable hermes-tweet
```

## Configure

Create an API key in the Xquik dashboard, then set:

```bash
export XQUIK_API_KEY="xq_..."
```

Optional settings:

```bash
export XQUIK_BASE_URL="https://xquik.com"
export HERMES_TWEET_ENABLE_ACTIONS="false"
```

Action endpoints are disabled unless `HERMES_TWEET_ENABLE_ACTIONS=true`.

## Security Model

Hermes Tweet never accepts credentials through tool arguments. Auth is read from
environment variables and injected by the plugin at request time.

The plugin blocks dashboard-only admin, billing, credit top-up, support-ticket,
API-key, and account re-authentication endpoints from the catalog. Private reads
and write-like endpoints go through `tweet_action`, which is hidden unless
`HERMES_TWEET_ENABLE_ACTIONS=true`.

## Tools

| Tool | Purpose |
| --- | --- |
| `tweet_explore` | Search the bundled Xquik endpoint catalog. No API call. |
| `tweet_read` | Call catalog-listed read-only endpoints. |
| `tweet_action` | Call write-like or private endpoints. Disabled by default. |

Use `tweet_explore` first, then call `tweet_read` or `tweet_action` with a
concrete `/api/v1/...` path.

## Slash Commands

| Command | Purpose |
| --- | --- |
| `/xstatus` | Show Xquik account, subscription, and usage status. |
| `/xtrends` | Show current X trends. |

## Development

Generate the bundled catalog from Xquik OpenAPI:

```bash
python scripts/build_catalog.py ../xquik/openapi.yaml
```

Run checks:

```bash
uv run --python 3.12 --extra dev ruff format --check .
uv run --python 3.12 --extra dev ruff check .
uv run --python 3.12 --extra dev basedpyright
uv run --python 3.12 --extra dev pytest --cov=hermes_tweet --cov=tests --cov-report=term-missing --cov-fail-under=100
uv run --python 3.12 --extra dev bandit -c pyproject.toml -r hermes_tweet scripts
uv run --python 3.12 --extra dev pip-audit
uv run --python 3.12 --extra dev python -m build
uv run --python 3.12 --extra dev twine check dist/*
```

For a single local quality gate:

```bash
uv run --python 3.12 --extra dev ruff format --check . && \
uv run --python 3.12 --extra dev ruff check . && \
uv run --python 3.12 --extra dev basedpyright && \
uv run --python 3.12 --extra dev pytest --cov=hermes_tweet --cov=tests --cov-report=term-missing --cov-fail-under=100 && \
uv run --python 3.12 --extra dev bandit -c pyproject.toml -r hermes_tweet scripts && \
uv run --python 3.12 --extra dev pip-audit && \
uv run --python 3.12 --extra dev python -m build && \
uv run --python 3.12 --extra dev twine check dist/*
```

## Relationship To TweetClaw

TweetClaw is the OpenClaw-native npm plugin. Hermes Tweet is the Hermes-native
Python plugin. Both use the same Xquik API contract.

## Public Repo Metadata

Recommended GitHub description:

> Native Hermes Agent plugin for X/Twitter automation through Xquik.

Recommended topics:

`hermes-agent`, `hermes-plugin`, `twitter`, `x`, `x-api`, `xquik`,
`tweet`, `automation`, `social-media`, `ai-agent`, `mcp`, `agent-tools`,
`twitter-api`, `twitter-automation`, `x-twitter`
