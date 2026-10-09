# Changelog

## [2.0.1] - 2026-10-09

### Changed

- Rewrote dense always-loaded Core rules as shorter imperative sentences while preserving outcome, authority, evidence, mutation, safety, progress, ownership, and recovery semantics.
- Anchored owner-level/high-consequence decisions in one runtime owner around product/business policy, durable architecture/public compatibility contracts, security/access, stateful migration/data loss, production/release/infrastructure target, public exposure, availability, or difficult/irreversible rollback posture, significant cost/legal/compliance, and explicit risk acceptance.
- Added a platform-neutral capability-discovery path: inspect current tools/connectors/actions, prefer the authoritative native route, try reasonable supported equivalents, and only then treat the capability as unavailable.
- Replaced the MachineRelay pseudo-predicate with four direct transport checks while preserving one complete self-sufficient copy block, exact identity literals, and safe fencing.
- Improved Claude.ai discovery metadata within the 200-character limit so start/continue/finish, cross-chat recovery, and Worker-assignment triggers remain discoverable; the documented lowercase `skill.md` Claude.ai adapter remains unchanged.

### Removed

- Removed the pre-v1.7 `skill/scripts/contract_check.py` compatibility validator, its Phase 2 test, CI invocation, structural requirement, and legacy Worker-dispatch compatibility prose. Historical release notes remain historical evidence, not current runtime behavior.

### Deliberately unchanged

- Worker `Base SHA`, `Start HEAD`, and `Checkpoint HEAD` semantics remain intact. They load only for explicit Worker flows, and their distinct generation-start vs correction/resume roles provide more recovery/staleness value than the small token reduction from collapsing them.

## [2.0.0] - 2026-10-09

### Major generation change

- This release is designated **v2.0.0** because the runtime/control-plane architecture was comprehensively rebuilt, even though G01-G16, supported distribution targets, and intended high-consequence behavior remain preserved.

### Changed

- Rebuilt the orchestration runtime around a compact always-loaded kernel plus event-triggered specialist references, preserving G01-G16 while materially reducing prompt/context and decision overhead.
- Replaced routine orchestration labels and repeated process ceremony with direct outcome, authority, evidence, progress, validation, and ownership invariants; retained exact identity and gate semantics where stale, cross-repository, destructive, release, or false-completion errors are consequential.
- Shifted ordinary development toward coherent implementation batches, targeted high-signal checks during active coding, required broad/exact-candidate validation near stability, and reruns only for invalidated or policy-bound evidence.
- Tightened repository/tool-content trust: legitimate scoped requirements and repository instructions remain usable, while arbitrary embedded text cannot become higher-level agent instruction or authorization.
- Made ordinary Master status output observational rather than a workflow boundary, so safe useful work continues without artificial `continue` nudges or promises of later work.
- Clarified MachineRelay transport so the relay block is self-contained and destination-focused while optional current-user explanation may remain outside the block.
- Renamed the ChatGPT-facing Skill display metadata from **GitHub Engineering Project Manager** to **GitHub Project Orchestrator** and updated the short description to reflect planning, implementation, review, recovery, release, and durable continuity.

### Runtime and coordination

- Reduced the ordinary runtime from 22,665 whitespace-separated words in v1.6.3 to about 7.6k words while keeping all 16 canonical Goals mapped to current runtime owners.
- Consolidated canonical guarantees to 33 behavior-oriented Rules and 38 behavior scenarios, removing historical representation/state vocabulary as an acceptance authority while preserving high-consequence semantics.
- Kept Worker assignment identity, status precedence, correction/resume checkpoints, independent-review completeness/verdict semantics, review freshness, release/delivery proof, recovery, and multi-repository authority boundaries explicit.
- Strengthened zero-chat continuity in both directions: non-recoverable decision-critical state is persisted in its natural owner as it arises during work, and replacement Masters recover only decision-relevant current state from durable project systems.
- Removed remaining low-value duplicate runtime prose while retaining intentional router/owner and verification overlaps required for progressive loading and high-consequence checks.

### Validation and distribution

- Issue #145 and PR #146 own the simplification, acceptance criteria, audits, and review history.
- The release workflow validates Goal/Rule/evaluation traceability, runtime budgets, compatibility/safety helpers, release tooling, clean runtime source, and exact candidate packages for every supported distribution.
- Release publication remains fail-closed: the v2.0.0 tag, release commit, prerelease state, and every required ZIP/checksum asset must match the exact published candidate.
- No empirical claim of universal model-quality, latency, or token-cost improvement is made; measured repository/runtime size reduction and deterministic validation are the evidence recorded for this release.
- The ten-platform distribution matrix remains unchanged and every package continues to be generated from the single canonical `skill/` runtime.

## [1.6.3] - 2026-10-03

### Added

- Added a bounded, provider-neutral consultation path for material unresolved interface judgment or critique. GitHub Project Orchestrator remains the project/repository/integration/release owner; a compatible interface specialist owns only the active interface decision/review, then control returns immediately to the Orchestrator or assigned implementation/platform owner.
- Added explicit anti-loop and Worker boundaries for composed interface work: already-returned implementation latitude continues locally, a returned packet never self-triggers another consultation, and out-of-contract Worker questions stay on the existing Worker status/contract-revision path.

