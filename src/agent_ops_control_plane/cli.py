"""Command line interface for Agent Ops Control Plane."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .redaction import scan_paths
from .social import write_launch_queue
from .status import build_status_receipt


def _cmd_status(args: argparse.Namespace) -> int:
    receipt = build_status_receipt(Path.cwd())
    if args.json:
        print(receipt.to_json())
    else:
        print(receipt.to_markdown() if args.markdown else receipt.to_json())
    return 0 if receipt.status in {"pass", "warn"} else 1


def _cmd_scan(args: argparse.Namespace) -> int:
    findings = scan_paths([Path(item) for item in args.paths])
    if args.json:
        print(json.dumps([finding.__dict__ for finding in findings], indent=2, sort_keys=True))
    elif findings:
        for finding in findings:
            print(f"{finding.path}:{finding.line}: {finding.kind}")
    else:
        print("secret scan passed: 0 findings")
    return 1 if findings else 0


def _cmd_launch_queue(args: argparse.Namespace) -> int:
    path = write_launch_queue(Path(args.output))
    print(f"wrote approval-gated launch queue: {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-ops")
    subparsers = parser.add_subparsers(dest="command", required=True)

    status = subparsers.add_parser("status", help="Print a redacted operator status receipt.")
    status.add_argument("--json", action="store_true", help="Print JSON.")
    status.add_argument("--markdown", action="store_true", help="Print Markdown.")
    status.set_defaults(func=_cmd_status)

    scan = subparsers.add_parser("scan", help="Scan files or directories for credential-shaped values.")
    scan.add_argument("paths", nargs="+")
    scan.add_argument("--json", action="store_true")
    scan.set_defaults(func=_cmd_scan)

    launch = subparsers.add_parser("launch", help="Launch workflow helpers.")
    launch_sub = launch.add_subparsers(dest="launch_command", required=True)
    queue = launch_sub.add_parser("queue", help="Write an approval-gated social launch queue.")
    queue.add_argument("--output", required=True)
    queue.set_defaults(func=_cmd_launch_queue)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

