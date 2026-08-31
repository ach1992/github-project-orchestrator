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


def embedded_candidate(path: Path) -> str:
    """Normalize only the Markdown section separator, not candidate content."""
    return path.read_text(encoding="utf-8").rstrip("\n") + "\n\n"


def replace_between(text: str, start: str, end: str, replacement: str) -> str:
    assert text.count(start) == 1, start
    assert text.count(end) == 1, end
    i = text.index(start)
    j = text.index(end)
    assert i < j
    return text[:i] + replacement + text[j:]


def expected_skill() -> str:
    return replace_between(
        base(SKILL),
        "## 1. Role and runtime state",
        "## 2. Universal invariants",
        embedded_candidate(P1 / "candidate-skill-section.md"),
    )


def expected_authority() -> str:
    text = replace_between(
        base(AUTHORITY),
        "## 1. Decision dimensions",
        "## 2. Applicable effects",
        embedded_candidate(P1 / "candidate-authority-section.md"),
    )
    return replace_between(
        text,
        "## 6. `WriteState.UNKNOWN`",
        "## 7. Optimistic concurrency",
        embedded_candidate(P4 / "candidate-write-unknown.md"),
    )


def expected_worker() -> str:
    return replace_between(
        base(WORKER),
        "## 1. Isolation",
        "## 2. Dispatch prompt",
        embedded_candidate(P2 / "candidate-worker-isolation.md"),
    )


def expected_master() -> str:
    marker = "For already-running CI/check/deployment/job, `pending` is dependency state, not failure."
    return replace_between(
        base(MASTER),
        marker,
        "## 10. Requirement changes",
        embedded_candidate(P3 / "candidate-pending-job.md"),
    )


def expected_continuity() -> str:
    marker = "For multi-repository outcomes, recover the small global coordination spine first:"
    return replace_between(
        base(CONTINUITY),
        "## 2. Recovery sequence",
        marker,
        embedded_candidate(P5 / "candidate-recovery.md"),
    )


def test_exact_composition() -> None:
    expected = {
        SKILL: expected_skill(),
        AUTHORITY: expected_authority(),
        WORKER: expected_worker(),
        MASTER: expected_master(),
        CONTINUITY: expected_continuity(),
    }
    for path, expected_text in expected.items():
        assert current(path) == expected_text, (
            f"{path} differs from exact Phase C base plus selected P1-P5 replacements"
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
    test_exact_composition()
    test_runtime_surface()
    print("Phase C P1-P5 runtime migration composition: PASS")


if __name__ == "__main__":
    main()
