#!/usr/bin/env python3
"""Adversarial fixtures for observable paired model/runtime trial scoring."""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SCORER = ROOT / "tools" / "score_model_trials.py"
CASES_PATH = ROOT / "benchmarks" / "phase7" / "model-trial-cases.json"

spec = importlib.util.spec_from_file_location("model_trial_score", SCORER)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Unable to load {SCORER}")
score = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score)

cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
score.validate_cases(copy.deepcopy(cases))
print("PASS model-trial-case-contract")

if score.selected_case_ids(copy.deepcopy(cases), "screening") != score.SCREENING_CASE_IDS:
    raise AssertionError("screening suite drifted from the frozen Phase B screening subset")
if score.selected_case_ids(copy.deepcopy(cases), "selection") != tuple(cases["case_ids"]):
    raise AssertionError("selection suite must remain the full canonical case set")
print("PASS model-trial-suite-selection")

try:
    score.selected_case_ids(copy.deepcopy(cases), "custom")
except ValueError as exc:
    if "unsupported model-trial evaluation suite" not in str(exc):
        raise
    print("PASS arbitrary-suite-rejected")
else:
    raise AssertionError("arbitrary model-trial suite unexpectedly accepted")

sign = score.one_sided_sign_test([1, 1, 1, 1, 1])
if sign["p_value"] != 0.03125:
    raise AssertionError(sign)
print("PASS exact-sign-test")


def observed(*, refs: int = 0, steps: int = 5, correct: bool = True, violations=None):
    return {
        "correct_next_action": correct,
        "protected_violations": list(violations or []),
        "steps_to_first_useful_action": steps,
        "unnecessary_questions": 0,
        "unnecessary_actions": 0,
        "unnecessary_reference_loads": refs,
        "manual_continue_required": False,
    }


def make_trials(*, improve_refs: bool = False, case_ids=None) -> dict:
    runs = []
    selected = list(case_ids if case_ids is not None else cases["case_ids"])
    for case_id in selected:
        for index in range(cases["minimum_pairs_per_case"]):
            pair_id = f"{case_id}-{index + 1}"
            input_fingerprint = f"input:{pair_id}:fixture-v1"
            baseline_first = index % 2 == 0
            base_order = 1 if baseline_first else 2
            candidate_order = 2 if baseline_first else 1
            runs.append(
                {
                    "run_id": f"{pair_id}-baseline",
                    "pair_id": pair_id,
                    "case_id": case_id,
                    "input_fingerprint": input_fingerprint,
                    "representation": "baseline",
                    "order": base_order,
                    "transcript_ref": f"artifact://{pair_id}/baseline",
                    "observed": observed(refs=1 if improve_refs else 0),
                }
            )
            runs.append(
                {
                    "run_id": f"{pair_id}-candidate",
                    "pair_id": pair_id,
                    "case_id": case_id,
                    "input_fingerprint": input_fingerprint,
                    "representation": "candidate",
                    "order": candidate_order,
                    "transcript_ref": f"artifact://{pair_id}/candidate",
                    "observed": observed(refs=0),
                }
            )
    return {
        "schema_version": 1,
        "suite_id": cases["suite_id"],
        "evidence_kind": "actual-model-runtime-ab",
        "baseline_representation": {
            "label": "v1.2.2-baseline",
            "ref": cases["baseline_ref"],
        },
        "candidate_representation": {
            "label": "candidate",
            "ref": "c" * 40,
        },
        "runtime_identity": {
            "model_id": "fixture-model",
            "model_version": "fixture-v1",
            "settings_fingerprint": "settings-fixture",
            "toolset_fingerprint": "toolset-fixture",
        },
        "runs": runs,
    }


identical = score.evaluate(copy.deepcopy(cases), make_trials())
if identical["ok"] or not any(
    "no material paired observable improvement" in error
    for error in identical["acceptance_errors"]
):
    raise AssertionError(f"identical candidate unexpectedly accepted: {identical}")
print("PASS identical-model-results-not-a-win")

improved_doc = make_trials(improve_refs=True)
improved = score.evaluate(copy.deepcopy(cases), copy.deepcopy(improved_doc))
if not improved["ok"]:
    raise AssertionError(improved)
if "avoidable_events" not in improved["improved_metrics"]:
    raise AssertionError(improved)
print("PASS observable-paired-improvement")

screening_doc = make_trials(improve_refs=True, case_ids=score.SCREENING_CASE_IDS)
screening = score.evaluate(copy.deepcopy(cases), copy.deepcopy(screening_doc), suite="screening")
if not screening["ok"]:
    raise AssertionError(screening)
if screening["evaluated_case_ids"] != list(score.SCREENING_CASE_IDS):
    raise AssertionError(screening)
if screening["pair_count"] != len(score.SCREENING_CASE_IDS) * cases["minimum_pairs_per_case"]:
    raise AssertionError(screening)
print("PASS frozen-screening-subset-can-be-scored")

selection_from_screening = score.evaluate(copy.deepcopy(cases), copy.deepcopy(screening_doc))
if selection_from_screening["ok"] or not any(
    "has 0 pairs" in error for error in selection_from_screening["acceptance_errors"]
):
    raise AssertionError("partial screening evidence unexpectedly satisfied full selection")
print("PASS screening-does-not-satisfy-selection")

screening_with_extra = copy.deepcopy(screening_doc)
extra_case = next(case_id for case_id in cases["case_ids"] if case_id not in score.SCREENING_CASE_IDS)
extra_pair = make_trials(improve_refs=True, case_ids=[extra_case])["runs"]
screening_with_extra["runs"].extend(extra_pair)
try:
    score.evaluate(copy.deepcopy(cases), screening_with_extra, suite="screening")
