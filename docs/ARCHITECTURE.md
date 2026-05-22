# Architecture

Agent Ops Control Plane is a portable operations layer for autonomous agent
systems. It does not replace the agent runtime. It wraps the runtime with
status, audit, risk, and launch workflows that can be tested independently.

## Layers

1. Runtime adapter
   - Integrates with the host agent system.
   - Reads status and metadata.
   - Avoids raw logs, prompts, memory, or credentials by default.

2. Redaction layer
   - Detects common credential-shaped values.
   - Redacts secret-like key/value pairs.
   - Supports pre-publication scans for docs, reports, and launch queues.

3. Risk policy layer
   - Classifies operations as read-only, local write, private-data access,
     credential-sensitive, external side effect, destructive, account/financial,
     or unknown.
   - Requires exact typed confirmation for high-risk classes.

4. Audit layer
   - Writes structured JSONL events.
   - Uses private file and directory modes.
   - Records outcomes such as approved, denied, blocked, skipped, and cancelled.

5. Operator receipt layer
   - Produces redacted Markdown and JSON receipts.
   - Keeps receipts useful for handoff without exposing private contents.

6. Launch workflow layer
   - Generates approval-gated social queues.
   - Separates draft generation from live account actions.
   - Leaves X/API publishing to explicit deployment-specific adapters.

## Non-Goals

- Direct social posting.
- Credential storage.
- Private memory mutation.
- Billing/account changes.
- Replacing a full observability stack.

## Adapter Strategy

The initial package ships with generic local helpers. Future adapters should
remain small:

- `launchd` adapter for macOS services.
- `systemd` adapter for Linux services.
- `docker` adapter for container backends.
- `github` adapter for PR and release receipts.
- `x_api` adapter for approval-gated posting.

Every adapter should expose read-only status first, then add high-risk actions
behind typed confirmation and audit logging.

