# Operator Handoff

This file tracks tasks that need a signed-in human account, a local secret, or a
maintainer response before Hermes Tweet can move forward.

## No Package Release Blocker

Hermes Tweet is published, installed, and discoverable across the primary
surfaces already:

- GitHub repository and docs homepage are public.
- PyPI, direct PyPI version JSON, and the simple index expose `0.1.6`.
- piwheels JSON and page expose `0.1.6`.
- SKILLS.re lists Hermes Tweet.
- AgentSkill lists Hermes Tweet and serves the agent install API.
- ClawHub lists Hermes Tweet with clean moderation and current `0.1.6`
  metadata.
- First-party Xquik docs and TweetClaw links are current.
- Awesome Skills lists Hermes Tweet under Integrations & APIs.
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
npx sundial-hub push skills/hermes-tweet --skill-version 0.1.6 --visibility public --categories social-media,automation,developer-tools
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

### SkillDock.io

- Route: `https://skilldock.io/`
- Submit path: authenticated `skilldock skill upload` publish flow, not a
  repo-native listing PR.
- Why manual: publishing requires a SkillDock account token or browser-backed
  login plus namespace ownership.
- Public repo note: `chigwell/skilldock.io` documents CLI upload and install
  flows but does not expose a documented GitHub catalog submission path for
  third-party skills.
- Do not open a repo issue or PR just to request listing. Use the documented
  upload flow only after operator approval for namespace, visibility, tags, and
  release version.

## Local Secret Needed

Real `tweet_read` smoke tests require `XQUIK_API_KEY` in the Hermes runtime.

Do not paste the key into chat, issue bodies, PR bodies, logs, or command text.
Set it locally through an ephemeral environment variable or `~/.hermes/.env`.
If a maintainer has stored the key in macOS Keychain as service
`xquik-api-key` and account `hermes-tweet`, prefer hydrating it only for the
smoke-test process:

```bash
XQUIK_API_KEY="$(security find-generic-password -a hermes-tweet -s xquik-api-key -w)" \
  hermes -z "Use tweet_explore, then read /api/v1/account. Do not call tweet_action." \
  --toolsets hermes-tweet
```

After editing `~/.hermes/.env`, run `/reload` in an active Hermes CLI session.
Gateway and cron sessions need a restart or new session.

When `XQUIK_API_KEY` is missing, Hermes should expose only `tweet_explore` from
this plugin. That is expected safe gating.

## Wait For Maintainers

Do not duplicate these routes:

- `aliaihub/awesome-hermes-usecases#2` is open and verified.
- `bcdev98/recommendation#1` is open. It adds Hermes Tweet to a Hermes Agent
  use-cases repo as a social media and community workflow for tweet search,
  reply reads, trends, monitoring, and action-gated posting.
- `fly-apps/hermes-flyio#1` is open. It adds a general optional-plugin install
  pattern to the Fly.io Hermes deployment example, using Hermes Tweet to show
  plugin installation, Fly secrets, and action-gated X/Twitter workflows.
- `cosmicstack-labs/mercury-agent-skills#1` is open. It adds a full
  `x-twitter-automation` SKILL.md to a Mercury/OpenClaw/Hermes-compatible
  skills registry, with Hermes Tweet referenced as the concrete Hermes
  implementation.
- `mergisi/awesome-hermes-agent#1` is open. It adds Hermes Tweet to the
  repo's explicit Plugins & Extensions section.
- `0xNyk/awesome-hermes-agent#65` is open. That repo requires issue-first
  resource recommendations instead of direct list PRs.
- `muhajirdev/awesome-hermes-agent#2` is open. That repo requires issue-first
  resource suggestions and asks contributors not to submit direct listing PRs.
- `amanning3390/hermeshub#54` is already open for `xquik-x` and
  `hermes-tweet`. Current blocker is an authorization-gated Vercel preview, so
  wait for maintainer action instead of resubmitting.
- `jefferyjob/awesome-hermes-agent-zh#1` is open. It is the Chinese mirror of
  the Hermes awesome list and uses the same issue-first resource recommendation
  flow.
- `zcweah1981/awesome-hermes-agent-zh#5` is open. It suggests adding Hermes
  Tweet to the Chinese Hermes Agent docs site as an X/Twitter plugin or
  workflow reference.
- `xianyu110/awesome-HermesAgent-tutorial#1` is open. It suggests adding
  Hermes Tweet to the Chinese Hermes Agent tutorial as a concrete X/Twitter
  search and automation plugin example.
- `xiangyugongzuoliu/hermes-agent-tutorial#1` is open. It follows that repo's
  issue-only contribution rule and suggests Hermes Tweet as an X/Twitter
  plugin, Skills workflow, and automation-boundary example.
- `jwangkun/hermes-agent-guide#7` is open. It suggests adding Hermes Tweet to
  the Chinese Hermes Agent guide as an X/Twitter search, trend reading, reply
  reading, and action-gated automation plugin example.
- `xiehongyu777/hermes-agent-guide#1` is open. It suggests adding Hermes Tweet
  to the Chinese Hermes source-learning guide as a Tool, Skills, and
  action-gated plugin permissions case study.
- `mudrii/hermes-agent-docs#2` is open. It proposes a small `plugins.md`
  examples section that includes Hermes Tweet among concrete community plugin
  references.
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
