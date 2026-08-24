# Hermes Tweet

Native Hermes Agent plugin for X automation through Xquik.

Every commit must reduce net handwritten source LOC. No exceptions. No one may waive this rule.
Additions require larger, useful simplifications elsewhere in this repository.
Formatting, minification, generated files, and deleted valuable tests or docs do not count.

## Commands

```bash
uv run --python 3.12 --group dev ruff format --check .
uv run --python 3.12 --group dev ruff check .
uv run --python 3.12 --group dev basedpyright
uv run --python 3.12 --group dev pytest --cov=hermes_tweet --cov=tests --cov-report=term-missing --cov-fail-under=100
uv run --python 3.12 --group dev bandit -c pyproject.toml -r hermes_tweet scripts fuzz
uv run --python 3.12 --group dev python scripts/check_public_safety.py
uv run --python 3.12 --group dev python scripts/check_license_headers.py
uv run --python 3.12 --group dev pip-audit
uv run --python 3.12 --group dev python scripts/check_public_links.py
uv run --python 3.12 --group dev python scripts/check_hermes_agent_compat.py
uv run --python 3.12 --group dev bash scripts/check_reproducible.sh
uv run --python 3.12 --group dev python -m build
uv run --python 3.12 --group dev twine check dist/*
actionlint .github/workflows/*.yml
python scripts/build_catalog.py ../xquik/openapi.yaml
```

## Rules

- Public repo: never commit secrets, tokens, cookies, private screenshots, or
  private implementation details.
- Never mention nonpublic service names, pricing units, or vendor architecture.
- Preserve user changes and avoid unrelated refactors.
- Keep the catalog generated from Xquik OpenAPI.
- Keep action endpoints gated behind `HERMES_TWEET_ENABLE_ACTIONS=true`.
- Check public links and run the safety scan before publication or outreach.
- Keep Hermes Agent plugin lifecycle, source SHA locks, install guidance, and
  workflow positioning current with official Hermes Agent docs and source.
- Do not weaken, suppress, or bypass lint, type, test, coverage, security, or
  package checks.
- Run the simplify skill after changing code.

## Release Checklist

1. Run all checks above against the current Xquik OpenAPI.
2. Verify `plugin.yaml`, `pyproject.toml`, README, and bundled skill version.
3. Publish through GitHub Actions from a clean, tagged release.
4. Use local PyPI auth only as a secret-safe fallback.
