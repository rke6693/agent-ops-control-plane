# X API Autonomy Gates

This document defines the required gates before any live social/X API posting
adapter is allowed to publish.

## Current State

- Draft generation is supported.
- Local JSONL launch queue generation is supported.
- Live publish is not implemented.
- No X API calls are made by this repo.

## Required Publish Gates

1. Credentials are loaded from a private deployment store, not repo files.
2. `agent-ops scan` passes over the post batch and receipts.
3. Each post has a stable ID.
4. Each post has a preview receipt.
5. Each post has `approval_required: true`.
6. The batch requires exact typed confirmation.
7. The adapter writes a private audit event before and after publishing.
8. Duplicate detection prevents reposting the same stable ID.
9. Rate-limit handling prevents runaway posting.
10. A kill switch can disable live posting immediately.
11. Queue validation proves every draft is still `approval_state: draft` before
    live publishing code is introduced.
12. The publishing adapter refuses rows with `live_publish_enabled: false`.

## Required Confirmation Phrase

```text
APPROVE SOCIAL.PUBLISH
```

## Explicitly Excluded

- Spam.
- Mass DMs.
- Reply automation without review.
- Impersonation.
- Engagement bait loops.
- Paid promotion without disclosure.
- Posting secrets, private data, or raw internal logs.

## Recommended Future Adapter Flow

```text
drafts -> secret scan -> preview -> approval -> dry-run receipt -> typed confirmation -> publish -> audit receipt
```

Until this exists, Agent Ops should treat X as a draft-and-approval channel
only.

## Current Queue Invariants

The public alpha launch queue enforces:

- unique non-empty `draft_id`
- `approval_required: true`
- `approval_state: draft`
- `live_publish_enabled: false`
- no prefilled reviewer or approval timestamp
- post copy under 280 characters
- no credential-shaped content in post copy
- known image prompt IDs only
- required secret-scan and typed-confirmation checks
