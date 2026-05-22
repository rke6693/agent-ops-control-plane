# Security Model

Agent Ops Control Plane is designed for local-first agent operations where
accidental external side effects and credential leakage are unacceptable.

## Risk Classes

- `read_only`: status, inventory, and metadata checks.
- `local_write`: local receipts and generated files.
- `private_data_access`: metadata-only access to private stores.
- `credential_sensitive`: creating, updating, forwarding, or inspecting secrets.
- `external_side_effect`: publishing, sending, posting, purchasing, or account
  changes outside the local machine.
- `destructive`: deletion, overwrite, backfill, or history rewrite.
- `financial_or_account_action`: billing, paid-account, trade, transfer, or
  account-permission changes.
- `unknown`: unmapped operations, default restricted.

## Confirmation Rules

High-risk operations require exact typed confirmation. Loose yes/no acceptance
is intentionally not enough.

Example:

```text
APPROVE SOCIAL.PUBLISH
```

Near misses, empty input, default enter, lowercase variants, and typos must be
treated as denied or cancelled.

## Audit Rules

Approval events should record:

- Operation name.
- Risk class.
- Outcome.
- Reason.
- Required confirmation phrase.
- Redacted metadata.
- Timestamp.

Audit files are JSONL and should be owner-only where supported.

## Social/API Boundary

The repo includes X launch drafts and approval-gated queues. It does not post
to X, mutate accounts, send DMs, or modify credentials. A deployment may add an
X API adapter only if it enforces:

- Dry-run by default.
- Exact typed confirmation for each campaign or batch.
- Per-post preview before publish.
- Private audit receipt.
- Rate-limit and duplicate protection.
- Emergency kill switch.

