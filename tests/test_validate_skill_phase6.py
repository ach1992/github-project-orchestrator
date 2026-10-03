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

        for spaces in range(4):
            visible = f"### A. One\n\n### B. Two\n\n{' ' * spaces}### C. Three\n"
            eval_path.write_text(index + visible, encoding="utf-8")
            validator.validate_traceability(root, skill)
            print(f"PASS supplemental-eval-visible-heading-indent-{spaces}")

        four_space_code = "### A. One\n\n### B. Two\n\n    ### C. Code, not heading\n"
        eval_path.write_text(index + four_space_code, encoding="utf-8")
        expect_failure(
            "supplemental-eval-four-space-heading-not-counted",
            lambda: validator.validate_traceability(root, skill),
            "Supplemental retrieval index references missing evaluation IDs: ['C']",
        )

        cross_line = "###\nC. False-positive paragraph, not an eval heading\n"
        if validator.parse_eval_ids(cross_line):
            raise AssertionError("eval ID must not cross a physical line boundary")
        print("PASS supplemental-eval-cross-line-pseudo-heading-not-counted")

        eval_path.write_text(
            index + "### A. One\n\n### B. Two\n\n" + cross_line,
            encoding="utf-8",
        )
        expect_failure(
            "supplemental-eval-cross-line-pseudo-heading-cannot-satisfy-index",
            lambda: validator.validate_traceability(root, skill),
            "Supplemental retrieval index references missing evaluation IDs: ['C']",
        )

        for separator_name, separator in (("spaces", "   "), ("tabs", "\t\t")):
            titleless = f"### C.{separator}\nFalse-positive paragraph, not a titled eval heading\n"
            if validator.parse_eval_ids(titleless):
                raise AssertionError(f"{separator_name} titleless eval heading was incorrectly counted")
            eval_path.write_text(
                index + "### A. One\n\n### B. Two\n\n" + titleless,
                encoding="utf-8",
            )
            expect_failure(
                f"supplemental-eval-titleless-{separator_name}-heading-cannot-satisfy-index",
                lambda: validator.validate_traceability(root, skill),
                "Supplemental retrieval index references missing evaluation IDs: ['C']",
            )

        uppercase_cdata = "<![CDATA[\n### C. Hidden fake\n]]>\n"
        if validator.parse_eval_ids(uppercase_cdata):
            raise AssertionError("uppercase CDATA contents must remain hidden")
        print("PASS supplemental-eval-uppercase-cdata-heading-not-counted")

        for cdata_name, cdata_start in (
            ("lowercase", "<![cdata["),
            ("mixed-case", "<![CdAtA["),
        ):
            visible_cdata = cdata_start + "\n### C. Visible future scenario\n]]>\n"
            if validator.parse_eval_ids(visible_cdata) != ["C"]:
                raise AssertionError(f"{cdata_name} CDATA-like text incorrectly hid visible C")
            eval_path.write_text(
                "### A. One\n\n### B. Two\n\n" + visible_cdata,
                encoding="utf-8",
            )
            expect_failure(
                f"supplemental-eval-{cdata_name}-cdata-visible-unanchored-rejected",
                lambda: validator.validate_traceability(root, skill),
                "Unanchored evaluation scenarios require a supplemental retrieval index: ['C']",
            )

        eval_path.write_text("### A. One\n\n### B. Two\n\n  ### C. Visible unanchored\n", encoding="utf-8")
        expect_failure(
            "supplemental-eval-indented-unanchored-requires-index",
            lambda: validator.validate_traceability(root, skill),
            "Unanchored evaluation scenarios require a supplemental retrieval index: ['C']",
        )

        comment_with_fence = (
            index
            + "### A. One\n\n### B. Two\n\n<!--\n```text\ninside comment\n-->\n### C. Three\n"
        )
        eval_path.write_text(comment_with_fence, encoding="utf-8")
        validator.validate_traceability(root, skill)
        print("PASS supplemental-eval-comment-fence-state-isolated")

        for html_name, html in (
            ("pre", "<pre>\n### C. Hidden fake\n</pre>\n"),
            ("div", "<div>\n### C. Hidden fake\n</div>\n\n"),
        ):
            eval_path.write_text(index + "### A. One\n\n### B. Two\n" + html, encoding="utf-8")
            expect_failure(
                f"supplemental-eval-{html_name}-html-heading-not-counted",
                lambda: validator.validate_traceability(root, skill),
                "Supplemental retrieval index references missing evaluation IDs: ['C']",
            )

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
Repository: owner/repo
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
    independent_review_text = (ROOT / "skill" / "references" / "independent-review.md").read_text(encoding="utf-8")
    relay_text = (ROOT / "skill" / "references" / "relay-transport.md").read_text(encoding="utf-8")
    rule_text = (ROOT / "design" / "RULE-MAP.md").read_text(encoding="utf-8")

    forbidden_legacy = (
        "When a relay is presented for copy/paste",
        "when presented for copy/paste",
    )
    for legacy in forbidden_legacy:
        if legacy in skill_text or legacy in project_text:
            raise AssertionError(f"machine-relay copyability is still conditional: {legacy}")

    required_skill = (
        "Before send, classify output purpose from the routed domain.",
        "If it is a MachineRelay, load [references/relay-transport.md](references/relay-transport.md)",
        "ordinary non-relay responses bypass it",
    )
    for phrase in required_skill:
        if phrase not in skill_text:
            raise AssertionError(f"canonical MachineRelay activation missing from SKILL.md: {phrase}")

    required_relay = (
        "Load this file only when the user-visible output is a **MachineRelay**",
        "Every user-visible MachineRelay is automatically one copy/paste artifact.",
        "MACHINE_RELAY_OUTPUT_OK(response) =",
        "exactly_one_copy_target_fenced_block(response)",
        "complete_domain_relay_inside_that_block(response)",
        "no_visible_content_before_or_after_block(response)",
        "relay_prose_is_english_unless_explicit_language_override(response)",
        "identity-bearing_or_decision-relevant_literals_remain_exact_unless_safety_redaction_requires_otherwise(response)",
        "outer_fence_safely_contains_any_embedded_fences(response)",
        "A separate copy-ready request is irrelevant.",
        "creates no lifecycle/state or second payload owner",
        "Direct non-relay user-facing explanation bypasses this predicate",
    )
    for phrase in required_relay:
        if phrase not in relay_text:
            raise AssertionError(f"canonical MachineRelay transport missing: {phrase}")

    all_runtime_text = skill_text + "\n" + "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "skill" / "references").glob("*.md")
    )
    if all_runtime_text.count("MACHINE_RELAY_OUTPUT_OK(response) =") != 1:
        raise AssertionError("MachineRelay predicate must have exactly one canonical definition")
    if "MACHINE_RELAY_OUTPUT_OK(response) =" in skill_text:
        raise AssertionError("relay-only predicate leaked back into the always-loaded kernel")

    relay_rule_rows = [
        line for line in rule_text.splitlines() if line.startswith("| `MACHINE-RELAY-PORTABLE` |")
    ]
    if len(relay_rule_rows) != 1:
        raise AssertionError("MACHINE-RELAY-PORTABLE must have exactly one canonical Rule-map row")
    relay_rule_fields = [field.strip() for field in relay_rule_rows[0].strip("|").split("|")]
    if len(relay_rule_fields) < 3 or relay_rule_fields[2] != "`relay-transport.md`":
        raise AssertionError("MACHINE-RELAY-PORTABLE canonical owner must be relay-transport.md")


    if "Every user-visible machine relay is automatically a copy/paste artifact" not in project_text:
        raise AssertionError("project-level machine-relay requirement is not unconditional")
    if "MACHINE_RELAY_OUTPUT_OK(response)" not in eval_text or "without waiting for a separate copy-ready request" not in eval_text:
        raise AssertionError("AT does not exercise the canonical pre-send predicate without a copy-ready request")
    if "returned independent-review result is itself a MachineRelay" not in eval_text:
        raise AssertionError("DI does not classify the independent-review result as MachineRelay")
    if "require `MACHINE_RELAY_OUTPUT_OK(response)` before send" not in eval_text:
        raise AssertionError("DI does not enforce the canonical pre-send predicate")
    if "received external review result" not in independent_review_text or "Receive-side normalization never authorizes malformed relay emission" not in independent_review_text:
        raise AssertionError("independent-review reconciliation does not distinguish received normalization from Skill emission")
    handoff_contract_text = independent_review_text.split("## 2. Review handoff", 1)[1].split("## 3. Result contract", 1)[0]
    required_review_prompt_dispatch = (
        "emit the complete `INDEPENDENT REVIEW CHAT` MachineRelay for user-mediated dispatch",
        "GitHub/PR/Issue state may be evidence/locators, never a substitute for that relay",
        "next chat to reconstruct it",
    )
    if "ready-to-paste" in handoff_contract_text:
        raise AssertionError("independent-review handoff duplicates transport copy/paste semantics")
    for phrase in required_review_prompt_dispatch:
        if phrase not in handoff_contract_text:
            raise AssertionError(f"independent-review prompt dispatch regression guard missing: {phrase}")
    bc_text = eval_text.split("### BC. Independent high-risk review handoff", 1)[1].split("### BD.", 1)[0]
    if "For user-mediated dispatch, emit the `INDEPENDENT REVIEW CHAT` relay itself; GitHub/PR/Issue state is evidence, not a substitute." not in bc_text:
        raise AssertionError("BC does not preserve direct reviewer-prompt dispatch semantics")
    regression_guard_text = eval_text.split("## 4. Regression guard", 1)[1]
    if "user-mediated independent review emits the reviewer relay itself rather than a durable-state pointer" not in regression_guard_text:
        raise AssertionError("Regression Guard does not preserve reviewer-prompt dispatch semantics")
    result_contract_text = independent_review_text.split("## 3. Result contract", 1)[1].split("## 4. Master reconciliation", 1)[0]
    if "An emitted `INDEPENDENT REVIEW RESULT` is a MachineRelay" not in result_contract_text:
        raise AssertionError("independent-review result does not classify itself as MachineRelay at the emission point")
    if "load `relay-transport.md` and require `MACHINE_RELAY_OUTPUT_OK(response)`" not in result_contract_text:
        raise AssertionError("independent-review result emission does not route to the canonical transport owner")
    if independent_review_text.count("MACHINE_RELAY_OUTPUT_OK(response)") != 1:
        raise AssertionError("independent-review must route result transport exactly once without duplicating the canonical rule")
    if "# INDEPENDENT REVIEW RESULT" in review_text:
        raise AssertionError("normal review path still embeds the cold independent-review result protocol")
    print("PASS machine-relay-pre-send-canonical-owner")


