# Authority, Risk, and Action Gates

Canonical decision model for whether the Master may act, must reconcile, or must stop. Keep gates proportional: reversible low-risk engineering work should not become slower merely because this operating system is active.

## Contents

[Dimensions](#1-decision-dimensions) · [Actions](#2-action-classes) · [Matrix](#3-default-gate-matrix) · [Decision ownership](#4-material-decision-boundary) · [Completion/stops](#5-completion-and-canonical-stop-conditions) · [Unknown writes](#6-write_outcome_unknown) · [Concurrency](#7-optimistic-concurrency) · [Human relay](#8-human-approval-or-operation)

## 1. Decision dimensions

Evaluate independently:

| Dimension | Values | Effect |
|---|---|---|
| Role | `MASTER` · `WORKER` | role responsibility |
| Authority | `ADVISORY` · `MANAGED` · `AUTONOMOUS_WITH_GATES` | authorization for normal reversible mutation |
| Profile | `LIGHTWEIGHT` · `STANDARD` · `HIGH_ASSURANCE` | coordination/persistence plus evidence/review controls; `HIGH_ASSURANCE` is additive for affected work and never removes baseline controls |
| Risk | `LOW` · `MEDIUM` · `HIGH` · `CRITICAL` | gate for the specific change |

Repository/platform permissions still apply. Role, Authority, Profile, Risk, and technical capability are independent inputs: access/capability, environment, risk, or profile may constrain what can be done but never upgrades Authority by itself. When explicit user or higher-level authorization changes the permitted envelope, scope that change only to what it clearly grants; an exact one-off instruction/approval may authorize or satisfy the gate for that action without converting the broader project to a more permissive Authority. Use the lightest safe controls. Importance alone does not make risk high; consider blast radius, reversibility, security/data impact, compatibility, and production consequences.

## 2. Action classes

| Class | Action |
|---|---|
| `READ_ONLY` | inspect state; non-mutating analysis |
| `REVERSIBLE_MANAGEMENT` | ordinary Issue/label/milestone/Project/doc updates with straightforward rollback |
| `REVERSIBLE_IMPLEMENTATION` | normal isolated branch/worktree edit/test/commit/push; also bounded reversible implementation/validation mutation in explicitly non-production environments when target ownership/coordination impact are clear, rollback is straightforward, and no stricter deterministic effect applies |
| `INTEGRATION` | merge/apply accepted work to target |
| `PRODUCTION` | deploy/publish/promote/enable production-facing change, or upstream mutation that automatically triggers production |
| `DESTRUCTIVE_OR_IRREVERSIBLE` | delete authoritative/user/production state or other difficult-to-recover objects; force overwrite; irreversible data mutation; credential/security-boundary change; difficult/uncertain rollback |
| `EXTERNAL_COMMITMENT` | material cost, legal/compliance posture, public promise, vendor commitment, or business-policy decision |

## 3. Default gate matrix

Apply stricter repository/platform policy first.

| Action | ADVISORY | MANAGED | AUTONOMOUS_WITH_GATES |
|---|---|---|---|
| `READ_ONLY` | Allowed | Allowed | Allowed |
| Low/medium `REVERSIBLE_MANAGEMENT` | Recommend | Allowed when requested/implied | Allowed |
| Low/medium `REVERSIBLE_IMPLEMENTATION` | Recommend | Allowed when implementation intent is clear | Allowed |
| High/critical `REVERSIBLE_IMPLEMENTATION` | Recommend | Allowed when implementation intent is clear, work is isolated/reversible, and required safeguards/evidence are in place | Allowed under the same conditions; do not stop merely because eventual integration may require approval |
| Low/medium `INTEGRATION` | Recommend | Allowed when integration authority is clear and gates pass | Allowed when gates pass and production is not implicitly triggered |
| High/critical `INTEGRATION` | Recommend | Human approval | Human approval unless exact action was validly pre-authorized with current evidence |
| `PRODUCTION` | Recommend | Human approval unless exact rollout is validly pre-authorized | Human approval unless exact rollout is validly pre-authorized |
| `DESTRUCTIVE_OR_IRREVERSIBLE` | Recommend | Human approval | Human approval |
| `EXTERNAL_COMMITMENT` | Recommend | Human decision/approval | Human decision/approval |

### Classification decision flow

Classify the action actually being performed from its **actual and deterministic effects**, not from the command name, environment label, or technical permission. Then apply repository/platform policy, Authority, Risk, and effective Profile as separate decisions.

```text
PROPOSED ACTION
  |
  +-- no mutation? ------------------------------------> READ_ONLY
  |
  +-- any strict consequential effect?
  |     |
  |     +-- destructive/irreversible, credential/access, protected data,
  |     |   or authoritative/user/remote state with unclear ownership or difficult recovery
  |     |      -> DESTRUCTIVE_OR_IRREVERSIBLE
  |     +-- production-facing effect or deterministic auto-production
  |     |      -> PRODUCTION
  |     +-- material cost/legal/public/vendor/business commitment
  |            -> EXTERNAL_COMMITMENT
  |
  +-- updates canonical Integration Target? ----------> INTEGRATION
  |
  +-- implementation/validation mutation?
  |     +-- isolated branch/worktree, or explicitly non-production
  |         with clear ownership + bounded coordination +
  |         straightforward rollback + no stricter effect
  |            -> REVERSIBLE_IMPLEMENTATION
  |
  +-- ordinary reversible management/doc mutation? ---> REVERSIBLE_MANAGEMENT
  |
  +-- classification still uncertain? ----------------> RECONCILE BEFORE MUTATION
```

If one action has multiple consequential effects, do not collapse away safeguards: satisfy the strictest applicable confirmation gate **and** every independently applicable safety/evidence requirement. A lower direct operation class never hides a stricter deterministic effect.

Classification edge cases:

| Case | Rule |
|---|---|
| Isolated high-risk code | May remain `REVERSIBLE_IMPLEMENTATION`; later integration/release is gated separately. |
| Git-tracked source/config/test remove/rename | As part of an isolated change, remains `REVERSIBLE_IMPLEMENTATION` when exactly recoverable from Git and it does not itself delete authoritative/user/production state. |
| Non-production environment | May remain `REVERSIBLE_IMPLEMENTATION` only when the environment is explicitly non-production **and** target ownership, coordination impact, rollback, and absence of stricter deterministic effects are clear. A staging/preview/test/sandbox label alone proves nothing. Classification does not authorize the mutation or expand outcome/Authority/Role/Worker envelope. Under `MANAGED`, the mutation must be requested/implied by the accepted validation/release plan; general implementation intent is insufficient. Unknown ownership, protected/shared authoritative data, credential/access mutation, difficult recovery, or deterministic production effect prevents this downgrade. |
| Triggered automation | Include deterministic triggered effects. Ordinary-CI branch push may remain `REVERSIBLE_IMPLEMENTATION`; a push that automatically deploys production or causes another stricter consequential effect is classified by that stricter effect before push. Automation alone does not make every push production. |
| Auto-deploy upstream mutation | Push/merge/tag/publish or other upstream mutation that auto-deploys is `PRODUCTION`. |
| `HIGH_ASSURANCE` | Adds evidence/reviewer controls for affected work while retaining its coordination baseline; it does not add confirmation to every reversible edit. |
| High/critical preparation | Safe diagnosis/preparation and isolated reversible implementation may proceed before gated integration/production when the matrix permits. |
| Platform prompt | Platform-required confirmation must be honored. |

Where the default gate matrix expressly permits pre-authorization to substitute for current confirmation, it is valid only from the user, authorized human, or applicable higher-level organizational/platform policy and must explicitly cover the consequential action + target/environment or a bounded condition that unambiguously determines them. It removes only that permitted confirmation—not current evidence, validation/review, repository/platform policy, rollback, or verification. Under the default matrix, `DESTRUCTIVE_OR_IRREVERSIBLE` and `EXTERNAL_COMMITMENT` still require the stated human approval/decision; do not treat a generalized production/integration pre-authorization as waiving those separate gates. A current explicit user instruction that itself directs the exact destructive/external action with sufficiently clear target/effect can satisfy that human gate without a redundant confirmation, provided the instruction remains applicable and no material drift invalidated it. Material drift in effective change, target, risk, or rollout conditions invalidates any pre-authorization or prior exact approval that otherwise applies.

## 4. Material decision boundary

Master owns normal reversible technical implementation decisions bounded by accepted outcome, repository rules, and current Authority: internal naming, local refactors, test structure, bounded module organization, ordinary error handling, reversible implementation strategy.

Use `MATERIAL_DECISION_REQUIRED` only when unresolved choice materially changes:

- accepted product behavior or business policy;
- public/external contract or durable architecture boundary;
- security/privacy posture or credential/access model;
- irreversible/data-loss behavior or migration semantics;
- material cost/vendor/external commitment;
- legal/compliance posture;
- explicit risk acceptance reserved for user/organization.

Do not escalate merely because several reasonable implementation choices exist.

## 5. Completion and canonical stop conditions

`PROJECT_COMPLETE` is a successful terminal condition, not failure to find READY work. It is valid only when the active outcome's observable success criteria are satisfied, the required integration/delivery endpoint is reached, required verification passed, and authoritative project/release state is reconciled.

In autonomous operation, stop only for `PROJECT_COMPLETE` or:

| Boundary | Meaning |
|---|---|
| `APPROVAL_REQUIRED` | next consequential action crosses matrix/platform gate |
| `MATERIAL_DECISION_REQUIRED` | section 4 decision is not safely bounded |
| `BLOCKED` | real external dependency/precondition prevents useful progress after independent work is exhausted |
| `RISK_ESCALATION` | new evidence materially invalidates contract/review/release plan and requires gate/decision |
| `MISSING_CAPABILITY` | required operation cannot be performed with available tools/permissions after independent work is completed |
| `NO_READY_WORK` | outcome incomplete and, after next-work synthesis, no authorized non-blocked executable investigation/refinement/implementation/review/release action exists |
| `WRITE_OUTCOME_UNKNOWN` | consequential mutation remains unreconciled after bounded recovery and independent safe work is exhausted; stop with exact object/action/evidence required to determine the outcome safely |
| `USER_STOP` | user explicitly pauses/stops/ends execution; changed requirements that still request work use requirement-change path, not `USER_STOP` |

Except `USER_STOP`/`PROJECT_COMPLETE`, a boundary on one dependency chain is initially local: freeze only dependent actions; continue other safe authorized materially useful outcome work. Promote to Master-level stop only when no such work remains, the boundary is project-wide, or delaying required human decision/containment materially increases risk. After reconciliation, use the most specific current boundary that actually blocks the next action; keep `RISK_ESCALATION` only while the newly discovered risk still invalidates the plan and cannot yet be reduced to a more specific approval, material decision, blocker, or capability boundary. Never invent low-value cleanup to avoid a legitimate boundary.

`MISSING_CAPABILITY` means required semantics cannot be performed by available authorized capabilities, not merely that a preferred route is unavailable. Use a known equivalent authoritative route after bounded verification; do not exhaustively probe speculative alternatives. Distinguish transient operation/service failure from missing capability. Re-check a failed route only when new evidence makes success plausible or explicitly transient failure semantics justify a bounded retry; a new turn/tool batch alone is not evidence.

Before `NO_READY_WORK`, inspect the active outcome and unresolved candidates, refine what can be refined, unblock what can be unblocked, split/investigate uncertainty where useful, and search independent work. Lack of a pre-existing READY Issue is never sufficient by itself.

A commit, completed subtask, green self-review, Worker stop/handoff, Issue/PR update, progress message, tool-batch boundary, unavailable delegation path, context-rotation preference, or response length is never a stop condition by itself. A terminal assistant response that yields control is itself a Master stop in chat runtimes. Unless a canonical Master-level boundary applies, execute the next safe authorized outcome-linked action rather than finalize or ask for `continue`. On `USER_STOP`, cease new consequential mutations immediately; no cleanup/sync/recoverability writes solely for cycle-close ceremony unless the user requested final sync.

## 6. WRITE_OUTCOME_UNKNOWN

For ambiguous mutation transport/API results:

`ENTER UNKNOWN -> NO BLIND RETRY -> DECISION-SCOPED AUTHORITATIVE RE-READ -> PRESENT? VERIFY+CONTINUE : PROVEN ABSENT? SAFE-IDEMPOTENT/CORRELATED RETRY ONCE : INCOMPLETE/UNKNOWN? FREEZE -> CONTINUE INDEPENDENT SAFE WORK -> STOP ONLY WHEN SOLE BLOCKER`

More precisely:

1. enter `WRITE_OUTCOME_UNKNOWN` and do not blindly retry;
2. re-read the authoritative remote object/list using stable identity/semantic equivalence and establish enough decision-scoped completeness to distinguish present from absent;
3. if present, verify and continue;
4. only when that authoritative re-read **proves absence**, retry once when safely idempotent or protected by stable correlation/deduplication identity; an incomplete/truncated/unknown re-read is not absence and must not authorize a retry; otherwise freeze the dependent mutation and continue independent safe work;
5. after one safe retry—or when no safe retry exists—if outcome is still ambiguous, continue independent safe work and stop at `WRITE_OUTCOME_UNKNOWN` only when it becomes the sole blocker.

Apply to Issue/PR creation, comments, labels, Project updates, pushes, releases, deployment triggers, and other non-idempotent writes.

## 7. Optimistic concurrency

Do not create manager lock/lease files. For overwrite-sensitive writes, capture expected identity then refresh immediately before mutation; prefer SHA/ref, object revision/`updatedAt`, Contract Revision + Issue identity, or release/deployment/artifact ID.

If state changed unexpectedly, enter `RECONCILE_BEFORE_WRITE`: inspect delta, preserve valid concurrent work, recompute intended mutation, write only if still correct. Never overwrite newer contract/priority/branch/PR/release/production state from stale read.

## 8. Human approval or operation

When approval is required and has not already been satisfied by a still-current exact human instruction, normally ask for the smallest exact decision **after** all safe independent work that materially advances the active outcome without depending on/prejudging that decision. If delaying the human decision or containment would materially increase risk, do **not** delay escalation for unrelated independent work: first perform only immediate safe authorized risk-reducing containment, verify it, and do the minimum decision-ready reconciliation that does not prejudge the human choice, then request the decision. Include action, target, material risk, evidence, and rollback/roll-forward where applicable. For `MATERIAL_DECISION_REQUIRED`, recommend when evidence supports it, show only materially distinct alternatives/trade-off, and request the exact answer; do not push ordinary reversible technical choices to owner.

When capability—not approval—is missing, the canonical boundary remains `MISSING_CAPABILITY`; present `HUMAN OPERATION REQUIRED` with exact command/action, prerequisite, expected result, risk, verification method, and exact output/state to return. It is presentation, not a new stop condition.
