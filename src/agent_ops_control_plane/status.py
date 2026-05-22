"""Redacted operator status receipts."""

from __future__ import annotations

import json
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal


@dataclass(frozen=True)
class Check:
    status: Literal["pass", "warn", "fail"]
    name: str
    message: str


@dataclass(frozen=True)
class StatusReceipt:
    status: Literal["pass", "warn", "fail"]
    generated_at: str
    read_only: bool
    redacted: bool
    checks: list[Check]

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True)

    def to_markdown(self) -> str:
        lines = [
            "# Agent Ops Status",
            "",
            f"- Status: `{self.status.upper()}`",
            f"- Read only: `{str(self.read_only).lower()}`",
            f"- Redacted: `{str(self.redacted).lower()}`",
            f"- Checks: `{len(self.checks)}`",
            "",
            "## Checks",
            "",
        ]
        for check in self.checks:
            lines.append(f"- `{check.status.upper()}` `{check.name}`: {check.message}")
        return "\n".join(lines) + "\n"


def build_status_receipt(repo_root: Path | None = None) -> StatusReceipt:
    root = repo_root or Path.cwd()
    checks = [
        Check("pass", "repo.root", f"Using repository `{root.name}`."),
        Check("pass", "secret.output", "Status receipt contains metadata only."),
    ]
    if shutil.which("git"):
        checks.append(Check("pass", "tool.git", "git is available."))
    else:
        checks.append(Check("warn", "tool.git", "git is not available on PATH."))
    if (root / ".env").exists():
        checks.append(Check("warn", "env.local", ".env exists locally and must not be committed."))
    else:
        checks.append(Check("pass", "env.local", "No local .env file found."))

    worst = "pass"
    if any(check.status == "fail" for check in checks):
        worst = "fail"
    elif any(check.status == "warn" for check in checks):
        worst = "warn"

    return StatusReceipt(
        status=worst,
        generated_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        read_only=True,
        redacted=True,
        checks=checks,
    )

