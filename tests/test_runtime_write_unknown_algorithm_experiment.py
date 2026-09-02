#!/usr/bin/env python3
"""Deterministic isolation checks for the #58 WriteState.UNKNOWN representation prototype."""
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
EXPERIMENT_DIR = ROOT / "benchmarks" / "phase7" / "experiments" / "write-unknown-canonical-algorithm-v1"
EXPERIMENT_PATH = EXPERIMENT_DIR / "experiment.json"
CANDIDATE_PATH = EXPERIMENT_DIR / "candidate-write-unknown.md"
README_PATH = EXPERIMENT_DIR / "README.md"
ANALYSIS_PATH = EXPERIMENT_DIR / "OPERATIONAL-ANALYSIS.md"
SOURCE_REF = "f161c1b3d30b148b0418c585531dfbeaf7ffec04"
SEMANTIC_BASELINE_REF = "f98e8a242c720931e34aa7c4e8a799090e3d0495"
TARGET_PATH = "skill/references/authority-gates.md"
START_HEADING = "## 6. `WriteState.UNKNOWN`"
END_HEADING = "## 7. Optimistic concurrency"
SYMBOLIC_FLOW = "WriteState.UNKNOWN -> NO BLIND RETRY -> DECISION-SCOPED AUTHORITATIVE RE-READ"
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


def section(text: str, start: str, end: str) -> str:
    if text.count(start) != 1 or text.count(end) != 1:
        raise AssertionError(f"section headings must occur exactly once: {start} / {end}")
    start_index = text.index(start)
    end_index = text.index(end)
    if start_index >= end_index:
        raise AssertionError("section headings out of order")
    return text[start_index:end_index]


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
    if experiment.get("schema_version") != 1 or experiment.get("experiment_id") != "write-unknown-canonical-algorithm-v1":
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
    print("PASS frozen-write-unknown-prototype-identities")

    replacement = experiment.get("replacement")
    expected_fields = {"path", "start_heading", "end_heading_exclusive", "candidate_section"}
    if not isinstance(replacement, dict) or set(replacement) != expected_fields:
        raise AssertionError("replacement contract fields drifted")
    if replacement["path"] != TARGET_PATH or replacement["start_heading"] != START_HEADING or replacement["end_heading_exclusive"] != END_HEADING:
        raise AssertionError("prototype replacement scope drifted")

    source = git_text(SOURCE_REF, TARGET_PATH)
    source_section = section(source, START_HEADING, END_HEADING)
    candidate = CANDIDATE_PATH.read_text(encoding="utf-8")
    if not candidate.startswith(START_HEADING):
        raise AssertionError("candidate must begin with target heading")
    if END_HEADING in candidate:
        raise AssertionError("candidate must not include exclusive end heading")
    materialized = source.replace(source_section, candidate.rstrip() + "\n\n", 1)

    required = (
        "Mark only the individual mutation `WriteState.UNKNOWN`",
        "do not blindly retry and do not automatically stop the Master",
        "stable identity or semantic equivalence",
        "enough decision-scoped completeness to distinguish **present**, **proven absent**, and **incomplete/unknown**",
        "If the equivalent write is **present**, verify it, mark the action `WriteState.KNOWN`, and continue",
        "If the re-read **proves absence**, retry at most once",
        "safely idempotent or protected by stable correlation/deduplication identity",
        "If retry is not safe, freeze the dependent mutation and continue independent safe work",
        "If the re-read is **incomplete/truncated/unknown**, never treat that as absence and never use it to authorize a retry",
        "keep that mutation at `WriteState.UNKNOWN`, continue independent safe work",
        "surface `MasterBoundary.WRITE_OUTCOME_UNKNOWN` only when it becomes the sole/project-wide controlling blocker",
        "Apply to Issue/PR creation, comments, labels, Project updates, pushes, releases, deployment triggers, and other non-idempotent writes",
    )
    missing = [fragment for fragment in required if fragment not in candidate]
    if missing:
        raise AssertionError(f"candidate lost WriteState.UNKNOWN semantics: {missing}")
    if SYMBOLIC_FLOW in candidate:
        raise AssertionError("candidate retained duplicate symbolic flow")
    if candidate.count("WriteState.UNKNOWN") < 2:
        raise AssertionError("candidate lost explicit UNKNOWN state handling")
    if "retry at most once" not in candidate:
        raise AssertionError("candidate lost one-retry bound")
    print(f"PASS WriteState.UNKNOWN structural diagnostic words {len(source_section.split())}->{len(candidate.split())}")

    start_index = source.index(START_HEADING)
    end_index = source.index(END_HEADING)
    materialized_end = materialized.index(END_HEADING)
    if materialized[:start_index] != source[:start_index]:
        raise AssertionError("authority-gates content before §6 changed")
    if materialized[materialized_end:] != source[end_index:]:
        raise AssertionError("optimistic-concurrency and later authority-gates content changed")
    print("PASS WriteState.UNKNOWN surrounding-authority-gates-byte-identity")

    with tempfile.TemporaryDirectory(prefix="gpo-write-unknown-") as temp_name:
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
            raise AssertionError("authority-gates state/boundary token surface changed")
        print("PASS WriteState.UNKNOWN non-target-runtime-byte-identity-and-state-surface")

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
                "materialized WriteState.UNKNOWN candidate failed validate_skill.py: "
                + (validation.stderr.strip() or validation.stdout.strip())
            )
        print("PASS materialized-WriteState.UNKNOWN-candidate-validation")

    readme = README_PATH.read_text(encoding="utf-8")
    analysis = ANALYSIS_PATH.read_text(encoding="utf-8")
    for required_text in (SOURCE_REF, SEMANTIC_BASELINE_REF, "One-to-one semantic ledger", "Representation fit versus KEEP"):
        if required_text not in readme:
            raise AssertionError(f"WriteState.UNKNOWN semantic ledger missing evidence: {required_text}")
    for scenario in (
        "Equivalent write is present after ambiguous transport",
        "Authoritative re-read proves absence and retry is safe",
        "Discovery is incomplete/truncated",
        "Proven absence but retry is unsafe",
        "One safe retry is still ambiguous",
        "Local UNKNOWN while independent work exists",
        "Unknown becomes the sole/project-wide blocker",
    ):
        if scenario not in analysis:
            raise AssertionError(f"WriteState.UNKNOWN operational analysis missing scenario: {scenario}")
    print("PASS WriteState.UNKNOWN ledger-and-operational-analysis-present")


if __name__ == "__main__":
    main()
