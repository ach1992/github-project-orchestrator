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
7. determine active outcome/completion condition, review queue, blockers, delivery state, and next executable action; when current effective profile is `HIGH_ASSURANCE`, recover the coordination baseline implied by current project/assignment state and retain those controls;
8. continue the valid plan instead of rebuilding it because chat history is absent.

After this baseline is established, do not re-enter the full recovery sequence for ordinary progress. A planned branch/worktree create/switch should verify the intended branch, base/HEAD, target relationship, and dirty-state ownership as needed, then resume execution. A failed GitHub/tool route should update transient capability knowledge and trigger an equivalent authoritative route when available; it should not by itself restart repository-wide recovery. Re-enter broader recovery only when concrete evidence materially invalidates the established baseline.

Old handoff hints are accelerators only. `scripts/repo_preflight.py --recovery` may accelerate local Git inspection but is transient and incomplete. Treat any explicit completeness flag as authoritative for the helper output: when `status_complete`/`dirty_complete` is false, `dirty: false` means no dirty state was safely observed, not proof that the worktree is clean; when history/tag completeness is false, do not infer absence from the missing local evidence. Its high-cardinality status/branch lists are intentionally bounded; when `*_truncated` is true, use the reported totals plus targeted Git inspection for the paths/refs relevant to recovery rather than treating the returned subset as complete. The helper intentionally avoids implicit lazy fetches and reports replacement/graft history semantics; perform explicit authorized fetches or targeted trusted inspection only when the missing evidence can affect the next decision.

## 3. Reconciliation rules

When state is stale or contradictory:

- prefer current direct evidence using the source hierarchy in `SKILL.md`;
- correct the authoritative current source rather than adding a compensating note elsewhere;
- close/supersede duplicates only after confirming intent/current work;
- preserve concurrent valid work and use optimistic concurrency for overwrite-sensitive updates;
- do not infer completed delivery from merged code or stale status fields;
- treat Worker summaries/chat as locators, not proof.

## 4. Recoverability test

A replacement Master with no chat history should be able to find, when relevant:

- project purpose, active outcome/success model/non-goals/durable constraints, with the canonical root project specification discoverable as the repository-level source for initial/project-level intent when needed;
- current milestone/backlog, dependencies, blockers, ownership, material risks;
- current architecture and development/validation/release rules;
- active Task Contracts and PR/review state, including persisted Worker assignment identity (current assignment-generation `Assignment ID`, revision, base, assigned branch/expected HEAD, Integration Target, Worker, execution Authority/profile, risk, and current status) when delegation is active;
- unresolved lasting decisions;
- release/deployment state and next valid action;
- authoritative locations and material relationships without chat history.

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

- finish a small review/merge if safe, or park work in committed/shared recoverable state when permitted; if incomplete implementation contains non-obvious state that would otherwise be lost, use the smallest safe existing Git/PR/Issue context that makes it recoverable, without creating checkpoint artifacts or ceremonial WIP commits;
- ensure Issues/PRs/branches/assignments/blockers/review findings/milestone state are current;
- persist unresolved material risks/decisions in proper sources;
- ensure no critical work exists only as uncommitted/unpushed local changes or chat instructions;
- run the recoverability test.

Workers may continue across Master rotation only when their Task Contract and persisted assignment identity, assigned branch/expected HEAD, Integration Target, Worker identity, execution Authority/profile, current status, and PR when one exists are recoverable. Do not rely on the old Master chat to reconstruct an active assignment.

## 7. New Master prompt

Provide only a short bootstrap prompt when rotation is actually needed:

```text
# NEW MASTER CHAT

Use `github-project-orchestrator` as MASTER for:
<repository URL or unambiguous identifier>

Mode: RECOVER, then continue.
Authority: <ADVISORY | MANAGED | AUTONOMOUS_WITH_GATES>
Operating profile: <LIGHTWEIGHT | STANDARD | HIGH_ASSURANCE>
Current objective/milestone: <short hint if useful>
Current focus: <optional Issue/PR pointer>

Preserve the supplied Role and Authority unless explicit current user direction or applicable higher-level organizational/platform authorization changes them, and preserve the scope of that authorization rather than widening an exact one-off permission into project-wide Authority. Repository/platform policy, technical access/capability, environment, risk, and Operating profile may further constrain the next action but never upgrade Authority by themselves. Re-establish the coordination baseline separately from actual coordination/recovery needs, then apply any justified `HIGH_ASSURANCE` escalation; if the current effective profile is `HIGH_ASSURANCE`, retain/recover the underlying coordination controls from authoritative project state rather than treating it as a replacement for `LIGHTWEIGHT`/`STANDARD`. Verify available capabilities, recover current truth from repository/GitHub/Git/CI/releases/deployments/durable docs, reconcile, then continue the next valid project action. Do not re-plan merely because this is a new chat.
```

Do not paste the old conversation, long historical summaries, root project specification, or stale SHAs unless a specific non-recoverable fact is still required. A replacement Master should not re-read the root specification merely because rotation occurred when current authoritative downstream state already makes project intent and the next action clear. If a replacement Master starts without a rotation prompt and Authority cannot be safely established from the current request or applicable higher-level authorization policy, use the least-permissive Authority justified by that evidence before consequential mutation; infer the lightest safe coordination baseline separately, then add any risk/policy-required assurance escalation. Never infer broader Authority from technical permissions, repository access, project size, risk level, or profile.
