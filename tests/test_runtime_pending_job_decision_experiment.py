#!/usr/bin/env python3
"""Deterministic isolation checks for the #56 pending-job decision-structure prototype."""
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
EXPERIMENT_DIR = ROOT / "benchmarks" / "phase7" / "experiments" / "pending-job-decision-structure-v1"
EXPERIMENT_PATH = EXPERIMENT_DIR / "experiment.json"
CANDIDATE_PATH = EXPERIMENT_DIR / "candidate-pending-job.md"
README_PATH = EXPERIMENT_DIR / "README.md"
ANALYSIS_PATH = EXPERIMENT_DIR / "OPERATIONAL-ANALYSIS.md"
SOURCE_REF = "b5c2574f50821de7133119f27f5abf69f10b2624"
SEMANTIC_BASELINE_REF = "f98e8a242c720931e34aa7c4e8a799090e3d0495"
TARGET_PATH = "skill/references/master-cycle.md"
START_MARKER = "For already-running CI/check/deployment/job, `pending` is dependency state, not failure."
END_HEADING = "## 10. Requirement changes"
STATE_RE = re.compile(r"\b(TaskState|WorkerStatus|WriteState|DeliveryState|MasterBoundary)\.([A-Z][A-Z0-9_]*)\b")


def git_bytes(*args: str) -> bytes:
    try:
        return subprocess.run(
            ["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise AssertionError(f"git {' '.join(args)} failed") from exc


def git_text(ref: str, path: str) -> str:
    return git_bytes("show", f"{ref}:{path}").decode("utf-8")


def skill_paths(ref: str) -> list[str]:
    return [
        line
        for line in git_bytes("ls-tree", "-r", "--name-only", ref, "skill").decode("utf-8").splitlines()
        if line
    ]


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


def collect_states(text: str) -> set[tuple[str, str]]:
    return set(STATE_RE.findall(text))


def main() -> None:
    experiment = json.loads(EXPERIMENT_PATH.read_text(encoding="utf-8"))
    if experiment.get("schema_version") != 1 or experiment.get("experiment_id") != "pending-job-decision-structure-v1":
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
    print("PASS frozen-pending-job-prototype-identities")

    replacement = experiment.get("replacement")
    expected_replacement_fields = {"path", "start_marker", "end_heading_exclusive", "candidate_section"}
    if not isinstance(replacement, dict) or set(replacement) != expected_replacement_fields:
        raise AssertionError("replacement contract fields drifted")
    if replacement["path"] != TARGET_PATH or replacement["start_marker"] != START_MARKER or replacement["end_heading_exclusive"] != END_HEADING:
        raise AssertionError("prototype replacement scope drifted")

    source = git_text(SOURCE_REF, TARGET_PATH)
    if source.count(START_MARKER) != 1 or source.count(END_HEADING) != 1:
        raise AssertionError("target markers must occur exactly once")
    start = source.index(START_MARKER)
    end = source.index(END_HEADING)
    if start >= end:
        raise AssertionError("target markers out of order")
    source_fragment = source[start:end]
    candidate = CANDIDATE_PATH.read_text(encoding="utf-8")
    materialized = source[:start] + candidate.rstrip() + "\n\n" + source[end:]

    required = (
        "`pending` is dependency state, not failure",
        "Continue independent useful work first",
        "prefer a real runtime-supported continuation mechanism over yielding control",
        "Use non-tight authoritative rechecks only when a transition is plausibly due",
        "expected job duration, tool/runtime limits, and diminishing value",
        "suitable real event/condition resume primitive exists",
        "Immediately continue the existing workflow; do not require a user nudge",
        "Stop waiting immediately, classify the failure",
        "autonomous continuation is unavailable, no longer reasonable, or exhausted",
        "exact external object, current status, why autonomous continuation cannot safely continue, exact resume condition, and recoverable state",
        "Never tight-poll, sleep indefinitely, fabricate background monitoring/resume, or manufacture work",
        "`DeliveryState.PENDING` remains a lifecycle state, not a terminal boundary label",
        "never use `MasterBoundary.NO_READY_WORK` merely because an already-running required dependency is unfinished",
    )
    missing = [fragment for fragment in required if fragment not in candidate]
    if missing:
        raise AssertionError(f"candidate lost pending-job semantics: {missing}")
    if "MasterBoundary.PENDING" in candidate or "WorkerStatus.PENDING" in candidate or "TaskState.PENDING" in candidate:
        raise AssertionError("candidate invented a pending state/boundary namespace")
    if candidate.count("| Current condition | Required action |") != 1:
        raise AssertionError("candidate must expose one decision table")
    print(f"PASS pending-job structural diagnostic words {len(source_fragment.split())}->{len(candidate.split())}")

    # Exact surrounding-byte guards inside the canonical owner.
    if materialized[:start] != source[:start]:
        raise AssertionError("master-cycle content before pending-job target changed")
    materialized_end = materialized.index(END_HEADING)
    if materialized[materialized_end:] != source[end:]:
        raise AssertionError("requirement-change and later master-cycle content changed")
    if "MASTER_STOP(boundary, independent_work)" not in materialized[materialized_end:]:
        raise AssertionError("MASTER_STOP predicate owner disappeared from unchanged suffix")
    print("PASS pending-job surrounding-master-cycle-byte-identity")

    with tempfile.TemporaryDirectory(prefix="gpo-pending-job-") as temp_name:
        temp_root = Path(temp_name)
        safe_extract_tar(git_bytes("archive", "--format=tar", SOURCE_REF, "skill"), temp_root)
        target = temp_root / TARGET_PATH
        target.write_text(materialized, encoding="utf-8")

        changed: set[str] = set()
        for path in skill_paths(SOURCE_REF):
            candidate_path = temp_root / path
            if not candidate_path.is_file():
                raise AssertionError(f"materialized runtime lost source path: {path}")
            if candidate_path.read_bytes() != git_bytes("show", f"{SOURCE_REF}:{path}"):
                changed.add(path)
        if changed != {TARGET_PATH}:
            raise AssertionError(f"prototype changed unexpected runtime paths: {sorted(changed)}")
        if collect_states(materialized) != collect_states(source):
            raise AssertionError("master-cycle state/boundary token surface changed")
        print("PASS pending-job non-target-runtime-byte-identity-and-state-surface")

        for source_path in ("design/RULE-MAP.md", "design/GOAL-MAP.md", "docs/PROJECT-SPEC.md"):
            destination = temp_root / source_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(git_bytes("show", f"{SOURCE_REF}:{source_path}"))
        validation = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "validate_skill.py"), str(temp_root / "skill"), "--allow-legacy-unindexed-evals"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if validation.returncode != 0:
            raise AssertionError(
                "materialized pending-job candidate failed validate_skill.py: "
                + (validation.stderr.strip() or validation.stdout.strip())
            )
        print("PASS materialized-pending-job-candidate-validation")

    readme = README_PATH.read_text(encoding="utf-8")
    analysis = ANALYSIS_PATH.read_text(encoding="utf-8")
    for required_text in (SOURCE_REF, SEMANTIC_BASELINE_REF, "One-to-one semantic ledger"):
        if required_text not in readme:
            raise AssertionError(f"pending-job semantic ledger missing evidence: {required_text}")
    for scenario in (
        "Independent work exists while CI is pending",
        "Pending becomes the sole dependency; short bounded wait is reasonable",
        "Dependency transitions to failure",
        "Long or unsupported wait becomes the sole blocker",
        "DeliveryState.PENDING namespace separation",
    ):
        if scenario not in analysis:
            raise AssertionError(f"pending-job operational analysis missing scenario: {scenario}")
    print("PASS pending-job ledger-and-operational-analysis-present")


if __name__ == "__main__":
    main()
