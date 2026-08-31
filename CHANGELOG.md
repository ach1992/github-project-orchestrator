# Changelog

All notable changes to this project are documented here.

## [1.2.3] - 2026-08-31

### Fixed

- Every user-visible machine relay is now automatically emitted as the complete response in exactly one fenced copy target, so Worker handoffs, independent-review prompts/results, and Master recovery relays no longer depend on a separate copy/paste-formatting request.

### Runtime compatibility

- This patch changes only the canonical machine-relay copy-target condition and its regression/evaluation coverage. Existing relay language/literal-preservation/redaction semantics and all role, authority, lifecycle, Worker, review-result, integration, release, delivery, and recovery semantics remain unchanged.
- Packaged runtime contents remain structurally identical to v1.2.2: only `SKILL.md` and `references/eval-scenarios.md` differ; no runtime script, domain reference, parser, registry, dependency, or platform-specific behavior is added or changed.
- Repository-only benchmark/equivalence tooling added after v1.2.2 remains outside all distributed Skill archives and does not alter packaged runtime behavior.

## [1.2.2] - 2026-08-31

### Changed

- Machine-relay English now applies to relay prose while identity-bearing and decision-relevant literals (including refs/SHAs, paths, commands, code/error strings, and quoted source-language text whose exact wording matters) stay exact unless an existing safety/redaction rule requires otherwise.
- Independent-review findings now use a severity-neutral record for `BLOCKER`, `REQUIRED`, and `OPTIONAL`, with a neutral finding ID and action wording that does not turn optional advice into required remediation.
- Independent-review completion/verdict semantics are explicit and deterministic: only `COMPLETE / APPROVE`, `COMPLETE / CHANGES_REQUIRED`, and `INCOMPLETE / NOT_ISSUED` are valid; incomplete reviews may still report supported actionable findings without issuing an overall verdict.
- Defensive-security relays now distinguish raw secret disclosure from authorized credentialed access through existing approved secret/runtime mechanisms, reducing unnecessary refusal pressure without weakening secret-handling or provider/platform safety boundaries.

### Runtime compatibility

- No lifecycle/status/state namespace, ProjectAuthority/ScopedAuthorization rule, approval/action-effect gate, Worker assignment model, integration/release/delivery semantic, parser, registry, or external dependency changes.
- The canonical owners remain `SKILL.md` for relay transport, `review-integration.md` for review result semantics, and `engineering-quality.md` for defensive-security continuation; local Worker/continuity reminders now reference the canonical transport rule instead of duplicating it.

## [1.2.1] - 2026-08-30

### Added

- A canonical machine-relay transport contract: AI-to-AI prompts/results are English by default and become exactly one fenced copy target when human-relayed, while role-specific domains retain payload semantics.
- A structured Worker handoff contract with complete assignment/result identity, explicit performed/not-run validation evidence, and one-block English output without changing `WorkerStatus` or assignment lifecycle semantics.
- A structured independent-review result contract that separates review completeness from verdict and prevents incomplete/unreviewable evidence from becoming a false approval or invented candidate defect.
- Evidence-backed defensive-security relay guidance that continues safely allowed analysis, remediation, and verification when one detail is restricted, without claiming authorization overrides provider/platform policy.

### Changed

- Worker dispatch/correction, independent-review prompt/result, and Master rotation now share one transport rule instead of duplicating language/copyability requirements across domain owners.
- Review relays now carry exact scope/policy limitations and distinguish `COMPLETE + APPROVE|CHANGES_REQUIRED` from `INCOMPLETE + NOT_ISSUED` as result fields rather than new orchestration states.
- Goal/Rule/evaluation traceability covers portable relay behavior, Worker response discipline, incomplete-review handling, and bounded defensive-security continuation.

### Runtime compatibility

- No `TaskState`, `WorkerStatus`, `WriteState`, `DeliveryState`, `MasterBoundary`, authority, action-effect, approval, integration, release, or delivery semantics change.
- No parser, template file, persisted relay registry, external dependency, or blanket security-review ceremony is introduced; direct user-facing language remains user-selected and explicit relay-language requests still override the English default.

## [1.2.0] - 2026-08-21

### Added

- First-class generated distributions for Manus, Qwen, and Claude.ai alongside the existing ChatGPT package, all produced from the single canonical runtime under `skill/`.
- A root `QWEN.md` bootstrap for Qwen environments that receive the repository URL but cannot install the Skill package directly.
- Deterministic platform-package regression coverage proving portable packages exclude OpenAI-only metadata/assets and remain byte-stable across source timestamp changes.

### Changed

