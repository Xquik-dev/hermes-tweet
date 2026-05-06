# Publication Checklist

## Before GitHub Publication

- [x] Set repository description from `docs/GITHUB_METADATA.md`.
- [x] Add recommended topics from `docs/GITHUB_METADATA.md`.
- [x] Enable issues.
- [x] Enable Dependabot alerts and security updates.
- [x] Enable secret scanning and push protection.
- [x] Confirm GitHub Actions is enabled.
- [x] Confirm branch protection requires CI.

## Before PyPI Publication

- [x] Add PyPI pending trusted publisher:
      `hermes-tweet` / `Xquik-dev` / `hermes-tweet` / `publish.yml` / `pypi`.
- [x] Regenerate catalog from current Xquik OpenAPI.
- [x] Run the full quality gate from `AGENTS.md`.
- [x] Build package from a clean working tree.
- [x] Run `twine check dist/*`.
- [x] Verify wheel contains `plugin.yaml`, `catalog_data.json`, and bundled skill.
- [x] Publish through GitHub Actions trusted publishing.
- [x] Verify PyPI metadata, README rendering, and install command.

## After Publication

- [x] Install from PyPI in a fresh environment.
- [ ] Run `hermes plugins enable hermes-tweet`.
- [ ] Confirm `tweet_explore`, `tweet_read`, and slash commands load.
- [ ] Confirm `tweet_action` is hidden unless action env is enabled.
- [ ] Add Xquik docs cross-link.
- [ ] Add TweetClaw README cross-link.
- [x] Start directory submissions from `docs/DISCOVERABILITY_AUDIT.md`.

Runtime verification note: local `hermes` CLI was not available during the
2026-05-06 heartbeat, so the plugin enable/load checks remain open.
