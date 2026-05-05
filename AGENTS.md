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
uv run --python 3.12 --extra dev python -m build
uv run --python 3.12 --extra dev twine check dist/*
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
- Do not weaken, suppress, or bypass lint, type, test, coverage, security, or
  package checks.
- Run the simplify skill after changing code.

## Release Checklist

1. Regenerate the catalog from current Xquik OpenAPI.
2. Run all checks above.
3. Build the package and run `twine check dist/*`.
4. Verify `plugin.yaml`, `pyproject.toml`, README, and bundled skill version.
5. Publish only from a clean working tree with PyPI auth configured locally.

