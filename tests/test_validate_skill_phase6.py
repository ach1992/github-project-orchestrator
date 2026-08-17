#!/usr/bin/env python3
"""Targeted negative/compatibility fixtures for Phase 6 deterministic lint."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_skill.py"
CONTRACT_CHECK = ROOT / "skill" / "scripts" / "contract_check.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_module("validate_skill", VALIDATOR)
contract_check = load_module("contract_check_phase6", CONTRACT_CHECK)


def expect_failure(name: str, action, contains: str) -> None:
    try:
        action()
    except ValueError as exc:
        if contains not in str(exc):
            raise AssertionError(f"{name}: expected error containing {contains!r}, got {exc!r}") from exc
        print(f"PASS {name}")
        return
    raise AssertionError(f"{name}: expected ValueError containing {contains!r}")


def write_trace_fixture(root: Path) -> tuple[Path, Path, Path, Path]:
    skill = root / "skill"
    references = skill / "references"
    design = root / "design"
    docs = root / "docs"
    references.mkdir(parents=True)
    design.mkdir()
    docs.mkdir()
    (skill / "SKILL.md").write_text("---\nname: fixture\ndescription: fixture\n---\n", encoding="utf-8")

    eval_path = references / "eval-scenarios.md"
    eval_path.write_text("### A. One\n\n### B. Two\n", encoding="utf-8")

    rule_path = design / "RULE-MAP.md"
    rule_path.write_text(
        "| Rule ID | Guarantee | Canonical owner | Source anchors | Eval anchors |\n"
        "|---|---|---|---|---|\n"
        "| `RULE-ONE` | first | `a.md` | x | A |\n"
        "| `RULE-TWO` | second | `b.md` | y | B |\n",
        encoding="utf-8",
    )

    project_path = docs / "PROJECT-SPEC.md"
    project_path.write_text(
        "| ID | Goal |\n|---|---|\n| `G01` | One |\n| `G02` | Two |\n",
        encoding="utf-8",
    )

    goal_path = design / "GOAL-MAP.md"
    goal_path.write_text(
        "| Goal | Primary rule families / Rule IDs | Existing evaluation anchors | Additional coverage |\n"
        "|---|---|---|---|\n"
        "| `G01` One | `RULE-ONE` | A | x |\n"
        "| `G02` Two | `RULE-TWO` | B | y |\n",
        encoding="utf-8",
    )
    return skill, eval_path, rule_path, goal_path


def traceability_tests() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        skill, eval_path, rule_path, goal_path = write_trace_fixture(root)
        validator.validate_traceability(root, skill)
        print("PASS traceability-valid")

        eval_path.write_text("### A. One\n\n### A. Duplicate\n", encoding="utf-8")
        expect_failure(
            "eval-duplicate",
            lambda: validator.validate_traceability(root, skill),
            "Duplicate evaluation scenario IDs",
        )
        eval_path.write_text("### A. One\n\n### C. Three\n", encoding="utf-8")
        expect_failure(
            "eval-gap",
            lambda: validator.validate_traceability(root, skill),
            "Evaluation scenario ID gaps detected: ['B']",
        )
        eval_path.write_text("### A. One\n\n### B. Two\n", encoding="utf-8")

        original_rules = rule_path.read_text(encoding="utf-8")
        rule_path.write_text(original_rules + "| `RULE-ONE` | duplicate | `c.md` | z | A |\n", encoding="utf-8")
        expect_failure(
            "rule-duplicate-owner",
            lambda: validator.validate_traceability(root, skill),
            "Duplicate canonical Rule rows/owners",
        )
        rule_path.write_text(original_rules, encoding="utf-8")

        original_goals = goal_path.read_text(encoding="utf-8")
        goal_path.write_text(original_goals.replace("`RULE-TWO`", "`RULE-ONE`"), encoding="utf-8")
        expect_failure(
            "rule-orphan",
            lambda: validator.validate_traceability(root, skill),
            "Canonical Rule IDs are not mapped to any Goal",
        )
        goal_path.write_text(original_goals.replace("`RULE-TWO`", "`RULE-THREE`"), encoding="utf-8")
        expect_failure(
            "goal-unknown-rule",
            lambda: validator.validate_traceability(root, skill),
            "references unknown Rule IDs",
        )
        goal_path.write_text(original_goals, encoding="utf-8")

        rule_path.write_text(original_rules.replace("| B |", "| Z |"), encoding="utf-8")
        expect_failure(
            "rule-missing-eval",
            lambda: validator.validate_traceability(root, skill),
            "references missing evaluation IDs: ['Z']",
        )


def state_tests() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        skill = Path(tmp) / "skill"
        refs = skill / "references"
        refs.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "`TaskState.INTEGRATED` `WorkerStatus.READY_FOR_REVIEW` `WriteState.UNKNOWN` "
            "`DeliveryState.PENDING` `MasterBoundary.BLOCKED`\n",
            encoding="utf-8",
        )
        (refs / "states.md").write_text("`WorkerStatus.STALE_ASSIGNMENT`\n", encoding="utf-8")
        validator.validate_state_tokens(skill)
        print("PASS state-valid")
        (refs / "states.md").write_text("`WorkerStatus.DONE`\n", encoding="utf-8")
        expect_failure(
            "state-legacy-token",
            lambda: validator.validate_state_tokens(skill),
            "WorkerStatus.DONE",
        )


SHA0 = "a" * 40
WORKER_BASE = f"""## Goal
Validate worker identity.

