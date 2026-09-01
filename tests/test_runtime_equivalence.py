#!/usr/bin/env python3
"""Adversarial fixtures for the immutable v1.2.2 runtime-equivalence gate."""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "benchmarks" / "phase7"
CHECKER = ROOT / "tools" / "check_runtime_equivalence.py"
CONFIG = BENCH / "runtime-optimization-baseline.json"
LANE = BENCH / "runtime-optimization-scenarios.json"
MODEL_TRIAL = BENCH / "model-trial-cases.json"

spec = importlib.util.spec_from_file_location("runtime_equivalence", CHECKER)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Unable to load {CHECKER}")
eq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eq)

config = json.loads(CONFIG.read_text(encoding="utf-8"))
result = eq.check_repository(ROOT, copy.deepcopy(config))
if not result["ok"]:
    raise AssertionError(result)
print("PASS immutable-v1.2.2-baseline-equivalence")

bad_config = copy.deepcopy(config)
bad_config["baseline_ref"] = "0" * 40
try:
    eq.validate_config(bad_config)
except ValueError as exc:
    if "must remain pinned to program baseline" not in str(exc):
        raise
    print("PASS baseline-ref-drift-rejected")
else:
    raise AssertionError("baseline-ref-drift: unexpectedly passed")

bad_config = copy.deepcopy(config)
bad_config["baseline_version"] = "9.9.9"
try:
    eq.validate_config(bad_config)
except ValueError as exc:
    if "must remain pinned to program baseline" not in str(exc):
        raise
    print("PASS baseline-version-drift-rejected")
else:
    raise AssertionError("baseline-version-drift: unexpectedly passed")

lane = json.loads(LANE.read_text(encoding="utf-8"))
if lane.get("schema_version") != 1:
    raise AssertionError("runtime optimization lane schema_version must be 1")
if lane.get("baseline_ref") != config["baseline_ref"]:
    raise AssertionError("runtime optimization lane must use the immutable configured baseline")
evidence_policy = lane.get("evidence_policy", {})
if evidence_policy.get("source_grounded_trace_is_model_performance_proof") is not False:
    raise AssertionError("source-grounded evidence must not claim independent model-performance proof")
if evidence_policy.get("source_grounded_friction_is_diagnostic_only") is not True:
    raise AssertionError("source-grounded friction must remain diagnostic-only")
if "practical_improvement_requires_actual_model_runtime_ab" in evidence_policy:
    raise AssertionError("obsolete mandatory actual model/runtime A/B policy must not remain active")
if evidence_policy.get("actual_model_runtime_ab_is_optional_corroboration") is not True:
    raise AssertionError("actual model/runtime A/B must remain optional corroboration")
if evidence_policy.get("candidate_requires_material_improvement_before_migration") is not True:
    raise AssertionError("candidate must still prove material improvement before migration")
if evidence_policy.get("protected_behavior_is_hard_gate") is not True:
    raise AssertionError("protected behavior must remain a hard gate")
required_cases = {
    "hot-fast-master-path",
    "consequential-mutation-authority-path",
    "worker-dispatch-and-resume",
    "cold-master-recovery",
    "review-integration-freshness",
    "pending-external-job-continuation",
    "integration-versus-delivery",
    "namespace-and-effect-isolation",
}
observed_cases = {case["id"] for case in lane.get("comparison_cases", [])}
if observed_cases != required_cases:
    raise AssertionError(
        f"runtime optimization comparison cases changed: expected={sorted(required_cases)} "
        f"observed={sorted(observed_cases)}"
    )
for case in lane["comparison_cases"]:
    if not case.get("protect") or not case.get("measure") or not case.get("eval_anchors"):
        raise AssertionError(f"comparison case is incomplete: {case.get('id')}")
print("PASS runtime-optimization-comparison-contract")

model_trial = json.loads(MODEL_TRIAL.read_text(encoding="utf-8"))
if model_trial.get("semantic_case_contract") != "benchmarks/phase7/runtime-optimization-scenarios.json":
    raise AssertionError("model trials must reference the canonical runtime optimization semantic case contract")
if set(model_trial.get("case_ids", [])) != observed_cases:
    raise AssertionError(
        "model-trial case IDs must exactly select the canonical runtime optimization cases"
    )
print("PASS model-trial-semantic-case-single-owner")

baseline = result["baseline_inventory"]


def expect_failure(name: str, candidate: dict, contains: str) -> None:
    errors, _notes = eq.compare_inventories(copy.deepcopy(baseline), candidate)
    text = "\n".join(errors)
    if contains not in text:
        raise AssertionError(f"{name}: expected {contains!r} in {text!r}")
    print(f"PASS {name}")


candidate = copy.deepcopy(baseline)
removed_rule = next(iter(candidate["rule_owners"]))
del candidate["rule_owners"][removed_rule]
expect_failure("removed-rule-rejected", candidate, "canonical Rule IDs removed")

candidate = copy.deepcopy(baseline)
rule = next(iter(candidate["rule_owners"]))
candidate["rule_owners"][rule] = "`different-owner.md`"
expect_failure("owner-drift-rejected", candidate, "canonical Rule owner changed")

candidate = copy.deepcopy(baseline)
candidate["goals"] = candidate["goals"][:-1]
expect_failure("goal-loss-rejected", candidate, "canonical Goal set changed")

candidate = copy.deepcopy(baseline)
namespace = "TaskState"
candidate["states"][namespace] = candidate["states"][namespace][:-1]
expect_failure("state-loss-rejected", candidate, "TaskState token set changed")

candidate = copy.deepcopy(baseline)
candidate["states"]["WorkerStatus"] = sorted(
    candidate["states"]["WorkerStatus"] + ["NEW_UNAPPROVED_STATE"]
)
expect_failure("state-expansion-rejected", candidate, "WorkerStatus token set changed")

candidate = copy.deepcopy(baseline)
candidate["direct_refs"] = candidate["direct_refs"][1:]
expect_failure("direct-router-loss-rejected", candidate, "no longer routed from SKILL.md")

candidate = copy.deepcopy(baseline)
candidate["eval_ids"] = candidate["eval_ids"][1:]
expect_failure("eval-loss-rejected", candidate, "baseline evaluation scenarios removed")

candidate = copy.deepcopy(baseline)
candidate["predicates_present"]["CAN_EXECUTE"] = False
expect_failure("predicate-owner-loss-rejected", candidate, "candidate predicate is not discoverable")

candidate = copy.deepcopy(baseline)
candidate["eval_ids"] = sorted(candidate["eval_ids"] + ["ZZ"])
errors, notes = eq.compare_inventories(copy.deepcopy(baseline), candidate)
if errors:
    raise AssertionError(f"additive-eval: unexpected errors: {errors}")
if not any("adds evaluation scenarios" in note for note in notes):
    raise AssertionError(f"additive-eval: expected review note, got {notes}")
print("PASS additive-eval-allowed-and-reported")

candidate = copy.deepcopy(baseline)
candidate["direct_refs"] = sorted(
    candidate["direct_refs"] + ["skill/references/example-additive.md"]
)
errors, notes = eq.compare_inventories(copy.deepcopy(baseline), candidate)
if errors:
    raise AssertionError(f"additive-direct-ref: unexpected errors: {errors}")
if not any("review activation cost" in note for note in notes):
    raise AssertionError(f"additive-direct-ref: expected activation-cost note, got {notes}")
print("PASS additive-direct-ref-allowed-and-reported")
