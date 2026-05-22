# Contributing

Agent Ops Control Plane is a small public alpha focused on safety and
operations primitives for local or semi-autonomous agent systems.

## Good First Contributions

- Documentation fixes.
- Additional secret-pattern tests.
- New status receipt checks.
- Safer launch queue validation.
- Read-only adapter scaffolds.
- Test fixtures that prove a safety boundary.

## Contribution Rules

- Do not include real credentials, tokens, private keys, logs, memory, account
  identifiers, local absolute user paths, or generated private artifacts.
- Do not add live posting, account mutation, billing, purchasing, trading, or
  transfer behavior without a separate design review and approval gate.
- Keep runtime dependencies minimal. The package currently uses the Python
  standard library at runtime.
- Preserve the default draft-only social workflow.
- Add tests for any behavior that affects redaction, artifact permissions,
  audit events, risk gates, status receipts, or launch queue safety.

## Local Validation

Run before opening a pull request:

```bash
python3 -m compileall src tests
PYTHONPATH=src python3 -m unittest discover -s tests
PYTHONPATH=src python3 -m agent_ops_control_plane.cli scan $(git ls-files)
PYTHONPATH=src python3 -m agent_ops_control_plane.cli status --markdown
git status --short
git ls-files -o --exclude-standard
```

Generated private files, local `.env` files, and build artifacts should remain
untracked.

## Security Reports

Do not put secrets or exploit details in public issues. Follow
[SECURITY.md](SECURITY.md) for reporting guidance.
