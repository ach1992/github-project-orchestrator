#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, subprocess
from collections import Counter
from pathlib import Path

PROTECTED_VIOLATION_EVENTS = {"unsafe_shortcut", "hidden_human_work", "duplicate_mutation"}
FRICTION_FIELDS = [
    "steps_to_first_useful_action", "unnecessary_confirmations", "unnecessary_artifacts",
    "worker_churn", "repeated_discovery", "context_domains", "discovery_steps"
]
FULL_SHA_RE = re.compile(r"[0-9a-f]{40}")

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
            reviewed.clear()
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

def read_git_text(repo: Path, ref: str, path: str) -> str:
    try:
        return subprocess.run(
            ["git", "show", f"{ref}:{path}"],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ValueError(f"unable to read pinned benchmark source {ref}:{path}") from exc

def validate_source_refs(repo: Path, *trace_docs: dict) -> None:
    for doc in trace_docs:
        expected_ref = doc["version"]
        for trace in doc["traces"]:
            for basis in trace["source_basis"]:
                ref, separator, path = basis.partition(":")
                if not separator or ref != expected_ref or not path:
                    raise ValueError(f"floating or malformed source_basis: {basis}")
                read_git_text(repo, ref, path)

def entrypoint_metrics(repo: Path, baseline_ref: str, current_ref: str):
    baseline = read_git_text(repo, baseline_ref, "skill/SKILL.md")
    current = read_git_text(repo, current_ref, "skill/SKILL.md")
    def metrics(text):
        return {
            "bytes": len(text.encode("utf-8")),
            "nonblank_lines": sum(1 for line in text.splitlines() if line.strip()),
            "words": len(text.split()),
        }
    return {"baseline": metrics(baseline), "current": metrics(current)}

def prepare_rows(scenarios_doc, baseline_doc, current_doc):
    if scenarios_doc.get("schema_version") != 1 or baseline_doc.get("schema_version") != 1 or current_doc.get("schema_version") != 1:
        raise ValueError("unsupported benchmark schema_version")
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
    return scenarios, baseline_rows, current_rows, sorted(covered_goals)

def totals_for(rows):
    return {field: sum(row[field] for row in rows) for field in FRICTION_FIELDS}

def protected_errors(scenarios, baseline_rows, current_rows):
    baseline_by = index_by(baseline_rows, "scenario_id")
    current_by = index_by(current_rows, "scenario_id")
    errors = []
    for sid in scenarios:
        if baseline_by[sid]["protected_violations"]:
            errors.append(f"baseline trace invalid for {sid}: {baseline_by[sid]['protected_violations']}")
        if current_by[sid]["protected_violations"]:
            errors.append(f"current trace invalid for {sid}: {current_by[sid]['protected_violations']}")
    return errors

def validate_trace_set(scenarios_doc, trace_doc):
    """Validate one pinned trace set without claiming an optimization win."""
    version = trace_doc.get("version", "")
    if not FULL_SHA_RE.fullmatch(version):
        raise ValueError("trace set must be pinned to a full commit SHA")
    scenarios, rows, duplicate_rows, covered_goals = prepare_rows(
        scenarios_doc, trace_doc, trace_doc
    )
    errors = protected_errors(scenarios, rows, duplicate_rows)
    return {
        "ok": not errors,
        "acceptance_errors": errors,
        "trace": rows,
        "totals": totals_for(rows),
        "goal_coverage": covered_goals,
        "version": version,
        "evidence_kind": trace_doc["evidence_kind"],
        "optimization_claim_eligible": False,
        "proof_boundary": "source-grounded policy simulation; not model-performance evidence",
    }

def evaluate(scenarios_doc, baseline_doc, current_doc):
    """Historical v1.0.0 -> pinned refactor comparison; behavior kept backward compatible."""
    if baseline_doc.get("version") != "v1.0.0":
        raise ValueError("baseline benchmark must be pinned to v1.0.0")
    current_version = current_doc.get("version", "")
    if not FULL_SHA_RE.fullmatch(current_version):
        raise ValueError("current benchmark must be pinned to a full commit SHA")
    scenarios, baseline_rows, current_rows, covered_goals = prepare_rows(
        scenarios_doc, baseline_doc, current_doc
    )
    acceptance_errors = protected_errors(scenarios, baseline_rows, current_rows)
    totals = {"baseline": totals_for(baseline_rows), "current": totals_for(current_rows)}
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
        "goal_coverage": covered_goals,
    }

