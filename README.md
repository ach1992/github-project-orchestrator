# GitHub Project Orchestrator

A reusable ChatGPT Skill for end-to-end GitHub software delivery. It is designed to act as a recoverable Engineering Project Manager and senior developer: establish lean repository readiness, frame outcomes, manage work, implement or delegate bounded tasks, review and integrate changes, recover across sessions, and drive verified releases.

## Install

1. Open the repository's **Releases** page.
2. Download `skill.zip` from the release you want to install.
3. In ChatGPT, open **Plugins** -> **Skills** -> **Create** -> **Upload from your computer**.
4. Upload `skill.zip`, review the Skill, and complete installation.

OpenAI documents computer upload as a supported Skill installation path. Direct installation from an arbitrary GitHub URL is not treated as a supported installer contract by this repository.

Official ChatGPT Skills documentation: https://help.openai.com/en/articles/20001066-skills-in-chatgpt

## Repository layout

```text
skill/                  Runtime Skill source shipped to ChatGPT
docs/                   Durable project intent and design documentation
tools/                  Repository-development validation helpers
tests/                   Regression and baseline evidence
.github/workflows/       Validation and release automation
VERSION                  Release version
CHANGELOG.md             Human-readable release history
```

Development-only files are intentionally kept outside `skill/` so they do not enter the runtime Skill package.

## Validate locally

```bash
python3 tools/validate_skill.py skill
```

The validator checks repository-specific structural invariants, Markdown references, Skill frontmatter, Python syntax, and the current baseline manifest when applicable.

## Release model

`main` is the release source of truth. When `VERSION` contains a version that does not yet have a matching GitHub Release, the release workflow validates the repository, packages `skill/` as `skill.zip`, generates a SHA-256 checksum, and publishes tag/release `v<VERSION>` from the exact `main` commit.

`v1.0.0` is the immutable baseline of the pre-refactor Skill. Future architectural optimization is evaluated against this baseline and its behavioral regression scenarios.
