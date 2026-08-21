#!/usr/bin/env python3
"""Build deterministic portable Skill archives from the canonical skill/ runtime."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import package_skill

ARCHIVE_ROOT = package_skill.ARCHIVE_ROOT
FIXED_ZIP_TIME = package_skill.FIXED_ZIP_TIME
EXCLUDED_SUFFIXES = package_skill.EXCLUDED_SUFFIXES
PORTABLE_EXCLUDED_TOP_LEVEL = {"agents", "assets"}
PLATFORMS = {"manus", "qwen", "claude"}
CLAUDE_DESCRIPTION = (
    "Manage GitHub software delivery end-to-end: recover state, plan, implement, review, "
    "integrate, and release safely. Use for multi-step repository work."
)
FRONTMATTER_RE = re.compile(r"\A---\n(?P<meta>.*?)\n---(?P<body>\n.*)\Z", re.DOTALL)
DESCRIPTION_RE = re.compile(r"(?m)^description:\s*.*$")
NAME_RE = re.compile(r"(?m)^name:\s*(?P<value>.+?)\s*$")


def validate_platform(platform: str) -> None:
    if platform not in PLATFORMS:
        raise ValueError(f"Unsupported platform: {platform}; expected one of {sorted(PLATFORMS)}")


def portable_source_files(skill_dir: Path) -> list[Path]:
    files: list[Path] = []
    for path in package_skill.source_files(skill_dir):
        relative = path.relative_to(skill_dir)
        if relative.parts and relative.parts[0] in PORTABLE_EXCLUDED_TOP_LEVEL:
            continue
        files.append(path)
    if not any(path.relative_to(skill_dir).as_posix() == "SKILL.md" for path in files):
        raise ValueError("Canonical Skill entrypoint is missing: SKILL.md")
    return files


def claude_entrypoint(source: bytes) -> bytes:
    text = source.decode("utf-8")
    match = FRONTMATTER_RE.match(text)
    if match is None:
        raise ValueError("Canonical SKILL.md must start with YAML frontmatter")

    metadata = match.group("meta")
    name_match = NAME_RE.search(metadata)
    if name_match is None:
        raise ValueError("Canonical SKILL.md frontmatter is missing name")
    name = name_match.group("value").strip().strip("\"'")
    if len(name) > 64:
        raise ValueError("Claude Skill name exceeds 64 characters")
    if len(CLAUDE_DESCRIPTION) > 200:
        raise ValueError("Claude Skill description exceeds 200 characters")

    replacement = f"description: {json.dumps(CLAUDE_DESCRIPTION)}"
    metadata, count = DESCRIPTION_RE.subn(replacement, metadata, count=1)
    if count != 1:
        raise ValueError("Canonical SKILL.md frontmatter must contain exactly one description field")
    return f"---\n{metadata}\n---{match.group('body')}".encode("utf-8")


def archive_relative_path(platform: str, relative: PurePosixPath) -> PurePosixPath:
    if platform == "claude" and relative == PurePosixPath("SKILL.md"):
        return PurePosixPath("skill.md")
    return relative


def entry_bytes(platform: str, relative: PurePosixPath, path: Path) -> bytes:
    data = path.read_bytes()
    if platform == "claude" and relative == PurePosixPath("SKILL.md"):
        return claude_entrypoint(data)
    return data


def package_entries(skill_dir: Path, platform: str) -> list[tuple[str, bytes]]:
    validate_platform(platform)
    skill_dir = skill_dir.resolve()
    entries: list[tuple[str, bytes]] = []
    for path in portable_source_files(skill_dir):
        relative = PurePosixPath(path.relative_to(skill_dir).as_posix())
        archive_relative = archive_relative_path(platform, relative)
        archive_path = str(PurePosixPath(ARCHIVE_ROOT) / archive_relative)
        entries.append((archive_path, entry_bytes(platform, relative, path)))

    license_path = package_skill.canonical_license(skill_dir)
    entries.append((str(PurePosixPath(ARCHIVE_ROOT) / package_skill.LICENSE_NAME), license_path.read_bytes()))
    return sorted(entries, key=lambda entry: entry[0])


def build(skill_dir: Path, platform: str, output_zip: Path) -> str:
    entries = package_entries(skill_dir, platform)
    output_zip = output_zip.resolve()
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    if output_zip.exists():
        output_zip.unlink()

    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, data in entries:
            info = zipfile.ZipInfo(name, date_time=FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.flag_bits |= 0x800
            archive.writestr(info, data, compress_type=zipfile.ZIP_STORED)

    return hashlib.sha256(output_zip.read_bytes()).hexdigest()


def validate_archive(skill_dir: Path, platform: str, output_zip: Path) -> None:
    expected = dict(package_entries(skill_dir, platform))
    with zipfile.ZipFile(output_zip) as archive:
        names = archive.namelist()
        if names != sorted(expected):
            raise ValueError(f"Package contents mismatch for {platform}: {names}")
        if set(names) != set(expected):
            missing = sorted(set(expected) - set(names))
            extra = sorted(set(names) - set(expected))
            raise ValueError(f"Package contents mismatch for {platform}; missing={missing}, extra={extra}")
        for name in names:
            pure = PurePosixPath(name)
            if pure.is_absolute() or ".." in pure.parts:
                raise ValueError(f"Unsafe archive path: {name}")
            if "__pycache__" in pure.parts or pure.suffix in EXCLUDED_SUFFIXES:
                raise ValueError(f"Generated Python artifact in package: {name}")
            if archive.read(name) != expected[name]:
                raise ValueError(f"Packaged content drifted from canonical source: {name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_dir", type=Path)
    parser.add_argument("platform", choices=sorted(PLATFORMS))
    parser.add_argument("output_zip", type=Path)
    parser.add_argument("checksum", type=Path)
    args = parser.parse_args()

    digest = build(args.skill_dir, args.platform, args.output_zip)
    validate_archive(args.skill_dir, args.platform, args.output_zip)
    package_skill.write_checksum(args.output_zip, args.checksum, digest)
    print(f"Built {args.output_zip} for {args.platform}: sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
