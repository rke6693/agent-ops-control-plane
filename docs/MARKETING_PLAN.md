# Marketing Plan

## Narrative

Most agent launches show a clever task. Agent Ops Control Plane shows the
boring-but-critical layer that makes those agents operable: status, redaction,
confirmation, audit, incident receipts, and launch queues.

## Taglines

- Agents need operations, not vibes.
- The safety layer for local-first agents.
- Redacted receipts, approval gates, and audit trails for autonomous systems.
- Stop shipping agent demos. Start operating agent systems.

## Channels

- X or another social channel via an operator-approved account, approval-gated.
- GitHub README and releases.
- Technical blog post.
- Hacker News "Show HN" after repo polish.
- Reddit communities where self-promotion is allowed and useful.
- Dev.to or Medium mirror for the operator guide.

## Content Pillars

1. Agent safety.
2. Local-first operations.
3. Redacted observability.
4. Approval gates for autonomy.
5. Practical founder/operator workflows.

## Launch Assets

- Hero visual: local agent control room.
- Architecture visual: agent runtime with ops control plane around it.
- Security visual: risk classes and confirmation gates.
- Status receipt screenshot.
- X launch thread.
- Short demo GIF/video: scan, status, launch queue.

See `docs/BRAND_ASSET_BRIEF.md` for filenames, alt text, and acceptance
criteria.

## Asset Priority

1. README hero image:
   `assets/public/agent-ops-control-plane-hero-1600x900.png`.
2. Architecture graphic:
   `assets/public/agent-ops-architecture-map-1600x1000.png`.
3. Operator receipt visual:
   `assets/public/agent-ops-status-receipt-cli-1694x929.png`.
4. X thread card image:
   `assets/public/agent-ops-og-image-1200x630.png`.
5. Short terminal demo GIF:
   `assets/public/agent-ops-demo-status-scan-queue.gif`.

The repo can go public without final image binaries, but the first public push
should include the prompt pack and asset checklist. The first marketing push
should wait until at least the README hero image and one status receipt visual
exist.

## Demo Script

1. Show a raw agent system with no receipt.
2. Run `agent-ops status --markdown`.
3. Show secret scan passing.
4. Generate social launch queue.
5. Show queue is approval-gated and not live-posting.
6. Explain how adapters can add live actions safely.

## First Blog Outline

Title:

```text
Agents Need Operations, Not Vibes
```

Sections:

1. Agent demos are not agent systems.
2. The minimum viable operations layer.
3. Risk classes and typed confirmations.
4. Why redacted receipts matter.
5. Launch queues without posting bots.
6. What the alpha includes.
7. What adapters should come next.
