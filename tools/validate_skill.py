#!/usr/bin/env python3
"""Structural and goal-traceability validator for GitHub Project Orchestrator."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILL = ROOT / "skill"

RUNTIME_REFERENCES = (
    "authority-gates.md",
    "continuity.md",
    "engineering-quality.md",
    "governance.md",
    "independent-review.md",
    "interface-specialist.md",
    "master-cycle.md",
    "relay-transport.md",
    "release.md",
    "review-integration.md",
    "task-contract.md",
    "worker-protocol.md",
)
REQUIRED_PATHS = (
    "SKILL.md",
    "agents/openai.yaml",
    "assets/icon.svg",
    *(f"references/{name}" for name in RUNTIME_REFERENCES),
    "scripts/repo_preflight.py",
)

FRONTMATTER_RE = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)
LINK_RE = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)")
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PROJECT_GOAL_RE = re.compile(r"^\|\s*"+chr(96)+r"(G\d{2})"+chr(96)+r"\s*\|", re.MULTILINE)
GOAL_ROW_RE = re.compile(
    r"^\|\s*"+chr(96)+r"(?P<goal>G\d{2})"+chr(96)+r"[^|]*\|\s*(?P<rules>.*?)\s*\|\s*(?P<evals>.*?)\s*\|\s*(?P<coverage>.*?)\s*\|\s*$",
    re.MULTILINE,
)
RULE_ROW_RE = re.compile(
    r"^\|\s*"+chr(96)+r"(?P<rule>[A-Z0-9]+(?:-[A-Z0-9]+)+)"+chr(96)+r"\s*\|\s*(?P<guarantee>.*?)\s*\|\s*(?P<owner>.*?)\s*\|\s*(?P<sources>.*?)\s*\|\s*(?P<evals>.*?)\s*\|\s*$",
    re.MULTILINE,
)
INLINE_RULE_RE = re.compile(chr(96)+r"([A-Z0-9]+(?:-[A-Z0-9]+)+)"+chr(96))
EVAL_HEADING_RE = re.compile(r"^###\s+([A-Z]+)\.\s+", re.MULTILINE)


def fail(message: str) -> None:
    raise ValueError(message)


def parse_frontmatter(path: Path) -> dict[str, str]:
    match = FRONTMATTER_RE.match(path.read_text(encoding="utf-8"))
    if not match:
        fail("SKILL.md is missing YAML-style frontmatter")
    values: dict[str, str] = {}
    for raw in match.group("body").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            fail(f"Unsupported frontmatter line: {raw!r}")
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if key in values:
            fail(f"Duplicate frontmatter key: {key}")
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1].replace(r'\"', '"')
        values[key] = value
    if set(values) != {"name", "description"}:
        fail(f"SKILL.md frontmatter must contain only name and description: {sorted(values)}")
    if not NAME_RE.fullmatch(values["name"]):
        fail(f"Invalid Skill name: {values['name']!r}")
    if not values["description"] or len(values["description"]) > 1024:
        fail("Skill description must be non-empty and at most 1024 characters")
    return values


def validate_paths(skill_dir: Path) -> None:
    missing = [p for p in REQUIRED_PATHS if not (skill_dir / p).is_file()]
    if missing:
        fail(f"Missing required runtime files: {missing}")


def validate_links(skill_dir: Path) -> None:
    for markdown in skill_dir.rglob("*.md"):
        for target in LINK_RE.findall(markdown.read_text(encoding="utf-8")):
            relative = target.split("#", 1)[0]
            if not relative:
                continue
            resolved = (markdown.parent / relative).resolve()
            try:
                resolved.relative_to(skill_dir.resolve())
            except ValueError as exc:
                raise ValueError(
                    f"Reference escapes Skill directory: {markdown.relative_to(skill_dir)} -> {target}"
                ) from exc
            if not resolved.exists():
                fail(f"Broken relative reference: {markdown.relative_to(skill_dir)} -> {target}")


def validate_router(skill_dir: Path) -> None:
    kernel = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    linked = {target.split("#", 1)[0] for target in LINK_RE.findall(kernel)}
    required = {f"references/{name}" for name in RUNTIME_REFERENCES}
    missing = sorted(required - linked)
    if missing:
        fail(f"SKILL.md must directly route every runtime reference: {missing}")


def validate_python(skill_dir: Path) -> None:
    for script in skill_dir.rglob("*.py"):
        compile(script.read_text(encoding="utf-8"), str(script), "exec")


def parse_csv_ids(cell: str, pattern: str, label: str) -> set[str]:
    values = {part.strip().strip(chr(96)) for part in cell.split(",") if part.strip()}
    invalid = sorted(value for value in values if not re.fullmatch(pattern, value))
    if invalid:
        fail(f"{label} contains invalid identifiers: {invalid}")
    return values


def validate_traceability(repo_root: Path) -> None:
    project = (repo_root / "docs/PROJECT-SPEC.md").read_text(encoding="utf-8")
    goal_map = (repo_root / "design/GOAL-MAP.md").read_text(encoding="utf-8")
    rule_map = (repo_root / "design/RULE-MAP.md").read_text(encoding="utf-8")
    eval_text = (repo_root / "design/EVAL-SCENARIOS.md").read_text(encoding="utf-8")

    project_goals = PROJECT_GOAL_RE.findall(project)
    if project_goals != [f"G{i:02d}" for i in range(1, 17)]:
        fail(f"PROJECT-SPEC canonical goals must be exactly G01-G16: {project_goals}")

    eval_ids = EVAL_HEADING_RE.findall(eval_text)
    if not eval_ids or len(eval_ids) != len(set(eval_ids)):
        fail("Evaluation scenario IDs must be present and unique")
    eval_set = set(eval_ids)

    rule_rows = list(RULE_ROW_RE.finditer(rule_map))
    if not rule_rows:
        fail("RULE-MAP contains no canonical rules")
    rule_ids = [row.group("rule") for row in rule_rows]
    if len(rule_ids) != len(set(rule_ids)):
        fail("RULE-MAP contains duplicate Rule IDs")
    rule_set = set(rule_ids)

    runtime_names = {"SKILL.md", *RUNTIME_REFERENCES}
    anchored_evals: set[str] = set()
    for row in rule_rows:
        owner = row.group("owner").strip().strip(chr(96))
        if owner not in runtime_names:
            fail(f"Rule {row.group('rule')} has unknown runtime owner: {owner}")
        anchors = parse_csv_ids(row.group("evals"), r"[A-Z]+", f"Rule {row.group('rule')}")
        unknown = sorted(anchors - eval_set)
        if unknown:
            fail(f"Rule {row.group('rule')} references missing evals: {unknown}")
        anchored_evals.update(anchors)

    goal_rows = list(GOAL_ROW_RE.finditer(goal_map))
    goal_ids = [row.group("goal") for row in goal_rows]
    if goal_ids != project_goals:
        fail(f"GOAL-MAP must contain G01-G16 in canonical order: {goal_ids}")

    mapped_rules: set[str] = set()
    for row in goal_rows:
        rules = set(INLINE_RULE_RE.findall(row.group("rules")))
        if not rules:
            fail(f"{row.group('goal')} maps no canonical rules")
        unknown_rules = sorted(rules - rule_set)
        if unknown_rules:
            fail(f"{row.group('goal')} references unknown rules: {unknown_rules}")
        mapped_rules.update(rules)

        anchors = parse_csv_ids(row.group("evals"), r"[A-Z]+", row.group("goal"))
        unknown_evals = sorted(anchors - eval_set)
        if unknown_evals:
            fail(f"{row.group('goal')} references missing evals: {unknown_evals}")
        anchored_evals.update(anchors)

    orphan_rules = sorted(rule_set - mapped_rules)
    if orphan_rules:
        fail(f"Canonical rules not mapped to any goal: {orphan_rules}")

    unanchored_evals = sorted(eval_set - anchored_evals)
    if unanchored_evals:
        fail(f"Evaluation scenarios not anchored by Rule/Goal maps: {unanchored_evals}")


def main() -> int:
    skill_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_SKILL.resolve()
    if len(sys.argv) > 2:
        fail("Usage: validate_skill.py [skill_dir]")
    validate_paths(skill_dir)
    frontmatter = parse_frontmatter(skill_dir / "SKILL.md")
    validate_links(skill_dir)
    validate_router(skill_dir)
    validate_python(skill_dir)
    validate_traceability(skill_dir.parent)
    print(f"Valid Skill: {frontmatter['name']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, SyntaxError, ValueError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
