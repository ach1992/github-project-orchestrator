#!/usr/bin/env python3
"""Budget and canonical-rule regression guard for the simplified runtime."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill"
RULE_MAP = ROOT / "design" / "RULE-MAP.md"

RUNTIME_REFS = (
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
)

REQUIRED_WORKER_IDENTITY_LITERALS = (
    "Assignment ID",
    "Contract Revision",
    "Repository",
    "Worker",
    "Base SHA",
    "Assigned Branch",
    "Start HEAD",
    "Checkpoint HEAD",
    "Integration Target",
)

REQUIRED_HIGH_CONSEQUENCE_RULES = {
    "OUTCOME-INTEGRITY",
    "EVIDENCE-TRUTH",
    "MUTATION-IDEMPOTENT",
    "AUTHORITY-SCOPE",
    "PERSISTENT-PROGRESS",
    "VALIDATION-ECONOMICS",
    "DEFENSIVE-SECURITY-CONTINUITY",
    "WORKER-BOUNDED",
    "ASSIGNMENT-IDENTITY",
    "WORKER-HANDOFF-PRECEDENCE",
    "REVIEW-FRESHNESS",
    "INTEGRATION-GATE",
    "RELEASE-MODEL-DISCOVER",
    "DELIVERY-PROOF",
    "RECOVERY-AUTHORITATIVE",
    "MACHINE-RELAY",
    "USER-STOP",
}


def words(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").split())


def main() -> None:
    kernel = SKILL / "SKILL.md"
    kernel_words = words(kernel)
    runtime_words = kernel_words + sum(words(SKILL / "references" / name) for name in RUNTIME_REFS)
    package_words = sum(
        words(path)
        for path in SKILL.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    )

    if kernel_words > 900:
        raise AssertionError(f"always-loaded kernel grew above 900 words: {kernel_words}")
    if runtime_words > 8000:
        raise AssertionError(f"ordinary runtime surface grew above 8000 words: {runtime_words}")
    if (SKILL / "references" / "eval-scenarios.md").exists():
        raise AssertionError("development evaluation leaked back into the packaged runtime")

    task_contract = (SKILL / "references" / "task-contract.md").read_text(encoding="utf-8")
    worker_protocol = (SKILL / "references" / "worker-protocol.md").read_text(encoding="utf-8")
    for literal in REQUIRED_WORKER_IDENTITY_LITERALS:
        if literal not in task_contract or literal not in worker_protocol:
            raise AssertionError(f"Worker identity literal disappeared from runtime: {literal}")

    if "exact `Repository` and assigned `Worker`" not in task_contract:
        raise AssertionError("Task Contract must persist exact Repository and assigned Worker identity")

    dispatch_start = worker_protocol.index("# WORKER DISPATCH")
    dispatch_end = worker_protocol.index("Do not repeat the full project history", dispatch_start)
    dispatch = worker_protocol[dispatch_start:dispatch_end]
    for field in ("Worker: <id>", "Repository: <exact repository>"):
        if field not in dispatch:
            raise AssertionError(f"Worker dispatch lost assignment identity field: {field}")

    handoff_start = worker_protocol.index("# WORKER HANDOFF")
    handoff_end = worker_protocol.index("The handoff is a locator and claim", handoff_start)
    handoff = worker_protocol[handoff_start:handoff_end]
    for field in ("Worker: <id>", "Repository: <exact repository>"):
        if field not in handoff:
            raise AssertionError(f"Worker handoff lost assignment identity field: {field}")

    if "assigned branch must differ from the Integration Target" not in task_contract:
        raise AssertionError("Worker assignment must keep branch/target separation")
    if "`Base SHA` remains the historical integration/stacking basis" not in task_contract:
        raise AssertionError("Worker Base SHA historical integration/stacking role disappeared")
    if "`Start HEAD` is the immutable generation start" not in task_contract:
        raise AssertionError("Worker Start HEAD generation-start role disappeared")
    if "exact `Checkpoint HEAD` for correction/resume" not in task_contract:
        raise AssertionError("Worker Checkpoint HEAD correction/resume role disappeared")
    if "Normal authorized commits on the assigned branch do not make `Start HEAD` stale." not in worker_protocol:
        raise AssertionError("Worker Start HEAD progress/staleness distinction disappeared")

    correction_start = worker_protocol.index("## 6. Correction/resume")
    correction = worker_protocol[correction_start:]
    for phrase in (
        "same assignment generation",
        "reviewed current `Checkpoint HEAD`",
        "Worker verifies that checkpoint before editing",
        "fresh Assignment ID",
    ):
        if phrase not in correction:
            raise AssertionError(f"Worker correction/resume relationship disappeared: {phrase}")

    if "`STALE_ASSIGNMENT`" not in worker_protocol:
        raise AssertionError("Worker stale-assignment status disappeared")

    rule_text = RULE_MAP.read_text(encoding="utf-8")
    rule_ids = set(
        re.findall(r"^\|\s*`([A-Z0-9]+(?:-[A-Z0-9]+)+)`\s*\|", rule_text, re.MULTILINE)
    )
    missing = sorted(REQUIRED_HIGH_CONSEQUENCE_RULES - rule_ids)
    if missing:
        raise AssertionError(f"canonical high-consequence rules disappeared: {missing}")

    print(
        f"PASS simplified-runtime-guard kernel_words={kernel_words} "
        f"runtime_words={runtime_words} package_words={package_words}"
    )


if __name__ == "__main__":
    main()
