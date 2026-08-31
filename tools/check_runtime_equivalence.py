#!/usr/bin/env python3
"""Compare mechanically checkable runtime semantics with an immutable baseline.

This checker intentionally validates only objective representation invariants. It does
not claim prose, engineering judgment, or model-performance equivalence; those remain
benchmark/review responsibilities.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

RULE_ROW_RE = re.compile(r"^`([A-Z][A-Z0-9-]+)`$")
GOAL_RE = re.compile(r"\bG\d{2}\b")
STATE_RE = re.compile(
    r"\b(TaskState|WorkerStatus|WriteState|DeliveryState|MasterBoundary)\.([A-Z][A-Z0-9_]*)\b"
)
EVAL_RE = re.compile(r"^###\s+([A-Z]{1,3})\.\s+", re.MULTILINE)
DIRECT_REF_RE = re.compile(r"\((references/[A-Za-z0-9._/-]+\.md)\)")
FULL_SHA_RE = re.compile(r"[0-9a-f]{40}")
TEXT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json"}


def run_git(repo: Path, *args: str) -> str:
    try:
        return subprocess.run(
            ["git", *args],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ValueError(f"git {' '.join(args)} failed") from exc


def git_text(repo: Path, ref: str, path: str) -> str:
    return run_git(repo, "show", f"{ref}:{path}")


def git_skill_texts(repo: Path, ref: str) -> dict[str, str]:
    paths = run_git(repo, "ls-tree", "-r", "--name-only", ref, "skill").splitlines()
    result: dict[str, str] = {}
    for path in paths:
        if Path(path).suffix in TEXT_SUFFIXES:
            result[path] = git_text(repo, ref, path)
    return result


def filesystem_skill_texts(repo: Path) -> dict[str, str]:
    root = repo / "skill"
    if not root.is_dir():
        raise ValueError("candidate skill/ directory is missing")
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            result[path.relative_to(repo).as_posix()] = path.read_text(encoding="utf-8")
    return result


def parse_rule_map(text: str) -> dict[str, str]:
    owners: dict[str, str] = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        match = RULE_ROW_RE.fullmatch(cells[0])
        if not match:
            continue
        rule_id = match.group(1)
        if rule_id in owners:
            raise ValueError(f"duplicate canonical Rule row: {rule_id}")
        owners[rule_id] = " ".join(cells[2].split())
    if not owners:
        raise ValueError("no canonical Rule rows found")
    return owners


def parse_goals(*texts: str) -> list[str]:
    return sorted({goal for text in texts for goal in GOAL_RE.findall(text)})


def parse_states(texts: dict[str, str], namespaces: list[str]) -> dict[str, list[str]]:
    observed = {namespace: set() for namespace in namespaces}
    for text in texts.values():
        for namespace, token in STATE_RE.findall(text):
            if namespace in observed:
                observed[namespace].add(token)
    missing_namespaces = [namespace for namespace, tokens in observed.items() if not tokens]
    if missing_namespaces:
        raise ValueError(f"state namespaces have no observed tokens: {missing_namespaces}")
    return {namespace: sorted(tokens) for namespace, tokens in observed.items()}


def parse_direct_refs(skill_text: str) -> list[str]:
    return sorted({f"skill/{path}" for path in DIRECT_REF_RE.findall(skill_text)})


def parse_eval_ids(text: str) -> list[str]:
    ids = EVAL_RE.findall(text)
    if len(ids) != len(set(ids)):
        duplicates = sorted({item for item in ids if ids.count(item) > 1})
        raise ValueError(f"duplicate evaluation scenario IDs: {duplicates}")
    return sorted(ids)


def predicate_presence(
    read_text,
    predicate_owners: dict[str, str],
) -> dict[str, bool]:
    result: dict[str, bool] = {}
    for predicate, path in predicate_owners.items():
        text = read_text(path)
        result[predicate] = bool(re.search(rf"\b{re.escape(predicate)}\s*\(", text))
    return result


def build_inventory(
    *,
    rule_map: str,
    goal_map: str,
    project_spec: str,
    skill_entrypoint: str,
    eval_scenarios: str,
    skill_texts: dict[str, str],
    namespaces: list[str],
    predicate_owners: dict[str, str],
    read_text,
) -> dict:
    return {
        "rule_owners": parse_rule_map(rule_map),
        "goals": parse_goals(goal_map, project_spec),
        "states": parse_states(skill_texts, namespaces),
        "direct_refs": parse_direct_refs(skill_entrypoint),
        "eval_ids": parse_eval_ids(eval_scenarios),
        "predicates_present": predicate_presence(read_text, predicate_owners),
    }


def compare_inventories(baseline: dict, candidate: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    notes: list[str] = []

    baseline_rules = baseline["rule_owners"]
    candidate_rules = candidate["rule_owners"]
    missing_rules = sorted(set(baseline_rules) - set(candidate_rules))
    added_rules = sorted(set(candidate_rules) - set(baseline_rules))
    if missing_rules:
        errors.append(f"canonical Rule IDs removed: {missing_rules}")
    if added_rules:
        errors.append(f"canonical Rule IDs added in representation-only program: {added_rules}")
    owner_changes = {
        rule: {"baseline": baseline_rules[rule], "candidate": candidate_rules[rule]}
        for rule in sorted(set(baseline_rules) & set(candidate_rules))
        if baseline_rules[rule] != candidate_rules[rule]
    }
    if owner_changes:
        errors.append(f"canonical Rule owner changed: {owner_changes}")

    if baseline["goals"] != candidate["goals"]:
        errors.append(
            f"canonical Goal set changed: baseline={baseline['goals']} candidate={candidate['goals']}"
        )

    for namespace, baseline_tokens in baseline["states"].items():
        candidate_tokens = candidate["states"].get(namespace, [])
        if baseline_tokens != candidate_tokens:
            errors.append(
                f"{namespace} token set changed: baseline={baseline_tokens} candidate={candidate_tokens}"
            )

    baseline_refs = set(baseline["direct_refs"])
    candidate_refs = set(candidate["direct_refs"])
    removed_refs = sorted(baseline_refs - candidate_refs)
    added_refs = sorted(candidate_refs - baseline_refs)
    if removed_refs:
        errors.append(f"baseline direct runtime references are no longer routed from SKILL.md: {removed_refs}")
    if added_refs:
        notes.append(f"candidate adds direct runtime references; review activation cost: {added_refs}")

    baseline_evals = set(baseline["eval_ids"])
    candidate_evals = set(candidate["eval_ids"])
    missing_evals = sorted(baseline_evals - candidate_evals)
    added_evals = sorted(candidate_evals - baseline_evals)
    if missing_evals:
        errors.append(f"baseline evaluation scenarios removed: {missing_evals}")
    if added_evals:
        notes.append(f"candidate adds evaluation scenarios: {added_evals}")

    for predicate, present in baseline["predicates_present"].items():
        if not present:
            errors.append(f"baseline predicate is not discoverable in configured owner: {predicate}")
        if not candidate["predicates_present"].get(predicate, False):
            errors.append(f"candidate predicate is not discoverable in configured owner: {predicate}")

    return errors, notes


def validate_config(config: dict) -> None:
    if config.get("schema_version") != 1:
        raise ValueError("unsupported runtime optimization baseline schema_version")
    baseline_ref = config.get("baseline_ref", "")
    if not FULL_SHA_RE.fullmatch(baseline_ref):
        raise ValueError("baseline_ref must be an immutable full commit SHA")
    if not re.fullmatch(r"\d+\.\d+\.\d+", config.get("baseline_version", "")):
        raise ValueError("baseline_version must use x.y.z syntax")
    required_surfaces = {
        "rule_map", "goal_map", "project_spec", "skill_entrypoint", "eval_scenarios"
    }
    if set(config.get("surfaces", {})) != required_surfaces:
        raise ValueError("baseline surfaces must contain exactly the required semantic surface keys")
    namespaces = config.get("state_namespaces")
    if namespaces != ["TaskState", "WorkerStatus", "WriteState", "DeliveryState", "MasterBoundary"]:
        raise ValueError("state_namespaces must preserve the canonical lifecycle namespace set/order")
    predicates = config.get("canonical_predicates", {})
    if set(predicates) != {"CAN_EXECUTE", "MASTER_STOP", "REVIEW_VALID", "DELIVERY_PROVEN"}:
        raise ValueError("canonical_predicates must preserve the configured decision-owner set")


def check_repository(repo: Path, config: dict) -> dict:
    repo = repo.resolve()
    validate_config(config)
    baseline_ref = config["baseline_ref"]
    resolved = run_git(repo, "rev-parse", f"{baseline_ref}^{{commit}}").strip()
    if resolved != baseline_ref:
        raise ValueError(f"baseline_ref resolved unexpectedly: {resolved}")
    version = git_text(repo, baseline_ref, "VERSION").strip()
    if version != config["baseline_version"]:
        raise ValueError(
            f"baseline version mismatch: config={config['baseline_version']} git={version}"
        )

    # The candidate must descend from the immutable comparison baseline. This does not
    # require current main to remain at the baseline SHA.
    try:
        run_git(repo, "merge-base", "--is-ancestor", baseline_ref, "HEAD")
    except ValueError as exc:
        raise ValueError("candidate HEAD does not descend from the immutable baseline") from exc

    surfaces = config["surfaces"]
    baseline_read = lambda path: git_text(repo, baseline_ref, path)
    candidate_read = lambda path: (repo / path).read_text(encoding="utf-8")

    baseline = build_inventory(
        rule_map=baseline_read(surfaces["rule_map"]),
        goal_map=baseline_read(surfaces["goal_map"]),
        project_spec=baseline_read(surfaces["project_spec"]),
        skill_entrypoint=baseline_read(surfaces["skill_entrypoint"]),
        eval_scenarios=baseline_read(surfaces["eval_scenarios"]),
        skill_texts=git_skill_texts(repo, baseline_ref),
        namespaces=config["state_namespaces"],
        predicate_owners=config["canonical_predicates"],
        read_text=baseline_read,
    )
    candidate = build_inventory(
        rule_map=candidate_read(surfaces["rule_map"]),
        goal_map=candidate_read(surfaces["goal_map"]),
        project_spec=candidate_read(surfaces["project_spec"]),
        skill_entrypoint=candidate_read(surfaces["skill_entrypoint"]),
        eval_scenarios=candidate_read(surfaces["eval_scenarios"]),
        skill_texts=filesystem_skill_texts(repo),
        namespaces=config["state_namespaces"],
        predicate_owners=config["canonical_predicates"],
        read_text=candidate_read,
    )
    errors, notes = compare_inventories(baseline, candidate)
    return {
        "ok": not errors,
        "baseline_ref": baseline_ref,
        "baseline_version": config["baseline_version"],
        "errors": errors,
        "notes": notes,
        "counts": {
            "rules": len(candidate["rule_owners"]),
            "goals": len(candidate["goals"]),
            "direct_refs": len(candidate["direct_refs"]),
            "eval_scenarios": len(candidate["eval_ids"]),
            "state_tokens": sum(len(tokens) for tokens in candidate["states"].values()),
        },
        "baseline_inventory": baseline,
        "candidate_inventory": candidate,
        "proof_boundary": (
            "mechanical representation invariants only; prose/judgment equivalence and actual "
            "LLM performance require benchmark plus review evidence"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("benchmarks/phase7/runtime-optimization-baseline.json"),
    )
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    config_path = args.config if args.config.is_absolute() else repo / args.config
    config = json.loads(config_path.read_text(encoding="utf-8"))
    result = check_repository(repo, config)
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
