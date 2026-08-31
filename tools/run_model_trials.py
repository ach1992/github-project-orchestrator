#!/usr/bin/env python3
"""Run auditable paired model trials for runtime-representation experiments.

The runner is intentionally a thin execution/evidence layer. Semantic case meaning
stays in runtime-optimization-scenarios.json, selection/scoring policy stays in
model-trial-cases.json + score_model_trials.py, and this module never judges
semantic correctness or private reasoning.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Callable

PROGRAM_BASELINE_REF = "f98e8a242c720931e34aa7c4e8a799090e3d0495"
SEMANTIC_CASE_CONTRACT = "benchmarks/phase7/runtime-optimization-scenarios.json"
MODEL_TRIAL_MANIFEST = "benchmarks/phase7/model-trial-cases.json"
DEFAULT_EXPERIMENT = "benchmarks/phase7/experiments/decision-frame-v1/experiment.json"
EVIDENCE_KIND = "actual-model-runtime-ab"
RAW_EVIDENCE_KIND = "actual-model-runtime-ab-raw-v1"
TOOLSET_ID = "runtime-reference-read-v1"
FULL_SHA_RE = re.compile(r"[0-9a-f]{40}")
TRIAL_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")
MAX_HTTP_RESPONSE_BYTES = 2 * 1024 * 1024
SENSITIVE_SETTING_KEY_RE = re.compile(
    r"(?:^|[_-])(api[_-]?key|token|secret|password|authorization|cookie)(?:$|[_-])",
    re.IGNORECASE,
)
RESERVED_MODEL_SETTINGS = {"model", "messages", "tools", "tool_choice", "stream", "n"}


class TransportError(RuntimeError):
    """A provider transport failure that invalidates a scored suite."""


class ProviderSchemaError(RuntimeError):
    """A provider response that cannot be audited under the controlled schema."""


@dataclass(frozen=True)
class RuntimeView:
    label: str
    ref: str
    entrypoint: str
    references: dict[str, str]
    entrypoint_sha256: str


@dataclass(frozen=True)
class RuntimeConfig:
    api_base_url: str
    endpoint_url: str
    model_id: str
    model_version: str
    settings: dict[str, Any]
    instruction_role: str
    timeout_seconds: float
    max_model_turns: int


Transport = Callable[[str, str, dict[str, Any], float], tuple[dict[str, Any], dict[str, Any]]]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fingerprint(value: Any) -> str:
    return "sha256:" + sha256_text(canonical_json(value))


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def repo_path(value: str) -> str:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or ".." in path.parts or str(path) != value:
        raise ValueError(f"repository path must be normalized and relative: {value!r}")
    return value


def git_bytes(repo: Path, *args: str) -> bytes:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ValueError(f"git {' '.join(args)} failed") from exc
    return proc.stdout


def git_text(repo: Path, *args: str) -> str:
    return git_bytes(repo, *args).decode("utf-8")


def validate_candidate_ref(candidate_ref: str) -> None:
    if not FULL_SHA_RE.fullmatch(candidate_ref):
        raise ValueError("candidate-ref must be an exact lowercase 40-character commit SHA")
    if candidate_ref == PROGRAM_BASELINE_REF:
        raise ValueError("candidate-ref must be distinct from the immutable baseline")


def verify_exact_commit(repo: Path, ref: str) -> None:
    if not FULL_SHA_RE.fullmatch(ref):
        raise ValueError(f"exact commit identity required: {ref!r}")
    resolved = git_text(repo, "rev-parse", "--verify", f"{ref}^{{commit}}").strip()
    if resolved != ref:
        raise ValueError(f"commit identity drift: expected {ref}, resolved {resolved}")


def replace_section(baseline: str, start: str, end: str, candidate: str) -> str:
    if baseline.count(start) != 1 or baseline.count(end) != 1:
        raise ValueError("baseline experiment section boundaries are not unique")
    if candidate.count(start) != 1 or not candidate.lstrip().startswith(start):
        raise ValueError("candidate section must begin with the configured start heading")
    if end in candidate:
        raise ValueError("candidate section must not contain the exclusive end heading")
    start_index = baseline.index(start)
    end_index = baseline.index(end)
    if start_index >= end_index:
        raise ValueError("baseline experiment section boundaries are out of order")
    return baseline[:start_index] + candidate.rstrip() + "\n\n" + baseline[end_index:]


def validate_experiment(experiment: dict[str, Any]) -> None:
    if experiment.get("schema_version") != 1:
        raise ValueError("unsupported representation experiment schema_version")
    if experiment.get("baseline_ref") != PROGRAM_BASELINE_REF:
        raise ValueError("experiment baseline drifted from the immutable program baseline")
    if experiment.get("baseline_entrypoint") != "skill/SKILL.md":
        raise ValueError("experiment baseline_entrypoint must remain skill/SKILL.md")
    if experiment.get("semantic_change_allowed") is not False:
        raise ValueError("model trials require a representation-only experiment")
    if experiment.get("canonical_runtime_changed_during_prototype") is not False:
        raise ValueError("prototype experiment must remain outside canonical skill runtime")
    replacement = experiment.get("replacement")
    if not isinstance(replacement, dict) or set(replacement) != {
        "start_heading",
        "end_heading_exclusive",
        "candidate_section",
    }:
        raise ValueError("experiment replacement contract is incomplete")
    for field in ("start_heading", "end_heading_exclusive", "candidate_section"):
        if not isinstance(replacement[field], str) or not replacement[field].strip():
            raise ValueError(f"experiment replacement {field} must be non-empty")
    repo_path(replacement["candidate_section"])
    if experiment.get("selection_case_contract") != SEMANTIC_CASE_CONTRACT:
        raise ValueError("experiment must use the canonical semantic case contract")
    if experiment.get("model_trial_manifest") != MODEL_TRIAL_MANIFEST:
        raise ValueError("experiment must use the canonical model-trial manifest")
    screening = experiment.get("screening_case_ids")
    if not isinstance(screening, list) or not screening:
        raise ValueError("experiment requires screening_case_ids")
    if any(not isinstance(case_id, str) or not case_id for case_id in screening):
        raise ValueError("experiment screening_case_ids must be non-empty strings")
    if len(screening) != len(set(screening)):
        raise ValueError("experiment screening_case_ids contain duplicates")


def load_experiment_from_git(repo: Path, candidate_ref: str, experiment_path: str) -> dict[str, Any]:
    experiment_path = repo_path(experiment_path)
    try:
        experiment = json.loads(git_text(repo, "show", f"{candidate_ref}:{experiment_path}"))
    except json.JSONDecodeError as exc:
        raise ValueError("candidate experiment descriptor is invalid JSON") from exc
    if not isinstance(experiment, dict):
        raise ValueError("candidate experiment descriptor must be an object")
    validate_experiment(experiment)
    return experiment


def load_runtime_views(
    repo: Path, candidate_ref: str, experiment_path: str
) -> tuple[RuntimeView, RuntimeView, dict[str, Any]]:
    validate_candidate_ref(candidate_ref)
    verify_exact_commit(repo, PROGRAM_BASELINE_REF)
    verify_exact_commit(repo, candidate_ref)
    experiment = load_experiment_from_git(repo, candidate_ref, experiment_path)
    replacement = experiment["replacement"]

    baseline_entrypoint = git_text(repo, "show", f"{PROGRAM_BASELINE_REF}:skill/SKILL.md")
    candidate_section = git_text(
        repo, "show", f"{candidate_ref}:{repo_path(replacement['candidate_section'])}"
    )
    candidate_entrypoint = replace_section(
        baseline_entrypoint,
        replacement["start_heading"],
        replacement["end_heading_exclusive"],
        candidate_section,
    )
    if candidate_entrypoint == baseline_entrypoint:
        raise ValueError("candidate materialization did not change the experiment entrypoint")

    reference_paths = [
        path.strip()
        for path in git_text(
            repo,
            "ls-tree",
            "-r",
            "--name-only",
            PROGRAM_BASELINE_REF,
            "skill/references",
        ).splitlines()
        if path.strip().endswith(".md")
    ]
    if not reference_paths:
        raise ValueError("immutable baseline has no runtime reference documents")
    references: dict[str, str] = {}
    for full_path in reference_paths:
        if not full_path.startswith("skill/"):
            raise ValueError(f"unexpected baseline runtime path: {full_path}")
        relative_path = full_path[len("skill/") :]
        repo_path(relative_path)
        references[relative_path] = git_text(
            repo, "show", f"{PROGRAM_BASELINE_REF}:{full_path}"
        )

    baseline = RuntimeView(
        label="v1.2.2-baseline",
        ref=PROGRAM_BASELINE_REF,
        entrypoint=baseline_entrypoint,
        references=dict(references),
        entrypoint_sha256=sha256_text(baseline_entrypoint),
    )
    candidate = RuntimeView(
        label=f"{experiment.get('experiment_id', 'candidate')}-candidate",
        ref=candidate_ref,
        entrypoint=candidate_entrypoint,
        references=dict(references),
        entrypoint_sha256=sha256_text(candidate_entrypoint),
    )
    return baseline, candidate, experiment


def validate_contracts(
    manifest: dict[str, Any], scenarios: dict[str, Any], experiment: dict[str, Any]
) -> dict[str, dict[str, Any]]:
    required_manifest = {
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
    if set(manifest) != required_manifest:
        raise ValueError("model-trial manifest fields changed unexpectedly")
    if manifest["schema_version"] != 1 or manifest["evidence_kind"] != EVIDENCE_KIND:
        raise ValueError("unsupported model-trial manifest")
    if manifest["baseline_ref"] != PROGRAM_BASELINE_REF:
        raise ValueError("model-trial manifest baseline drifted")
    if manifest["semantic_case_contract"] != SEMANTIC_CASE_CONTRACT:
        raise ValueError("model-trial manifest semantic owner drifted")
    minimum_pairs = manifest["minimum_pairs_per_case"]
    if not isinstance(minimum_pairs, int) or isinstance(minimum_pairs, bool) or minimum_pairs < 1:
        raise ValueError("minimum_pairs_per_case must be a positive integer")
    case_ids = manifest["case_ids"]
    if not isinstance(case_ids, list) or not case_ids or len(case_ids) != len(set(case_ids)):
        raise ValueError("model-trial manifest case_ids are invalid")

    if scenarios.get("schema_version") != 1 or scenarios.get("baseline_ref") != PROGRAM_BASELINE_REF:
        raise ValueError("semantic scenario contract baseline/schema drifted")
    rows = scenarios.get("comparison_cases")
    if not isinstance(rows, list) or not rows:
        raise ValueError("semantic scenario contract requires comparison_cases")
    by_id: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("comparison case must be an object")
        case_id = row.get("id")
        if not isinstance(case_id, str) or not case_id or case_id in by_id:
            raise ValueError("comparison case IDs must be unique non-empty strings")
        trial_input = row.get("trial_input")
        if not isinstance(trial_input, dict) or not trial_input:
            raise ValueError(f"comparison case {case_id} requires canonical trial_input")
        by_id[case_id] = row
    if set(case_ids) != set(by_id):
        raise ValueError("model-trial manifest must select exactly the canonical semantic case IDs")
    screening = experiment["screening_case_ids"]
    if any(case_id not in by_id for case_id in screening):
        raise ValueError("experiment screening case is missing from the semantic case owner")
    return by_id


def build_plan(
    manifest: dict[str, Any],
    cases_by_id: dict[str, dict[str, Any]],
    experiment: dict[str, Any],
    candidate_ref: str,
    suite: str,
    pairs_per_case: int,
    trial_id: str,
) -> dict[str, Any]:
    validate_candidate_ref(candidate_ref)
    if not TRIAL_ID_RE.fullmatch(trial_id):
        raise ValueError("trial-id must use only letters, digits, dot, underscore, or hyphen")
    minimum = manifest["minimum_pairs_per_case"]
    if not isinstance(pairs_per_case, int) or isinstance(pairs_per_case, bool) or pairs_per_case < minimum:
        raise ValueError(f"pairs-per-case must be at least {minimum}")
    if suite == "screening":
        selected = list(experiment["screening_case_ids"])
    elif suite == "selection":
        selected = list(manifest["case_ids"])
    else:
        raise ValueError(f"unsupported suite: {suite}")

    inputs: dict[str, dict[str, str]] = {}
    for case_id in selected:
        trial_input = cases_by_id[case_id]["trial_input"]
        input_text = "CASE INPUT (canonical JSON):\n" + canonical_json(trial_input)
        inputs[case_id] = {
            "input_text": input_text,
            "input_fingerprint": "sha256:" + sha256_text(input_text),
        }

    runs: list[dict[str, Any]] = []
    for case_id in selected:
        for pair_index in range(1, pairs_per_case + 1):
            pair_id = f"{trial_id}:{case_id}:p{pair_index:02d}"
            order = ("baseline", "candidate") if pair_index % 2 == 1 else ("candidate", "baseline")
            for position, representation in enumerate(order, start=1):
                runs.append(
                    {
                        "run_id": f"{pair_id}:{representation}",
                        "pair_id": pair_id,
                        "case_id": case_id,
                        "input_fingerprint": inputs[case_id]["input_fingerprint"],
                        "input_text": inputs[case_id]["input_text"],
                        "representation": representation,
                        "order": position,
                    }
                )

    plan_core = {
        "schema_version": 1,
        "suite_id": manifest["suite_id"],
        "evidence_kind": EVIDENCE_KIND,
        "trial_id": trial_id,
        "suite": suite,
        "pairs_per_case": pairs_per_case,
        "baseline_ref": PROGRAM_BASELINE_REF,
        "candidate_ref": candidate_ref,
        "case_ids": selected,
        "runs": runs,
    }
    plan = dict(plan_core)
    plan["plan_fingerprint"] = fingerprint(plan_core)
    validate_plan(plan)
    return plan


def validate_plan(plan: dict[str, Any]) -> None:
    if plan.get("schema_version") != 1 or plan.get("evidence_kind") != EVIDENCE_KIND:
        raise ValueError("unsupported trial plan")
    if plan.get("baseline_ref") != PROGRAM_BASELINE_REF:
        raise ValueError("trial plan baseline drifted")
    validate_candidate_ref(str(plan.get("candidate_ref", "")))
    expected_fingerprint = plan.get("plan_fingerprint")
    core = {key: value for key, value in plan.items() if key != "plan_fingerprint"}
    if expected_fingerprint != fingerprint(core):
        raise ValueError("trial plan fingerprint does not match plan content")
    runs = plan.get("runs")
    if not isinstance(runs, list) or not runs:
        raise ValueError("trial plan requires runs")
    seen_run_ids: set[str] = set()
    pairs: dict[str, list[dict[str, Any]]] = {}
    for run in runs:
        if not isinstance(run, dict) or set(run) != {
            "run_id",
            "pair_id",
            "case_id",
            "input_fingerprint",
            "input_text",
            "representation",
            "order",
        }:
            raise ValueError("trial plan run fields changed unexpectedly")
        run_id = run["run_id"]
        if not isinstance(run_id, str) or not run_id or run_id in seen_run_ids:
            raise ValueError("trial plan run_id must be unique and non-empty")
        seen_run_ids.add(run_id)
        if run["representation"] not in {"baseline", "candidate"} or run["order"] not in {1, 2}:
            raise ValueError(f"invalid representation/order in run {run_id}")
        if not isinstance(run["input_text"], str) or not run["input_text"]:
            raise ValueError(f"run {run_id} requires exact input_text")
        expected_input = "sha256:" + sha256_text(run["input_text"])
        if run["input_fingerprint"] != expected_input:
            raise ValueError(f"run {run_id} input_fingerprint does not match exact input")
        pairs.setdefault(run["pair_id"], []).append(run)
    for pair_id, rows in pairs.items():
        if len(rows) != 2:
            raise ValueError(f"pair {pair_id} must contain exactly two planned runs")
        if {row["representation"] for row in rows} != {"baseline", "candidate"}:
            raise ValueError(f"pair {pair_id} must contain one baseline and one candidate")
        if {row["order"] for row in rows} != {1, 2}:
            raise ValueError(f"pair {pair_id} must have complementary order")
        if len({row["case_id"] for row in rows}) != 1:
            raise ValueError(f"pair {pair_id} must use one case_id")
        if len({row["input_fingerprint"] for row in rows}) != 1 or len(
            {row["input_text"] for row in rows}
        ) != 1:
            raise ValueError(f"pair {pair_id} baseline/candidate inputs do not match exactly")


def reject_sensitive_setting_keys(value: Any, path: str = "settings") -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            if not isinstance(key, str):
                raise ValueError(f"{path} keys must be strings")
            normalized = key.replace("-", "_")
            if SENSITIVE_SETTING_KEY_RE.search(normalized):
                raise ValueError(f"sensitive-looking model setting is not allowed: {path}.{key}")
            reject_sensitive_setting_keys(nested, f"{path}.{key}")
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            reject_sensitive_setting_keys(nested, f"{path}[{index}]")


def parse_settings(settings_json: str | None) -> dict[str, Any]:
    if settings_json is None:
        raise ValueError("explicit MODEL_SETTINGS_JSON/--settings-json is required for live runs")
    try:
        settings = json.loads(settings_json)
    except json.JSONDecodeError as exc:
        raise ValueError("model settings must be valid JSON") from exc
    if not isinstance(settings, dict):
        raise ValueError("model settings must be a JSON object")
    conflicts = RESERVED_MODEL_SETTINGS.intersection(settings)
    if conflicts:
        raise ValueError(f"model settings contain runner-owned keys: {sorted(conflicts)}")
    reject_sensitive_setting_keys(settings)
    return settings


def normalize_api_base_url(value: str) -> tuple[str, str]:
    if not value or not value.strip():
        raise ValueError("API_BASE_URL is required for live runs")
    parsed = urllib.parse.urlsplit(value.strip())
    if parsed.scheme not in {"https", "http"} or not parsed.hostname:
        raise ValueError("API_BASE_URL must be an absolute http(s) URL")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("API_BASE_URL must not contain credentials, query, or fragment")
    if parsed.scheme == "http" and parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
        raise ValueError("plaintext HTTP is allowed only for loopback/local mocked endpoints")
    path = parsed.path.rstrip("/")
    base = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, path, "", ""))
    if path.endswith("/chat/completions"):
        endpoint = base
    else:
        endpoint_path = (path + "/chat/completions") if path else "/chat/completions"
        endpoint = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, endpoint_path, "", ""))
    return base, endpoint


def build_runtime_config(
    *,
    api_base_url: str | None,
    model_id: str | None,
    model_version: str | None,
    settings_json: str | None,
    instruction_role: str,
    timeout_seconds: float,
    max_model_turns: int,
    environ: dict[str, str] | os._Environ[str],
) -> tuple[RuntimeConfig, str]:
    base_input = api_base_url or environ.get("API_BASE_URL")
    model = model_id or environ.get("MODEL_ID")
    version = model_version or environ.get("MODEL_VERSION")
    settings_source = settings_json if settings_json is not None else environ.get("MODEL_SETTINGS_JSON")
    secret = environ.get("RUNTIME_MODEL_API_KEY", "")
    if not isinstance(base_input, str):
        raise ValueError("API_BASE_URL is required for live runs")
    base, endpoint = normalize_api_base_url(base_input)
    if not isinstance(model, str) or not model.strip():
        raise ValueError("MODEL_ID is required for live runs")
    if not isinstance(version, str) or not version.strip():
        raise ValueError("MODEL_VERSION is required for live runs")
    if not secret.strip():
        raise ValueError("RUNTIME_MODEL_API_KEY must be provisioned in the runtime environment")
    settings = parse_settings(settings_source)
    if instruction_role not in {"system", "developer"}:
        raise ValueError("instruction-role must be system or developer")
    if not isinstance(timeout_seconds, (int, float)) or isinstance(timeout_seconds, bool) or timeout_seconds <= 0:
        raise ValueError("timeout must be positive")
    if not isinstance(max_model_turns, int) or isinstance(max_model_turns, bool) or max_model_turns < 1:
        raise ValueError("max-model-turns must be a positive integer")
    return (
        RuntimeConfig(
            api_base_url=base,
            endpoint_url=endpoint,
            model_id=model.strip(),
            model_version=version.strip(),
            settings=settings,
            instruction_role=instruction_role,
            timeout_seconds=float(timeout_seconds),
            max_model_turns=max_model_turns,
        ),
        secret,
    )


def runtime_reference_tool() -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": "read_runtime_reference",
            "description": "Read one routed GitHub Project Orchestrator runtime reference by exact relative path.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
                "additionalProperties": False,
            },
        },
    }


def toolset_fingerprint(runtime: RuntimeView) -> str:
    return fingerprint(
        {
            "toolset_id": TOOLSET_ID,
            "tool": runtime_reference_tool(),
            "reference_paths": sorted(runtime.references),
        }
    )


def settings_fingerprint(config: RuntimeConfig) -> str:
    return fingerprint(
        {
            "api_base_url": config.api_base_url,
            "endpoint_kind": "chat-completions",
            "instruction_role": config.instruction_role,
            "model_settings": config.settings,
            "max_model_turns": config.max_model_turns,
        }
    )


def redact_secret(text: str, secret: str) -> str:
    if secret:
        text = text.replace(secret, "[REDACTED]")
        encoded = urllib.parse.quote(secret, safe="")
        if encoded and encoded != secret:
            text = text.replace(encoded, "[REDACTED]")
    return text


def http_chat_completion(
    endpoint: str, api_key: str, payload: dict[str, Any], timeout: float
) -> tuple[dict[str, Any], dict[str, Any]]:
    body = canonical_json(payload).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read(MAX_HTTP_RESPONSE_BYTES + 1)
            if len(raw) > MAX_HTTP_RESPONSE_BYTES:
                raise TransportError("provider response exceeded audit-safe size limit")
            status = getattr(response, "status", 200)
    except urllib.error.HTTPError as exc:
        try:
            error_body = exc.read(8192).decode("utf-8", errors="replace")
        except Exception:
            error_body = ""
        detail = redact_secret(error_body, api_key)
        raise TransportError(f"provider HTTP {exc.code}: {detail[:4096]}") from None
    except urllib.error.URLError as exc:
        raise TransportError(redact_secret(f"provider connection failed: {exc.reason}", api_key)) from None
    except TimeoutError:
        raise TransportError("provider request timed out") from None
    try:
        decoded = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProviderSchemaError("provider returned invalid JSON") from exc
    if not isinstance(decoded, dict):
        raise ProviderSchemaError("provider response must be a JSON object")
    return decoded, {"http_status": int(status)}


def trial_instruction(runtime: RuntimeView) -> str:
    return (
        "You are executing an audited GitHub Project Orchestrator representation trial. "
        "Follow the supplied runtime exactly and act only on the case state supplied by the user. "
        "Use read_runtime_reference only when the runtime routes you to a reference path. "
        "Do not invent external repository state or claim actions that the controlled toolset cannot perform. "
        "Do not expose private chain-of-thought; provide only the observable response/actions needed to execute the runtime.\n\n"
        "<GITHUB_PROJECT_ORCHESTRATOR_RUNTIME>\n"
        + runtime.entrypoint
        + "\n</GITHUB_PROJECT_ORCHESTRATOR_RUNTIME>"
    )


def extract_choice(response: dict[str, Any]) -> tuple[dict[str, Any], str | None, str | None]:
    choices = response.get("choices")
    if not isinstance(choices, list) or len(choices) != 1 or not isinstance(choices[0], dict):
        raise ProviderSchemaError("provider response must contain exactly one choice")
    choice = choices[0]
    message = choice.get("message")
    if not isinstance(message, dict):
        raise ProviderSchemaError("provider choice requires a message object")
    content = message.get("content")
    refusal = message.get("refusal")
    if content is not None and not isinstance(content, str):
        raise ProviderSchemaError("provider assistant content must be text or null")
    if refusal is not None and not isinstance(refusal, str):
        raise ProviderSchemaError("provider assistant refusal must be text or null")
    finish_reason = choice.get("finish_reason")
    if finish_reason is not None and not isinstance(finish_reason, str):
        raise ProviderSchemaError("provider finish_reason must be text or null")
    tool_calls = message.get("tool_calls")
    if tool_calls is not None and not isinstance(tool_calls, list):
        raise ProviderSchemaError("provider tool_calls must be an array when present")
    safe_message = {
        "role": "assistant",
        "content": content,
    }
    if tool_calls:
        safe_message["tool_calls"] = tool_calls
    return safe_message, refusal, finish_reason


def handle_tool_call(call: Any, runtime: RuntimeView) -> tuple[dict[str, Any], dict[str, Any]]:
    if not isinstance(call, dict):
        raise ProviderSchemaError("tool call must be an object")
    call_id = call.get("id")
    if not isinstance(call_id, str) or not call_id:
        raise ProviderSchemaError("tool call requires a non-empty id")
    function = call.get("function")
    if call.get("type") != "function" or not isinstance(function, dict):
        result = {"error": "unsupported_tool_type"}
        operation = {"tool_call_id": call_id, "tool": "unsupported", "status": "rejected"}
        return result, operation
    name = function.get("name")
    arguments = function.get("arguments")
    if name != "read_runtime_reference" or not isinstance(arguments, str):
        result = {"error": "unsupported_tool_call"}
        operation = {
            "tool_call_id": call_id,
            "tool": str(name) if name is not None else "unknown",
            "status": "rejected",
        }
        return result, operation
    try:
        parsed = json.loads(arguments)
    except json.JSONDecodeError:
        parsed = None
    if not isinstance(parsed, dict) or set(parsed) != {"path"} or not isinstance(parsed.get("path"), str):
        result = {"error": "invalid_tool_arguments"}
        operation = {
            "tool_call_id": call_id,
            "tool": name,
            "status": "rejected",
        }
        return result, operation
    path = parsed["path"]
    try:
        repo_path(path)
    except ValueError:
        result = {"error": "invalid_reference_path"}
        operation = {"tool_call_id": call_id, "tool": name, "status": "rejected", "path": path}
        return result, operation
    content = runtime.references.get(path)
    if content is None:
        result = {"error": "reference_not_available", "path": path}
        operation = {"tool_call_id": call_id, "tool": name, "status": "rejected", "path": path}
        return result, operation
    result = {"path": path, "content": content}
    operation = {
        "tool_call_id": call_id,
        "tool": name,
        "status": "completed",
        "path": path,
        "content_sha256": sha256_text(content),
        "content_bytes": len(content.encode("utf-8")),
    }
    return result, operation


def execute_conversation(
    runtime: RuntimeView,
    run_plan: dict[str, Any],
    config: RuntimeConfig,
    api_key: str,
    transport: Transport,
) -> dict[str, Any]:
    messages: list[dict[str, Any]] = [
        {"role": config.instruction_role, "content": trial_instruction(runtime)},
        {"role": "user", "content": run_plan["input_text"]},
    ]
    tool = runtime_reference_tool()
    tool_operations: list[dict[str, Any]] = []
    provider_calls: list[dict[str, Any]] = []
    last_content: str | None = None
    last_refusal: str | None = None
    last_finish: str | None = None

    for model_turn in range(1, config.max_model_turns + 1):
        payload: dict[str, Any] = {
            "model": config.model_id,
            "messages": messages,
            "tools": [tool],
            "tool_choice": "auto",
        }
        payload.update(config.settings)
        response, transport_meta = transport(
            config.endpoint_url, api_key, payload, config.timeout_seconds
        )
        assistant_message, refusal, finish_reason = extract_choice(response)
        response_id = response.get("id")
        if response_id is not None and not isinstance(response_id, str):
            raise ProviderSchemaError("provider response id must be text when present")
        provider_calls.append(
            {
                "model_turn": model_turn,
                "http_status": transport_meta.get("http_status"),
                "provider_response_id": response_id,
                "finish_reason": finish_reason,
            }
        )
        last_content = assistant_message.get("content")
        last_refusal = refusal
        last_finish = finish_reason
        tool_calls = assistant_message.get("tool_calls") or []
        if not tool_calls:
            return {
                "status": "complete",
                "termination": "assistant_output",
                "output": {"content": last_content, "refusal": last_refusal},
                "provider_calls": provider_calls,
                "tool_operations": tool_operations,
            }

        messages.append(assistant_message)
        for call in tool_calls:
            result, operation = handle_tool_call(call, runtime)
            tool_operations.append(operation)
            call_id = call.get("id") if isinstance(call, dict) else None
            if not isinstance(call_id, str) or not call_id:
                raise ProviderSchemaError("auditable tool call requires a stable id")
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call_id,
                    "content": canonical_json(result),
                }
            )

    return {
        "status": "complete",
        "termination": "tool_round_limit",
        "output": {"content": last_content, "refusal": last_refusal},
        "provider_calls": provider_calls,
        "tool_operations": tool_operations,
        "last_finish_reason": last_finish,
    }


def build_runtime_identity(config: RuntimeConfig, runtime: RuntimeView) -> dict[str, Any]:
    return {
        "api_base_url": config.api_base_url,
        "endpoint_kind": "chat-completions",
        "model_id": config.model_id,
        "model_version": config.model_version,
        "settings": config.settings,
        "instruction_role": config.instruction_role,
        "max_model_turns": config.max_model_turns,
        "settings_fingerprint": settings_fingerprint(config),
        "toolset_id": TOOLSET_ID,
        "toolset_fingerprint": toolset_fingerprint(runtime),
    }


def execute_suite(
    repo: Path,
    plan: dict[str, Any],
    baseline: RuntimeView,
    candidate: RuntimeView,
    config: RuntimeConfig,
    api_key: str,
    transport: Transport = http_chat_completion,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    validate_plan(plan)
    baseline_toolset = toolset_fingerprint(baseline)
    candidate_toolset = toolset_fingerprint(candidate)
    if baseline_toolset != candidate_toolset:
        raise ValueError("baseline/candidate toolsets are not equivalent")
    runtime_identity = build_runtime_identity(config, baseline)
    execution_id = fingerprint(
        {
            "plan_fingerprint": plan["plan_fingerprint"],
            "model_id": config.model_id,
            "model_version": config.model_version,
            "settings_fingerprint": runtime_identity["settings_fingerprint"],
            "toolset_fingerprint": runtime_identity["toolset_fingerprint"],
        }
    )
    try:
        runner_head = git_text(repo, "rev-parse", "HEAD").strip()
    except ValueError:
        runner_head = "unknown"
    try:
        runner_sha256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    except OSError:
        runner_sha256 = "unknown"

    raw: dict[str, Any] = {
        "schema_version": 1,
        "evidence_kind": RAW_EVIDENCE_KIND,
        "status": "complete",
        "created_at": utc_now(),
        "trial_id": plan["trial_id"],
        "execution_id": execution_id,
        "suite_id": plan["suite_id"],
        "plan_fingerprint": plan["plan_fingerprint"],
        "baseline_representation": {
            "label": baseline.label,
            "ref": baseline.ref,
            "entrypoint_sha256": baseline.entrypoint_sha256,
        },
        "candidate_representation": {
            "label": candidate.label,
            "ref": candidate.ref,
            "entrypoint_sha256": candidate.entrypoint_sha256,
        },
        "runtime_identity": runtime_identity,
        "runner_identity": {"git_head": runner_head, "script_sha256": runner_sha256},
        "plan": plan,
        "runs": [],
        "failure": None,
    }

    runtimes = {"baseline": baseline, "candidate": candidate}
    for run_plan in plan["runs"]:
        audit_ref = f"trial://{execution_id}/{run_plan['run_id']}"
        started_at = utc_now()
        try:
            observable = execute_conversation(
                runtimes[run_plan["representation"]],
                run_plan,
                config,
                api_key,
                transport,
            )
        except (TransportError, ProviderSchemaError, ValueError) as exc:
            message = redact_secret(str(exc), api_key)
            raw["status"] = "incomplete"
            raw["failure"] = {
                "run_id": run_plan["run_id"],
                "type": exc.__class__.__name__,
                "message": message,
            }
            break
        raw["runs"].append(
            {
                "run_id": run_plan["run_id"],
                "pair_id": run_plan["pair_id"],
                "case_id": run_plan["case_id"],
                "input_fingerprint": run_plan["input_fingerprint"],
                "representation": run_plan["representation"],
                "order": run_plan["order"],
                "audit_ref": audit_ref,
                "started_at": started_at,
                "completed_at": utc_now(),
                **observable,
            }
        )

    if raw["status"] != "complete" or len(raw["runs"]) != len(plan["runs"]):
        raw["status"] = "incomplete"
        return raw, None
    template = build_annotation_template(raw)
    return raw, template


def validate_raw_evidence(raw: dict[str, Any]) -> None:
    if raw.get("schema_version") != 1 or raw.get("evidence_kind") != RAW_EVIDENCE_KIND:
        raise ValueError("unsupported raw evidence")
    if raw.get("status") != "complete" or raw.get("failure") is not None:
        raise ValueError("incomplete raw evidence cannot produce scorer input")
    plan = raw.get("plan")
    if not isinstance(plan, dict):
        raise ValueError("raw evidence requires the exact trial plan")
    validate_plan(plan)
    runs = raw.get("runs")
    if not isinstance(runs, list) or len(runs) != len(plan["runs"]):
        raise ValueError("raw evidence run count does not match the frozen plan")
    planned = {run["run_id"]: run for run in plan["runs"]}
    seen_refs: set[str] = set()
    seen_runs: set[str] = set()
    for run in runs:
        if not isinstance(run, dict):
            raise ValueError("raw evidence run must be an object")
        run_id = run.get("run_id")
        audit_ref = run.get("audit_ref")
        if not isinstance(run_id, str) or run_id not in planned or run_id in seen_runs:
            raise ValueError("raw evidence run_id is missing, duplicate, or not in the frozen plan")
        seen_runs.add(run_id)
        if not isinstance(audit_ref, str) or not audit_ref or audit_ref in seen_refs:
            raise ValueError("raw evidence audit_ref must be unique and non-empty")
        seen_refs.add(audit_ref)
        expected = planned[run_id]
        for field in ("pair_id", "case_id", "input_fingerprint", "representation", "order"):
            if run.get(field) != expected[field]:
                raise ValueError(f"raw evidence drifted from plan for {run_id}: {field}")
    runtime = raw.get("runtime_identity")
    if not isinstance(runtime, dict):
        raise ValueError("raw evidence requires runtime_identity")
    for field in ("model_id", "model_version", "settings_fingerprint", "toolset_fingerprint"):
        if not isinstance(runtime.get(field), str) or not runtime[field].strip():
            raise ValueError(f"raw evidence runtime_identity missing {field}")


def build_annotation_template(raw: dict[str, Any]) -> dict[str, Any]:
    validate_raw_evidence(raw)
    runtime = raw["runtime_identity"]
    baseline = raw["baseline_representation"]
    candidate = raw["candidate_representation"]
    return {
        "schema_version": 1,
        "suite_id": raw["suite_id"],
        "evidence_kind": EVIDENCE_KIND,
        "baseline_representation": {"label": baseline["label"], "ref": baseline["ref"]},
        "candidate_representation": {"label": candidate["label"], "ref": candidate["ref"]},
        "runtime_identity": {
            "model_id": runtime["model_id"],
            "model_version": runtime["model_version"],
            "settings_fingerprint": runtime["settings_fingerprint"],
            "toolset_fingerprint": runtime["toolset_fingerprint"],
        },
        "runs": [
            {
                "run_id": run["run_id"],
                "pair_id": run["pair_id"],
                "case_id": run["case_id"],
                "input_fingerprint": run["input_fingerprint"],
                "representation": run["representation"],
                "order": run["order"],
                "transcript_ref": run["audit_ref"],
                "observed": {
                    "correct_next_action": None,
                    "protected_violations": None,
                    "steps_to_first_useful_action": None,
                    "unnecessary_questions": None,
                    "unnecessary_actions": None,
                    "unnecessary_reference_loads": None,
                    "manual_continue_required": None,
                },
            }
            for run in raw["runs"]
        ],
    }


def ensure_output_absent(path: Path | None, label: str) -> None:
    if path is not None and path.exists():
        raise ValueError(f"{label} already exists; refusing to overwrite auditable evidence: {path}")


def write_json_exclusive(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, sort_keys=True, indent=2)
        handle.write("\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--candidate-ref", required=True)
    parser.add_argument("--experiment", default=DEFAULT_EXPERIMENT)
    parser.add_argument("--manifest", default=MODEL_TRIAL_MANIFEST)
    parser.add_argument("--scenarios", default=SEMANTIC_CASE_CONTRACT)
    parser.add_argument("--suite", choices=("screening", "selection"), default="screening")
    parser.add_argument("--pairs", type=int)
    parser.add_argument("--trial-id")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--plan-output", type=Path)
    parser.add_argument("--raw-output", type=Path)
    parser.add_argument("--annotation-template-output", type=Path)
    parser.add_argument("--api-base-url")
    parser.add_argument("--model-id")
    parser.add_argument("--model-version")
    parser.add_argument("--settings-json")
    parser.add_argument("--instruction-role", choices=("system", "developer"), default="system")
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--max-model-turns", type=int, default=8)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    secret = ""
    try:
        repo = args.repo_root.resolve()
        manifest_path = repo / repo_path(args.manifest)
        scenarios_path = repo / repo_path(args.scenarios)
        manifest = load_json(manifest_path)
        scenarios = load_json(scenarios_path)
        baseline, candidate, experiment = load_runtime_views(
            repo, args.candidate_ref, args.experiment
        )
        cases_by_id = validate_contracts(manifest, scenarios, experiment)
        pairs = args.pairs if args.pairs is not None else manifest["minimum_pairs_per_case"]
        trial_id = args.trial_id or f"trial-{uuid.uuid4().hex}"
        plan = build_plan(
            manifest,
            cases_by_id,
            experiment,
            args.candidate_ref,
            args.suite,
            pairs,
            trial_id,
        )
        plan["representations"] = {
            "baseline": {
                "label": baseline.label,
                "ref": baseline.ref,
                "entrypoint_sha256": baseline.entrypoint_sha256,
            },
            "candidate": {
                "label": candidate.label,
                "ref": candidate.ref,
                "entrypoint_sha256": candidate.entrypoint_sha256,
            },
        }
        # Representation hashes are audit metadata, not part of the predeclared order/input plan.
        validate_plan({key: value for key, value in plan.items() if key != "representations"})

        ensure_output_absent(args.plan_output, "plan-output")
        ensure_output_absent(args.raw_output, "raw-output")
        ensure_output_absent(args.annotation_template_output, "annotation-template-output")
        if args.plan_output is not None:
            write_json_exclusive(args.plan_output, plan)

        if args.dry_run:
            if args.raw_output is not None or args.annotation_template_output is not None:
                raise ValueError("dry-run does not write raw/scorer evidence outputs")
            print(json.dumps(plan, ensure_ascii=False, sort_keys=True, indent=2))
            return

        if args.raw_output is None or args.annotation_template_output is None:
            raise ValueError("live runs require --raw-output and --annotation-template-output")
        config, secret = build_runtime_config(
            api_base_url=args.api_base_url,
            model_id=args.model_id,
            model_version=args.model_version,
            settings_json=args.settings_json,
            instruction_role=args.instruction_role,
            timeout_seconds=args.timeout,
            max_model_turns=args.max_model_turns,
            environ=os.environ,
        )
        execution_plan = {key: value for key, value in plan.items() if key != "representations"}
        raw, template = execute_suite(
            repo,
            execution_plan,
            baseline,
            candidate,
            config,
            secret,
        )
        write_json_exclusive(args.raw_output, raw)
        if template is None:
            print(
                json.dumps(
                    {
                        "status": "incomplete",
                        "execution_id": raw["execution_id"],
                        "raw_output": str(args.raw_output),
                        "failure": raw["failure"],
                    },
                    sort_keys=True,
                ),
                file=sys.stderr,
            )
            raise SystemExit(2)
        write_json_exclusive(args.annotation_template_output, template)
        print(
            json.dumps(
                {
                    "status": "complete",
                    "execution_id": raw["execution_id"],
                    "raw_output": str(args.raw_output),
                    "annotation_template_output": str(args.annotation_template_output),
                    "annotation_required_before_scoring": True,
                },
                sort_keys=True,
            )
        )
    except SystemExit:
        raise
    except Exception as exc:
        message = redact_secret(str(exc), secret)
        print(f"ERROR: {message}", file=sys.stderr)
        raise SystemExit(2) from None


if __name__ == "__main__":
    main()
