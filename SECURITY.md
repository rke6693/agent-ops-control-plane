# Security Policy

Agent Ops Control Plane is a local-first public alpha. It is designed to help
operators keep agent status, artifact writing, risk gates, and launch queues
reviewable before any live adapter is added.

## Reporting A Vulnerability

Do not paste secrets, tokens, private logs, account identifiers, or exploit
details into a public issue.

Preferred reporting path:

1. Use GitHub private vulnerability reporting or a GitHub Security Advisory if
   it is available for this repository.
2. If private reporting is not available, open a public issue with a short
   non-sensitive summary such as "security report available" and wait for a
   maintainer response.

## Scope

In scope:

- Secret scanning and redaction behavior.
- Private artifact permissions.
- Approval audit event behavior.
- Risk-class and typed-confirmation behavior.
- Draft-only launch queue safety.

Out of scope for this alpha:

- Live social publishing adapters.
- Account, billing, purchase, transfer, or trading actions.
- Private memory systems.
- Provider-specific runtime integrations.
- Third-party service configuration outside this repository.

## Public Repo Hygiene

This repository should not contain:

- Real credentials, API keys, tokens, private keys, or session cookies.
- Private logs, private memory, generated private artifacts, or local caches.
- Workstation-specific absolute paths.
- Account-specific social handles in reusable examples.
- Unreviewed external design candidate links.

Before release, run:

```bash
python3 -m compileall src tests
PYTHONPATH=src python3 -m unittest discover -s tests
PYTHONPATH=src python3 -m agent_ops_control_plane.cli scan $(git ls-files)
PYTHONPATH=src python3 -m agent_ops_control_plane.cli status --markdown
git status --short
git ls-files -o --exclude-standard
```
