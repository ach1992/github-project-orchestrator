#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

ZERO_SHA = "0" * 40


def current_version(repo_root: Path) -> str:
    return (repo_root / "VERSION").read_text(encoding="utf-8").strip()


def version_at(ref: str, repo_root: Path) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(repo_root), "show", f"{ref}:VERSION"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def should_publish(*, event: str, before: str, repo_root: Path) -> bool:
    if event == "workflow_dispatch":
        return True
    if event != "push":
        return False
    if not before or before == ZERO_SHA:
        return True

    previous = version_at(before, repo_root)
    if previous is None:
        # Fail safe toward publication validation rather than silently skipping
        # a release when the comparison identity is unavailable.
        return True
    return previous != current_version(repo_root)


def main() -> int:
    parser = argparse.ArgumentParser(description="Decide whether this main-branch event intends a release.")
    parser.add_argument("--event", required=True)
    parser.add_argument("--before", default="")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    publish = should_publish(
        event=args.event,
        before=args.before,
        repo_root=Path(args.repo_root).resolve(),
    )
    print("true" if publish else "false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
