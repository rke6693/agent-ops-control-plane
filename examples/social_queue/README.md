# Social Queue Example

Generate a local approval-gated queue:

```bash
agent-ops launch queue --output /tmp/agent-ops-launch-queue.jsonl
```

The generated rows include:

- `approval_required: true`
- `live_publish_enabled: false`
- account hint only, not credentials
- draft copy only, not API execution

