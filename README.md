# Agent Ops Control Plane

Local-first safety, reliability, approval-audit, and launch-operations tooling
for autonomous agent systems.

> Agents need operations, not vibes.

Agent Ops Control Plane packages practical operating patterns from a real
local-agent hardening project: redacted status receipts, risk gates, private
artifacts, audit events, and approval-gated launch queues. It is designed for
builders who need agent systems that can be operated, reviewed, and improved
repeatedly instead of shipped as fragile demos.

## Why This Exists

Most agent frameworks focus on getting a model to do something impressive once.
The harder problem starts after that:

- What tools are enabled?
- Which actions require approval?
- Did the operator get a redacted receipt?
- Did a generated report leak secrets?
- Can launch content be queued without becoming a posting bot?

Agent Ops Control Plane gives those concerns a small, testable home.

## What It Provides

- Redacted operator status receipts.
- Private-by-default artifact helpers.
- Structured approval audit events.
- Risk-class policy for tool and workflow decisions.
- Secret-pattern scanning for generated reports and launch artifacts.
- Approval-gated social launch queue scaffolding.
- Public launch strategy, image-prompt pack, and X post drafts.

## Safe Defaults

- No live social posting.
- No account mutation.
- No credential printing.
- No private memory mutation.
- No Docker, provider, or external API side effects.
- All generated private artifacts use owner-only permissions where the platform
  supports them.

## Quickstart

```bash
cd agent-ops-control-plane
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
agent-ops status --markdown
agent-ops launch queue --output /tmp/agent-ops-launch-queue.jsonl
agent-ops scan README.md docs examples
python -m unittest discover -s tests
```

Example status receipt:

```text
# Agent Ops Status

- Status: `PASS`
- Read only: `true`
- Redacted: `true`
```

Example approval-gated launch queue row:

```json
{
  "approval_required": true,
  "channel": "x",
  "live_publish_enabled": false,
  "post_type": "launch_thread_1"
}
```

## Public Positioning

Agent Ops Control Plane is not another agent framework. It is an operations
layer for making agent frameworks safer to run:

1. Know what is enabled.
2. Gate what is dangerous.
3. Audit decisions without leaking secrets.
4. Produce operator receipts.
5. Launch with approval-gated content workflows.

## Repository Map

```text
src/agent_ops_control_plane/   Portable Python package
tests/                         Stdlib unittest coverage
docs/                          Public architecture and launch strategy
examples/                      Example configs and social queues
assets/prompts/                ChatGPT Image 2 prompt pack
```

## Launch Materials

- Technical summary: [docs/TECHNICAL_SUMMARY.md](docs/TECHNICAL_SUMMARY.md)
- Launch strategy: [docs/LAUNCH_STRATEGY.md](docs/LAUNCH_STRATEGY.md)
- Marketing plan: [docs/MARKETING_PLAN.md](docs/MARKETING_PLAN.md)
- X launch drafts: [docs/X_LAUNCH_DRAFTS.md](docs/X_LAUNCH_DRAFTS.md)
- X API autonomy gates: [docs/API_AUTONOMY_GATES.md](docs/API_AUTONOMY_GATES.md)
- Image prompt pack: [assets/prompts/chatgpt-image-2-prompts.md](assets/prompts/chatgpt-image-2-prompts.md)
- Publication checklist: [docs/PUBLICATION_READINESS.md](docs/PUBLICATION_READINESS.md)
- GitHub Actions CI template: [docs/ci/github-actions-ci.yml](docs/ci/github-actions-ci.yml)

## Important Boundary

This repo intentionally does not include private operator runtime data, raw logs,
credentials, private memory, messaging identifiers, X API tokens, or workstation
specific launchd plists. Any live social or account automation must be layered
behind an explicit approval gate in the operator's own deployment.

## Current Public Alpha Scope

This alpha is intentionally narrow:

- It provides operations primitives.
- It proves those primitives with tests.
- It prepares launch content safely.
- It does not claim to be a full observability platform or autonomous-agent
  runtime.

## Limitations

- No live social posting adapter is included.
- No provider-specific runtime adapter is included yet.
- No memory-content inspection or mutation is included.
- No full observability backend is included.
- No account, billing, purchase, trade, or transfer actions are supported.

## Release Readiness

Before publishing or tagging a release:

```bash
python -m pip install -e .
agent-ops scan $(git ls-files)
python -m unittest discover -s tests
git status --short
git ls-files -o --exclude-standard
```

Do not publish if generated private artifacts, local `.env` files, secrets,
private memory, or live account automation adapters are present.

The CI workflow is stored as a template under `docs/ci/`. Move it to
`.github/workflows/ci.yml` only from a GitHub token/session with `workflow`
scope.
