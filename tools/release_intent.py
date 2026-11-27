#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
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
    if result.returncode == 0:
        return result.stdout.strip()

    # A known commit without VERSION is an introduction, not an unreadable
    # comparison. Do not turn missing history or a corrupt blob into intent.
    tree = subprocess.run(
        ["git", "-C", str(repo_root), "ls-tree", "--name-only", ref, "--", "VERSION"],
        text=True,
        capture_output=True,
        check=False,
    )
    if tree.returncode == 0 and not tree.stdout.strip():
        return None
    detail = result.stderr.strip() or tree.stderr.strip() or "comparison unavailable"
    raise RuntimeError(
        f"Cannot determine previous VERSION at {ref}: {detail}. "
        "Recover the comparison commit or use workflow_dispatch for an explicit release attempt."
    )


def should_publish(*, event: str, before: str, repo_root: Path) -> bool:
    if event == "workflow_dispatch":
        return True
    if event != "push":
        return False
    if before == ZERO_SHA:
        return True
    if not before:
        raise RuntimeError("Push release intent requires the event's before commit; recover that identity.")

    previous = version_at(before, repo_root)
    if previous is None:
        return True
    return previous != current_version(repo_root)


def main() -> int:
    parser = argparse.ArgumentParser(description="Decide whether this main-branch event intends a release.")
    parser.add_argument("--event", required=True)
    parser.add_argument("--before", default="")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    try:
        publish = should_publish(
            event=args.event,
            before=args.before,
            repo_root=Path(args.repo_root).resolve(),
        )
    except (OSError, RuntimeError) as exc:
        print(f"Release intent could not be determined: {exc}", file=sys.stderr)
        return 1
    print("true" if publish else "false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