def defensive_security_review_evidence_regression_tests() -> None:
    project_text = (ROOT / "docs" / "PROJECT-SPEC.md").read_text(encoding="utf-8")
    engineering_text = (ROOT / "skill" / "references" / "engineering-quality.md").read_text(encoding="utf-8")
    review_text = (ROOT / "skill" / "references" / "review-integration.md").read_text(encoding="utf-8")
    independent_review_text = (ROOT / "skill" / "references" / "independent-review.md").read_text(encoding="utf-8")
    eval_text = (ROOT / "skill" / "references" / "eval-scenarios.md").read_text(encoding="utf-8")
    rule_text = (ROOT / "design" / "RULE-MAP.md").read_text(encoding="utf-8")

    required = {
        "project": (
            project_text,
            (
                "For independent/read-only review, evidence acquisition defaults to authoritative source/diff",
                "report an evidence-backed finding or explicit review limitation instead of manufacturing a new probe",
                "Bounded defensive regression tests remain available during explicitly scoped implementation/remediation",
            ),
        ),
        "engineering": (
            engineering_text,
            (
                "For an independent/read-only reviewer relay, default evidence acquisition to authoritative source/diff",
                "Do not ask the reviewer to invent, generate, mutate, or execute novel adversarial payloads/probes",
                "the reviewer should report an evidence-backed `BLOCKER`/`REQUIRED` finding or `INCOMPLETE / NOT_ISSUED`",
                "This reviewer boundary does not prohibit bounded defensive regression tests during explicitly scoped implementation/remediation",
            ),
        ),
        "review": (
            independent_review_text,
            (
                "for independent/read-only review also carry the reviewer evidence-acquisition boundary",
                "do not request novel adversarial payload/probe generation or execution merely to prove robustness",
                "missing required evidence becomes a finding or explicit review limitation rather than a reviewer-created probe",
            ),
        ),
        "eval": (
            eval_text,
            (
                "In the independent/read-only review variant",
                "novel adversarial payload/probe generation or execution by a reviewer solely to prove bypassability/robustness",
                "Explicitly scoped, authorized, isolated defensive implementation/remediation may still add bounded regression tests",
            ),
        ),
        "rule-map": (
            rule_text,
            (
                "`DEFENSIVE-SECURITY-CONTINUATION`",
                "Independent/read-only reviewers prefer source/diff, repository-owned existing tests, current CI/log/artifact evidence",
                "explicitly scoped defensive implementation/remediation testing remains available when authorized and policy-permitted",
            ),
        ),
    }

    for surface, (text, phrases) in required.items():
        for phrase in phrases:
            if phrase not in text:
                raise AssertionError(f"{surface} lost defensive-review evidence boundary: {phrase}")

    print("PASS defensive-security-review-evidence-boundary")


