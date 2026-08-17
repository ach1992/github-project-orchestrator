# GitHub Project Orchestrator

A reusable ChatGPT Skill for end-to-end GitHub software delivery. It is designed to act as a recoverable Engineering Project Manager and senior developer: establish lean repository readiness, frame outcomes, manage dependency-aware work, implement or delegate bounded tasks, review and integrate changes, recover across sessions, and drive verified releases without turning orchestration itself into unnecessary process.

## Install

1. Open the repository's **Releases** page.
2. Download `skill.zip` from the release you want to install.
3. In ChatGPT, open **Plugins** -> **Skills** -> **Create** -> **Upload from your computer**.
4. Upload `skill.zip`, review the Skill, and complete installation.

OpenAI documents computer upload as a supported Skill installation path. Direct installation from an arbitrary GitHub URL is not treated as a supported installer contract by this repository.

Official ChatGPT Skills documentation: https://help.openai.com/en/articles/20001066-skills-in-chatgpt

## Project map

Start here when developing, reviewing, or recovering this project. This is navigation to authoritative sources, not a duplicate status report.

| Need | Authoritative source |
|---|---|
| mission, canonical goals, non-goals, success model | [`docs/PROJECT-SPEC.md`](docs/PROJECT-SPEC.md) |
| Goal -> Rule -> evaluation traceability | [`design/GOAL-MAP.md`](design/GOAL-MAP.md) |
| v1.0.0 semantic Rule IDs and proposed canonical owners | [`design/RULE-MAP.md`](design/RULE-MAP.md) |
| typed state/scope/lifetime model | [`design/STATE-MODEL.md`](design/STATE-MODEL.md) |
| execution/authority/effect/boundary relationships | [`design/DECISION-GRAPHS.md`](design/DECISION-GRAPHS.md) |
| phased refactor plan and exit gates | [`design/MIGRATION.md`](design/MIGRATION.md) |
| current actionable work and decisions | [GitHub Issues](https://github.com/ach1992/github-project-orchestrator/issues) |
| runtime source shipped to ChatGPT | [`skill/`](skill/) |
| immutable baseline and installable artifacts | [GitHub Releases](https://github.com/ach1992/github-project-orchestrator/releases) |

The repository is intentionally organized for **zero-chat recovery**: current project truth should be discoverable through this map, GitHub work items, Git/PR/CI evidence, and releases without relying on previous conversation history. Do not create parallel manager-memory or status-summary archives.

## Repository layout

```text
skill/                  Runtime Skill source shipped to ChatGPT
docs/                   Durable project intent/specification
design/                 Development-only semantic/design traceability
tools/                  Repository-development validation helpers
tests/                  Regression and baseline evidence
.github/workflows/       Validation and release automation
VERSION                  Release version
CHANGELOG.md             Human-readable release history
```

Development-only files are intentionally kept outside `skill/` so they do not enter the runtime Skill package.

## Development principles

- **Outcome before activity:** Issues, PRs, docs, tests, and process are means to verified delivery.
- **Low friction without rule loss:** optimize decision quality and agent usability, not raw token/file reduction.
- **Rule preservation > text preservation:** prose may be consolidated only when protected behavior remains canonical and tested.
- **Process proportional to need:** small work stays light; coordination grows only when dependency/risk/recovery value justifies it.
- **Evidence over narrative:** current Git/GitHub/CI/release/deployment identity owns factual state.
- **Recoverable and navigable:** persist only continuation-relevant truth in its natural owner and keep relationships easy to traverse.

## Validate locally

```bash
python3 tools/validate_skill.py skill
```

The validator checks repository-specific structural invariants, Markdown references, Skill frontmatter, Python syntax, and the current baseline manifest when applicable. Additional deterministic refactor lint is planned in later phases; scripts must not replace agent judgment where semantics are qualitative.

## Release model

`main` is the release source of truth. When `VERSION` contains a version that does not yet have a matching GitHub Release, the release workflow validates the repository, packages `skill/` as `skill.zip`, generates a SHA-256 checksum, and publishes tag/release `v<VERSION>` from the exact `main` commit.

`v1.0.0` is the immutable pre-refactor runtime baseline. Architectural changes are incremental, traceable to canonical Goal/Rule IDs, and evaluated against baseline behavior before a later runtime release is published.

The public-distribution license is intentionally tracked as a separate owner decision in [Issue #3](https://github.com/ach1992/github-project-orchestrator/issues/3); do not infer a license until that issue is resolved.
