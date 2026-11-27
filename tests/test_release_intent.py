#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("release_intent", ROOT / "tools" / "release_intent.py")
assert SPEC and SPEC.loader
release_intent = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = release_intent
SPEC.loader.exec_module(release_intent)


class ReleaseIntentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.name", "Test"], check=True)
        (self.repo / "VERSION").write_text("1.1.1\n", encoding="utf-8")
        (self.repo / "README.md").write_text("initial\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.repo), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-qm", "initial"], check=True)
        self.before = subprocess.check_output(["git", "-C", str(self.repo), "rev-parse", "HEAD"], text=True).strip()

    def commit(self, message: str) -> None:
        subprocess.run(["git", "-C", str(self.repo), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-qm", message], check=True)

    def test_non_release_push_with_unchanged_version_skips_publication(self) -> None:
        (self.repo / "README.md").write_text("docs only\n", encoding="utf-8")
        self.commit("docs")
        self.assertFalse(
            release_intent.should_publish(event="push", before=self.before, repo_root=self.repo)
        )

    def test_version_change_on_push_requests_publication(self) -> None:
        (self.repo / "VERSION").write_text("1.1.2\n", encoding="utf-8")
        self.commit("bump")
        self.assertTrue(
            release_intent.should_publish(event="push", before=self.before, repo_root=self.repo)
        )

    def test_manual_dispatch_requests_publication(self) -> None:
        self.assertTrue(
            release_intent.should_publish(event="workflow_dispatch", before="", repo_root=self.repo)
        )

    def test_unavailable_before_identity_does_not_authorize_publication(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "Cannot determine previous VERSION"):
            release_intent.should_publish(event="push", before="f" * 40, repo_root=self.repo)

    def test_push_without_before_identity_requires_recovery(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "before commit"):
            release_intent.should_publish(event="push", before="", repo_root=self.repo)

    def test_initial_branch_push_requests_publication(self) -> None:
        self.assertTrue(
            release_intent.should_publish(event="push", before="0" * 40, repo_root=self.repo)
        )

    def test_known_absent_version_is_an_introduction(self) -> None:
        (self.repo / "VERSION").unlink()
        self.commit("remove version")
        previous = subprocess.check_output(
            ["git", "-C", str(self.repo), "rev-parse", "HEAD"], text=True
        ).strip()
        (self.repo / "VERSION").write_text("1.1.1\n", encoding="utf-8")
        self.commit("introduce version")
        self.assertTrue(
            release_intent.should_publish(event="push", before=previous, repo_root=self.repo)
        )

    def test_unavailable_comparison_cli_has_no_publish_output(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "release_intent.py"),
             "--event", "push", "--before", "f" * 40, "--repo-root", str(self.repo)],
            text=True, capture_output=True, check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("Cannot determine previous VERSION", result.stderr)


if __name__ == "__main__":
    unittest.main()
