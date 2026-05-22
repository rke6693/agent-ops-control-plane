import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from agent_ops_control_plane.social import queue_as_jsonl
from agent_ops_control_plane.social import SocialDraft, validate_social_drafts
from agent_ops_control_plane.status import build_status_receipt


class StatusSocialCliTests(unittest.TestCase):
    def test_status_receipt_is_redacted_and_read_only(self):
        receipt = build_status_receipt(Path.cwd())
        self.assertTrue(receipt.read_only)
        self.assertTrue(receipt.redacted)
        self.assertIn("Agent Ops Status", receipt.to_markdown())

    def test_launch_queue_is_approval_gated(self):
        rows = [json.loads(line) for line in queue_as_jsonl().splitlines()]
        self.assertGreaterEqual(len(rows), 4)
        self.assertTrue(all(row["approval_required"] for row in rows))
        self.assertFalse(any(row["live_publish_enabled"] for row in rows))
        self.assertTrue(all(row["approval_state"] == "draft" for row in rows))
        self.assertTrue(all(row["requires_confirmation_phrase"] == "APPROVE SOCIAL.PUBLISH" for row in rows))
        self.assertEqual(len({row["draft_id"] for row in rows}), len(rows))

    def test_launch_queue_rejects_live_publish_enabled(self):
        draft = SocialDraft(
            draft_id="bad",
            campaign="test",
            channel="x",
            account_hint="example-operator-account",
            post_type="bad",
            copy="This should not be live.",
            asset_prompt_id=None,
            objective="test",
            review_notes="test",
            live_publish_enabled=True,
        )
        with self.assertRaises(ValueError):
            validate_social_drafts((draft,))

    def test_launch_queue_rejects_unknown_asset_prompt(self):
        draft = SocialDraft(
            draft_id="bad-asset",
            campaign="test",
            channel="x",
            account_hint="example-operator-account",
            post_type="bad",
            copy="This should not reference an unknown asset.",
            asset_prompt_id="missing-asset",
            objective="test",
            review_notes="test",
        )
        with self.assertRaises(ValueError):
            validate_social_drafts((draft,))

    def test_launch_queue_preview_fixture_is_fresh(self):
        fixture = Path("examples/social_queue/launch_queue.preview.jsonl")
        self.assertTrue(fixture.exists())
        self.assertEqual(fixture.read_text(encoding="utf-8"), queue_as_jsonl())

    def test_cli_status_markdown(self):
        result = subprocess.run(
            [sys.executable, "-m", "agent_ops_control_plane.cli", "status", "--markdown"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("# Agent Ops Status", result.stdout)

    def test_cli_launch_queue_writes_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "queue.jsonl"
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "agent_ops_control_plane.cli",
                    "launch",
                    "queue",
                    "--output",
                    str(output),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0)
            self.assertTrue(output.exists())
            self.assertIn("example-operator-account", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
