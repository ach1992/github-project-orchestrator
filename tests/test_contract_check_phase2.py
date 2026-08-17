#!/usr/bin/env python3
"""Focused Phase 2 compatibility checks for the Task Contract validator."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skill" / "scripts" / "contract_check.py"

spec = importlib.util.spec_from_file_location("contract_check", SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Unable to load {SCRIPT}")
contract_check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract_check)

SHA0 = "a" * 40
SHA1 = "b" * 40
BASE = f"""## Goal
Ship ontology normalization.

## Scope
In: assignment schema.
Out: policy changes.

## Acceptance
- [ ] Validator is deterministic.

## Validation
Run targeted checks.

## Dependencies
none

## Risk / Release
Risk: LOW

Issue: ach1992/github-project-orchestrator#5
Assignment ID: 5-g1
Contract Revision: 1
Base SHA: {SHA0}
Assigned Branch: worker/5
Integration Target: main
Worker: W1
Assignment Status: ACTIVE
Task Risk: LOW
"""


def check(name: str, text: str, expected: bool, contains: str | None = None) -> None:
    result = contract_check.validate(text, "substantive", True)
    if result["ok"] != expected:
        raise AssertionError(f"{name}: expected ok={expected}, got {result}")
    if contains and not any(contains in error for error in result["errors"]):
        raise AssertionError(f"{name}: missing error {contains!r}: {result['errors']}")
    print(f"PASS {name}")


def main() -> None:
    check(
        "canonical-standard-high",
        BASE
        + f"""Start HEAD: {SHA0}
Checkpoint HEAD: {SHA1}
Project Authority: AUTONOMOUS_WITH_GATES
Coordination Baseline: STANDARD
Assurance Level: HIGH_ASSURANCE
Scoped Authorization: none
Delivery Requirement: DELIVERY_REQUIRED
Delivery Target: production
Delivery State: NOT_STARTED
""",
        True,
    )

    check(
        "legacy-standard",
        BASE
        + f"""Expected Starting HEAD: {SHA0}
Authority: MANAGED
Operating Profile: STANDARD
""",
        True,
    )

    check(
        "legacy-lightweight",
        BASE
        + f"""Expected Starting HEAD: {SHA0}
Authority: AUTONOMOUS_WITH_GATES
Operating Profile: LIGHTWEIGHT
""",
        True,
    )

    check(
        "legacy-high-ambiguous",
        BASE
        + f"""Expected Starting HEAD: {SHA0}
Authority: MANAGED
Operating Profile: HIGH_ASSURANCE
""",
        False,
        "ambiguous without a persisted Coordination Baseline",
    )

    check(
        "transitional-high-with-baseline",
        BASE
        + f"""Expected Starting HEAD: {SHA0}
Authority: MANAGED
Coordination Baseline: STANDARD
Operating Profile: HIGH_ASSURANCE
""",
        True,
    )

    check(
        "canonical-and-legacy-authority",
        BASE
        + f"""Start HEAD: {SHA0}
Project Authority: MANAGED
Authority: MANAGED
Coordination Baseline: STANDARD
Assurance Level: NORMAL
""",
        False,
        "use Project Authority or legacy Authority",
    )

    check(
        "bad-checkpoint",
        BASE
        + f"""Start HEAD: {SHA0}
Checkpoint HEAD: short
Project Authority: MANAGED
Coordination Baseline: STANDARD
Assurance Level: NORMAL
""",
        False,
        "Checkpoint HEAD must be a non-zero full Git commit SHA",
    )

    check(
        "same-branch-target",
        BASE.replace("Integration Target: main", "Integration Target: refs/heads/worker/5")
        + f"""Start HEAD: {SHA0}
Project Authority: MANAGED
Coordination Baseline: STANDARD
Assurance Level: NORMAL
""",
        False,
        "Assigned Branch must differ from Integration Target",
    )

    check(
        "zero-start",
        BASE
        + f"""Start HEAD: {'0' * 40}
Project Authority: MANAGED
Coordination Baseline: STANDARD
Assurance Level: NORMAL
""",
        False,
        "Start HEAD must be a non-zero full Git commit SHA",
    )


if __name__ == "__main__":
    main()
