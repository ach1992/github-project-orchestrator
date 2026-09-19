# Platform Distributions

`skill/` is the single canonical runtime source for GitHub Project Orchestrator. Platform packages are generated from that source during validation/release; platform-specific runtime forks are not maintained.

## Supported distributions

| Platform | Release asset | Entrypoint/layout | Platform-specific adaptation |
|---|---|---|---|
| ChatGPT | `skill.zip` | wrapped `SKILL.md` package | Canonical package, including OpenAI interface metadata/assets. |
| Manus | `github-project-orchestrator-manus.zip` | `github-project-orchestrator/SKILL.md` | Canonical portable runtime with OpenAI-only `agents/` and `assets/` omitted. |
| Qwen Code | `github-project-orchestrator-qwen.zip` | `github-project-orchestrator/SKILL.md` | Canonical portable runtime with OpenAI-only metadata/assets omitted. Root [`QWEN.md`](../QWEN.md) provides a repository-link bootstrap when package installation is unavailable. |
| Claude.ai | `github-project-orchestrator-claude.zip` | `github-project-orchestrator/skill.md` | Canonical portable runtime with OpenAI-only metadata/assets omitted; only the entrypoint filename and discovery description are adapted to Claude custom-Skill requirements. |
| Z.ai ZCode | `github-project-orchestrator-zcode.zip` | `github-project-orchestrator/SKILL.md` | No runtime transformation; directory bundle matches ZCode's documented Skill discovery model. |
| Grok Build | `github-project-orchestrator-grok.zip` | `github-project-orchestrator/SKILL.md` | No runtime transformation; directory bundle matches Grok Build's documented Skill discovery model. |
| Kimi Code | `github-project-orchestrator-kimi.zip` | `github-project-orchestrator/SKILL.md` | No runtime transformation; directory bundle matches Kimi Code Agent Skills. |
| Google Gemini (Gemini Apps Skills) | `github-project-orchestrator-gemini.zip` | root `SKILL.md` | Wrapper directory is removed because Gemini Apps ZIP upload requires `SKILL.md` in the archive's root/main folder. |
| DeepSeek Harness | `github-project-orchestrator-deepseek.zip` | `github-project-orchestrator/SKILL.md` | No runtime transformation; directory bundle matches DeepSeek Harness's documented `<name>/SKILL.md` model. |
| Microsoft Copilot Studio | `github-project-orchestrator-copilot.zip` | root `SKILL.md` | Wrapper directory is removed for direct Copilot Studio Skill ZIP upload; runtime bytes remain canonical. |

Every archive also has a matching `.sha256` asset.

## Source-of-truth rule

Core orchestration behavior is developed only under `skill/`. Portable distributions copy canonical runtime files by default and exclude the OpenAI-specific top-level `agents/` and `assets/` interface surfaces. This default-inclusion rule ensures that a future canonical runtime directory such as `templates/` or another supporting resource is not silently omitted from non-OpenAI packages.

Generated platform packages must not introduce platform-specific project-management, engineering, authority, recovery, review, integration, or release behavior. A platform adaptation is allowed only when required for discovery, packaging, installation, or tool-capability compatibility.

The release packager uses three layout classes rather than maintaining platform forks:

- **wrapped canonical `SKILL.md` bundle:** Manus, Qwen Code, Z.ai ZCode, Grok Build, Kimi Code, and DeepSeek Harness;
- **root-upload `SKILL.md` ZIP:** Google Gemini and Microsoft Copilot Studio;
- **Claude-specific discovery adapter:** lowercase `skill.md` plus the bounded Claude discovery description.

This keeps fixes and behavior changes synchronized across platforms and prevents distribution drift.

## Packaging

`tools/package_skill.py` continues to build the canonical ChatGPT artifact. `tools/package_platform_skills.py` builds every portable platform artifact directly from `skill/` and validates archive contents against the canonical source.

Examples:

