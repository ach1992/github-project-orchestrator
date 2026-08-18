#!/usr/bin/env python3
"""Focused regression checks for the bundled read-only repository preflight helper."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = ROOT / "skill" / "scripts" / "repo_preflight.py"

spec = importlib.util.spec_from_file_location("repo_preflight", PREFLIGHT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Unable to load {PREFLIGHT}")
repo_preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(repo_preflight)


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def init_repo(path: Path, marker: str) -> str:
    path.mkdir(parents=True)
    git(path, "init")
    git(path, "config", "user.name", "Preflight Test")
    git(path, "config", "user.email", "preflight@example.invalid")
    (path / "README.md").write_text(f"{marker}\n", encoding="utf-8")
    git(path, "add", "README.md")
    git(path, "commit", "-m", f"init {marker}")
    return git(path, "rev-parse", "HEAD")


def write_sentinel(path: Path, marker: Path) -> None:
    path.write_text(
        "#!/usr/bin/env python3\n"
        "from pathlib import Path\n"
        f"Path({str(marker)!r}).write_text('invoked\\n', encoding='utf-8')\n",
        encoding="utf-8",
    )
    path.chmod(0o755)


def assert_url_sanitization() -> None:
    cases = {
        "https://user:token@example.com/owner/repo.git?token=secret#fragment": "https://example.com/owner/repo.git",
        "git@github.com:owner/repo.git?token=secret#fragment": "github.com:owner/repo.git",
        "ext::opaque-secret-payload": "ext::<redacted-helper-payload>",
    }
    for value, expected in cases.items():
        actual = repo_preflight.sanitize_remote_url(value)
        if actual != expected:
            raise AssertionError(f"sanitize_remote_url({value!r})={actual!r}, expected {expected!r}")
    print("PASS preflight-url-sanitization")


def assert_fsmonitor_not_invoked(root: Path) -> None:
    repo = root / "fsmonitor-repo"
    init_repo(repo, "fsmonitor")
    marker = root / "fsmonitor-invoked"
    sentinel = root / "fsmonitor-sentinel.py"
    write_sentinel(sentinel, marker)
    git(repo, "config", "core.fsmonitor", str(sentinel))

    if repo_preflight.git_supports_boolean_fsmonitor():
        result = repo_preflight.collect(repo)
        if marker.exists():
            raise AssertionError("configured core.fsmonitor executable was invoked")
        if result["dirty"] or not result["dirty_complete"] or not result["status_complete"]:
            raise AssertionError(f"fsmonitor-safe status should remain complete for a simple clean repository: {result}")
    else:
        try:
            repo_preflight.collect(repo)
        except RuntimeError as exc:
            if "core.fsmonitor requires Git 2.36 or newer" not in str(exc):
                raise
        else:
            raise AssertionError("preflight should fail closed when configured fsmonitor cannot be safely suppressed")
        if marker.exists():
            raise AssertionError("configured core.fsmonitor executable was invoked before fail-closed exit")
    print("PASS preflight-fsmonitor-sentinel")


def assert_filters_not_invoked(root: Path) -> None:
    repo = root / "filter-repo"
    init_repo(repo, "filter")
    (repo / ".gitattributes").write_text("*.dat filter=sentinel\n", encoding="utf-8")
    (repo / "tracked.dat").write_text("tracked\n", encoding="utf-8")
    git(repo, "add", ".gitattributes", "tracked.dat")
    git(repo, "commit", "-m", "add filtered path before helper config")

    marker = root / "filter-invoked"
    sentinel = root / "filter-sentinel.py"
    write_sentinel(sentinel, marker)
    git(repo, "config", "filter.sentinel.clean", str(sentinel))
    git(repo, "config", "filter.sentinel.process", str(sentinel))

    result = repo_preflight.collect(repo)
    if marker.exists():
        raise AssertionError("configured clean/process filter executable was invoked")
    if result["dirty_complete"] or result["status_complete"]:
        raise AssertionError(f"tracked executable filters must make exact worktree status incomplete: {result}")
    if result["executable_filter_drivers"] != ["sentinel"]:
        raise AssertionError(f"active executable filter driver was not reported: {result}")
    if not any("clean/process filters" in reason for reason in result["status_incomplete_reasons"]):
        raise AssertionError(f"filter-related incompleteness reason was not reported: {result}")
    print("PASS preflight-filter-sentinel")


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    repo = root / "repo"
    other = root / "other"
    expected_head = init_repo(repo, "primary")
    init_repo(other, "other")

    clean = repo_preflight.collect(repo)
    if Path(clean["repo_root"]) != repo.resolve() or clean["head"] != expected_head:
        raise AssertionError("preflight did not report the explicitly requested repository identity")
    if clean["dirty"] or not clean["dirty_complete"]:
        raise AssertionError(f"simple clean repository was not proven clean: {clean}")
    print("PASS preflight-clean-identity")

    old_git_dir = os.environ.get("GIT_DIR")
    old_work_tree = os.environ.get("GIT_WORK_TREE")
    try:
        os.environ["GIT_DIR"] = str(other / ".git")
        os.environ["GIT_WORK_TREE"] = str(other)
        poisoned = repo_preflight.collect(repo)
    finally:
        if old_git_dir is None:
            os.environ.pop("GIT_DIR", None)
        else:
            os.environ["GIT_DIR"] = old_git_dir
        if old_work_tree is None:
            os.environ.pop("GIT_WORK_TREE", None)
        else:
            os.environ["GIT_WORK_TREE"] = old_work_tree

    if Path(poisoned["repo_root"]) != repo.resolve() or poisoned["head"] != expected_head:
        raise AssertionError("ambient Git identity variables redirected preflight away from the requested repository")
    print("PASS preflight-ambient-git-isolation")

    for name in ("a.txt", "b.txt", "c.txt"):
        (repo / name).write_text(name, encoding="utf-8")
    dirty = repo_preflight.collect(repo, max_status=1)
    if not dirty["dirty"]:
        raise AssertionError("untracked files were not detected as dirty state")
    if dirty["status_total"] < 3 or not dirty["status_truncated"] or len(dirty["status_porcelain"]) != 1:
        raise AssertionError(f"bounded status metadata is inconsistent: {dirty}")
    print("PASS preflight-dirty-bounds")

    assert_fsmonitor_not_invoked(root)
    assert_filters_not_invoked(root)

assert_url_sanitization()
