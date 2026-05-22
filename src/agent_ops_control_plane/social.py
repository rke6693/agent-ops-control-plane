"""Approval-gated social launch queue generation."""

from __future__ import annotations

import json
import hashlib
from dataclasses import asdict, dataclass
from pathlib import Path

from .artifacts import write_private_text
import re

from .redaction import scan_text
from .risk import Operation, RiskClass, confirmation_phrase


@dataclass(frozen=True)
class SocialDraft:
    draft_id: str
    campaign: str
    channel: str
    account_hint: str
    post_type: str
    copy: str
    asset_prompt_id: str | None
    objective: str
    review_notes: str
    approval_state: str = "draft"
    required_checks: tuple[str, ...] = (
        "secret_scan",
        "manual_preview",
        "exact_typed_confirmation",
        "private_audit_receipt",
    )
    reviewer: str | None = None
    approved_at: str | None = None
    publish_blocked_reason: str = "live publishing disabled in public alpha"
    approval_required: bool = True
    live_publish_enabled: bool = False


KNOWN_ASSET_PROMPT_IDS = {
    "hero-control-room",
    "architecture-map",
    "security-rings",
    "operator-receipt",
    "launch-queue",
    "og-social-card",
}
COPY_PLACEHOLDER_RE = re.compile(r"(?i)(<insert|<url|placeholder|todo|tbd)")

SOCIAL_PUBLISH_OPERATION = Operation(
    "social.publish",
    RiskClass.EXTERNAL_SIDE_EFFECT,
    "Publish content to a live social account.",
)


LAUNCH_DRAFTS: tuple[SocialDraft, ...] = (
    SocialDraft(
        draft_id="aocp-launch-thread-001",
        campaign="v0.1.0-alpha",
        channel="x",
        account_hint="example-operator-account",
        post_type="launch_thread_1",
        copy=(
            "Most AI agent launches prove a model can do one impressive thing. "
            "Agent Ops Control Plane is for the day after: redacted status receipts, "
            "risk classes, typed approvals, secret scans, and local launch queues "
            "for people operating agents."
        ),
        asset_prompt_id="hero-control-room",
        objective="Open the launch thread with the problem and positioning.",
        review_notes="Add repo URL only after the public repo is live.",
    ),
    SocialDraft(
        draft_id="aocp-launch-thread-002",
        campaign="v0.1.0-alpha",
        channel="x",
        account_hint="example-operator-account",
        post_type="launch_thread_2",
        copy=(
            "Thesis: agents need operations, not vibes. If an agent can touch files, "
            "memory, credentials, accounts, or tools, the operator needs to know what "
            "is enabled, what is risky, what changed, and what cannot run without approval."
        ),
        asset_prompt_id="architecture-map",
        objective="State the thesis in a short quotable form.",
        review_notes="Keep this post concise; avoid adding feature bloat.",
    ),
    SocialDraft(
        draft_id="aocp-launch-thread-003",
        campaign="v0.1.0-alpha",
        channel="x",
        account_hint="example-operator-account",
        post_type="launch_thread_3",
        copy=(
            "v0.1.0-alpha ships the small primitives first: agent-ops status, "
            "agent-ops scan, private JSONL audit events, risk-class confirmation "
            "policy, and an approval-gated X launch queue that does not post."
        ),
        asset_prompt_id="security-rings",
        objective="List concrete shipped capabilities.",
        review_notes="Verify the listed capabilities still match the repo before posting.",
    ),
    SocialDraft(
        draft_id="aocp-launch-thread-004",
        campaign="v0.1.0-alpha",
        channel="x",
        account_hint="example-operator-account",
        post_type="launch_thread_4",
        copy=(
            "The social workflow is deliberately boring: draft locally -> scan -> "
            "preview -> approve -> exact typed confirmation -> audit receipt. This "
            "repo stops before live posting; any X API adapter has to prove those gates first."
        ),
        asset_prompt_id=None,
        objective="Defuse unsafe automation concerns before they arise.",
        review_notes="Do not weaken this safety boundary for launch engagement.",
    ),
    SocialDraft(
        draft_id="aocp-launch-thread-005",
        campaign="v0.1.0-alpha",
        channel="x",
        account_hint="example-operator-account",
        post_type="launch_thread_5",
        copy=(
            "The operator receipt is the product proof. In one screen it should answer: "
            "what is enabled, what is redacted, what is high-risk, and what needs human "
            "approval before it can touch the outside world."
        ),
        asset_prompt_id="operator-receipt",
        objective="Explain the operator value in practical terms.",
        review_notes="Pair with a README/status screenshot or generated visual.",
    ),
    SocialDraft(
        draft_id="aocp-launch-thread-006",
        campaign="v0.1.0-alpha",
        channel="x",
        account_hint="example-operator-account",
        post_type="launch_thread_6",
        copy=(
            "Where this should go next: launchd/systemd status adapters, Docker checks, "
            "GitHub release receipts, and a gated X API publisher with duplicate "
            "protection and a kill switch."
        ),
        asset_prompt_id=None,
        objective="Invite useful technical collaboration.",
        review_notes="Use after repo issues are enabled.",
    ),
    SocialDraft(
        draft_id="aocp-launch-thread-007",
        campaign="v0.1.0-alpha",
        channel="x",
        account_hint="example-operator-account",
        post_type="launch_thread_7",
        copy=(
            "If you run local or semi-autonomous agents, clone it, run the status/scan "
            "commands, and open an issue for the adapter you want first. The goal is "
            "simple: make autonomy operable."
        ),
        asset_prompt_id="launch-queue",
        objective="Close with a call for builders and feedback.",
        review_notes="Insert repo URL and one concrete issue/discussion link if available.",
    ),
)


