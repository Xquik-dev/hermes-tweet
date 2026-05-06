# Observability

Hermes Tweet exposes operational visibility through structured tool outputs,
Hermes plugin logs, and slash commands.

## Runtime Signals

- `/xstatus` returns account, subscription, and usage status.
- `/xtrends` confirms authenticated read access and current trend availability.
- Tool handlers return JSON strings for both success and error cases.
- API failures include HTTP status and response payload without exposing
  credentials.
- `hermes plugins list` shows whether the plugin is installed and enabled.
- `hermes tools list` shows the `hermes-tweet` toolset in non-interactive
  terminals. Bare `hermes tools` opens the interactive tool UI and requires a
  TTY. Hermes v0.12.0 lists plugin toolsets there, not every individual plugin
  tool name.
- The Hermes plugin registry exposes loaded tools, slash commands, and bundled
  plugin skills for deterministic runtime smoke tests.

## Safety Signals

- `tweet_read` rejects private or write-like endpoints.
- `tweet_action` rejects every call unless `HERMES_TWEET_ENABLE_ACTIONS=true`.
- Dashboard-only admin, billing, credit top-up, support-ticket, API-key, and
  account re-authentication endpoints are omitted from the catalog.

## CI Signals

Public CI runs workflow linting, formatting, linting, type checking, tests,
coverage, security scan, dependency audit, package build, and package metadata
validation.
The release workflow uses current artifact actions so trusted-publishing runs
stay ahead of GitHub Actions runtime deprecations.

## Runtime Smoke Test

Use this check after installing or updating Hermes Tweet:

```bash
hermes tools list
hermes -z "Use tweet_explore, then read /api/v1/account. Do not call tweet_action." --toolsets hermes-tweet
```

Record only sanitized outcomes:

- Catalog exploration succeeded.
- Without `XQUIK_API_KEY`, Hermes exposed only `tweet_explore` from this plugin.
- With `XQUIK_API_KEY`, account read succeeded or returned a status code.
- `tweet_action` stayed hidden or disabled when `HERMES_TWEET_ENABLE_ACTIONS`
  was unset.
- `/xstatus` and `/xtrends` were registered.

Do not store API keys in shell history, docs, issue comments, CI logs, PR bodies,
or Hermes prompts. Use an ephemeral environment variable for one-off smoke tests
or `~/.hermes/.env` for local persistent Hermes sessions. After changing
`~/.hermes/.env` in an active Hermes session, run `/reload` before the smoke
test so the session reads the new values.
