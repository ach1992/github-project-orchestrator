#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess
from collections import Counter
from pathlib import Path

PROTECTED_VIOLATION_EVENTS = {"unsafe_shortcut", "hidden_human_work", "duplicate_mutation"}

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def index_by(items, key):
    result = {}
    for item in items:
        value = item[key]
        if value in result:
            raise ValueError(f"duplicate {key}: {value}")
        result[value] = item
    return result

def analyze(scenario, trace):
    if trace.get("source_basis") is None or not trace.get("source_basis"):
        raise ValueError(f"trace {trace.get('scenario_id')} is missing source_basis")
    events = trace["events"]
    types = [e["type"] for e in events]
    missing = []
    counts = Counter(types)
    required_counts = Counter(scenario["required_events"])
    for event_type, needed in required_counts.items():
        if counts[event_type] < needed:
            missing.append(f"missing event {event_type} x{needed-counts[event_type]}")
    first_action = next((i for i, e in enumerate(events) if e["type"] == "useful_action"), None)
    if first_action is None:
        missing.append("no useful_action")
        first_action = len(events)
    stop_events = [e for e in events if e["type"] == "stop"]
    wrong_stop = len(stop_events) != 1 or stop_events[0].get("boundary") != scenario["expected_stop"]
    confirmations = counts["human_confirmation"]
    unnecessary_confirmations = max(0, confirmations - scenario["required_confirmations"])
    missing_confirmations = max(0, scenario["required_confirmations"] - confirmations)
    dispatches = counts["worker_dispatch"]
    worker_churn = max(0, dispatches - scenario["required_worker_dispatches"])
    missing_dispatches = max(0, scenario["required_worker_dispatches"] - dispatches)
    artifacts = counts["artifact_create"]
    unnecessary_artifacts = max(0, artifacts - scenario["required_artifacts"])
    missing_artifacts = max(0, scenario["required_artifacts"] - artifacts)
    discovers = [e.get("target") for e in events if e["type"] == "discover"]
    repeated_discovery = sum(count - 1 for count in Counter(discovers).values() if count > 1)
    context_domains = len({e.get("target") for e in events if e["type"] == "load_domain"})
    violations = [e["type"] for e in events if e["type"] in PROTECTED_VIOLATION_EVENTS]
    expected_coordination = scenario.get("expected_coordination")
    if expected_coordination is not None:
        observed = [e.get("value") for e in events if e["type"] == "coordination"]
        if observed != [expected_coordination]:
            violations.append(f"coordination_mismatch:{observed}->{expected_coordination}")
    reviewed = set()
    for e in events:
        if e["type"] == "fresh_review":
            reviewed.add(e.get("candidate"))
        elif e["type"] == "candidate_change":
            reviewed.discard(e.get("candidate"))
        elif e["type"] == "integration_verified" and e.get("candidate") not in reviewed:
            violations.append("stale_integration")
    if scenario["delivery_required"] and counts["delivery_verified"] < 1:
        violations.append("missing_delivery_verification")
    if missing_confirmations:
        violations.append("missing_required_confirmation")
    if missing_dispatches:
        violations.append("missing_required_worker_dispatch")
    if missing_artifacts:
        violations.append("missing_required_artifact")
    if wrong_stop:
        violations.append("wrong_stop")
    violations.extend(missing)
    return {
        "scenario_id": scenario["id"],
        "protected_violations": violations,
        "steps_to_first_useful_action": first_action,
        "unnecessary_confirmations": unnecessary_confirmations,
        "unnecessary_artifacts": unnecessary_artifacts,
        "worker_churn": worker_churn,
        "repeated_discovery": repeated_discovery,
        "context_domains": context_domains,
        "discovery_steps": counts["discover"],
    }

