#!/usr/bin/env python3
"""Scope and semantic guards for the refined Phase C P1-P5 runtime migration."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "0165bc2a26bdf7452f05160c3e91f47b4fa7ae9c"

SKILL = "skill/SKILL.md"
AUTHORITY = "skill/references/authority-gates.md"
WORKER = "skill/references/worker-protocol.md"
MASTER = "skill/references/master-cycle.md"
CONTINUITY = "skill/references/continuity.md"
RUNTIME_PATHS = (SKILL, AUTHORITY, WORKER, MASTER, CONTINUITY)

P4 = ROOT / "benchmarks/phase7/experiments/write-unknown-canonical-algorithm-v1"
STATE_TOKEN = re.compile(
    r"\b(?:TaskState|WorkerStatus|WriteState|DeliveryState|MasterBoundary)\.[A-Z_]+\b"
)


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
    return path.read_text(encoding="utf-8").rstrip("\n") + "\n\n"


def extract_between(text: str, start: str, end: str) -> str:
    assert text.count(start) == 1, start
    assert text.count(end) == 1, end
    i = text.index(start)
    j = text.index(end)
    assert i < j
    return text[i:j]


def mask_regions(text: str, regions: tuple[tuple[str, str], ...]) -> str:
    """Replace only declared migration surfaces with stable sentinels."""
    for index, (start, end) in enumerate(regions):
        assert text.count(start) == 1, start
        assert text.count(end) == 1, end
        i = text.index(start)
        j = text.index(end)
        assert i < j
        text = text[:i] + f"<PHASE_C_REGION_{index}>\n" + text[j:]
    return text


def assert_only_regions(path: str, regions: tuple[tuple[str, str], ...]) -> None:
    assert mask_regions(current(path), regions) == mask_regions(base(path), regions), (
        f"{path} changed outside declared Phase C representation surfaces"
    )


def require_all(text: str, fragments: tuple[str, ...]) -> None:
    for fragment in fragments:
        assert fragment in text, fragment


def test_declared_runtime_scope_only() -> None:
    assert_only_regions(
        SKILL,
        (("## 1. Role and runtime state", "## 2. Universal invariants"),),
    )
    assert_only_regions(
        AUTHORITY,
        (
            ("## 1. Decision dimensions", "## 2. Applicable effects"),
            ("## 6. `WriteState.UNKNOWN`", "## 7. Optimistic concurrency"),
        ),
    )
    assert_only_regions(
        WORKER,
        (("## 1. Isolation", "## 2. Dispatch prompt"),),
    )
    assert_only_regions(
        MASTER,
        (
            (
                "For already-running CI/check/deployment/job, `pending` is dependency state, not failure.",
                "## 10. Requirement changes",
            ),
        ),
    )
    assert_only_regions(
        CONTINUITY,
        (
            (
                "## 2. Recovery sequence",
                "For multi-repository outcomes, recover the small global coordination spine first:",
            ),
        ),
    )

    changed = subprocess.run(
        ["git", "diff", "--name-only", BASE, "HEAD", "--", "skill"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout.splitlines()
    assert set(changed) == set(RUNTIME_PATHS)


def test_p1_runtime_dimensions_are_lossless_and_owned() -> None:
    skill = extract_between(current(SKILL), "## 1. Role and runtime state", "## 2. Universal invariants")
    authority = extract_between(current(AUTHORITY), "## 1. Decision dimensions", "## 2. Applicable effects")

    require_all(
        skill,
        (
            "Retain the current value until the actual assignment basis changes.",
            "Retain the current value until the actual authorization basis changes.",
            "may constrain execution but never broaden `ProjectAuthority`",
            "chat/Master rotation alone never makes it more permissive",
            "exact action/target/effect grant; never a project-wide authority upgrade",
            "Retain the current value until the actual coordination basis changes, including across Master rotation.",
            "`STANDARD` remains compatible with FAST execution and never implies FULL.",
            "additive only for affected work when risk, policy, or explicit authorized controls justify it",
            "never removes baseline controls or by itself implies approval or FULL execution",
            "return to `NORMAL` when that escalation ends",
            "classified per substantive change only when decision-relevant",
            "These dimensions remain orthogonal unless a canonical rule explicitly connects them.",
            "Project/repository size alone does not select `STANDARD` or `HIGH_ASSURANCE`.",
            "Infer safely instead of asking the user to choose ceremony.",
        ),
    )
    assert "`KEEP` until" not in skill

    require_all(
        authority,
        (
            "as independent inputs to gate evaluation",
            "Technical capability and environment remain separate execution constraints.",
            "owns authorization/action-gate interpretation",
            "`ProjectAuthority` is the project-wide authorization envelope for normal reversible mutation.",
            "changes only from applicable explicit user or higher-level authorization",
            "may constrain execution but never grant or widen it",
            "may authorize that exact action or satisfy only the applicable gate for it",
            "without converting the broader project to a more permissive `ProjectAuthority`",
            "`CoordinationBaseline` contributes coordination/persistence controls",
            "`STANDARD` does not imply FULL execution",
            "adds evidence/review controls without removing baseline controls",
            "does not by itself create human approval or a different `ProjectAuthority`",
            "`RiskLevel` determines proportional gate/evidence depth for the specific change when decision-relevant",
        ),
    )


def test_p2_worker_schema_and_preedit_behavior_stay_distinct() -> None:
    worker = extract_between(current(WORKER), "## 1. Isolation", "## 2. Dispatch prompt")
    require_all(
        worker,
        (
            "Use a dedicated worktree when useful for isolation; its filesystem path is runtime location, not assignment identity.",
            "[task-contract.md](task-contract.md) §8 owns the persisted Worker assignment/concurrency envelope.",
            "current assigned-branch/worktree attachment, state, and safety",
            "verify the current persisted assignment envelope from §8",
            "current assigned-branch/worktree HEAD = immutable `Start HEAD`",
            "later authorized same-generation commits may advance beyond it without staleness",
            "current assigned-branch HEAD = Master-supplied `Checkpoint HEAD`",
            "Any material identity/checkpoint mismatch -> `WorkerStatus.STALE_ASSIGNMENT`; never guess.",
            "never broadens assignment because Master is unavailable",
        ),
    )


def test_p3_pending_job_branches_are_discriminated() -> None:
    marker = "For already-running CI/check/deployment/job, `pending` is dependency state, not failure."
    pending = extract_between(current(MASTER), marker, "## 10. Requirement changes")
    require_all(
        pending,
        (
            "Continue independent useful work first.",
            "Once no independent useful work remains and `pending` is the sole dependency",
            "dependency is still pending; independent useful work still exists | Continue it before waiting",
            "no independent useful work remains; `pending` is the sole dependency; a safe runtime-supported continuation path is available and still reasonable",
            "without inventing precedence",
            "bounded, non-tight authoritative rechecks only when a transition is plausibly due",
            "a suitable real event/condition resume primitive",
            "dependency resolves successfully | Immediately continue the existing workflow; do not require a user nudge.",
            "dependency fails | Stop waiting immediately, classify the failure",
            "dependency is still pending; no independent useful work remains; it is the sole remaining blocker; bounded autonomous continuation is unavailable, no longer reasonable, or exhausted",
            "Never tight-poll, sleep indefinitely, fabricate background monitoring/resume, or manufacture work.",
            "`DeliveryState.PENDING` remains a lifecycle state, not a terminal boundary label",
            "never use `MasterBoundary.NO_READY_WORK` merely because an already-running required dependency is unfinished",
        ),
    )
    # Combined transitions must remain disjoint without relying on row order:
    # PENDING+independent, PENDING+continuation, SUCCESS+independent,
    # FAILED+independent, and PENDING+exhausted each have one condition class.
    conditions = {
        match.strip()
        for match in re.findall(r"^\| ([^|]+?) \|", pending, flags=re.MULTILINE)
        if match.strip() not in {"Current condition", "---"}
    }
    assert conditions == {
        "dependency is still pending; independent useful work still exists",
        "no independent useful work remains; `pending` is the sole dependency; a safe runtime-supported continuation path is available and still reasonable",
        "dependency resolves successfully",
        "dependency fails",
        "dependency is still pending; no independent useful work remains; it is the sole remaining blocker; bounded autonomous continuation is unavailable, no longer reasonable, or exhausted",
    }
    assert "independent useful work still exists" not in conditions


def test_p4_write_unknown_remains_exact_selected_algorithm() -> None:
    current_fragment = extract_between(
        current(AUTHORITY),
        "## 6. `WriteState.UNKNOWN`",
        "## 7. Optimistic concurrency",
    )
    assert current_fragment == embedded_candidate(P4 / "candidate-write-unknown.md")


def test_p5_recovery_is_progressive_without_forcing_a_third_phase() -> None:
    recovery = extract_between(
        current(CONTINUITY),
        "## 2. Recovery sequence",
        "For multi-repository outcomes, recover the small global coordination spine first:",
    )
    require_all(
        recovery,
        (
            "Recover progressively: start with orientation, enter the active path normally, and widen only when a concrete trigger makes deeper context decision-relevant.",
            "`Triggered depth` is a conditional side path that may become necessary from orientation or from the active path; it is not a mandatory third phase.",
            "**Orientation spine — always first.**",
            "Project Map or equivalent truth-location index",
            "Before establishing any still-unresolved conclusion below, follow only the minimum live control-plane pointers",
            "active Issue/Project/milestone and PR/branch/check/dependency state",
            "Then establish the active project outcome/completion condition",
            "active project outcome/completion condition",
            "recover `ProjectAuthority` and `CoordinationBaseline` independently",
            "recover any affected-chain `AssuranceLevel` and exact current `ScopedAuthorization`",
            "chat loss alone is not a trigger",
            "enter only that needed depth now rather than forcing unrelated active-path reading first",
            "**Active-path context — normal next layer.**",
            "**Triggered depth — conditional side path.**",
            "Load the root specification when project-level intent cannot be established safely from current downstream authoritative state or when material contradiction/change makes it decision-relevant.",
            "Stop recovery reading once repository/target identity, active outcome, controlling dependencies/blockers",
            "Continue the valid plan instead of rebuilding it because chat history is absent.",
            "A large repository or long-lived project is a reason to narrow recovery by workstream, not to read more by default.",
        ),
    )
    orientation = extract_between(
        recovery,
        "- **Orientation spine — always first.**",
        "- **Active-path context — normal next layer.**",
    )
    discovery = "Before establishing any still-unresolved conclusion below"
    conclusion = "Then establish the active project outcome/completion condition"
    # Zero chat + no useful status hint + Project Map as pointers only must still read
    # the minimum live control plane before deriving outcome/Authority/critical path.
    assert orientation.index("Project Map or equivalent truth-location index") < orientation.index(discovery)
    assert orientation.index(discovery) < orientation.index(conclusion)
    assert "from the applicable authoritative evidence" in orientation
    assert "chat loss alone is not a trigger" in orientation
    assert "| Recovery layer | Required work |" not in recovery


def test_state_namespaces_and_machine_relay_stay_unchanged() -> None:
    for path in RUNTIME_PATHS:
        assert set(STATE_TOKEN.findall(current(path))) == set(STATE_TOKEN.findall(base(path))), path

    baseline_relay = (
        "Every machine relay emitted in a user-visible response is automatically a copy/paste artifact: "
        "the entire response must be exactly one copy-target fenced code block containing the complete relay"
    )
    assert baseline_relay in base(SKILL)
    assert baseline_relay in current(SKILL)


def main() -> None:
    test_declared_runtime_scope_only()
    test_p1_runtime_dimensions_are_lossless_and_owned()
    test_p2_worker_schema_and_preedit_behavior_stay_distinct()
    test_p3_pending_job_branches_are_discriminated()
    test_p4_write_unknown_remains_exact_selected_algorithm()
    test_p5_recovery_is_progressive_without_forcing_a_third_phase()
    test_state_namespaces_and_machine_relay_stay_unchanged()
    print("Phase C refined P1-P5 runtime migration guards: PASS")


if __name__ == "__main__":
    main()
