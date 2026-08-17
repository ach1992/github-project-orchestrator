#!/usr/bin/env python3
"""Validate minimum Task Contract and optional Worker assignment fields."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REQUIRED_SECTIONS = ("Goal", "Scope", "Acceptance", "Validation", "Dependencies", "Risk / Release")
WORKER_REQUIRED_FIELDS = (
    "Assignment ID",
    "Contract Revision",
    "Base SHA",
    "Assigned Branch",
    "Integration Target",
    "Worker",
    "Assignment Status",
    "Task Risk",
)
VALID_AUTHORITIES = {"MANAGED", "AUTONOMOUS_WITH_GATES"}
VALID_COORDINATION_BASELINES = {"LIGHTWEIGHT", "STANDARD"}
VALID_ASSURANCE_LEVELS = {"NORMAL", "HIGH_ASSURANCE"}
VALID_LEGACY_PROFILES = {"LIGHTWEIGHT", "STANDARD", "HIGH_ASSURANCE"}
VALID_RISKS = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
VALID_DELIVERY_REQUIREMENTS = {"INTEGRATION_ONLY", "DELIVERY_REQUIRED"}
VALID_DELIVERY_STATES = {"NOT_STARTED", "PENDING", "DELIVERED", "FAILED_OR_UNKNOWN"}
FULL_SHA_RE = re.compile(r"(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})")
PLACEHOLDER_RE = re.compile(r"^\s*(?:<[^<>]+>|\{[^{}]+\}|\[replace[^\]]*\]|\.\.\.|tbd|tba|todo|unknown|none|null|n/?a)\s*$", re.IGNORECASE)
FENCE_OPEN_RE = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})(?:[^\r\n]*)$")
MARKDOWN_ITEM_PREFIX_RE = re.compile(r"^\s*(?:[-*+]\s+)?(?:\[[ xX]\]\s*)?")
SECTION_LABEL_RE = {
    "Scope": re.compile(r"^(?:In|Out)\s*:\s*", re.IGNORECASE),
    "Risk / Release": re.compile(r"^(?:Risk|Release)\s*:\s*", re.IGNORECASE),
}
MARKDOWN_SCAFFOLD_RE = re.compile(r"^[\s`*_~#>|+\-=:.\[\](){}]*$")


def read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def strip_fenced_code(text: str) -> str:
    """Remove fenced code/example blocks so templates are not parsed as contracts."""
    output: list[str] = []
    fence_char: str | None = None
    fence_len = 0

    for line in text.splitlines(keepends=True):
        stripped = line.rstrip("\r\n")
        match = FENCE_OPEN_RE.match(stripped)
        if fence_char is None:
            if match:
                marker = match.group(1)
                fence_char = marker[0]
                fence_len = len(marker)
                output.append("\n" if line.endswith(("\n", "\r")) else "")
            else:
                output.append(line)
            continue

        close_match = re.match(rf"^[ \t]{{0,3}}{re.escape(fence_char)}{{{fence_len},}}[ \t]*$", stripped)
        if close_match:
            fence_char = None
            fence_len = 0
        output.append("\n" if line.endswith(("\n", "\r")) else "")

    return "".join(output)


def strip_html_comments(text: str) -> str:
    """Remove HTML comments while preserving line structure and inline code spans."""
    output: list[str] = []
    index = 0
    in_comment = False

    while index < len(text):
        if in_comment:
            if text.startswith("-->", index):
                output.extend("   ")
                index += 3
                in_comment = False
                continue
            char = text[index]
            output.append(char if char in "\r\n" else " ")
            index += 1
            continue

        if text[index] == "`":
            run_end = index + 1
            while run_end < len(text) and text[run_end] == "`":
                run_end += 1
            run_len = run_end - index
            marker = "`" * run_len
            close = re.search(rf"(?<!`){re.escape(marker)}(?!`)", text[run_end:])
            if close:
                close_end = run_end + close.end()
                output.append(text[index:close_end])
                index = close_end
                continue
            output.append(text[index:run_end])
            index = run_end
            continue

        if text.startswith("<!--", index):
            output.extend("    ")
            index += 4
            in_comment = True
            continue

        output.append(text[index])
        index += 1

    return "".join(output)


def section_bodies(text: str, title: str) -> list[str]:
    pattern = re.compile(rf"(?ms)^##\s+{re.escape(title)}\s*$\n(.*?)(?=^##\s+|\Z)")
    return [match.group(1).strip() for match in pattern.finditer(text)]


def field_values(text: str, field: str) -> list[str]:
    pattern = re.compile(rf"(?mi)^(?:[-*][ \t]*)?{re.escape(field)}[ \t]*:[ \t]*([^\r\n]*)\r?$")
    return [match.group(1).strip() for match in pattern.finditer(text)]


def unique_field(text: str, field: str, errors: list[str]) -> tuple[bool, str | None]:
    values = field_values(text, field)
    if len(values) > 1:
        errors.append(f"Duplicate Worker assignment field: {field}")
        return True, None
    if not values:
        return False, None
    return True, values[0]


def validate_local_branch_name(value: str, field: str) -> tuple[str | None, str | None]:
    """Return a deterministic local branch identity without repository-dependent shorthand expansion."""
    cleaned = value.strip()
    if not cleaned:
        return None, f"{field} is incomplete."
    if cleaned.startswith("refs/remotes/"):
        return None, f"{field} must identify a local branch, not a remote-tracking ref."
    if cleaned.startswith("refs/heads/"):
        normalized = cleaned.removeprefix("refs/heads/")
    elif cleaned.startswith("refs/"):
        return None, f"{field} must identify a local branch under refs/heads/, not another Git ref namespace."
    else:
        normalized = cleaned

    if not normalized:
        return None, f"{field} is incomplete."
    if normalized.startswith("-") or normalized == "HEAD":
        return None, f"{field} must be a normal local Git branch name, not a revision/pseudo-ref shorthand."

    env = os.environ.copy()
    for key in list(env):
        if key.startswith("GIT_TRACE"):
            env.pop(key, None)
    env["GIT_TRACE2"] = "0"
    env["GIT_TRACE2_EVENT"] = "0"
    env["GIT_TRACE2_PERF"] = "0"

    try:
        result = subprocess.run(
            ["git", "check-ref-format", f"refs/heads/{normalized}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            env=env,
        )
    except FileNotFoundError:
        return None, f"Git executable is required to validate {field} identity."

    if result.returncode != 0:
        return None, f"{field} must be a valid local Git branch identity, not a filesystem/worktree path, revision shorthand, or invalid ref name."
    return normalized, None


def normalize_assigned_branch_identity(value: str) -> tuple[str | None, str | None]:
    return validate_local_branch_name(value, "Assigned Branch")


def normalize_integration_target_identity(value: str) -> tuple[str | None, str | None]:
    cleaned = value.strip()
    if cleaned.startswith("refs/remotes/"):
        return None, (
            "Integration Target must use canonical repository branch identity, not a remote-tracking ref; "
            "use a simple name such as `main` or `refs/heads/<branch>`."
        )
    if not cleaned.startswith("refs/heads/") and "/" in cleaned:
        return None, (
            "Integration Target branch names containing `/` must use canonical `refs/heads/<branch>` form; "
            "remote-tracking aliases such as `origin/main` are not valid Integration Target identity."
        )
    return validate_local_branch_name(cleaned, "Integration Target")


def is_placeholder(value: str | None) -> bool:
    if value is None or not value.strip():
        return True
    cleaned = value.strip().strip("`*_ ")
    return bool(PLACEHOLDER_RE.fullmatch(cleaned))


def valid_full_sha(value: str) -> bool:
    return bool(FULL_SHA_RE.fullmatch(value)) and any(ch != "0" for ch in value.lower())


def section_is_placeholder_only(body: str, section: str) -> bool:
    """Reject untouched template bodies without judging subjective prose quality."""
    for raw_line in body.splitlines():
        value = MARKDOWN_ITEM_PREFIX_RE.sub("", raw_line).strip()
        if not value:
            continue
        label_re = SECTION_LABEL_RE.get(section)
        if label_re:
            value = label_re.sub("", value, count=1).strip()
        if not value or MARKDOWN_SCAFFOLD_RE.fullmatch(value):
            continue
        if section == "Dependencies" and value.lower() == "none":
            return False
        if not is_placeholder(value):
            return False
    return True


def require_value(present: bool, value: str | None, field: str, errors: list[str]) -> None:
    if not present or is_placeholder(value):
        errors.append(f"Missing or placeholder Worker assignment field: {field}")


def resolve_alias(
    parsed: str,
    canonical: str,
    legacy: str,
    errors: list[str],
) -> tuple[str | None, bool]:
    canonical_present, canonical_value = unique_field(parsed, canonical, errors)
    legacy_present, legacy_value = unique_field(parsed, legacy, errors)
    if canonical_present and legacy_present:
        errors.append(f"Ambiguous Worker assignment fields: use {canonical} or legacy {legacy}, not both.")
        return None, True
    if canonical_present:
        require_value(True, canonical_value, canonical, errors)
        return canonical_value, False
    if legacy_present:
        require_value(True, legacy_value, legacy, errors)
        return legacy_value, False
    errors.append(f"Missing Worker assignment field: {canonical} (legacy {legacy} is accepted during migration).")
    return None, False


def resolve_coordination_and_assurance(parsed: str, errors: list[str]) -> tuple[str | None, str | None]:
    baseline_present, baseline = unique_field(parsed, "Coordination Baseline", errors)
    assurance_present, assurance = unique_field(parsed, "Assurance Level", errors)
    profile_present, profile = unique_field(parsed, "Operating Profile", errors)

    if baseline_present and assurance_present:
        require_value(True, baseline, "Coordination Baseline", errors)
        require_value(True, assurance, "Assurance Level", errors)
        if profile_present:
            errors.append(
                "Ambiguous Worker assignment fields: canonical Coordination Baseline + Assurance Level must not be combined with legacy Operating Profile."
            )
        return baseline, assurance

    if baseline_present and not assurance_present:
        require_value(True, baseline, "Coordination Baseline", errors)
        if not profile_present or is_placeholder(profile):
            errors.append("Missing Worker assignment field: Assurance Level.")
            return baseline, None
        profile_upper = profile.upper()
        if profile_upper == "HIGH_ASSURANCE":
            return baseline, "HIGH_ASSURANCE"
        errors.append(
            "Legacy Operating Profile may accompany canonical Coordination Baseline only when it is HIGH_ASSURANCE; otherwise persist canonical Assurance Level."
        )
        return baseline, None

    if assurance_present:
        require_value(True, assurance, "Assurance Level", errors)
        errors.append("Missing Worker assignment field: Coordination Baseline.")
        if profile_present:
            errors.append(
                "Legacy Operating Profile cannot supply a missing baseline when canonical Assurance Level is already persisted; persist Coordination Baseline explicitly."
            )
        return None, assurance

    if not profile_present or is_placeholder(profile):
        errors.append(
            "Missing Worker assignment fields: Coordination Baseline + Assurance Level (legacy Operating Profile is accepted when lossless)."
        )
        return None, None

    profile_upper = profile.upper()
    if profile_upper == "LIGHTWEIGHT":
        return "LIGHTWEIGHT", "NORMAL"
    if profile_upper == "STANDARD":
        return "STANDARD", "NORMAL"
    if profile_upper == "HIGH_ASSURANCE":
        errors.append(
            "Legacy Operating Profile HIGH_ASSURANCE is ambiguous without a persisted Coordination Baseline; do not guess LIGHTWEIGHT or STANDARD."
        )
        return None, "HIGH_ASSURANCE"
    return None, None


def validate(text: str, level: str, worker: bool, issue_identity: str | None = None) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    parsed = strip_html_comments(strip_fenced_code(text))

    require_full_contract = worker or level != "trivial"
    if not require_full_contract:
        if not parsed.strip():
            errors.append("Trivial work still needs a discoverable change description or PR context outside fenced examples.")
    else:
        section_map: dict[str, list[str]] = {}
        for section in REQUIRED_SECTIONS:
            bodies = section_bodies(parsed, section)
            section_map[section] = bodies
            if not bodies:
                errors.append(f"Missing section: ## {section}")
            elif len(bodies) > 1:
                errors.append(f"Duplicate canonical section: ## {section}")
            elif not bodies[0]:
                errors.append(f"Empty section: ## {section}")
            elif section_is_placeholder_only(bodies[0], section):
                errors.append(f"Placeholder-only section: ## {section}")

        acceptance_bodies = section_map.get("Acceptance", [])
        acceptance = acceptance_bodies[0] if len(acceptance_bodies) == 1 else ""
        if acceptance and "[ ]" not in acceptance and "[x]" not in acceptance.lower():
            warnings.append("Acceptance has no markdown checklist item; ensure criteria remain objectively verifiable.")

    if worker:
        issue_values = field_values(parsed, "Issue")
        if len(issue_values) > 1:
            errors.append("Duplicate Worker assignment field: Issue")
            issue = None
        elif issue_values:
            issue = issue_values[0] if issue_values[0].strip() else issue_identity
        else:
            issue = issue_identity
        if is_placeholder(issue):
            errors.append("Missing Worker assignment Issue/work-item identity; include `Issue:` or pass --issue.")

        values: dict[str, str | None] = {}
        for field in WORKER_REQUIRED_FIELDS:
            present, value = unique_field(parsed, field, errors)
            values[field] = value
            require_value(present, value, field, errors)

        start_head, _ = resolve_alias(parsed, "Start HEAD", "Expected Starting HEAD", errors)
        project_authority, _ = resolve_alias(parsed, "Project Authority", "Authority", errors)
        coordination_baseline, assurance_level = resolve_coordination_and_assurance(parsed, errors)

        checkpoint_present, checkpoint_head = unique_field(parsed, "Checkpoint HEAD", errors)
        if checkpoint_present and is_placeholder(checkpoint_head):
            errors.append("Checkpoint HEAD must be omitted when not applicable; if present it must be a non-placeholder full commit SHA.")

        scoped_auth_present, scoped_authorization = unique_field(parsed, "Scoped Authorization", errors)
        if scoped_auth_present and is_placeholder(scoped_authorization) and (scoped_authorization or "").strip().lower() != "none":
            errors.append("Scoped Authorization must be a concrete grant or `none` when the field is present.")

        revision = values["Contract Revision"]
        if revision and not is_placeholder(revision) and not re.fullmatch(r"[1-9]\d*", revision):
            errors.append("Contract Revision must be a positive integer for Worker assignments.")

        sha_fields = (("Base SHA", values["Base SHA"]), ("Start HEAD", start_head))
        if checkpoint_present:
            sha_fields += (("Checkpoint HEAD", checkpoint_head),)
        for field, value in sha_fields:
            if value and not is_placeholder(value) and not valid_full_sha(value):
                errors.append(f"{field} must be a non-zero full Git commit SHA (40 or 64 hexadecimal characters).")

        assigned_branch = values["Assigned Branch"]
        integration_target = values["Integration Target"]
        assigned_identity = None
        target_identity = None
        if assigned_branch and not is_placeholder(assigned_branch):
            assigned_identity, assigned_error = normalize_assigned_branch_identity(assigned_branch)
            if assigned_error:
                errors.append(assigned_error)
        if integration_target and not is_placeholder(integration_target):
            target_identity, target_error = normalize_integration_target_identity(integration_target)
            if target_error:
                errors.append(target_error)
        if assigned_identity and target_identity and assigned_identity == target_identity:
            errors.append("Assigned Branch must differ from Integration Target; Workers do not integrate directly.")

        assignment_status = values["Assignment Status"]
        if assignment_status and not is_placeholder(assignment_status) and assignment_status.upper() != "ACTIVE":
            errors.append("Assignment Status must be ACTIVE for a dispatch-ready Worker assignment.")

        if project_authority and not is_placeholder(project_authority) and project_authority.upper() not in VALID_AUTHORITIES:
            errors.append("Project Authority for an implementation Worker must be MANAGED or AUTONOMOUS_WITH_GATES.")

        if coordination_baseline and not is_placeholder(coordination_baseline) and coordination_baseline.upper() not in VALID_COORDINATION_BASELINES:
            errors.append("Coordination Baseline must be LIGHTWEIGHT or STANDARD.")

        if assurance_level and not is_placeholder(assurance_level) and assurance_level.upper() not in VALID_ASSURANCE_LEVELS:
            errors.append("Assurance Level must be NORMAL or HIGH_ASSURANCE.")

        profile_present, profile = unique_field(parsed, "Operating Profile", [])
        if profile_present and profile and not is_placeholder(profile) and profile.upper() not in VALID_LEGACY_PROFILES:
            errors.append("Legacy Operating Profile must be LIGHTWEIGHT, STANDARD, or HIGH_ASSURANCE.")

        risk = values["Task Risk"]
        if risk and not is_placeholder(risk) and risk.upper() not in VALID_RISKS:
            errors.append("Task Risk must be LOW, MEDIUM, HIGH, or CRITICAL.")

        delivery_requirement_present, delivery_requirement = unique_field(parsed, "Delivery Requirement", errors)
        if delivery_requirement_present and not is_placeholder(delivery_requirement):
            if delivery_requirement.upper() not in VALID_DELIVERY_REQUIREMENTS:
                errors.append("Delivery Requirement must be INTEGRATION_ONLY or DELIVERY_REQUIRED.")

        delivery_target_present, delivery_target = unique_field(parsed, "Delivery Target", errors)
        if delivery_target_present and is_placeholder(delivery_target):
            errors.append("Delivery Target must be concrete when the field is present.")

        delivery_state_present, delivery_state = unique_field(parsed, "Delivery State", errors)
        if delivery_state_present and not is_placeholder(delivery_state):
            if delivery_state.upper() not in VALID_DELIVERY_STATES:
                errors.append("Delivery State must be NOT_STARTED, PENDING, DELIVERED, or FAILED_OR_UNKNOWN.")

    return {"ok": not errors, "level": level, "worker": worker, "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Contract markdown file, or - for stdin")
    parser.add_argument("--level", choices=("trivial", "substantive"), default="substantive")
    parser.add_argument("--worker", action="store_true", help="Require embedded Worker assignment identity fields")
    parser.add_argument("--issue", help="Issue/work-item identity when it is external to the contract text")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    try:
        result = validate(read_text(args.path), args.level, args.worker, args.issue)
    except OSError as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}), file=sys.stderr)
        return 2

    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
