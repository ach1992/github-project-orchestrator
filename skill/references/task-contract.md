# Task Contract

Use a compact Task Contract when explicit coordination/control improves execution; do not require one merely because code behavior changes. Prefer an existing Issue/authoritative work item when the contract must survive delegation, coordination, material risk, or context loss. For bounded low/medium-risk Master-only work whose goal, acceptance, validation, dependencies, and rollback are already clear from user request + repository evidence, use the implicit fast-path contract.

## 1. Logical lifecycle

Map to existing repository workflow when possible. State names are namespace-qualified so matching tokens in other domains never imply propagation:

`TaskState.DRAFT -> TaskState.BLOCKED | TaskState.READY -> TaskState.IN_PROGRESS -> TaskState.IN_REVIEW -> TaskState.CHANGES_REQUESTED | TaskState.INTEGRATION_READY -> TaskState.INTEGRATED`

Also allow namespaced task states such as `TaskState.CANCELLED`, `TaskState.SUPERSEDED`, and `TaskState.ROLLED_BACK` when applicable. Legacy `MERGE_READY` is the compatibility name for `TaskState.INTEGRATION_READY`; it does not require a PR/merge mechanism when the recognized repository-normal integration path is non-PR.

Delivery is a separate dimension. `DeliveryRequirement=INTEGRATION_ONLY` completes at the required verified integration boundary. When `DeliveryRequirement=DELIVERY_REQUIRED`, track the explicit `DeliveryTarget` and the independent lifecycle `DeliveryState.NOT_STARTED -> DeliveryState.PENDING -> DeliveryState.DELIVERED`, with `DeliveryState.FAILED_OR_UNKNOWN` when evidence is missing or delivery fails. Never infer `DeliveryState` from `DeliveryTarget`, or delivery completion from `TaskState.INTEGRATED`.

## 2. Execution path and contract threshold

`SUBSTANTIVE` means observable behavior/interface/dependency/data/security/operations or review complexity changes materially; `TRIVIAL` means none do. Use this distinction only when it affects delegation, validation, or helper behavior. Neither is a required per-change state, `RiskLevel`, `CoordinationBaseline`, `AssuranceLevel`, FAST/FULL selector, or contract trigger by itself; substantive work may still be safe for Master FAST PATH.

Choose `ExecutionPath=FAST|FULL` with the canonical criteria in `master-cycle.md`, then decide contract form/persistence without conflating those dimensions:

| Situation | Contract / READY behavior |
|---|---|
| FAST Master work with no relevant existing explicit contract | user request + current repository evidence may serve as the implicit contract; no READY artifact |
| FAST Master work already owned by a relevant explicit Issue/contract | reuse and keep that existing contract current; do not create a second contract or promote to FULL merely because the artifact exists |
| FULL Master work | explicit Task Contract + READY before contracted implementation |
| Any Worker dispatch / multi-actor implementation | explicit full compact Task Contract + READY + persisted assignment identity before dispatch |

Persist an explicit contract only when durable identity materially helps delegation, multi-item/cross-session coordination, recovery, unresolved blockers/decisions, material risk, or repository/team policy; otherwise FULL Master work may stay transient. If intent would become unrecoverable, persist only the minimum unresolved intent in its natural owner, reusing an existing work item when suitable. Cohesive partial PRs keep the same persisted contract open; do not close/recreate it for mechanical seams. Close it only when the accepted outcome completes or the contract otherwise legitimately terminates under the existing `TaskState` lifecycle.

## 3. Compact contract schema

When an explicit Task Contract is warranted, include as applicable:

```markdown
Contract Revision: 1

## Goal
<observable outcome and why it matters>

## Scope
- In: ...
- Out: ...

## Acceptance
- [ ] ...

## Validation
- <exact automated checks, reproduction, or manual verification>

## Dependencies
- #... or none

## Risk / Release
Risk: <LOW | MEDIUM | HIGH | CRITICAL plus material notes>
Delivery Requirement: <INTEGRATION_ONLY | DELIVERY_REQUIRED>
Delivery Target: <explicit target when delivery is required; omit when not applicable>
Delivery State: <NOT_STARTED | PENDING | DELIVERED | FAILED_OR_UNKNOWN when persisted here>
```

