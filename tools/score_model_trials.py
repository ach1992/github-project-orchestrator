#!/usr/bin/env python3
"""Score paired observable A/B trials for runtime-representation candidates.

This scorer never consumes or requests private chain-of-thought. It accepts only the
closed observable evidence schema plus auditable transcript/tool-log references.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from collections import defaultdict
from pathlib import Path

FULL_SHA_RE = re.compile(r"[0-9a-f]{40}")
PROGRAM_BASELINE_REF = "f98e8a242c720931e34aa7c4e8a799090e3d0495"
SEMANTIC_CASE_CONTRACT = "benchmarks/phase7/runtime-optimization-scenarios.json"
REQUIRED_CASE_CONTRACT_FIELDS = {
    "schema_version",
    "suite_id",
    "baseline_ref",
    "semantic_case_contract",
    "minimum_pairs_per_case",
    "sign_test_alpha",
    "evidence_kind",
    "primary_metrics",
    "observable_only",
    "case_ids",
}
REQUIRED_TRIAL_FIELDS = {
    "schema_version",
    "suite_id",
    "evidence_kind",
    "baseline_representation",
    "candidate_representation",
    "runtime_identity",
    "runs",
}
REQUIRED_REPRESENTATION_FIELDS = {"label", "ref"}
REQUIRED_RUNTIME_IDENTITY = {
    "model_id",
    "model_version",
    "settings_fingerprint",
    "toolset_fingerprint",
}
REQUIRED_RUN_FIELDS = {
    "run_id",
    "pair_id",
    "case_id",
    "input_fingerprint",
    "representation",
    "order",
    "transcript_ref",
    "observed",
}
REQUIRED_OBSERVED_FIELDS = {
    "correct_next_action",
    "protected_violations",
    "steps_to_first_useful_action",
    "unnecessary_questions",
    "unnecessary_actions",
    "unnecessary_reference_loads",
    "manual_continue_required",
}
PRIMARY_METRICS = (
    "protected_violation_count",
    "decision_error",
    "steps_to_first_useful_action",
    "avoidable_events",
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_cases(cases_doc: dict) -> tuple[str, ...]:
    if set(cases_doc) != REQUIRED_CASE_CONTRACT_FIELDS:
        raise ValueError(
            f"model-trial case contract fields must be exactly {sorted(REQUIRED_CASE_CONTRACT_FIELDS)}"
        )
    if cases_doc["schema_version"] != 1:
        raise ValueError("unsupported model-trial case schema_version")
    if cases_doc["suite_id"] != "lossless-runtime-representation-v1":
        raise ValueError("unexpected model-trial suite_id")
    if cases_doc["baseline_ref"] != PROGRAM_BASELINE_REF:
        raise ValueError("model-trial baseline must remain pinned to v1.2.2 program baseline")
    if cases_doc["semantic_case_contract"] != SEMANTIC_CASE_CONTRACT:
        raise ValueError("model-trial semantic case contract must remain canonical Phase 7 runtime contract")
    if cases_doc["evidence_kind"] != "actual-model-runtime-ab":
        raise ValueError("model-trial case contract must require actual-model-runtime-ab evidence")
    if cases_doc["observable_only"] is not True:
        raise ValueError("model-trial contract must remain observable-only")
    minimum = cases_doc["minimum_pairs_per_case"]
    if not isinstance(minimum, int) or isinstance(minimum, bool) or minimum < 1:
        raise ValueError("minimum_pairs_per_case must be a positive integer")
    alpha = cases_doc["sign_test_alpha"]
    if not isinstance(alpha, (int, float)) or isinstance(alpha, bool) or not (0 < alpha <= 0.5):
        raise ValueError("sign_test_alpha must be in (0, 0.5]")
    if tuple(cases_doc["primary_metrics"]) != PRIMARY_METRICS:
        raise ValueError("primary_metrics changed from the observable selection contract")

    case_ids = cases_doc["case_ids"]
    if not isinstance(case_ids, list) or not case_ids:
        raise ValueError("model-trial case_ids must be a non-empty list")
    if any(not isinstance(case_id, str) or not case_id for case_id in case_ids):
        raise ValueError("every model-trial case_id must be a non-empty string")
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("duplicate model-trial case_id")
    return tuple(case_ids)


def _nonnegative_int(value, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{field} must be a non-negative integer")
    return value


def validate_observed(observed: dict, run_id: str) -> None:
    if set(observed) != REQUIRED_OBSERVED_FIELDS:
        raise ValueError(
            f"run {run_id} observed fields must be exactly {sorted(REQUIRED_OBSERVED_FIELDS)}"
        )
    if not isinstance(observed["correct_next_action"], bool):
        raise ValueError(f"run {run_id} correct_next_action must be boolean")
    violations = observed["protected_violations"]
    if not isinstance(violations, list) or any(
        not isinstance(item, str) or not item.strip() for item in violations
    ):
        raise ValueError(f"run {run_id} protected_violations must be a list of non-empty strings")
    _nonnegative_int(observed["steps_to_first_useful_action"], "steps_to_first_useful_action")
    _nonnegative_int(observed["unnecessary_questions"], "unnecessary_questions")
    _nonnegative_int(observed["unnecessary_actions"], "unnecessary_actions")
    _nonnegative_int(observed["unnecessary_reference_loads"], "unnecessary_reference_loads")
    if not isinstance(observed["manual_continue_required"], bool):
        raise ValueError(f"run {run_id} manual_continue_required must be boolean")


def run_metrics(run: dict) -> dict[str, int]:
    observed = run["observed"]
    return {
        "protected_violation_count": len(observed["protected_violations"]),
        "decision_error": 0 if observed["correct_next_action"] else 1,
        "steps_to_first_useful_action": observed["steps_to_first_useful_action"],
        "avoidable_events": (
            observed["unnecessary_questions"]
            + observed["unnecessary_actions"]
            + observed["unnecessary_reference_loads"]
            + int(observed["manual_continue_required"])
        ),
    }


def one_sided_sign_test(differences: list[int]) -> dict:
    """Exact H0 p=0.5 sign test where positive means candidate is better."""
    positive = sum(1 for value in differences if value > 0)
    negative = sum(1 for value in differences if value < 0)
    non_ties = positive + negative
    if non_ties == 0:
        p_value = 1.0
    else:
        p_value = (
            sum(math.comb(non_ties, k) for k in range(positive, non_ties + 1))
            / (2 ** non_ties)
        )
    return {
        "positive": positive,
        "negative": negative,
        "ties": len(differences) - non_ties,
        "non_ties": non_ties,
        "p_value": p_value,
    }


def evaluate(cases_doc: dict, trials_doc: dict) -> dict:
    case_ids = validate_cases(cases_doc)
    case_id_set = set(case_ids)
    if set(trials_doc) != REQUIRED_TRIAL_FIELDS:
        raise ValueError(
            f"model-trial result fields must be exactly {sorted(REQUIRED_TRIAL_FIELDS)}"
        )
    if trials_doc["schema_version"] != 1:
        raise ValueError("unsupported model-trial result schema_version")
    if trials_doc["suite_id"] != cases_doc["suite_id"]:
        raise ValueError("trial suite_id does not match case contract")
    if trials_doc["evidence_kind"] != "actual-model-runtime-ab":
        raise ValueError("trial evidence_kind must be actual-model-runtime-ab")

    baseline = trials_doc["baseline_representation"]
    candidate = trials_doc["candidate_representation"]
    if not isinstance(baseline, dict) or set(baseline) != REQUIRED_REPRESENTATION_FIELDS:
        raise ValueError("baseline_representation must contain exactly label and ref")
    if not isinstance(candidate, dict) or set(candidate) != REQUIRED_REPRESENTATION_FIELDS:
        raise ValueError("candidate_representation must contain exactly label and ref")
    baseline_ref = baseline["ref"]
    candidate_ref = candidate["ref"]
    if baseline_ref != cases_doc["baseline_ref"] or baseline_ref != PROGRAM_BASELINE_REF:
        raise ValueError("trial baseline representation does not match immutable program baseline")
    if not FULL_SHA_RE.fullmatch(candidate_ref) or candidate_ref == baseline_ref:
        raise ValueError("candidate representation must be a distinct exact full commit SHA")
    if not isinstance(baseline["label"], str) or not baseline["label"].strip():
        raise ValueError("baseline representation requires a non-empty label")
    if not isinstance(candidate["label"], str) or not candidate["label"].strip():
        raise ValueError("candidate representation requires a non-empty label")

    runtime_identity = trials_doc["runtime_identity"]
    if not isinstance(runtime_identity, dict) or set(runtime_identity) != REQUIRED_RUNTIME_IDENTITY:
        raise ValueError(
            f"runtime_identity fields must be exactly {sorted(REQUIRED_RUNTIME_IDENTITY)}"
        )
    if any(not isinstance(value, str) or not value.strip() for value in runtime_identity.values()):
        raise ValueError("runtime_identity values must be non-empty strings")

    runs = trials_doc["runs"]
    if not isinstance(runs, list) or not runs:
        raise ValueError("model-trial results require runs")

    pair_rows: dict[str, list[dict]] = defaultdict(list)
    seen_run_ids: set[str] = set()
    seen_transcript_refs: set[str] = set()
    for row in runs:
        if not isinstance(row, dict) or set(row) != REQUIRED_RUN_FIELDS:
            raise ValueError(
                f"every trial run must contain exactly {sorted(REQUIRED_RUN_FIELDS)}"
            )
        run_id = row["run_id"]
        if not isinstance(run_id, str) or not run_id:
            raise ValueError("every trial run requires a non-empty run_id")
        if run_id in seen_run_ids:
            raise ValueError(f"duplicate trial run_id: {run_id}")
        seen_run_ids.add(run_id)
        pair_id = row["pair_id"]
        case_id = row["case_id"]
        input_fingerprint = row["input_fingerprint"]
        representation = row["representation"]
        order = row["order"]
        transcript_ref = row["transcript_ref"]
        if not isinstance(pair_id, str) or not pair_id:
            raise ValueError(f"run {run_id} requires pair_id")
        if case_id not in case_id_set:
            raise ValueError(f"run {run_id} uses unknown case_id: {case_id}")
        if not isinstance(input_fingerprint, str) or not input_fingerprint.strip():
            raise ValueError(f"run {run_id} requires non-empty input_fingerprint")
        if representation not in {"baseline", "candidate"}:
            raise ValueError(f"run {run_id} representation must be baseline or candidate")
        if order not in {1, 2}:
            raise ValueError(f"run {run_id} order must be 1 or 2")
        if not isinstance(transcript_ref, str) or not transcript_ref.strip():
            raise ValueError(f"run {run_id} requires auditable transcript_ref")
        if transcript_ref in seen_transcript_refs:
            raise ValueError(f"duplicate transcript_ref is not auditable per run: {transcript_ref}")
        seen_transcript_refs.add(transcript_ref)
        observed = row["observed"]
        if not isinstance(observed, dict):
            raise ValueError(f"run {run_id} requires observed object")
        validate_observed(observed, run_id)
        pair_rows[pair_id].append(row)

    pairs: list[tuple[dict, dict]] = []
    pairs_by_case: dict[str, list[tuple[dict, dict]]] = defaultdict(list)
    baseline_first_by_case: dict[str, int] = defaultdict(int)
    candidate_first_by_case: dict[str, int] = defaultdict(int)
    for pair_id, rows in sorted(pair_rows.items()):
        if len(rows) != 2:
            raise ValueError(f"pair {pair_id} must contain exactly two runs")
        if {row["representation"] for row in rows} != {"baseline", "candidate"}:
            raise ValueError(f"pair {pair_id} must contain one baseline and one candidate run")
        if {row["order"] for row in rows} != {1, 2}:
            raise ValueError(f"pair {pair_id} must use complementary order 1/2")
        if len({row["case_id"] for row in rows}) != 1:
            raise ValueError(f"pair {pair_id} must use one case_id")
        if len({row["input_fingerprint"] for row in rows}) != 1:
            raise ValueError(f"pair {pair_id} baseline/candidate inputs do not match")
        by_rep = {row["representation"]: row for row in rows}
        baseline_row = by_rep["baseline"]
        candidate_row = by_rep["candidate"]
        case_id = baseline_row["case_id"]
        pairs.append((baseline_row, candidate_row))
        pairs_by_case[case_id].append((baseline_row, candidate_row))
        if baseline_row["order"] == 1:
            baseline_first_by_case[case_id] += 1
        else:
            candidate_first_by_case[case_id] += 1

    errors: list[str] = []
    minimum = cases_doc["minimum_pairs_per_case"]
    for case_id in case_ids:
        count = len(pairs_by_case[case_id])
        if count < minimum:
            errors.append(f"case {case_id} has {count} pairs; requires at least {minimum}")
        if count:
            imbalance = abs(
                baseline_first_by_case[case_id] - candidate_first_by_case[case_id]
            )
            if imbalance > 1:
                errors.append(
                    f"case {case_id} has materially unbalanced run order: "
                    f"baseline-first={baseline_first_by_case[case_id]} "
                    f"candidate-first={candidate_first_by_case[case_id]}"
                )

    totals = {
        "baseline": {metric: 0 for metric in PRIMARY_METRICS},
        "candidate": {metric: 0 for metric in PRIMARY_METRICS},
    }
    per_case = {}
    differences = {metric: [] for metric in PRIMARY_METRICS}
    for case_id in case_ids:
        case_pairs = pairs_by_case[case_id]
        case_totals = {
            "baseline": {metric: 0 for metric in PRIMARY_METRICS},
            "candidate": {metric: 0 for metric in PRIMARY_METRICS},
        }
        for baseline_row, candidate_row in case_pairs:
            base_metrics = run_metrics(baseline_row)
            cand_metrics = run_metrics(candidate_row)
            for metric in PRIMARY_METRICS:
                case_totals["baseline"][metric] += base_metrics[metric]
                case_totals["candidate"][metric] += cand_metrics[metric]
                totals["baseline"][metric] += base_metrics[metric]
                totals["candidate"][metric] += cand_metrics[metric]
                differences[metric].append(base_metrics[metric] - cand_metrics[metric])
        per_case[case_id] = case_totals

    if totals["candidate"]["protected_violation_count"] != 0:
        errors.append("candidate has protected-behavior violations")

    for case_id, case_totals in per_case.items():
        for metric in PRIMARY_METRICS:
            if case_totals["candidate"][metric] > case_totals["baseline"][metric]:
                errors.append(
                    f"candidate worsens {metric} in case {case_id}: "
                    f"baseline={case_totals['baseline'][metric]} "
                    f"candidate={case_totals['candidate'][metric]}"
                )

    sign_tests = {
        metric: one_sided_sign_test(differences[metric]) for metric in PRIMARY_METRICS
    }
    alpha = cases_doc["sign_test_alpha"]
    improved_metrics = [
        metric
        for metric in PRIMARY_METRICS
        if totals["candidate"][metric] < totals["baseline"][metric]
        and sign_tests[metric]["p_value"] <= alpha
    ]
    if not improved_metrics:
        errors.append(
            "candidate has no material paired observable improvement at configured sign-test alpha"
        )

    return {
        "ok": not errors,
        "acceptance_errors": errors,
        "suite_id": cases_doc["suite_id"],
        "semantic_case_contract": cases_doc["semantic_case_contract"],
        "evidence_kind": trials_doc["evidence_kind"],
        "baseline_ref": baseline_ref,
        "candidate_ref": candidate_ref,
        "runtime_identity": runtime_identity,
        "pair_count": len(pairs),
        "pairs_per_case": {case_id: len(pairs_by_case[case_id]) for case_id in case_ids},
        "totals": totals,
        "per_case": per_case,
        "sign_tests": sign_tests,
        "improved_metrics": improved_metrics,
        "proof_boundary": (
            "scores supplied observable paired records only; semantic case meaning remains owned by "
            "the canonical Phase 7 runtime-optimization scenario contract; transcript authenticity, "
            "provider bias, cross-model generalization, and semantic completeness still require review"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cases",
        type=Path,
        default=Path("benchmarks/phase7/model-trial-cases.json"),
    )
    parser.add_argument("--trials", type=Path, required=True)
    args = parser.parse_args()
    result = evaluate(load(args.cases), load(args.trials))
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
