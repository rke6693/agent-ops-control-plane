# Technical Summary

Agent Ops Control Plane packages practical patterns from a real local-agent
hardening project as a public-ready operations layer for autonomous agent
systems.

## Problem

Agent systems often gain tools, memory, credentials, and external integrations
before they gain operating discipline. That creates predictable failure modes:

- Unclear runtime status.
- Unsafe tool execution.
- Secret leakage in logs or reports.
- No durable approval audit.
- Private-state growth without deletion readiness.
- Social/account automation without approval gates.
- No repeatable validation cycle.

## Solution

This package provides small, testable primitives that can sit beside any agent
runtime:

- Redaction and secret scans.
- Owner-only local artifact writing.
- JSONL approval audit events.
- Risk classes and typed confirmation policy.
- Redacted status receipts.
- Approval-gated launch queue generation.
- Public launch docs and image-prompt assets.

## Current Modules

- `redaction.py`: detects credential-shaped values and redacts sensitive
  key/value strings.
- `artifacts.py`: writes private text and JSONL artifacts with owner-only modes.
- `risk.py`: defines risk classes and exact typed confirmation behavior.
- `audit.py`: builds and writes redacted approval audit events.
- `status.py`: produces redacted Markdown/JSON operator receipts.
- `social.py`: generates approval-gated X launch draft queues.
- `cli.py`: exposes status, scan, and launch queue commands.

## Current Commands

```bash
agent-ops status --markdown
agent-ops status --json
agent-ops scan README.md docs examples src tests assets
agent-ops launch queue --output /tmp/agent-ops-launch-queue.jsonl
```

## Validation Commands

The repository uses only the Python standard library at runtime.

From an activated editable install:

```bash
python -m compileall src tests
python -m unittest discover -s tests
agent-ops status --markdown
agent-ops launch queue --output /tmp/agent-ops-launch-queue.jsonl
agent-ops scan $(git ls-files)
```

Expected result:

- Compile passes.
- Unit tests pass.
- Status receipt is redacted and read-only.
- Launch queue rows are approval-gated and not live-publishable.
- Secret scan reports 0 findings.
- Generated private launch queue files use owner-only mode where supported.
- GitHub Actions CI is provided as `docs/ci/github-actions-ci.yml`; activating
  it requires a GitHub token/session with `workflow` scope.

## Public Readiness

This repo is suitable for a first public alpha after:

1. GitHub repo creation.
2. First commit and CI run.
3. Optional generated visual assets added to `assets/`.
4. Final README screenshot or status receipt image.
5. Manual review of X launch drafts.

## What Is Intentionally Not Included

- Private operator memory.
- Private logs.
- Credentials or tokens.
- Live X API posting.
- Messaging delivery.
- Docker mutation.
- Account or billing actions.
- Workstation-specific launchd configuration.

## Best Public Framing

Agent Ops Control Plane should be presented as an operations and safety layer,
not a full agent framework:

```text
Agents need operations, not vibes.
```