def interface_specialist_composition_regression_tests() -> None:
    skill_text = (ROOT / "skill" / "SKILL.md").read_text(encoding="utf-8")
    interface_text = (ROOT / "skill" / "references" / "interface-specialist.md").read_text(encoding="utf-8")
    engineering_text = (ROOT / "skill" / "references" / "engineering-quality.md").read_text(encoding="utf-8")
    eval_text = (ROOT / "skill" / "references" / "eval-scenarios.md").read_text(encoding="utf-8")

    required = {
        "skill": (
            skill_text,
            (
                "[references/interface-specialist.md](references/interface-specialist.md)",
                "unresolved interface judgment",
                "no project-authority, approval, code-review, or automatic re-consult implication",
            ),
        ),
        "interface": (
            interface_text,
            (
                "Product Interface Designer v0.2.1",
                "7aeef3475f160a000e0ec9ab1a6618b41d63f70a",
                "not a runtime version pin",
                "provider-neutral",
                "Consult a compatible interface specialist only when **all** are true:",
                "Master code/integration-review trigger",
                "Material interface impact alone is neither `MasterBoundary.MATERIAL_DECISION_REQUIRED`",
                "The specialist contract owns field semantics; this Skill only consumes them.",
                "the packet never triggers another specialist call by itself",
                "Specialist unavailability alone is not a Master stop.",
            ),
        ),
        "engineering": (
            engineering_text,
            (
                "owns unresolved interface intent/critique only",
                "still owns material engineering realization/evidence",
                "fallback when specialist consultation is not triggered or unavailable",
            ),
        ),
        "eval": (
            eval_text,
            (
                "### DS. Unresolved interface judgment uses one bounded specialist consultation",
                "### DT. Trivial or already-decided UI work does not invoke the specialist",
                "### DU. Specialist unavailability preserves bounded standalone progress",
                "### DV. Returned packet does not create ping-pong or Worker scope growth",
                "This specialization trigger alone does not imply the canonical material-decision boundary",
                "Master code/integration review",
                "automatic specialist repository mutation/implementation",
                "| interface-specialist composition, materiality, packet/return-control, and fallback | `DS`, `DT`, `DU`, `DV` |",
            ),
        ),
    }
    for surface, (text, phrases) in required.items():
        for phrase in phrases:
            if phrase not in text:
                raise AssertionError(f"{surface} lost interface-specialist composition boundary: {phrase}")

    schema_line = "`Intent` · `Decision` · `Constraints` · `Implementation latitude` · `Evidence` · `Open assumptions`"
    if interface_text.count(schema_line) != 1:
        raise AssertionError("interface decision packet must expose exactly one shared six-field schema")
    if "| **Intent** |" in interface_text or "| **Decision** |" in interface_text:
        raise AssertionError("caller must consume the shared packet schema without duplicating provider field semantics")
    if "material interface decision" in skill_text or "material interface decision" in interface_text or "material interface decision" in engineering_text:
        raise AssertionError("interface specialization must not overload the canonical material-decision term")

    interface_router = next(line for line in skill_text.splitlines() if "interface-specialist.md" in line)
    engineering_router = next(line for line in skill_text.splitlines() if "engineering-quality.md" in line)
    if "interface review" in interface_router.lower() or "master review" in interface_router.lower():
        raise AssertionError("interface critique must not collide with the Master code/integration review route")
    if "user-facing quality" in engineering_router.lower():
        raise AssertionError("engineering router must not broadly compete for unresolved interface judgment")
    if "| user-facing quality |" not in engineering_text:
        raise AssertionError("standalone/fallback user-facing engineering guidance was lost")

    for specialist_internal in (
        "references/design-core.md",
        "references/internationalization.md",
        "references/persian-rtl.md",
        "references/composition.md",
    ):
        if specialist_internal in interface_text:
            raise AssertionError(f"caller copied/imported Product Interface Designer internals: {specialist_internal}")

    print("PASS interface-specialist-composition-boundaries")

