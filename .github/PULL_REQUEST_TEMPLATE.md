## Summary

## Verification

- [ ] `uv run --python 3.12 --extra dev ruff format --check .`
- [ ] `uv run --python 3.12 --extra dev ruff check .`
- [ ] `uv run --python 3.12 --extra dev basedpyright`
- [ ] `uv run --python 3.12 --extra dev pytest --cov=hermes_tweet --cov=tests --cov-report=term-missing --cov-fail-under=100`
- [ ] `uv run --python 3.12 --extra dev bandit -c pyproject.toml -r hermes_tweet scripts`
- [ ] `uv run --python 3.12 --extra dev pip-audit`
- [ ] `uv run --python 3.12 --extra dev python -m build`
- [ ] `uv run --python 3.12 --extra dev twine check dist/*`
- [ ] `actionlint .github/workflows/*.yml`

## Public Safety

- [ ] No secrets, tokens, cookies, private screenshots, or private implementation details.
- [ ] Write-like endpoints remain gated.
- [ ] Public claims are source-verified.
