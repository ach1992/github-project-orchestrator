#!/usr/bin/env python3
"""Deterministic mocked tests for the auditable model-trial runner."""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "tools" / "run_model_trials.py"
SCORER_PATH = ROOT / "tools" / "score_model_trials.py"
MANIFEST_PATH = ROOT / "benchmarks" / "phase7" / "model-trial-cases.json"
SCENARIOS_PATH = ROOT / "benchmarks" / "phase7" / "runtime-optimization-scenarios.json"

runner_spec = importlib.util.spec_from_file_location("model_trial_runner", RUNNER_PATH)
if runner_spec is None or runner_spec.loader is None:
    raise RuntimeError(f"Unable to load {RUNNER_PATH}")
runner = importlib.util.module_from_spec(runner_spec)
sys.modules[runner_spec.name] = runner
runner_spec.loader.exec_module(runner)

scorer_spec = importlib.util.spec_from_file_location("model_trial_scorer_for_runner", SCORER_PATH)
if scorer_spec is None or scorer_spec.loader is None:
    raise RuntimeError(f"Unable to load {SCORER_PATH}")
scorer = importlib.util.module_from_spec(scorer_spec)
scorer_spec.loader.exec_module(scorer)

manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
scenarios = json.loads(SCENARIOS_PATH.read_text(encoding="utf-8"))
candidate_ref = "9" * 40
experiment = {
    "schema_version": 1,
    "experiment_id": "fixture-experiment",
    "baseline_ref": runner.PROGRAM_BASELINE_REF,
    "baseline_entrypoint": "skill/SKILL.md",
    "replacement": {
        "start_heading": "## 1. Role and runtime state",
        "end_heading_exclusive": "## 2. Universal invariants",
        "candidate_section": "benchmarks/phase7/experiments/fixture/candidate-section.md",
    },
    "semantic_change_allowed": False,
    "canonical_runtime_changed_during_prototype": False,
    "screening_case_ids": ["hot-fast-master-path", "cold-master-recovery"],
    "selection_case_contract": runner.SEMANTIC_CASE_CONTRACT,
    "model_trial_manifest": runner.MODEL_TRIAL_MANIFEST,
}
runner.validate_experiment(copy.deepcopy(experiment))
cases_by_id = runner.validate_contracts(
    copy.deepcopy(manifest), copy.deepcopy(scenarios), copy.deepcopy(experiment)
)
print("PASS runner-contract-single-owner")

plan = runner.build_plan(
    copy.deepcopy(manifest),
    cases_by_id,
    copy.deepcopy(experiment),
    candidate_ref,
    "screening",
    manifest["minimum_pairs_per_case"],
    "fixture-trial",
)
if len(plan["runs"]) != 12:
    raise AssertionError(f"screening plan must contain 12 executions: {len(plan['runs'])}")
if plan["case_ids"] != experiment["screening_case_ids"]:
    raise AssertionError(plan["case_ids"])
for case_id in plan["case_ids"]:
    pairs = {}
    for row in [r for r in plan["runs"] if r["case_id"] == case_id]:
        pairs.setdefault(row["pair_id"], []).append(row)
    if len(pairs) != 3:
        raise AssertionError(pairs)
    first_counts = {"baseline": 0, "candidate": 0}
    for rows in pairs.values():
        if len({r["input_text"] for r in rows}) != 1 or len(
            {r["input_fingerprint"] for r in rows}
        ) != 1:
            raise AssertionError("paired inputs must be exact")
        first = next(row for row in rows if row["order"] == 1)
        first_counts[first["representation"]] += 1
    if abs(first_counts["baseline"] - first_counts["candidate"]) > 1:
        raise AssertionError(first_counts)
print("PASS deterministic-12-execution-screening-plan")

mismatch = copy.deepcopy(plan)
mismatch["runs"][1]["input_text"] += " drift"
mismatch["plan_fingerprint"] = runner.fingerprint(
    {key: value for key, value in mismatch.items() if key != "plan_fingerprint"}
)
try:
    runner.validate_plan(mismatch)
except ValueError as exc:
    if "input_fingerprint" not in str(exc) and "inputs do not match" not in str(exc):
        raise
    print("PASS paired-input-drift-rejected")
else:
    raise AssertionError("paired input drift unexpectedly accepted")

bad_order = copy.deepcopy(plan)
first_pair = bad_order["runs"][0]["pair_id"]
for row in bad_order["runs"]:
    if row["pair_id"] == first_pair:
        row["order"] = 1