### Changed

- Kept specialist invocation materiality-based rather than UI-keyword-based: trivial presentation edits, settled interface intent, and implementation inside returned latitude do not trigger consultation.
- Deduplicated interface-decision packet ownership after the cross-Skill audit. Product Interface Designer remains the sole owner of the exact packet schema and field semantics; Orchestrator consumes the canonical packet while retaining only caller-relevant behavior such as implementation latitude, unresolved-assumption routing, authority boundaries, return control, and fallback.
- Removed the closed-world exact six-field schema mirror and exact-field validation from Orchestrator, so compatible provider-owned packet evolution does not create artificial caller staleness. No second packet format or copied Product Interface Designer rulebook was introduced.

### Compatibility and validation

- Issues #140 and #142 / PRs #141 and #143 own the implementation, audit, and rationale. The final runtime is `main@26f6d1b3020783d1e8fbb03cbfdf3ab20b568d66`.
- Product Interface Designer compatibility was rechecked against current `AChWorks/product-interface-designer@468e6cf1ee68edca91f3a01d45fad7257f283ae8`; its latest composition/discovery work explicitly makes no packet/schema change.
- Canonical inventories are 69 rules, 16 goals, 126 scenarios, 13 direct references, and 30 state tokens. No new Rule ID, Goal ID, role, approval gate, lifecycle/state namespace, Worker status, Master boundary, or packet field was added.
- Exact-head PR #143 validation run `37083094583` passed after replacing one phrase-fragile test anchor with a semantic ownership guard; post-merge main run `37083185684` passed the full validation workflow.
- Current main validation passed Skill validation, traceability/duplication checks, runtime equivalence, benchmark/scorer controls, Phase C composition, model-trial tooling, deterministic canonical/platform packaging, publisher tests, immutable baseline verification, and runtime cleanliness.
- The release preparation changes only `VERSION`, this changelog, and the README version label; the audited runtime remains byte-identical to the validated integrated implementation.

### Distribution

- The existing ten-archive release matrix remains unchanged: canonical `skill.zip` plus nine platform-specific packages, each with a matching SHA-256 checksum.
- The current validated runtime builds canonical `skill.zip` deterministically as `sha256=ed966b6b02a06051a84562af6f7e7d3b417cbeb8c972ca6ad521683a7c3dfd39`; the version-only release preparation does not alter package contents.
- Previously installed Skills are not automatically replaced by this publication.

## [1.6.2] - 2026-10-01

### Fixed

- Routed both Master and Worker to the existing execution/supply-chain safety guidance before executing untrusted candidate code. This trigger alone does not activate full review/integration or extend Worker authority.
- Completed optimistic-concurrency guidance with documented, available server-enforced identity/revision preconditions. Rejections require reconciliation, partial guards protect only their documented identities, and unsupported operations retain the existing non-atomic fallback and risk gates without fabricated API support.
- Clarified evidence reuse against the exact proved code/object surface and unchanged material assumptions: unrelated SHA movement alone does not invalidate that proof or turn it into a fresh run on another candidate. Candidate-bound mandatory checks remain required.
- Kept Draft/Ready tied to actual candidate maturity and repository policy rather than external-wait/status-only CI retriggers; required validation is consumed at the point required by policy, not an invented immediate broad run after every interim edit.

### Compatibility and validation

- Issue #137 / PR #138 own the bounded implementation and its rationale. Existing rule owners, approval boundaries, Worker isolation, unknown-write handling, release/recovery semantics and project-specific CI requirements remain intact.
- No new Rule ID, Goal ID, Eval ID, role, state, runtime reference, helper, execution-time checklist or evidence registry was added. Canonical inventories remain 69 rules, 16 goals, 122 scenarios and 12 direct references.
- The four operational files gained 132 whitespace-separated words in total, including 17 in the entrypoint. Four existing scenarios E/M/BU/DM were extended; the existing Phase 6 harness adds one positive check and twelve small negative mutation fixtures. These protect text/structure, not measured model performance.
- Implementation CI runs `36911508651` and `36911787721` passed. The release preparation changes only VERSION, this changelog and the README version label; the validated runtime is unchanged.
- The improvement claim is narrower decision ambiguity and better-aligned safety/validation timing. No live-model trial, universal reliability gain or measured latency reduction is claimed.

### Distribution

- All ten supported platform archives and matching SHA-256 checksums continue to be built from the same canonical runtime and verified by the existing publisher. Previously installed Skills are not automatically replaced.

## [1.6.1] - 2026-10-01

### Fixed

- Prevented Issues/authoritative work items from being treated as complete merely because an intermediate PR merged, the item is already Closed/DONE, or a sibling completed while accepted completion criteria, dependencies, target-branch CI, or other required post-integration proof remain unsatisfied or unknown.
- Made persisted acceptance checkboxes evidence-derived: only verified satisfied criteria are marked complete; required remainder stays on the same active outcome and cannot be demoted to optional follow-up merely to permit closure.
- Added bounded recovery for premature closure: when authoritative evidence shows required criteria still pending, the stale closed presentation is reconciled/reopened when authorized and execution continues from the unmet criterion.
- Clarified `DeliveryRequirement=INTEGRATION_ONLY` across Task Contract, governance, and release semantics: it removes a separate delivery predicate only after the accepted work's own completion criteria and required integration/post-integration proof are satisfied.

