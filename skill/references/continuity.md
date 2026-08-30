# Continuity, Recovery, and Master Rotation

The project must survive loss of the current chat or Master. Continuity comes from authoritative current state, not a parallel manager-memory archive. Context management must never become an artificial project stop.

## Contents

[Retention](#1-retention-test) · [Recovery](#2-recovery-sequence) · [Reconciliation](#3-reconciliation-rules) · [Recoverability](#4-recoverability-test) · [Rotation](#5-master-rotation) · [Safe boundary](#6-safe-rotation-boundary) · [New Master prompt](#7-new-master-prompt)

## 1. Retention test

Persist information only when all are true:

1. a future contributor/Master needs it to decide, execute safely, understand a lasting constraint, or continue unresolved work;
2. it is not already recoverable from a stronger source such as Git, GitHub, CI, or deployment history;
3. it is likely to matter beyond the current orchestration cycle, **or** it is active delegated-assignment identity needed to survive unexpected Master loss before the first push/PR/handoff.

Persist stable goals/constraints, current architecture/engineering rules, unresolved dependencies/risks, lasting decisions, reusable operational hazards/procedures, and the minimum active Worker assignment identity required for cross-Master reconciliation. Reconcile/remove transient assignment status when the assignment is no longer active rather than retaining a historical manager archive. For bounded transient Master-only work, persist nothing while intent remains safely reconstructable; if ambiguous implementation state would otherwise cross a handoff/rotation/recovery boundary without an interpretable owner, persist only the minimum unresolved intent in the natural PR/Issue/commit/workflow context. Do not persist routine logs, Worker transcripts, merged PR summaries, resolved blockers, periodic snapshots, or chat summaries.

Never create `MASTER_STATE`, `manager-memory/`, `checkpoints/`, `handoffs/`, or similar archives solely for orchestration continuity.

## 2. Recovery sequence

A new/replacement Master enters `RECOVER` before consequential project mutation:

1. identify repository, target/default branches, checkout/worktrees, repository rules, and current capabilities;
2. read an existing lightweight Project Map/index if present, then only durable docs relevant to current work; consult the canonical root project specification only when project-level intent cannot be established safely from current downstream authoritative state or when material contradiction/change makes it decision-relevant;
3. inspect active Issues/milestones/Projects/risks/assignments;
4. inspect open PRs/reviews/checks/branches/dependencies;
5. inspect recent Git/release/deployment state only as needed;
6. reconcile contradictions/stale assignments;
7. determine active outcome/completion condition, review queue, blockers, `DeliveryRequirement`/`DeliveryTarget`/`DeliveryState`, and next executable action; recover `ProjectAuthority` and `CoordinationBaseline` independently, plus any affected-chain `AssuranceLevel` and exact current `ScopedAuthorization`;
8. continue the valid plan instead of rebuilding it because chat history is absent.

Keep cold recovery progressive and bounded:

- **Orientation spine:** establish repository/repositories, current project outcome/completion, Project Map or equivalent truth-location index, `ProjectAuthority`, `CoordinationBaseline`, any currently affected `AssuranceLevel`, and the active critical path/workstream.
- **Active-path context:** enter only the repository/workstream sources needed for the next decision: current Issue/contract, PR/branch/CI, direct dependencies/interfaces, blockers/risks, and integration/delivery state.
- **Triggered depth:** load broader architecture, other workstreams, root specification, historical decisions, or release history only when a contradiction, dependency, interface, risk, or project-level decision makes that context materially relevant.

Stop recovery reading once repository/target identity, active outcome, controlling dependencies/blockers, current `ProjectAuthority`/`CoordinationBaseline`/affected `AssuranceLevel`, current candidate/review/delivery state, and the next executable action are decision-valid. A large repository or long-lived project is a reason to narrow recovery by workstream, not to read more by default.

For multi-repository outcomes, recover the small global coordination spine first: outcome/completion, repository/workstream ownership, cross-repository dependencies/interfaces, integration/release order, and delivery target. Then enter only the local repository contexts on the active critical path. Local Issues/PRs/CI/repository rules remain authoritative; do not reconstruct them in a central recovery snapshot.

Never reconstruct `CoordinationBaseline` from `AssuranceLevel`, risk, project size, or technical access. Legacy `Operating Profile: LIGHTWEIGHT|STANDARD` can be interpreted losslessly as the same CoordinationBaseline with `AssuranceLevel=NORMAL`. Legacy `Operating Profile: HIGH_ASSURANCE` is not enough to identify its missing coordination baseline: recover that baseline from authoritative persisted project/assignment state or preserve the ambiguity until it is resolved; do not guess.

After this baseline is established, do not re-enter the full recovery sequence for ordinary progress. A planned branch/worktree create/switch should verify the intended branch, base/HEAD, target relationship, and dirty-state ownership as needed, then resume execution. A failed GitHub/tool route should update transient capability knowledge and trigger an equivalent authoritative route when available; it should not by itself restart repository-wide recovery. Re-enter broader recovery only when concrete evidence materially invalidates the established baseline. When a material dependency, architecture/interface assumption, ownership boundary, risk, or release constraint changes, reconcile the affected workstream/critical-path slice first and widen recovery only when the impact actually crosses that boundary.

Old handoff hints are accelerators only. `scripts/repo_preflight.py --recovery` may accelerate local Git inspection but is transient and incomplete. Treat any explicit completeness flag as authoritative for the helper output: when `status_complete`/`dirty_complete` is false, `dirty: false` means no dirty state was safely observed, not proof that the worktree is clean; when history/tag completeness is false, do not infer absence from the missing local evidence. Its high-cardinality status/branch lists are intentionally bounded; when `*_truncated` is true, use the reported totals plus targeted Git inspection for the paths/refs relevant to recovery rather than treating the returned subset as complete. The helper intentionally avoids implicit lazy fetches and reports replacement/graft history semantics; perform explicit authorized fetches or targeted trusted inspection only when the missing evidence can affect the next decision.

## 3. Reconciliation rules

When state is stale or contradictory:

- prefer current direct evidence using the source hierarchy in `SKILL.md`;
- correct the authoritative current source rather than adding a compensating note elsewhere;
- repair/remove stale Project Map or relationship pointers after the authoritative target is reconciled; never preserve a misleading link merely to explain history;
- close/supersede duplicates only after confirming intent/current work, and keep the surviving authoritative owner rather than creating another summary artifact;
- preserve concurrent valid work and use optimistic concurrency for overwrite-sensitive updates;
- do not infer `DeliveryState.DELIVERED` from `TaskState.INTEGRATED`, target/environment naming, or stale status fields;
- do not infer a `MasterBoundary` from matching `TaskState`/`WorkerStatus`/`WriteState`/`DeliveryState` token text;
- treat Worker summaries/chat as locators, not proof.

## 4. Recoverability test

A replacement Master with no chat history should be able to find, when relevant:

- project purpose, active outcome/success model/non-goals/durable constraints, with the canonical root project specification discoverable as the repository-level source for initial/project-level intent when needed;
- current milestone/backlog, dependencies, blockers, ownership, material risks;
- current architecture and development/validation/release rules;
- active Task Contracts and PR/review state, including persisted Worker assignment identity when delegation is active: current-generation `Assignment ID`, revision, `Base SHA`, Assigned Branch, immutable `Start HEAD`, Integration Target, Worker, `ProjectAuthority`, `CoordinationBaseline`, `AssuranceLevel`, exact current `ScopedAuthorization` when any, risk/release constraints, current Assignment Status, and same-generation `Checkpoint HEAD` when a correction/resume is active;
- unresolved lasting decisions;
- release/deployment state including independent `DeliveryRequirement`, `DeliveryTarget`, and `DeliveryState`, plus next valid action;
- authoritative locations and material relationships without chat history.

For large or multi-repository projects, the test is satisfied when the replacement Master can find the global outcome/dependency/release spine and then reach the active local workstream sources progressively; it does **not** require an exhaustive central snapshot of every repository or work item.

If not, persist only the missing future-useful fact in its proper source. Do not duplicate facts already reconstructable from Git/GitHub merely to make recovery faster, and do not promote a transient task to a standalone Issue when an existing PR/commit/work item already makes its intent recoverable.

## 5. Master rotation

Rotation is a **context optimization**, not a project stop condition.

Assess:

- `CONTINUE`: current context remains reliable; keep executing authorized work.
- `ROTATE_SOON`: finish the current bounded execution chain to a safe recoverable boundary, then rotate before a substantially different/high-risk chain when rotation is actually possible/useful.
- `ROTATE_NOW`: only when context degradation creates a concrete correctness risk, the platform/runtime requires rotation, or the user explicitly requests it. Place active work at a safe recoverable boundary first when possible.

Signals include repeated confusion/stale assumptions, excessive dependence on old chat instead of sources, a clean major milestone boundary, or explicit user/platform need. Several completed cycles alone are not sufficient. Do not stop merely to recommend a fresh chat when the current runtime can continue reliably.

## 6. Safe rotation boundary

Before rotation:

- finish a small review/integration if safe, or park work in committed/shared recoverable state when permitted; if incomplete implementation contains non-obvious state that would otherwise be lost, use the smallest safe existing Git/PR/Issue context that makes it recoverable, without creating checkpoint artifacts or ceremonial WIP commits;
- ensure Issues/PRs/branches/assignments/blockers/review findings/milestone state are current;
- persist unresolved material risks/decisions in proper sources;
- ensure no critical work exists only as uncommitted/unpushed local changes or chat instructions;
- run the recoverability test.

Workers may continue across Master rotation only when their Task Contract and persisted assignment identity are recoverable: Assignment ID, revision, Base SHA, Assigned Branch, immutable Start HEAD, Integration Target, Worker identity, ProjectAuthority, CoordinationBaseline, AssuranceLevel, applicable ScopedAuthorization, current Assignment Status, risk/release constraints, and current correction/resume Checkpoint HEAD when any, plus PR when one exists. Do not rely on the old Master chat to reconstruct an active assignment.

## 7. New Master prompt

Provide only a short bootstrap prompt when rotation is actually needed. When presented for relay, apply the canonical `SKILL.md` machine-relay transport contract rather than restating its transport rules here.

```text
# NEW MASTER CHAT

Use `github-project-orchestrator` as MASTER for:
<repository URL or unambiguous identifier>

Mode: RECOVER, then continue.
Project Authority: <ADVISORY | MANAGED | AUTONOMOUS_WITH_GATES>
Coordination Baseline: <LIGHTWEIGHT | STANDARD>
Assurance Level: <NORMAL | HIGH_ASSURANCE when currently applicable>
Scoped Authorization: <exact current grant if any; otherwise none>
Current objective/milestone: <short hint if useful>
Current focus: <optional Issue/PR pointer>

Preserve the supplied Role and ProjectAuthority unless explicit current user direction or applicable higher-level organizational/platform authorization changes them. Preserve exact ScopedAuthorization only within its stated action/target/effect; never widen it into project-wide ProjectAuthority. Repository/platform policy, technical access/capability, environment, RiskLevel, CoordinationBaseline, and AssuranceLevel may constrain the next action but never upgrade ProjectAuthority.

Recover CoordinationBaseline separately from AssuranceLevel. If AssuranceLevel is HIGH_ASSURANCE, retain/recover the underlying baseline from authoritative project/assignment state; never treat HIGH_ASSURANCE as a replacement for LIGHTWEIGHT/STANDARD or guess a missing legacy baseline. Verify available capabilities, recover current truth from repository/GitHub/Git/CI/releases/deployments/durable docs, reconcile, then continue the next valid project action. Do not re-plan merely because this is a new chat.
```

Do not paste the old conversation, long historical summaries, root project specification, or stale SHAs unless a specific non-recoverable fact is still required. A replacement Master should not re-read the root specification merely because rotation occurred when current authoritative downstream state already makes project intent and the next action clear. If a replacement Master starts without a rotation prompt and ProjectAuthority cannot be safely established from the current request or applicable higher-level authorization policy, use the least-permissive ProjectAuthority justified by that evidence before consequential mutation; infer the lightest safe CoordinationBaseline separately, then add only any risk/policy-required AssuranceLevel escalation. Never infer broader ProjectAuthority from technical permissions, repository access, project size, RiskLevel, CoordinationBaseline, or AssuranceLevel.
