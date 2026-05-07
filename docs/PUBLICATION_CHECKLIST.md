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
- [x] Add Xquik docs cross-link.
- [x] Add TweetClaw README cross-link.
- [x] Start directory submissions from `docs/DISCOVERABILITY_AUDIT.md`.

## Manual Operator Actions

See `docs/OPERATOR_HANDOFF.md` for optional signed-in submissions, local-secret
smoke tests, and maintainer-blocked directory routes. No urgent manual action is
required after the v0.1.6 release; the remaining useful manual paths are
SkillRegistry.io upload, Sundial authenticated publish, optional Skills.Rest
outreach after operator approval, and local
`XQUIK_API_KEY` smoke testing.

Runtime verification note: on 2026-05-06, local Hermes Agent v0.12.0 loaded
Hermes Tweet from a git install, registered `tweet_explore`, `tweet_read`,
`tweet_action`, `/xstatus`, `/xtrends`, and `hermes-tweet:hermes-tweet`, ran a
real `tweet_read` call against `/api/v1/account`, and confirmed
`tweet_action` returns disabled while `HERMES_TWEET_ENABLE_ACTIONS` is unset.
The runtime check also found and fixed directory-plugin namespace import issues
in the root loader and catalog resource lookup.

Runtime verification note: on 2026-05-07, a live smoke test used an ephemeral
`XQUIK_API_KEY` from the maintainer's macOS Keychain, not repo files, command
text, PRs, issues, logs, CI, or `~/.hermes/.env`. Direct Xquik probes returned
HTTP 200 for `/api/v1/account`, `/api/v1/radar`, `/api/v1/trends`,
`/api/v1/x/users/search`, and `/api/v1/x/tweets/search`. Local Hermes Agent
v0.12.0 loaded the enabled `hermes-tweet` toolset, a one-shot `tweet_read`
against `/api/v1/account` returned `LIVE_ACCOUNT_READ_OK` without echoing the
key, and `tweet_action` stayed disabled while
`HERMES_TWEET_ENABLE_ACTIONS` was unset.

Release verification note: on 2026-05-06, v0.1.3 published through GitHub
Actions trusted publishing. PyPI direct version JSON exposed the dedicated
Hermes Tweet guide for Homepage and Documentation immediately, while the
project JSON and simple index lagged briefly before showing v0.1.3. A fresh
Python 3.12 install verified the wheel metadata, `plugin.yaml`,
`catalog_data.json`, and bundled `hermes-tweet` skill. Local Hermes Agent
v0.12.0 then updated the git plugin to 0.1.3 and loaded the toolset, tools,
slash commands, bundled skill, `tweet_explore`, and disabled `tweet_action`.
Use `hermes tools list` for scripted diagnostics; `hermes tools --summary`
requires an interactive TTY in this runtime.

Release verification note: on 2026-05-06, v0.1.4 published through GitHub
Actions trusted publishing after PR #46 and master CI passed. PyPI direct
version JSON, project JSON, and the simple index exposed 0.1.4 after brief
cache lag. A fresh Python 3.12 install verified the wheel metadata,
`plugin.yaml`, `catalog_data.json`, and bundled `hermes-tweet` skill with
registry-oriented `version`, `author`, and `tags` frontmatter. Local Hermes
Agent v0.12.0 installed the committed branch as plugin version 0.1.4, loaded
the `hermes-tweet` toolset, verified the bundled plugin skill metadata, ran
`tweet_explore` in a one-shot tool probe, and confirmed `tweet_action` returns
disabled while `HERMES_TWEET_ENABLE_ACTIONS` is unset. piwheels JSON initially
lagged at 0.1.3, then reported 0.1.4 before the run ended.

Release verification note: on 2026-05-06, v0.1.5 published through GitHub
Actions trusted publishing after PR #55 and master CI passed. PyPI direct
version JSON, project JSON, and the simple index exposed 0.1.5 after brief
cache lag. A fresh Python 3.12 install with `--refresh-package hermes-tweet`
verified the wheel metadata, `plugin.yaml`, `catalog_data.json`, and bundled
`hermes-tweet` skill with nested registry metadata. Local Hermes Agent v0.12.0
installed the built wheel with
`uv pip install --python ~/.hermes/hermes-agent/venv/bin/python`, because that
Hermes venv does not expose `python -m pip`. The runtime loaded the
`hermes-tweet` toolset, registered `tweet_explore`, `tweet_read`,
`tweet_action`, `/xstatus`, `/xtrends`, and the bundled skill, verified
`tweet_explore`, and confirmed API/action gates stay closed while
`XQUIK_API_KEY` is unset. piwheels JSON and page initially lagged at 0.1.4, then
exposed 0.1.5 before final verification ended.

Release verification note: on 2026-05-07, v0.1.6 published through GitHub
Actions trusted publishing after PR #66 and master CI passed. PyPI direct
version JSON, project JSON, and the simple index expose 0.1.6. A fresh Python
3.12 install verified the published wheel metadata, `plugin.yaml`,
`catalog_data.json`, and bundled `hermes-tweet` skill with the refreshed
`/api/v1/x/dm/{userId}` request-body description. Local Hermes Agent v0.12.0
installed the published PyPI wheel with
`uv pip install --python ~/.hermes/hermes-agent/venv/bin/python --refresh --index-url https://pypi.org/simple 'hermes-tweet==0.1.6'`,
loaded the `hermes-tweet` toolset, ran a live one-shot `tweet_read` against
`/api/v1/account` without echoing the Keychain-loaded API key, and confirmed
`tweet_action` remains disabled while `HERMES_TWEET_ENABLE_ACTIONS` is unset.
ClawHub was updated to registry version `1.0.2` with hosted 0.1.6 metadata and
clean moderation. piwheels JSON and page still lagged at 0.1.5 during this
verification pass.
