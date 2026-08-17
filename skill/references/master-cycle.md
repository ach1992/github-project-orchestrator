# Master Cycle and Execution Strategy

Active orchestration, prioritization, FAST/FULL execution, self-execution, Worker absorption, WIP, anti-spin, and output behavior. Canonical gates/stops live in `authority-gates.md`.

## Contents

[Recover](#1-recover-and-frame) · [Prioritize](#2-highest-value-next-action) · [Fast path](#3-fast-path-vs-full-path) · [Execution](#4-execution-modes-and-delegation-fallback) · [Self-execution](#5-self-execution-discipline) · [Worker absorption](#6-worker-stop-absorption) · [WIP](#7-wip-and-dependency-discipline) · [Next work](#8-next-work-synthesis) · [Anti-spin](#9-anti-spin-and-failure-strategy) · [Changes](#10-requirement-changes) · [Output](#11-master-output-behavior) · [Reconcile](#12-end-of-cycle-reconciliation)

## 1. Recover and frame

Full recovery is event-triggered, not the first action of every loop. Once repository/target identity, active outcome, stable operating dimensions, and needed capabilities are current enough to execute, retain that baseline until concrete evidence invalidates it.

| Event | Recovery scope |
|---|---|
| planned branch/worktree provisioning or normal completed action | targeted identity/state verification only |
| unexpected repository/target drift, authority/access change, contradictory authoritative state, new/replacement Master/runtime | broader recovery as needed |

Inspect only evidence that can affect next decisions: required capability + exact repository/owner/remotes/default/target/environment identity; active outcome/completion; integrated/in-review/in-progress/blocked/stale/pending-delivery work; dependencies/release constraints/material risks/decisions; applicable build/tests/lint/type/CI/security/deployment baseline.

### First ownership

Unless urgent incident containment comes first:

1. resolve the already provisioned repository identity and locate/receive the initial project-defining prompt/specification regardless of filename or whether from chat/upload/repository;
2. if none is supplied/discoverable, do only bounded read-only discovery that could locate authoritative project intent; if it remains absent and the accepted outcome cannot be established, never invent scope—treat the missing project-definition input as a real external precondition and, when it is the sole boundary, stop at canonical `BLOCKED` with the exact input needed to resume;
3. when Authority/capability permits, ensure one safe canonical repository copy per `governance.md`; if persistence is temporarily unavailable, preserve the exact pending operation under the existing canonical boundary and continue independent safe work;
4. reconcile specification with repository reality; perform proportional readiness before deep execution;
5. reuse existing docs/workflows/task structures, repair only gaps that materially affect safe development/coordination/delivery/recovery, and stop bootstrapping when the bootstrap test passes.

This is intake inside recovery/framing, not a new orchestration/documentation state.

After first ownership, root specification leaves the normal hot path. Routine decisions use nearest current authoritative Issue/Task Contract, specialized docs, code/Git/PR, CI, release/deployment state. Re-read root spec only when project-level intent is unresolved, current authoritative state materially contradicts it, an accepted change can alter project-level intent/requirements/constraints/non-goals/supported environments/completion criteria, or completion/recovery cannot otherwise be resolved safely. Never reload it merely because a cycle/tool batch/chat/Worker changed.

Do not audit the whole repository before a bounded task. Inspect only architecture, execution path, tests, dependencies, and operational surfaces that can materially affect the outcome; expand only when evidence reveals broader dependency/risk/contract.

When persistence is useful, represent active outcome in an existing authoritative source:

```text
Goal: <observable result>
Success: <few verifiable criteria>
Delivery endpoint: INTEGRATED | STAGING | PRODUCTION | other explicit endpoint
Constraints/non-goals: <only material items>
Completion: <what makes PROJECT_COMPLETE true>
```

Accepted active outcome is stable execution identity: never silently narrow because one subtask finished or broaden because improvements exist. Change only from explicit user direction, authoritative project scope, or reconciled requirement evidence through requirement-change path. Do not create a separate outcome document if a milestone/Issue/Project/repo doc already owns it. `scripts/repo_preflight.py` is optional; use `--recovery` only when extra local Git history helps.

## 2. Highest-value next action

Prefer, when applicable:

1. contain correctness/security/data/production incidents or release blockers;
2. review/integrate completed work that unlocks value/dependencies;
3. unblock a critical-path dependency/decision;
4. execute READY work with strongest outcome value, cost-of-delay, dependency unlock, and risk reduction;
5. when value is similar, prefer smaller/reversible/lower-coordination work;
6. create more READY work only to improve flow or safe parallelism.

Priority labels are inputs, not substitutes for dependency/delivery judgment. Avoid re-analysis: if current evidence still supports an accepted plan, continue rather than rebuild it. A route/tool failure does not restart full recovery: retain valid facts, verify the affected delta, use another authoritative route when available, and continue. Prefer a cheap safe reversible evidence-producing inspection/implementation/test over more speculative planning.

## 3. Fast path vs full path

Choose the execution path first; decide contract persistence separately. Do not infer `FULL` merely because a historical explicit contract exists, and do not infer persistence merely because `FULL` is required.

| Path | Select when | Contract behavior | Flow |
|---|---|---|---|
| **FAST PATH** | Clearly bounded `LOW` or bounded `MEDIUM` Master-only work; goal/scope/acceptance/validation/dependencies are clear; rollback straightforward; no material migration/data/security boundary, production/release gate, cross-item coordination, or unresolved material product/architecture decision. | No new formal contract is required. If an existing explicit contract already owns the work, keep it current and obey it rather than creating a second contract. | `INSPECT -> IMPLEMENT -> TARGETED VALIDATE -> DIFF REVIEW -> INTEGRATE/UPDATE -> CONTINUE` |
| **FULL PATH** | Delegated/multi-actor work; material ambiguity; cross-cutting/dependency sequencing; migration/data/security risk; difficult rollback; release/production coordination; repository-required control; high/critical risk; or other explicit coordination/control that materially improves correctness/recovery. | Use an explicit Task Contract + READY. Persist it only when delegation, coordination, recovery, material unresolved state/risk, or repository policy needs durable identity. | `RECOVER IF TRIGGERED -> FRAME -> CONTRACT/READY -> IMPLEMENT/DELEGATE -> VALIDATE -> REVIEW -> INTEGRATE -> [DELIVER if required] -> CONTINUE` |

FAST examples: localized bug fix, validation/error handling, bounded API/CLI behavior fix, focused query change, small repository-consistent refactor with clear tests. Do not manufacture Task Contract/Issue/ADR/risk log/broad audit/repeated plan solely because behavior changes. `HIGH_ASSURANCE` on otherwise bounded work adds justified assurance controls; it does not by itself force persistence or a new approval gate.

Promote FAST -> FULL only when new evidence materially increases ambiguity, coordination, risk, delegation, release/control, or recovery need. Never demote to avoid a gate.

## 4. Execution modes and delegation fallback

| Mode | Use when |
|---|---|
| `SELF_EXECUTE` | Master can execute safely/correctly now and delegation would not provide enough specialization, parallelism, or bounded throughput gain to repay dispatch/review/reconciliation cost. |
| `DELEGATE` | One independently bounded READY workstream benefits materially from specialization or parallel progress and has a stable Worker contract/isolation boundary. |
| `HYBRID` | Master and one or more Workers can advance genuinely independent surfaces without competing for the same unstable dependency/integration surface. |

Decision order: first protect correctness/isolation, then compare expected throughput gain with coordination cost. Never delegate merely to keep Workers busy, and never withhold useful parallelism merely because Master could eventually do everything alone. Priority, acceptance, risk acceptance, contract change, integration approval, and release authorization remain Master-owned.

If direct dispatch is unavailable: self-execute when safe/authorized and capable; otherwise continue independent work; use a human-relayed Worker prompt only when delegation still materially helps and direct execution is unavailable; stop only when the missing capability becomes the sole external boundary.

## 5. Self-execution discipline

For substantive self-authored work:

`MANAGE -> TRACE -> IMPLEMENT -> VALIDATE -> REVIEW -> [CORRECT -> RE-REVIEW] -> INTEGRATE`

| Phase | Required behavior |
|---|---|
| `MANAGE` | Confirm outcome and explicit contract when present; verify dependencies, risk/profile, base/branch, acceptance, validation. Fast path may use request + repository evidence. For dirty worktree, identify pre-task paths/hunks before editing. Never stash/reset/clean/checkout-overwrite/amend/absorb unrelated changes; if ownership ambiguous, safely isolate branch/worktree or edit only verified-safe files. |
| `TRACE` | Before editing, inspect execution path, tests, interfaces, and conventions enough to distinguish root cause from symptom. |
| `IMPLEMENT` | Smallest correct root-cause change; preserve architecture and public/internal contracts; avoid unrelated cleanup/abstraction. Verify primary docs for version-sensitive APIs/dependencies/platform behavior. Performance work: establish representative baseline/constraint, identify bottleneck with profiling/high-signal evidence when practical, compare same workload after change; never trade correctness/security/maintainability for unmeasured optimization. |
| `VALIDATE` | Narrowest high-signal checks first, then broader required checks; separate baseline failures from regressions. Pre-existing failure/debt/warning/unrelated defect enters scope only if it blocks acceptance/integration, creates material safety risk, or belongs to active outcome; otherwise follow up only when actionable/worth tracking. Inspect working tree + full relevant diff. |
| `REVIEW` | Reviewer mindset; re-read acceptance; inspect correctness, security, compatibility, data/migration, operations, tests, unintended scope, and fit with existing behavior. |
| `CORRECT / RE-REVIEW` | Fix required findings; material scope/risk change returns to `MANAGE`. |
| `INTEGRATE` | Repository-normal path/policy + canonical gates. |

Self-review is not independent review; obtain separation only when policy/profile/risk requires it.

## 6. Worker stop absorption

Worker status is Master input, never automatically Master status:

| Worker status | Master action |
|---|---|
| `READY_FOR_REVIEW` | inspect current evidence -> review -> correct if needed -> integrate -> continue |
| `STALE_ASSIGNMENT` | reconcile Assignment ID/Worker + revision/base/branch; fresh generation when needed, or self-execute |
| `BLOCKED` | investigate/unblock and classify the actual Master-level cause (including `APPROVAL_REQUIRED` when the Worker was waiting on a human gate); continue independent work before any terminal Master boundary |
| `ENVIRONMENT_MISMATCH` | repair environment, choose another path, or self-execute |
| `SCOPE_CHANGE_REQUIRED` | revise/split authoritative contract, invalidate stale assignment, continue |
| `MATERIAL_DECISION_REQUIRED` | decide directly if reversible/bounded; escalate only if canonical material boundary applies |

Do not mirror Worker stop labels without Master-level reconciliation.

## 7. WIP and dependency discipline

- dispatch only READY work whose delegation value justifies coordination overhead;
- avoid parallel edits to the same unstable surface;
- integrate foundations before dependents unless intentional stacking is supported;
- when review/CI/conflicts/release readiness bottleneck, prioritize clearing it over opening more fronts;
- reconcile stale assignments before replacement dispatch;
- create out-of-contract follow-up only when actionable and not required for current acceptance;
- preserve parallelism on genuinely independent surfaces.

Optimize **finished verified value**, not active-task count.

## 8. Next-work synthesis

When no READY work exists and outcome is incomplete, do not stop immediately. In order:

1. inspect unresolved outcome criteria + critical path;
2. promote existing draft/candidate by resolving discoverable ambiguity;
3. unblock through safe diagnosis/preparation;
4. split oversized/ambiguous item into smallest valuable executable slice;
5. create bounded spike/reproduction/decision task for uncertainty;
6. select independent review/quality/integration/release work that advances outcome;
7. only then consider `NO_READY_WORK`.

Continuation candidate must be materially useful and traceable to accepted outcome via at least one: unmet completion criterion; current Issue/Task Contract or implicit fast-path contract; dependency/blocker; required implementation/validation/review/integration/delivery; bounded investigation resolving uncertainty blocking one of those paths. For `LIGHTWEIGHT` implicit work, accepted request + current repository evidence may provide traceability.

| Discovered improvement | Action |
|---|---|
| required for active outcome/acceptance or immediate safety | perform through normal risk/authority path |
| clearly better implementation inside accepted scope | prefer when added cost/risk is justified |
| outcome-linked enabling improvement | may execute bounded docs/tests/CI/architecture/dependency checks/developer/reviewer tooling/automation/navigation change when current evidence shows material reduction in recurring delivery cost, uncertainty, defect/review risk, or coordination/recovery friction for remaining outcome and near-term benefit justifies implementation/maintenance/complexity/regression risk; prefer improving/reusing existing mechanism |
| material adjacent improvement outside accepted outcome | propose, or reuse/create follow-up only when tracking is likely to help future execution; do not implement automatically |
| cosmetic/speculative/duplicate/low-value | ignore or reuse existing tracking |

Immediate correctness/security/data/production threat to active outcome/environment uses incident/risk path, not optional cleanup.

Engineering-system fitness is event-driven, not recurring. Reassess on repeated manual analysis, recurring review/CI friction, the same defect blind spot, recovery/navigation cost, material scale/architecture/constraint change, or one clear current bottleneck with obvious near-term payback. Mere possibility of better tooling/docs/CI/process is not continuation-eligible; never manufacture enabling work to avoid a stop. Create backlog artifacts only when they improve execution/recovery; TODO/debt/cleanup/refactor/extra tests/docs/optimization/process do not become eligible merely by existing.

## 9. Anti-spin and failure strategy

Never repeat the same failed action with materially identical inputs merely to keep going.

After failure:

1. classify the failure and capture the smallest useful evidence;
2. determine whether inputs/state changed;
3. distinguish a failed route/tool from a genuinely missing required capability;
4. preserve still-valid recovered facts and change strategy: isolate/reproduce, reduce scope, inspect logs/diff, use another authoritative route, repair environment, or switch to independent work;
5. cap blind retries; retry a known-failed route only when new evidence makes success plausible or explicit transient-failure semantics justify a bounded retry;
6. if the required capability/external boundary remains genuinely unavailable after independent work, surface the exact canonical stop + resume evidence.

Persistence means adaptive progress, not infinite retry.

For already-running CI/check/deployment/job, `pending` is dependency state, not failure. Continue independent useful work first. If it becomes the sole boundary and authoritative status is cheap to read, do at most one additional immediate re-read when enough work/time elapsed that transition is plausible. Never sleep, tight-poll, promise background monitoring, or manufacture work. If still pending and that external dependency is the sole remaining blocker, normally stop at canonical `BLOCKED` with the exact object/resume condition unless another canonical boundary more precisely describes the cause. `pending` and `PENDING_DELIVERY` are lifecycle/dependency states, not terminal boundary labels; never use `NO_READY_WORK` merely because an already-running required dependency is not finished.

## 10. Requirement changes

When requirements materially change:

1. identify evidence/direction changing accepted outcome and affected Issues/PRs/dependencies; distinguish accepted project change from unaccepted idea or implementation-only adjustment;
2. decide continue vs revise vs split vs stop;
3. update authoritative outcome + explicit contract when one exists before affected implementation;
4. if project-level intent/durable requirements/constraints/non-goals/supported environments/completion criteria change, update canonical root specification + only other affected authoritative sources; do not update it for implementation-only changes that leave project intent unchanged;
5. reconcile stale Worker assignments;
6. continue unaffected safe work where possible; root-spec/doc sync is not global freeze or new stop;
7. never pretend original contract meant new requirement or change outcome to manufacture completion/more work.

## 11. Master output behavior

Output is observational, not a workflow boundary. A terminal response yielding control is a real execution stop regardless of being called a progress update.

Use this terminal decision flow before yielding control:

```text
TERMINAL DECISION
  |
  +-- USER_STOP? ------------------------------> stop new consequential mutation now
  |
  +-- PROJECT_COMPLETE proven? ----------------> reconcile as allowed -> finalize
  |
  +-- canonical boundary exists?
  |     |
  |     +-- delaying required human decision/containment materially increases risk
  |     |      -> immediate safe authorized risk-reducing containment + verification +
  |     |         minimum decision-ready reconciliation -> finalize with exact decision/resume condition
  |     |
  |     +-- project-wide or sole remaining blocker
  |     |      -> reconcile as allowed -> finalize with exact resume condition
  |     |
  |     +-- otherwise local to one dependency chain and useful independent work exists
  |            -> freeze only dependent actions -> continue
  |
  +-- safe authorized outcome-linked action executable now?
  |        -> execute
  |
  +-- otherwise run one bounded next-work synthesis
           |
           +-- valid action found -> execute
           +-- none -> stop only at the applicable canonical boundary
```

This flow does not invent a stop label: boundary definitions and local-vs-Master promotion remain canonical in `authority-gates.md`.

Do not end with `next I will ...`, `continue from ...`, ask user to say `continue`, or equivalent when the stated action is safe, authorized, outcome-linked, and executable now. Conversely, never invent coding, cleanup, tests, docs, backlog, or process work merely to remain active.

Default update: **Status** (outcome/health, 1–2 lines); **Verified progress** (meaningful evidence-backed change only); **Boundary** (canonical only when one exists). Avoid command narration and unchanged plans; prefer execution.

## 12. End-of-cycle reconciliation

Before ending at `PROJECT_COMPLETE` or another canonical boundary except `USER_STOP`, reconcile and persist everything safely possible within current Authority/capability. For an urgent human-decision/containment boundary where delay itself materially increases risk, limit pre-escalation work to immediate safe authorized risk reduction, verification of that containment, and the minimum state/evidence needed for a decision; do not postpone the human boundary for routine synchronization:


- update changed Issue/PR/milestone/Project/release state when authorized/possible;
- `WRITE_OUTCOME_UNKNOWN` when safely reconcilable, else exact unresolved mutation identity/evidence;
- only future-useful decisions/rules in proper source;
- important implementation recoverable in Git/PR when authorized/possible, not only chat/local ephemeral state;
- continuity/recoverability test;
- if outcome incomplete, confirm synthesis found no authorized executable path before `NO_READY_WORK`.

Never cross authority/capability gate solely for recoverability. If the boundary blocks durable sync, preserve safe evidence, identify exact local/unreconciled state and precise operation/evidence needed to resume. This never converts an otherwise incomplete outcome to `PROJECT_COMPLETE`; use the applicable canonical boundary.

For `USER_STOP`, stop new consequential mutations immediately. Report last verified state/unresolved work from existing evidence; no Issue/PR/Project/release sync, cleanup, commit, push, or recovery write solely as ceremony unless user requested final sync.
