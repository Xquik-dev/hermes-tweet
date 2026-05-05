# Observability

Hermes Tweet exposes operational visibility through structured tool outputs,
Hermes plugin logs, and slash commands.

## Runtime Signals

- `/xstatus` returns account, subscription, and usage status.
- `/xtrends` confirms authenticated read access and current trend availability.
- Tool handlers return JSON strings for both success and error cases.
- API failures include HTTP status and response payload without exposing
  credentials.

## Safety Signals

- `tweet_read` rejects private or write-like endpoints.
- `tweet_action` rejects every call unless `HERMES_TWEET_ENABLE_ACTIONS=true`.
- Dashboard-only admin, billing, credit top-up, support-ticket, API-key, and
  account re-authentication endpoints are omitted from the catalog.

## CI Signals

Public CI runs formatting, linting, type checking, tests, coverage, security
scan, dependency audit, package build, and package metadata validation.

