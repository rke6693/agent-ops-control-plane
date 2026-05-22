"""Redaction and secret-pattern scanning helpers."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |)?PRIVATE KEY-----")),
    ("openai-key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{24,}\b")),
    ("anthropic-key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{24,}\b")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{30,}\b")),
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{30,}\b")),
    ("aws-access-key", re.compile(r"\bA(?:KIA|SIA)[A-Z0-9]{16}\b")),
    ("telegram-bot-token", re.compile(r"\b\d{8,12}:[A-Za-z0-9_-]{30,}\b")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
)

PLACEHOLDER_VALUE_RE = re.compile(
    r"(?i)^(?:<?redacted>?|placeholder|example|dummy|fake|test|token-?value|not-a-secret|sample|)$"
)

KEY_VALUE_RE = re.compile(
    r"(?i)\b([A-Za-z0-9_-]{3,})\s*[:=]\s*([^\n\r#]+)"
)
SENSITIVE_KEY_RE = re.compile(
    r"(?i)(?:^|[_-])(?:api[_-]?key|secret|token|password|credential|authorization|bearer|oauth|access[_-]?token|refresh[_-]?token|consumer[_-]?key|cookie|session)(?:$|[_-])"
)


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    kind: str


def redact_text(value: str) -> str:
    """Redact common secret-shaped values while preserving useful context."""

    redacted = value
    for kind, pattern in SECRET_PATTERNS:
        redacted = pattern.sub(f"<redacted:{kind}>", redacted)

    def _replace_key_value(match: re.Match[str]) -> str:
        key = match.group(1)
        raw = match.group(2)
        if not is_sensitive_key(key):
            return match.group(0)
        if is_placeholder_value(raw):
            return match.group(0)
        return f"{key}=<redacted>"

    return KEY_VALUE_RE.sub(_replace_key_value, redacted)


def scan_text(text: str, *, path: str = "<memory>") -> list[Finding]:
    findings: list[Finding] = []
    for line_no, line in enumerate(text.splitlines(), 1):
        for kind, pattern in SECRET_PATTERNS:
            if any(not is_placeholder_value(match.group(0)) for match in pattern.finditer(line)):
                findings.append(Finding(path=path, line=line_no, kind=kind))
        for match in KEY_VALUE_RE.finditer(line):
            if not is_sensitive_key(match.group(1)):
                continue
            value = match.group(2).strip().strip("\"'")
            if value and not is_placeholder_value(value):
                findings.append(Finding(path=path, line=line_no, kind="sensitive-key-value"))
    return findings


def iter_text_files(paths: Iterable[Path]) -> Iterable[Path]:
    for path in paths:
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file() and not _is_probably_binary(child):
                    yield child
        elif path.is_file() and not _is_probably_binary(path):
            yield path


def scan_paths(paths: Iterable[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_text_files(paths):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        findings.extend(scan_text(text, path=str(path)))
    return findings


def _is_probably_binary(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            chunk = handle.read(2048)
    except OSError:
        return True
    return b"\0" in chunk


def is_placeholder_value(value: str) -> bool:
    return bool(PLACEHOLDER_VALUE_RE.fullmatch(value.strip().strip("\"'")))


def is_sensitive_key(key: str) -> bool:
    normalized = key.strip().strip("\"'").lower().replace("-", "_")
    if normalized.endswith("_patterns") or normalized.endswith("_sensitive"):
        return False
    if normalized in {"credential_sensitive"}:
        return False
    return bool(SENSITIVE_KEY_RE.search(normalized))
