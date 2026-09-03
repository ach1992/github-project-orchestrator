#!/usr/bin/env python3
"""Adversarial fixtures for historical v1.2.2 and current v1.3.2 representation controls."""
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
if result["current_eval_control"]["ref"] != eq.CURRENT_EVAL_CONTROL_REF:
    raise AssertionError("current eval control ref mismatch")
if "DK" not in result["current_eval_control"]["eval_ids"]:
    raise AssertionError("v1.3.2 current eval control must include DK")
if "DK" in result["baseline_inventory"]["eval_ids"]:
    raise AssertionError("historical v1.2.2 baseline unexpectedly includes DK")
print("PASS immutable-v1.3.2-current-eval-control")

bad_config = copy.deepcopy(config)
bad_config["schema_version"] = 1
try:
    eq.validate_config(bad_config)
except ValueError as exc:
    if "unsupported runtime optimization baseline schema_version" not in str(exc):
        raise
    print("PASS baseline-config-schema-v1-rejected")
else:
    raise AssertionError("baseline-config-schema-v1: unexpectedly passed")

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

bad_config = copy.deepcopy(config)
bad_config["current_eval_control"]["ref"] = "0" * 40
try:
    eq.validate_config(bad_config)
except ValueError as exc:
    if "current eval control ref must remain pinned" not in str(exc):
        raise
    print("PASS current-eval-control-ref-drift-rejected")
else:
    raise AssertionError("current-eval-control-ref-drift: unexpectedly passed")

bad_config = copy.deepcopy(config)
bad_config["current_eval_control"]["version"] = "9.9.9"
try:
    eq.validate_config(bad_config)
except ValueError as exc:
    if "current eval control version must remain pinned" not in str(exc):
        raise
    print("PASS current-eval-control-version-drift-rejected")
else:
    raise AssertionError("current-eval-control-version-drift: unexpectedly passed")

control_ids = result["current_eval_control"]["eval_ids"]
without_dk = [value for value in control_ids if value != "DK"]
current_errors, _current_notes = eq.compare_current_eval_control(control_ids, without_dk)
if not any("current v1.3.2 evaluation scenarios removed: ['DK']" in error for error in current_errors):
    raise AssertionError(f"current eval control did not reject DK loss: {current_errors}")
print("PASS current-v1.3.2-dk-loss-rejected")

current_eval_text = eq.git_text(
    ROOT, eq.CURRENT_EVAL_CONTROL_REF, config["surfaces"]["eval_scenarios"]
)
dk_start = current_eval_text.index("### DK. ")
guard_start = current_eval_text.index("\n## 4. Regression guard", dk_start)
without_real_dk = current_eval_text[:dk_start] + current_eval_text[guard_start:]
for hidden_name, hidden_dk in (
    ("commented", "<!--\n### DK. Hidden fake\n-->\n"),
    ("fenced", "```text\n### DK. Hidden fake\n```\n"),
):
    hostile_text = without_real_dk.replace(
        "## 4. Regression guard", hidden_dk + "\n## 4. Regression guard", 1
    )
    hostile_ids = eq.parse_eval_ids(hostile_text)
    if "DK" in hostile_ids:
        raise AssertionError(f"{hidden_name} hidden DK heading incorrectly counted")
    hostile_errors, _hostile_notes = eq.compare_current_eval_control(control_ids, hostile_ids)
    expected = "current v1.3.2 evaluation scenarios removed: ['DK']"
    if expected not in hostile_errors:
        raise AssertionError(
            f"{hidden_name} hidden-DK bypass was not rejected: {hostile_errors}"
        )
    print(f"PASS current-v1.3.2-{hidden_name}-dk-bypass-rejected")

