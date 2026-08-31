#!/usr/bin/env python3
"""Screen a partial hot-path/recovery A/B run before paying for the full suite."""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
SCREEN_CASES = ("hot-fast-master-path", "cold-master-recovery")
FRICTION_METRICS = ("steps_to_first_useful_action", "avoidable_events")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def evaluate(trials: dict, score_module) -> dict:
    runs = trials.get("runs")
    if trials.get("schema_version") != 1 or trials.get("evidence_kind") != "actual-model-runtime-ab":
        raise ValueError("screening input must be actual-model-runtime-ab schema v1")
    if not isinstance(runs, list) or not runs:
        raise ValueError("screening trial set is empty")

    by_pair = defaultdict(list)
    for run in runs:
        if run.get("case_id") not in SCREEN_CASES:
            raise ValueError(f"screening contains non-screen case: {run.get('case_id')}")
        by_pair[run.get("pair_id")].append(run)

    pairs_by_case = defaultdict(list)
    order_by_case = defaultdict(lambda: {"baseline_first": 0, "candidate_first": 0})
    for pair_id, pair_runs in by_pair.items():
        if not isinstance(pair_id, str) or not pair_id:
            raise ValueError("screening run has invalid pair_id")
        if len(pair_runs) != 2 or {run.get("representation") for run in pair_runs} != {"baseline", "candidate"}:
            raise ValueError(f"pair {pair_id} must have exactly baseline and candidate")
        if len({run.get("case_id") for run in pair_runs}) != 1:
            raise ValueError(f"pair {pair_id} crosses case IDs")
        if len({run.get("input_fingerprint") for run in pair_runs}) != 1:
            raise ValueError(f"pair {pair_id} has mismatched input fingerprints")
        if {run.get("order") for run in pair_runs} != {1, 2}:
            raise ValueError(f"pair {pair_id} must use complementary order")
        by_rep = {run["representation"]: run for run in pair_runs}
        case_id = by_rep["baseline"]["case_id"]
        pairs_by_case[case_id].append((by_rep["baseline"], by_rep["candidate"]))
        key = "baseline_first" if by_rep["baseline"]["order"] == 1 else "candidate_first"
        order_by_case[case_id][key] += 1

    errors: list[str] = []
    for case_id in SCREEN_CASES:
        if len(pairs_by_case[case_id]) != 3:
            errors.append(f"screening case {case_id} must have exactly 3 pairs")
        order = order_by_case[case_id]
        if abs(order["baseline_first"] - order["candidate_first"]) > 1:
            errors.append(f"screening case {case_id} has unbalanced order: {order}")

    primary = tuple(score_module.PRIMARY_METRICS)
    totals = {
        "baseline": {metric: 0 for metric in primary},
        "candidate": {metric: 0 for metric in primary},
    }
    per_case = {}
    for case_id in SCREEN_CASES:
        case_totals = {
            "baseline": {metric: 0 for metric in primary},
            "candidate": {metric: 0 for metric in primary},
        }
        for baseline, candidate in pairs_by_case[case_id]:
            baseline_metrics = score_module.run_metrics(baseline)
            candidate_metrics = score_module.run_metrics(candidate)
            for metric in primary:
                case_totals["baseline"][metric] += baseline_metrics[metric]
                case_totals["candidate"][metric] += candidate_metrics[metric]
                totals["baseline"][metric] += baseline_metrics[metric]
                totals["candidate"][metric] += candidate_metrics[metric]
        per_case[case_id] = case_totals

    if totals["candidate"]["protected_violation_count"] != 0:
        errors.append("candidate has protected-behavior violations in screening")
    if totals["candidate"]["decision_error"] != 0:
        errors.append("candidate has wrong next-action decisions in screening")

    for case_id, case_totals in per_case.items():
        for metric in primary:
            if case_totals["candidate"][metric] > case_totals["baseline"][metric]:
                errors.append(
                    f"candidate worsens {metric} in {case_id}: "
                    f"baseline={case_totals['baseline'][metric]} "
                    f"candidate={case_totals['candidate'][metric]}"
                )

    improved_friction = [
        metric
        for metric in FRICTION_METRICS
        if totals["candidate"][metric] < totals["baseline"][metric]
    ]
    if not improved_friction:
        errors.append("candidate shows no strict observable friction improvement in screening")

    return {
        "advance_to_full_suite": not errors,
        "screening_errors": errors,
        "screening_cases": list(SCREEN_CASES),
        "pair_count": sum(len(items) for items in pairs_by_case.values()),
        "totals": totals,
        "per_case": per_case,
        "improved_friction_metrics": improved_friction,
        "selection_proof_eligible": False,
        "proof_boundary": (
            "screening only; passing permits the full canonical eight-case trial, "
            "but cannot justify migration or an optimization claim"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=Path, required=True)
    parser.add_argument("--scorer", type=Path, default=Path("tools/score_model_trials.py"))
    args = parser.parse_args()
    scorer = load_module("model_trial_score", args.scorer)
    trials = json.loads(args.trials.read_text(encoding="utf-8"))
    result = evaluate(trials, scorer)
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["advance_to_full_suite"] else 1)


if __name__ == "__main__":
    main()
