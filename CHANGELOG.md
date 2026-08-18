# Changelog

All notable changes to this project are documented here.

## [1.1.1] - 2026-08-18

### Fixed

- Healthy pending CI/check/deployment dependencies no longer force a one-re-read `MasterBoundary.BLOCKED` stop when the runtime can safely continue with bounded, non-tight autonomous rechecks or a real resume primitive.
- Pending external work now freezes only actions that actually depend on its result, so independently executable source/diff/acceptance review and other outcome-linked work are not unnecessarily serialized behind CI.
- Canonical design vocabulary now uses `ExecutionStrategy=SELF_EXECUTE`, and delivery eval language uses `DeliveryState.PENDING` instead of the legacy `PENDING_DELIVERY` spelling.

### Added

- Sentinel regression tests proving repository preflight does not execute configured `core.fsmonitor` or active tracked-path `filter.<driver>.clean` / `filter.<driver>.process` helpers, while preserving safe complete or explicit incomplete/fail-closed semantics.

### Changed

- The public README is reorganized around value, intended users, installation/update, practical startup usage, operating expectations, version/license, and links to deeper development evidence instead of exposing internal architecture as the primary path.

### Runtime compatibility

- This is a patch-level maintenance release. It preserves the existing lifecycle/`MasterBoundary` separation, authority gates, review freshness, anti-spin protections, recovery model, and deterministic release workflow while repairing continuation precedence and dependency classification.
- `v1.0.0` remains the immutable pre-refactor baseline, and previous `v1.1.0` release artifacts are not modified.

## [1.1.0] - 2026-08-18

### Added

- MIT public-distribution license, copyright (c) 2026 ACh (`https://github.com/ach1992`).
- Focused regression coverage for the bundled read-only repository preflight helper, including requested-repository identity isolation, credential-safe remote display, clean/dirty evidence, and bounded status reporting.

### Changed

- Release packaging now injects the single canonical repository `LICENSE` into `skill.zip` and rejects duplicate Skill-local license ownership, while preserving byte-deterministic archive construction and SHA-256 evidence.
- Project/design/benchmark documentation is reconciled to the completed Phase 1-8 migration so historical roadmap language cannot be mistaken for current unresolved work.
- Phase 7 runtime provenance is pinned to the immutable reachable `v1.1.0-rc.1` release commit after verifying its full `skill/` tree is identical to the former intermediate pin, so historical benchmark validation survives feature-branch cleanup.
- Stable-release validation includes repository-preflight regressions in addition to the existing runtime, compatibility, deterministic-lint, benchmark, package, publisher, immutable-baseline, and cleanliness checks.

### Runtime compatibility

- The Final GA readiness changes do not intentionally alter the runtime policy shipped in `v1.1.0-rc.1`; the runtime still preserves the lossless ontology, event routing, authority/effect model, bounded recovery, delegation, review-freshness, and delivery protections validated during the refactor.
- `v1.0.0` remains the immutable pre-refactor baseline and `v1.1.0-rc.1` remains an immutable prerelease artifact.

### Distribution

- `v1.1.0` is distributed under the MIT License; the downloadable Skill archive carries the same canonical license notice as the repository.

## [1.1.0-rc.1] - 2026-08-18

### Added

- Lossless runtime ontology with independent `CoordinationBaseline`, `AssuranceLevel`, `ProjectAuthority`, `ScopedAuthorization`, namespaced lifecycles, simultaneous `ApplicableEffects`, and explicit delivery identity/state.
- Canonical low-friction decision predicates and direct role/event routing from the compact runtime entrypoint.
- Scalable workstream/multi-repository coordination and progressive zero-chat recovery.
- Deterministic development lint for state vocabulary and Goal/Rule/evaluation traceability.
- Reproducible operational benchmark coverage across small, medium, large, recovery, delegation, review, release, and local-blocker scenarios.
- Deterministic `skill.zip` packaging with SHA-256 evidence and prerelease-aware GitHub publishing.

### Changed

- Reduced routine context and discovery overhead while preserving fresh review, authority, production, and delivery protections against the immutable `v1.0.0` baseline.
- Worker execution context is bounded by task/role triggers rather than loading project-wide governance by default.
- Large-project coordination keeps local work authoritative behind a minimal global outcome/dependency/release spine.
- Runtime/design documentation now reflects canonical post-refactor ownership instead of migration-era wording.
- Independent review is defined by separation from the authoring Master context, not by a distinct GitHub username; a fresh independent chat/model, review tool, or human reviewer can provide the additional review unless repository/platform policy explicitly requires a native approval identity. Manual review relay is therefore a valid path rather than `MISSING_CAPABILITY` when no external GitHub reviewer account is available.
- Release publication now fails closed on version/tag collisions: the remote tag must resolve to the exact release `GITHUB_SHA`, publication uses the pre-verified tag with `gh release create --verify-tag`, and an existing release is accepted as idempotent only when its tag, prerelease state, `skill.zip`, and checksum asset exactly match the current candidate.

### Compatibility

- Legacy `Authority` / `Expected Starting HEAD` and losslessly recoverable legacy `Operating Profile` inputs remain accepted for persisted v1.0.0-era contracts and recovery.
- Ambiguous legacy `Operating Profile: HIGH_ASSURANCE` still requires an authoritative coordination baseline; the runtime does not guess missing state.
- `v1.0.0` remains immutable and installable as the pre-refactor baseline.

### Distribution

- This release candidate predates the MIT licensing decision completed for `v1.1.0`; it remains an immutable historical prerelease artifact.

## [1.0.0] - 2026-08-18

### Added

- Initial public repository baseline of the existing `github-project-orchestrator` Skill.
- Runtime Skill source under `skill/` without semantic refactoring.
- Repository validation, immutable baseline manifest, and automated `skill.zip` release packaging.
- Durable project specification for future performance-oriented refactoring.