- Release validation now builds four platform artifacts from the same commit: `skill.zip`, `github-project-orchestrator-manus.zip`, `github-project-orchestrator-qwen.zip`, and `github-project-orchestrator-claude.zip`, each with a SHA-256 checksum.
- The release publisher now fails closed unless all eight required assets are present and an existing release proves exact tag/SHA/prerelease/asset-byte identity.
- Claude packaging uses the platform-required lowercase `skill.md` entrypoint and a bounded discovery description while preserving the canonical runtime body, references, and scripts.

### Runtime compatibility

- The canonical orchestration runtime is unchanged. Manus, Qwen, Claude.ai, and ChatGPT share the same `SKILL.md` behavior, references, scripts, authority model, recovery model, review rules, and release semantics.
- Platform adaptations are restricted to packaging, discovery, installation, and tool-capability boundaries; no platform-specific manager-state files or orchestration forks are introduced.

## [1.1.2] - 2026-08-20

### Added

- A directly routed `engineering-quality.md` runtime domain selects only engineering concerns material to the current change and carries them through implementation/evidence without introducing a universal checklist, persisted concern state, or new approval gate.
- Production diagnosability guidance now covers proportional logging severity/context/correlation, controlled runtime diagnostics, diagnostic-versus-audit logging, sensitive-data minimization/redaction, telemetry noise/retention/access/cost, and metrics/traces/health/alerts only when they materially improve detection or diagnosis.
- Conditional implementation guidance now covers resilience/failure handling, privacy, capacity/resource/cost behavior, configuration/environment discipline, user-facing accessibility/error/loading/localization/timezone concerns, and credible restore/recovery when those surfaces are relevant.

### Changed

- `G05`, `G06`, `G07`, and `G11` trace through the new canonical `ENGINEERING-CONCERNS-PROPORTIONAL` rule while preserving existing Goal/Rule ownership and reuse of current regression guards.
- CI/automation fitness is now explicit but remains evidence-triggered under the existing `ARTIFACT-FITNESS` model: inspect trigger scope, duplicate work, concurrency/superseded runs, permissions, critical-path latency, matrix/caching payoff, resource cost, retention, maintainability, and discoverability only when current evidence justifies it.
- Current-runtime validation requires the new domain to remain directly routed from `SKILL.md` without retroactively requiring it in the immutable `v1.0.0` baseline.

### Fixed

- Release automation no longer starts the write-capable publication job for ordinary validated `main` changes whose `VERSION` is unchanged; intentional version changes and manual dispatches still use the exact fail-closed tag/SHA/assets publisher.
- Workflow concurrency now separates PR validation from release publication: superseded PR validations can be canceled, `main`/manual validations are not placed in one replaceable pending slot, and write-capable publication jobs serialize with queued preservation so a version-bump release intent cannot be silently discarded by a later push.

### Runtime compatibility

- `v1.1.2` adds no lifecycle/status/state dimension, no `EngineeringConcerns` contract field, no blanket logging/telemetry/testing/documentation requirement, and no human confirmation gate.
- Existing FAST/FULL selection, ProjectAuthority/ScopedAuthorization, Worker scope/ownership, Master stop/continuation, review freshness, release/delivery state, zero-chat recovery, and immutable `v1.0.0` baseline semantics remain unchanged.
- Routine/localized work with no material concern trigger preserves its current `CoordinationBaseline` and may use the existing FAST path when FAST criteria independently fit; required quality concerns are addressed proportionally rather than deferred merely to make delivery appear faster.

## [1.1.1] - 2026-08-18

### Fixed

- Healthy pending CI/check/deployment dependencies no longer force a one-re-read `MasterBoundary.BLOCKED` stop when the runtime can safely continue with bounded, non-tight autonomous rechecks or a real resume primitive.
- Pending external work now freezes only actions that actually depend on its result, so independently executable source/diff/acceptance review and other outcome-linked work are not unnecessarily serialized behind CI.
- Canonical design vocabulary now uses `ExecutionStrategy=SELF_EXECUTE`, and delivery eval language uses `DeliveryState.PENDING` instead of the legacy `PENDING_DELIVERY` spelling.

### Added

- Sentinel regression tests proving repository preflight does not execute configured `core.fsmonitor` or active tracked-path `filter.<driver>.clean` / `filter.<driver>.process` helpers, while preserving safe complete or explicit incomplete/fail-closed semantics.

### Changed

- The public README is reorganized around value, intended users, installation/update, practical startup usage, operating expectations, version/license, and links to deeper development evidence instead of exposing internal architecture as the primary path.
- Phase 7 benchmark documentation now explicitly marks the `v1.1.0-rc.1` traces as historical evidence so they cannot be mistaken for candidate-current proof of the `v1.1.1` continuation policy.

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
