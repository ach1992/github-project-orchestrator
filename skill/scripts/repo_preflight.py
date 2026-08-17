#!/usr/bin/env python3
"""Conservative read-only Git repository preflight for github-project-orchestrator."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

# Ambient Git variables can redirect repository/worktree/object/index/config identity.
# Preflight must inspect the repository explicitly supplied with -C, not inherited state.
GIT_ENV_EXACT_BLOCKLIST = {
    # Repository-local identity/storage overrides (see `git rev-parse --local-env-vars`).
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_COMMON_DIR",
    "GIT_CONFIG",
    "GIT_CONFIG_COUNT",
    "GIT_CONFIG_PARAMETERS",
    "GIT_DIR",
    "GIT_GRAFT_FILE",
    "GIT_IMPLICIT_WORK_TREE",
    "GIT_INDEX_FILE",
    "GIT_INTERNAL_SUPER_PREFIX",
    "GIT_NO_REPLACE_OBJECTS",
    "GIT_OBJECT_DIRECTORY",
    "GIT_PREFIX",
    "GIT_REPLACE_REF_BASE",
    "GIT_SHALLOW_FILE",
    "GIT_WORK_TREE",
    # Environment-level config/discovery redirection that can contaminate local reads.
    "GIT_CEILING_DIRECTORIES",
    "GIT_CONFIG_GLOBAL",
    "GIT_CONFIG_NOSYSTEM",
    "GIT_CONFIG_SYSTEM",
    "GIT_DISCOVERY_ACROSS_FILESYSTEM",
    "GIT_NAMESPACE",
}
GIT_ENV_PREFIX_BLOCKLIST = ("GIT_CONFIG_KEY_", "GIT_CONFIG_VALUE_", "GIT_TRACE")
ZERO_OIDS = {"0" * 40, "0" * 64}
DEFAULT_MAX_STATUS = 200
DEFAULT_MAX_BRANCHES = 200
MAX_LIST_LIMIT = 5000
MAX_SAFETY_DETAILS = 20


def clean_git_env() -> dict[str, str]:
    env = os.environ.copy()
    for key in list(env):
        if key in GIT_ENV_EXACT_BLOCKLIST or key.startswith(GIT_ENV_PREFIX_BLOCKLIST):
            env.pop(key, None)
    # These commands are local/read-only: never prompt or perform implicit promisor fetches.
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GIT_NO_LAZY_FETCH"] = "1"
    return env


def run_process(command: list[str], *, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        input=input_text,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        errors="surrogateescape",
        check=False,
        env=clean_git_env(),
    )


def git_command(
    repo: Path,
    *args: str,
    config_overrides: tuple[tuple[str, str], ...] = (),
) -> list[str]:
    command = ["git", "--no-optional-locks"]
    for key, value in config_overrides:
        command.extend(["-c", f"{key}={value}"])
    command.extend(["-C", str(repo), *args])
    return command


def run_git_result(
    repo: Path,
    *args: str,
    config_overrides: tuple[tuple[str, str], ...] = (),
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    return run_process(
        git_command(repo, *args, config_overrides=config_overrides),
        input_text=input_text,
    )


def run_git(
    repo: Path,
    *args: str,
    check: bool = True,
    config_overrides: tuple[tuple[str, str], ...] = (),
) -> str:
    result = run_git_result(repo, *args, config_overrides=config_overrides)
    if check and result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout.rstrip("\r\n")


@lru_cache(maxsize=1)
def git_supports_boolean_fsmonitor() -> bool:
    result = run_process(["git", "--version"])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git --version failed")

    match = re.search(r"\b(\d+)\.(\d+)(?:\.(\d+))?", result.stdout)
    if not match:
        raise RuntimeError(f"Could not parse Git version: {result.stdout.strip()}")
    return (int(match.group(1)), int(match.group(2))) >= (2, 36)


def git_config_present(repo: Path, key: str) -> bool:
    result = run_git_result(repo, "config", "--get-regexp", rf"^{re.escape(key)}$")
    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr.strip() or f"git config lookup failed for {key}")
    return result.returncode == 0


def fsmonitor_safe_overrides(repo: Path) -> tuple[tuple[str, str], ...]:
    if git_supports_boolean_fsmonitor():
        return (("core.fsmonitor", "false"),)

    if git_config_present(repo, "core.fsmonitor"):
        raise RuntimeError(
            "Safe preflight with configured core.fsmonitor requires Git 2.36 or newer; "
            "upgrade Git or disable fsmonitor outside this helper before retrying."
        )
    return ()


def run_git_index_result(
    repo: Path,
    *args: str,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    return run_git_result(
        repo,
        *args,
        config_overrides=fsmonitor_safe_overrides(repo),
        input_text=input_text,
    )


def read_status_result(repo: Path) -> subprocess.CompletedProcess[str]:
    return run_git_index_result(
        repo,
        "status",
        "--porcelain=v1",
        "--untracked-files=normal",
        "--ignore-submodules=all",
    )


def looks_like_local_path(value: str) -> bool:
    return value.startswith(("/", "./", "../", "~/", "\\\\")) or bool(re.match(r"^[A-Za-z]:[\\/]", value))


def sanitize_remote_url(value: str | None) -> str | None:
    """Return a display-safe remote URL without credentials, query, or fragment."""
    if not value:
        return None

    helper_match = re.match(r"^([A-Za-z][A-Za-z0-9+.-]*)::", value)
    if helper_match:
        return f"{helper_match.group(1)}::<redacted-helper-payload>"

    if "://" in value:
        try:
            parsed = urlsplit(value)
        except ValueError:
            scheme, remainder = value.split("://", 1)
            remainder = remainder.split("#", 1)[0].split("?", 1)[0]
            authority, separator, path = remainder.partition("/")
            safe_authority = authority.rsplit("@", 1)[-1]
            safe_path = f"/{path}" if separator else ""
            return f"{scheme}://{safe_authority}{safe_path}"

        safe_netloc = parsed.netloc.rsplit("@", 1)[-1]
        return urlunsplit((parsed.scheme, safe_netloc, parsed.path, "", ""))

    if looks_like_local_path(value):
        return value

    safe = value.split("#", 1)[0].split("?", 1)[0]
    if "@" in safe:
        # Covers SCP-like user@host:path and protocol-less user:token@host/path forms.
        safe = safe.rsplit("@", 1)[1]
    return safe


def normalize_oid(value: str) -> str | None:
    return None if value in ZERO_OIDS else value


def bounded_lines(value: str, limit: int) -> tuple[list[str], int, bool]:
    lines = value.splitlines() if value else []
    total = len(lines)
    return lines[:limit], total, total > limit


def split_nul(value: str) -> list[str]:
    if not value:
        return []
    items = value.split("\0")
    if items and items[-1] == "":
        items.pop()
    return items


def path_from_git_cwd(repo: Path, value: str) -> Path:
    path = Path(value)
    return path.resolve() if path.is_absolute() else (repo / path).resolve()


def path_is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def executable_filter_drivers(repo: Path) -> tuple[list[str], bool]:
    """Return active clean/process filter driver names without executing them."""
    config = run_git_result(
        repo,
        "config",
        "--null",
        "--name-only",
        "--get-regexp",
        r"^filter\..*\.(clean|process)$",
    )
    if config.returncode == 1:
        return [], True
    if config.returncode != 0:
        return [], False

    configured: dict[str, str] = {}
    for key in split_nul(config.stdout):
        match = re.match(r"^filter\.(.+)\.(clean|process)$", key, re.IGNORECASE)
        if match:
            configured.setdefault(match.group(1).lower(), match.group(1))

    if not configured:
        return [], True

    tracked = run_git_index_result(repo, "ls-files", "-z")
    if tracked.returncode != 0:
        return [], False
    if not tracked.stdout:
        return [], True

    attrs = run_git_index_result(repo, "check-attr", "-z", "--stdin", "filter", input_text=tracked.stdout)
    if attrs.returncode != 0:
        return [], False

    values = split_nul(attrs.stdout)
    if len(values) % 3 != 0:
        return [], False

    active: set[str] = set()
    for index in range(0, len(values), 3):
        attr_value = values[index + 2]
        configured_name = configured.get(attr_value.lower())
        if configured_name:
            active.add(configured_name)
    return sorted(active), True


def submodule_paths(repo: Path) -> tuple[list[str], bool]:
    result = run_git_index_result(repo, "ls-files", "--stage", "-z")
    if result.returncode != 0:
        return [], False

    paths: set[str] = set()
    for entry in split_nul(result.stdout):
        metadata, separator, path = entry.partition("\t")
        if not separator:
            continue
        mode = metadata.split(" ", 1)[0]
        if mode == "160000":
            paths.add(path)
    return sorted(paths), True


def observed_dirty_without_worktree_comparison(repo: Path, head: str | None) -> tuple[bool, list[str], bool]:
    """Observe safe dirty signals that do not require clean/process filters or submodule traversal."""
    reasons: list[str] = []
    complete = True

    if head:
        staged = run_git_index_result(
            repo,
            "diff-index",
            "--cached",
            "--quiet",
            "--no-ext-diff",
            "--no-textconv",
            head,
            "--",
        )
        if staged.returncode == 1:
            reasons.append("staged changes observed")
        elif staged.returncode != 0:
            complete = False
    else:
        staged = run_git_index_result(repo, "ls-files", "--cached", "-z")
        if staged.returncode == 0:
            if staged.stdout:
                reasons.append("staged changes observed in unborn repository")
        else:
            complete = False

    deleted = run_git_index_result(repo, "ls-files", "--deleted", "-z")
    if deleted.returncode == 0:
        if deleted.stdout:
            reasons.append("deleted tracked paths observed")
    else:
        complete = False

    untracked = run_git_index_result(repo, "ls-files", "--others", "--exclude-standard", "-z")
    if untracked.returncode == 0:
        if untracked.stdout:
            reasons.append("untracked paths observed")
    else:
        complete = False

    return bool(reasons), reasons, complete


def collect_status(repo: Path, head: str | None, max_status: int) -> dict:
    filters, filter_detection_complete = executable_filter_drivers(repo)
    submodules, submodule_detection_complete = submodule_paths(repo)

    status_output = ""
    status_ran = False
    reasons: list[str] = []

    if not filter_detection_complete:
        reasons.append("could not prove that tracked-path clean/process filters are absent")
    elif filters:
        reasons.append("exact worktree comparison skipped because tracked paths use executable clean/process filters")
    else:
        status = read_status_result(repo)
        if status.returncode == 0:
            status_output = status.stdout.rstrip("\r\n")
            status_ran = True
        else:
            reasons.append("exact status could not be completed from local objects under no-lazy-fetch mode")

    if not submodule_detection_complete:
        reasons.append("could not determine whether indexed submodules exist")
    elif submodules:
        reasons.append("submodule worktree internals were not traversed by read-only preflight")

    status_items, status_total, status_truncated = bounded_lines(status_output, max_status)
    status_complete = status_ran and filter_detection_complete and not filters and submodule_detection_complete and not submodules

    observed_dirty, observed_reasons, observed_complete = observed_dirty_without_worktree_comparison(repo, head)
    dirty = bool(status_output) or observed_dirty
    if not observed_complete:
        reasons.append("some safe fallback dirty-state probes could not be completed from local objects")

    if status_complete:
        observed_reasons = []

    return {
        "dirty": dirty,
        "dirty_complete": status_complete,
        "status_porcelain": status_items,
        "status_total": status_total,
        "status_truncated": status_truncated,
        "status_complete": status_complete,
        "status_total_is_lower_bound": not status_complete,
        "status_incomplete_reasons": reasons,
        "observed_dirty_reasons": observed_reasons,
        "executable_filter_drivers": filters[:MAX_SAFETY_DETAILS],
        "executable_filter_driver_count": len(filters),
        "executable_filter_drivers_truncated": len(filters) > MAX_SAFETY_DETAILS,
        "submodule_paths": submodules[:MAX_SAFETY_DETAILS],
        "submodule_count": len(submodules),
        "submodule_paths_truncated": len(submodules) > MAX_SAFETY_DETAILS,
    }


def detect_history_rewrites(repo: Path) -> dict:
    replacements = run_git_result(repo, "for-each-ref", "--format=%(refname)", "refs/replace/")
    replacement_refs = replacements.stdout.splitlines() if replacements.returncode == 0 else []
    replacement_detection_complete = replacements.returncode == 0

    graft_path_value = run_git(repo, "rev-parse", "--git-path", "info/grafts", check=False)
    graft_path = path_from_git_cwd(repo, graft_path_value) if graft_path_value else None
    legacy_grafts_present = bool(graft_path and graft_path.is_file() and graft_path.stat().st_size > 0)

    altered = bool(replacement_refs) or legacy_grafts_present
    return {
        "replacement_refs_active": bool(replacement_refs),
        "replacement_ref_count": len(replacement_refs),
        "replacement_refs": replacement_refs[:MAX_SAFETY_DETAILS],
        "replacement_refs_truncated": len(replacement_refs) > MAX_SAFETY_DETAILS,
        "replacement_ref_detection_complete": replacement_detection_complete,
        "legacy_grafts_present": legacy_grafts_present,
        "history_semantics_altered": altered,
    }


def collect(
    repo: Path,
    recovery: bool = False,
    recent: int = 8,
    max_status: int = DEFAULT_MAX_STATUS,
    max_branches: int = DEFAULT_MAX_BRANCHES,
) -> dict:
    # Keep every Git command anchored to the originally requested repository context.
    # `--show-toplevel` is descriptive only: core.worktree may intentionally point elsewhere.
    root = Path(run_git(repo, "rev-parse", "--show-toplevel")).resolve()
    git_dir = Path(run_git(repo, "rev-parse", "--absolute-git-dir")).resolve()
    common_dir_value = run_git(repo, "rev-parse", "--git-common-dir")
    common_dir = path_from_git_cwd(repo, common_dir_value)

    head = run_git(repo, "rev-parse", "--verify", "HEAD", check=False) or None
    branch = run_git(repo, "symbolic-ref", "--quiet", "--short", "HEAD", check=False) or None
    history = detect_history_rewrites(repo)
    status = collect_status(repo, head, max_status)

    remotes = []
    names = run_git(repo, "remote", check=False).splitlines()
    for name in names:
        fetch = run_git(repo, "remote", "get-url", name, check=False) or None
        push = run_git(repo, "remote", "get-url", "--push", name, check=False) or None
        remotes.append({"name": name, "fetch_url": sanitize_remote_url(fetch), "push_url": sanitize_remote_url(push)})

    worktrees = []
    raw = run_git(repo, "worktree", "list", "--porcelain", check=False)
    current = {}
    for line in raw.splitlines() + [""]:
        if not line:
            if current:
                worktrees.append(current)
                current = {}
            continue
        key, _, value = line.partition(" ")
        if key in {"worktree", "HEAD", "branch"}:
            current[key.lower()] = normalize_oid(value) if key == "HEAD" else value
        else:
            current[key] = True if not value else value

    upstream = run_git(repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}", check=False) or None

    remote_candidates = []
    if upstream and "/" in upstream:
        remote_candidates.append(upstream.split("/", 1)[0])
    for preferred in ("origin", "upstream"):
        if preferred in names:
            remote_candidates.append(preferred)
    remote_candidates.extend(names)

    default_branch = None
    seen_remotes = set()
    for remote in remote_candidates:
        if remote in seen_remotes:
            continue
        seen_remotes.add(remote)
        remote_head = run_git(
            repo,
            "symbolic-ref",
            "--quiet",
            "--short",
            f"refs/remotes/{remote}/HEAD",
            check=False,
        )
        prefix = f"{remote}/"
        if remote_head.startswith(prefix):
            default_branch = remote_head[len(prefix):]
            break

    requested_within_worktree = path_is_within(repo, root)
    identity_notes: list[str] = []
    if not requested_within_worktree:
        identity_notes.append(
            "Requested repository context resolves to a different effective worktree; Git commands remained anchored to the requested repository identity."
        )
    if history["history_semantics_altered"]:
        identity_notes.append(
            "Replacement refs or legacy grafts alter interpreted Git object/history semantics; raw HEAD/ref identity remains separately reported."
        )

    data = {
        "requested_path": str(repo),
        "repo_root": str(root),
        "git_dir": str(git_dir),
        "git_common_dir": str(common_dir),
        "requested_path_within_worktree": requested_within_worktree,
        "identity_notes": identity_notes,
        "branch": branch,
        "head": head,
        "upstream": upstream,
        "default_branch": default_branch,
        **status,
        "remotes": remotes,
        "worktrees": worktrees,
        **history,
    }

    if recovery:
        branches = run_git(repo, "for-each-ref", "--format=%(refname:short) %(objectname)", "refs/heads/", check=False)
        branch_items, branch_total, branch_truncated = bounded_lines(branches, max_branches)

        if head:
            recent_result = run_git_result(
                repo,
                "log",
                f"-{recent}",
                "--date=iso-strict",
                "--pretty=format:%H%x09%ad%x09%s",
                config_overrides=(("log.showSignature", "false"),),
            )
            recent_commits = recent_result.stdout.splitlines() if recent_result.returncode == 0 else []
            recent_commits_complete = recent_result.returncode == 0
        else:
            recent_commits = []
            recent_commits_complete = True

        tags_result = run_git_result(repo, "tag", "--sort=-creatordate")
        recent_tags = tags_result.stdout.splitlines()[:10] if tags_result.returncode == 0 else []
        recent_tags_complete = tags_result.returncode == 0

        limitations = [
            "Does not contain authoritative GitHub Issue/PR/Project/CI state.",
            "Does not contain deployment/production state.",
            "High-cardinality status/branch lists may be bounded; use totals/truncation flags and targeted Git inspection when needed.",
            "Does not perform implicit promisor/lazy fetches; incomplete local-object evidence must be refreshed explicitly when needed and authorized.",
            "Refresh remote refs and query authoritative systems separately when needed.",
        ]
        if not data["status_complete"]:
            limitations.append(
                "Worktree status is intentionally partial because an exact safe read could not be proven; dirty=false means no dirty state was safely observed, not proof of a clean worktree."
            )
        if not recent_commits_complete or not recent_tags_complete:
            limitations.append(
                "Some recovery history/tag evidence is incomplete from local objects under no-lazy-fetch mode; use an explicit authorized fetch or targeted authoritative inspection if that evidence matters."
            )
        if history["history_semantics_altered"]:
            limitations.append(
                "Replacement refs or legacy grafts alter interpreted history; keep raw ref/object identity distinct from interpreted history for identity-sensitive decisions."
            )

        data.update({
            "warning": "TRANSIENT READ-ONLY RECOVERY VIEW. Do not commit or use as authoritative manager state.",
            "local_branches": branch_items,
            "local_branch_total": branch_total,
            "local_branches_truncated": branch_truncated,
            "recent_commits": recent_commits,
            "recent_commits_complete": recent_commits_complete,
            "recent_tags": recent_tags,
            "recent_tags_complete": recent_tags_complete,
            "limitations": limitations,
        })

    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", nargs="?", default=".", help="Repository path (default: current directory)")
    parser.add_argument("--recovery", action="store_true", help="Include extra transient local Git recovery context")
    parser.add_argument("--recent", type=int, default=8, help="Recent commits with --recovery (default: 8)")
    parser.add_argument(
        "--max-status",
        type=int,
        default=DEFAULT_MAX_STATUS,
        help=f"Maximum status entries returned; total/truncation metadata is always included (default: {DEFAULT_MAX_STATUS})",
    )
    parser.add_argument(
        "--max-branches",
        type=int,
        default=DEFAULT_MAX_BRANCHES,
        help=f"Maximum local branches returned with --recovery (default: {DEFAULT_MAX_BRANCHES})",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    args = parser.parse_args()

    if args.recent < 1 or args.recent > 50:
        print(json.dumps({"ok": False, "error": "--recent must be between 1 and 50"}), file=sys.stderr)
        return 2
    for flag, value in (("--max-status", args.max_status), ("--max-branches", args.max_branches)):
        if value < 1 or value > MAX_LIST_LIMIT:
            print(json.dumps({"ok": False, "error": f"{flag} must be between 1 and {MAX_LIST_LIMIT}"}), file=sys.stderr)
            return 2

    try:
        data = collect(
            Path(args.repo).resolve(),
            recovery=args.recovery,
            recent=args.recent,
            max_status=args.max_status,
            max_branches=args.max_branches,
        )
    except (RuntimeError, FileNotFoundError, OSError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 2

    print(json.dumps({"ok": True, **data}, indent=2 if args.pretty else None, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