## Scope
In: deterministic schema.
Out: qualitative READY judgment.

## Acceptance
- [ ] Invalid identity combinations fail deterministically.

## Validation
Run Phase 6 fixtures.

## Dependencies
none

## Risk / Release
Risk: LOW

Issue: owner/repo#9
Assignment ID: 9-g1
Contract Revision: 1
Base SHA: {SHA0}
Assigned Branch: worker/9
Integration Target: main
Worker: W9
Assignment Status: ACTIVE
Task Risk: LOW
Start HEAD: {SHA0}
Project Authority: MANAGED
Coordination Baseline: STANDARD
Assurance Level: NORMAL
"""


def contract_result(text: str) -> dict:
    return contract_check.validate(text, "substantive", True)


def expect_contract_failure(name: str, text: str, contains: str) -> None:
    result = contract_result(text)
    if result["ok"]:
        raise AssertionError(f"{name}: expected failure, got {result}")
    if not any(contains in error for error in result["errors"]):
        raise AssertionError(f"{name}: missing {contains!r}: {result['errors']}")
    print(f"PASS {name}")


def worker_contract_tests() -> None:
    valid = contract_result(WORKER_BASE)
    if not valid["ok"]:
        raise AssertionError(f"worker-valid: {valid}")
    print("PASS worker-valid")

    expect_contract_failure(
        "worker-advisory-authority",
        WORKER_BASE.replace("Project Authority: MANAGED", "Project Authority: ADVISORY"),
        "must be MANAGED or AUTONOMOUS_WITH_GATES",
    )
    expect_contract_failure(
        "worker-invalid-baseline",
        WORKER_BASE.replace("Coordination Baseline: STANDARD", "Coordination Baseline: HIGH_ASSURANCE"),
        "Coordination Baseline must be LIGHTWEIGHT or STANDARD",
    )
    expect_contract_failure(
        "worker-invalid-assurance",
        WORKER_BASE.replace("Assurance Level: NORMAL", "Assurance Level: STANDARD"),
        "Assurance Level must be NORMAL or HIGH_ASSURANCE",
    )
    expect_contract_failure(
        "worker-inactive-dispatch",
        WORKER_BASE.replace("Assignment Status: ACTIVE", "Assignment Status: COMPLETE"),
        "Assignment Status must be ACTIVE",
    )
    expect_contract_failure(
        "worker-target-equals-branch",
        WORKER_BASE.replace("Integration Target: main", "Integration Target: refs/heads/worker/9"),
        "Assigned Branch must differ from Integration Target",
    )


def main() -> None:
    traceability_tests()
    state_tests()
    worker_contract_tests()


if __name__ == "__main__":
    main()