Use positive integer `Contract Revision` for persisted work that may be delegated/materially revised. Transient explicit Master-only contract may omit it; persist + add revision before Worker dispatch or whenever cross-cycle reconciliation needs identity. Delivery fields need not be duplicated when an existing authoritative release/deployment object already owns them; when they are persisted in the contract, keep `DeliveryRequirement`, `DeliveryTarget`, and `DeliveryState` independent. Optional only when useful: parent/milestone, affected interfaces/data stores, rollback requirement, owner/Worker. Do not copy repo-wide rules into each Issue; link durable rules and use native GitHub relationships when available.

## 4. Acceptance criteria

Criteria must be observable behavior or verifiable engineering properties; define important negative/edge behavior when failure matters. Avoid vague `works correctly`, `clean code`, or `handle edge cases` without stating what must be true.

## 5. Validation strategy

Choose the strongest practical evidence for the change:

| Change | Strong practical evidence |
|---|---|
| bug | reproduce when practical; regression test; relevant suite |
| feature | behavior tests + integration/e2e where boundary requires |
| refactor | preserved behavior with existing/new tests + targeted static checks |
| docs | relevant link/command/example validation |
| config/infra | syntax/plan/dry-run/staging + rollback awareness |
| migration/data | forward behavior, compatibility window, partial failure, rollback/restore/roll-forward proportional to risk |
| security-sensitive | permission/abuse/input/error-path checks + happy path |

Treat validation as a **minimum sufficient evidence plan**, not an inventory of every possible check:

- `Minimum` removes duplicate proof, never an independent acceptance/risk/compatibility/security/data/repository-policy guarantee; every material requirement still needs adequate evidence.
- Prefer fast local discriminating feedback for the changed surface, then rely on repository-required/current CI or other authoritative gates for the broader proof they own. Do not duplicate a broad local suite when it adds no material differential signal.
- Reuse green evidence only while the exact code/object, relevant dependency/config/toolchain/environment assumptions, and the requirement proved remain unchanged; freshness does not mean rerunning unchanged proof for ceremony.

If the current local environment is **proven** unable to execute a required check faithfully (for example a deterministic preflight shows a missing required service/extension, incompatible database semantics are established, or a resource ceiling is reproducible), record that limitation once for the unchanged conditions and use an available compatible authoritative environment/CI route. One ambiguous or plausibly transient failure is not proof of incompatibility. Do not repeatedly invoke the same proven-incompatible local route unless relevant conditions changed.

Never weaken tests/checks to manufacture a pass. Repository-required checks remain mandatory for every candidate identity to which policy binds them; evidence reuse or route substitution never bypasses a required gate.

## 6. Change risk

Use only as much `RiskLevel` classification as controls need:

| Risk | Meaning |
|---|---|
| `LOW` | localized, reversible, small blast radius |
| `MEDIUM` | meaningful behavior/interface change with bounded rollback |
| `HIGH` | material security/auth/data migration/broad compatibility/production stability impact |
| `CRITICAL` | potentially destructive/irreversible, major security exposure, or high production blast radius |

Importance alone does not make risk high. A task may temporarily need `AssuranceLevel=HIGH_ASSURANCE` without changing unrelated work's `CoordinationBaseline`, assurance, or Authority.

## 7. Contract revision

Increment only when active work materially changes outcome, scope, acceptance, validation, dependencies, risk, or release expectations. Then: briefly note material change in authoritative Issue/PR -> reconcile implementation/dependencies -> invalidate stale Worker assignments -> never overwrite concurrent contract revision without `authority-gates.md` optimistic reconciliation. Do not increment for wording-only cleanup.

## 8. Worker assignment identity

Before any Worker dispatch, bind/persist:

| Field | Requirement |
|---|---|
| `Assignment ID` | unique current generation; stable during that generation; fresh generation/nonce after replacement/reissue/invalidation (e.g. `184-r3-g2-a7f91de`); never reuse superseded/cancelled/replaced ID |
| Work item / revision | Issue/work-item identity + numeric `Contract Revision` |
| `Repository` | exact canonical repository identity used at dispatch and persisted as assignment identity; must not be inferred from Issue, dependency, project, or surrounding repository context; `worker-protocol.md` consumes this exact value as the Worker's repository mutation boundary |
| Git start | exact `Base SHA`; `Assigned Branch` as local branch or `refs/heads/<branch>` (never worktree path/remote-tracking ref); exact immutable `Start HEAD` (Base SHA when no divergence is intended) |
| `Integration Target` | distinct canonical repository branch: simple name such as `main`, or `refs/heads/<branch>` when name contains `/`; never `origin/main` or `refs/remotes/origin/main` |
| Execution envelope | Worker identity; `Assignment Status: ACTIVE` at dispatch, later reconciled to the repository's completed/superseded/cancelled equivalent; inherited `Project Authority` (`MANAGED` or `AUTONOMOUS_WITH_GATES`); `Coordination Baseline` (`LIGHTWEIGHT` or `STANDARD`); `Assurance Level` (`NORMAL` or `HIGH_ASSURANCE`); exact `Scoped Authorization` when one applies; required validation + risk/release constraints |
| Correction / resume | exact `Checkpoint HEAD` supplied by Master for the same assignment generation; omit it on initial dispatch unless a correction/resume checkpoint already exists |