bad_order["plan_fingerprint"] = runner.fingerprint(
    {key: value for key, value in bad_order.items() if key != "plan_fingerprint"}
)
try:
    runner.validate_plan(bad_order)
except ValueError as exc:
    if "complementary order" not in str(exc):
        raise
    print("PASS order-plan-mutation-rejected")
else:
    raise AssertionError("order mutation unexpectedly accepted")

duplicate_run = copy.deepcopy(plan)
duplicate_run["runs"][1]["run_id"] = duplicate_run["runs"][0]["run_id"]
duplicate_run["plan_fingerprint"] = runner.fingerprint(
    {key: value for key, value in duplicate_run.items() if key != "plan_fingerprint"}
)
try:
    runner.validate_plan(duplicate_run)
except ValueError as exc:
    if "run_id" not in str(exc):
        raise
    print("PASS duplicate-run-identity-rejected")
else:
    raise AssertionError("duplicate run identity unexpectedly accepted")

try:
    runner.validate_candidate_ref(runner.PROGRAM_BASELINE_REF)
except ValueError as exc:
    if "distinct" not in str(exc):
        raise
    print("PASS candidate-identity-drift-rejected")
else:
    raise AssertionError("baseline reused as candidate")

bad_experiment = copy.deepcopy(experiment)
bad_experiment["baseline_ref"] = "0" * 40
try:
    runner.validate_experiment(bad_experiment)
except ValueError as exc:
    if "baseline drifted" not in str(exc):
        raise
    print("PASS experiment-baseline-drift-rejected")
else:
    raise AssertionError("experiment baseline drift unexpectedly accepted")

try:
    runner.build_runtime_config(
        api_base_url="https://example.invalid/v1",
        model_id="fixture-model",
        model_version="fixture-v1",
        settings_json="{}",
        instruction_role="system",
        timeout_seconds=10,
        max_model_turns=4,
        environ={},
    )
except ValueError as exc:
    if "RUNTIME_MODEL_API_KEY" not in str(exc):
        raise
    print("PASS missing-runtime-secret-fails-closed")
else:
    raise AssertionError("live config unexpectedly accepted without runtime secret")

try:
    runner.parse_settings('{"authorization":"must-not-be-here"}')
except ValueError as exc:
    if "sensitive-looking" not in str(exc):
        raise
    print("PASS sensitive-model-setting-rejected")
else:
    raise AssertionError("sensitive model setting unexpectedly accepted")

base_runtime = runner.RuntimeView(
    label="baseline",
    ref=runner.PROGRAM_BASELINE_REF,
    entrypoint="baseline runtime entrypoint",
    references={"references/master-cycle.md": "baseline reference content"},
    entrypoint_sha256=runner.sha256_text("baseline runtime entrypoint"),
)
candidate_runtime = runner.RuntimeView(
    label="candidate",
    ref=candidate_ref,
    entrypoint="candidate runtime entrypoint",
    references={"references/master-cycle.md": "baseline reference content"},
    entrypoint_sha256=runner.sha256_text("candidate runtime entrypoint"),
)
secret = "fixture-super-secret-api-key"
config, loaded_secret = runner.build_runtime_config(
    api_base_url="https://provider.example/v1",
    model_id="fixture-model",
    model_version="fixture-v1",
    settings_json='{"temperature":0}',
    instruction_role="system",
    timeout_seconds=10,
    max_model_turns=4,
    environ={"RUNTIME_MODEL_API_KEY": secret},
)
if loaded_secret != secret:
    raise AssertionError("runtime secret was not loaded from environment")


class FinalTransport:
    def __init__(self):
        self.calls = []

    def __call__(self, endpoint, api_key, payload, timeout):
        if api_key != secret or endpoint != "https://provider.example/v1/chat/completions":
            raise AssertionError("transport envelope drift")
        self.calls.append(copy.deepcopy(payload))
        index = len(self.calls)
        return (
            {
                "id": f"response-{index}",
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {"role": "assistant", "content": "observable output"},
                    }
                ],
            },
            {"http_status": 200},
        )


transport = FinalTransport()
raw, template = runner.execute_suite(
    ROOT,
    copy.deepcopy(plan),
    base_runtime,
    candidate_runtime,
    config,
    secret,
    transport=transport,
)
if raw["status"] != "complete" or template is None or len(raw["runs"]) != 12:
    raise AssertionError(raw)
