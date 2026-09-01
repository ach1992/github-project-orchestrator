# Authority, Risk, and Action Gates

Canonical decision model for whether the Master may act, must reconcile, or must stop. Keep gates proportional: reversible low-risk engineering work should not become slower merely because this operating system is active.

## Contents

[Dimensions](#1-decision-dimensions) · [Effects](#2-applicable-effects) · [Matrix](#3-default-gate-matrix) · [Decision ownership](#4-material-decision-boundary) · [Completion/stops](#5-completion-and-canonical-stop-conditions) · [Unknown writes](#6-writestateunknown) · [Concurrency](#7-optimistic-concurrency) · [Human relay](#8-human-approval-or-operation)

## 1. Decision dimensions

Use the current `Role`, `ProjectAuthority`, `ScopedAuthorization`, `CoordinationBaseline`, `AssuranceLevel`, and `RiskLevel` established in `SKILL.md` as independent inputs to gate evaluation. Technical capability and environment remain separate execution constraints. This domain consumes the shared dimension ontology rather than re-declaring its values; it owns authorization/action-gate interpretation and applies current action effects, obligations, repository/platform policy, and gate evidence.

`ProjectAuthority` is the project-wide authorization envelope for normal reversible mutation. It changes only from applicable explicit user or higher-level authorization; access/capability, environment, risk, coordination, or assurance may constrain execution but never grant or widen it. Repository/platform permissions still apply. When explicit user or higher-level authorization changes the permitted project envelope, scope the change only to what it clearly grants.

An exact one-off instruction/approval is `ScopedAuthorization`: where the canonical matrix permits scoped authorization, it may authorize that exact action or satisfy only the applicable gate for it, without converting the broader project to a more permissive `ProjectAuthority`. `CoordinationBaseline` contributes coordination/persistence controls; `STANDARD` does not imply FULL execution. `AssuranceLevel=HIGH_ASSURANCE` adds evidence/review controls without removing baseline controls and does not by itself create human approval or a different `ProjectAuthority`. `RiskLevel` determines proportional gate/evidence depth for the specific change when decision-relevant.

Use the lightest safe controls. Importance alone does not make risk high; consider blast radius, reversibility, security/data impact, compatibility, and production consequences.

## 2. Applicable effects

Classify the action actually being performed by its simultaneous actual/deterministic consequences. `ApplicableEffects` is a set, not a scalar class:

| Effect | Action consequence |
|---|---|
| `READ_ONLY` | inspect state; non-mutating analysis; mutually exclusive with mutation effects |
| `REVERSIBLE_MANAGEMENT` | ordinary Issue/label/milestone/Project/doc updates with straightforward rollback |
| `REVERSIBLE_IMPLEMENTATION` | normal isolated branch/worktree edit/test/commit/push; also bounded reversible implementation/validation mutation in explicitly non-production environments when target ownership/coordination impact are clear, rollback is straightforward, and no separate stricter deterministic effect is ignored |
| `INTEGRATION` | merge/apply accepted work to target |
| `PRODUCTION` | deploy/publish/promote/enable production-facing change, or upstream mutation that automatically triggers production |
| `DESTRUCTIVE_OR_IRREVERSIBLE` | delete authoritative/user/production state or other difficult-to-recover objects; force overwrite; irreversible data mutation; credential/security-boundary change; difficult/uncertain rollback |
| `EXTERNAL_COMMITMENT` | material cost, legal/compliance posture, public promise, vendor commitment, or business-policy decision |

For mutation actions:

```text
ApplicableEffects(action) = {every effect that actually/deterministically applies}
RequiredObligations(action) = union(Obligations(effect) for effect in ApplicableEffects(action))
```

No scalar precedence may erase an independent obligation. For example, a merge that also auto-deploys and performs an irreversible migration has `ApplicableEffects={INTEGRATION, PRODUCTION, DESTRUCTIVE_OR_IRREVERSIBLE}`. Production pre-authorization may satisfy the production confirmation only; it cannot waive the destructive obligation.

## 3. Default gate matrix

Apply stricter repository/platform policy first. For multi-effect actions, apply every applicable row and take the union of required gates/evidence; satisfying one row never removes another row's independent obligation.

| Applicable effect | ADVISORY | MANAGED | AUTONOMOUS_WITH_GATES |
|---|---|---|---|
| `READ_ONLY` | Allowed | Allowed | Allowed |
| Low/medium `REVERSIBLE_MANAGEMENT` | Recommend | Allowed when requested/implied | Allowed |
| Low/medium `REVERSIBLE_IMPLEMENTATION` | Recommend | Allowed when implementation intent is clear | Allowed |
| High/critical `REVERSIBLE_IMPLEMENTATION` | Recommend | Allowed when implementation intent is clear, work is isolated/reversible, and required safeguards/evidence are in place | Allowed under the same conditions; do not stop merely because eventual integration may require approval |
| Low/medium `INTEGRATION` | Recommend | Allowed when integration authority is clear and gates pass | Allowed when gates pass and `PRODUCTION` is not also applicable without its gate being satisfied |
| High/critical `INTEGRATION` | Recommend | Human approval | Human approval unless exact action was validly pre-authorized with current evidence |
| `PRODUCTION` | Recommend | Human approval unless exact rollout is validly pre-authorized | Human approval unless exact rollout is validly pre-authorized |
| `DESTRUCTIVE_OR_IRREVERSIBLE` | Recommend | Human approval | Human approval |
| `EXTERNAL_COMMITMENT` | Recommend | Human decision/approval | Human decision/approval |

### `CAN_EXECUTE(action)`

Use one canonical execution predicate instead of independently re-deriving the same authority/gate decision in each runtime domain:

```text
CAN_EXECUTE(action) =
    AcceptedScopeAllows(action)
    AND RoleAllows(action)
    AND ProjectAuthorityAllows(action)
    AND RepositoryAndPlatformPolicyAllow(action)
    AND ApplicableEffectsAreKnown(action)
    AND RequiredObligationsAreSatisfied(action)
    AND AnyScopedAuthorizationUsedIsCurrentAndExact(action)
    AND RequiredCapabilityIsAvailable(action)
    AND RequiredMutableIdentityEvidenceIsFresh(action)
```

Interpret each term only when it is applicable to the proposed action, using this file's matrix plus authoritative repository/platform state. `CAN_EXECUTE=false` is not itself a terminal Master boundary: reconcile uncertainty, use an authorized equivalent path, or classify the actual canonical boundary while independent useful work continues. `ADVISORY` does not become mutation-capable through technical access; `ScopedAuthorization` satisfies only the exact gate it covers; uncertain `ApplicableEffects` or stale required mutable identity must be reconciled before mutation.

### Classification decision flow

Classify from actual and deterministic effects, not from command name, environment label, or technical permission. Then apply repository/platform policy, ProjectAuthority, any applicable ScopedAuthorization, RiskLevel, CoordinationBaseline, and AssuranceLevel as independent decisions.

```text
PROPOSED ACTION
  |
  +-- no mutation? ------------------------------------> ApplicableEffects={READ_ONLY}
  |
  `-- mutation:
        start ApplicableEffects={}
        |
        +-- ordinary reversible management/doc mutation? -> add REVERSIBLE_MANAGEMENT
        +-- implementation/validation mutation? ----------> add REVERSIBLE_IMPLEMENTATION when its own effect is reversible
        +-- updates canonical Integration Target? --------> add INTEGRATION
        +-- production-facing or deterministic auto-prod? -> add PRODUCTION
        +-- destructive/irreversible/access/protected-data
        |   effect or difficult recovery? ----------------> add DESTRUCTIVE_OR_IRREVERSIBLE
        +-- material cost/legal/public/vendor/business
        |   commitment? ----------------------------------> add EXTERNAL_COMMITMENT
        |
        `-- any effect materially uncertain? --------------> RECONCILE BEFORE MUTATION

REQUIRED CONTROLS = union of obligations for every applicable effect
```

A lower direct operation effect never hides a stricter deterministic effect.

Classification edge cases:

| Case | Rule |
|---|---|
| Isolated high-risk code | May have only `REVERSIBLE_IMPLEMENTATION`; later integration/release effects are classified and gated when those actions occur. |
| Git-tracked source/config/test remove/rename | As part of an isolated change, remains `REVERSIBLE_IMPLEMENTATION` when exactly recoverable from Git and it does not itself delete authoritative/user/production state. |
| Non-production environment | May remain `REVERSIBLE_IMPLEMENTATION` only when the environment is explicitly non-production **and** target ownership, coordination impact, rollback, and absence of separate stricter deterministic effects are clear. A staging/preview/test/sandbox label alone proves nothing. Classification does not authorize the mutation or expand outcome/ProjectAuthority/Role/Worker envelope. Under `MANAGED`, the mutation must be requested/implied by the accepted validation/release plan; general implementation intent is insufficient. Unknown ownership, protected/shared authoritative data, credential/access mutation, difficult recovery, or deterministic production effect adds/prevents ignoring the relevant stricter effect. |
| Triggered automation | Include deterministic triggered effects. Ordinary-CI branch push may have only `REVERSIBLE_IMPLEMENTATION`; a push that automatically deploys production also has `PRODUCTION` before push. Automation alone does not make every push production. |
| Auto-deploy upstream mutation | Push/merge/tag/publish or other upstream mutation that auto-deploys includes `PRODUCTION`. |
| `AssuranceLevel=HIGH_ASSURANCE` | Adds evidence/reviewer controls for affected work while retaining its CoordinationBaseline; it does not add confirmation to every reversible edit. |
| High/critical preparation | Safe diagnosis/preparation and isolated reversible implementation may proceed before separately gated integration/production when the matrix permits. |
| Platform prompt | Platform-required confirmation must be honored. |

Where the default gate matrix expressly permits pre-authorization to substitute for current confirmation, a `ScopedAuthorization` is valid only from the user, authorized human, or applicable higher-level organizational/platform policy and must explicitly cover the consequential action + target/environment or a bounded condition that unambiguously determines them. It removes only that permitted confirmation—not current evidence, validation/review, repository/platform policy, rollback, or verification—and never mutates ProjectAuthority.

Under the default matrix, `DESTRUCTIVE_OR_IRREVERSIBLE` and `EXTERNAL_COMMITMENT` still require the stated human approval/decision. Do not treat a generalized production/integration pre-authorization as waiving those separate gates. A current explicit user instruction that itself directs the exact destructive/external action with sufficiently clear target/effect can be the applicable ScopedAuthorization satisfying that human gate without redundant confirmation, provided the instruction remains applicable and no material drift invalidated it. Material drift in effective change, target, risk, or rollout conditions invalidates any affected pre-authorization/prior exact approval.

## 4. Material decision boundary

Master owns normal reversible technical implementation decisions bounded by accepted outcome, repository rules, and current ProjectAuthority: internal naming, local refactors, test structure, bounded module organization, ordinary error handling, reversible implementation strategy.

Use `MasterBoundary.MATERIAL_DECISION_REQUIRED` only when unresolved choice materially changes:

- accepted product behavior or business policy;
- public/external contract or durable architecture boundary;
- security/privacy posture or credential/access model;
- irreversible/data-loss behavior or migration semantics;
- material cost/vendor/external commitment;
- legal/compliance posture;
- explicit risk acceptance reserved for user/organization.

Do not escalate merely because several reasonable implementation choices exist.

## 5. Completion and canonical stop conditions

`MasterBoundary.PROJECT_COMPLETE` is a successful terminal condition, not failure to find READY work. It is valid only when the active outcome's observable success criteria are satisfied, the required integration/delivery endpoint is reached, required verification passed, and authoritative project/release state is reconciled.

In autonomous operation, the canonical Master boundaries are:

| MasterBoundary | Meaning |
|---|---|
| `PROJECT_COMPLETE` | active outcome, required integration/delivery, verification, and reconciliation are complete |
| `APPROVAL_REQUIRED` | next consequential action crosses matrix/platform gate |
| `MATERIAL_DECISION_REQUIRED` | section 4 decision is not safely bounded |
| `BLOCKED` | real external dependency/precondition prevents useful progress after independent work is exhausted |
| `RISK_ESCALATION` | new evidence materially invalidates contract/review/release plan and requires gate/decision |
| `MISSING_CAPABILITY` | required operation cannot be performed with available tools/permissions after independent work is completed |
| `NO_READY_WORK` | outcome incomplete and, after next-work synthesis, no authorized non-blocked executable investigation/refinement/implementation/review/release action exists |
| `WRITE_OUTCOME_UNKNOWN` | an action remains `WriteState.UNKNOWN` after bounded recovery and independent safe work is exhausted; stop with exact object/action/evidence required to determine the outcome safely |
| `USER_STOP` | user explicitly pauses/stops/ends execution; changed requirements that still request work use requirement-change path, not USER_STOP |

This section defines boundary meaning; `MASTER_STOP(...)` in `master-cycle.md` is the single owner of when a detected boundary becomes a terminal Master response. A local boundary does not terminate the project merely because its token exists.

`MasterBoundary.MISSING_CAPABILITY` means required semantics cannot be performed by available authorized capabilities, not merely that a preferred route is unavailable. Use a known equivalent authoritative route after bounded verification; do not exhaustively probe speculative alternatives. Distinguish transient operation/service failure from missing capability. Re-check a failed route only when new evidence makes success plausible or explicitly transient failure semantics justify a bounded retry; a new turn/tool batch alone is not evidence.

Before `MasterBoundary.NO_READY_WORK`, inspect the active outcome and unresolved candidates, refine what can be refined, unblock what can be unblocked, split/investigate uncertainty where useful, and search independent work. Lack of a pre-existing READY Issue is never sufficient by itself.

On `MasterBoundary.USER_STOP`, cease new consequential mutations immediately; no cleanup/sync/recoverability writes solely for cycle-close ceremony unless the user requested final sync.

## 6. `WriteState.UNKNOWN`

For ambiguous mutation transport/API results, use one guarded recovery algorithm:

1. Mark only the individual mutation `WriteState.UNKNOWN`; do not blindly retry and do not automatically stop the Master.
2. Re-read the authoritative remote object/list using stable identity or semantic equivalence, with enough decision-scoped completeness to distinguish **present**, **proven absent**, and **incomplete/unknown**.
3. If the equivalent write is **present**, verify it, mark the action `WriteState.KNOWN`, and continue.
4. If the re-read **proves absence**, retry at most once and only when the retry is safely idempotent or protected by stable correlation/deduplication identity. If retry is not safe, freeze the dependent mutation and continue independent safe work.
5. If the re-read is **incomplete/truncated/unknown**, never treat that as absence and never use it to authorize a retry; freeze the dependent mutation and continue independent safe work.
6. After the one safe retry—or when no safe retry exists—if outcome remains ambiguous, keep that mutation at `WriteState.UNKNOWN`, continue independent safe work, and surface `MasterBoundary.WRITE_OUTCOME_UNKNOWN` only when it becomes the sole/project-wide controlling blocker.

Apply to Issue/PR creation, comments, labels, Project updates, pushes, releases, deployment triggers, and other non-idempotent writes.

## 7. Optimistic concurrency

Do not create manager lock/lease files. For overwrite-sensitive writes, capture expected identity then refresh immediately before mutation; prefer SHA/ref, object revision/`updatedAt`, Contract Revision + Issue identity, or release/deployment/artifact ID.

If state changed unexpectedly, enter the local reconcile-before-write condition: inspect delta, preserve valid concurrent work, recompute intended mutation, write only if still correct. Never overwrite newer contract/priority/branch/PR/release/production state from stale read. A local reconciliation condition is not automatically a MasterBoundary.

## 8. Human approval or operation

When approval is required and has not already been satisfied by a still-current exact ScopedAuthorization/human instruction, normally ask for the smallest exact decision **after** all safe independent work that materially advances the active outcome without depending on/prejudging that decision. If delaying the human decision or containment would materially increase risk, do **not** delay escalation for unrelated independent work: first perform only immediate safe authorized risk-reducing containment, verify it, and do the minimum decision-ready reconciliation that does not prejudge the human choice, then request the decision. Include action, target, material risk, evidence, and rollback/roll-forward where applicable. For `MasterBoundary.MATERIAL_DECISION_REQUIRED`, recommend when evidence supports it, show only materially distinct alternatives/trade-off, and request the exact answer; do not push ordinary reversible technical choices to owner.

When capability—not approval—is missing, the canonical boundary remains `MasterBoundary.MISSING_CAPABILITY`; present `HUMAN OPERATION REQUIRED` with exact command/action, prerequisite, expected result, risk, verification method, and exact output/state to return. It is presentation, not a new stop condition.
