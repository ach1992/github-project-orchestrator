#!/usr/bin/env python3
"""Create a stable line-level source index for a Skill runtime specification."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
from pathlib import Path

NORMATIVE_HINT = re.compile(
    r"\b(must|must not|always|never|do not|only|required|require|cannot|should|should not|"
    r"keep|prefer|avoid|verify|re-read|reconcile|stop|continue|persist|protect|treat|use|"
    r"select|classify|infer|escalate|retain|preserve|create|remove|return|read)\b",
    re.IGNORECASE,
)


def line_kind(text: str) -> str:
    stripped = text.lstrip()
    if stripped.startswith("#"):
        return "heading"
    if stripped.startswith("|"):
        return "table"
    if re.match(r"^(?:[-*+] |\d+[.)] )", stripped):
        return "list"
    if stripped.startswith("```"):
        return "fence"
    return "text"


def occurrence_id(relative: str, line_number: int, text: str) -> str:
    payload = f"{relative}\0{line_number}\0{text}".encode("utf-8")
    return "SRC-" + hashlib.sha256(payload).hexdigest()[:12].upper()


def source_files(skill_dir: Path) -> list[Path]:
    files = [skill_dir / "SKILL.md"]
    files.extend(
        path
        for path in sorted((skill_dir / "references").glob("*.md"))
        if path.name != "eval-scenarios.md"
    )
    return files


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-dir", type=Path, default=Path("skill"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    skill_dir = args.skill_dir.resolve()
    rows: list[tuple[str, str, int, str, str, str]] = []
    for path in source_files(skill_dir):
        relative = str(path.relative_to(skill_dir))
        for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            text = raw.rstrip()
            if not text.strip():
                continue
            rows.append(
                (
                    occurrence_id(relative, line_number, text),
                    relative,
                    line_number,
                    line_kind(text),
                    "yes" if NORMATIVE_HINT.search(text) else "no",
                    text,
                )
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("occurrence_id", "path", "line", "kind", "normative_hint", "text"))
        writer.writerows(rows)

    print(f"Indexed {len(rows)} non-empty runtime lines into {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
