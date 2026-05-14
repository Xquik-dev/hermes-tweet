# Hermes Tweet

Native Hermes Agent plugin for X automation through Xquik.

## Commands

```bash
uv run --python 3.12 --extra dev ruff format --check .
uv run --python 3.12 --extra dev ruff check .
uv run --python 3.12 --extra dev basedpyright
uv run --python 3.12 --extra dev pytest --cov=hermes_tweet --cov=tests --cov-report=term-missing --cov-fail-under=100
uv run --python 3.12 --extra dev bandit -c pyproject.toml -r hermes_tweet scripts
uv run --python 3.12 --extra dev pip-audit
uv run --python 3.12 --extra dev python scripts/check_public_links.py
uv run --python 3.12 --extra dev python -m build
uv run --python 3.12 --extra dev twine check dist/*
actionlint .github/workflows/*.yml
python scripts/build_catalog.py ../xquik/openapi.yaml
```

## Rules

- Public repo: never commit secrets, tokens, cookies, private screenshots, or
  private implementation details.
- Keep external communication generic and public-safe.
- Never mention internal service names, internal cost units, or private vendor
  architecture.
- Preserve user changes and avoid unrelated refactors.
- Keep the catalog generated from Xquik OpenAPI.
- Keep action endpoints gated behind `HERMES_TWEET_ENABLE_ACTIONS=true`.
- Check public documentation and manifest links before publication or outreach.
- Do not weaken, suppress, or bypass lint, type, test, coverage, security, or
  package checks.
- Run the simplify skill after changing code.

## Release Checklist

1. Regenerate the catalog from current Xquik OpenAPI.
2. Run all checks above.
3. Verify all public documentation and manifest links.
4. Build the package and run `twine check dist/*`.
5. Verify `plugin.yaml`, `pyproject.toml`, README, and bundled skill version.
6. Publish through GitHub Actions trusted publishing from a clean, tagged release.
7. Use local PyPI auth only as a fallback, and never print or commit credentials.
