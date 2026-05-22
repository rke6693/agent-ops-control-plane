# Publication Readiness

## Verdict

Ready for a public alpha repo after an explicit external-publish approval.

## Recommended GitHub Settings

- Visibility: public.
- Default branch: `main`.
- Issues: enabled.
- Discussions: optional.
- Wiki: disabled.
- Actions: enabled.
- Secret scanning: enabled if available.
- Branch protection: enable after initial push.
- CI template: `docs/ci/github-actions-ci.yml`; move to `.github/workflows/`
  only from a GitHub session with `workflow` scope.

## Suggested Repo Description

```text
Local-first safety, reliability, audit, and launch operations tooling for autonomous agents.
```

## Suggested Topics

```text
ai-agents, agent-ops, local-first, ai-safety, observability, security, audit,
developer-tools, autonomous-agents
```

## First Release

Tag:

```text
v0.1.0-alpha
```

Release title:

```text
Agent Ops Control Plane v0.1.0-alpha
```

Release notes:

```text
Initial public alpha with redacted status receipts, secret scanning,
private artifact helpers, risk-class confirmation policy, approval audit
events, launch queue drafts, and public launch documentation.
```

## Pre-Publish Gate

Run:

```bash
python3 -m pip install -e .
python -m unittest discover -s tests
agent-ops scan $(git ls-files)
git status --short
git ls-files -o --exclude-standard
```

Confirm:

- No `.env` file is tracked.
- No generated private artifacts are tracked.
- No private memory or logs are tracked.
- No live X API adapter is presented as active.
- X drafts are marked as drafts.
- `git status --short` shows no unexpected tracked changes.
- `git ls-files -o --exclude-standard` shows no unexpected untracked files.
