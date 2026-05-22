# Agent Ops Control Plane v0.1.0-alpha

Initial public alpha for local-first agent operations.

## Included

- Redacted operator status receipts.
- Secret-pattern scanner for generated reports and launch artifacts.
- Private-by-default local artifact helpers.
- Structured JSONL approval audit events.
- Risk classes and exact typed confirmation policy.
- Approval-gated social launch queue scaffolding.
- Public Image 2 launch asset bundle and prompt pack.
- Security policy, contribution guide, issue templates, PR template, and
  Dependabot configuration.

## Safe Defaults

- No live social posting adapter.
- No account mutation.
- No credential printing.
- No private memory mutation.
- No provider, Docker, billing, purchase, trading, or transfer side effects.

## Validation

```bash
python3 -m compileall src tests
PYTHONPATH=src python3 -m unittest discover -s tests
PYTHONPATH=src python3 -m agent_ops_control_plane.cli scan $(git ls-files)
PYTHONPATH=src python3 -m agent_ops_control_plane.cli status --markdown
PYTHONPATH=src python3 -m agent_ops_control_plane.cli launch queue --output /tmp/agent-ops-launch-queue.jsonl
```

## Known Limitations

- CI workflow is still provided as a template under `docs/ci/` until it can be
  activated from a GitHub session with workflow scope.
- The package is an operations layer, not a full agent framework.
- Live adapters should start as read-only or dry-run scaffolds and only move to
  external actions after explicit approval gates are implemented.
