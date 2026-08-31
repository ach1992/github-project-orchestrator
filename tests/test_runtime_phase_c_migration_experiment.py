#!/usr/bin/env python3
"""Materialize and verify the exact #38 selected P1-P5 runtime candidate."""
from __future__ import annotations

import base64
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
BASE_REF = "0165bc2a26bdf7452f05160c3e91f47b4fa7ae9c"
SEMANTIC_BASELINE = "f98e8a242c720931e34aa7c4e8a799090e3d0495"
TARGETS = {
    "skill/SKILL.md",
    "skill/references/authority-gates.md",
    "skill/references/worker-protocol.md",
    "skill/references/master-cycle.md",
    "skill/references/continuity.md",
}
STATE_RE = re.compile(r"\b(TaskState|WorkerStatus|WriteState|DeliveryState|MasterBoundary)\.([A-Z][A-Z0-9_]*)\b")

EXPERIMENTS = (
    "benchmarks/phase7/experiments/runtime-dimension-invariants-v2/experiment.json",
    "benchmarks/phase7/experiments/worker-assignment-owner-dedup-v1/experiment.json",
    "benchmarks/phase7/experiments/pending-job-decision-structure-v1/experiment.json",
    "benchmarks/phase7/experiments/write-unknown-canonical-algorithm-v1/experiment.json",
    "benchmarks/phase7/experiments/progressive-recovery-procedure-v1/experiment.json",
)


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


def normalized_replacements(doc: dict) -> list[dict]:
    if "replacements" in doc:
        rows = doc["replacements"]
    else:
        rows = [doc["replacement"]]
    if not isinstance(rows, list) or not rows:
        raise AssertionError(f"experiment {doc.get('experiment_id')} has no replacement")
    return rows


def bounds(text: str, replacement: dict) -> tuple[int, int]:
    if "start_heading" in replacement:
        start_marker = replacement["start_heading"]
    elif "start_marker" in replacement:
        start_marker = replacement["start_marker"]
    else:
        raise AssertionError("replacement missing start marker")

    if "end_heading_exclusive" in replacement:
        end_marker = replacement["end_heading_exclusive"]
    elif "end_marker_exclusive" in replacement:
        end_marker = replacement["end_marker_exclusive"]
    else:
        raise AssertionError("replacement missing end marker")

    if text.count(start_marker) != 1 or text.count(end_marker) != 1:
        raise AssertionError(f"replacement markers must occur exactly once: {replacement['path']}")
    start = text.index(start_marker)
    end = text.index(end_marker)
    if start >= end:
        raise AssertionError(f"replacement markers out of order: {replacement['path']}")
    return start, end


def replacement_source_section(doc: dict, replacement: dict) -> str:
    source = git_text(doc["source_ref"], replacement["path"])
    start, end = bounds(source, replacement)
    return source[start:end]


def apply_replacement(current: str, replacement: dict, candidate: str) -> str:
    start, end = bounds(current, replacement)
    return current[:start] + candidate.rstrip() + "\n\n" + current[end:]


def emit_base64(path: str, content: str) -> None:
    encoded = base64.b64encode(content.encode("utf-8")).decode("ascii")
    print(f"BEGIN_MIGRATION_B64 {path}")
    for offset in range(0, len(encoded), 76):
        print(encoded[offset : offset + 76])
    print(f"END_MIGRATION_B64 {path}")


def main() -> None:
    if git_bytes("rev-parse", f"{BASE_REF}^{{commit}}").decode().strip() != BASE_REF:
        raise AssertionError("Phase C base ref did not resolve exactly")
    if git_bytes("rev-parse", f"{SEMANTIC_BASELINE}^{{commit}}").decode().strip() != SEMANTIC_BASELINE:
        raise AssertionError("semantic baseline did not resolve exactly")
    git_bytes("merge-base", "--is-ancestor", SEMANTIC_BASELINE, BASE_REF)
    git_bytes("merge-base", "--is-ancestor", BASE_REF, "HEAD")

    original = {path: git_text(BASE_REF, path) for path in TARGETS}
    expected = dict(original)
    touched: set[str] = set()

    for experiment_path in EXPERIMENTS:
        doc = json.loads((ROOT / experiment_path).read_text(encoding="utf-8"))
        if doc.get("semantic_change_allowed") is not False or doc.get("canonical_runtime_changed_during_prototype") is not False:
            raise AssertionError(f"selected experiment is not representation-only: {doc.get('experiment_id')}")
        if doc.get("semantic_baseline_ref") != SEMANTIC_BASELINE:
            raise AssertionError(f"selected experiment semantic baseline drifted: {doc.get('experiment_id')}")
        if git_bytes("rev-parse", f"{doc['source_ref']}^{{commit}}").decode().strip() != doc["source_ref"]:
            raise AssertionError(f"selected source ref did not resolve: {doc.get('experiment_id')}")

        for replacement in normalized_replacements(doc):
            path = replacement["path"]
            if path not in TARGETS:
                raise AssertionError(f"unexpected Phase C target path: {path}")
            base_start, base_end = bounds(original[path], replacement)
            base_section = original[path][base_start:base_end]
            reviewed_section = replacement_source_section(doc, replacement)
            if base_section != reviewed_section:
                raise AssertionError(
                    f"selected target surface drifted since prototype review: {doc.get('experiment_id')} {path}"
                )
            candidate_path = ROOT / replacement["candidate_section"]
            candidate = candidate_path.read_text(encoding="utf-8")
            expected[path] = apply_replacement(expected[path], replacement, candidate)
            touched.add(path)

    if touched != TARGETS:
        raise AssertionError(f"Phase C target set drifted: {sorted(touched)}")

    # Representation-only namespace and preserved post-v1.2.2 behavior checks.
    for path in TARGETS:
        if set(STATE_RE.findall(expected[path])) != set(STATE_RE.findall(original[path])):
            raise AssertionError(f"state/boundary token surface changed in {path}")
    relay_literal = "Every machine relay emitted in a user-visible response is automatically a copy/paste artifact"
    if relay_literal not in original["skill/SKILL.md"] or relay_literal not in expected["skill/SKILL.md"]:
        raise AssertionError("accepted v1.2.3 complete-response relay behavior was not preserved")

    # Materialize exact combined runtime and run the normal validator.
    with tempfile.TemporaryDirectory(prefix="gpo-phase-c-") as tmp:
        root = Path(tmp)
        safe_extract(git_bytes("archive", "--format=tar", BASE_REF, "skill"), root)
        for path, content in expected.items():
            (root / path).write_text(content, encoding="utf-8")
        for path in ("design/RULE-MAP.md", "design/GOAL-MAP.md", "docs/PROJECT-SPEC.md"):
            dst = root / path
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(git_bytes("show", f"{BASE_REF}:{path}"))
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "validate_skill.py"), str(root / "skill")],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode:
            raise AssertionError(result.stderr.strip() or result.stdout.strip())

    # If canonical files are already migrated on this branch, require exact equality.
    current_head = git_bytes("rev-parse", "HEAD^{commit}").decode().strip()
    canonical_differences = []
    for path in sorted(TARGETS):
        head_content = git_text(current_head, path)
        if head_content != expected[path]:
            canonical_differences.append(path)
    if canonical_differences:
        print("PHASE_C_CANONICAL_PENDING=" + ",".join(canonical_differences))
    else:
        print("PASS Phase C canonical runtime exactly matches selected materialization")

    print("PASS Phase C selected P1-P5 materialization validates")
    print("PASS Phase C selected source surfaces have no unreviewed drift")
    for path in sorted(TARGETS):
        emit_base64(path, expected[path])


if __name__ == "__main__":
    main()
