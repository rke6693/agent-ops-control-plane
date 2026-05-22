import json
import tempfile
import unittest
from pathlib import Path

from agent_ops_control_plane.audit import build_audit_event, write_audit_event
from agent_ops_control_plane.risk import (
    Operation,
    RiskClass,
    confirm,
    confirmation_phrase,
    requires_typed_confirmation,
)


class RiskAuditTests(unittest.TestCase):
    def test_read_only_does_not_require_typed_confirmation(self):
        op = Operation("status.read", RiskClass.READ_ONLY, "Read status.")
        self.assertFalse(requires_typed_confirmation(op.risk))
        self.assertTrue(confirm(op, ""))

    def test_external_side_effect_requires_exact_confirmation(self):
        op = Operation("social.publish", RiskClass.EXTERNAL_SIDE_EFFECT, "Post to X.")
        self.assertTrue(requires_typed_confirmation(op.risk))
        self.assertFalse(confirm(op, "yes"))
        self.assertFalse(confirm(op, confirmation_phrase(op).lower()))
        self.assertTrue(confirm(op, confirmation_phrase(op)))

    def test_audit_event_redacts_metadata(self):
        op = Operation("social.publish", RiskClass.EXTERNAL_SIDE_EFFECT, "Post to X.")
        event = build_audit_event(
            op,
            "blocked",
            reason="missing approval",
            metadata={"nested": {"access_token": "supersecretvalue123"}},
        )
        self.assertEqual(event.metadata["nested"]["access_token"], "<redacted>")

    def test_audit_reason_redacts_complete_authorization_header(self):
        op = Operation("social.publish", RiskClass.EXTERNAL_SIDE_EFFECT, "Post to X.")
        key = "Auth" + "orization"
        event = build_audit_event(
            op,
            "blocked",
            reason=f"{key}: Bearer abcdef ghijkl",
        )
        self.assertEqual(event.reason, f"{key}=<redacted>")

    def test_write_audit_event_jsonl(self):
        op = Operation("social.publish", RiskClass.EXTERNAL_SIDE_EFFECT, "Post to X.")
        event = build_audit_event(op, "skipped", reason="dry run only")
        with tempfile.TemporaryDirectory() as tmp:
            path = write_audit_event(Path(tmp) / "audit" / "events.jsonl", event)
            payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["operation"], "social.publish")
        self.assertEqual(payload["outcome"], "skipped")


if __name__ == "__main__":
    unittest.main()
