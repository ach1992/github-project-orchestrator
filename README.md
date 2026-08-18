# GitHub Project Orchestrator

A reusable ChatGPT Skill for end-to-end GitHub software delivery. It combines an engineering project manager and senior developer workflow: recover current project state from Git/GitHub, choose the highest-value next action, implement or delegate bounded work, review and integrate safely, and drive release work to verified completion without unnecessary process or manual `continue` nudges.

## Why use it

GitHub Project Orchestrator is intended for developers and technical owners who want ChatGPT to take sustained ownership of a software outcome rather than answer one isolated coding question at a time.

Typical uses include:

- continuing an existing repository from its current Issues, PRs, branches, CI, and release state;
- delivering a feature, bug fix, maintenance release, or multi-step engineering milestone end-to-end;
- coordinating bounded Worker tasks while keeping review and integration ownership with the Master;
- recovering cleanly in a fresh chat without depending on the previous conversation;
- preserving human approval for genuinely consequential gates while automating ordinary reversible engineering work.

## Install or update

1. Open this repository's **Releases** page and download `skill.zip` from the release you want to use.
2. In an eligible ChatGPT account, open **Plugins** -> **Skills** -> **Create** -> **Upload from your computer**.
3. Upload `skill.zip`, review the Skill, and complete the installation flow.
4. To move to a newer release, repeat the same upload flow with that release's `skill.zip` and follow the review/install steps shown by ChatGPT.

OpenAI documents computer upload as a supported Skill installation path. Direct installation from an arbitrary GitHub URL is not treated as an installer contract by this repository.

Official ChatGPT Skills documentation: https://help.openai.com/en/articles/20001066-skills-in-chatgpt

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
- The Skill does not create background-work promises, artificial busywork, or parallel manager-state archives just to appear active.

## Version and license

Release: **v1.1.1**

Licensed under the [MIT License](LICENSE). The released `skill.zip` includes the same canonical `LICENSE` notice at its package root.

Copyright (c) 2026 [ACh](https://github.com/ach1992).

## Development and evidence

The public README is intentionally not a second runtime specification. Deeper authoritative sources are:

- project mission, goals, constraints, and definition of done: [`docs/PROJECT-SPEC.md`](docs/PROJECT-SPEC.md);
- Goal and Rule traceability: [`design/GOAL-MAP.md`](design/GOAL-MAP.md) and [`design/RULE-MAP.md`](design/RULE-MAP.md);
- runtime state vocabulary: [`design/STATE-MODEL.md`](design/STATE-MODEL.md);
- runtime entrypoint and references: [`skill/SKILL.md`](skill/SKILL.md) and [`skill/references/`](skill/references/);
- source-grounded operational benchmark: [`benchmarks/phase7/`](benchmarks/phase7/);
- release history: [`CHANGELOG.md`](CHANGELOG.md).

For maintainers, the pull-request workflow in [`.github/workflows/release.yml`](.github/workflows/release.yml) runs structural validation, compatibility tests, repository-preflight safety tests, deterministic lint, benchmark scoring/adversarial tests, deterministic packaging, publisher tests, immutable-baseline checks, and runtime cleanliness checks. `main` is the release source of truth; a successful validated push to `main` builds the deterministic `skill.zip` and `skill.zip.sha256` and publishes the exact version through the repository's release tooling.
