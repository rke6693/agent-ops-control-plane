# X Launch Drafts

Account hint: example-operator-account

These posts are drafts. They are not posted by this repo.

## Launch Thread

1.

Most AI agent launches prove a model can do one impressive thing. Agent Ops
Control Plane is for the day after: redacted status receipts, risk classes,
typed approvals, secret scans, and local launch queues for people operating
agents.

2.

Thesis: agents need operations, not vibes. If an agent can touch files, memory,
credentials, accounts, or tools, the operator needs to know what is enabled,
what is risky, what changed, and what cannot run without approval.

3.

v0.1.0-alpha ships the small primitives first: `agent-ops status`,
`agent-ops scan`, private JSONL audit events, risk-class confirmation policy,
and an approval-gated X launch queue that does not post.

4.

The social workflow is deliberately boring: draft locally -> scan -> preview ->
approve -> exact typed confirmation -> audit receipt. This repo stops before
live posting; any X API adapter has to prove those gates first.

5.

The operator receipt is the product proof. In one screen it should answer:
what is enabled, what is redacted, what is high-risk, and what needs human
approval before it can touch the outside world.

6.

Where this should go next: launchd/systemd status adapters, Docker checks,
GitHub release receipts, and a gated X API publisher with duplicate protection
and a kill switch.

7.

If you run local or semi-autonomous agents, clone it, run the status/scan
commands, and open an issue for the adapter you want first.

Repo: <insert GitHub URL>

## Standalone Posts

Agents need operations, not vibes.

Agent Ops Control Plane gives local-first agents redacted receipts, approval
gates, audit trails, and launch queues that do not post without explicit
approval.

---

If your agent can touch credentials, accounts, files, or memory, it needs more
than prompts.

It needs risk classes, typed confirmation, private audit trails, and secret
scans.

That is what Agent Ops Control Plane packages.

---

Shipping an agent demo is easy.

Operating an agent system is the hard part.

Agent Ops Control Plane focuses on the unglamorous pieces that keep autonomy
usable: status, redaction, approvals, audit, and incident receipts.

---

The safest social automation starts as non-automation:

draft -> scan -> preview -> approve -> typed confirmation -> audit -> publish

Agent Ops Control Plane currently stops at drafts and queues. That is
intentional.
