# Hermes Tweet installed

Hermes Tweet installs as the `hermes-tweet` toolset. If you skipped `--enable`, run:

```bash
hermes plugins enable hermes-tweet
hermes plugins list
```

Set your Xquik API key before using read tools:

```bash
export XQUIK_API_KEY="xq_..."
```

For persistent Hermes sessions, add it to `~/.hermes/.env`:

```bash
XQUIK_API_KEY=xq_...
```

After editing `~/.hermes/.env`, reload the CLI or restart gateway and cron sessions.
Without `XQUIK_API_KEY`, Hermes exposes only `tweet_explore` from this plugin.

Keep actions disabled unless you intend to allow account changes:

```bash
export HERMES_TWEET_ENABLE_ACTIONS=false
```

Run this smoke test:

```bash
hermes -z "Use tweet_explore, then read /api/v1/account. Do not call tweet_action." --toolsets hermes-tweet
```

Use catalog-listed `/api/v1/...` paths from `tweet_explore`. Copied endpoint
URLs are accepted only when they resolve to catalog-listed paths.

Expect:

- `tweet_explore` loads without an API call.
- `tweet_read` works when `XQUIK_API_KEY` is set.
- `/xstatus` and `/xtrends` are registered slash commands.
- `tweet_action` stays hidden or returns a disabled error unless
  `HERMES_TWEET_ENABLE_ACTIONS=true`.

For Hermes Agent v0.16.0, do not use `hermes -z "/xstatus"` as a slash-command smoke
test. One-shot `-z` treats that text as a model prompt. Verify slash commands in
an active CLI or gateway session, or through the plugin registry tests.
