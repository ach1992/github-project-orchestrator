#!/usr/bin/env python3
"""Adversarial fixtures for Phase B hot/recovery screening."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "tools" / "score_runtime_ab_screening.py"
MODEL = ROOT / "tools" / "score_model_trials.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


screen = load_module("runtime_ab_screening", SCREEN)
model = load_module("model_trial_score", MODEL)


def observed(*, steps: int, refs: int = 0, correct: bool = True, violations=None):
    return {
        "correct_next_action": correct,
        "protected_violations": list(violations or []),
        "steps_to_first_useful_action": steps,
        "unnecessary_questions": 0,
        "unnecessary_actions": 0,
        "unnecessary_reference_loads": refs,
        "manual_continue_required": False,
    }


def trials(*, baseline_steps: int = 3, candidate_steps: int = 2):
    runs = []
    for case_id in screen.SCREEN_CASES:
        for index in range(3):
            pair_id = f"{case_id}-{index + 1}"
            baseline_order = 1 if index % 2 == 0 else 2
            candidate_order = 2 if baseline_order == 1 else 1
            common = {
                "pair_id": pair_id,
                "case_id": case_id,
                "input_fingerprint": f"input:{pair_id}",
            }
            runs.append({
                **common,
                "run_id": f"{pair_id}-baseline",
                "representation": "baseline",
                "order": baseline_order,
                "transcript_ref": f"artifact://{pair_id}/baseline",
                "observed": observed(steps=baseline_steps),
            })
            runs.append({
                **common,
                "run_id": f"{pair_id}-candidate",
                "representation": "candidate",
                "order": candidate_order,
                "transcript_ref": f"artifact://{pair_id}/candidate",
                "observed": observed(steps=candidate_steps),
            })
    return {
        "schema_version": 1,
        "suite_id": "lossless-runtime-representation-v1",
        "evidence_kind": "actual-model-runtime-ab",
        "baseline_representation": {"label": "baseline", "ref": "f" * 40},
        "candidate_representation": {"label": "candidate", "ref": "c" * 40},
        "runtime_identity": {
            "model_id": "fixture",
            "model_version": "fixture-v1",
            "settings_fingerprint": "settings",
            "toolset_fingerprint": "tools",
        },
        "runs": runs,
    }


passing = screen.evaluate(trials(), model)
if not passing["advance_to_full_suite"]:
    raise AssertionError(passing)
if passing["selection_proof_eligible"] is not False:
    raise AssertionError("screening must never be migration proof")
if "steps_to_first_useful_action" not in passing["improved_friction_metrics"]:
    raise AssertionError(passing)
print("PASS strict-friction-improvement-advances-only-to-full-suite")

identical = screen.evaluate(trials(baseline_steps=2, candidate_steps=2), model)
if identical["advance_to_full_suite"]:
    raise AssertionError(identical)
if not any("no strict observable friction improvement" in e for e in identical["screening_errors"]):
    raise AssertionError(identical)
print("PASS identical-screening-does-not-advance")

unsafe_doc = trials()
next(run for run in unsafe_doc["runs"] if run["representation"] == "candidate")["observed"]["protected_violations"] = ["unsafe"]
unsafe = screen.evaluate(unsafe_doc, model)
if unsafe["advance_to_full_suite"]:
    raise AssertionError(unsafe)
print("PASS protected-regression-blocks-screening")

wrong_doc = trials()
next(run for run in wrong_doc["runs"] if run["representation"] == "candidate")["observed"]["correct_next_action"] = False
wrong = screen.evaluate(wrong_doc, model)
if wrong["advance_to_full_suite"]:
    raise AssertionError(wrong)
print("PASS decision-error-blocks-screening")

regressed_doc = trials()
first_case = screen.SCREEN_CASES[0]
for run in regressed_doc["runs"]:
    if run["case_id"] == first_case and run["representation"] == "candidate":
        run["observed"]["unnecessary_reference_loads"] = 2
regressed = screen.evaluate(regressed_doc, model)
if regressed["advance_to_full_suite"]:
    raise AssertionError(regressed)
if not any("worsens avoidable_events" in e for e in regressed["screening_errors"]):
    raise AssertionError(regressed)
print("PASS per-case-regression-cannot-be-averaged-away")

mismatch_doc = trials()
first_pair = mismatch_doc["runs"][0]["pair_id"]
next(
    run for run in mismatch_doc["runs"]
    if run["pair_id"] == first_pair and run["representation"] == "candidate"
)["input_fingerprint"] = "different"
try:
    screen.evaluate(mismatch_doc, model)
except ValueError as exc:
    if "mismatched input fingerprints" not in str(exc):
        raise
    print("PASS screening-input-mismatch-rejected")
else:
    raise AssertionError("mismatched screening input unexpectedly accepted")
