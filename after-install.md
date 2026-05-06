# Hermes Tweet Installed

Hermes Tweet is enabled as the `hermes-tweet` toolset.

Set your Xquik API key before using read tools:

```bash
export XQUIK_API_KEY="xq_..."
```

For persistent Hermes sessions, add it to `~/.hermes/.env`:

```bash
XQUIK_API_KEY=xq_...
```

Keep actions disabled unless you are intentionally allowing account-changing
operations:

```bash
export HERMES_TWEET_ENABLE_ACTIONS=false
```

Quick smoke test:

```bash
hermes -z "Use tweet_explore, then read /api/v1/account. Do not call tweet_action." --toolsets hermes-tweet
```

Expected behavior:

- `tweet_explore` loads without an API call.
- `tweet_read` works when `XQUIK_API_KEY` is set.
- `/xstatus` and `/xtrends` are registered slash commands.
- `tweet_action` returns a disabled error unless `HERMES_TWEET_ENABLE_ACTIONS=true`.