def hostile_eval_text(hidden_payload: str) -> str:
    candidate_text = (ROOT / config["surfaces"]["eval_scenarios"]).read_text(encoding="utf-8")
    real_dk_start = candidate_text.index("### DK. ")
    real_guard_start = candidate_text.index("\n## 4. Regression guard", real_dk_start)
    candidate_text = candidate_text[:real_dk_start] + candidate_text[real_guard_start:]

    visible_row = "| representation-only semantic preservation | `DK` |\n"
    if candidate_text.count(visible_row) != 1:
        raise AssertionError("candidate must contain exactly one visible DK supplemental row")
    candidate_text = candidate_text.replace(visible_row, "", 1)
    marker = "This table is navigation only; it defines no runtime policy or scenario semantics.\n\n"
    if candidate_text.count(marker) != 1:
        raise AssertionError("candidate supplemental navigation marker drifted")
    return candidate_text.replace(marker, marker + hidden_payload + "\n", 1)


with tempfile.TemporaryDirectory(prefix="gpo-hidden-eval-e2e-parent-") as parent_name:
    temp_root = Path(parent_name) / "candidate"
    subprocess.run(
        ["git", "worktree", "add", "--quiet", "--detach", str(temp_root), "HEAD"],
        cwd=ROOT,
        check=True,
    )
    try:
        for hidden_name, hidden_payload in (
            (
                "commented",
                "<!--\n### DK. Hidden fake scenario\n"
                "| representation-only semantic preservation | `DK` |\n-->",
            ),
            (
                "fenced-backtick",
                "```text\n### DK. Hidden fake scenario\n"
                "| representation-only semantic preservation | `DK` |\n```",
            ),
            (
                "fenced-tilde",
                "~~~text\n### DK. Hidden fake scenario\n"
                "| representation-only semantic preservation | `DK` |\n~~~",
            ),
            (
                "raw-html-pre",
                "<pre>\n### DK. Hidden fake scenario\n</pre>\n",
            ),
            (
                "raw-html-div",
                "<div>\n### DK. Hidden fake scenario\n</div>\n\n",
            ),
        ):
            eval_path = temp_root / config["surfaces"]["eval_scenarios"]
            eval_path.write_text(hostile_eval_text(hidden_payload), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, "tools/check_runtime_equivalence.py", "--repo-root", "."],
                cwd=temp_root,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            if completed.returncode != 1:
                raise AssertionError(
                    f"{hidden_name} hidden-DK end-to-end bypass unexpectedly returned "
                    f"{completed.returncode}: {completed.stdout} {completed.stderr}"
                )
            payload = json.loads(completed.stdout)
            expected = "current v1.3.2 evaluation scenarios removed: ['DK']"
            if expected not in payload.get("errors", []):
                raise AssertionError(
                    f"{hidden_name} hidden-DK end-to-end error missing: {payload.get('errors')}"
                )
            print(f"PASS current-v1.3.2-{hidden_name}-dk-end-to-end-rejected")
    finally:
        subprocess.run(
            ["git", "worktree", "remove", "--force", str(temp_root)],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

for spaces in range(4):
    indented = current_eval_text.replace(
        "### DK. Structured rewrite preserves independent prose semantics",
        f"{' ' * spaces}### DK. Structured rewrite preserves independent prose semantics",
        1,
    )
    if "DK" not in eq.parse_eval_ids(indented):
        raise AssertionError(f"visible DK heading with {spaces} leading spaces was not counted")
    print(f"PASS current-v1.3.2-visible-dk-indent-{spaces}")

four_space = current_eval_text.replace(
    "### DK. Structured rewrite preserves independent prose semantics",
    "    ### DK. Structured rewrite preserves independent prose semantics",
    1,
)
if "DK" in eq.parse_eval_ids(four_space):
    raise AssertionError("four-space indented DK pseudo-heading was incorrectly counted")
print("PASS current-v1.3.2-four-space-dk-not-counted")

comment_fence_text = "<!--\n```text\ninside comment\n-->\n### DK. Visible after comment\n"
if eq.parse_eval_ids(comment_fence_text) != ["DK"]:
    raise AssertionError("fence opener inside HTML comment suppressed a later visible heading")
print("PASS current-v1.3.2-comment-fence-state-isolated")

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
