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


def supplemental_eval_index_tests() -> None:
    index = (
        "### Supplemental retrieval index\n\n"
        "Rule/Goal anchors are seeds.\n\n"
        "| Change surface | Supplemental eval IDs |\n"
        "|---|---|\n"
        "| fixture | `C` |\n\n"
    )

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        skill, eval_path, rule_path, goal_path = write_trace_fixture(root)
        base = "### A. One\n\n### B. Two\n\n### C. Three\n"

        eval_path.write_text(index + base, encoding="utf-8")
        validator.validate_traceability(root, skill)
        print("PASS supplemental-eval-valid")

        index_without_row = index.replace("| fixture | `C` |\n", "")
        commented_row = index_without_row.replace(
            "|---|---|\n",
            "|---|---|\n<!--\n| fixture | `C` |\n-->\n",
        )
        eval_path.write_text(commented_row + base, encoding="utf-8")
        expect_failure(
            "supplemental-eval-commented-row-not-counted",
            lambda: validator.validate_traceability(root, skill),
            "Unanchored evaluation scenarios are missing from the supplemental retrieval index",
        )

        fenced_row = index_without_row.replace(
            "|---|---|\n",
            "|---|---|\n```text\n| fixture | `C` |\n```\n",
        )
        eval_path.write_text(fenced_row + base, encoding="utf-8")
        expect_failure(
            "supplemental-eval-fenced-row-not-counted",
            lambda: validator.validate_traceability(root, skill),
            "Unanchored evaluation scenarios are missing from the supplemental retrieval index",
        )

        fenced_tilde_row = index_without_row.replace(
            "|---|---|\n",
            "|---|---|\n~~~text\n| fixture | `C` |\n~~~\n",
        )
        eval_path.write_text(fenced_tilde_row + base, encoding="utf-8")
        expect_failure(
            "supplemental-eval-tilde-fenced-row-not-counted",
            lambda: validator.validate_traceability(root, skill),
            "Unanchored evaluation scenarios are missing from the supplemental retrieval index",
        )

        stray_row = index_without_row + "Narrative only.\n\n| fixture | `C` |\n\n"
        eval_path.write_text(stray_row + base, encoding="utf-8")
        expect_failure(
            "supplemental-eval-stray-row-not-counted",
            lambda: validator.validate_traceability(root, skill),
            "Unanchored evaluation scenarios are missing from the supplemental retrieval index",
        )

        base_without_c = "### A. One\n\n### B. Two\n"
        eval_path.write_text(
            index + base_without_c + "<!--\n### C. Hidden fake\n-->\n",
            encoding="utf-8",
        )
        expect_failure(
            "supplemental-eval-commented-heading-not-counted",
            lambda: validator.validate_traceability(root, skill),
            "Supplemental retrieval index references missing evaluation IDs: ['C']",
        )

        eval_path.write_text(
            index + base_without_c + "```text\n### C. Hidden fake\n```\n",
            encoding="utf-8",
        )
        expect_failure(
            "supplemental-eval-fenced-heading-not-counted",
            lambda: validator.validate_traceability(root, skill),
            "Supplemental retrieval index references missing evaluation IDs: ['C']",
        )

        eval_path.write_text(
            index + base_without_c + "~~~text\n### C. Hidden fake\n~~~\n",
            encoding="utf-8",
        )
        expect_failure(
            "supplemental-eval-tilde-fenced-heading-not-counted",
            lambda: validator.validate_traceability(root, skill),
            "Supplemental retrieval index references missing evaluation IDs: ['C']",
        )

        eval_path.write_text(base, encoding="utf-8")
        expect_failure(
            "supplemental-eval-missing-index",
            lambda: validator.validate_traceability(root, skill),
            "Unanchored evaluation scenarios require a supplemental retrieval index",
        )

        legacy_base = "### A. One\n\n### B. Two\n\n### C. Three\n"
        eval_path.write_text(legacy_base, encoding="utf-8")
        validator.validate_traceability(root, skill, allow_legacy_unindexed_evals=True)
        print("PASS supplemental-eval-legacy-pre-dk-compatibility")

        # Build contiguous AA..DK headings without relying on repository content.
        def eval_id(value: int) -> str:
            chars = []
            while value:
                value, remainder = divmod(value - 1, 26)
                chars.append(chr(ord("A") + remainder))
            return "".join(reversed(chars))

        current_like = "".join(f"### {eval_id(i)}. Fixture {i}\n\n" for i in range(1, validator.eval_id_to_int("DK") + 1))
        eval_path.write_text(current_like, encoding="utf-8")
        expect_failure(
            "supplemental-eval-legacy-flag-rejected-for-current-inventory",
            lambda: validator.validate_traceability(
                root, skill, allow_legacy_unindexed_evals=True
            ),
            "Legacy unindexed-eval compatibility is allowed only for pre-v1.3.2 eval inventories ending at or before DJ",
        )

        eval_path.write_text(index.replace("`C`", "`D`") + base, encoding="utf-8")
        expect_failure(
            "supplemental-eval-missing-id",
            lambda: validator.validate_traceability(root, skill),
            "Supplemental retrieval index references missing evaluation IDs",
        )

        eval_path.write_text(index + base + "\n### D. Four\n", encoding="utf-8")
        expect_failure(
            "supplemental-eval-new-unindexed-scenario",
            lambda: validator.validate_traceability(root, skill),
            "Unanchored evaluation scenarios are missing from the supplemental retrieval index",
        )

        duplicate_index = index.replace("| fixture | `C` |", "| fixture | `C` |\n| duplicate | `C` |")
        eval_path.write_text(duplicate_index + base, encoding="utf-8")
        expect_failure(
            "supplemental-eval-duplicate-id",
            lambda: validator.validate_traceability(root, skill),
            "Supplemental retrieval index contains duplicate evaluation IDs",
        )

        eval_path.write_text(index.replace("`C`", "`C1`") + base, encoding="utf-8")
        expect_failure(
            "supplemental-eval-invalid-id",
            lambda: validator.validate_traceability(root, skill),
            "Supplemental retrieval index contains invalid evaluation ID syntax",
        )

        anchored_rules = rule_path.read_text(encoding="utf-8").replace("| B |", "| B, C |")
        rule_path.write_text(anchored_rules, encoding="utf-8")
        eval_path.write_text(index + base, encoding="utf-8")
        expect_failure(
            "supplemental-eval-anchored-duplication",
            lambda: validator.validate_traceability(root, skill),
            "Supplemental retrieval index must contain only Rule/Goal-unanchored evaluation IDs",
        )

        rule_path.write_text(anchored_rules.replace("| B, C |", "| B |"), encoding="utf-8")
        eval_path.write_text(index + "### A. One\n\n### B. Two\n", encoding="utf-8")
        expect_failure(
            "supplemental-eval-deleted-scenario",
            lambda: validator.validate_traceability(root, skill),
            "Supplemental retrieval index references missing evaluation IDs",
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



def machine_relay_transport_regression_tests() -> None:
    skill_text = (ROOT / "skill" / "SKILL.md").read_text(encoding="utf-8")
    project_text = (ROOT / "docs" / "PROJECT-SPEC.md").read_text(encoding="utf-8")
    eval_text = (ROOT / "skill" / "references" / "eval-scenarios.md").read_text(encoding="utf-8")
    review_text = (ROOT / "skill" / "references" / "review-integration.md").read_text(encoding="utf-8")

    forbidden_legacy = (
        "When a relay is presented for copy/paste",
        "when presented for copy/paste",
    )
    for legacy in forbidden_legacy:
        if legacy in skill_text or legacy in project_text:
            raise AssertionError(f"machine-relay copyability is still conditional: {legacy}")

    required_skill = (
        "Before sending any user-visible response, classify its output purpose from the current routed domain.",
        "If it is a MachineRelay, require `MACHINE_RELAY_OUTPUT_OK(response)` from §7",
        "Classify it once from the routed domain/purpose before rendering; a separate request for copy-ready formatting is irrelevant.",
        "Every user-visible MachineRelay is automatically a copy/paste artifact.",
        "MACHINE_RELAY_OUTPUT_OK(response) =",
        "exactly_one_copy_target_fenced_block(response)",
        "complete_domain_relay_inside_that_block(response)",
        "no_visible_content_before_or_after_block(response)",
        "relay_prose_is_english_unless_explicit_language_override(response)",
        "identity-bearing_or_decision-relevant_literals_remain_exact_unless_safety_redaction_requires_otherwise(response)",
        "outer_fence_safely_contains_any_embedded_fences(response)",
        "If the predicate is false, repair the response before sending it.",
        "pure pre-send output-validity check",
        "ordinary non-relay responses do not enter that predicate",
    )
    for phrase in required_skill:
        if phrase not in skill_text:
            raise AssertionError(f"canonical machine-relay pre-send invariant missing: {phrase}")

    if skill_text.count("MACHINE_RELAY_OUTPUT_OK(response) =") != 1:
        raise AssertionError("MachineRelay predicate must have exactly one canonical definition")
    for ref_path in (ROOT / "skill" / "references").glob("*.md"):
        if "MACHINE_RELAY_OUTPUT_OK(response) =" in ref_path.read_text(encoding="utf-8"):
            raise AssertionError(f"duplicate MachineRelay predicate owner: {ref_path}")

    if "Every user-visible machine relay is automatically a copy/paste artifact" not in project_text:
        raise AssertionError("project-level machine-relay requirement is not unconditional")
    if "MACHINE_RELAY_OUTPUT_OK(response)" not in eval_text or "without waiting for a separate copy-ready request" not in eval_text:
        raise AssertionError("AT does not exercise the canonical pre-send predicate without a copy-ready request")
    if "returned independent-review result is itself a MachineRelay" not in eval_text:
        raise AssertionError("DI does not classify the independent-review result as MachineRelay")
    if "require `MACHINE_RELAY_OUTPUT_OK(response)` before send" not in eval_text:
        raise AssertionError("DI does not enforce the canonical pre-send predicate")
    if "received external review result" not in review_text or "receive-side normalization never authorizes malformed relay emission" not in review_text:
        raise AssertionError("review reconciliation does not distinguish received normalization from Skill emission")
    if "must satisfy `MACHINE_RELAY_OUTPUT_OK(response)`" not in review_text:
        raise AssertionError("review output path does not point back to the canonical predicate")
    print("PASS machine-relay-pre-send-canonical-owner")


def coordination_baseline_governance_regression_tests() -> None:
    governance_text = (ROOT / "skill" / "references" / "governance.md").read_text(encoding="utf-8")
    skill_text = (ROOT / "skill" / "SKILL.md").read_text(encoding="utf-8")
    engineering_text = (ROOT / "skill" / "references" / "engineering-quality.md").read_text(encoding="utf-8")

    lightweight = governance_text.split("### `CoordinationBaseline=LIGHTWEIGHT`", 1)[1].split(
        "### `CoordinationBaseline=STANDARD`", 1
    )[0]
    required = (
        "no material multi-item dependency or material coordination arising from migration, "
        "production/release, or security/data concerns"
    )
    if required not in lightweight:
        raise AssertionError("LIGHTWEIGHT no longer ties migration/security/release exclusions to material coordination")

    legacy = "no material multi-item dependency, migration, production/release coordination, or security/data blast radius"
    if legacy in lightweight:
        raise AssertionError("legacy concern=>STANDARD implication returned")

    if "`LIGHTWEIGHT` for bounded low-coordination outcomes" not in skill_text:
        raise AssertionError("canonical CoordinationBaseline ontology no longer defines LIGHTWEIGHT by coordination shape")
    if (
        "Concern selection by itself never changes accepted scope, `RiskLevel`, `AssuranceLevel`, `ExecutionPath`, "
        "`CoordinationBaseline`, `ProjectAuthority`, or approval requirements."
        not in engineering_text
    ):
        raise AssertionError("engineering concern selection no longer preserves dimension orthogonality")
    print("PASS coordination-baseline-concern-orthogonality")


def main() -> None:
    traceability_tests()
    supplemental_eval_index_tests()
    state_tests()
    worker_contract_tests()
    machine_relay_transport_regression_tests()
    coordination_baseline_governance_regression_tests()


if __name__ == "__main__":
    main()
