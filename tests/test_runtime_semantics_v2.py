#!/usr/bin/env python3
"""Semantic runtime guard for the simplified GitHub Project Orchestrator."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill"

RUNTIME_REFS = [
    "authority-gates.md",
    "continuity.md",
    "engineering-quality.md",
    "governance.md",
    "independent-review.md",
    "interface-specialist.md",
    "master-cycle.md",
    "relay-transport.md",
    "release.md",
    "review-integration.md",
    "task-contract.md",
    "worker-protocol.md",
]


def text(path: str) -> str:
    return (SKILL / path).read_text(encoding="utf-8")


def require(label: str, source: str, terms: tuple[str, ...]) -> None:
    missing = [term for term in terms if term.lower() not in source.lower()]
    if missing:
        raise AssertionError(f"{label}: missing semantic anchors: {missing}")


def main() -> None:
    kernel = text("SKILL.md")
    refs = {name: text(f"references/{name}") for name in RUNTIME_REFS}

    kernel_words = len(kernel.split())
    runtime_words = kernel_words + sum(len(value.split()) for value in refs.values())
    package_files = [path for path in SKILL.rglob("*") if path.is_file() and "__pycache__" not in path.parts]
    package_words = sum(len(path.read_text(encoding="utf-8").split()) for path in package_files)
    if kernel_words > 900:
        raise AssertionError(f"always-loaded kernel grew above 900 words: {kernel_words}")
    if runtime_words > 8000:
        raise AssertionError(f"routine runtime surface grew above 8000 words: {runtime_words}")
    if package_words > 10000:
        raise AssertionError(f"packaged Skill source grew above 10000 words: {package_words}")
    forbidden_package_paths = (
        SKILL / "references/eval-scenarios.md",
        SKILL / "scripts/contract_check.py",
    )
    leaked_paths = [str(path.relative_to(SKILL)) for path in forbidden_package_paths if path.exists()]
    if leaked_paths:
        raise AssertionError(f"development/legacy machinery leaked into runtime package: {leaked_paths}")

    obsolete_hot_states = (
        "CoordinationBaseline",
        "AssuranceLevel",
        "ExecutionPath",
        "ContractPersistence",
        "TaskState",
        "MasterBoundary",
        "WriteState",
        "DeliveryState",
        "ApplicableEffects",
        "REVIEW_VALID",
        "CAN_EXECUTE",
    )
    leaked = [name for name in obsolete_hot_states if name in kernel]
    if leaked:
        raise AssertionError(f"obsolete orchestration state leaked into hot kernel: {leaked}")

    require(
        "kernel",
        kernel,
        (
            "implement a coherent batch",
            "targeted high-signal checks",
            "stabilize the candidate",
            "required broad/exact-candidate gates",
            "review the effective diff",
            "verify delivery",
            "MACHINE_RELAY_OUTPUT_OK(response)",
        ),
    )
    require(
        "authority",
        refs["authority-gates.md"],
        (
            "Repository mutation scope is an allowlist",
            "Production requires human approval",
            "Ambiguous write outcome",
            "Optimistic concurrency",
            "related repositories",
        ),
    )
    require(
        "governance",
        refs["governance.md"],
        (
            "discover -> reuse/update -> create only when absence is established -> verify",
            "one canonical repository copy",
            "one meaningful work item",
            "CI bottlenecks",
        ),
    )
    require(
        "planning",
        refs["master-cycle.md"],
        (
            "minimum meaningful slices",
            "Self-execute when delegation would cost as much as it saves",
            "broad suites/CI as acceptance evidence near candidate stability",
            "material adjacent improvement outside current outcome",
            "Do not invent cleanup",
        ),
    )
    require(
        "worker",
        refs["worker-protocol.md"],
        (
            "Assignment ID",
            "Assigned Branch",
            "Integration Target",
            "STALE_ASSIGNMENT",
            "READY_FOR_REVIEW",
            "Do not integrate/release",
        ),
    )
    require(
        "review",
        refs["review-integration.md"],
        (
            "exact candidate/HEAD",
            "prior approval/verdict never automatically transfers",
            "targeted checks first when informative",
            "required tests/CI/approvals complete for the current candidate",
            "one independent review after candidate stabilization",
        ),
    )
    require(
        "independent review",
        refs["independent-review.md"],
        (
            "Reviewer authority: READ_ONLY",
            "novel adversarial probes",
            "Completion: COMPLETE | INCOMPLETE",
            "APPROVE",
            "exact delta",
        ),
    )
    require(
        "release",
        refs["release.md"],
        (
            "Integration is not delivery",
            "artifact/commit/config",
            "rollback or roll-forward",
            "delivery as unproven/failed",
        ),
    )
    require(
        "continuity",
        refs["continuity.md"],
        (
            "authoritative project systems",
            "prior chat/summary is a locator",
            "replacement Master",
            "Do not copy full project history",
        ),
    )
    require(
        "relay",
        refs["relay-transport.md"],
        (
            "MACHINE_RELAY_OUTPUT_OK(response)",
            "exactly_one_copy_target_fenced_block",
            "no_visible_content_before_or_after_block",
        ),
    )

    print(
        f"PASS simplified-runtime-semantics kernel_words={kernel_words} "
        f"runtime_words={runtime_words} package_words={package_words}"
    )


if __name__ == "__main__":
    main()
