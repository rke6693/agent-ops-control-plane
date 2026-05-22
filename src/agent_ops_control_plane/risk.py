"""Risk classes and confirmation policy for agent operations."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RiskClass(str, Enum):
    READ_ONLY = "read_only"
    LOCAL_WRITE = "local_write"
    PRIVATE_DATA_ACCESS = "private_data_access"
    CREDENTIAL_SENSITIVE = "credential_sensitive"
    EXTERNAL_SIDE_EFFECT = "external_side_effect"
    DESTRUCTIVE = "destructive"
    FINANCIAL_OR_ACCOUNT_ACTION = "financial_or_account_action"
    UNKNOWN = "unknown"


HIGH_RISK_CLASSES = {
    RiskClass.CREDENTIAL_SENSITIVE,
    RiskClass.EXTERNAL_SIDE_EFFECT,
    RiskClass.DESTRUCTIVE,
    RiskClass.FINANCIAL_OR_ACCOUNT_ACTION,
    RiskClass.UNKNOWN,
}


@dataclass(frozen=True)
class Operation:
    name: str
    risk: RiskClass
    description: str
    confirmation_phrase: str | None = None


DEFAULT_OPERATIONS: tuple[Operation, ...] = (
    Operation("status.read", RiskClass.READ_ONLY, "Read redacted operator status."),
    Operation("artifact.write_private", RiskClass.LOCAL_WRITE, "Write owner-only local receipt."),
    Operation("memory.audit", RiskClass.PRIVATE_DATA_ACCESS, "Read metadata-only memory status."),
    Operation("secrets.configure", RiskClass.CREDENTIAL_SENSITIVE, "Create or update credentials."),
    Operation("social.publish", RiskClass.EXTERNAL_SIDE_EFFECT, "Publish content to a live social account."),
    Operation("repo.delete", RiskClass.DESTRUCTIVE, "Delete repository or artifact data."),
    Operation("account.change", RiskClass.FINANCIAL_OR_ACCOUNT_ACTION, "Change paid account or billing settings."),
)


def requires_typed_confirmation(risk: RiskClass) -> bool:
    return risk in HIGH_RISK_CLASSES


def confirmation_phrase(operation: Operation) -> str:
    if operation.confirmation_phrase:
        return operation.confirmation_phrase
    return f"APPROVE {operation.name.upper()}"


def confirm(operation: Operation, user_input: str) -> bool:
    if not requires_typed_confirmation(operation.risk):
        return True
    return user_input == confirmation_phrase(operation)