def project_start_bootstrap_regression_tests() -> None:
    project_text = (ROOT / "docs" / "PROJECT-SPEC.md").read_text(encoding="utf-8")
    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    skill_text = (ROOT / "skill" / "SKILL.md").read_text(encoding="utf-8")
    master_text = (ROOT / "skill" / "references" / "master-cycle.md").read_text(encoding="utf-8")
    governance_text = (ROOT / "skill" / "references" / "governance.md").read_text(encoding="utf-8")
    eval_text = (ROOT / "skill" / "references" / "eval-scenarios.md").read_text(encoding="utf-8")
    rule_text = (ROOT / "design" / "RULE-MAP.md").read_text(encoding="utf-8")

    required = {
        "project": (
            project_text,
            (
                "existing authorized GitHub repository or an explicitly resolved repository creation target",
                "verified create-only-if-absent semantics",
                "repository discovery/creation",
            ),
        ),
        "readme": (
            readme_text,
            (
                "The target GitHub repository identity must be exact.",
                "an absent target may be created only when the normal scope/authority/policy/capability gates permit it",
            ),
        ),
        "skill": (
            skill_text,
            (
                "stable architecture / detailed supported-environment specifications / engineering-release rules",
            ),
        ),
        "master": (
            master_text,
            (
                "resolve project definition and repository target as one bounded intake pass",
                "discover before creating",
                "CAN_EXECUTE(create repository)",
                "startup-specific stop",
            ),
        ),
        "governance": (
            governance_text,
            (
                "prefer `docs/PROJECT-SPEC.md` as the default canonical location",
                "derive means scope and align artifacts to accepted intent and evidence",
                "`README.md` as the user/developer entry surface by default",
                "not normally the canonical root project specification",
                "## 2. Root project specification",
                "project-level supported-environment/platform commitments",
            ),
        ),
        "rule-map": (
            rule_text,
            (
                "`ROOT-SPEC-CANONICAL`",
                "| B, AU, AZ |",
                "| AZ, CX, DQ |",
            ),
        ),
    }
    for surface, (text, phrases) in required.items():
        for phrase in phrases:
            if phrase not in text:
                raise AssertionError(f"{surface} lost project-start bootstrap requirement: {phrase}")

    if "already provisioned repository identity" in master_text:
        raise AssertionError("first ownership still requires a pre-provisioned repository")
    if "The GitHub repository must already exist" in readme_text:
        raise AssertionError("README still requires a pre-existing repository")

    root_spec_rows = [line for line in rule_text.splitlines() if line.startswith("| `ROOT-SPEC-CANONICAL` |")]
    if len(root_spec_rows) != 1:
        raise AssertionError("ROOT-SPEC-CANONICAL must have exactly one Rule-map row")
    root_spec_fields = [field.strip() for field in root_spec_rows[0].strip("|").split("|")]
    root_spec_anchors = {anchor.strip() for anchor in root_spec_fields[-1].split(",")}
    required_root_spec_anchors = {"BV", "BW", "BX", "CD", "CY"}
    if "AZ" in root_spec_anchors or not required_root_spec_anchors.issubset(root_spec_anchors):
        raise AssertionError(f"ROOT-SPEC-CANONICAL has imprecise eval anchors: {root_spec_fields[-1]}")

    az_text = eval_text.split("### AZ. First end-to-end ownership uses proportional bootstrap", 1)[1].split(
        "### BA.", 1
    )[0]
    for phrase in (
        "may be absent with an exact intended repository creation target",
        "CAN_EXECUTE(create repository)",
        "verify the created remote identity",
        "duplicate repository creation",
        "startup-specific lifecycle/state",
    ):
        if phrase not in az_text:
            raise AssertionError(f"AZ does not cover project-start repository-creation variant: {phrase}")

    bv_text = eval_text.split("### BV. First ownership with root specification already in repository", 1)[1].split(
        "### BW.", 1
    )[0]
    if "A README counts only when the repository clearly and intentionally uses it" not in bv_text:
        raise AssertionError("BV no longer distinguishes an intentional root spec from an ordinary README")

    bw_text = eval_text.split("### BW. First ownership with root specification supplied outside repository", 1)[1].split(
        "### BX.", 1
    )[0]
    for phrase in ("docs/PROJECT-SPEC.md", "ordinary README", "spec plus repository reality"):
        if phrase not in bw_text:
            raise AssertionError(f"BW lost canonical project-spec/README separation: {phrase}")

    print("PASS first-ownership-repository-creation-and-project-spec")


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



