# GitHub Project Orchestrator

A portable Agent Skill for end-to-end GitHub software delivery, distributed for ChatGPT, Manus, Qwen, and Claude.ai from one canonical runtime. It combines an engineering project manager and senior developer workflow: recover current project state from Git/GitHub, choose the highest-value next action, implement or delegate bounded work, review and integrate safely, and drive release work to verified completion without unnecessary process or manual `continue` nudges.

## Why use it

GitHub Project Orchestrator is intended for developers and technical owners who want an AI agent to take sustained ownership of a software outcome rather than answer one isolated coding question at a time.

Typical uses include:

- continuing an existing repository from its current Issues, PRs, branches, CI, and release state;
- delivering a feature, bug fix, maintenance release, or multi-step engineering milestone end-to-end;
- coordinating bounded Worker tasks while keeping review and integration ownership with the Master;
- recovering cleanly in a fresh chat without depending on the previous conversation;
- preserving human approval for genuinely consequential gates while automating ordinary reversible engineering work.

## Install or update

Open the repository's **Releases** page and use the package for your platform:

| Platform | Release asset | Installation / activation |
|---|---|---|
| ChatGPT | `skill.zip` | Upload as a custom Skill in ChatGPT. |
| Manus | `github-project-orchestrator-manus.zip` | Upload from the Manus Skills interface. |
| Qwen | `github-project-orchestrator-qwen.zip` | Extract into a Qwen Code Skill directory. For repository-link environments, provide this repository URL and have Qwen read [`QWEN.md`](QWEN.md) first. |
| Claude.ai | `github-project-orchestrator-claude.zip` | Enable code execution, then upload from **Customize -> Skills**. |

Each archive has a matching `.sha256` checksum. Manus, Qwen, and Claude packages are generated from `skill/`; they are not independently maintained forks.

Official platform references:

- ChatGPT Skills: https://help.openai.com/en/articles/20001066-skills-in-chatgpt
- Manus Skills: https://help.manus.im/en/articles/14753565-how-to-share-and-use-skills-in-manus
- Qwen Code Agent Skills: https://qwenlm.github.io/qwen-code-docs/en/users/features/skills/
- Claude custom Skills: https://support.claude.com/en/articles/12512180-use-skills-in-claude

See [`docs/PLATFORM-DISTRIBUTIONS.md`](docs/PLATFORM-DISTRIBUTIONS.md) for the single-source distribution model and platform-specific packaging boundaries.

## Start using it

For an existing repository, a compact Master prompt is usually enough:

```text
Use github-project-orchestrator as MASTER for:
https://github.com/OWNER/REPOSITORY

Mode: RECOVER, then continue end-to-end.
Project Authority: AUTONOMOUS_WITH_GATES

Recover current truth from the repository and GitHub, then continue the next valid project action until a genuine external boundary or project completion.
```

You can also point the Master at a specific Issue, PR, milestone, release, or project outcome. Durable repository/GitHub evidence remains authoritative when chat history is absent or stale.

## Operating expectations

- The GitHub repository must already exist and be identifiable to the Master.
- The Skill favors the smallest safe process that still protects correctness, review freshness, authorization, and recovery.
- Ordinary reversible implementation can proceed autonomously when authorized; material approval, production, destructive, or other applicable gates remain explicit.
- A pending CI/check/deployment does not automatically stop the workflow: useful independent work should continue first, and supported bounded continuation can keep short waits from requiring a user nudge.
- Self-review is not relabeled independent review. When independent review is required, use a genuinely separate reviewer context/person/tool unless repository policy requires a native GitHub reviewer identity.
- Worker, reviewer, and Master-rotation relays are English by default and use one copyable block when human-relayed; structured Worker/reviewer results preserve exact identity, evidence, completeness, and limitations for the receiving Master.
- Security-sensitive AI relays state evidence-backed defensive scope and continue safely allowed analysis/remediation/testing when one detail is restricted, without claiming policy bypass or broadening authorization.
- The Skill does not create background-work promises, artificial busywork, or parallel manager-state archives just to appear active.

## Version and license

Release: **v1.3.0**

Licensed under the [MIT License](LICENSE). Every released platform archive includes the same canonical `LICENSE` notice at its package root.

Copyright (c) 2026 [ACh](https://github.com/ach1992).

## Development and evidence

The public README is intentionally not a second runtime specification. Deeper authoritative sources are:

- project mission, goals, constraints, and definition of done: [`docs/PROJECT-SPEC.md`](docs/PROJECT-SPEC.md);
- Goal and Rule traceability: [`design/GOAL-MAP.md`](design/GOAL-MAP.md) and [`design/RULE-MAP.md`](design/RULE-MAP.md);
- runtime state vocabulary: [`design/STATE-MODEL.md`](design/STATE-MODEL.md);
- runtime entrypoint and references: [`skill/SKILL.md`](skill/SKILL.md) and [`skill/references/`](skill/references/);
- platform distribution policy: [`docs/PLATFORM-DISTRIBUTIONS.md`](docs/PLATFORM-DISTRIBUTIONS.md);
- source-grounded operational benchmark: [`benchmarks/phase7/`](benchmarks/phase7/);
- release history: [`CHANGELOG.md`](CHANGELOG.md).

For maintainers, the pull-request workflow in [`.github/workflows/release.yml`](.github/workflows/release.yml) runs structural validation, compatibility tests, repository-preflight safety tests, deterministic lint, benchmark scoring/adversarial tests, deterministic packaging for every supported platform, publisher tests, immutable-baseline checks, and runtime cleanliness checks. `main` remains the validated integration source of truth; release publication is attempted only when `VERSION` changes on `main` or the workflow is explicitly dispatched, and the publisher enforces exact version/tag/SHA/all-assets identity.
