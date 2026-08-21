# Platform Distributions

`skill/` is the single canonical runtime source for GitHub Project Orchestrator. Platform packages are generated from that source during validation/release; platform-specific runtime forks are not maintained.

## Supported distributions

| Platform | Release asset | Entrypoint | Platform-specific adaptation |
|---|---|---|---|
| ChatGPT | `skill.zip` | `SKILL.md` | Canonical package, including OpenAI interface metadata/assets. |
| Manus | `github-project-orchestrator-manus.zip` | `SKILL.md` | Portable runtime only: entrypoint, `references/`, `scripts/`, and canonical `LICENSE`. |
| Qwen | `github-project-orchestrator-qwen.zip` | `SKILL.md` | Portable runtime only. Root [`QWEN.md`](../QWEN.md) provides a repository-link bootstrap when package installation is unavailable. |
| Claude.ai | `github-project-orchestrator-claude.zip` | `skill.md` | Portable runtime only; the entrypoint filename and discovery description are adapted to Claude custom-Skill requirements. |

Every archive also has a matching `.sha256` asset.

## Source-of-truth rule

Core orchestration behavior is developed only under `skill/`:

- `skill/SKILL.md`
- `skill/references/`
- `skill/scripts/`

Generated Manus, Qwen, and Claude packages must not introduce platform-specific project-management, engineering, authority, recovery, or release behavior. A platform adaptation is allowed only when required for discovery, packaging, installation, or tool capability compatibility.

This keeps fixes and behavior changes synchronized across platforms and prevents distribution drift.

## Packaging

The existing `tools/package_skill.py` continues to build the canonical ChatGPT artifact. `tools/package_platform_skills.py` builds the portable Manus, Qwen, and Claude artifacts directly from `skill/` and validates archive contents against the canonical source.

Example:

```bash
python3 tools/package_platform_skills.py skill manus github-project-orchestrator-manus.zip github-project-orchestrator-manus.zip.sha256
python3 tools/package_platform_skills.py skill qwen github-project-orchestrator-qwen.zip github-project-orchestrator-qwen.zip.sha256
python3 tools/package_platform_skills.py skill claude github-project-orchestrator-claude.zip github-project-orchestrator-claude.zip.sha256
```

Do not commit generated package copies as alternate runtime sources.

## Platform notes

### Manus

Manus supports uploaded `.zip`/`.skill` packages and GitHub-imported Skills. This repository uses the release ZIP as the stable multi-platform distribution surface so the repository root can remain platform-neutral.

### Qwen

Qwen Code natively supports `SKILL.md` Agent Skills. For Qwen environments that work from a GitHub repository link rather than an installed Skill, [`QWEN.md`](../QWEN.md) explicitly routes the model to the canonical `skill/SKILL.md` kernel and its event-driven references.

### Claude.ai

Claude custom Skills support ZIP upload and use a lowercase `skill.md` entrypoint with bounded metadata. The Claude package therefore changes only the entrypoint filename and discovery description; the runtime body, references, and scripts remain canonical.

## Release discipline

A release is valid only when the canonical ChatGPT artifact and every supported platform artifact are generated from the same commit and the publisher verifies the exact release asset bytes for that tag.