def validate_social_drafts(drafts: tuple[SocialDraft, ...] = LAUNCH_DRAFTS) -> None:
    seen: set[str] = set()
    for draft in drafts:
        if not draft.draft_id:
            raise ValueError("social draft is missing draft_id")
        if draft.draft_id in seen:
            raise ValueError(f"duplicate social draft id: {draft.draft_id}")
        seen.add(draft.draft_id)
        if draft.approval_state != "draft":
            raise ValueError(f"{draft.draft_id} must remain in draft state")
        if draft.approval_required is not True:
            raise ValueError(f"{draft.draft_id} must require approval")
        if draft.live_publish_enabled is not False:
            raise ValueError(f"{draft.draft_id} must not enable live publishing")
        if draft.reviewer is not None or draft.approved_at is not None:
            raise ValueError(f"{draft.draft_id} must not be pre-approved")
        if len(draft.copy) > 280:
            raise ValueError(f"{draft.draft_id} copy exceeds 280 characters")
        if COPY_PLACEHOLDER_RE.search(draft.copy):
            raise ValueError(f"{draft.draft_id} copy contains placeholder text")
        if scan_text(draft.copy, path=draft.draft_id):
            raise ValueError(f"{draft.draft_id} copy contains credential-shaped text")
        if draft.asset_prompt_id and draft.asset_prompt_id not in KNOWN_ASSET_PROMPT_IDS:
            raise ValueError(f"{draft.draft_id} references unknown asset prompt")
        required_checks = {
            "secret_scan",
            "manual_preview",
            "exact_typed_confirmation",
            "private_audit_receipt",
        }
        missing_checks = required_checks.difference(draft.required_checks)
        if missing_checks:
            missing = ", ".join(sorted(missing_checks))
            raise ValueError(f"{draft.draft_id} missing required checks: {missing}")


def draft_to_payload(draft: SocialDraft) -> dict[str, object]:
    payload = asdict(draft)
    payload["content_hash"] = hashlib.sha256(draft.copy.encode("utf-8")).hexdigest()
    payload["requires_confirmation_phrase"] = confirmation_phrase(SOCIAL_PUBLISH_OPERATION)
    return payload


def queue_as_jsonl(drafts: tuple[SocialDraft, ...] = LAUNCH_DRAFTS) -> str:
    validate_social_drafts(drafts)
    return "".join(json.dumps(draft_to_payload(draft), sort_keys=True) + "\n" for draft in drafts)


def write_launch_queue(path: Path) -> Path:
    return write_private_text(path, queue_as_jsonl())