### Runtime compatibility and optimization

- Reused the existing `POST-INTEGRATION-RECONCILE` Rule and `review-integration.md` canonical owner; no new Rule ID, Goal ID, lifecycle/status namespace, Role, approval gate, router edge, helper, persistence mechanism, or parallel completion owner was introduced.
- Kept the always-loaded `skill/SKILL.md` byte-identical to v1.6.0. The added runtime wording is confined to triggered references, with Scenario `DR` providing the distinct regression case for partial-integration/premature-closure behavior.
- Existing project-completion/outcome-stability scenarios remain separate: Scenario `DR` protects work-item presentation/checkbox/auto-close recovery semantics rather than duplicating their general completion rules.
- Canonical inventories are 69 Rule IDs, 122 standalone Eval IDs, and 16 Goal IDs.

### Validation

- Issue #133 / PR #134 implemented the fix; exact-head workflow `36894645646` and post-merge `main` workflow `36894748222` completed successfully.
- The first candidate exposed a hard-coded future Eval-ID fixture collision; the test was corrected at its root to derive the next Eval ID from the current inventory, then the exact corrected candidate passed the full workflow.
- Issue #135 records the final duplication/semantic-efficiency audit, release evidence, exact release identity, and branch cleanup so continuation does not depend on chat history.
- The normal release workflow continues to validate Skill structure/traceability, contract/preflight safety, deterministic lint, runtime equivalence and representation controls, benchmark/scorer checks, Phase C composition, model-trial tooling, release intent/publisher behavior, deterministic canonical/platform packaging, immutable baseline integrity, and runtime cleanliness.

### Distribution

- The ten-platform release matrix remains unchanged; all release archives and matching SHA-256 checksums are generated from the single canonical runtime.

## [1.6.0] - 2026-10-01

### Added

- Added first-ownership support for projects whose exact GitHub repository target does not yet exist: after decision-scoped discovery proves absence, the Master may create the repository only when the existing repository-scope, authority, policy, capability, and material-setting gates permit it, then verifies the remote identity before continuing.
- Added a bounded project-start sequence that resolves project definition and repository target together, establishes or reuses one canonical root project specification, reconciles it with repository reality, and performs only proportional bootstrap work that materially helps safe execution or recovery.

### Changed

- Clarified root-spec ownership without adding a parallel documentation system: when no authoritative equivalent exists, `docs/PROJECT-SPEC.md` is the preferred default, while valid existing equivalents are reused rather than renamed or duplicated for convention.
- Clarified that `README.md` is normally the user/developer entry surface rather than a second project-intent owner, while preserving repositories that intentionally use README as their root project specification.
- Reserved remote-repository **creation** terminology for GitHub repository establishment and kept existing local branch/worktree/checkout **provisioning** terminology for workspace isolation, reducing model ambiguity.
- Clarified that the root project specification owns project-level supported-environment/platform commitments and compatibility boundaries, while specialized repository docs own detailed environment/version specifications and engineering-release rules.
- Tightened `ROOT-SPEC-CANONICAL` traceability so its eval anchors remain on the dedicated root-spec scenarios instead of over-claiming the broader first-ownership bootstrap scenario.

### Runtime compatibility

- No new Rule ID, Eval ID, Goal ID, lifecycle/status namespace, Role, `ProjectAuthority` mode, `MasterBoundary`, approval gate, Worker/review/release state, or parallel source-of-truth mechanism was introduced.
- The existing mutation, authorization, capability, bootstrap, and root-spec invariants were reused rather than creating a startup-specific authority or lifecycle model.
- Canonical inventories remain 69 Rule IDs, 121 standalone Eval IDs, and 16 Goal IDs.

### Validation

- PR #128 introduced the first-ownership repository-creation capability and received independent HIGH_ASSURANCE review before integration.
- PR #130 performed the follow-up semantic/source-ownership cleanup; its exact candidate workflow run #365 and post-merge `main` workflow run #366 completed successfully.
- Validation continued to cover Skill structure, contract compatibility, repository preflight safety, deterministic lint, representation controls, benchmark/scorer checks, runtime equivalence, runtime representation experiments, Phase C composition, model-trial tooling, release-intent decisions, deterministic canonical/platform packaging, exact publisher behavior, immutable baseline verification, and clean runtime source.

### Distribution

- The ten-platform release matrix remains unchanged; all release packages and matching SHA-256 checksums continue to be generated from the single canonical runtime.

All notable changes to this project are documented here.

## [1.5.2] - 2026-09-22

### Fixed

