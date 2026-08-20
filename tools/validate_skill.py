#!/usr/bin/env python3
"""Repository-local structural and traceability validator for GitHub Project Orchestrator."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import Counter
from pathlib import Path

REQUIRED_RUNTIME_PATHS = (
    "SKILL.md",
    "agents/openai.yaml",
    "assets/icon.svg",
    "references/authority-gates.md",
    "references/continuity.md",
    "references/engineering-quality.md",
    "references/eval-scenarios.md",
    "references/governance.md",
    "references/master-cycle.md",
    "references/release.md",
    "references/review-integration.md",
    "references/task-contract.md",
    "references/worker-protocol.md",
    "scripts/contract_check.py",
    "scripts/repo_preflight.py",
)
REQUIRED_DIRECT_ROUTER_TARGETS = tuple(
    path for path in REQUIRED_RUNTIME_PATHS if path.startswith("references/")
)

FRONTMATTER_RE = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)
LINK_RE = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)")
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
EVAL_HEADING_RE = re.compile(r"^###\s+([A-Z]+)\.\s+", re.MULTILINE)
PROJECT_GOAL_ROW_RE = re.compile(r"^\|\s*`(G\d{2})`(?:\s+[^|]*)?\s*\|", re.MULTILINE)
GOAL_ROW_RE = re.compile(
    r"^\|\s*`(?P<goal>G\d{2})`(?:\s+[^|]*)?\s*\|\s*(?P<rules>.*?)\s*\|\s*(?P<evals>.*?)\s*\|\s*(?P<coverage>.*?)\s*\|\s*$",
    re.MULTILINE,
)
RULE_ROW_RE = re.compile(
    r"^\|\s*`(?P<rule>[A-Z0-9]+(?:-[A-Z0-9]+)+)`\s*\|\s*(?P<guarantee>.*?)\s*\|\s*(?P<owner>.*?)\s*\|\s*(?P<sources>.*?)\s*\|\s*(?P<evals>.*?)\s*\|\s*$",
    re.MULTILINE,
)
INLINE_RULE_RE = re.compile(r"`([A-Z0-9]+(?:-[A-Z0-9]+)+)`")
STATE_TOKEN_RE = re.compile(
    r"\b(?P<namespace>TaskState|WorkerStatus|WriteState|DeliveryState|MasterBoundary)\.(?P<token>[A-Z][A-Z0-9_]*)\b"
)
STATE_ENUMS = {
    "TaskState": {
        "DRAFT",
        "BLOCKED",
        "READY",
        "IN_PROGRESS",
        "IN_REVIEW",
        "CHANGES_REQUESTED",
        "INTEGRATION_READY",
        "INTEGRATED",
        "CANCELLED",
        "SUPERSEDED",
        "ROLLED_BACK",
    },
    "WorkerStatus": {
        "STALE_ASSIGNMENT",
        "MATERIAL_DECISION_REQUIRED",
        "SCOPE_CHANGE_REQUIRED",
        "ENVIRONMENT_MISMATCH",
        "BLOCKED",
        "READY_FOR_REVIEW",
    },
    "WriteState": {"KNOWN", "UNKNOWN"},
    "DeliveryState": {"NOT_STARTED", "PENDING", "DELIVERED", "FAILED_OR_UNKNOWN"},
    "MasterBoundary": {
        "PROJECT_COMPLETE",
        "APPROVAL_REQUIRED",
        "MATERIAL_DECISION_REQUIRED",
        "BLOCKED",
        "RISK_ESCALATION",
        "MISSING_CAPABILITY",
        "NO_READY_WORK",
        "WRITE_OUTCOME_UNKNOWN",
        "USER_STOP",
    },
}


def fail(message: str) -> None:
    raise ValueError(message)


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        fail("SKILL.md is missing valid YAML-style frontmatter delimiters")

    values: dict[str, str] = {}
    for raw_line in match.group("body").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            fail(f"Unsupported frontmatter line: {raw_line!r}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in values:
            fail(f"Duplicate frontmatter key: {key}")
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1].replace('\\"', '"')
        values[key] = value

    if set(values) != {"name", "description"}:
        fail(f"SKILL.md frontmatter must contain only name and description; found {sorted(values)}")
    if not NAME_RE.fullmatch(values["name"]):
        fail(f"Invalid Skill name: {values['name']!r}")
    if not values["description"].strip():
        fail("Skill description must not be empty")
    if len(values["description"]) > 1024:
        fail("Skill description exceeds 1024 characters")
    return values


def validate_required_paths(skill_dir: Path) -> None:
    for relative in REQUIRED_RUNTIME_PATHS:
        path = skill_dir / relative
        if not path.is_file():
            fail(f"Missing required runtime file: {relative}")


def validate_markdown_links(skill_dir: Path) -> None:
    for markdown in skill_dir.rglob("*.md"):
        text = markdown.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            clean_target = target.split("#", 1)[0]
            if not clean_target:
                continue
            resolved = (markdown.parent / clean_target).resolve()
            try:
                resolved.relative_to(skill_dir.resolve())
            except ValueError as exc:
                raise ValueError(
                    f"Reference escapes Skill directory: {markdown.relative_to(skill_dir)} -> {target}"
                ) from exc
            if not resolved.exists():
                fail(f"Broken relative reference: {markdown.relative_to(skill_dir)} -> {target}")


def validate_direct_router(skill_dir: Path) -> None:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    direct_targets = {target.split("#", 1)[0] for target in LINK_RE.findall(text)}
    missing = sorted(set(REQUIRED_DIRECT_ROUTER_TARGETS) - direct_targets)
    if missing:
        fail(f"SKILL.md must directly route every required runtime reference; missing={missing}")


def validate_python(skill_dir: Path) -> None:
    for script in skill_dir.rglob("*.py"):
        source = script.read_text(encoding="utf-8")
        compile(source, str(script), "exec")


def eval_id_to_int(value: str) -> int:
    total = 0
    for char in value:
        total = total * 26 + (ord(char) - ord("A") + 1)
    return total


def int_to_eval_id(value: int) -> str:
    chars: list[str] = []
    while value > 0:
        value, remainder = divmod(value - 1, 26)
        chars.append(chr(ord("A") + remainder))
    return "".join(reversed(chars))


def parse_eval_ids(text: str) -> list[str]:
    return EVAL_HEADING_RE.findall(text)


def validate_eval_ids(text: str) -> set[str]:
    eval_ids = parse_eval_ids(text)
    if not eval_ids:
        fail("No evaluation scenario IDs found in references/eval-scenarios.md")
    duplicates = sorted(value for value, count in Counter(eval_ids).items() if count > 1)
    if duplicates:
        fail(f"Duplicate evaluation scenario IDs: {duplicates}")

    numeric = sorted(eval_id_to_int(value) for value in eval_ids)
    expected = set(range(1, numeric[-1] + 1))
    actual = set(numeric)
    missing = [int_to_eval_id(value) for value in sorted(expected - actual)]
    if missing:
        fail(f"Evaluation scenario ID gaps detected: {missing}")
    return set(eval_ids)


def parse_eval_anchors(cell: str, context: str) -> set[str]:
    values = [part.strip().strip("`") for part in cell.split(",") if part.strip()]
    if not values:
        fail(f"{context} must include at least one evaluation anchor")
    invalid = [value for value in values if not re.fullmatch(r"[A-Z]+", value)]
    if invalid:
        fail(f"{context} contains invalid evaluation anchor syntax: {invalid}")
    return set(values)


def validate_traceability(repo_root: Path, skill_dir: Path) -> None:
    rule_map_path = repo_root / "design" / "RULE-MAP.md"
    goal_map_path = repo_root / "design" / "GOAL-MAP.md"
    project_spec_path = repo_root / "docs" / "PROJECT-SPEC.md"
    eval_path = skill_dir / "references" / "eval-scenarios.md"
    required = (rule_map_path, goal_map_path, project_spec_path, eval_path)
    missing_files = [str(path.relative_to(repo_root)) for path in required if not path.is_file()]
    if missing_files:
        fail(f"Traceability source files are missing: {missing_files}")

    eval_ids = validate_eval_ids(eval_path.read_text(encoding="utf-8"))

    rule_text = rule_map_path.read_text(encoding="utf-8")
    rule_matches = list(RULE_ROW_RE.finditer(rule_text))
    if not rule_matches:
        fail("No canonical Rule rows found in design/RULE-MAP.md")
    rule_ids = [match.group("rule") for match in rule_matches]
    duplicate_rules = sorted(value for value, count in Counter(rule_ids).items() if count > 1)
    if duplicate_rules:
        fail(f"Duplicate canonical Rule rows/owners in design/RULE-MAP.md: {duplicate_rules}")

    rule_id_set = set(rule_ids)
    for match in rule_matches:
        rule_id = match.group("rule")
        owner = match.group("owner").strip().strip("`").strip()
        if not owner:
            fail(f"Rule {rule_id} is missing a canonical owner")
        anchors = parse_eval_anchors(match.group("evals"), f"Rule {rule_id}")
        missing_anchors = sorted(anchors - eval_ids, key=eval_id_to_int)
        if missing_anchors:
            fail(f"Rule {rule_id} references missing evaluation IDs: {missing_anchors}")

    project_goal_ids = PROJECT_GOAL_ROW_RE.findall(project_spec_path.read_text(encoding="utf-8"))
    duplicate_project_goals = sorted(value for value, count in Counter(project_goal_ids).items() if count > 1)
    if duplicate_project_goals:
        fail(f"Duplicate canonical Goal IDs in docs/PROJECT-SPEC.md: {duplicate_project_goals}")
    if not project_goal_ids:
        fail("No canonical Goal IDs found in docs/PROJECT-SPEC.md")

    goal_text = goal_map_path.read_text(encoding="utf-8")
    goal_matches = list(GOAL_ROW_RE.finditer(goal_text))
    if not goal_matches:
        fail("No Goal mapping rows found in design/GOAL-MAP.md")
    goal_ids = [match.group("goal") for match in goal_matches]
    duplicate_goal_rows = sorted(value for value, count in Counter(goal_ids).items() if count > 1)
    if duplicate_goal_rows:
        fail(f"Duplicate Goal rows in design/GOAL-MAP.md: {duplicate_goal_rows}")

    project_goal_set = set(project_goal_ids)
    goal_id_set = set(goal_ids)
    missing_goal_rows = sorted(project_goal_set - goal_id_set)
    unknown_goal_rows = sorted(goal_id_set - project_goal_set)
    if missing_goal_rows or unknown_goal_rows:
        fail(
            "Goal Map must match canonical project Goal IDs; "
            f"missing={missing_goal_rows}, unknown={unknown_goal_rows}"
        )

    mapped_rules: set[str] = set()
    for match in goal_matches:
        goal_id = match.group("goal")
        referenced_rules = set(INLINE_RULE_RE.findall(match.group("rules")))
        unknown_rules = sorted(referenced_rules - rule_id_set)
        if unknown_rules:
            fail(f"Goal {goal_id} references unknown Rule IDs: {unknown_rules}")
        mapped_rules.update(referenced_rules)

        anchors = parse_eval_anchors(match.group("evals"), f"Goal {goal_id}")
        missing_anchors = sorted(anchors - eval_ids, key=eval_id_to_int)
        if missing_anchors:
            fail(f"Goal {goal_id} references missing evaluation IDs: {missing_anchors}")

    orphan_rules = sorted(rule_id_set - mapped_rules)
    if orphan_rules:
        fail(f"Canonical Rule IDs are not mapped to any Goal in design/GOAL-MAP.md: {orphan_rules}")


def validate_state_tokens(skill_dir: Path) -> None:
    for markdown in [skill_dir / "SKILL.md", *sorted((skill_dir / "references").glob("*.md"))]:
        text = markdown.read_text(encoding="utf-8")
        for match in STATE_TOKEN_RE.finditer(text):
            namespace = match.group("namespace")
            token = match.group("token")
            if token not in STATE_ENUMS[namespace]:
                fail(
                    f"Unknown or legacy namespaced state token in {markdown.relative_to(skill_dir)}: "
                    f"{namespace}.{token}"
                )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_baseline(skill_dir: Path, manifest_path: Path) -> None:
    if not manifest_path.is_file():
        fail(f"Baseline manifest is missing: {manifest_path}")

    expected: dict[str, str] = {}
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, relative = line.split("  ", 1)
        expected[relative] = digest

    actual_paths = sorted(path for path in skill_dir.rglob("*") if path.is_file() and "__pycache__" not in path.parts)
    actual = {str(path.relative_to(skill_dir)): sha256_file(path) for path in actual_paths}
    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        changed = sorted(path for path in set(actual) & set(expected) if actual[path] != expected[path])
        fail(f"baseline drift detected; missing={missing}, extra={extra}, changed={changed}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_dir", type=Path)
    parser.add_argument(
        "--baseline-manifest",
        type=Path,
        help="Compare the supplied Skill source exactly against this SHA-256 baseline manifest.",
    )
    args = parser.parse_args()

    skill_dir = args.skill_dir.resolve()
    validate_required_paths(skill_dir)
    frontmatter = parse_frontmatter(skill_dir / "SKILL.md")
    validate_markdown_links(skill_dir)
    if args.baseline_manifest is None:
        validate_direct_router(skill_dir)
        validate_state_tokens(skill_dir)
        validate_traceability(skill_dir.parent, skill_dir)
    validate_python(skill_dir)
    if args.baseline_manifest is not None:
        validate_baseline(skill_dir, args.baseline_manifest.resolve())
    print(f"Valid Skill: {frontmatter['name']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, SyntaxError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
