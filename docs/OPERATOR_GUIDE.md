# Operator Guide

## Install Locally

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
```

## Check Status

```bash
agent-ops status --markdown
agent-ops status --json
```

## Generate A Launch Queue

```bash
agent-ops launch queue --output /tmp/agent-ops-launch-queue.jsonl
```

The queue is a local approval-gated artifact. It is not posted anywhere.

## Scan Before Publishing

```bash
agent-ops scan README.md docs examples src tests
```

## Run Tests

```bash
python -m unittest discover -s tests
```

## Public Release Checklist

1. Run tests.
2. Run secret scan.
3. Confirm `.env` is not tracked.
4. Confirm launch queue has `approval_required: true`.
5. Confirm `live_publish_enabled: false`.
6. Review image prompts for brand fit.
7. Review all X drafts manually.
8. Tag release only after docs and examples are clean.