- Restored the v1.4.0-era Master-to-Reviewer behavior for user-mediated independent review: when a fresh reviewer chat/model/human is used, the Master emits the complete `INDEPENDENT REVIEW CHAT` relay instead of replacing it with a GitHub/PR/Issue pointer or asking the next chat to reconstruct the request.
- Kept GitHub/PR/Issue state as authoritative review evidence/locators without allowing durable state to substitute for the reviewer relay itself.
- Minimized the restored rule and its evaluation coverage so `independent-review.md` owns only handoff semantics, `relay-transport.md` remains the single transport owner, and Scenario BC / Regression Guard preserve the behavior without duplicate transport wording.

### Runtime compatibility

- No independent-review trigger, reviewer result contract, verdict semantics, integration ownership, Rule ID, lifecycle/state namespace, Worker relay, Master rotation behavior, or transport predicate changed.
- `review-integration.md`, `relay-transport.md`, `SKILL.md`, Rule/Goal maps, and the state model remain unchanged by the final optimization.
- The fix is intentionally limited to the Master-to-Reviewer user-mediated independent-review handoff path and its regression coverage.

### Validation

- PR #124 restored the explicit handoff behavior; PR #125 minimized the runtime/eval wording and merged as `main@026ca2c7f47cb476ae2a73a422575256915c493f` from candidate `45c2bbad0d8d0ebfd49f95dfa69c3bbee6eebc3f`.
- PR #125 exact-head workflow `35664756680` and post-merge `main` workflow `35666131348` completed successfully.
- Deterministic validation continues to enforce direct reviewer-prompt dispatch, Scenario BC coverage, Regression Guard coverage, single transport ownership, runtime equivalence, and deterministic packaging.

### Distribution

- The existing ten-platform release matrix is unchanged; all release archives continue to be generated from the single canonical runtime with matching SHA-256 checksum assets.


## [1.5.1] - 2026-09-21

### Fixed

- Restored the existing MachineRelay transport behavior for emitted `INDEPENDENT REVIEW RESULT` output after the v1.5.0 runtime-structure split by moving the already-existing result-emission activation to the `independent-review.md` result-contract point.
- Removed the later duplicate emission reminder from Master reconciliation, so `relay-transport.md` remains the single canonical transport owner and `independent-review.md` routes result transport exactly once.
- Strengthened the existing regression guard to require result-local MachineRelay classification and routing to `MACHINE_RELAY_OUTPUT_OK(response)` without duplicating the canonical transport predicate.

### Runtime compatibility

- No result schema, verdict semantics, review lifecycle, Rule ID, state namespace, or transport predicate changed.
- `relay-transport.md`, ordinary Master-to-reviewer handoff behavior, Master-rotation/new-Master relay behavior, and `review-integration.md` remain unchanged.
- The fix is intentionally limited to the Reviewer-to-Master `INDEPENDENT REVIEW RESULT` emission path.

### Validation

- PR #121 merged the bounded fix as `main@34b43f36897b58fd2f4093163a50e746343af004` from candidate `52fe63837ab499227a66e2fd38ab3dc8d0cc9789`.
- PR-head workflow `35538645912` and post-merge main workflow `35538671653` both completed successfully.
- Local validation passed `tools/validate_skill.py`, Phase C runtime migration checks, the Phase 6 MachineRelay regression checks, all standalone runnable test scripts, `unittest` discovery, and `git diff --check`.

### Distribution

- The existing ten-platform release matrix is unchanged; release artifacts continue to be generated from the single canonical runtime with matching SHA-256 checksum assets.

## [1.5.0] - 2026-09-19

### Changed

- Reworked the orchestration runtime representation to absorb field-proven throughput lessons without adding new canonical Rule IDs, runtime state/lifecycle namespaces, Risk/Assurance modes, or standalone eval IDs.
- Reduced routine hot-path loading and duplicated decision prose by moving independent-review and MachineRelay transport details behind direct event-driven references, compressing Recovery/review/Worker decision structures, and retaining the trigger coverage and long-reference tables of contents required for reliable progressive loading.
- Added right-sized minimum-meaningful-slice guidance, cohesive partial-PR Task Contract continuity, conditional Draft/Ready maturity guidance, stale-sensitive acceptance serialization, and isolation-preserving CI sharding guidance without suppressing valid independent parallel work.
- Corrected `MACHINE-RELAY-PORTABLE` canonical ownership to `relay-transport.md` and added exact fail-closed representation controls so the intentional relocation cannot become a generic Rule-owner bypass.

### Validation

- PR #115 reconciled cleanly with `v1.4.0` main using merge commit `6f6e1b936acd26d7fcd603ae4ed01d3f47e8066e`; the current-main reconciliation changed only 10 platform/release files and no file under `skill/`.
- Exact reconciled-head workflow `35431139594` completed successfully, including runtime equivalence, Phase C, benchmark/scorer, deterministic canonical/platform packaging, exact publisher, immutable-baseline, and clean-runtime checks.
- PR #115 merged as `main@1a4493a72f1a14c0beb71946735054a19eb6b52d`; post-merge main workflow `35431190176` also completed successfully.
- The runtime lineage received independent HIGH_ASSURANCE review before the final remediation. The post-review remediation changed only design/evidence/validation-control files, and the later current-main reconciliation also changed no Skill runtime wording; under the Owner-approved integration criterion, no redundant independent re-review was required for those non-runtime-only deltas.
- Canonical inventory remains 69 Rule IDs and 121 standalone eval IDs with unchanged runtime state/value sets. The release makes no unsupported numerical claim about model speed, cost, or accuracy.

