"""Private-by-default artifact helpers."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


PRIVATE_DIR_MODE = 0o700
PRIVATE_FILE_MODE = 0o600


def ensure_private_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(path, PRIVATE_DIR_MODE)
    except PermissionError:
        pass
    return path


def write_private_text(path: Path, text: str) -> Path:
    ensure_private_dir(path.parent)
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    fd = os.open(path, flags, PRIVATE_FILE_MODE)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(text)
    try:
        os.chmod(path, PRIVATE_FILE_MODE)
    except PermissionError:
        pass
    return path


def append_private_jsonl(path: Path, payload: dict[str, Any]) -> Path:
    ensure_private_dir(path.parent)
    flags = os.O_WRONLY | os.O_CREAT | os.O_APPEND
    fd = os.open(path, flags, PRIVATE_FILE_MODE)
    with os.fdopen(fd, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True, separators=(",", ":")))
        handle.write("\n")
    try:
        os.chmod(path, PRIVATE_FILE_MODE)
    except PermissionError:
        pass
    return path

