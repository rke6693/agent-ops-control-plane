# Launch Strategy

## Positioning

Agent Ops Control Plane is the operations layer for builders who are done
shipping fragile agent demos.

Core message:

```text
Agents need operations, not vibes.
```

Promise:

- Make local agents safer to run.
- Produce redacted receipts.
- Gate dangerous actions.
- Audit approvals without leaking secrets.
- Turn launch work into approval-gated queues.

## Audience

- AI engineers building local or semi-autonomous agents.
- Solo founders running operator agents.
- DevRel teams demonstrating safe autonomy.
- Security-conscious builders evaluating agent frameworks.
- Technical creators covering agent infrastructure.

## Launch Sequence

### Pre-Launch

- Publish public repo with clean README and CI.
- Add screenshots or generated visual assets.
- Prepare X launch thread and short demo video outline.
- Prepare one technical blog post.
- Prepare Hacker News and Reddit-safe summaries.

### Launch Day

- Post the launch thread from an operator-approved account after manual approval.
- Pin repo and README visual.
- Publish a short technical writeup.
- Share a demo receipt showing redacted status and approval gating.
- Invite issues around adapters: launchd, systemd, Docker, GitHub, X API.

Launch-day rule:

- Do not post via API until the X API adapter has dry-run receipts, duplicate
  detection, exact typed confirmation, and private audit events.

### Post-Launch

- Ship `v0.1.1` with feedback fixes.
- Add one adapter based on demand.
- Publish a "how to operate your agent safely" article.
- Collect examples from other local agent systems.

## Success Metrics

Activation metrics:

- 3 external clean-clone runs.
- 1 adapter request from a real user.
- 1 feedback issue that includes command output.
- 1 user-generated improvement PR or reproducible bug report.

Distribution metrics:

- 20 X saves/bookmarks.
- 5 meaningful GitHub issues or discussions.
- 3 forks from agent builders.

Safety metrics:

- 0 launch safety corrections.
- 0 secret-scan findings in public artifacts.
- 0 accidental live social/account actions.

## Launch Risks

- Overpromising autonomy.
- Confusion with full agent frameworks.
- Fear of social automation misuse.
- Local-only positioning seeming less exciting than cloud demos.

Mitigation:

- Lead with safety and operator receipts.
- Keep live posting explicitly approval-gated.
- Show concrete examples and tests.
- Avoid claiming production maturity before external users validate it.

## Launch Readiness Gate

The project can go live when all are true:

- README explains the problem in under 30 seconds.
- Tests pass.
- Secret scan passes.
- X drafts contain no live credentials, private facts, or account tokens.
- Image prompts are ready or generated assets have been scanned before commit.
- GitHub repo settings are ready.
- External publishing is explicitly approved in the current run.

## Launch Gate Matrix

| State | Required Commands | Reviewer Action | Allowed External Behavior | Blocking Conditions |
| --- | --- | --- | --- | --- |
| `draft` | `agent-ops launch queue --output /tmp/agent-ops-launch-queue.jsonl` | Review copy, asset pairings, and safety notes | None | Missing draft IDs, placeholders, over-280-char posts, unknown assets, or scan findings |
| `ready` | `agent-ops scan README.md docs examples src tests assets` and `python -m unittest discover -s tests` | Confirm repo URL, image assets, and queue preview | Public repo may be prepared if separately approved | Failed tests, failed scan, dirty worktree, unreviewed generated assets |
| `approved` | Re-run scan over final queue and handoff artifacts | Exact approval for public repo push or specific post batch | Approved repo push; no social posting unless separately approved | No exact approval, missing audit receipt, stale queue hash, missing kill switch for live adapters |
| `published` | Post-publish status and scan receipts | Verify public URL, CI, and launch thread accuracy | Only the explicitly approved action | Unexpected account mutation, duplicate post, failed CI, or safety correction needed |

The current package only implements `draft` queue generation. Live X API
publishing is intentionally out of scope until a future adapter implements the
`ready`, `approved`, and `published` gates with audit receipts.
