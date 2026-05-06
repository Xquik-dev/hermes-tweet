# Operator Handoff

This file tracks tasks that need a signed-in human account, a local secret, or a
maintainer response before Hermes Tweet can move forward.

## No Urgent Manual Action

Hermes Tweet is published, installed, and discoverable across the primary
surfaces already:

- GitHub repository and docs homepage are public.
- PyPI, direct PyPI version JSON, simple index, piwheels JSON, and piwheels page
  expose `0.1.5`.
- SKILLS.re lists Hermes Tweet.
- AgentSkill lists Hermes Tweet and serves the agent install API.
- ClawHub lists Hermes Tweet with clean moderation.
- First-party Xquik docs and TweetClaw links are current.
- Local Hermes v0.12.0 exposes the `hermes-tweet` plugin toolset.

## Optional Manual Submissions

These are useful but not blocking.

### SkillRegistry.io

- Route: `https://skillregistry.io/upload`
- Submit: `skills/hermes-tweet/SKILL.md`
- Why manual: upload requires GitHub sign-in and admin review.
- Do not submit through an unauthenticated API or create a listing PR; no such
  route is documented.

### Sundial

- Route: `https://www.sundialhub.com/`
- Submit command after authentication:

```bash
npx sundial-hub push skills/hermes-tweet --skill-version 0.1.5 --visibility public --categories social-media,automation,developer-tools
```

- Why manual: local `sundial-hub` auth is not configured.
- Before submission, confirm categories and changelog with the operator.
- Do not open a direct `sundial-org/skills` PR unless maintainers document a
  third-party contribution route.

### Skills.Rest

- Route: `https://skills.rest/contribute`
- Submit: `skills/hermes-tweet/SKILL.md` or the public GitHub tree URL.
- Why manual: the published page says GitHub PRs go through
  `github.com/skills-rest/submissions`, but that repository currently returns
  404; the remaining visible routes are email/form review.
- Do not email maintainers or submit a package without operator approval for the
  outbound message, categories, and changelog.

## Local Secret Needed

Real `tweet_read` smoke tests require `XQUIK_API_KEY` in the Hermes runtime.

Do not paste the key into chat, issue bodies, PR bodies, logs, or command text.
Set it locally through an ephemeral environment variable or `~/.hermes/.env`.
After editing `~/.hermes/.env`, run `/reload` in an active Hermes CLI session.
Gateway and cron sessions need a restart or new session.

When `XQUIK_API_KEY` is missing, Hermes should expose only `tweet_explore` from
this plugin. That is expected safe gating.

## Wait For Maintainers

Do not duplicate these routes:

- `aliaihub/awesome-hermes-usecases#2` is open and verified.
- `Karanjot786/agent-skills-cli#11` tracks the single-skill submit 404.
- `skillsgate/skillsgate#8` tracks the macOS arm64 package wrapper failure.
- `diegosouzapw/awesome-omni-skill#5` tracks public submit and browse API 403s.
- `ksimback/hermes-ecosystem#169`, `0xarkstar/awesome-hermes-agent#1`, and
  `codesstar/hermes-skill-atlas#1` are already open routes.
- `philipbankier/awesome-agent-skills#11` already covers the adjacent
  Xquik-dev X/Twitter scraper; wait for maintainer action before proposing a
  second Xquik entry there.

## Adoption-Gated Routes

Some awesome lists require more stars or adoption before submission. Retry only
after Hermes Tweet clears the target's documented threshold.
