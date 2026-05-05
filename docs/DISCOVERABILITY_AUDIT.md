# Discoverability Audit

Hermes Tweet is a public Hermes Agent plugin for X automation through Xquik.

## Current Public Surfaces

| Surface | Status | Notes |
| --- | --- | --- |
| GitHub repository | Published | Public at `https://github.com/Xquik-dev/hermes-tweet`. |
| PyPI package | Pending | Package name: `hermes-tweet`. |
| Hermes ecosystem directories | In audit | Submit only where plugin listings are relevant and rules allow it. |
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
| 2026-05-06 | `ksimback/hermes-ecosystem` / Hermes Atlas | Deferred | Read README, CONTRIBUTING, issue templates, issue and PR history, and searched for Hermes Tweet/Xquik terms. The map is relevant, but its inclusion rules require at least 1 GitHub star unless official or notable. Revisit after the repo has initial adoption. |