### Distribution

- The ten-platform distribution matrix introduced in v1.4.0 remains intact; every release artifact continues to be generated from the same canonical runtime with matching SHA-256 checksums.

## [1.4.0] - 2026-09-19

### Added

- Added deterministic portable release packages for Z.ai ZCode, Grok Build, Kimi Code, Google Gemini (Gemini Apps Skills), DeepSeek Harness, and Microsoft Copilot Studio.
- Added root-layout Skill ZIP generation for direct Gemini Apps and Copilot Studio uploads while reusing the existing wrapped `SKILL.md` directory layout for ZCode, Grok Build, Kimi Code, and DeepSeek Harness.
- Added regression coverage for the complete platform inventory, deterministic package bytes, exact canonical `SKILL.md` preservation, wrapper-vs-root layout, OpenAI-only metadata exclusion, and fail-closed release-asset completeness.

### Runtime compatibility

- The canonical runtime under `skill/` is unchanged. No platform-specific orchestration, authority, review, Worker, recovery, integration, or release semantics are introduced.
- New platform adaptations are restricted to archive layout, discovery/install documentation, release asset generation, and exact publisher verification.

### Distribution

- The release pipeline now builds ten platform distributions and matching SHA-256 checksums from one commit: ChatGPT, Manus, Qwen Code, Claude.ai, Z.ai ZCode, Grok Build, Kimi Code, Google Gemini, DeepSeek Harness, and Microsoft Copilot Studio.
- Consumer chat surfaces are not misrepresented as file-import targets when first-party documentation exposes the installable Skill format through a separate harness/product surface such as ZCode, Grok Build, Kimi Code, DeepSeek Harness, or Copilot Studio.

## [1.3.7] - 2026-09-18

### Fixed

- Added an explicit persistent `RepositoryMutationScope` boundary under the existing `AUTHORIZATION-SCOPED` owner so related, linked, dependent, discovered, or merely accessible repositories never inherit mutation authority.
- Kept cross-repository coordination and read-only dependency inspection available while requiring out-of-scope writes to become exact handoffs for the target repository's authorized Master/owner.
- Made direct and deterministic cross-repository mutation targets part of the same pre-action authorization decision, preventing an authorized action in repository A from silently causing an unauthorized write in repository B.
- Clarified that exact action-specific `ScopedAuthorization` can cover only the exact repository/action it names where the canonical matrix permits it; it never persistently widens `RepositoryMutationScope` or later Master-rotation scope.
- Persisted exact Worker `Repository` identity before dispatch under the existing `ASSIGNMENT-IDENTITY` owner, and reused that identity for execution, pre-push validation, handoff, correction/resume, and zero-chat Master recovery.

### Validation

- Issue #106 / PR #107 completed exact-candidate GitHub Actions run `35302533355` successfully, including contract compatibility, repository preflight, deterministic lint/traceability, representation controls, runtime equivalence/prototypes, benchmark, Phase C composition, model-trial tooling, release-intent, packaging/publisher, immutable-baseline, and clean-runtime checks.
- A fresh separate HIGH_ASSURANCE independent review of candidate `f6183e49280a1d8811639f53c98b5064b0c944d9` returned `COMPLETE / APPROVE` with no findings after independently confirming both prior REQUIRED findings and the predicate/decision-flow interaction fix were resolved.
- All 12 requested repository-scope decision variants passed independent semantic review, including one-off non-persistent authorization, deterministic A-to-B effects, pre-handoff Worker repository recovery, and stale-repository detection.
- PR #107 merged as `main@d4352d9a8db1428de662d520c8da63717aa408af`; post-merge main validation run `35303488962` completed successfully.

### Runtime compatibility

- No new Role, lifecycle/status namespace, ProjectAuthority mode, Worker status, release/delivery state, or parallel repository-permission Rule was introduced.
- `AUTHORIZATION-SCOPED` remains the canonical repository-authorization owner, while `ASSIGNMENT-IDENTITY` remains the canonical persisted Worker assignment owner.
- Existing FAST/FULL selection, effect/approval gates, independent-review semantics, Worker lifecycle, MachineRelay transport, release behavior, and ordinary authorized single-repository autonomy remain intact.

### Distribution

- ChatGPT, Manus, Qwen, and Claude.ai packages continue to be generated from the single canonical `skill/` runtime and published together with matching SHA-256 checksum assets by the exact-SHA fail-closed release workflow.

## [1.3.6] - 2026-09-17

### Fixed

- Made security-sensitive independent/read-only review evidence acquisition explicitly source/diff/evidence-based so reviewers use authoritative code, repository-owned existing tests, current CI/log/artifact evidence, and safe read-only inspection instead of inventing new adversarial payloads or synthetic security probes merely to demonstrate robustness.
- Made insufficient inspectable security evidence produce an evidence-backed review finding or explicit incomplete-review limitation rather than manufactured proof or silent approval, while preserving the same security acceptance bar and provider/platform policy boundary.
- Preserved bounded defensive regression testing for explicitly scoped implementation/remediation when it is required, authorized, isolated/reversible, and policy-permitted; the reviewer-only evidence boundary does not suppress legitimate security engineering.

