#!/usr/bin/env python3
"""Run observable paired A/B trials against an OpenAI-compatible chat-completions API.

The harness measures only visible tool use and terminal decisions. It never requests,
records, or scores private chain-of-thought.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any

PROGRAM_BASELINE = "f98e8a242c720931e34aa7c4e8a799090e3d0495"
DIRECT_REFERENCE_PATHS = (
    "references/authority-gates.md",
    "references/master-cycle.md",
    "references/engineering-quality.md",
    "references/governance.md",
    "references/task-contract.md",
    "references/worker-protocol.md",
    "references/review-integration.md",
    "references/release.md",
    "references/continuity.md",
    "references/eval-scenarios.md",
)
TERMINAL_TOOLS = {"execute_action", "ask_user", "stop"}
REASON_CODES = (
    "APPROVAL_REQUIRED",
    "DECISION_REQUIRED",
    "HUMAN_OPERATION_REQUIRED",
    "OTHER",
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def fingerprint(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def git_text(repo: Path, ref: str, path: str) -> str:
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
        raise ValueError(f"unable to read {ref}:{path}") from exc


def git_sha(repo: Path, ref: str) -> str:
    try:
        sha = subprocess.run(
            ["git", "rev-parse", f"{ref}^{{commit}}"],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ValueError(f"unable to resolve git ref: {ref}") from exc
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError(f"git ref did not resolve to a full SHA: {ref} -> {sha}")
    return sha


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_inputs(doc: dict) -> list[dict]:
    if doc.get("schema_version") != 1 or doc.get("experiment_id") != "decision-frame-v1":
        raise ValueError("unexpected decision-frame trial input schema/experiment")
    if doc.get("baseline_ref") != PROGRAM_BASELINE:
        raise ValueError("trial inputs must remain pinned to the immutable program baseline")
    policy = doc.get("input_policy", {})
    if policy.get("oracle_hidden_from_model") is not True:
        raise ValueError("trial oracle must remain hidden from the model")
    if policy.get("private_chain_of_thought_requested") is not False:
        raise ValueError("trial inputs must not request private chain-of-thought")
    if policy.get("same_input_required_within_pair") is not True:
        raise ValueError("paired trials must require identical input")
    inputs = doc.get("inputs")
    if not isinstance(inputs, list) or not inputs:
        raise ValueError("trial inputs are empty")
    seen = set()
    counts = defaultdict(int)
    required_top = {"input_id", "case_id", "prompt", "state", "action_options", "oracle"}
    for item in inputs:
        if not isinstance(item, dict) or set(item) != required_top:
            raise ValueError(f"every trial input must contain exactly {sorted(required_top)}")
        input_id = item["input_id"]
        if not isinstance(input_id, str) or not input_id or input_id in seen:
            raise ValueError(f"invalid/duplicate input_id: {input_id}")
        seen.add(input_id)
        counts[item["case_id"]] += 1
        if not isinstance(item["prompt"], str) or not item["prompt"].strip():
            raise ValueError(f"input {input_id} has empty prompt")
        if not isinstance(item["state"], dict) or not item["state"]:
            raise ValueError(f"input {input_id} has empty state")
        for dimension, state in item["state"].items():
            if set(state) != {"value", "basis_changed"}:
                raise ValueError(f"input {input_id} state {dimension} must have value/basis_changed")
            if not isinstance(state["basis_changed"], bool):
                raise ValueError(f"input {input_id} basis_changed must be boolean")
        actions = item["action_options"]
        if not isinstance(actions, list) or not actions or len(actions) != len(set(actions)):
            raise ValueError(f"input {input_id} action_options must be unique/non-empty")
        oracle = item["oracle"]
        terminal = oracle.get("terminal")
        if terminal not in TERMINAL_TOOLS:
            raise ValueError(f"input {input_id} has invalid terminal oracle")
        required_oracle = {
            "terminal",
            "required_reference_loads",
            "allowed_reference_loads",
            "required_state_resolutions",
        }
        if terminal == "execute_action":
            required_oracle.add("action_id")
            if oracle.get("action_id") not in actions:
                raise ValueError(f"input {input_id} oracle action is not an action option")
        elif terminal == "ask_user":
            required_oracle.add("reason_code")
            if oracle.get("reason_code") not in REASON_CODES:
                raise ValueError(f"input {input_id} has invalid oracle reason_code")
        if set(oracle) != required_oracle:
            raise ValueError(
                f"input {input_id} oracle fields must be exactly {sorted(required_oracle)}"
            )
        required_refs = oracle["required_reference_loads"]
        allowed_refs = oracle["allowed_reference_loads"]
        if not set(required_refs).issubset(set(allowed_refs)):
            raise ValueError(f"input {input_id} required refs must be allowed")
        if any(ref not in DIRECT_REFERENCE_PATHS for ref in allowed_refs):
            raise ValueError(f"input {input_id} uses unknown runtime reference")
        if any(dim not in item["state"] for dim in oracle["required_state_resolutions"]):
            raise ValueError(f"input {input_id} requires unknown state dimension")
    if policy.get("three_frozen_inputs_per_case") is True:
        wrong = {case: count for case, count in counts.items() if count != 3}
        if wrong:
            raise ValueError(f"expected exactly three frozen inputs per case: {wrong}")
    return inputs


def model_visible_input(item: dict) -> dict:
    return {
        "case_id": item["case_id"],
        "prompt": item["prompt"],
        "state": item["state"],
        "action_options": item["action_options"],
    }


def build_system_prompt(entrypoint: str) -> str:
    return (
        "You are executing the GitHub Project Orchestrator runtime below. Follow it exactly. "
        "This benchmark evaluates only observable tool use and terminal control decisions. "
        "Do not reveal, describe, or output private chain-of-thought. Do not answer in prose. "
        "Call at most one tool per assistant turn. Load a runtime reference only when the Skill "
        "requires that domain. Use resolve_state only when authoritative state really must be "
        "refreshed/reclassified. When sufficient evidence exists, terminate by calling exactly "
        "one of execute_action, ask_user, or stop.\n\n"
        "--- SKILL ENTRYPOINT ---\n"
        f"{entrypoint}\n"
        "--- END SKILL ENTRYPOINT ---"
    )


def build_user_prompt(item: dict) -> str:
    actions = "\n".join(f"- {action}" for action in item["action_options"])
    state_summary = "\n".join(
        f"- {dimension}={data['value']} (basis_changed={str(data['basis_changed']).lower()})"
        for dimension, data in item["state"].items()
    )
    return (
        f"CASE_ID: {item['case_id']}\n"
        f"INPUT_ID: {item['input_id']}\n\n"
        f"{item['prompt']}\n\n"
        "Authoritative runtime-state snapshot available to this case:\n"
        f"{state_summary}\n\n"
        "Allowed execute_action IDs:\n"
        f"{actions}\n"
    )


def tool_definitions() -> list[dict]:
    return [
        {
            "type": "function",
            "function": {
                "name": "load_reference",
                "description": "Load one directly routed runtime reference when the Skill requires that domain.",
                "parameters": {
                    "type": "object",
                    "properties": {"path": {"type": "string"}},
                    "required": ["path"],
                    "additionalProperties": False,
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "resolve_state",
                "description": "Refresh/reclassify one runtime dimension from authoritative state only when its basis requires it.",
                "parameters": {
                    "type": "object",
                    "properties": {"dimension": {"type": "string"}},
                    "required": ["dimension"],
                    "additionalProperties": False,
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "execute_action",
                "description": "Take the selected next project-control/engineering action.",
                "parameters": {
                    "type": "object",
                    "properties": {"action_id": {"type": "string"}},
                    "required": ["action_id"],
                    "additionalProperties": False,
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "ask_user",
                "description": "Stop for a real user/human gate only when required.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reason_code": {"type": "string", "enum": list(REASON_CODES)},
                        "question": {"type": "string"},
                    },
                    "required": ["reason_code", "question"],
                    "additionalProperties": False,
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "stop",
                "description": "Emit a canonical terminal boundary only when the runtime permits stopping.",
                "parameters": {
                    "type": "object",
                    "properties": {"boundary": {"type": "string"}},
                    "required": ["boundary"],
                    "additionalProperties": False,
                },
            },
        },
    ]


class OpenAICompatibleClient:
    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        model: str,
        temperature: float,
        max_tokens: int,
        timeout: float,
    ) -> None:
        if not base_url.startswith(("https://", "http://")):
            raise ValueError("API base URL must start with https:// or http://")
        if not api_key:
            raise ValueError("model API key is empty")
        if not model:
            raise ValueError("model id is empty")
        self.endpoint = base_url.rstrip("/") + "/chat/completions"
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout

    def complete(self, messages: list[dict], tools: list[dict]) -> dict:
        payload = {
            "model": self.model,
            "messages": messages,
            "tools": tools,
            "tool_choice": "auto",
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        request = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:2000]
            raise RuntimeError(f"model API HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"model API connection failed: {exc.reason}") from exc
        data = json.loads(body)
        choices = data.get("choices")
        if not isinstance(choices, list) or not choices:
            raise RuntimeError("model API response has no choices")
        message = choices[0].get("message")
        if not isinstance(message, dict):
            raise RuntimeError("model API response has no assistant message")
        return {"message": message, "response_model": data.get("model")}


def parse_tool_call(call: dict) -> tuple[str, dict, str]:
    function = call.get("function")
    if not isinstance(function, dict):
        raise ValueError("tool call missing function")
    name = function.get("name")
    call_id = call.get("id")
    if not isinstance(name, str) or not isinstance(call_id, str):
        raise ValueError("tool call missing name/id")
    raw_args = function.get("arguments", "{}")
    if isinstance(raw_args, str):
        args = json.loads(raw_args or "{}")
    elif isinstance(raw_args, dict):
        args = raw_args
    else:
        raise ValueError("tool call arguments must be JSON object/string")
    if not isinstance(args, dict):
        raise ValueError("tool call arguments must decode to object")
    return name, args, call_id


def score_terminal(item: dict, name: str, args: dict) -> tuple[bool, int, bool]:
    oracle = item["oracle"]
    expected = oracle["terminal"]
    if name != expected:
        return False, 1 if name == "ask_user" else 0, name == "stop"
    if name == "execute_action":
        return args.get("action_id") == oracle["action_id"], 0, False
    if name == "ask_user":
        return args.get("reason_code") == oracle["reason_code"], 0, False
    return True, 0, False


def run_one(
    *,
    client,
    item: dict,
    entrypoint: str,
    read_reference,
    representation: str,
    order: int,
    max_turns: int,
) -> tuple[dict, dict]:
    tools = tool_definitions()
    messages: list[dict] = [
        {"role": "system", "content": build_system_prompt(entrypoint)},
        {"role": "user", "content": build_user_prompt(item)},
    ]
    events: list[dict] = []
    loaded_refs: list[str] = []
    resolved: list[str] = []
    unnecessary_refs = 0
    unnecessary_actions = 0
    protected_violations: list[str] = []
    terminal_name = None
    terminal_args: dict = {}
    response_models: list[str] = []

    for _turn in range(max_turns):
        response = client.complete(messages, tools)
        response_model = response.get("response_model")
        if response_model:
            response_models.append(str(response_model))
        message = response["message"]
        tool_calls = message.get("tool_calls")
        if not isinstance(tool_calls, list) or not tool_calls:
            events.append({"type": "non_tool_response", "content": message.get("content")})
            protected_violations.append("non_tool_response")
            break
        messages.append({
            "role": "assistant",
            "content": message.get("content"),
            "tool_calls": tool_calls,
        })
        if len(tool_calls) > 1:
            events.append({"type": "multiple_tool_calls_same_turn", "count": len(tool_calls)})
            unnecessary_actions += len(tool_calls) - 1

        for raw_call in tool_calls:
            try:
                name, args, call_id = parse_tool_call(raw_call)
            except (ValueError, json.JSONDecodeError) as exc:
                events.append({"type": "invalid_tool_call", "error": str(exc)})
                protected_violations.append("invalid_tool_call")
                terminal_name = "invalid"
                break
            events.append({"type": "tool_call", "name": name, "args": args})

            if name == "load_reference":
                path = args.get("path")
                if path not in DIRECT_REFERENCE_PATHS:
                    protected_violations.append("invalid_reference_path")
                    result = {"error": "invalid reference path"}
                else:
                    if path in loaded_refs or path not in item["oracle"]["allowed_reference_loads"]:
                        unnecessary_refs += 1
                    loaded_refs.append(path)
                    result = {"path": path, "content": read_reference(path)}
                messages.append({
                    "role": "tool",
                    "tool_call_id": call_id,
                    "name": name,
                    "content": json.dumps(result, ensure_ascii=False),
                })
                continue

            if name == "resolve_state":
                dimension = args.get("dimension")
                state = item["state"].get(dimension)
                if state is None:
                    protected_violations.append("invalid_state_dimension")
                    result = {"error": "unknown state dimension"}
                else:
                    if dimension in resolved or not state["basis_changed"]:
                        unnecessary_actions += 1
                    resolved.append(dimension)
                    result = {"dimension": dimension, **state}
                messages.append({
                    "role": "tool",
                    "tool_call_id": call_id,
                    "name": name,
                    "content": json.dumps(result, ensure_ascii=False),
                })
                continue

            if name in TERMINAL_TOOLS:
                terminal_name = name
                terminal_args = args
                break

            protected_violations.append("unknown_tool")
            terminal_name = "invalid"
            break

        if terminal_name is not None:
            break

    if terminal_name is None:
        protected_violations.append("no_terminal_action")
        terminal_name = "invalid"

    missing_refs = sorted(
        set(item["oracle"]["required_reference_loads"]) - set(loaded_refs)
    )
    if missing_refs:
        protected_violations.extend(f"missing_required_reference:{ref}" for ref in missing_refs)

    if terminal_name in TERMINAL_TOOLS:
        correct, unnecessary_question, manual_continue = score_terminal(
            item, terminal_name, terminal_args
        )
    else:
        correct, unnecessary_question, manual_continue = False, 0, True
    if not correct:
        protected_violations.append("incorrect_next_control_action")

    nonterminal_tool_calls = sum(
        1
        for event in events
        if event.get("type") == "tool_call" and event.get("name") not in TERMINAL_TOOLS
    )
    observed = {
        "correct_next_action": correct,
        "protected_violations": sorted(set(protected_violations)),
        "steps_to_first_useful_action": nonterminal_tool_calls,
        "unnecessary_questions": unnecessary_question,
        "unnecessary_actions": unnecessary_actions,
        "unnecessary_reference_loads": unnecessary_refs,
        "manual_continue_required": manual_continue,
    }
    transcript = {
        "schema_version": 1,
        "input_id": item["input_id"],
        "case_id": item["case_id"],
        "representation": representation,
        "order": order,
        "model_visible_input_fingerprint": fingerprint(model_visible_input(item)),
        "events": events,
        "loaded_references": loaded_refs,
        "resolved_state_dimensions": resolved,
        "terminal": {"name": terminal_name, "args": terminal_args},
        "response_models": response_models,
        "observed": observed,
        "private_chain_of_thought_recorded": False,
    }
    return observed, transcript


def select_inputs(inputs: list[dict], mode: str) -> list[dict]:
    if mode == "full":
        return inputs
    screening_cases = {"hot-fast-master-path", "cold-master-recovery"}
    return [item for item in inputs if item["case_id"] in screening_cases]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument(
        "--experiment",
        type=Path,
        default=Path("benchmarks/phase7/experiments/decision-frame-v1/experiment.json"),
    )
    parser.add_argument(
        "--inputs",
        type=Path,
        default=Path("benchmarks/phase7/experiments/decision-frame-v1/trial-inputs.json"),
    )
    parser.add_argument("--mode", choices=("screen", "full"), default="screen")
    parser.add_argument("--api-base-url", required=True)
    parser.add_argument("--api-key-env", default="RUNTIME_MODEL_API_KEY")
    parser.add_argument("--model", required=True)
    parser.add_argument("--model-version", required=True)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=800)
    parser.add_argument("--max-turns", type=int, default=8)
    parser.add_argument("--timeout", type=float, default=90.0)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    inputs_path = args.inputs if args.inputs.is_absolute() else repo / args.inputs
    experiment_path = args.experiment if args.experiment.is_absolute() else repo / args.experiment
    output_dir = args.output_dir if args.output_dir.is_absolute() else repo / args.output_dir
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError("output directory must be absent or empty")
    output_dir.mkdir(parents=True, exist_ok=True)
    transcripts_dir = output_dir / "transcripts"
    transcripts_dir.mkdir()

    inputs_doc = json.loads(inputs_path.read_text(encoding="utf-8"))
    inputs = validate_inputs(inputs_doc)
    selected = select_inputs(inputs, args.mode)
    if not selected:
        raise ValueError("selected trial input set is empty")

    candidate_ref = git_sha(repo, "HEAD")
    if candidate_ref == PROGRAM_BASELINE:
        raise ValueError("candidate experiment HEAD must differ from immutable baseline")

    materializer = load_module(
        "runtime_experiment_materializer",
        repo / "tools" / "materialize_runtime_experiment.py",
    )
    with tempfile.TemporaryDirectory(prefix="runtime-ab-candidate-") as tmp:
        candidate_root = Path(tmp)
        materialized = materializer.materialize(repo, experiment_path, candidate_root)
        candidate_skill = candidate_root / "skill"
        candidate_entrypoint = (candidate_skill / "SKILL.md").read_text(encoding="utf-8")

        baseline_entrypoint = git_text(repo, PROGRAM_BASELINE, "skill/SKILL.md")
        api_key = os.environ.get(args.api_key_env, "")
        client = OpenAICompatibleClient(
            base_url=args.api_base_url,
            api_key=api_key,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            timeout=args.timeout,
        )

        toolset_fp = fingerprint(tool_definitions())
        settings = {
            "temperature": args.temperature,
            "max_tokens": args.max_tokens,
            "max_turns": args.max_turns,
            "tool_choice": "auto",
            "api_protocol": "openai-compatible-chat-completions-tools",
        }
        settings_fp = fingerprint(settings)

        runs: list[dict] = []
        case_seen = defaultdict(int)
        for item in selected:
            case_index = case_seen[item["case_id"]]
            case_seen[item["case_id"]] += 1
            order = ["baseline", "candidate"] if case_index % 2 == 0 else ["candidate", "baseline"]
            input_fp = fingerprint(model_visible_input(item))
            for position, representation in enumerate(order, start=1):
                if representation == "baseline":
                    entrypoint = baseline_entrypoint
                    read_reference = lambda path, _repo=repo: git_text(
                        _repo, PROGRAM_BASELINE, f"skill/{path}"
                    )
                else:
                    entrypoint = candidate_entrypoint
                    read_reference = lambda path, _root=candidate_skill: (
                        _root / path
                    ).read_text(encoding="utf-8")

                observed, transcript = run_one(
                    client=client,
                    item=item,
                    entrypoint=entrypoint,
                    read_reference=read_reference,
                    representation=representation,
                    order=position,
                    max_turns=args.max_turns,
                )
                run_id = f"{item['input_id']}-{representation}"
                transcript_path = transcripts_dir / f"{run_id}.json"
                transcript.update({
                    "run_id": run_id,
                    "candidate_ref": candidate_ref,
                    "baseline_ref": PROGRAM_BASELINE,
                    "model_id": args.model,
                    "model_version": args.model_version,
                    "settings_fingerprint": settings_fp,
                    "toolset_fingerprint": toolset_fp,
                    "candidate_entrypoint_sha256": materialized["candidate_entrypoint_sha256"],
                })
                transcript_path.write_text(
                    json.dumps(transcript, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
                runs.append({
                    "run_id": run_id,
                    "pair_id": item["input_id"],
                    "case_id": item["case_id"],
                    "input_fingerprint": input_fp,
                    "representation": representation,
                    "order": position,
                    "transcript_ref": f"artifact://transcripts/{transcript_path.name}",
                    "observed": observed,
                })
                # Avoid accidental burst behavior on hosted endpoints without making timing a metric.
                time.sleep(0.2)

    trials = {
        "schema_version": 1,
        "suite_id": "lossless-runtime-representation-v1",
        "evidence_kind": "actual-model-runtime-ab",
        "baseline_representation": {
            "label": "v1.2.2-baseline",
            "ref": PROGRAM_BASELINE,
        },
        "candidate_representation": {
            "label": f"decision-frame-v1@{candidate_ref[:12]}",
            "ref": candidate_ref,
        },
        "runtime_identity": {
            "model_id": args.model,
            "model_version": args.model_version,
            "settings_fingerprint": settings_fp,
            "toolset_fingerprint": toolset_fp,
        },
        "runs": runs,
    }
    trials_path = output_dir / "actual-model-trials.json"
    trials_path.write_text(
        json.dumps(trials, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    manifest = {
        "schema_version": 1,
        "experiment_id": "decision-frame-v1",
        "mode": args.mode,
        "baseline_ref": PROGRAM_BASELINE,
        "candidate_ref": candidate_ref,
        "input_file_sha256": hashlib.sha256(inputs_path.read_bytes()).hexdigest(),
        "settings": settings,
        "settings_fingerprint": settings_fp,
        "toolset_fingerprint": toolset_fp,
        "run_count": len(runs),
        "pair_count": len(runs) // 2,
        "private_chain_of_thought_recorded": False,
        "selection_proof_eligible": args.mode == "full",
    }
    (output_dir / "trial-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
