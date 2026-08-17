#!/usr/bin/env python3
"""Repository-local structural validator for GitHub Project Orchestrator."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

REQUIRED_RUNTIME_PATHS = (
    "SKILL.md",
    "agents/openai.yaml",
    "assets/icon.svg",
    "references/authority-gates.md",
    "references/continuity.md",
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
