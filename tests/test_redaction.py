import tempfile
import unittest
from pathlib import Path

from agent_ops_control_plane.redaction import redact_text, scan_paths, scan_text


class RedactionTests(unittest.TestCase):
    def test_redacts_secret_like_values(self):
        text = "api" + "_key=supersecretvalue123"
        self.assertIn("<redacted", redact_text(text))

    def test_scan_ignores_placeholders(self):
        key = "OPENAI" + "_API_KEY"
        findings = scan_text(f"{key}=placeholder")
        self.assertEqual(findings, [])

    def test_scan_does_not_ignore_non_placeholder_substrings(self):
        for marker in ("test", "example", "sample", "fake", "dummy"):
            with self.subTest(marker=marker):
                findings = scan_text("api" + f"_key=prod-{marker}-secret-1234567890")
                self.assertEqual(len(findings), 1)

    def test_scan_detects_sensitive_key_values(self):
        findings = scan_text("access" + "_token=realvalue123")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].kind, "sensitive-key-value")

    def test_scan_detects_env_style_sensitive_keys(self):
        keys = (
            "OPENAI" + "_API_KEY",
            "X" + "_ACCESS_TOKEN",
            "DATABASE" + "_PASSWORD",
            "SESSION" + "_COOKIE",
        )
        for key in keys:
            with self.subTest(key=key):
                findings = scan_text(f"{key}=realvalue1234567890")
                self.assertEqual(len(findings), 1)

    def test_env_style_placeholder_suppression_is_value_exact(self):
        key = "OPENAI" + "_API_KEY"
        self.assertEqual(scan_text(f"{key}=placeholder"), [])
        findings = scan_text(f"{key}=prod-placeholder-secret-1234567890")
        self.assertEqual(len(findings), 1)

    def test_redacts_env_style_sensitive_keys(self):
        key = "OPENAI" + "_API_KEY"
        self.assertEqual(redact_text(f"{key}=realvalue1234567890"), f"{key}=<redacted>")

    def test_redacts_complete_bearer_header(self):
        key = "Auth" + "orization"
        redacted = redact_text(f"{key}: Bearer abcdef ghijkl")
        self.assertEqual(redacted, f"{key}=<redacted>")

    def test_redacts_complete_cookie_header(self):
        key = "Cook" + "ie"
        name = "ses" + "sion"
        redacted = redact_text(f"{key}: {name}=abcdef; refresh=ghijkl")
        self.assertEqual(redacted, f"{key}=<redacted>")

    def test_scan_does_not_skip_secret_because_line_mentions_example(self):
        value = "ghp_" + "A" * 32
        findings = scan_text(f"example docs accidentally include {value}")
        self.assertEqual(len(findings), 1)

    def test_scan_paths_finds_private_key_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.txt"
            header = "-----BEGIN " + "PRIVATE KEY-----"
            path.write_text(f"{header}\nabc\n", encoding="utf-8")
            findings = scan_paths([path])
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].kind, "private-key")


if __name__ == "__main__":
    unittest.main()