except ValueError as exc:
    if "outside screening suite" not in str(exc):
        raise
    print("PASS screening-extra-case-rejected")
else:
    raise AssertionError("screening accepted a case outside the frozen subset")

unsafe = copy.deepcopy(improved_doc)
unsafe_candidate = next(row for row in unsafe["runs"] if row["representation"] == "candidate")
unsafe_candidate["observed"]["protected_violations"] = ["unsafe_shortcut"]
unsafe_result = score.evaluate(copy.deepcopy(cases), unsafe)
if unsafe_result["ok"] or not any(
    "protected-behavior violations" in error for error in unsafe_result["acceptance_errors"]
):
    raise AssertionError(f"unsafe candidate unexpectedly accepted: {unsafe_result}")
print("PASS safety-regression-cannot-be-averaged-away")

decision_regression = copy.deepcopy(improved_doc)
row = next(r for r in decision_regression["runs"] if r["representation"] == "candidate")
row["observed"]["correct_next_action"] = False
decision_result = score.evaluate(copy.deepcopy(cases), decision_regression)
if decision_result["ok"] or not any(
    "decision_error" in error for error in decision_result["acceptance_errors"]
):
    raise AssertionError(f"decision regression unexpectedly accepted: {decision_result}")
print("PASS decision-regression-rejected")

step_regression = copy.deepcopy(improved_doc)
first_case = cases["case_ids"][0]
for row in step_regression["runs"]:
    if row["case_id"] == first_case and row["representation"] == "candidate":
        row["observed"]["steps_to_first_useful_action"] += 1
step_result = score.evaluate(copy.deepcopy(cases), step_regression)
if step_result["ok"] or not any(
    "steps_to_first_useful_action" in error for error in step_result["acceptance_errors"]
):
    raise AssertionError(f"step regression unexpectedly accepted: {step_result}")
print("PASS friction-regression-rejected")

biased = copy.deepcopy(improved_doc)
for row in biased["runs"]:
    row["order"] = 1 if row["representation"] == "baseline" else 2
biased_result = score.evaluate(copy.deepcopy(cases), biased)
if biased_result["ok"] or not any(
    "unbalanced run order" in error for error in biased_result["acceptance_errors"]
):
    raise AssertionError(f"order-biased suite unexpectedly accepted: {biased_result}")
print("PASS order-bias-rejected")

incomplete = copy.deepcopy(improved_doc)
first_pair = incomplete["runs"][0]["pair_id"]
incomplete["runs"] = [
    row
    for row in incomplete["runs"]
    if not (row["pair_id"] == first_pair and row["representation"] == "candidate")
]
try:
    score.evaluate(copy.deepcopy(cases), incomplete)
except ValueError as exc:
    if "exactly two runs" not in str(exc):
        raise
    print("PASS incomplete-pair-rejected")
else:
    raise AssertionError("incomplete pair unexpectedly accepted")

mismatched_input = copy.deepcopy(improved_doc)
first_pair = mismatched_input["runs"][0]["pair_id"]
candidate_run = next(
    row
    for row in mismatched_input["runs"]
    if row["pair_id"] == first_pair and row["representation"] == "candidate"
)
candidate_run["input_fingerprint"] = "input:different"
try:
    score.evaluate(copy.deepcopy(cases), mismatched_input)
except ValueError as exc:
    if "inputs do not match" not in str(exc):
        raise
    print("PASS mismatched-paired-input-rejected")
else:
    raise AssertionError("mismatched paired input unexpectedly accepted")

missing_transcript = copy.deepcopy(improved_doc)
missing_transcript["runs"][0]["transcript_ref"] = ""
try:
    score.evaluate(copy.deepcopy(cases), missing_transcript)
except ValueError as exc:
    if "transcript_ref" not in str(exc):
        raise
    print("PASS missing-audit-reference-rejected")
else:
    raise AssertionError("missing transcript reference unexpectedly accepted")

duplicate_transcript = copy.deepcopy(improved_doc)
duplicate_transcript["runs"][1]["transcript_ref"] = duplicate_transcript["runs"][0]["transcript_ref"]
try:
    score.evaluate(copy.deepcopy(cases), duplicate_transcript)
except ValueError as exc:
    if "duplicate transcript_ref" not in str(exc):
        raise
    print("PASS duplicate-audit-reference-rejected")
else:
    raise AssertionError("duplicate transcript reference unexpectedly accepted")

private_reasoning = copy.deepcopy(improved_doc)
private_reasoning["runs"][0]["chain_of_thought"] = "private reasoning must not enter evidence"
try:
    score.evaluate(copy.deepcopy(cases), private_reasoning)
except ValueError as exc:
    if "every trial run must contain exactly" not in str(exc):
        raise
    print("PASS private-reasoning-field-rejected")
else:
    raise AssertionError("private reasoning field unexpectedly accepted")

bad_cases = copy.deepcopy(cases)
bad_cases["baseline_ref"] = "0" * 40
try:
    score.validate_cases(bad_cases)
except ValueError as exc:
    if "program baseline" not in str(exc):
        raise
    print("PASS model-trial-baseline-drift-rejected")
else:
    raise AssertionError("model-trial baseline drift unexpectedly accepted")

missing_screening_case = copy.deepcopy(cases)
missing_screening_case["case_ids"].remove(score.SCREENING_CASE_IDS[0])
try:
    score.validate_cases(missing_screening_case)
except ValueError as exc:
    if "frozen screening case" not in str(exc):
        raise
    print("PASS frozen-screening-case-drift-rejected")
else:
    raise AssertionError("canonical case set unexpectedly dropped a frozen screening case")
