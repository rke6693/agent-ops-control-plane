"""Structured approval audit events."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from .artifacts import append_private_jsonl
from .redaction import redact_text
from .risk import Operation, confirmation_phrase

AuditOutcome = Literal["approved", "denied", "blocked", "skipped", "cancelled"]
SENSITIVE_METADATA_KEYS = (
    "api_key",
    "secret",
    "token",
    "password",
    "credential",
    "authorization",
    "bearer",
    "oauth",
    "access_token",
    "refresh_token",
    "consumer_key",
    "cookie",
    "session",
)


@dataclass(frozen=True)
class AuditEvent:
    event: str
    operation: str
    risk_class: str
    outcome: AuditOutcome
    reason: str
    required_confirmation: str | None
    metadata: dict[str, Any]
    created_at: str


def build_audit_event(
    operation: Operation,
    outcome: AuditOutcome,
    *,
    reason: str,
    metadata: dict[str, Any] | None = None,
) -> AuditEvent:
    clean_metadata = _sanitize_metadata(metadata or {})
    return AuditEvent(
        event="agent_ops.approval",
        operation=operation.name,
        risk_class=operation.risk.value,
        outcome=outcome,
        reason=redact_text(reason),
        required_confirmation=confirmation_phrase(operation),
        metadata=clean_metadata,
        created_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )


def write_audit_event(path: Path, event: AuditEvent) -> Path:
    return append_private_jsonl(path, asdict(event))


def _sanitize_metadata(value: Any) -> Any:
    if isinstance(value, dict):
        sanitized: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key)
            if any(marker in key_text.lower() for marker in SENSITIVE_METADATA_KEYS):
                sanitized[key_text] = "<redacted>"
            else:
                sanitized[key_text] = _sanitize_metadata(item)
        return sanitized
    if isinstance(value, list):
        return [_sanitize_metadata(item) for item in value]
    if isinstance(value, tuple):
        return [_sanitize_metadata(item) for item in value]
    return redact_text(str(value))