### Validation

- Issue #101 / PR #103 completed full local workflow-equivalent validation, exact-head GitHub Actions, a separate HIGH_ASSURANCE independent review with `COMPLETE / APPROVE` and no findings, and successful post-merge `main` validation in run `35186429792`.
- Added deterministic cross-surface regression coverage (`PASS defensive-security-review-evidence-boundary`) spanning the project specification, canonical engineering-quality owner, independent-review handoff, existing `DJ` eval, and Rule Map traceability.
- The integrated runtime keeps `DEFENSIVE-SECURITY-CONTINUATION` as the single canonical Rule owner and adds no parallel security-policy layer.

### Runtime compatibility

- No lifecycle/status namespace, Role/ProjectAuthority/ScopedAuthorization rule, effect gate, Worker lifecycle, FAST/FULL selector, Task Contract persistence rule, integration/release state, or external runtime dependency is introduced.
- Existing repository-owned security tests remain reviewable/runnable, and implementation/remediation behavior remains available inside the accepted authorization and platform-policy boundary.

### Distribution

- ChatGPT, Manus, Qwen, and Claude.ai packages continue to be generated from the single canonical `skill/` runtime and published together with matching SHA-256 checksum assets by the exact-SHA fail-closed release workflow.

## [1.3.5] - 2026-09-15

### Changed

- Right-sized orchestration around a **minimum meaningful slice** so reviewable sibling work that shares one accepted behavior and materially aligned dependency/ownership/risk/rollback/release/validation boundaries can travel together, while materially different acceptance/control boundaries remain split.
- Reframed validation as a **minimum sufficient evidence plan**: remove duplicate proof without dropping independent acceptance, risk, compatibility, security/data, repository-policy, or current-candidate CI guarantees.
- Made remediation review delta-focused without weakening freshness: every changed candidate that requires independent review still needs a fresh exact-candidate verdict, prior verdicts never transfer, and review widens whenever a delta can invalidate assumptions on unchanged surfaces.
- Added event-driven phase cutlines that preserve all accepted completion work while moving only newly discovered outside-gate non-blocking work to follow-up, and expanded anti-spin to successful-but-nonprogressing assurance loops.

### Validation

- Added direct adversarial scenarios `DL`-`DP` for work-package right-sizing, proportional validation/evidence reuse, delta-focused fresh re-review, phase-cutline scope preservation, and assurance-overhead anti-spin.
- Extended existing Rule Map anchors to those scenarios without introducing a new Rule ID, lifecycle/status namespace, or canonical owner.
- The final semantic package was reconstructed twice with byte-identical `skill.zip` output before repository integration validation; exact-head repository CI and the existing HIGH_ASSURANCE review/integration gates remain mandatory for the release candidate.

### Runtime compatibility

- Existing authority/effect gates, Worker lifecycle, FAST/FULL selection, contract persistence, review separation, integration controls, and release/delivery semantics remain intact.
- The changes reduce repeated Issue/PR/CI/review and environment-mismatch overhead only when doing so preserves accepted scope, reviewability, independent guarantees, repository-required gates, and exact-candidate review freshness.
- No universal PR-size, test-count, retry-count, or elapsed-time threshold is introduced.

### Distribution

- ChatGPT, Manus, Qwen, and Claude.ai packages continue to be generated from the single canonical `skill/` runtime and published together with matching SHA-256 checksum assets by the exact-SHA fail-closed release workflow.

## [1.3.4] - 2026-09-14

### Changed

- Made repository/workspace handling explicitly reuse-first: reuse a suitable existing repository/worktree before provisioning another, prefer `git worktree` when branch/task isolation is sufficient, and use a separate full clone only when repository-level isolation or tooling genuinely requires it.
- Made cleanup of task-created checkouts/worktrees, generated artifacts, test environments, and containers explicitly ownership- and state-safe so temporary resources are removed only after their purpose ends and no useful uncommitted, unpushed, ambiguous, or unrelated state can be lost.

### Validation

- A repository-wide runtime audit confirmed the new workspace-provisioning and disposable-resource decisions have one canonical owner in `skill/SKILL.md`; existing Master, Worker, continuity, and authority references retain only their distinct identity/isolation/recovery responsibilities rather than duplicating the new policy.
- PR #97 and the post-merge `main` workflow both completed the full deterministic validation, runtime-equivalence, benchmark, packaging, publisher, immutable-baseline, and runtime-cleanliness suites successfully before this release preparation.

### Runtime compatibility

- This patch specializes the existing `MUTATION-IDEMPOTENT` and `PROTECT-UNRELATED` invariants; it adds no lifecycle/status namespace, canonical Rule ID, authority/gate change, FAST/FULL or persistence change, review/release-state change, external runtime dependency, or parallel cleanup subsystem.

### Distribution

- ChatGPT, Manus, Qwen, and Claude.ai packages continue to be generated from the single canonical `skill/` runtime and published together with matching SHA-256 checksum assets by the exact-SHA fail-closed release workflow.