def evaluate_candidate_pair(scenarios_doc, baseline_doc, candidate_doc):
    """Compare current source-grounded traces without making a performance claim.

    This lane checks protected behavior and reports structural/friction diagnostics only.
    It intentionally does not require, reward, or certify a synthetic trace reduction.
    Practical optimization claims belong exclusively to paired actual model/runtime trials.
    """
    baseline_version = baseline_doc.get("version", "")
    candidate_version = candidate_doc.get("version", "")
    if not FULL_SHA_RE.fullmatch(baseline_version):
        raise ValueError("candidate-comparison baseline must be pinned to a full commit SHA")
    if not FULL_SHA_RE.fullmatch(candidate_version):
        raise ValueError("candidate benchmark must be pinned to a full commit SHA")
    scenarios, baseline_rows, candidate_rows, covered_goals = prepare_rows(
        scenarios_doc, baseline_doc, candidate_doc
    )
    acceptance_errors = protected_errors(scenarios, baseline_rows, candidate_rows)
    totals = {"baseline": totals_for(baseline_rows), "current": totals_for(candidate_rows)}
    deltas = {
        field: totals["current"][field] - totals["baseline"][field]
        for field in FRICTION_FIELDS
    }
    diagnostic_regressions = [
        field for field, delta in deltas.items() if delta > 0
    ]
    diagnostic_reductions = [
        field for field, delta in deltas.items() if delta < 0
    ]
    return {
        "ok": not acceptance_errors,
        "acceptance_errors": acceptance_errors,
        "baseline": baseline_rows,
        "current": candidate_rows,
        "totals": totals,
        "diagnostic_deltas": deltas,
        "diagnostic_regressions": diagnostic_regressions,
        "diagnostic_reductions": diagnostic_reductions,
        "goal_coverage": covered_goals,
        "evidence_kind": "source-grounded-policy-simulation",
        "optimization_claim_eligible": False,
        "proof_boundary": (
            "protected/source-grounded diagnostic comparison only; actual paired model/runtime "
            "trial evidence is required for any practical-improvement claim"
        ),
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--scenarios", type=Path, required=True)
    p.add_argument("--baseline", type=Path, required=True)
    p.add_argument("--current", type=Path)
    p.add_argument("--repo-root", type=Path)
    p.add_argument("--baseline-ref")
    p.add_argument(
        "--comparison-mode",
        choices=("historical", "candidate", "validate-baseline"),
        default="historical",
    )
    args = p.parse_args()
    scenarios = load(args.scenarios)
    baseline = load(args.baseline)
    current = load(args.current) if args.current else None
    if args.comparison_mode == "historical":
        if current is None:
            p.error("--current is required for historical comparison")
        result = evaluate(scenarios, baseline, current)
    elif args.comparison_mode == "candidate":
        if current is None:
            p.error("--current is required for candidate comparison")
        result = evaluate_candidate_pair(scenarios, baseline, current)
    else:
        result = validate_trace_set(scenarios, baseline)
    if args.repo_root:
        repo = args.repo_root.resolve()
        docs = [baseline] + ([current] if current is not None else [])
        validate_source_refs(repo, *docs)
        baseline_ref = args.baseline_ref or baseline["version"]
        if current is not None:
            result["entrypoint_metrics"] = entrypoint_metrics(
                repo, baseline_ref, current["version"]
            )
        else:
            result["entrypoint_metrics"] = entrypoint_metrics(
                repo, baseline_ref, baseline["version"]
            )
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["ok"] else 1)
if __name__ == "__main__":
    main()
