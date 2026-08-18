# GitHub Project Orchestrator

A reusable ChatGPT Skill for end-to-end GitHub software delivery. It is designed to act as a recoverable Engineering Project Manager and senior developer: establish lean repository readiness, frame outcomes, manage dependency-aware work, implement or delegate bounded tasks, review and integrate changes, recover across sessions, and drive verified releases without turning orchestration itself into unnecessary process.

## Install

1. Open the repository's **Releases** page.
2. Download `skill.zip` from the release you want to install.
3. In ChatGPT, open **Plugins** -> **Skills** -> **Create** -> **Upload from your computer**.
4. Upload `skill.zip`, review the Skill, and complete installation.

OpenAI documents computer upload as a supported Skill installation path. Direct installation from an arbitrary GitHub URL is not treated as a supported installer contract by this repository.

Official ChatGPT Skills documentation: https://help.openai.com/en/articles/20001066-skills-in-chatgpt

## License

Licensed under the [MIT License](LICENSE).

Copyright (c) 2026 [ACh](https://github.com/ach1992).

The released `skill.zip` includes the same canonical `LICENSE` notice at its package root so the downloadable Skill carries its distribution terms with it.

## Project map

Start here when developing, reviewing, or recovering this project. This is navigation to authoritative sources, not a duplicate status report.

| Need | Authoritative source |
|---|---|
| durable project mission, goals, non-goals, constraints, definition of done | [`docs/PROJECT-SPEC.md`](docs/PROJECT-SPEC.md) |
| semantic goal inventory and rule coverage | [`design/GOAL-MAP.md`](design/GOAL-MAP.md) |
| canonical Rule IDs and runtime owners | [`design/RULE-MAP.md`](design/RULE-MAP.md) |
| canonical runtime state vocabulary/model | [`design/STATE-MODEL.md`](design/STATE-MODEL.md) |
| core runtime behavior | [`skill/SKILL.md`](skill/SKILL.md) + direct references under [`skill/references/`](skill/references/) |
| operational benchmark/evidence | [`benchmarks/phase7/`](benchmarks/phase7/) |
| active delivery work, blockers, and accepted phase scope | GitHub Issues / Pull Requests |
| validation/release automation | [`.github/workflows/release.yml`](.github/workflows/release.yml) + [`tools/`](tools/) + [`tests/`](tests/) |

## Runtime architecture

The runtime entrypoint is intentionally compact. `skill/SKILL.md` establishes the orthogonal runtime dimensions, universal invariants, source-of-truth model, Master/Worker entry paths, and a direct role/event router. Detailed rules live in one-level references and are loaded only when their event is active.

Key runtime dimensions are independent unless a canonical rule explicitly connects them:

- `Role`: `MASTER` or `WORKER`;
- `ProjectAuthority`: project-wide authorization envelope;
- `ScopedAuthorization`: exact one-off action/effect grant;
- `CoordinationBaseline`: `LIGHTWEIGHT` or `STANDARD`;
- `AssuranceLevel`: `NORMAL` or scoped `HIGH_ASSURANCE`;
- `RiskLevel`: per substantive change.

Review evidence is bound to the current target/candidate/contract identity. Self-review is never independent review. When independent review is required, independence means a separate reviewer context/person/tool from the authoring Master; a distinct GitHub username or native PR approval is required only when repository/platform policy or the applicable gate explicitly requires that mechanism.

## Validate locally

```bash
python3 tools/validate_skill.py skill
python3 tests/test_contract_check_phase2.py
python3 tests/test_repo_preflight.py
python3 tests/test_validate_skill_phase6.py
python3 tools/score_phase7_benchmark.py \
  --scenarios benchmarks/phase7/scenarios.json \
  --baseline benchmarks/phase7/traces-v1.0.0.json \
  --current benchmarks/phase7/traces-current.json \
  --repo-root . \
  --baseline-ref v1.0.0
python3 tests/test_phase7_benchmark.py
python3 tests/test_package_skill.py
python3 tests/test_publish_release.py
```

The validator checks repository structure, runtime references/routing, namespaced state vocabulary, Goal/Rule/eval traceability, Python syntax, and immutable baseline compatibility. Phase 7 adds source-grounded operational A/B scoring plus adversarial negative fixtures; qualitative engineering judgment remains outside deterministic lint. Release validation also covers the bundled read-only repository preflight helper, byte-deterministic package construction including the canonical MIT license notice, and fail-closed release identity handling used by the release workflow.

## Release model

`main` is the release source of truth. The release workflow validates the repository, packages `skill/` plus the canonical repository `LICENSE` as `skill.zip`, generates `skill.zip.sha256`, and binds `v<VERSION>` to the exact release `GITHUB_SHA` before publication. A pre-existing or concurrently created version tag that resolves to another commit is a hard failure; publication uses the already verified tag with `gh release create --verify-tag` rather than relying on implicit tag creation. Versions containing a prerelease suffix (for example `1.1.0-rc.1`) are published as GitHub prereleases.

An existing release is treated as an idempotent success only when its version tag still resolves to the exact release SHA, its prerelease state is correct, and both published assets are byte-for-byte identical to the package and checksum built from that commit. Otherwise the workflow fails closed instead of silently reporting delivery.

`v1.0.0` is the immutable pre-refactor runtime baseline. Architectural changes are incremental, traceable to canonical Goal/Rule IDs, and evaluated against baseline behavior before a later runtime release is published.
