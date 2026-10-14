# Publication checklist

Hermes Tweet is published as `hermes-tweet` on PyPI. Require PyPI and GitHub
Releases to match protected source. Verify live versions before every release.

## Before GitHub publication

- [x] Set repository description from `docs/GITHUB_METADATA.md`.
- [x] Add recommended GitHub topics from `docs/GITHUB_METADATA.md`.
- [x] Enable issues, Actions, Dependabot alerts, and security updates.
- [x] Enable secret scanning and push protection.
- [x] Confirm branch protection requires the `xquik-local-checks` status.

## Before PyPI publication

- [x] Store the PyPI token where `bin/release-local` reads it.
- [x] Protect release tags from updates and deletion.
- [x] Regenerate `hermes_tweet/catalog_data.json` from current Xquik OpenAPI.
- [x] Run `bin/check-local`.
- [x] Build from a clean working tree and run `twine check dist/*`.
- [x] Verify the wheel contains `plugin.yaml`, `catalog_data.json`, and the
  bundled Hermes skill.
- [x] Publish with `bin/release-local`.
- [x] Verify PyPI metadata, README rendering, simple index visibility, and a
  fresh install.

## After publication

- [x] Install from PyPI in a fresh environment.
- [ ] Run `hermes plugins enable hermes-tweet`.
- [ ] Confirm `tweet_explore`, `tweet_read`, `tweet_action`, `/xstatus`, and
  `/xtrends` load.
- [x] Confirm `tweet_action` is blocked unless
  `HERMES_TWEET_ENABLE_ACTIONS=true`.
- [x] Confirm PyPI, piwheels, ClawHub, first-party docs, Context7, DeepWiki,
  and accepted ecosystem listings show current public metadata.
- [x] Maintain accepted public listings in `docs/ECOSYSTEM.md`.
- [x] Use `docs/SUBMISSION_READINESS.md` before public skill, plugin, catalog,
  registry, awesome-list, or integration submissions.
- [x] Keep Codex plugin metadata, root security policy, local icon, and scanner
  workflow ready for Codex catalog submissions.

## Release gate

Merge each version change through protected `master`. Then run
`bin/release-local` on a clean `master`.

It runs `bin/check-local`, checks every public link, builds, and uploads to
PyPI. It compares the PyPI files with the local build. Only then it pushes the
`v*` tag and creates the GitHub release with both distributions.

`bin/release-local --dry-run` previews a release. It uploads, tags, and
releases nothing.

PyPI has no trusted publisher for `hermes-tweet`. A maintainer's PyPI token is
the only way it publishes. `bin/release-local` reads that token from the
Keychain item that `PYPI_KEYCHAIN_SERVICE` names.

Never create or publish the GitHub release manually.

Run these checks before any new package release.

```bash
uv run --python 3.12 --group dev ruff format --check .
uv run --python 3.12 --group dev ruff check .
uv run --python 3.12 --group dev basedpyright
uv run --python 3.12 --group dev pytest --cov=hermes_tweet --cov=tests --cov-report=term-missing --cov-fail-under=100
uv run --python 3.12 --group dev bandit -c pyproject.toml -r hermes_tweet scripts fuzz
uv run --python 3.12 --group dev python scripts/check_public_safety.py
uv run --python 3.12 --group dev pip-audit
uv run --python 3.12 --group dev python scripts/check_public_links.py
uv run --python 3.12 --group dev python scripts/check_hermes_agent_compat.py
uv run --python 3.12 --group dev bash scripts/check_reproducible.sh
uv run --python 3.12 --group dev python -m build
uv run --python 3.12 --group dev twine check dist/*
```

## Hermes Agent compatibility gate

Before changing plugin registration, manifests, install docs, or release
metadata, verify the current official Hermes Agent plugin docs and source.

- [Build a Hermes Plugin](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins)
- [Plugins feature guide](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins/)
- [`hermes_cli/plugins.py`](https://github.com/NousResearch/hermes-agent/blob/main/hermes_cli/plugins.py)
- [`tools/registry.py`](https://github.com/NousResearch/hermes-agent/blob/main/tools/registry.py)
- [`hermes_cli/plugins_cmd.py`](https://github.com/NousResearch/hermes-agent/blob/main/hermes_cli/plugins_cmd.py)

Run the compatibility checker before release, outreach, or plugin-facing docs
updates.

```bash
uv run --python 3.12 --group dev python scripts/check_hermes_agent_compat.py
```

If a locked Hermes Agent source SHA changes, review the official diff first,
then update Hermes Tweet runtime, docs, tests, and the checker lock together.

The latest reviewed locks date from August 20, 2026. They are `hermes_cli/plugins.py`
`2493d8f21eddc0617d04e9ee48812846086eade4`, `tools/registry.py`
`081040911499f8bb7e5a947e9c85b5e459fd3dd0`, and
`hermes_cli/plugins_cmd.py` `912d93208d2169f2a51bff4dc8b6fed1dfd204c0`.

Reviewed changes preserve manifest and registration APIs.

Keep the runtime contract aligned with those sources.

- `plugin.yaml` keeps the rich `XQUIK_API_KEY` `requires_env` installer prompt.
- `tweet_explore` stays ungated and makes no network call.
- `tweet_read` stays gated by `check_api_available` and `XQUIK_API_KEY`.
- `tweet_action` stays gated by `action_enabled`, `XQUIK_API_KEY`, and
  `HERMES_TWEET_ENABLE_ACTIONS`.
- Tool handlers accept future Hermes context keyword arguments, catch
  exceptions, and return JSON strings.
- Bundled skills continue to register through `ctx.register_skill`.
- `plugin.yaml` declares `python_runtime: external`, and `httpx` stays the only
  runtime dependency, so Hermes admits the plugin without a dependency step.
- Install docs explain that user and PyPI entry-point plugins are opt-in and
  need `--enable`, `hermes plugins enable hermes-tweet`, or an explicit
  `plugins.enabled` entry.
- Install docs explain Hermes may warn or block after its security scan.
- Local project-plugin docs mention `HERMES_ENABLE_PROJECT_PLUGINS=true` only
  for trusted repositories.
- User-facing docs keep at least one concrete Hermes Agent workflow section for
  social listening, launch monitoring, support triage, research, audits, and
  controlled publishing.

## Runtime smoke test

Use a local secret store or ephemeral environment variable. Never paste an API
key into chat, commits, PRs, issues, or logs.

```bash
hermes tools list
hermes -z "Use tweet_explore, then read /api/v1/account. Do not call tweet_action." --toolsets hermes-tweet
```

Expect these results.

- `tweet_explore` loads without an API call.
- Copied endpoint URLs resolve only to catalog-listed `/api/v1/...` paths.
- `tweet_read` works when `XQUIK_API_KEY` is configured.
- `tweet_action` stays hidden or returns a disabled error unless actions are
  explicitly enabled.
- `/xstatus` and `/xtrends` are registered slash commands.

## Manual operator actions

Keep optional signed-in submissions, local-secret smoke tests, pending outreach,
duplicate checks, and maintainer-blocked directory routes in private operator
notes. Do not commit those operational notes to the public repository. A new
package release and post-publication checks remain.