for index in range(0, len(transport.calls), 2):
    first_user = transport.calls[index]["messages"][1]["content"]
    second_user = transport.calls[index + 1]["messages"][1]["content"]
    if first_user != second_user:
        raise AssertionError("baseline/candidate did not receive exact paired input")
print("PASS mocked-positive-paired-execution")

forbidden_keys = {"chain_of_thought", "private_reasoning", "reasoning_content"}


def walk_keys(value):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key
            yield from walk_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from walk_keys(nested)


if forbidden_keys.intersection(walk_keys(raw)):
    raise AssertionError("raw evidence exposed a private-reasoning field")
print("PASS raw-evidence-private-reasoning-fields-absent")

if any(run["observed"]["correct_next_action"] is not None for run in template["runs"]):
    raise AssertionError("annotation template silently judged correctness")
try:
    scorer.evaluate(copy.deepcopy(manifest), copy.deepcopy(template))
except ValueError:
    print("PASS unannotated-template-cannot-be-scored")
else:
    raise AssertionError("unannotated template unexpectedly passed scorer validation")

missing_audit = copy.deepcopy(raw)
missing_audit["runs"][0]["audit_ref"] = ""
try:
    runner.validate_raw_evidence(missing_audit)
except ValueError as exc:
    if "audit_ref" not in str(exc):
        raise
    print("PASS missing-audit-identity-rejected")
else:
    raise AssertionError("missing audit identity unexpectedly accepted")

duplicate_audit = copy.deepcopy(raw)
duplicate_audit["runs"][1]["audit_ref"] = duplicate_audit["runs"][0]["audit_ref"]
try:
    runner.validate_raw_evidence(duplicate_audit)
except ValueError as exc:
    if "audit_ref" not in str(exc):
        raise
    print("PASS duplicate-audit-identity-rejected")
else:
    raise AssertionError("duplicate audit identity unexpectedly accepted")


class ToolTransport:
    def __init__(self):
        self.count = 0

    def __call__(self, endpoint, api_key, payload, timeout):
        self.count += 1
        if self.count == 1:
            return (
                {
                    "id": "tool-response",
                    "choices": [
                        {
                            "finish_reason": "tool_calls",
                            "message": {
                                "role": "assistant",
                                "content": None,
                                "tool_calls": [
                                    {
                                        "id": "call-1",
                                        "type": "function",
                                        "function": {
                                            "name": "read_runtime_reference",
                                            "arguments": '{"path":"references/master-cycle.md"}',
                                        },
                                    }
                                ],
                            },
                        }
                    ],
                },
                {"http_status": 200},
            )
        tool_message = payload["messages"][-1]
        if tool_message["role"] != "tool" or "baseline reference content" not in tool_message["content"]:
            raise AssertionError("runtime reference tool result was not returned to model")
        return (
            {
                "id": "final-response",
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {"role": "assistant", "content": "after tool"},
                    }
                ],
            },
            {"http_status": 200},
        )


single = runner.execute_conversation(
    base_runtime,
    plan["runs"][0],
    config,
    secret,
    ToolTransport(),
)
if single["tool_operations"][0]["path"] != "references/master-cycle.md":
    raise AssertionError(single)
if "content" in single["tool_operations"][0]:
    raise AssertionError("raw tool audit should hash reference content rather than duplicate it")
print("PASS observable-runtime-reference-tool-audit")


class FailingTransport:
    def __init__(self):
        self.count = 0

    def __call__(self, endpoint, api_key, payload, timeout):
        self.count += 1
        if self.count == 2:
            raise runner.TransportError(f"simulated failure accidentally echoed {secret}")
        return (
            {
                "id": f"response-{self.count}",
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {"role": "assistant", "content": "first run"},
                    }
                ],
            },
            {"http_status": 200},
        )


partial, partial_template = runner.execute_suite(
    ROOT,
    copy.deepcopy(plan),
    base_runtime,
    candidate_runtime,
    config,
    secret,
    transport=FailingTransport(),
)
serialized = json.dumps(partial)
if partial["status"] != "incomplete" or partial_template is not None:
    raise AssertionError(partial)
if secret in serialized or "[REDACTED]" not in serialized:
    raise AssertionError("partial evidence did not redact runtime secret")
if len(partial["runs"]) != 1:
    raise AssertionError("transport failure must fail closed rather than continue an imbalanced suite")
print("PASS transport-failure-partial-evidence-fails-closed-and-redacts-secret")