def entrypoint_metrics(repo: Path, baseline_ref: str):
    current = (repo / "skill" / "SKILL.md").read_text(encoding="utf-8")
    try:
        baseline = subprocess.run(
            ["git", "show", f"{baseline_ref}:skill/SKILL.md"],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    def metrics(text):
        return {
            "bytes": len(text.encode("utf-8")),
            "nonblank_lines": sum(1 for line in text.splitlines() if line.strip()),
            "words": len(text.split()),
        }
    return {"baseline": metrics(baseline), "current": metrics(current)}

def evaluate(scenarios_doc, baseline_doc, current_doc):
    if scenarios_doc.get("schema_version") != 1 or baseline_doc.get("schema_version") != 1 or current_doc.get("schema_version") != 1:
        raise ValueError("unsupported benchmark schema_version")
    if baseline_doc.get("version") != "v1.0.0":
        raise ValueError("baseline benchmark must be pinned to v1.0.0")
    if baseline_doc.get("evidence_kind") != "source-grounded-policy-simulation" or current_doc.get("evidence_kind") != "source-grounded-policy-simulation":
        raise ValueError("benchmark traces must declare source-grounded-policy-simulation evidence kind")
    scenarios = index_by(scenarios_doc["scenarios"], "id")
    baseline = index_by(baseline_doc["traces"], "scenario_id")
    current = index_by(current_doc["traces"], "scenario_id")
    if set(baseline) != set(scenarios) or set(current) != set(scenarios):
        raise ValueError("trace/scenario ID sets must match exactly")
    all_goals = {f"G{i:02d}" for i in range(1,17)}
    covered_goals = {goal for scenario in scenarios.values() for goal in scenario["goal_ids"]}
    missing_goals = sorted(all_goals - covered_goals)
    if missing_goals:
        raise ValueError(f"operational scenarios do not cover canonical goals: {missing_goals}")
    baseline_rows = [analyze(scenarios[sid], baseline[sid]) for sid in scenarios]
    current_rows = [analyze(scenarios[sid], current[sid]) for sid in scenarios]
    baseline_by = index_by(baseline_rows, "scenario_id")
    current_by = index_by(current_rows, "scenario_id")
    acceptance_errors = []
    for sid in scenarios:
        if baseline_by[sid]["protected_violations"]:
            acceptance_errors.append(f"baseline trace invalid for {sid}: {baseline_by[sid]['protected_violations']}")
        if current_by[sid]["protected_violations"]:
            acceptance_errors.append(f"current trace invalid for {sid}: {current_by[sid]['protected_violations']}")
    friction_fields = [
        "steps_to_first_useful_action", "unnecessary_confirmations", "unnecessary_artifacts",
        "worker_churn", "repeated_discovery", "context_domains", "discovery_steps"
    ]
    totals = {}
    for label, rows in (("baseline", baseline_rows), ("current", current_rows)):
        totals[label] = {field: sum(row[field] for row in rows) for field in friction_fields}
    for field in ("unnecessary_confirmations", "unnecessary_artifacts", "worker_churn", "repeated_discovery"):
        if totals["current"][field] > totals["baseline"][field]:
            acceptance_errors.append(f"current worsened {field}")
    if totals["current"]["steps_to_first_useful_action"] >= totals["baseline"]["steps_to_first_useful_action"]:
        acceptance_errors.append("current does not reduce aggregate steps to first useful action")
    if totals["current"]["context_domains"] > totals["baseline"]["context_domains"]:
        acceptance_errors.append("current increases aggregate context-domain activation")
    if totals["current"]["discovery_steps"] >= totals["baseline"]["discovery_steps"]:
        acceptance_errors.append("current does not reduce aggregate discovery/recovery steps")
    return {
        "ok": not acceptance_errors,
        "acceptance_errors": acceptance_errors,
        "baseline": baseline_rows,
        "current": current_rows,
        "totals": totals,
        "goal_coverage": sorted(covered_goals),
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--scenarios", type=Path, required=True)
    p.add_argument("--baseline", type=Path, required=True)
    p.add_argument("--current", type=Path, required=True)
    p.add_argument("--repo-root", type=Path)
    p.add_argument("--baseline-ref", default="v1.0.0")
    args = p.parse_args()
    result = evaluate(load(args.scenarios), load(args.baseline), load(args.current))
    if args.repo_root:
        result["entrypoint_metrics"] = entrypoint_metrics(args.repo_root.resolve(), args.baseline_ref)
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["ok"] else 1)
if __name__ == "__main__":
    main()
