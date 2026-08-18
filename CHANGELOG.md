# Changelog

All notable changes to this project are documented here.

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
- Independent review is defined by separation from the authoring Master context, not by a distinct GitHub username; a fresh independent chat/model, review tool, or human reviewer can provide the additional review unless repository/platform policy explicitly requires a native approval identity.

### Compatibility

- Legacy `Authority` / `Expected Starting HEAD` and losslessly recoverable legacy `Operating Profile` inputs remain accepted for persisted v1.0.0-era contracts and recovery.
- Ambiguous legacy `Operating Profile: HIGH_ASSURANCE` still requires an authoritative coordination baseline; the runtime does not guess missing state.
- `v1.0.0` remains immutable and installable as the pre-refactor baseline.

### Distribution

- This release candidate does not change the unresolved public-license decision tracked in Issue #3 and does not claim third-party redistribution/modification rights beyond the repository's existing language.

## [1.0.0] - 2026-08-18

### Added

- Initial public repository baseline of the existing `github-project-orchestrator` Skill.
- Runtime Skill source under `skill/` without semantic refactoring.
- Repository validation, immutable baseline manifest, and automated `skill.zip` release packaging.
- Durable project specification for future performance-oriented refactoring.
