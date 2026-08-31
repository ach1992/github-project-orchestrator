#!/usr/bin/env python3
"""Adversarial checks for the Phase 7 operational benchmark scorer."""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "benchmarks" / "phase7"
SCORER = ROOT / "tools" / "score_phase7_benchmark.py"

spec = importlib.util.spec_from_file_location("phase7_score", SCORER)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Unable to load {SCORER}")
score = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score)

scenarios = json.loads((BENCH / "scenarios.json").read_text(encoding="utf-8"))
baseline = json.loads((BENCH / "traces-v1.0.0.json").read_text(encoding="utf-8"))
current = json.loads((BENCH / "traces-current.json").read_text(encoding="utf-8"))
runtime_baseline = json.loads((BENCH / "traces-v1.2.2.json").read_text(encoding="utf-8"))


def result(cur: dict) -> dict:
    return score.evaluate(copy.deepcopy(scenarios), copy.deepcopy(baseline), cur)


def trace(doc: dict, scenario_id: str) -> dict:
    return next(item for item in doc["traces"] if item["scenario_id"] == scenario_id)


def expect_fail(name: str, cur: dict, contains: str) -> None:
    outcome = result(cur)
    if outcome["ok"]:
        raise AssertionError(f"{name}: unexpectedly passed")
    text = "\n".join(outcome["acceptance_errors"])
    if contains not in text:
        raise AssertionError(f"{name}: missing {contains!r} in {text!r}")
    print(f"PASS {name}")


valid = result(copy.deepcopy(current))
if not valid["ok"]:
    raise AssertionError(valid)
print("PASS valid-benchmark")

score.validate_source_refs(ROOT, baseline, current)
print("PASS pinned-source-provenance")

floating = copy.deepcopy(current)
trace(floating, "small-routine-fix")["source_basis"][0] = "main:skill/SKILL.md"
try:
    score.validate_source_refs(ROOT, baseline, floating)
except ValueError as exc:
    if "floating or malformed source_basis" not in str(exc):
        raise
    print("PASS floating-provenance-rejected")
else:
    raise AssertionError("floating-provenance: unexpectedly passed")

cur = copy.deepcopy(current)
t = trace(cur, "review-head-drift")
t["events"] = [
    event
    for event in t["events"]
    if not (event["type"] == "fresh_review" and event.get("candidate") == "c2")
]
expect_fail("stale-integration", cur, "stale_integration")

cur = copy.deepcopy(current)
t = trace(cur, "review-head-drift")
t["events"] = [
    event
    for event in t["events"]
    if not (event["type"] == "fresh_review" and event.get("candidate") == "c2")
]
next(event for event in t["events"] if event["type"] == "integration_verified")["candidate"] = "c1"
expect_fail("old-candidate-review-invalidated", cur, "stale_integration")

cur = copy.deepcopy(current)
t = trace(cur, "auto-production-release")
t["events"] = [event for event in t["events"] if event["type"] != "delivery_verified"]
expect_fail("missing-delivery-verification", cur, "missing_delivery_verification")

cur = copy.deepcopy(current)
t = trace(cur, "local-blocker-independent-work")
next(event for event in t["events"] if event["type"] == "stop")["boundary"] = "BLOCKED"
expect_fail("premature-global-stop", cur, "wrong_stop")

cur = copy.deepcopy(current)
t = trace(cur, "small-routine-fix")
t["events"].insert(2, {"type": "human_confirmation", "reason": "unnecessary"})
expect_fail("unnecessary-confirmation", cur, "current worsened unnecessary_confirmations")

cur = copy.deepcopy(current)
t = trace(cur, "small-routine-fix")
t["events"].insert(2, {"type": "unsafe_shortcut"})
expect_fail("unsafe-shortcut", cur, "unsafe_shortcut")

cur = copy.deepcopy(current)
t = trace(cur, "bounded-worker-delegation")
next(event for event in t["events"] if event["type"] == "coordination")["value"] = "STANDARD"
expect_fail("coordination-overweight", cur, "coordination_mismatch")

# Representation-optimization lane: first validate the exact v1.2.2 policy trace
# without claiming that a source-grounded simulation is independent model evidence.
runtime_valid = score.validate_trace_set(copy.deepcopy(scenarios), copy.deepcopy(runtime_baseline))
if not runtime_valid["ok"]:
    raise AssertionError(runtime_valid)
print("PASS v1.2.2-runtime-baseline-valid")
score.validate_source_refs(ROOT, runtime_baseline)
print("PASS v1.2.2-runtime-baseline-provenance")

# Identical traces are not an optimization win. A representation candidate must have
# a material measured improvement rather than merely a different shape/version label.
same_candidate = copy.deepcopy(runtime_baseline)
same_candidate["version"] = "a" * 40
same_result = score.evaluate_candidate_pair(
    copy.deepcopy(scenarios), copy.deepcopy(runtime_baseline), same_candidate
)
if same_result["ok"] or not any(
    "no material source-grounded friction improvement" in error
    for error in same_result["acceptance_errors"]
):
    raise AssertionError(f"identical-candidate unexpectedly accepted: {same_result}")
print("PASS identical-representation-not-a-win")

# Model a lossless representation improvement that avoids one pre-action re-derivation
# in the hot path while keeping all protected scenario events intact.
improved_candidate = copy.deepcopy(runtime_baseline)
improved_candidate["version"] = "b" * 40
hot = trace(improved_candidate, "small-routine-fix")
for index, event in enumerate(hot["events"]):
    if event == {"type": "classify", "target": "Role"}:
        del hot["events"][index]
        break
improved_result = score.evaluate_candidate_pair(
    copy.deepcopy(scenarios), copy.deepcopy(runtime_baseline), improved_candidate
)
if not improved_result["ok"]:
    raise AssertionError(improved_result)
if "steps_to_first_useful_action" not in improved_result["improved_material_fields"]:
    raise AssertionError(improved_result)
print("PASS measurable-lossless-candidate-improvement")

unsafe_candidate = copy.deepcopy(improved_candidate)
trace(unsafe_candidate, "small-routine-fix")["events"].insert(2, {"type": "unsafe_shortcut"})
unsafe_result = score.evaluate_candidate_pair(
    copy.deepcopy(scenarios), copy.deepcopy(runtime_baseline), unsafe_candidate
)
if unsafe_result["ok"] or not any(
    "unsafe_shortcut" in error for error in unsafe_result["acceptance_errors"]
):
    raise AssertionError(f"unsafe candidate unexpectedly accepted: {unsafe_result}")
print("PASS optimization-cannot-average-away-safety-regression")

worse_candidate = copy.deepcopy(improved_candidate)
trace(worse_candidate, "small-routine-fix")["events"].insert(
    2, {"type": "load_domain", "target": "unnecessary-cold-domain"}
)
worse_result = score.evaluate_candidate_pair(
    copy.deepcopy(scenarios), copy.deepcopy(runtime_baseline), worse_candidate
)
if worse_result["ok"] or not any(
    "candidate worsened context_domains" in error
    for error in worse_result["acceptance_errors"]
):
    raise AssertionError(f"context-regressing candidate unexpectedly accepted: {worse_result}")
print("PASS context-regression-rejected")
