#!/usr/bin/env python3
"""Exact composition guards for the Phase C P1-P5 canonical runtime migration."""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "0165bc2a26bdf7452f05160c3e91f47b4fa7ae9c"

SKILL = "skill/SKILL.md"
AUTHORITY = "skill/references/authority-gates.md"
WORKER = "skill/references/worker-protocol.md"
MASTER = "skill/references/master-cycle.md"
CONTINUITY = "skill/references/continuity.md"

P1 = ROOT / "benchmarks/phase7/experiments/runtime-dimension-invariants-v2"
P2 = ROOT / "benchmarks/phase7/experiments/worker-assignment-owner-dedup-v1"
P3 = ROOT / "benchmarks/phase7/experiments/pending-job-decision-structure-v1"
P4 = ROOT / "benchmarks/phase7/experiments/write-unknown-canonical-algorithm-v1"
P5 = ROOT / "benchmarks/phase7/experiments/progressive-recovery-procedure-v1"


def current(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def base(path: str) -> str:
    return subprocess.run(
        ["git", "show", f"{BASE}:{path}"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout


def candidate(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_between(text: str, start: str, end: str) -> tuple[str, str, str]:
    assert text.count(start) == 1, start
    assert text.count(end) == 1, end
    i = text.index(start)
    j = text.index(end)
    assert i < j
    return text[:i], text[i:j], text[j:]


def assert_one_replacement(path: str, start: str, end: str, expected: str) -> None:
    old_before, _, old_after = split_between(base(path), start, end)
    new_before, new_mid, new_after = split_between(current(path), start, end)
    assert new_before == old_before, f"unexpected bytes before selected migration surface in {path}"
    assert new_after == old_after, f"unexpected bytes after selected migration surface in {path}"
    assert new_mid == expected, f"canonical section does not equal selected prototype in {path}"


def test_p1() -> None:
    assert_one_replacement(
        SKILL,
        "## 1. Role and runtime state",
        "## 2. Universal invariants",
        candidate(P1 / "candidate-skill-section.md"),
    )
    assert_one_replacement(
        AUTHORITY,
        "## 1. Decision dimensions",
        "## 2. Applicable effects",
        candidate(P1 / "candidate-authority-section.md"),
    )


def test_p2() -> None:
    assert_one_replacement(
        WORKER,
        "## 1. Isolation",
        "## 2. Dispatch prompt",
        candidate(P2 / "candidate-worker-isolation.md"),
    )


def test_p3() -> None:
    marker = "For already-running CI/check/deployment/job, `pending` is dependency state, not failure."
    assert_one_replacement(
        MASTER,
        marker,
        "## 10. Requirement changes",
        candidate(P3 / "candidate-pending-job.md"),
    )


def test_p4() -> None:
    assert_one_replacement(
        AUTHORITY,
        "## 6. `WriteState.UNKNOWN`",
        "## 7. Optimistic concurrency",
        candidate(P4 / "candidate-write-unknown.md"),
    )


def test_p5() -> None:
    marker = "For multi-repository outcomes, recover the small global coordination spine first:"
    assert_one_replacement(
        CONTINUITY,
        "## 2. Recovery sequence",
        marker,
        candidate(P5 / "candidate-recovery.md"),
    )


def test_runtime_surface() -> None:
    changed = subprocess.run(
        ["git", "diff", "--name-only", BASE, "HEAD", "--", "skill"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout.splitlines()
    assert set(changed) == {SKILL, AUTHORITY, WORKER, MASTER, CONTINUITY}

    baseline_relay = (
        "Every machine relay emitted in a user-visible response is automatically a copy/paste artifact: "
        "the entire response must be exactly one copy-target fenced code block containing the complete relay"
    )
    assert baseline_relay in base(SKILL)
    assert baseline_relay in current(SKILL)


def main() -> None:
    test_p1()
    test_p2()
    test_p3()
    test_p4()
    test_p5()
    test_runtime_surface()
    print("Phase C P1-P5 runtime migration composition: PASS")


if __name__ == "__main__":
    main()
