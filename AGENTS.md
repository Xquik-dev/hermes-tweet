# Agent Guide for Hermes Tweet

This file tells coding agents how to change this repository.
Hermes Tweet is a Hermes Agent plugin for X (Twitter) search and approved X actions.

## Know the layout

- `plugin.yaml` and `hermes_tweet/plugin.yaml` describe the plugin to Hermes. Keep them identical.
- `hermes_tweet/__init__.py` registers the 3 tools, the 2 slash commands and the bundled Skill.
- `hermes_tweet/tools.py` runs `tweet_explore`, `tweet_read` and `tweet_action`.
- `hermes_tweet/client.py` sends each request to the Xquik API.
- `scripts/build_catalog.py` writes the endpoint catalog to `hermes_tweet/catalog_data.json`.
- `skills/hermes-tweet/` and `hermes_tweet/skills/hermes-tweet/` hold the bundled Skill. Keep both copies identical.
- `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` describe the plugin to Claude Code and Codex.
- `tests/` holds the pytest suite. `scripts/` holds the check scripts.

## Set up

Install the locked dependencies on Python 3.12.

```bash
uv sync --locked --python 3.12 --group dev
```

## Run the checks

`bin/check-local` runs every check a change must pass. Run it before you open a pull request.

```bash
bin/check-local --no-status
```

Without `--no-status`, it posts a commit status for a clean, pushed commit.

Run single checks while you work.

```bash
uv run ruff format --check .
uv run ruff check --ignore-noqa .
uv run basedpyright
uv run mypy
uv run pytest --cov=hermes_tweet --cov=tests --cov-report=term-missing --cov-fail-under=100
uv run python scripts/check_public_safety.py
uv run python scripts/check_license_headers.py
uv run bandit -c pyproject.toml -r hermes_tweet scripts fuzz
uv run pip-audit
bash scripts/plugin-scan
```

Regenerate the catalog after the OpenAPI schema changes.

```bash
uv run python scripts/build_catalog.py /path/to/openapi.yaml
```

## Follow the code rules

- Ruff runs every rule. Fix each finding, because `--ignore-noqa` voids `noqa` comments.
- basedpyright and mypy run in strict mode. Never use `typing.Any` or `typing.cast`.
- The build rejects `type: ignore`, `mypy:` and `pyright:` comments.
- Tests cover 100% of `hermes_tweet` and `tests`. Add a test for each code change.
- Start each Python, shell, TOML and YAML file with the 2 SPDX lines the other files carry.
- Change dependencies in `pyproject.toml`, then run `uv lock`.

## Keep actions safe

- Tools never accept credentials as arguments. The plugin reads `XQUIK_API_KEY` at request time.
- `tweet_explore` and `tweet_read` handle reads. `tweet_action` handles private reads and writes.
- `tweet_action` stays off until `HERMES_TWEET_ENABLE_ACTIONS=true`.
- Keep admin, billing, credit, support, guest-wallet and API-key routes out of the catalog.

## Write public text

- Every file here is public. Describe only public behavior.
- Add each new public text file to `scripts/public_surfaces.py`. The safety scan reads that list.
- Never commit secrets, API keys or `.env` files.
- Update the README and both Skill copies when behavior changes.
- Never weaken a lint, type, coverage, security, dependency or package check.
