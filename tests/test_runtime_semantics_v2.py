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