## [1.3.3] - 2026-09-03

### Changed

- Added a compact supplemental retrieval index for the 24 evaluation scenarios not reachable through existing Rule/Goal eval anchors, while keeping Rule/Goal IDs as seed anchors rather than treating the supplemental index as exhaustive semantic ownership.
- Added explicit self-modification retrieval guidance: combine affected Rule/Goal anchors with matching supplemental scenarios, exact predicate/state/helper/field searches, relevant Regression Guard clauses, and `DK` for representation-only rewrites; widen the set whenever relevance is uncertain.
- Kept all 115 evaluation scenario bodies and their physical ordering intact; normal project runtime routing and canonical Rule/Goal/state/gate behavior are unchanged.

### Fixed

- Closed a deterministic regression-control gap where removing the accepted `DK` scenario from v1.3.2 could still pass both `validate_skill.py` and the historical runtime-equivalence check. Current releases now retain an immutable v1.3.2 eval-inventory control in addition to the historical v1.2.2 semantic baseline.
- `validate_skill.py` now requires every Rule/Goal-unanchored scenario to appear in the supplemental retrieval surface, rejects missing/unknown/duplicate coverage, and prevents the bounded pre-v1.3.2 compatibility flag from bypassing current inventories.
- Centralized eval-heading discovery in a bounded shared Markdown parser and hardened it against headings hidden in comments, fenced code, supported raw-HTML blocks, cross-line heading tricks, titleless headings, indentation ambiguity, and CDATA case mistakes.

### Validation

- Independent HIGH_ASSURANCE review of PR #95 completed with `APPROVE` after multiple adversarial remediation rounds covering hidden Markdown, raw HTML, GFM fence boundaries, physical-line parsing, CDATA handling, and non-empty eval titles.
- The former v1.3.2 failure mode was reproduced again before release: deleting `DK` passed both old controls, while the new current-control path rejects equivalent scenario removal; an added unanchored scenario is also rejected until retrieval coverage is registered.
- Exact merged-tree validation passes with 115 eval scenarios, deterministic Skill validation, runtime-equivalence controls, regression suites, packaging tests, and runtime-cleanliness checks. No controlled live-model speed/accuracy percentage claim is made.

### Runtime compatibility

- This patch improves Skill self-modification/evaluation retrieval and release-time regression assurance; it does not change ordinary Master/Worker orchestration semantics, authority gates, lifecycle namespaces, review/integration behavior, release/delivery behavior, or normal routing.
- The distributed Skill adds only the small retrieval index/guidance in `references/eval-scenarios.md`; the parser, current-control logic, and expanded adversarial tests are repository tooling and are not part of the normal always-loaded runtime path.

### Distribution

- ChatGPT, Manus, Qwen, and Claude.ai packages continue to be generated from the single canonical `skill/` runtime and published together with matching SHA-256 checksum assets by the exact-SHA fail-closed release workflow.

## [1.3.2] - 2026-09-03

### Changed

- Re-expressed cold-recovery orientation as an explicit four-step execution-identity -> truth/live-evidence -> control-state -> active-workstream sequence, with Triggered depth kept as a conditional interrupt rather than a mandatory extra phase.
- Decomposed the dense Master `IMPLEMENT` cell into independently applicable correctness/root-cause, architecture-fitness, structural-change, compatibility, scope, version-sensitive-contract, and performance facets; all applicable facets still apply and row order creates no precedence.
- Separated human handling into orthogonal interaction-content and escalation-timing surfaces while keeping canonical `MASTER_STOP(...)` terminality authoritative, so ordinary, material-decision, urgent-risk, project-wide, and missing-capability cases compose without inventing a second stop owner.
- Strengthened the lossless-representation methodology and regression coverage so structured rewrites must preserve independently operative rules, conditions, qualifiers, defaults, overrides, scope, and ownership without inventing exclusivity, precedence, exhaustiveness, or shared activation.

### Validation

- An independent HIGH_ASSURANCE adversarial review compared exact `v1.3.1@f8dfdbd95bb9e2ccabd4244d921613bf94c1a9b9` semantics with the integrated representation candidate and returned `COMPLETE / APPROVE` with `CURRENT_BETTER`: no lost, narrowed, or broadened protected concepts; no new material implication/precedence/exclusivity; no canonical-owner drift; and no harmful duplication found across the audited runtime/reference surfaces.
- Repository validation, exact-head CI, deterministic packaging, immutable-baseline checks, and runtime-cleanliness checks remain supporting evidence; no controlled live actual-model A/B percentage claim is made.

### Runtime compatibility

- This is a representation-focused patch release. It introduces no new lifecycle/status namespace, `ProjectAuthority`/`ScopedAuthorization` rule, approval-effect gate, Worker lifecycle, FAST/FULL selector, review/integration rule, release/delivery state, parser, registry, or external runtime dependency.
- The protected orchestration decisions from v1.3.1 remain decision-equivalent while clause segmentation, ordering reconstruction, mixed-purpose parsing, and human-timing composition are made more explicit.
- Further refactoring of these reviewed surfaces should now be evidence-triggered by observed application failure or recurring friction rather than continued for visual consistency or theoretical elegance.

