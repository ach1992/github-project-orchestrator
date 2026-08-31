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


# Historical Phase 7 acceptance remains unchanged.
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

# Representation-optimization source-grounded lane validates protected behavior and
# reports diagnostics only. It is deliberately ineligible to prove LLM optimization.
runtime_valid = score.validate_trace_set(copy.deepcopy(scenarios), copy.deepcopy(runtime_baseline))
if not runtime_valid["ok"]:
    raise AssertionError(runtime_valid)
if runtime_valid["optimization_claim_eligible"] is not False:
    raise AssertionError(runtime_valid)
print("PASS v1.2.2-runtime-baseline-valid-not-performance-proof")
score.validate_source_refs(ROOT, runtime_baseline)
print("PASS v1.2.2-runtime-baseline-provenance")

# Identical source-grounded traces are semantically acceptable. They simply prove no
# measured model/runtime improvement by itself; current program policy owns the broader practical-benefit determination, with paired model/runtime trials optional corroboration.
same_candidate = copy.deepcopy(runtime_baseline)
same_candidate["version"] = "a" * 40
same_result = score.evaluate_candidate_pair(
    copy.deepcopy(scenarios), copy.deepcopy(runtime_baseline), same_candidate
)
if not same_result["ok"]:
    raise AssertionError(same_result)
if same_result["optimization_claim_eligible"] is not False:
    raise AssertionError(same_result)
if any(same_result["diagnostic_deltas"].values()):
    raise AssertionError(same_result)
print("PASS identical-source-trace-valid-but-not-an-optimization-claim")

# A hand-authored synthetic reduction is diagnostic only; it must never become evidence
# that a model actually reconstructs fewer decisions or executes faster/more accurately.
reduced_candidate = copy.deepcopy(runtime_baseline)
reduced_candidate["version"] = "b" * 40
hot = trace(reduced_candidate, "small-routine-fix")
for index, event in enumerate(hot["events"]):
    if event == {"type": "classify", "target": "Role"}:
        del hot["events"][index]
        break
reduced_result = score.evaluate_candidate_pair(
    copy.deepcopy(scenarios), copy.deepcopy(runtime_baseline), reduced_candidate
)
if not reduced_result["ok"]:
    raise AssertionError(reduced_result)
if reduced_result["optimization_claim_eligible"] is not False:
    raise AssertionError(reduced_result)
if "steps_to_first_useful_action" not in reduced_result["diagnostic_reductions"]:
    raise AssertionError(reduced_result)
print("PASS synthetic-source-reduction-remains-diagnostic-only")

# Protected-behavior failures remain hard failures in the source-grounded lane.
unsafe_candidate = copy.deepcopy(reduced_candidate)
trace(unsafe_candidate, "small-routine-fix")["events"].insert(2, {"type": "unsafe_shortcut"})
unsafe_result = score.evaluate_candidate_pair(
    copy.deepcopy(scenarios), copy.deepcopy(runtime_baseline), unsafe_candidate
)
if unsafe_result["ok"] or not any(
    "unsafe_shortcut" in error for error in unsafe_result["acceptance_errors"]
):
    raise AssertionError(f"unsafe candidate unexpectedly accepted: {unsafe_result}")
print("PASS source-grounded-safety-regression-rejected")

# Structural friction increases are surfaced for review but are not misrepresented as
# measured LLM regressions; current program evidence policy decides practical value, with actual A/B trials optional corroboration.
noisier_candidate = copy.deepcopy(runtime_baseline)
noisier_candidate["version"] = "c" * 40
trace(noisier_candidate, "small-routine-fix")["events"].insert(
    2, {"type": "load_domain", "target": "unnecessary-cold-domain"}
)
noisier_result = score.evaluate_candidate_pair(
    copy.deepcopy(scenarios), copy.deepcopy(runtime_baseline), noisier_candidate
)
if not noisier_result["ok"]:
    raise AssertionError(noisier_result)
if noisier_result["optimization_claim_eligible"] is not False:
    raise AssertionError(noisier_result)
if "context_domains" not in noisier_result["diagnostic_regressions"]:
    raise AssertionError(noisier_result)
print("PASS source-context-regression-reported-not-overclaimed")
