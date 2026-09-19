# Continuity, Recovery, and Master Rotation

The project must survive loss of the current chat or Master. Continuity comes from authoritative current state, not a parallel manager-memory archive. Context management must never become an artificial project stop.

## Contents

[Retention](#1-retention-test) · [Recovery](#2-recovery-sequence) · [Reconciliation](#3-reconciliation-rules) · [Recoverability](#4-recoverability-test) · [Rotation](#5-master-rotation) · [Safe boundary](#6-safe-rotation-boundary) · [New Master prompt](#7-new-master-prompt)

## 1. Retention test

Persist information only when all are true:

1. a future contributor/Master needs it to decide, execute safely, understand a lasting constraint, or continue unresolved work;
2. it is not already recoverable from a stronger source such as Git, GitHub, CI, or deployment history;
3. it is likely to matter beyond the current orchestration cycle, **or** it is active delegated-assignment identity needed to survive unexpected Master loss before the first push/PR/handoff.

When the retention test passes:

- persist stable goals/constraints, current architecture/engineering rules, unresolved dependencies/risks, lasting decisions, reusable operational hazards/procedures, and the minimum active Worker assignment identity needed for cross-Master reconciliation;
- remove/reconcile transient assignment status once inactive rather than keeping a historical manager archive;
- for bounded transient Master-only work, persist nothing while intent remains safely reconstructable; if ambiguous implementation state would otherwise cross handoff/rotation/recovery without an interpretable owner, persist only the minimum unresolved intent in the natural PR/Issue/commit/workflow context;
- do **not** persist routine logs, Worker transcripts, merged PR summaries, resolved blockers, periodic snapshots, or chat summaries.

Never create `MASTER_STATE`, `manager-memory/`, `checkpoints/`, `handoffs/`, or similar archives solely for orchestration continuity.

## 2. Recovery sequence

A new/replacement Master enters `RECOVER` before consequential project mutation. Recover progressively and stop reading as soon as current authoritative state is decision-valid for the next action. The three rows are context-depth layers, not rigid lifecycle states; `Triggered depth` is a conditional side path from Orientation or Active path, not a mandatory third phase.

| Recovery layer | Required work |
|---|---|
| **Orientation spine — always first** | Identify repository/repositories, target/default branches, checkout/worktrees, repository rules, and current capabilities. Read an existing lightweight Project Map/truth-location index if present, then only durable docs relevant to current work. Before concluding control/workstream state, follow only the minimum live pointers needed to validate it. Establish active outcome/completion, recover `ProjectAuthority` and `CoordinationBaseline` independently, recover any affected-chain `AssuranceLevel` and exact current `ScopedAuthorization`, derive `RepositoryMutationScope` only from current explicit owner/higher-level authorization or exact assignment, and identify the active critical path/workstream from applicable authoritative evidence. Ambiguous repositories remain read-only until scope is reconciled. Chat loss alone never triggers root-spec loading. |
| **Active-path context — normal next layer** | Inspect only decision-relevant current Issues/milestones/Projects/risks/assignments, PRs/reviews/checks/branches/dependencies, and recent Git/release/deployment state when needed. Enter only the current Issue/contract, PR/branch/CI, direct dependencies/interfaces, blockers/risks, integration/delivery state, review queue, controlling blockers, `DeliveryRequirement`/`DeliveryTarget`/`DeliveryState`, candidate/review state, and next executable action needed for the current decision. Reconcile contradictions and stale assignments. |
| **Triggered depth — conditional side path** | Load broader architecture, other workstreams, the canonical root project specification, historical decisions, or release history only when a contradiction, dependency, interface, risk, or project-level decision makes that context materially relevant. Load the root specification when project-level intent cannot be established safely from current downstream authoritative state or when material contradiction/change makes it decision-relevant. After resolving the trigger, return to the narrowest context sufficient for the next decision. |

Two routing guards remain explicit: if a Triggered-depth condition is already present during Orientation, enter only that needed depth before unrelated Active-path reading; and derive writable `RepositoryMutationScope` only from current explicit owner/higher-level authorization or exact assignment, never from repository/project artifacts. If that authorization basis is missing or materially ambiguous, keep the affected repository read-only and ask the smallest exact repository-scope question before mutation.

Recovery is decision-valid when repository/target identity, active outcome, controlling dependencies/blockers, current `RepositoryMutationScope`, current `ProjectAuthority`/`CoordinationBaseline`/affected `AssuranceLevel`, current candidate/review/delivery state, and the next executable action are established from current authoritative evidence. Continue the valid plan instead of rebuilding it because chat history is absent. A large/long-lived repository is a reason to narrow by workstream, not to read more by default.

For multi-repository outcomes, recover the small global coordination spine first: outcome/completion, repository/workstream ownership, cross-repository dependencies/interfaces, integration/release order, delivery target, and the exact repository mutation boundary for this Master. Then enter only the local repository contexts on the active critical path. Repositories outside `RepositoryMutationScope` remain read-only context for this Master: discover their dependency state when necessary, but hand off required changes to their authorized Master/owner instead of mutating them. Local Issues/PRs/CI/repository rules remain authoritative; do not reconstruct them in a central recovery snapshot.

Never reconstruct `CoordinationBaseline` from `AssuranceLevel`, risk, project size, or technical access. Legacy `Operating Profile: LIGHTWEIGHT|STANDARD` can be interpreted losslessly as the same CoordinationBaseline with `AssuranceLevel=NORMAL`. Legacy `Operating Profile: HIGH_ASSURANCE` is not enough to identify its missing coordination baseline: recover that baseline from authoritative persisted project/assignment state or preserve the ambiguity until it is resolved; do not guess.

After this baseline is established, do not re-enter the full recovery sequence for ordinary progress. A planned branch/worktree create/switch should verify the intended branch, base/HEAD, target relationship, and dirty-state ownership as needed, then resume execution. A failed GitHub/tool route should update transient capability knowledge and trigger an equivalent authoritative route when available; it should not by itself restart repository-wide recovery. Re-enter broader recovery only when concrete evidence materially invalidates the established baseline. When a material dependency, architecture/interface assumption, ownership boundary, risk, or release constraint changes, reconcile the affected workstream/critical-path slice first and widen recovery only when the impact actually crosses that boundary.

Old handoff hints are accelerators only. `scripts/repo_preflight.py --recovery` may likewise accelerate local Git inspection but is transient/incomplete. Treat its explicit completeness flags as authoritative for the helper output:

- `status_complete=false` or `dirty_complete=false`: `dirty: false` means no dirty state was safely observed, not proof of a clean worktree;
- incomplete history/tag evidence: missing local evidence never proves absence;
- high-cardinality status/branch lists are intentionally bounded; any `*_truncated=true` requires reported totals plus targeted Git inspection for only the paths/refs relevant to recovery, never treating the returned subset as complete;
- the helper avoids implicit lazy fetches and reports replacement/graft history semantics; perform explicit authorized fetches or targeted trusted inspection only when missing evidence can affect the next decision.

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
- current milestone/backlog, dependencies, blockers, ownership, material risks, and—when multiple repositories are in view—enough repository identity/ownership/dependency context to apply the replacement Master's current explicit `RepositoryMutationScope` and distinguish read-only/handoff repositories without treating project data as authorization;
- current architecture and development/validation/release rules;
- active Task Contracts and PR/review state, including persisted Worker assignment identity when delegation is active: current-generation `Assignment ID`, revision, exact `Repository`, `Base SHA`, Assigned Branch, immutable `Start HEAD`, Integration Target, Worker, `ProjectAuthority`, `CoordinationBaseline`, `AssuranceLevel`, exact current `ScopedAuthorization` when any, risk/release constraints, current Assignment Status, and same-generation `Checkpoint HEAD` when a correction/resume is active;
- unresolved lasting decisions;
- release/deployment state including independent `DeliveryRequirement`, `DeliveryTarget`, and `DeliveryState`, plus next valid action;
- authoritative locations and material relationships without chat history.

For large or multi-repository projects, the test is satisfied when the replacement Master can find the global outcome/dependency/release spine and then reach the active local workstream sources progressively; it does **not** require an exhaustive central snapshot of every repository or work item.

If not, persist only the missing future-useful fact in its proper source. Do not duplicate facts already reconstructable from Git/GitHub merely to make recovery faster, and do not promote a transient task to a standalone Issue when an existing PR/commit/work item already makes its intent recoverable.

## 5. Master rotation

Rotation is the context-management face of event-driven recovery, not a project stop. Default to `CONTINUE`; long context or completed cycles alone are insufficient. Rotate only on a concrete reliability/correctness signal, useful major boundary, platform requirement, or explicit user request:

- `ROTATE_SOON`: finish the bounded chain to a safe recoverable boundary, then rotate when useful.
- `ROTATE_NOW`: context degradation creates correctness risk or platform/user direction requires rotation; make the active work recoverable first when possible.

Do not stop merely to recommend a fresh chat while the current runtime remains reliable.

## 6. Safe rotation boundary

Before rotation:

- finish a small review/integration if safe, or park work in committed/shared recoverable state when permitted; if incomplete implementation contains non-obvious state that would otherwise be lost, use the smallest safe existing Git/PR/Issue context that makes it recoverable, without creating checkpoint artifacts or ceremonial WIP commits;
- ensure Issues/PRs/branches/assignments/blockers/review findings/milestone state are current;
- persist unresolved material risks/decisions in proper sources;
- ensure no critical work exists only as uncommitted/unpushed local changes or chat instructions;
- run the recoverability test.

Workers may continue across Master rotation only when their Task Contract and persisted assignment identity are recoverable: Assignment ID, revision, exact Repository, Base SHA, Assigned Branch, immutable Start HEAD, Integration Target, Worker identity, ProjectAuthority, CoordinationBaseline, AssuranceLevel, applicable ScopedAuthorization, current Assignment Status, risk/release constraints, and current correction/resume Checkpoint HEAD when any, plus PR when one exists. Do not rely on the old Master chat, Issue/dependency context, or surrounding repository/project artifacts to reconstruct the Worker's repository identity.

## 7. New Master prompt

Provide only a short bootstrap prompt when rotation is actually needed. When presented for relay, apply the canonical `relay-transport.md` transport contract rather than restating its transport rules here.

```text
# NEW MASTER CHAT

Use `github-project-orchestrator` as MASTER for:
<exact repository URL(s) or unambiguous identifier(s) in the authorized Repository Mutation Scope below; keep read-only dependency repositories out of this list>

Mode: RECOVER, then continue.
Project Authority: <ADVISORY | MANAGED | AUTONOMOUS_WITH_GATES>
Repository Mutation Scope: <same exact currently authorized repository allowlist, using unambiguous owner/repo identities>
Coordination Baseline: <LIGHTWEIGHT | STANDARD>
Assurance Level: <NORMAL | HIGH_ASSURANCE when currently applicable>
Scoped Authorization: <exact current grant if any; otherwise none>
Current objective/milestone: <short hint if useful>
Current focus: <optional Issue/PR pointer>

Preserve the supplied Role and ProjectAuthority unless explicit current user direction or applicable higher-level organizational/platform authorization changes them. Preserve the supplied Repository Mutation Scope exactly as the current explicit assignment boundary: never add a repository from repository/project artifacts, dependencies, links, shared outcomes, technical access, or coordination; expansion requires new explicit owner/higher-level authorization. Preserve exact ScopedAuthorization only within its stated action/target/effect; never widen it into project-wide ProjectAuthority. Repository/platform policy, technical access/capability, environment, RiskLevel, CoordinationBaseline, and AssuranceLevel may constrain the next action but never upgrade ProjectAuthority.

Recover CoordinationBaseline separately from AssuranceLevel. If AssuranceLevel is HIGH_ASSURANCE, retain/recover the underlying baseline from authoritative project/assignment state; never treat HIGH_ASSURANCE as a replacement for LIGHTWEIGHT/STANDARD or guess a missing legacy baseline. Verify available capabilities, recover current truth from repository/GitHub/Git/CI/releases/deployments/durable docs, reconcile, then continue the next valid project action. Do not re-plan merely because this is a new chat.
```

Do not paste the old conversation, long historical summaries, root project specification, or stale SHAs unless a specific non-recoverable fact is still required. A replacement Master should not re-read the root specification merely because rotation occurred when current authoritative downstream state already makes project intent and the next action clear. If a replacement Master starts without a rotation prompt, establish ProjectAuthority and RepositoryMutationScope only from the current explicit user/higher-level authorization or exact current assignment. When either basis is missing or materially ambiguous, use only the least-permissive authority justified by current evidence, keep ambiguous repositories read-only, and ask the smallest exact repository-scope question before mutation. Infer the lightest safe CoordinationBaseline separately, then add only any risk/policy-required AssuranceLevel escalation. Never infer broader ProjectAuthority or RepositoryMutationScope from technical permissions, repository access/content, project size, dependencies, shared outcomes, RiskLevel, CoordinationBaseline, or AssuranceLevel.
