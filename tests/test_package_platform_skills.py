#!/usr/bin/env python3
"""Regression checks for generated Manus, Qwen, and Claude Skill packages."""

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
PACKAGER = ROOT / "tools" / "package_platform_skills.py"
LICENSE_TEXT = "MIT fixture license\n"

spec = importlib.util.spec_from_file_location("package_platform_skills", PACKAGER)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Unable to load {PACKAGER}")
package_platform_skills = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package_platform_skills)


def build_fixture(root: Path) -> Path:
    skill = root / "skill"
    (skill / "references").mkdir(parents=True)
    (skill / "scripts").mkdir(parents=True)
    (skill / "templates").mkdir(parents=True)
    (skill / "agents").mkdir(parents=True)
    (skill / "assets").mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\n"
        "name: github-project-orchestrator\n"
        "description: \"A deliberately long canonical description that platform packaging may adapt.\"\n"
        "---\n\n"
        "# Runtime\n\n"
        "Read [rules](references/rules.md).\n",
        encoding="utf-8",
    )
    (skill / "references" / "rules.md").write_text("rules\n", encoding="utf-8")
    (skill / "scripts" / "tool.py").write_text("print('ok')\n", encoding="utf-8")
    (skill / "templates" / "future.txt").write_text("portable future runtime\n", encoding="utf-8")
    (skill / "agents" / "openai.yaml").write_text("interface: openai\n", encoding="utf-8")
    (skill / "assets" / "icon.svg").write_text("<svg/>\n", encoding="utf-8")
    (root / "LICENSE").write_text(LICENSE_TEXT, encoding="utf-8")
    return skill


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    skill = build_fixture(root)

    for platform in sorted(package_platform_skills.PLATFORMS):
        output_a = root / f"{platform}-a.zip"
        output_b = root / f"{platform}-b.zip"
        digest_a = package_platform_skills.build(skill, platform, output_a)
        package_platform_skills.validate_archive(skill, platform, output_a)

        now = time.time() + 3600
        for path in [*skill.rglob("*"), root / "LICENSE"]:
            if path.is_file():
                os.utime(path, (now, now))
        digest_b = package_platform_skills.build(skill, platform, output_b)
        package_platform_skills.validate_archive(skill, platform, output_b)
        if digest_a != digest_b or output_a.read_bytes() != output_b.read_bytes():
            raise AssertionError(f"{platform} package is not deterministic")

        with zipfile.ZipFile(output_a) as archive:
            names = archive.namelist()
            if "github-project-orchestrator/agents/openai.yaml" in names:
                raise AssertionError(f"OpenAI metadata leaked into {platform} package")
            if "github-project-orchestrator/assets/icon.svg" in names:
                raise AssertionError(f"OpenAI asset leaked into {platform} package")
            if "github-project-orchestrator/templates/future.txt" not in names:
                raise AssertionError(f"future portable runtime file was omitted from {platform} package")
            if archive.read("github-project-orchestrator/LICENSE") != LICENSE_TEXT.encode("utf-8"):
                raise AssertionError(f"{platform} package license drifted")

            if platform == "claude":
                if "github-project-orchestrator/SKILL.md" in names:
                    raise AssertionError("Claude package retained uppercase SKILL.md")
                entry = archive.read("github-project-orchestrator/skill.md").decode("utf-8")
                expected = package_platform_skills.CLAUDE_DESCRIPTION
                if f'description: "{expected}"' not in entry:
                    raise AssertionError("Claude package did not apply bounded description metadata")
                if len(expected) > 200:
                    raise AssertionError("Claude description limit regressed")
                if "# Runtime" not in entry or "references/rules.md" not in entry:
                    raise AssertionError("Claude packaging changed runtime instructions")
            else:
                if "github-project-orchestrator/SKILL.md" not in names:
                    raise AssertionError(f"{platform} package is missing SKILL.md")

        print(f"PASS platform-package-{platform}")

    try:
        package_platform_skills.package_entries(skill, "unknown")
    except ValueError as exc:
        if "Unsupported platform" not in str(exc):
            raise
        print("PASS platform-package-unknown-rejected")
    else:
        raise AssertionError("unknown platform unexpectedly accepted")
