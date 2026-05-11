# Publication Checklist

Hermes Tweet is published as `hermes-tweet` on PyPI and currently released at
`0.1.6`.

## Before GitHub Publication

- [x] Set repository description from `docs/GITHUB_METADATA.md`.
- [x] Add recommended GitHub topics from `docs/GITHUB_METADATA.md`.
- [x] Enable issues, Actions, Dependabot alerts, and security updates.
- [x] Enable secret scanning and push protection.
- [x] Confirm branch protection requires CI.

## Before PyPI Publication

- [x] Add the PyPI trusted publisher for `Xquik-dev/hermes-tweet`.
- [x] Regenerate `hermes_tweet/catalog_data.json` from current Xquik OpenAPI.
- [x] Run the full quality gate from `AGENTS.md`.
- [x] Build from a clean working tree and run `twine check dist/*`.
- [x] Verify the wheel contains `plugin.yaml`, `catalog_data.json`, and the
  bundled Hermes skill.
- [x] Publish through GitHub Actions trusted publishing.
- [x] Verify PyPI metadata, README rendering, simple index visibility, and a
  fresh install.

## After Publication

- [x] Install from PyPI in a fresh environment.
- [x] Run `hermes plugins enable hermes-tweet`.
- [x] Confirm `tweet_explore`, `tweet_read`, `tweet_action`, `/xstatus`, and
  `/xtrends` load.
- [x] Confirm `tweet_action` is blocked unless
  `HERMES_TWEET_ENABLE_ACTIONS=true`.
- [x] Confirm PyPI, piwheels, ClawHub, first-party docs, Context7, DeepWiki,
  and accepted ecosystem listings show current public metadata.
- [x] Maintain accepted public ecosystem surfaces in `docs/ECOSYSTEM.md`.

## Release Gate

Run these checks before any new package release:

```bash
uv run --python 3.12 --extra dev ruff format --check .
uv run --python 3.12 --extra dev ruff check .
uv run --python 3.12 --extra dev basedpyright
uv run --python 3.12 --extra dev pytest --cov=hermes_tweet --cov=tests --cov-report=term-missing --cov-fail-under=100
uv run --python 3.12 --extra dev bandit -c pyproject.toml -r hermes_tweet scripts
uv run --python 3.12 --extra dev pip-audit
uv run --python 3.12 --extra dev python -m build
uv run --python 3.12 --extra dev twine check dist/*
actionlint .github/workflows/*.yml
```

## Runtime Smoke Test

Use a local secret store or ephemeral environment variable. Never paste an API
key into chat, commits, PRs, issues, or logs.

```bash
hermes tools list
hermes -z "Use tweet_explore, then read /api/v1/account. Do not call tweet_action." --toolsets hermes-tweet
```

Expected result:

- `tweet_explore` loads without an API call.
- `tweet_read` works when `XQUIK_API_KEY` is configured.
- `tweet_action` stays hidden or returns a disabled error unless actions are
  explicitly enabled.
- `/xstatus` and `/xtrends` are registered slash commands.

## Manual Operator Actions

Keep optional signed-in submissions, local-secret smoke tests, pending outreach,
duplicate checks, and maintainer-blocked directory routes in private operator
notes. Do not commit those operational notes to the public repository. No
package release blocker remains after the `0.1.6` release.
