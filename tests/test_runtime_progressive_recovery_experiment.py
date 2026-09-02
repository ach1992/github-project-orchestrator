#!/usr/bin/env python3
"""Deterministic isolation checks for the #60 progressive recovery prototype."""
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
EXP = ROOT / "benchmarks" / "phase7" / "experiments" / "progressive-recovery-procedure-v1"
SOURCE_REF = "9cfbc9bc57be4690796d3d9996a517cd257746c5"
BASELINE_REF = "f98e8a242c720931e34aa7c4e8a799090e3d0495"
TARGET = "skill/references/continuity.md"
START = "## 2. Recovery sequence"
END = "For multi-repository outcomes, recover the small global coordination spine first:"
STATE_RE = re.compile(r"\b(TaskState|WorkerStatus|WriteState|DeliveryState|MasterBoundary)\.([A-Z][A-Z0-9_]*)\b")


def git_bytes(*args: str) -> bytes:
    try:
        return subprocess.run(["git", *args], cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise AssertionError(f"git {' '.join(args)} failed") from exc


def git_text(ref: str, path: str) -> str:
    return git_bytes("show", f"{ref}:{path}").decode("utf-8")


def safe_extract(data: bytes, destination: Path) -> None:
    destination = destination.resolve()
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:") as archive:
        for member in archive.getmembers():
            target = (destination / member.name).resolve()
            try:
                target.relative_to(destination)
            except ValueError as exc:
                raise AssertionError(f"unsafe archive path: {member.name}") from exc
            if member.issym() or member.islnk():
                raise AssertionError(f"runtime archive contains link: {member.name}")
        archive.extractall(destination)


def main() -> None:
    doc = json.loads((EXP / "experiment.json").read_text(encoding="utf-8"))
    if doc.get("experiment_id") != "progressive-recovery-procedure-v1":
        raise AssertionError("unexpected experiment identity")
    if doc.get("source_ref") != SOURCE_REF or doc.get("semantic_baseline_ref") != BASELINE_REF:
        raise AssertionError("frozen refs drifted")
    if doc.get("semantic_change_allowed") is not False or doc.get("canonical_runtime_changed_during_prototype") is not False:
        raise AssertionError("prototype must remain representation-only")
    if git_bytes("rev-parse", f"{SOURCE_REF}^{{commit}}").decode().strip() != SOURCE_REF:
        raise AssertionError("source ref did not resolve exactly")
    if git_bytes("rev-parse", f"{BASELINE_REF}^{{commit}}").decode().strip() != BASELINE_REF:
        raise AssertionError("semantic baseline did not resolve exactly")
    git_bytes("merge-base", "--is-ancestor", BASELINE_REF, SOURCE_REF)
    git_bytes("merge-base", "--is-ancestor", SOURCE_REF, "HEAD")
    print("PASS frozen-progressive-recovery-identities")

    source = git_text(SOURCE_REF, TARGET)
    if source.count(START) != 1 or source.count(END) != 1:
        raise AssertionError("recovery markers must occur exactly once")
    start, end = source.index(START), source.index(END)
    if start >= end:
        raise AssertionError("recovery markers out of order")
    source_prefix = source[start:end]
    candidate = (EXP / "candidate-recovery.md").read_text(encoding="utf-8")
    materialized = source[:start] + candidate.rstrip() + "\n\n" + source[end:]

    required = (
        "A new/replacement Master enters `RECOVER` before consequential project mutation",
        "target/default branches, checkout/worktrees, repository rules, and current capabilities",
        "Read an existing lightweight Project Map/index if present",
        "recover `ProjectAuthority` and `CoordinationBaseline` independently",
        "recover any affected `AssuranceLevel` and exact current `ScopedAuthorization`",
        "Treat the canonical root project specification as triggered depth: do not load it merely because chat is absent",
        "active Issues/milestones/Projects/risks/assignments",
        "open PRs/reviews/checks/branches/dependencies",
        "recent Git/release/deployment state only as needed",
        "Reconcile contradictions and stale assignments",
        "`DeliveryRequirement`/`DeliveryTarget`/`DeliveryState`",
        "**Orientation spine**",
        "**Active-path context**",
        "**Triggered depth**",
        "Load the root specification when project-level intent cannot be established safely from current downstream authoritative state or when material contradiction/change makes it decision-relevant",
        "Once repository/target identity, active outcome, controlling dependencies/blockers",
        "continue the valid plan instead of rebuilding it because chat history is absent",
        "A large repository or long-lived project is a reason to narrow recovery by workstream, not to read more by default",
    )
    missing = [item for item in required if item not in candidate]
    if missing:
        raise AssertionError(f"candidate lost recovery semantics: {missing}")
    if candidate.count("| Recovery layer | Required work |") != 1:
        raise AssertionError("candidate must contain one progressive recovery table")
    if "Keep cold recovery progressive and bounded:" in candidate or "1. identify repository" in candidate:
        raise AssertionError("candidate retained duplicate recovery representation")
    print(f"PASS progressive-recovery diagnostic words {len(source_prefix.split())}->{len(candidate.split())}")

    materialized_end = materialized.index(END)
    if materialized[:start] != source[:start] or materialized[materialized_end:] != source[end:]:
        raise AssertionError("prototype changed recovery content outside target prefix")
    for item in (
        "For multi-repository outcomes",
        "Never reconstruct `CoordinationBaseline` from `AssuranceLevel`",
        "do not re-enter the full recovery sequence for ordinary progress",
        "A failed GitHub/tool route should update transient capability knowledge",
        "Re-enter broader recovery only when concrete evidence materially invalidates the established baseline",
    ):
        if item not in materialized[materialized_end:]:
            raise AssertionError(f"later recovery rule disappeared: {item}")
    print("PASS progressive-recovery later-rules-byte-identity")

    with tempfile.TemporaryDirectory(prefix="gpo-recovery-") as tmp:
        root = Path(tmp)
        safe_extract(git_bytes("archive", "--format=tar", SOURCE_REF, "skill"), root)
        (root / TARGET).write_text(materialized, encoding="utf-8")
        changed = set()
        paths = git_bytes("ls-tree", "-r", "--name-only", SOURCE_REF, "skill").decode().splitlines()
        for path in paths:
            file_path = root / path
            if not file_path.is_file():
                raise AssertionError(f"materialized runtime lost path: {path}")
            if file_path.read_bytes() != git_bytes("show", f"{SOURCE_REF}:{path}"):
                changed.add(path)
        if changed != {TARGET}:
            raise AssertionError(f"unexpected runtime paths changed: {sorted(changed)}")
        if set(STATE_RE.findall(materialized)) != set(STATE_RE.findall(source)):
            raise AssertionError("continuity state/boundary surface changed")
        for path in ("design/RULE-MAP.md", "design/GOAL-MAP.md", "docs/PROJECT-SPEC.md"):
            dst = root / path
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(git_bytes("show", f"{SOURCE_REF}:{path}"))
        result = subprocess.run([sys.executable, str(ROOT / "tools" / "validate_skill.py"), str(root / "skill"), "--allow-legacy-unindexed-evals"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode:
            raise AssertionError(result.stderr.strip() or result.stdout.strip())
    print("PASS progressive-recovery isolation-state-surface-validation")

    readme = (EXP / "README.md").read_text(encoding="utf-8")
    analysis = (EXP / "OPERATIONAL-ANALYSIS.md").read_text(encoding="utf-8")
    for item in (SOURCE_REF, BASELINE_REF, "One-to-one semantic ledger", "Representation fit versus KEEP"):
        if item not in readme:
            raise AssertionError(f"ledger missing: {item}")
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
            raise AssertionError(f"analysis missing scenario: {scenario}")
    print("PASS progressive-recovery ledger-and-operational-analysis")


if __name__ == "__main__":
    main()
