#!/usr/bin/env python3
"""Deterministic isolation checks for the #54 Worker assignment-owner prototype."""
from __future__ import annotations

import io
import json
import re
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT_DIR = ROOT / "benchmarks" / "phase7" / "experiments" / "worker-assignment-owner-dedup-v1"
EXPERIMENT_PATH = EXPERIMENT_DIR / "experiment.json"
CANDIDATE_PATH = EXPERIMENT_DIR / "candidate-worker-isolation.md"
README_PATH = EXPERIMENT_DIR / "README.md"
ANALYSIS_PATH = EXPERIMENT_DIR / "OPERATIONAL-ANALYSIS.md"
SOURCE_REF = "af4b2aa86d8a13ca5f45ecf6ed4aadc8f741c386"
SEMANTIC_BASELINE_REF = "f98e8a242c720931e34aa7c4e8a799090e3d0495"
TARGET_PATH = "skill/references/worker-protocol.md"
STATE_RE = re.compile(
    r"\b(TaskState|WorkerStatus|WriteState|DeliveryState|MasterBoundary)\.([A-Z][A-Z0-9_]*)\b"
)


def git_bytes(*args: str) -> bytes:
    try:
        return subprocess.run(
            ["git", *args],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise AssertionError(f"git {' '.join(args)} failed") from exc


def git_text(ref: str, path: str) -> str:
    return git_bytes("show", f"{ref}:{path}").decode("utf-8")


def section(text: str, start: str, end: str) -> str:
    if text.count(start) != 1 or text.count(end) != 1:
        raise AssertionError(f"section headings must each occur exactly once: {start} / {end}")
    start_index = text.index(start)
    end_index = text.index(end)
    if start_index >= end_index:
        raise AssertionError("section headings out of order")
    return text[start_index:end_index]


def replace_section(source: str, start: str, end: str, candidate: str) -> str:
    source_section = section(source, start, end)
    if candidate.count(start) != 1 or not candidate.lstrip().startswith(start):
        raise AssertionError("candidate must begin with configured start heading")
    if end in candidate:
        raise AssertionError("candidate must not include exclusive end heading")
    return source.replace(source_section, candidate.rstrip() + "\n\n", 1)


def safe_extract_tar(data: bytes, destination: Path) -> None:
    destination = destination.resolve()
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:") as archive:
        for member in archive.getmembers():
            target = (destination / member.name).resolve()
            try:
                target.relative_to(destination)
            except ValueError as exc:
                raise AssertionError(f"unsafe archive path: {member.name}") from exc
            if member.issym() or member.islnk():
                raise AssertionError(f"runtime archive must not contain links: {member.name}")
        archive.extractall(destination)


def skill_paths(ref: str) -> list[str]:
    return [
        line
        for line in git_bytes("ls-tree", "-r", "--name-only", ref, "skill").decode("utf-8").splitlines()
        if line
    ]


def collect_states_from_ref(ref: str) -> set[tuple[str, str]]:
    states: set[tuple[str, str]] = set()
    for path in skill_paths(ref):
        if path == "skill/SKILL.md" or (path.startswith("skill/references/") and path.endswith(".md")):
            states.update(STATE_RE.findall(git_text(ref, path)))
    return states


def collect_states_from_root(root: Path) -> set[tuple[str, str]]:
    states: set[tuple[str, str]] = set()
    for path in [root / "SKILL.md", *sorted((root / "references").glob("*.md"))]:
        states.update(STATE_RE.findall(path.read_text(encoding="utf-8")))
    return states


def main() -> None:
    experiment = json.loads(EXPERIMENT_PATH.read_text(encoding="utf-8"))
    if experiment.get("schema_version") != 1 or experiment.get("experiment_id") != "worker-assignment-owner-dedup-v1":
        raise AssertionError("unexpected experiment identity")
    if experiment.get("source_ref") != SOURCE_REF or experiment.get("semantic_baseline_ref") != SEMANTIC_BASELINE_REF:
        raise AssertionError("frozen experiment refs drifted")
    if experiment.get("semantic_change_allowed") is not False or experiment.get("canonical_runtime_changed_during_prototype") is not False:
        raise AssertionError("prototype must remain representation-only and outside canonical runtime")

    if git_bytes("rev-parse", f"{SOURCE_REF}^{{commit}}").decode().strip() != SOURCE_REF:
        raise AssertionError("source ref did not resolve exactly")
    if git_bytes("rev-parse", f"{SEMANTIC_BASELINE_REF}^{{commit}}").decode().strip() != SEMANTIC_BASELINE_REF:
        raise AssertionError("semantic baseline did not resolve exactly")
    git_bytes("merge-base", "--is-ancestor", SEMANTIC_BASELINE_REF, SOURCE_REF)
    git_bytes("merge-base", "--is-ancestor", SOURCE_REF, "HEAD")
    print("PASS frozen-worker-prototype-identities")

    replacement = experiment.get("replacement")
    if not isinstance(replacement, dict) or replacement.get("path") != TARGET_PATH:
        raise AssertionError("prototype replacement scope drifted")
    if set(replacement) != {"path", "start_heading", "end_heading_exclusive", "candidate_section"}:
        raise AssertionError("replacement contract fields drifted")
    if experiment.get("canonical_assignment_owner") != "skill/references/task-contract.md#8-worker-assignment-identity":
        raise AssertionError("canonical assignment owner drifted")

    source = git_text(SOURCE_REF, TARGET_PATH)
    candidate = CANDIDATE_PATH.read_text(encoding="utf-8")
    source_section = section(source, replacement["start_heading"], replacement["end_heading_exclusive"])
    materialized_text = replace_section(
        source,
        replacement["start_heading"],
        replacement["end_heading_exclusive"],
        candidate,
    )

    required = (
        "One Worker = one Task Contract + one assigned branch at a time.",
        "filesystem path is runtime location, never assignment identity",
        "[task-contract.md](task-contract.md) §8 owns the persisted Worker assignment/concurrency envelope",
        "read that current envelope and verify it rather than reconstructing its fields here",
        "repository/working directory and current worktree are the intended assigned branch and safe to modify",
        "every persisted assignment/envelope assumption is current",
        "current assigned-branch/worktree HEAD equals immutable `Start HEAD`",
        "normal authorized commits in the same valid generation may advance beyond it without staleness",
        "current assigned-branch HEAD equals the Master-supplied `Checkpoint HEAD` before editing",
        "Any material identity/checkpoint mismatch -> `WorkerStatus.STALE_ASSIGNMENT`; never guess.",
        "Worker never upgrades `ProjectAuthority`, `ScopedAuthorization`, `CoordinationBaseline`, or `AssuranceLevel`",
        "never broadens assignment because Master is unavailable",
    )
    missing = [fragment for fragment in required if fragment not in candidate]
    if missing:
        raise AssertionError(f"candidate lost Worker isolation semantics: {missing}")
    if "Assignment ID`; exact `Base SHA`" in candidate or "active Assignment Status" in candidate:
        raise AssertionError("candidate re-declared the canonical assignment field ontology")
    if len(candidate.split()) >= len(source_section.split()):
        raise AssertionError("candidate did not reduce the duplicate Worker isolation rendition")
    print(f"PASS Worker isolation structural diagnostic {len(source_section.split())}->{len(candidate.split())}")

    with tempfile.TemporaryDirectory(prefix="gpo-worker-dedup-") as temp_name:
        temp_root = Path(temp_name)
        safe_extract_tar(git_bytes("archive", "--format=tar", SOURCE_REF, "skill"), temp_root)
        target = temp_root / TARGET_PATH
        target.write_text(materialized_text, encoding="utf-8")

        changed: set[str] = set()
        for path in skill_paths(SOURCE_REF):
            candidate_path = temp_root / path
            if not candidate_path.is_file():
                raise AssertionError(f"materialized runtime lost source path: {path}")
            if candidate_path.read_bytes() != git_bytes("show", f"{SOURCE_REF}:{path}"):
                changed.add(path)
        if changed != {TARGET_PATH}:
            raise AssertionError(f"prototype changed unexpected runtime paths: {sorted(changed)}")

        if collect_states_from_root(temp_root / "skill") != collect_states_from_ref(SOURCE_REF):
            raise AssertionError("state namespace/token surface changed")
        if (temp_root / "skill" / "SKILL.md").read_bytes() != git_bytes("show", f"{SOURCE_REF}:skill/SKILL.md"):
            raise AssertionError("Worker entry routing changed")
        if (temp_root / "skill" / "references" / "task-contract.md").read_bytes() != git_bytes(
            "show", f"{SOURCE_REF}:skill/references/task-contract.md"
        ):
            raise AssertionError("canonical Task Contract assignment owner changed")
        print("PASS Worker prototype non-target-runtime-byte-identity")

        # Everything from Dispatch onward must remain byte-identical because transport,
        # staleness, handoff, blocker, absorption, and correction semantics are out of scope.
        end_heading = replacement["end_heading_exclusive"]
        if materialized_text[materialized_text.index(end_heading):] != source[source.index(end_heading):]:
            raise AssertionError("Worker Protocol content after Isolation changed")
        print("PASS dispatch-handoff-staleness-corrections-unchanged")

        for source_path in ("design/RULE-MAP.md", "design/GOAL-MAP.md", "docs/PROJECT-SPEC.md"):
            destination = temp_root / source_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(git_bytes("show", f"{SOURCE_REF}:{source_path}"))
        validation = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "validate_skill.py"), str(temp_root / "skill")],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if validation.returncode != 0:
            raise AssertionError(
                "materialized Worker candidate failed validate_skill.py: "
                + (validation.stderr.strip() or validation.stdout.strip())
            )
        print("PASS materialized-Worker-candidate-validation")

    readme = README_PATH.read_text(encoding="utf-8")
    analysis = ANALYSIS_PATH.read_text(encoding="utf-8")
    for required_text in (SOURCE_REF, SEMANTIC_BASELINE_REF, "single exact assignment envelope owner"):
        if required_text not in readme:
            raise AssertionError(f"Worker semantic ledger missing required evidence: {required_text}")
    for scenario in (
        "Initial Worker dispatch before first edit",
        "Normal authorized Worker progress",
        "Same-generation correction/resume",
        "Assignment generation replaced or invalidated",
        "Master unavailable during Worker execution",
    ):
        if scenario not in analysis:
            raise AssertionError(f"Worker operational analysis missing scenario: {scenario}")
    print("PASS Worker ledger-and-operational-analysis-present")


if __name__ == "__main__":
    main()
