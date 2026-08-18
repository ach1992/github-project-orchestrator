#!/usr/bin/env python3
"""Regression checks for deterministic Phase 8 release packaging."""

from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import time
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
PACKAGER = ROOT / "tools" / "package_skill.py"

spec = importlib.util.spec_from_file_location("package_skill", PACKAGER)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Unable to load {PACKAGER}")
package_skill = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package_skill)


def build_fixture(root: Path) -> Path:
    skill = root / "skill"
    (skill / "references").mkdir(parents=True)
    (skill / "scripts" / "__pycache__").mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: fixture\ndescription: fixture\n---\n", encoding="utf-8")
    (skill / "references" / "rules.md").write_text("rules\n", encoding="utf-8")
    (skill / "scripts" / "tool.py").write_text("print('ok')\n", encoding="utf-8")
    (skill / "scripts" / "tool.pyc").write_bytes(b"compiled")
    (skill / "scripts" / "__pycache__" / "tool.cpython.pyc").write_bytes(b"cache")
    return skill


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    skill = build_fixture(root)
    zip_a = root / "a.zip"
    zip_b = root / "b.zip"
    checksum = root / "a.sha256"

    digest_a = package_skill.build(skill, zip_a)
    package_skill.validate_archive(skill, zip_a)
    package_skill.write_checksum(zip_a, checksum, digest_a)

    now = time.time() + 3600
    for path in skill.rglob("*"):
        if path.is_file():
            os.utime(path, (now, now))
    digest_b = package_skill.build(skill, zip_b)
    package_skill.validate_archive(skill, zip_b)

    if digest_a != digest_b or zip_a.read_bytes() != zip_b.read_bytes():
        raise AssertionError("package is not deterministic across source mtime changes")
    print("PASS deterministic-package")

    with zipfile.ZipFile(zip_a) as archive:
        names = archive.namelist()
    if names != sorted(names):
        raise AssertionError(f"archive entries are not sorted: {names}")
    if any("__pycache__" in name or name.endswith((".pyc", ".pyo")) for name in names):
        raise AssertionError(f"generated Python artifact leaked into archive: {names}")
    if not all(name.startswith("github-project-orchestrator/") for name in names):
        raise AssertionError(f"unexpected archive root: {names}")
    print("PASS package-contents")

    expected_checksum = f"{digest_a}  a.zip\n"
    if checksum.read_text(encoding="utf-8") != expected_checksum:
        raise AssertionError("checksum file format drifted")
    print("PASS package-checksum")

    target = skill / "references" / "target.md"
    target.write_text("target\n", encoding="utf-8")
    link = skill / "references" / "link.md"
    try:
        link.symlink_to(target.name)
    except (OSError, NotImplementedError):
        print("SKIP package-symlink")
    else:
        try:
            package_skill.build(skill, root / "symlink.zip")
        except ValueError as exc:
            if "Symlinks are not permitted" not in str(exc):
                raise
            print("PASS package-symlink")
        else:
            raise AssertionError("symlink unexpectedly allowed in release package")
