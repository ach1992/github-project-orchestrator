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
LICENSE_TEXT = "MIT fixture license\n"

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
    (root / "LICENSE").write_text(LICENSE_TEXT, encoding="utf-8")
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
    for path in [*skill.rglob("*"), root / "LICENSE"]:
        if path.is_file():
            os.utime(path, (now, now))
    digest_b = package_skill.build(skill, zip_b)
    package_skill.validate_archive(skill, zip_b)

    if digest_a != digest_b or zip_a.read_bytes() != zip_b.read_bytes():
        raise AssertionError("package is not deterministic across source mtime changes")
    print("PASS deterministic-package")

    with zipfile.ZipFile(zip_a) as archive:
        names = archive.namelist()
        packaged_license = archive.read("github-project-orchestrator/LICENSE")
    if names != sorted(names):
        raise AssertionError(f"archive entries are not sorted: {names}")
    if any("__pycache__" in name or name.endswith((".pyc", ".pyo")) for name in names):
        raise AssertionError(f"generated Python artifact leaked into archive: {names}")
    if not all(name.startswith("github-project-orchestrator/") for name in names):
        raise AssertionError(f"unexpected archive root: {names}")
    if packaged_license != LICENSE_TEXT.encode("utf-8"):
        raise AssertionError("packaged LICENSE does not match canonical repository LICENSE")
    print("PASS package-contents-license")

    expected_checksum = f"{digest_a}  a.zip\n"
    if checksum.read_text(encoding="utf-8") != expected_checksum:
        raise AssertionError("checksum file format drifted")
    print("PASS package-checksum")

    license_path = root / "LICENSE"
    license_path.unlink()
    try:
        package_skill.build(skill, root / "missing-license.zip")
    except ValueError as exc:
        if "LICENSE is missing" not in str(exc):
            raise
        print("PASS package-license-required")
    else:
        raise AssertionError("package unexpectedly allowed a missing canonical LICENSE")
    license_path.write_text(LICENSE_TEXT, encoding="utf-8")

    duplicate_license = skill / "LICENSE"
    duplicate_license.write_text("duplicate\n", encoding="utf-8")
    try:
        package_skill.build(skill, root / "duplicate-license.zip")
    except ValueError as exc:
        if "must not duplicate" not in str(exc):
            raise
        print("PASS package-license-single-owner")
    else:
        raise AssertionError("package unexpectedly allowed duplicate LICENSE ownership")
    duplicate_license.unlink()

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
            raise AssertionError("symlink unexpectedly allowed")
