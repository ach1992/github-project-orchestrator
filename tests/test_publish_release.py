#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("publish_release", ROOT / "tools" / "publish_release.py")
assert SPEC and SPEC.loader
publish_release = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = publish_release
SPEC.loader.exec_module(publish_release)

SHA = "1" * 40
OTHER_SHA = "2" * 40


class PublishReleaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.old_cwd = os.getcwd()
        os.chdir(self.tmp.name)
        self.addCleanup(os.chdir, self.old_cwd)
        Path("VERSION").write_text("1.1.0-rc.1\n", encoding="utf-8")
        Path("skill.zip").write_bytes(b"zip")
        Path("skill.zip.sha256").write_bytes(b"sum  skill.zip\n")
        self.env = mock.patch.dict(os.environ, {"GH_REPO": "o/r", "GITHUB_SHA": SHA}, clear=False)
        self.env.start()
        self.addCleanup(self.env.stop)

    def metadata(self) -> publish_release.ReleaseMetadata:
        return publish_release.ReleaseMetadata("R1", "v1.1.0-rc.1", False, True)

    def test_mismatched_existing_tag_fails_before_release_lookup(self) -> None:
        with mock.patch.object(publish_release, "resolve_remote_tag_commit", return_value=OTHER_SHA), mock.patch.object(
            publish_release, "get_release_metadata"
        ) as get_release:
            with self.assertRaisesRegex(RuntimeError, "Version/tag collision"):
                publish_release.publish_release()
        get_release.assert_not_called()

    def test_existing_exact_release_requires_exact_assets(self) -> None:
        with mock.patch.object(publish_release, "resolve_remote_tag_commit", return_value=SHA), mock.patch.object(
            publish_release, "get_release_metadata", return_value=self.metadata()
        ), mock.patch.object(publish_release, "verify_release_assets", side_effect=RuntimeError("asset mismatch")):
            with self.assertRaisesRegex(RuntimeError, "asset mismatch"):
                publish_release.publish_release()

    def test_existing_exact_release_is_idempotent(self) -> None:
        with mock.patch.object(publish_release, "resolve_remote_tag_commit", return_value=SHA), mock.patch.object(
            publish_release, "get_release_metadata", return_value=self.metadata()
        ), mock.patch.object(publish_release, "verify_release_assets") as verify_assets, mock.patch.object(
            publish_release, "run_checked"
        ) as run_checked:
            publish_release.publish_release()
        verify_assets.assert_called_once()
        run_checked.assert_not_called()

    def test_missing_tag_is_created_then_release_uses_verify_tag_without_target(self) -> None:
        tag_values = iter([None, SHA, SHA, SHA])
        metadata_values = iter([None, self.metadata()])
        commands: list[list[str]] = []

        def fake_run(args: list[str], *, capture_output: bool = True):
            commands.append(args)
            return subprocess.CompletedProcess(args, 0, "", "")

        with mock.patch.object(publish_release, "resolve_remote_tag_commit", side_effect=lambda tag: next(tag_values)), mock.patch.object(
            publish_release, "create_remote_tag"
        ) as create_tag, mock.patch.object(
            publish_release, "get_release_metadata", side_effect=lambda owner, repo, tag: next(metadata_values)
        ), mock.patch.object(publish_release, "verify_release_assets"), mock.patch.object(
            publish_release, "run_checked", side_effect=fake_run
        ):
            publish_release.publish_release()

        create_tag.assert_called_once_with("o/r", "v1.1.0-rc.1", SHA)
        release_commands = [cmd for cmd in commands if cmd[:3] == ["gh", "release", "create"]]
        self.assertEqual(len(release_commands), 1)
        command = release_commands[0]
        self.assertIn("--verify-tag", command)
        self.assertIn("--prerelease", command)
        self.assertNotIn("--target", command)

    def test_tag_creation_race_must_reconcile_to_same_sha(self) -> None:
        with mock.patch.object(publish_release, "resolve_remote_tag_commit", return_value=None), mock.patch.object(
            publish_release,
            "create_remote_tag",
            side_effect=subprocess.CalledProcessError(1, ["gh", "api"]),
        ), mock.patch.object(publish_release, "assert_tag_identity", side_effect=RuntimeError("wrong sha")), mock.patch.object(
            publish_release, "get_release_metadata"
        ) as get_release:
            with self.assertRaisesRegex(RuntimeError, "wrong sha"):
                publish_release.publish_release()
        get_release.assert_not_called()


if __name__ == "__main__":
    unittest.main()