def decision_boundary_precision_regression_tests() -> None:
    """Guard scoped text/ownership, not model behavior or measured efficiency."""
    paths = {
        "kernel": "skill/SKILL.md",
        "authority": "skill/references/authority-gates.md",
        "task": "skill/references/task-contract.md",
        "review": "skill/references/review-integration.md",
        "eval": "skill/references/eval-scenarios.md",
    }
    texts = {key: (ROOT / path).read_text(encoding="utf-8") for key, path in paths.items()}

    def section(source: str, start: str, end: str) -> str:
        if source.count(start) != 1 or source.count(end) != 1:
            raise ValueError(f"Missing or duplicate boundary: {start}")
        return source.split(start, 1)[1].split(end, 1)[0]

    def check(candidate: dict[str, str]) -> None:
        router = section(candidate["kernel"], "## 5. One-step role/event router", "## 6. Worker entry")
        rows = [line for line in router.splitlines() if line.startswith("| ") and "Master review; CI failure" in line]
        if len(rows) != 1:
            raise ValueError("execution-safety: expected one canonical router row")
        concurrency = section(candidate["authority"], "## 7. Optimistic concurrency", "## 8. Human approval or operation")
        validation = section(candidate["task"], "## 5. Validation strategy", "## 6. Change risk")
        maturity = section(candidate["review"], "## 1. Establish review target", "### `REVIEW_VALID(envelope)`")
        failures = section(candidate["review"], "## 4. CI failures", "## 5. Conflicts")
        required = {
            "execution-safety": (rows[0], (
                "before executing untrusted candidate code (either role)",
                "execution alone: apply only",
                "(references/review-integration.md#2-review-standard)",
                "other triggers: use `REVIEW_VALID(envelope)` and current integration evidence",
            )),
            "concurrency": (concurrency, (
                "Do not create manager lock/lease files.",
                "When the available operation documents an enforced expected-identity/revision precondition",
                "submit the verified expected value with the write",
                "only the identities covered by that precondition, not the entire review/authorization envelope",
                "If state changed unexpectedly or the precondition is rejected",
                "Never remove a rejected precondition to force the write",
                "A local reconciliation condition is not automatically a MasterBoundary.",
                "When no such precondition is available, retain read/reconcile/verify",
                "assess residual race risk under existing gates",
                "Do not invent API support or claim atomic protection; absence alone creates no new gate.",
            )),
            "evidence-reuse": (validation, (
                "exact code/object surface it proves",
                "relevant dependency/config/toolchain/environment assumptions, and the requirement proved remain unchanged",
                "unrelated SHA movement alone does not invalidate that evidence or make it a fresh run on the new candidate",
                "Repository-required checks remain mandatory for every candidate identity to which policy binds them",
            )),
            "candidate-maturity": (maturity, (
                "use it only to signal candidate maturity and avoid knowingly stale acceptance work",
                "not merely to represent an external wait or retrigger unchanged validation",
                "Follow any policy-required transition",
                "Draft/Ready remains presentation, adds no `TaskState`, and skips no exact-candidate gate",
            )),
            "policy-timing": (failures, (
                "prefer the narrowest check/job that can discriminate the suspected cause",
                "each new candidate must satisfy every repository-required gate at the point required by policy",
            )),
        }
        for label, (region, phrases) in required.items():
            for phrase in phrases:
                if phrase not in region:
                    raise ValueError(f"{label}: missing scoped guard: {phrase}")
        # The new subsection link must target the existing safety owner, not a parallel protocol.
        safety = section(candidate["review"], "## 2. Review standard", "## 3. Evidence authority and freshness")
        if "For untrusted contributor changes, inspect execution/supply-chain surfaces before running them." not in safety:
            raise ValueError("execution-safety: canonical subsection lost pre-execution obligation")
        if "Never reprioritize, broaden task/repository scope, integrate the target" not in candidate["kernel"]:
            raise ValueError("execution-safety: Worker ownership guard lost")
        if "Mark only the individual mutation `WriteState.UNKNOWN`" not in candidate["authority"]:
            raise ValueError("concurrency: ambiguous transport must retain its existing owner")
        scenario_guards = {
            "M": ("N", ("Route pre-execution safety directly", "an independently triggered full review remains required")),
            "E": ("F", ("A HEAD-only guard does not validate the base", "An ambiguous write still follows `WriteState.UNKNOWN`")),
            "BU": ("BV", ("For a stable external wait", "Follow any policy-required transition")),
            "DM": ("DN", ("Changed shared assumptions invalidate the affected proof", "including per-push checks when actually required")),
        }
        for ident, (next_ident, phrases) in scenario_guards.items():
            scenario = section(candidate["eval"], f"### {ident}. ", f"### {next_ident}. ")
            if any(phrase not in scenario for phrase in phrases):
                raise ValueError(f"scenario-{ident}: missing decision counterexample")

    check(texts)
    print("PASS decision-boundary-precision-positive")
    # Mutation fixtures verify that the guards fail when an essential discriminator is lost.
    mutations = (
        ("execution-trigger", "kernel", "before executing untrusted candidate code (either role); ", "execution-safety"),
        ("safety-anchor", "kernel", "#2-review-standard", "execution-safety"),
        ("execution-only-scope", "kernel", "execution alone: apply only", "execution-safety"),
        ("native-precondition", "authority", "submit the verified expected value with the write", "concurrency"),
        ("partial-precondition", "authority", "not the entire review/authorization envelope", "concurrency"),
        ("rejection-bypass", "authority", "Never remove a rejected precondition to force the write", "concurrency"),
        ("unsupported-fallback", "authority", "absence alone creates no new gate", "concurrency"),
        ("proof-surface", "task", "surface it proves", "evidence-reuse"),
        ("old-proof-identity", "task", "or make it a fresh run on the new candidate", "evidence-reuse"),
        ("external-wait", "review", "not merely to represent an external wait or retrigger unchanged validation", "candidate-maturity"),
        ("required-transition", "review", "Follow any policy-required transition", "candidate-maturity"),
        ("policy-timing", "review", "at the point required by policy", "policy-timing"),
    )
    for name, key, removed, error in mutations:
        if texts[key].count(removed) != 1:
            raise AssertionError(f"Ambiguous mutation fixture: {name}")
        mutant = dict(texts)
        mutant[key] = mutant[key].replace(removed, "", 1)
        expect_failure(f"decision-boundary-{name}", lambda: check(mutant), error)

def main() -> None:
    traceability_tests()
    supplemental_eval_index_tests()
    state_tests()
    worker_contract_tests()
    machine_relay_transport_regression_tests()
    defensive_security_review_evidence_regression_tests()
    interface_specialist_composition_regression_tests()
    project_start_bootstrap_regression_tests()
    coordination_baseline_governance_regression_tests()
    decision_boundary_precision_regression_tests()


if __name__ == "__main__":
    main()
