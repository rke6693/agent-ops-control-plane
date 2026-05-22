import subprocess
import unittest
from pathlib import Path


TEXT_SUFFIXES = {
    "",
    ".cfg",
    ".example",
    ".ini",
    ".json",
    ".jsonl",
    ".md",
    ".py",
    ".toml",
    ".txt",
    ".yml",
    ".yaml",
}


def tracked_text_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        capture_output=True,
        check=True,
        text=True,
    )
    paths: list[Path] = []
    for raw_path in result.stdout.splitlines():
        path = Path(raw_path)
        if path.suffix.lower() in TEXT_SUFFIXES:
            paths.append(path)
    return paths


class PublicationSafetyTests(unittest.TestCase):
    def test_public_text_has_no_private_project_or_account_markers(self):
        forbidden = (
            "Tech" + "TrendsPulse",
            "Her" + "mes",
            "Tele" + "gram",
            "/Users/" + "agent1",
            "canva" + ".com/d/",
            "design" + ".canva",
        )
        failures: list[str] = []

        for path in tracked_text_files():
            text = path.read_text(encoding="utf-8")
            for marker in forbidden:
                if marker in text:
                    failures.append(f"{path}: contains private/publication marker")

        self.assertEqual([], failures)


if __name__ == "__main__":
    unittest.main()
