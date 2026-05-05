# Publication Checklist

## Before GitHub Publication

- [ ] Set repository description from `docs/GITHUB_METADATA.md`.
- [ ] Add recommended topics from `docs/GITHUB_METADATA.md`.
- [ ] Enable issues.
- [ ] Enable Dependabot alerts and security updates.
- [ ] Confirm GitHub Actions is enabled.
- [ ] Confirm branch protection requires CI.

## Before PyPI Publication

- [ ] Regenerate catalog from current Xquik OpenAPI.
- [ ] Run the full quality gate from `AGENTS.md`.
- [ ] Build package from a clean working tree.
- [ ] Run `twine check dist/*`.
- [ ] Verify wheel contains `plugin.yaml`, `catalog_data.json`, and bundled skill.
- [ ] Publish with local PyPI auth only.
- [ ] Verify PyPI metadata, README rendering, and install command.

## After Publication

- [ ] Install from PyPI in a fresh environment.
- [ ] Run `hermes plugins enable hermes-tweet`.
- [ ] Confirm `tweet_explore`, `tweet_read`, and slash commands load.
- [ ] Confirm `tweet_action` is hidden unless action env is enabled.
- [ ] Add Xquik docs cross-link.
- [ ] Add TweetClaw README cross-link.
- [ ] Start directory submissions from `docs/DISCOVERABILITY_AUDIT.md`.

