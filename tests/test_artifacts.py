import os
import stat
import tempfile
import unittest
from pathlib import Path

from agent_ops_control_plane.artifacts import append_private_jsonl, write_private_text


class ArtifactTests(unittest.TestCase):
    def test_private_text_permissions_under_permissive_umask(self):
        with tempfile.TemporaryDirectory() as tmp:
            old_umask = os.umask(0)
            try:
                path = write_private_text(Path(tmp) / "nested" / "receipt.txt", "ok\n")
            finally:
                os.umask(old_umask)

            self.assertEqual(stat.S_IMODE(path.parent.stat().st_mode), 0o700)
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)

    def test_private_jsonl_permissions_under_permissive_umask(self):
        with tempfile.TemporaryDirectory() as tmp:
            old_umask = os.umask(0)
            try:
                path = append_private_jsonl(Path(tmp) / "audit" / "events.jsonl", {"ok": True})
            finally:
                os.umask(old_umask)

            self.assertEqual(stat.S_IMODE(path.parent.stat().st_mode), 0o700)
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
            self.assertIn('"ok":true', path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

