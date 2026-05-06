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
- [x] Run `hermes plugins enable hermes-tweet`.
- [x] Confirm `tweet_explore`, `tweet_read`, and slash commands load.
- [x] Confirm `tweet_action` is blocked unless action env is enabled.
- [ ] Add Xquik docs cross-link.
- [ ] Add TweetClaw README cross-link.
- [x] Start directory submissions from `docs/DISCOVERABILITY_AUDIT.md`.

Runtime verification note: on 2026-05-06, local Hermes Agent v0.12.0 loaded
Hermes Tweet from a git install, registered `tweet_explore`, `tweet_read`,
`tweet_action`, `/xstatus`, `/xtrends`, and `hermes-tweet:hermes-tweet`, ran a
real `tweet_read` call against `/api/v1/account`, and confirmed
`tweet_action` returns disabled while `HERMES_TWEET_ENABLE_ACTIONS` is unset.
The runtime check also found and fixed directory-plugin namespace import issues
in the root loader and catalog resource lookup.
