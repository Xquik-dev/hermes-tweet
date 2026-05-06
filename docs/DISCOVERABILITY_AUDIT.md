# Discoverability Audit

Hermes Tweet is a public Hermes Agent plugin for X automation through Xquik.

## Current Public Surfaces

| Surface | Status | Notes |
| --- | --- | --- |
| GitHub repository | Published | Public at `https://github.com/Xquik-dev/hermes-tweet`. |
| PyPI package | Published | Public at `https://pypi.org/project/hermes-tweet/`. |
| Hermes ecosystem directories | In progress | Hermes Atlas PR `https://github.com/ksimback/hermes-ecosystem/pull/169`, Hermes Skill Atlas submission `https://github.com/codesstar/hermes-skill-atlas/issues/1`, and `itgoyo/hermes-skills` PR `https://github.com/itgoyo/hermes-skills/pull/1` are open. |
| Xquik docs | Pending | Add after repository URL is live. |
| TweetClaw README cross-link | Pending | Add after repository URL is live. |

## Candidate Discovery Queries

- `Hermes Agent plugin directory`
- `Hermes Agent Twitter plugin`
- `Hermes Agent X plugin`
- `Hermes Agent skills hub`
- `Hermes Agent awesome list`
- `Hermes plugin marketplace`
- `AI agent social media plugin`
- `Twitter automation Hermes Agent`

## Submission Rules

- Read each candidate repository's README, contributing guide, code of conduct,
  issue templates, PR templates, and license before submitting.
- Search open issues, closed issues, open PRs, merged PRs, and repository
  content for `hermes-tweet`, `xquik`, `tweetclaw`, and `x-twitter-scraper`.
- Do not submit duplicates, rejected entries, broad promotional copy, or
  unrelated directory entries.
- Prefer one high-quality compliant PR over many shallow submissions.
- Record no-op reasons so future runs do not repeat work.

## Audit Log

| Date | Target | Result | Notes |
| --- | --- | --- | --- |
| 2026-05-06 | Initial repo preparation | Prepared | Added public metadata, strict CI, templates, and publication checklist. |
| 2026-05-06 | `Xquik-dev/hermes-tweet` GitHub repository | Published | Created public repo, pushed `master`, confirmed CI success, and aligned GitHub topics with repo metadata. |
| 2026-05-06 | Official Hermes Agent docs | Compatible | Checked plugin, toolset, slash-command, and skill docs. Current repo still matches `ctx.register_tool`, `ctx.register_command`, bundled skill, and `hermes_agent.plugins` entry point patterns. |
| 2026-05-06 | `0xNyk/awesome-hermes-agent` | No new submission | Read README, CONTRIBUTING, CODE_OF_CONDUCT, license, issue and PR history, and searched for Hermes Tweet/Xquik terms. The list is relevant, but CONTRIBUTING asks for issues instead of direct PRs and issue #44 already covers Xquik X access, so a second issue would be duplicative today. |
| 2026-05-06 | `ksimback/hermes-ecosystem` / Hermes Atlas | PR open | Read README, CONTRIBUTING, issue templates, validator workflow, issue and PR history, and searched open issues, closed issues, PRs, and repository content for Hermes Tweet/Xquik terms. No duplicate was found. Opened repo suggestion issue `https://github.com/ksimback/hermes-ecosystem/issues/168` in `Plugins & Extensions`; Atlas validation passed and created PR `https://github.com/ksimback/hermes-ecosystem/pull/169`. |
| 2026-05-06 | `amanning3390/hermeshub` | No new submission | Read README, workflows, issue and PR history, and searched for Hermes Tweet/Xquik terms. The registry accepts skill PRs, but PR #54 already proposes an Xquik X skill, so a Hermes Tweet submission would duplicate the active queue. |
| 2026-05-06 | `ChuckSRQ/awesome-hermes-skills` | No new submission | Read README, license, repo files, and searched issues, PRs, and repository content for Hermes Tweet/Xquik terms. The repo is a curated four-skill bundle with no contribution guide, issue templates, or outside-entry list format; direct Hermes Tweet listing would be thin. Revisit only if the repo opens a general catalog section or requests third-party skill submissions. |
| 2026-05-06 | `codesstar/hermes-skill-atlas` | Issue open | Read README, CONTRIBUTING, issue templates, license, data format, open issues, open PRs, and searched repository content for Hermes Tweet/Xquik terms. No duplicate was found. Opened skill submission issue `https://github.com/codesstar/hermes-skill-atlas/issues/1` in `通讯社交 (Comms)` with PyPI install, bundled skill, and action-gating metadata. |
| 2026-05-06 | `itgoyo/hermes-skills` | PR open | Read README contribution rules, repo files, open issues, open PRs, and repository content for Hermes Tweet/Xquik terms. No duplicate was found. Opened PR `https://github.com/itgoyo/hermes-skills/pull/1` adding a repo-native `social-media/hermes-tweet` skill, README count entry, and `.bundled_manifest` hash. |