```bash
python3 tools/package_platform_skills.py skill manus github-project-orchestrator-manus.zip github-project-orchestrator-manus.zip.sha256
python3 tools/package_platform_skills.py skill zcode github-project-orchestrator-zcode.zip github-project-orchestrator-zcode.zip.sha256
python3 tools/package_platform_skills.py skill grok github-project-orchestrator-grok.zip github-project-orchestrator-grok.zip.sha256
python3 tools/package_platform_skills.py skill kimi github-project-orchestrator-kimi.zip github-project-orchestrator-kimi.zip.sha256
python3 tools/package_platform_skills.py skill gemini github-project-orchestrator-gemini.zip github-project-orchestrator-gemini.zip.sha256
python3 tools/package_platform_skills.py skill deepseek github-project-orchestrator-deepseek.zip github-project-orchestrator-deepseek.zip.sha256
python3 tools/package_platform_skills.py skill copilot github-project-orchestrator-copilot.zip github-project-orchestrator-copilot.zip.sha256
```

Do not commit generated package copies as alternate runtime sources.

## Platform notes

### Manus

Manus supports uploaded `.zip`/`.skill` packages and GitHub-imported Skills. This repository uses the release ZIP as the stable distribution surface so the repository root can remain platform-neutral.

### Qwen Code

Qwen Code natively supports `SKILL.md` Agent Skills. For Qwen environments that work from a GitHub repository link rather than an installed Skill, [`QWEN.md`](../QWEN.md) explicitly routes the model to the canonical `skill/SKILL.md` kernel and its event-driven references.

### Claude.ai

Claude custom Skills support ZIP upload and use a lowercase `skill.md` entrypoint with bounded metadata. The Claude package changes only the entrypoint filename and discovery description; the runtime body and supporting portable runtime files remain canonical.

### Z.ai ZCode

ZCode discovers directory-form Skills containing `SKILL.md` under user or workspace Skill roots such as `~/.zcode/skills/` and `.zcode/skills/`. The release ZIP therefore preserves the `github-project-orchestrator/` wrapper so that directory can be extracted directly into a ZCode Skill root. The package target is ZCode; no direct ZIP-import capability is claimed for the consumer `chat.z.ai` interface.

### Grok Build

Grok Build documents directory-form Skills with `SKILL.md` and supports user/project Skill roots such as `~/.grok/skills/` and `.grok/skills/`. The release bundle uses that layout unchanged. Grok on `grok.com` also exposes first-party Skills, but this repository does not claim a web ZIP-import path that current first-party documentation does not establish.

### Kimi Code

Kimi Code Agent Skills use directory-form `SKILL.md` bundles and support Skill roots including `~/.kimi-code/skills/` and the portable `~/.agents/skills/`. Kimi Agent also supports custom Skills in its product UI; the released archive is specifically packaged for the documented Kimi Code file-based Skill surface.

### Google Gemini

Gemini Apps Skills support direct `SKILL.md` or ZIP upload. For ZIPs, Gemini requires `SKILL.md` in the root/main folder. The Gemini distribution therefore removes only the outer archive wrapper; `SKILL.md`, references, scripts, and license contents otherwise stay canonical. OpenAI-specific metadata/assets remain excluded.

### DeepSeek Harness

DeepSeek Harness supports directory bundles using `<name>/SKILL.md`. The release ZIP preserves the `github-project-orchestrator/` wrapper for extraction into a configured Harness Skill root. This package targets DeepSeek Harness and does not claim that consumer `chat.deepseek.com` currently provides the same file-import surface.

### Microsoft Copilot Studio

Copilot Studio agents powered by the GitHub Copilot harness can upload an existing Skill as `SKILL.md` or a ZIP package. The Copilot distribution uses a root-level `SKILL.md` upload layout and preserves canonical runtime bytes. This package targets Copilot Studio; no direct Skill ZIP-import capability is claimed for the consumer `copilot.microsoft.com` chat interface.

## Release discipline

A release is valid only when the canonical ChatGPT artifact and every supported platform artifact are generated from the same commit and the publisher verifies the exact release asset bytes for that tag. The publisher fails closed when any required ZIP or checksum is missing or differs from the candidate.
