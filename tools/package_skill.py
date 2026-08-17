#!/usr/bin/env python3
"""Build a deterministic installable Skill archive and SHA-256 checksum."""

from __future__ import annotations

import argparse
import hashlib
import stat
import zipfile
from pathlib import Path, PurePosixPath

ARCHIVE_ROOT = "github-project-orchestrator"
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def source_files(skill_dir: Path) -> list[Path]:
    if not skill_dir.is_dir():
        raise ValueError(f"Skill directory does not exist: {skill_dir}")

    files: list[Path] = []
    for path in sorted(skill_dir.rglob("*")):
        relative = path.relative_to(skill_dir)
        if "__pycache__" in relative.parts or path.suffix in EXCLUDED_SUFFIXES:
            continue
        if path.is_symlink():
            raise ValueError(f"Symlinks are not permitted in release packages: {relative}")
        if path.is_file():
            files.append(path)
    if not files:
        raise ValueError("Skill directory contains no packageable files")
    return files


def archive_name(skill_dir: Path, path: Path) -> str:
    relative = PurePosixPath(path.relative_to(skill_dir).as_posix())
    return str(PurePosixPath(ARCHIVE_ROOT) / relative)


def build(skill_dir: Path, output_zip: Path) -> str:
    skill_dir = skill_dir.resolve()
    output_zip = output_zip.resolve()
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    if output_zip.exists():
        output_zip.unlink()

    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in source_files(skill_dir):
            info = zipfile.ZipInfo(archive_name(skill_dir, path), date_time=FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.flag_bits |= 0x800
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    digest = hashlib.sha256(output_zip.read_bytes()).hexdigest()
    return digest


def write_checksum(output_zip: Path, checksum_path: Path, digest: str) -> None:
    checksum_path = checksum_path.resolve()
    checksum_path.parent.mkdir(parents=True, exist_ok=True)
    checksum_path.write_text(f"{digest}  {output_zip.name}\n", encoding="utf-8")


def validate_archive(skill_dir: Path, output_zip: Path) -> None:
    expected = {archive_name(skill_dir.resolve(), path) for path in source_files(skill_dir.resolve())}
    with zipfile.ZipFile(output_zip) as archive:
        actual = set(archive.namelist())
        if actual != expected:
            missing = sorted(expected - actual)
            extra = sorted(actual - expected)
            raise ValueError(f"Package contents mismatch; missing={missing}, extra={extra}")
        for name in actual:
            pure = PurePosixPath(name)
            if pure.is_absolute() or ".." in pure.parts:
                raise ValueError(f"Unsafe archive path: {name}")
            if "__pycache__" in pure.parts or pure.suffix in EXCLUDED_SUFFIXES:
                raise ValueError(f"Generated Python artifact in package: {name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_dir", type=Path)
    parser.add_argument("output_zip", type=Path)
    parser.add_argument("checksum", type=Path)
    args = parser.parse_args()

    digest = build(args.skill_dir, args.output_zip)
    validate_archive(args.skill_dir, args.output_zip)
    write_checksum(args.output_zip, args.checksum, digest)
    print(f"Built {args.output_zip}: sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
