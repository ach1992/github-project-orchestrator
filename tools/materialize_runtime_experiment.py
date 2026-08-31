#!/usr/bin/env python3
"""Materialize a representation experiment from an immutable Skill baseline."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import subprocess
import tarfile
from pathlib import Path

PROGRAM_BASELINE = "f98e8a242c720931e34aa7c4e8a799090e3d0495"


def git_bytes(repo: Path, *args: str) -> bytes:
    try:
        return subprocess.run(
            ["git", *args],
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ValueError(f"git {' '.join(args)} failed") from exc


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_extract_tar(data: bytes, destination: Path) -> None:
    destination = destination.resolve()
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:") as archive:
        for member in archive.getmembers():
            target = (destination / member.name).resolve()
            try:
                target.relative_to(destination)
            except ValueError as exc:
                raise ValueError(f"unsafe archive path: {member.name}") from exc
            if member.issym() or member.islnk():
                raise ValueError(f"runtime experiment archive must not contain links: {member.name}")
        archive.extractall(destination)


def replace_section(baseline: str, start: str, end: str, candidate: str) -> str:
    if baseline.count(start) != 1:
        raise ValueError(f"baseline must contain start heading exactly once: {start}")
    if baseline.count(end) != 1:
        raise ValueError(f"baseline must contain end heading exactly once: {end}")
    if candidate.count(start) != 1 or not candidate.lstrip().startswith(start):
        raise ValueError("candidate section must begin with the configured start heading exactly once")
    if end in candidate:
        raise ValueError("candidate section must not include the exclusive end heading")
    start_index = baseline.index(start)
    end_index = baseline.index(end)
    if start_index >= end_index:
        raise ValueError("baseline section headings are out of order")
    candidate = candidate.rstrip() + "\n\n"
    return baseline[:start_index] + candidate + baseline[end_index:]


def materialize(repo: Path, experiment_path: Path, output_dir: Path) -> dict:
    repo = repo.resolve()
    experiment_path = experiment_path.resolve()
    output_dir = output_dir.resolve()
    experiment = json.loads(experiment_path.read_text(encoding="utf-8"))

    if experiment.get("schema_version") != 1:
        raise ValueError("unsupported representation experiment schema_version")
    if experiment.get("baseline_ref") != PROGRAM_BASELINE:
        raise ValueError("representation experiment must remain pinned to the immutable program baseline")
    if experiment.get("semantic_change_allowed") is not False:
        raise ValueError("representation experiment must not allow semantic change")
    if experiment.get("canonical_runtime_changed_during_prototype") is not False:
        raise ValueError("prototype must remain outside the canonical runtime")

    replacement = experiment.get("replacement", {})
    required = {"start_heading", "end_heading_exclusive", "candidate_section"}
    if set(replacement) != required:
        raise ValueError("replacement contract must contain exactly start/end/candidate_section")

    baseline_path = experiment.get("baseline_entrypoint")
    if baseline_path != "skill/SKILL.md":
        raise ValueError("representation experiment baseline_entrypoint must be skill/SKILL.md")
    candidate_path = repo / replacement["candidate_section"]
    try:
        candidate_path.resolve().relative_to(repo)
    except ValueError as exc:
        raise ValueError("candidate section must stay inside the repository") from exc
    candidate_section = candidate_path.read_text(encoding="utf-8")

    baseline_bytes = git_bytes(repo, "show", f"{PROGRAM_BASELINE}:{baseline_path}")
    baseline_text = baseline_bytes.decode("utf-8")
    candidate_text = replace_section(
        baseline_text,
        replacement["start_heading"],
        replacement["end_heading_exclusive"],
        candidate_section,
    )

    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError("output directory must be absent or empty")
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = git_bytes(repo, "archive", "--format=tar", PROGRAM_BASELINE, "skill")
    safe_extract_tar(archive, output_dir)

    skill_path = output_dir / "skill" / "SKILL.md"
    skill_path.write_text(candidate_text, encoding="utf-8")

    metadata = {
        "schema_version": 1,
        "experiment_id": experiment["experiment_id"],
        "baseline_ref": PROGRAM_BASELINE,
        "baseline_entrypoint_sha256": sha256(baseline_bytes),
        "candidate_section_sha256": sha256(candidate_section.encode("utf-8")),
        "candidate_entrypoint_sha256": sha256(candidate_text.encode("utf-8")),
        "replacement_start": replacement["start_heading"],
        "replacement_end_exclusive": replacement["end_heading_exclusive"],
        "semantic_change_allowed": False,
    }
    (output_dir / "experiment-materialization.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--experiment", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    experiment_path = args.experiment if args.experiment.is_absolute() else repo / args.experiment
    output_dir = args.output_dir if args.output_dir.is_absolute() else repo / args.output_dir
    metadata = materialize(repo, experiment_path, output_dir)
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
