#!/usr/bin/env python3
"""Deterministic isolation checks for the #60 progressive recovery representation prototype."""
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
EXPERIMENT_DIR = ROOT / "benchmarks" / "phase7" / "experiments" / "progressive-recovery-procedure-v1"
EXPERIMENT_PATH = EXPERIMENT_DIR / "experiment.json"
CANDIDATE_PATH = EXPERIMENT_DIR / "candidate-recovery.md"
README_PATH = EXPERIMENT_DIR / "README.md"
ANALYSIS_PATH = EXPERIMENT_DIR / "OPERATIONAL-ANALYSIS.md"
SOURCE_REF = "9cfbc9bc57be4690796d3d9996a517cd257746c5"
SEMANTIC_BASELINE_REF = "f98e8a242c720931e34aa7c4e8a799090e3d0495"
TARGET_PATH = "skill/references/continuity.md"
START_HEADING = "## 2. Recovery sequence"
END_MARKER = "For multi-repository outcomes, recover the small global coordination spine first:"
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
    if experiment.get("schema_version") != 1 or experiment.get("experiment_id") != "progressive-recovery-procedure-v1":
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
    print("PASS frozen-progressive-recovery-prototype-identities")

    replacement = experiment.get("replacement")
    expected_fields = {"path", "start_heading", "end_marker_exclusive", "candidate_section"}
    if not isinstance(replacement, dict) or set(replacement) != expected_fields:
        raise AssertionError("replacement contract fields drifted")
    if replacement["path"] != TARGET_PATH or replacement["start_heading"] != START_HEADING or replacement["end_marker_exclusive"] != END_MARKER:
        raise AssertionError("prototype replacement scope drifted")

    source = git_text(SOURCE_REF, TARGET_PATH)
    if source.count(START_HEADING) != 1 or source.count(END_MARKER) != 1:
        raise AssertionError("target markers must occur exactly once")
    start = source.index(START_HEADING)
    end = source.index(END_MARKER)
    if start >= end:
        raise AssertionError("target markers out of order")
    source_prefix = source[start:end]
    candidate = CANDIDATE_PATH.read_text(encoding="utf-8")
    if not candidate.startswith(START_HEADING):
        raise AssertionError("candidate must begin with target heading")
    if END_MARKER in candidate:
        raise AssertionError("candidate must not include exclusive end marker")
    materialized = source[:start] + candidate.rstrip() + "\n\n" + source[end:]

    required = (
        "A new/replacement Master enters `RECOVER` before consequential project mutation",
        "target/default branches, checkout/worktrees, repository rules, and current capabilities",
        "Read an existing lightweight Project Map/index if present",
        "Consult the canonical root project specification only when project-level intent cannot be established safely from current downstream authoritative state or when material contradiction/change makes it decision-relevant",
        "active Issues/milestones/Projects/risks/assignments",
        "open PRs/reviews/checks/branches/dependencies",
        "recent Git/release/deployment state only as needed",
        "Reconcile contradictions and stale assignments",
        "`DeliveryRequirement`/`DeliveryTarget`/`DeliveryState`",
        "`ProjectAuthority`, `CoordinationBaseline`, any affected `AssuranceLevel`, exact current `ScopedAuthorization`",
        "**Orientation spine**",
        "**Active-path context**",
        "**Triggered depth**",
        "broader architecture, other workstreams, the root specification, historical decisions, or release history only when",
        "Once repository/target identity, active outcome, controlling dependencies/blockers",
        "continue the valid plan instead of rebuilding it because chat history is absent",
        "A large repository or long-lived project is a reason to narrow recovery by workstream, not to read more by default",
    )
    missing = [fragment for fragment in required if fragment not in candidate]
    if missing:
        raise AssertionError(f"candidate lost recovery semantics: {missing}")
    if candidate.count("| Recovery layer | Required work |") != 1:
        raise AssertionError("candidate must expose one progressive recovery table")
    if "1. identify repository" in candidate or "Keep cold recovery progressive and bounded:" in candidate:
        raise AssertionError("candidate retained duplicate recovery representation")
    print(f"PASS progressive-recovery structural diagnostic words {len(source_prefix.split())}->{len(candidate.split())}")

    materialized_end = materialized.index(END_MARKER)
    if materialized[:start] != source[:start]:
        raise AssertionError("continuity content before recovery target changed")
    if materialized[materialized_end:] != source[end:]:
        raise AssertionError("multi-repository and later recovery rules changed")
    later_required = (
        "For multi-repository outcomes",
        "Never reconstruct `CoordinationBaseline` from `AssuranceLevel`",
        "do not re-enter the full recovery sequence for ordinary progress",
        "A failed GitHub/tool route should update transient capability knowledge",
        "Re-enter broader recovery only when concrete evidence materially invalidates the established baseline",
    )
    for fragment in later_required:
        if fragment not in materialized[materialized_end:]:
            raise AssertionError(f"unchanged later recovery rule disappeared: {fragment}")
    print("PASS progressive-recovery later-rules-byte-identity")

    with tempfile.TemporaryDirectory(prefix="gpo-progressive-recovery-") as temp_name:
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
            raise AssertionError("continuity state/boundary token surface changed")
        print("PASS progressive-recovery non-target-runtime-byte-identity-and-state-surface")

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
                "materialized progressive-recovery candidate failed validate_skill.py: "
                + (validation.stderr.strip() or validation.stdout.strip())
            )
        print("PASS materialized-progressive-recovery-candidate-validation")

    readme = README_PATH.read_text(encoding="utf-8")
    analysis = ANALYSIS_PATH.read_text(encoding="utf-8")
    for required_text in (SOURCE_REF, SEMANTIC_BASELINE_REF, "One-to-one semantic ledger", "Representation fit versus KEEP"):
        if required_text not in readme:
            raise AssertionError(f"progressive recovery ledger missing evidence: {required_text}")
    for scenario in (
        "Zero-chat recovery with sufficient downstream current truth",
        "Root specification becomes materially relevant",
        "Planned branch/worktree transition after valid recovery baseline",
        "Preferred GitHub/tool route fails after baseline",
        "Material drift invalidates baseline",
        "Multi-repository outcome",
        "Large long-lived repository",
        "Authority/profile recovery across rotation",
    ):
        if scenario not in analysis:
            raise AssertionError(f"progressive recovery analysis missing scenario: {scenario}")
    print("PASS progressive-recovery ledger-and-operational-analysis-present")


if __name__ == "__main__":
    main()