### Distribution

- ChatGPT, Manus, Qwen, and Claude.ai packages continue to be generated from the single canonical `skill/` runtime and published together with matching SHA-256 checksum assets by the exact-SHA fail-closed release workflow.

## [1.3.1] - 2026-09-02

### Changed

- Reframed architecture handling around **fitness for accepted work** rather than preservation or novelty: reuse existing architecture when it remains fit, and permit bounded structural change when correct implementation requires it or current evidence shows material net benefit to that accepted work.
- Expanded the implementation rule from root-cause-only structural exceptions to accepted-requirement-aware engineering, so a legitimate feature can evolve an internal boundary without first pretending the existing structure is itself a defect.
- Reconciled `G05`, `G06`, and `G15` traceability and Scenario `BA` so architecture-fit implementation, engineering-system enabling work, and proactive improvement remain distinct owners instead of overlapping objectives.

### Fixed

- Removed the over-broad architecture-preservation wording that could bias the Master toward keeping an unfit internal boundary or internal contract merely because it already existed.
- Tightened the architecture-fitness hot path so cross-task `repeated outcome-linked work` no longer becomes an extra refactor justification inside normal `IMPLEMENT`; recurring delivery/review/analysis friction remains covered by the existing outcome-linked enabling-work path with remaining-outcome and near-term-payback constraints.
- Bound historical Phase C scope/fingerprint checks to the immutable published `v1.3.0@52a9c56210e9ecd1bbc91170de40131658dbd4e9` snapshot rather than future current HEAD, so later legitimate Skill evolution cannot create a false historical-composition failure while current semantic guards continue to inspect current runtime behavior.

### Runtime compatibility

- No new lifecycle/status namespace, `ProjectAuthority`/`ScopedAuthorization` rule, approval-effect gate, Worker lifecycle, FAST/FULL selector, review/integration rule, release/delivery state, parser, registry, or external runtime dependency is introduced.
- Existing architecture remains preferred when fit; theoretical elegance alone is not sufficient reason to refactor, and material adjacent improvements remain outside accepted scope unless separately accepted.
- No controlled live actual-model A/B performance claim is made. Release confidence is based on source-grounded adversarial behavior review plus deterministic repository validation, CI, packaging, and exact release-identity checks.

### Distribution

- ChatGPT, Manus, Qwen, and Claude.ai packages continue to be generated from the single canonical `skill/` runtime and published together with matching SHA-256 checksum assets by the exact-SHA fail-closed release workflow.

## [1.3.0] - 2026-09-02

### Changed

- Completed the Phase C lossless runtime decision-representation migration across the selected P1-P5 families: runtime-dimension stability/non-implication locality, Worker assignment-owner deduplication, discriminated pending-job continuation, one canonical `WriteState.UNKNOWN` recovery algorithm, and progressive cold recovery with conditional triggered depth.
- Hardened MachineRelay rendering with one canonical pre-send `MACHINE_RELAY_OUTPUT_OK(response)` predicate while keeping domain payload ownership singular and ordinary direct user-facing responses outside the relay predicate.
- Reframed actual model/runtime A/B trials as optional corroboration under the accepted proof policy; deterministic equivalence, source-grounded structural evidence, protected-behavior gates, and independent review remain required without mislabeling structural evidence as measured model performance.
- Added auditable model-trial runner/scorer infrastructure, Phase C migration evidence/experiments, composition guards, and broader CI coverage for the migrated representation families.

### Fixed

- `CoordinationBaseline=LIGHTWEIGHT` is now selected from actual coordination shape: migration, production/release, or security/data concerns require `STANDARD` only when they create material coordination needs, while their independent Risk/Assurance/Execution/Release controls remain fully applicable.
- Retired only the obsolete candidate-era Phase C changed-path equality so future legitimate Skill evolution does not fail a historical composition assumption; P1-P5/#64 fingerprints, semantic guards, and state-namespace protections remain intact.
- Reconciled release-facing documentation so the public README reports the current release and historical migration/design documents no longer present closed readiness work as current.

### Runtime compatibility

- This release is intentionally lossless with respect to protected orchestration semantics: no new lifecycle/status namespace, ProjectAuthority/ScopedAuthorization expansion, approval-effect shortcut, Worker lifecycle, delivery-state model, integration/release gate, parser, registry, or external runtime dependency is introduced.
- `LIGHTWEIGHT + FULL`, `LIGHTWEIGHT + HIGH_ASSURANCE`, and other independently valid dimension combinations remain supported when their canonical criteria require them.
- The immutable `v1.2.2@f98e8a242c720931e34aa7c4e8a799090e3d0495` representation baseline remains historical comparison evidence and is not rebased to this release.
- No controlled live actual-model A/B performance claim is made; the release evidence is semantic, structural, deterministic, CI/package, and independent-review evidence.

### Distribution

- ChatGPT, Manus, Qwen, and Claude.ai packages continue to be generated from the single canonical `skill/` runtime and published together with matching SHA-256 checksum assets by the exact-SHA fail-closed release workflow.

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
