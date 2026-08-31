#!/usr/bin/env python3
"""Deterministic fixtures for the observable runtime A/B trial harness."""
from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "tools" / "run_runtime_ab_trials.py"
INPUTS = ROOT / "benchmarks" / "phase7" / "experiments" / "decision-frame-v1" / "trial-inputs.json"

spec = importlib.util.spec_from_file_location("runtime_ab_harness", HARNESS)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Unable to load {HARNESS}")
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)

inputs_doc = json.loads(INPUTS.read_text(encoding="utf-8"))
inputs = h.validate_inputs(inputs_doc)
if len(inputs) != 24:
    raise AssertionError(f"expected 24 frozen inputs, got {len(inputs)}")
counts = Counter(item["case_id"] for item in inputs)
if set(counts.values()) != {3} or len(counts) != 8:
    raise AssertionError(f"expected 3 inputs across 8 cases, got {counts}")
print("PASS frozen-24-input-contract")

for item in inputs:
    visible = h.model_visible_input(item)
    if "oracle" in visible:
        raise AssertionError("oracle leaked into model-visible input")
    if h.fingerprint(visible) != h.fingerprint(h.model_visible_input(item)):
        raise AssertionError("input fingerprint is not deterministic")
print("PASS hidden-oracle-and-deterministic-input-fingerprint")

screen = h.select_inputs(inputs, "screen")
if len(screen) != 6 or {item["case_id"] for item in screen} != {
    "hot-fast-master-path", "cold-master-recovery"
}:
    raise AssertionError("screening set must be exactly 6 frozen hot/recovery inputs")
if len(h.select_inputs(inputs, "full")) != 24:
    raise AssertionError("full selection set must contain all 24 inputs")
print("PASS screening-and-full-selection")


class FakeClient:
    def __init__(self, messages):
        self.responses = list(messages)

    def complete(self, messages, tools):
        if not self.responses:
            raise AssertionError("fake model exhausted")
        return {
            "message": self.responses.pop(0),
            "response_model": "fixture-model-v1",
        }


def call(call_id: str, name: str, args: dict) -> dict:
    return {
        "role": "assistant",
        "content": None,
        "tool_calls": [
            {
                "id": call_id,
                "type": "function",
                "function": {
                    "name": name,
                    "arguments": json.dumps(args),
                },
            }
        ],
    }


hot = next(item for item in inputs if item["input_id"] == "hot-fast-01")
client = FakeClient([
    call("c1", "load_reference", {"path": "references/master-cycle.md"}),
    call("c2", "execute_action", {"action_id": "inspect_target_file"}),
])
observed, transcript = h.run_one(
    client=client,
    item=hot,
    entrypoint="fixture skill entrypoint",
    read_reference=lambda path: f"fixture:{path}",
    representation="candidate",
    order=2,
    max_turns=4,
)
if observed != {
    "correct_next_action": True,
    "protected_violations": [],
    "steps_to_first_useful_action": 1,
    "unnecessary_questions": 0,
    "unnecessary_actions": 0,
    "unnecessary_reference_loads": 0,
    "manual_continue_required": False,
}:
    raise AssertionError(observed)
if transcript["private_chain_of_thought_recorded"] is not False:
    raise AssertionError("trial transcript must not claim to record private reasoning")
print("PASS correct-observable-tool-path")

client = FakeClient([
    call("c1", "resolve_state", {"dimension": "Role"}),
    call("c2", "load_reference", {"path": "references/master-cycle.md"}),
    call("c3", "execute_action", {"action_id": "inspect_target_file"}),
])
observed, _ = h.run_one(
    client=client,
    item=hot,
    entrypoint="fixture",
    read_reference=lambda path: f"fixture:{path}",
    representation="baseline",
    order=1,
    max_turns=5,
)
if observed["unnecessary_actions"] != 1 or observed["steps_to_first_useful_action"] != 2:
    raise AssertionError(observed)
print("PASS stable-state-reconstruction-is-observable-friction")

client = FakeClient([
    call("c1", "execute_action", {"action_id": "rebuild_project_plan"}),
])
observed, _ = h.run_one(
    client=client,
    item=hot,
    entrypoint="fixture",
    read_reference=lambda path: f"fixture:{path}",
    representation="candidate",
    order=2,
    max_turns=2,
)
if observed["correct_next_action"] is not False:
    raise AssertionError(observed)
if "incorrect_next_control_action" not in observed["protected_violations"]:
    raise AssertionError(observed)
if not any(
    item.startswith("missing_required_reference:")
    for item in observed["protected_violations"]
):
    raise AssertionError(observed)
print("PASS wrong-action-and-missing-domain-rejected")

client = FakeClient([
    {"role": "assistant", "content": "I would inspect the file.", "tool_calls": []}
])
observed, _ = h.run_one(
    client=client,
    item=hot,
    entrypoint="fixture",
    read_reference=lambda path: f"fixture:{path}",
    representation="candidate",
    order=2,
    max_turns=2,
)
if "non_tool_response" not in observed["protected_violations"]:
    raise AssertionError(observed)
print("PASS prose-instead-of-observable-tool-use-rejected")

system = h.build_system_prompt("fixture")
if "Do not reveal, describe, or output private chain-of-thought" not in system:
    raise AssertionError("harness must explicitly exclude private chain-of-thought")
print("PASS private-reasoning-not-requested")
