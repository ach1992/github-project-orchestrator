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

cur = copy.deepcopy(current)
t = trace(cur, "review-head-drift")
t["events"] = [
    event
    for event in t["events"]
    if not (event["type"] == "fresh_review" and event.get("candidate") == "c2")
]
expect_fail("stale-integration", cur, "stale_integration")

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
