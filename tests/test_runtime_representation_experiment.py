#!/usr/bin/env python3
"""Validate the Phase B decision-frame prototype without changing canonical skill/."""
from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
BASELINE = "f98e8a242c720931e34aa7c4e8a799090e3d0495"
EXPERIMENT = ROOT / "benchmarks" / "phase7" / "experiments" / "decision-frame-v1" / "experiment.json"
MATERIALIZER = ROOT / "tools" / "materialize_runtime_experiment.py"
EQUIVALENCE = ROOT / "tools" / "check_runtime_equivalence.py"
TRACEABILITY_CONTEXT = (
    "design/RULE-MAP.md",
    "design/GOAL-MAP.md",
    "docs/PROJECT-SPEC.md",
)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def materialize_baseline_traceability_context(output: Path) -> None:
    """Provide the immutable repo-level sources required by normal validate_skill.py."""
    for relative in TRACEABILITY_CONTEXT:
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(
            subprocess.run(
                ["git", "show", f"{BASELINE}:{relative}"],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            ).stdout
        )


materializer = load_module("runtime_experiment_materializer", MATERIALIZER)
eq = load_module("runtime_equivalence", EQUIVALENCE)
experiment = json.loads(EXPERIMENT.read_text(encoding="utf-8"))

with tempfile.TemporaryDirectory(prefix="decision-frame-v1-") as tmp:
    output = Path(tmp)
    metadata = materializer.materialize(ROOT, EXPERIMENT, output)
    if metadata["baseline_ref"] != BASELINE:
        raise AssertionError(metadata)
    candidate_skill = output / "skill"
    candidate_entry = (candidate_skill / "SKILL.md").read_text(encoding="utf-8")
    baseline_entry = subprocess.run(
        ["git", "show", f"{BASELINE}:skill/SKILL.md"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout

    replacement = experiment["replacement"]
    start = replacement["start_heading"]
    end = replacement["end_heading_exclusive"]
    baseline_start = baseline_entry.index(start)
    baseline_end = baseline_entry.index(end)
    candidate_start = candidate_entry.index(start)
    candidate_end = candidate_entry.index(end)
    if baseline_entry[:baseline_start] != candidate_entry[:candidate_start]:
        raise AssertionError("prototype changed content before the isolated Section 1 replacement")
    if baseline_entry[baseline_end:] != candidate_entry[candidate_end:]:
        raise AssertionError("prototype changed content after the isolated Section 1 replacement")
    print("PASS isolated-entrypoint-section-only")

    baseline_paths = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", BASELINE, "skill"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout.splitlines()
    candidate_paths = sorted(
        path.relative_to(output).as_posix()
        for path in candidate_skill.rglob("*")
        if path.is_file()
    )
    if sorted(baseline_paths) != candidate_paths:
        raise AssertionError(
            f"materialized candidate Skill file set drifted: baseline={baseline_paths} candidate={candidate_paths}"
        )
    for relative in baseline_paths:
        if relative == "skill/SKILL.md":
            continue
        baseline_bytes = subprocess.run(
            ["git", "show", f"{BASELINE}:{relative}"],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout
        candidate_bytes = (output / relative).read_bytes()
        if baseline_bytes != candidate_bytes:
            raise AssertionError(f"prototype changed non-entrypoint runtime file: {relative}")
    print("PASS non-entrypoint-runtime-byte-identical")

    baseline_refs = eq.parse_direct_refs(baseline_entry)
    candidate_refs = eq.parse_direct_refs(candidate_entry)
    if baseline_refs != candidate_refs:
        raise AssertionError(
            f"direct runtime routing changed: baseline={baseline_refs} candidate={candidate_refs}"
        )
    print("PASS direct-runtime-routing-identical")

    stable_rows = {
        "`Role` | its actual assignment basis changes | `KEEP` the current value",
        "`ProjectAuthority` | its actual authorization basis changes | `KEEP` the current value",
        "`CoordinationBaseline` | its actual coordination basis changes | `KEEP` the current value",
    }
    for row in stable_rows:
        if row not in candidate_entry:
            raise AssertionError(f"candidate decision frame is missing expected stable-state row: {row}")
    if "not as a persisted project artifact or new lifecycle state" not in candidate_entry:
        raise AssertionError("candidate frame must remain transient/non-persisted")
    print("PASS explicit-transient-keep-frame")

    # validate_skill.py intentionally checks repo-level Rule/Goal/project traceability
    # through skill_dir.parent. The experiment materializer copies only runtime skill/
    # so supply those exact immutable baseline sources solely as validation context.
    materialize_baseline_traceability_context(output)
    subprocess.run(
        [sys.executable, str(ROOT / "tools" / "validate_skill.py"), str(candidate_skill)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    print("PASS materialized-candidate-skill-validation")

bad = copy.deepcopy(experiment)
bad["baseline_ref"] = "0" * 40
with tempfile.TemporaryDirectory(prefix="decision-frame-bad-baseline-") as tmp:
    bad_path = Path(tmp) / "experiment.json"
    bad_path.write_text(json.dumps(bad), encoding="utf-8")
    try:
        materializer.materialize(ROOT, bad_path, Path(tmp) / "out")
    except ValueError as exc:
        if "immutable program baseline" not in str(exc):
            raise
        print("PASS experiment-baseline-drift-rejected")
    else:
        raise AssertionError("experiment baseline drift unexpectedly accepted")

bad = copy.deepcopy(experiment)
bad["semantic_change_allowed"] = True
with tempfile.TemporaryDirectory(prefix="decision-frame-semantic-change-") as tmp:
    bad_path = Path(tmp) / "experiment.json"
    bad_path.write_text(json.dumps(bad), encoding="utf-8")
    try:
        materializer.materialize(ROOT, bad_path, Path(tmp) / "out")
    except ValueError as exc:
        if "must not allow semantic change" not in str(exc):
            raise
        print("PASS semantic-change-experiment-rejected")
    else:
        raise AssertionError("semantic-change experiment unexpectedly accepted")