Persist this minimum in authoritative existing work item/repo-native equivalent **before dispatch**, so replacement Master can reconstruct assignment before first push/PR/handoff.

- Fresh Assignment ID for new generation, including different Worker or reissue after supersede/cancel/invalidation; same ID for ordinary corrections on the same valid Worker/branch/PR.
- Worktree path is transient runtime location, never persisted assignment identity. On **initial dispatch before the first contracted edit**, verify the assigned branch/worktree current HEAD equals immutable `Start HEAD`. After normal authorized Worker commits in the same valid generation, `Start HEAD` remains the historical verified start and is no longer a required equality with current HEAD. For a same-generation correction/resume, Master supplies the reviewed/current `Checkpoint HEAD`; verify current assigned-branch HEAD against that checkpoint before editing.
- Assigned Worker branch must differ from canonical Integration Target; direct integration remains Master responsibility. Remote-tracking aliases are invalid Integration Target identity because they can disguise the same branch.
- Assignment ID is correlation/generation aid, not new truth: authoritative work item identifies active generation; Git refs own code state; persisted worker/repository/base/revision/branch/start-HEAD/target preserve dispatch assumptions for stale detection.
- `ProjectAuthority` is project-wide authority. `ScopedAuthorization`, when present, is an exact grant for its stated action/target/effect and never silently upgrades `ProjectAuthority`, `CoordinationBaseline`, or `AssuranceLevel`.

The schema above is the canonical assignment-identity input consumed by `worker-protocol.md` §4 for staleness classification. Normal authorized Worker commits may advance current HEAD beyond `Start HEAD`; that field remains the immutable verified generation start.

During Phase 2 compatibility, `scripts/contract_check.py` accepts legacy `Authority` as `Project Authority` and legacy `Expected Starting HEAD` as `Start HEAD`. Legacy `Operating Profile: LIGHTWEIGHT|STANDARD` maps losslessly to the same `CoordinationBaseline` with `AssuranceLevel=NORMAL`. Legacy `Operating Profile: HIGH_ASSURANCE` is accepted only when an authoritative `Coordination Baseline` is also persisted; otherwise the helper rejects the ambiguous state rather than guessing a baseline.

## 9. READY gate

Applies to delegated work and FULL-path Master work. FAST Master work needs no READY artifact, but the same decision-relevant facts must be clear enough to act safely.

| READY condition | If not yet true |
|---|---|
| outcome/scope is implementable and unambiguous enough for this change | discover/refine; split only when needed |
| acceptance is observable | define the smallest verifiable acceptance boundary |
| validation is defined | identify the strongest practical evidence before implementation/dispatch |
| dependencies are satisfied or intentionally/safely stacked | unblock, sequence, or make stacking explicit |
| required product/architecture/security decisions are resolved | Master decides bounded reversible technical choices; escalate only canonical material decisions |
| risk/release implications are understood enough for the next action | inspect/classify/gate proportionally before acting |

Discover safely discoverable missing information read-only instead of asking the user. READY is a decision gate, not a documentation ceremony: do not create extra artifacts merely to represent facts already authoritative and recoverable elsewhere.

Use `scripts/contract_check.py` when a local contract is available and convenient. `--worker` requires the full compact contract plus dispatch-ready `ACTIVE` assignment and Issue identity; it rejects malformed/placeholder assignment identity, invalid branch/target relationships, duplicate/ambiguous canonical fields, and ambiguous legacy `HIGH_ASSURANCE` without a persisted coordination baseline. Branch identity is literal. The helper is optional, does not judge prose or replace READY, and must not block equivalent manual/tool verification.
