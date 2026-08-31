#!/usr/bin/env python3
"""Deterministic isolation checks for the #52 runtime-dimension representation prototype."""
from __future__ import annotations

import io
import json
import re
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT_DIR = ROOT / "benchmarks" / "phase7" / "experiments" / "runtime-dimension-invariants-v2"
EXPERIMENT_PATH = EXPERIMENT_DIR / "experiment.json"
README_PATH = EXPERIMENT_DIR / "README.md"
ANALYSIS_PATH = EXPERIMENT_DIR / "OPERATIONAL-ANALYSIS.md"
SOURCE_REF = "9e584166008567d71591d2a03bf7da713d3664a4"
SEMANTIC_BASELINE_REF = "f98e8a242c720931e34aa7c4e8a799090e3d0495"
TARGET_PATHS = {
    "skill/SKILL.md",
    "skill/references/authority-gates.md",
}
DIRECT_REF_RE = re.compile(r"\((references/[A-Za-z0-9._/-]+\.md)\)")
STATE_RE = re.compile(
    r"\b(TaskState|WorkerStatus|WriteState|DeliveryState|MasterBoundary)\.([A-Z][A-Z0-9_]*)\b"
)


def git_bytes(*args: str) -> bytes:
    try:
        return subprocess.run(
            ["git", *args],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise AssertionError(f"git {' '.join(args)} failed") from exc


def git_text(ref: str, path: str) -> str:
    return git_bytes("show", f"{ref}:{path}").decode("utf-8")


def safe_extract_tar(data: bytes, destination: Path) -> None:
    destination = destination.resolve()
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:") as archive:
        for member in archive.getmembers():
            target = (destination / member.name).resolve()
            try:
                target.relative_to(destination)
            except ValueError as exc:
                raise AssertionError(f"unsafe archive path: {member.name}") from exc
            if member.issym() or member.islnk():
                raise AssertionError(f"experiment archive must not contain links: {member.name}")
        archive.extractall(destination)


def section(text: str, start: str, end: str) -> str:
    if text.count(start) != 1:
        raise AssertionError(f"source must contain start heading exactly once: {start}")
    if text.count(end) != 1:
        raise AssertionError(f"source must contain end heading exactly once: {end}")
    start_index = text.index(start)
    end_index = text.index(end)
    if start_index >= end_index:
        raise AssertionError(f"section headings out of order: {start} / {end}")
    return text[start_index:end_index]


def replace_section(source: str, start: str, end: str, candidate: str) -> str:
    source_section = section(source, start, end)
    if candidate.count(start) != 1 or not candidate.lstrip().startswith(start):
        raise AssertionError(f"candidate must begin with the configured start heading: {start}")
    if end in candidate:
        raise AssertionError(f"candidate must not include exclusive end heading: {end}")
    candidate = candidate.rstrip() + "\n\n"
    return source.replace(source_section, candidate, 1)


def word_count(text: str) -> int:
    return len(text.split())


def skill_paths(ref: str) -> list[str]:
    return [
        line
        for line in git_bytes("ls-tree", "-r", "--name-only", ref, "skill").decode("utf-8").splitlines()
        if line
    ]


def collect_states(root: Path) -> set[tuple[str, str]]:
    result: set[tuple[str, str]] = set()
    for path in [root / "SKILL.md", *sorted((root / "references").glob("*.md"))]:
        result.update(STATE_RE.findall(path.read_text(encoding="utf-8")))
    return result


def collect_source_states(ref: str) -> set[tuple[str, str]]:
    result: set[tuple[str, str]] = set()
    for path in skill_paths(ref):
        if path == "skill/SKILL.md" or (path.startswith("skill/references/") and path.endswith(".md")):
            result.update(STATE_RE.findall(git_text(ref, path)))
    return result


def write_source_file(ref: str, path: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(git_bytes("show", f"{ref}:{path}"))


def main() -> None:
    experiment = json.loads(EXPERIMENT_PATH.read_text(encoding="utf-8"))
    if experiment.get("schema_version") != 1:
        raise AssertionError("unsupported experiment schema_version")
    if experiment.get("experiment_id") != "runtime-dimension-invariants-v2":
        raise AssertionError("unexpected experiment_id")
    if experiment.get("source_ref") != SOURCE_REF:
        raise AssertionError("prototype source_ref drifted")
    if experiment.get("semantic_baseline_ref") != SEMANTIC_BASELINE_REF:
        raise AssertionError("semantic baseline drifted")
    if experiment.get("semantic_change_allowed") is not False:
        raise AssertionError("representation prototype must not allow semantic change")
    if experiment.get("canonical_runtime_changed_during_prototype") is not False:
        raise AssertionError("prototype must remain outside canonical runtime")

    resolved_source = git_bytes("rev-parse", f"{SOURCE_REF}^{{commit}}").decode("utf-8").strip()
    resolved_semantic = git_bytes("rev-parse", f"{SEMANTIC_BASELINE_REF}^{{commit}}").decode("utf-8").strip()
    if resolved_source != SOURCE_REF or resolved_semantic != SEMANTIC_BASELINE_REF:
        raise AssertionError("frozen prototype identity did not resolve exactly")
    git_bytes("merge-base", "--is-ancestor", SEMANTIC_BASELINE_REF, SOURCE_REF)
    git_bytes("merge-base", "--is-ancestor", SOURCE_REF, "HEAD")
    print("PASS frozen-prototype-identities")

    replacements = experiment.get("replacements")
    if not isinstance(replacements, list) or len(replacements) != 2:
        raise AssertionError("prototype must contain exactly two section replacements")
    if {item.get("path") for item in replacements} != TARGET_PATHS:
        raise AssertionError("prototype replacement scope drifted")

    with tempfile.TemporaryDirectory(prefix="gpo-dimension-experiment-") as temp_name:
        temp_root = Path(temp_name)
        archive = git_bytes("archive", "--format=tar", SOURCE_REF, "skill")
        safe_extract_tar(archive, temp_root)
        candidate_sections: dict[str, str] = {}
        source_sections: dict[str, str] = {}

        for replacement in replacements:
            if set(replacement) != {"path", "start_heading", "end_heading_exclusive", "candidate_section"}:
                raise AssertionError("replacement contract fields drifted")
            path = replacement["path"]
            start = replacement["start_heading"]
            end = replacement["end_heading_exclusive"]
            candidate_path = ROOT / replacement["candidate_section"]
            try:
                candidate_path.resolve().relative_to(ROOT.resolve())
            except ValueError as exc:
                raise AssertionError("candidate section escaped repository") from exc
            candidate = candidate_path.read_text(encoding="utf-8")
            source = git_text(SOURCE_REF, path)
            source_sections[path] = section(source, start, end)
            candidate_sections[path] = candidate.rstrip() + "\n\n"
            materialized = replace_section(source, start, end, candidate)
            destination = temp_root / path
            destination.write_text(materialized, encoding="utf-8")

        changed: set[str] = set()
        for path in skill_paths(SOURCE_REF):
            candidate_path = temp_root / path
            if not candidate_path.is_file():
                raise AssertionError(f"materialized runtime lost source path: {path}")
            if candidate_path.read_bytes() != git_bytes("show", f"{SOURCE_REF}:{path}"):
                changed.add(path)
        if changed != TARGET_PATHS:
            raise AssertionError(f"prototype changed unexpected runtime paths: {sorted(changed)}")
        print("PASS non-target-runtime-byte-identity")

        source_skill = git_text(SOURCE_REF, "skill/SKILL.md")
        candidate_skill = (temp_root / "skill" / "SKILL.md").read_text(encoding="utf-8")
        source_refs = sorted(set(DIRECT_REF_RE.findall(source_skill)))
        candidate_refs = sorted(set(DIRECT_REF_RE.findall(candidate_skill)))
        if candidate_refs != source_refs:
            raise AssertionError(
                f"direct runtime routing changed: source={source_refs} candidate={candidate_refs}"
            )
        if collect_states(temp_root / "skill") != collect_source_states(SOURCE_REF):
            raise AssertionError("state namespace/token surface changed")
        print("PASS routing-and-state-surface-unchanged")

        skill_section = candidate_sections["skill/SKILL.md"]
        required_skill_fragments = (
            "| Dimension | Values / responsibility | Stability / non-implication |",
            "`KEEP` until the actual assignment basis changes.",
            "`KEEP` until the actual authorization basis changes.",
            "Capability, environment, risk, coordination, or assurance never widens it",
            "chat/Master rotation never makes it more permissive",
            "Never upgrades project-wide `ProjectAuthority`.",
            "`KEEP` until the actual coordination basis changes, including across Master rotation.",
            "`STANDARD` remains FAST-compatible and never implies FULL.",
            "Apply `HIGH_ASSURANCE` only to affected work",
            "return to `NORMAL` when that escalation ends",
            "It never implies approval or FULL.",
            "Classify per substantive change only when decision-relevant.",
            "Dimensions remain orthogonal unless a canonical rule explicitly connects them.",
            "Project/repository size alone selects neither `STANDARD` nor `HIGH_ASSURANCE`.",
        )
        missing_skill = [fragment for fragment in required_skill_fragments if fragment not in skill_section]
        if missing_skill:
            raise AssertionError(f"candidate kernel lost protected dimension semantics: {missing_skill}")
        if skill_section.count("`KEEP`") != 3:
            raise AssertionError("candidate must express KEEP only for Role, ProjectAuthority, CoordinationBaseline")
        if "Reuse still-valid runtime state" in skill_section or "DecisionFrame" in skill_section:
            raise AssertionError("candidate reintroduced the superseded additive decision-frame abstraction")

        authority_section = candidate_sections["skill/references/authority-gates.md"]
        required_authority_fragments = (
            "established in `SKILL.md` as independent inputs to gate evaluation",
            "This domain does not reclassify those dimensions",
            "Repository/platform permissions still apply.",
            "scope the change only to what it clearly grants",
            "may satisfy only the applicable gate for that action",
            "without converting the broader project to a more permissive `ProjectAuthority`",
            "Use the lightest safe controls.",
            "Importance alone does not make risk high",
            "blast radius, reversibility, security/data impact, compatibility, and production consequences",
        )
        missing_authority = [fragment for fragment in required_authority_fragments if fragment not in authority_section]
        if missing_authority:
            raise AssertionError(f"candidate authority bridge lost gate semantics: {missing_authority}")
        if "`ADVISORY`" in authority_section or "`AUTONOMOUS_WITH_GATES`" in authority_section:
            raise AssertionError("authority bridge re-declared the kernel ProjectAuthority value ontology")
        print("PASS protected-dimension-and-gate-semantics")

        source_skill_words = word_count(source_sections["skill/SKILL.md"])
        candidate_skill_words = word_count(candidate_sections["skill/SKILL.md"])
        source_authority_words = word_count(source_sections["skill/references/authority-gates.md"])
        candidate_authority_words = word_count(candidate_sections["skill/references/authority-gates.md"])
        if candidate_skill_words > source_skill_words:
            raise AssertionError(
                f"always-active kernel section grew: source={source_skill_words} candidate={candidate_skill_words}"
            )
        if candidate_authority_words >= source_authority_words:
            raise AssertionError("gate-specific candidate did not remove the repeated dimension ontology")
        if candidate_skill_words + candidate_authority_words >= source_skill_words + source_authority_words:
            raise AssertionError("combined activated target sections did not reduce structural duplication")
        print(
            "PASS structural-diagnostic "
            f"skill={source_skill_words}->{candidate_skill_words} "
            f"authority={source_authority_words}->{candidate_authority_words} "
            f"combined={source_skill_words + source_authority_words}->"
            f"{candidate_skill_words + candidate_authority_words}"
        )

        for source_path in ("design/RULE-MAP.md", "design/GOAL-MAP.md", "docs/PROJECT-SPEC.md"):
            write_source_file(SOURCE_REF, source_path, temp_root / source_path)
        validation = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "validate_skill.py"), str(temp_root / "skill")],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if validation.returncode != 0:
            raise AssertionError(
                "materialized candidate failed validate_skill.py: "
                + (validation.stderr.strip() or validation.stdout.strip())
            )
        print("PASS materialized-candidate-skill-validation")

    readme = README_PATH.read_text(encoding="utf-8")
    analysis = ANALYSIS_PATH.read_text(encoding="utf-8")
    for required in (SOURCE_REF, SEMANTIC_BASELINE_REF, "REVISE / superseded by this prototype"):
        if required not in readme:
            raise AssertionError(f"semantic ledger missing required identity/verdict: {required}")
    for scenario in (
        "Repeated bounded Master FAST work",
        "Zero-chat Master recovery",
        "Technical capability increases without Authority change",
        "STANDARD coordination on bounded FAST work",
        "HIGH_ASSURANCE on bounded work",
        "Scoped one-off approval",
    ):
        if scenario not in analysis:
            raise AssertionError(f"source-grounded analysis missing scenario: {scenario}")
    print("PASS ledger-and-operational-analysis-present")


if __name__ == "__main__":
    main()
