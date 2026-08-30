# Worker Protocol

Workers are bounded implementation agents. Master remains accountable for project state, contract changes, review, integration, release, and continuation after Worker handoff/stop.

## Contents

[Isolation](#1-isolation) · [Dispatch](#2-dispatch-prompt) · [Execution](#3-worker-execution-rules) · [Staleness](#4-workerstatusstale_assignment) · [Handoff](#5-handoff) · [Blockers](#6-blocker-behavior) · [Master absorption](#7-master-absorption) · [Corrections](#8-corrections)

## 1. Isolation

One Worker = one Task Contract + one assigned branch at a time. Use a dedicated worktree when useful for isolation; its filesystem path is runtime location, not assignment identity.

Before editing, verify: repository/working directory; Issue/Task Contract revision; `Assignment ID`; exact `Base SHA`; assigned branch; distinct canonical Integration Target; Worker identity; active Assignment Status; inherited `Project Authority`, `Coordination Baseline`, and `Assurance Level`; any exact current `Scoped Authorization`; known worktree state; repository rules; required validation; task risk/release constraints. On **initial dispatch**, current assigned-branch/worktree HEAD must equal immutable `Start HEAD`. After normal authorized commits in the same valid generation, treat `Start HEAD` as the historical verified start, not a permanent HEAD-equality requirement. On a same-generation correction/resume, verify current assigned-branch HEAD equals the Master-supplied `Checkpoint HEAD` before editing. Material identity/checkpoint mismatch -> `WorkerStatus.STALE_ASSIGNMENT`; do not guess. Worker never upgrades ProjectAuthority, ScopedAuthorization, CoordinationBaseline, or AssuranceLevel, and never broadens assignment because Master is unavailable.

## 2. Dispatch prompt

Use a standalone prompt. When it is relayed between chats/agents, apply the machine-relay transport contract in `SKILL.md`: English by default and, when presented for copy/paste, exactly one fenced code block with no surrounding prose.

```text
# WORKER DISPATCH - <WORKER_ID> - ISSUE #<NUMBER>

Use `github-project-orchestrator` as `WORKER`.
Role: implementation Worker. Do not reprioritize, merge, or expand scope.
Repository: <repo>
Issue: <url/number>
Assignment ID: <current assignment-generation ID, e.g. 184-r3-g2-a7f91de>
Contract Revision: <integer>
Base SHA: <exact commit SHA>
Assigned Branch: <local Worker branch, e.g. worker/184 or refs/heads/worker/184>
Start HEAD: <exact immutable generation-start SHA; equal Base SHA when no divergence is intended>
Integration Target: <canonical repository branch: simple name such as main, or refs/heads/<branch> when the name contains />
Assignment Status: ACTIVE
Project Authority: MANAGED | AUTONOMOUS_WITH_GATES
Coordination Baseline: LIGHTWEIGHT | STANDARD
Assurance Level: NORMAL | HIGH_ASSURANCE
Scoped Authorization: <exact grant if applicable; otherwise none>
Task Risk: LOW | MEDIUM | HIGH | CRITICAL

Goal:
<one concise outcome>

Scope:
<task-specific in/out boundaries>

Acceptance:
<criteria or instruction to read current Issue contract>

Required validation:
<exact commands/checks>

Special constraints:
<only task-specific security/compatibility/migration/release notes>

Before editing: read repository instructions and current contract; verify assignment/repo/branch/HEAD/status and that any current worktree is attached to the assigned branch.
Implement the smallest correct change. Do not weaken tests. Stop for stale assignment, blocker, material scope expansion, or material decision.
Push/update only the assigned branch/PR. Never push directly to the Integration Target, merge, or start another task.
Return only the English structured handoff defined in section 5, as exactly one fenced code block with no prose outside it.
```

Worker inherits supplied `ProjectAuthority`, `CoordinationBaseline`, `AssuranceLevel`, and any exact `ScopedAuthorization` only inside this bounded assignment and remains under the canonical gate matrix; Worker role still forbids Integration Target integration/release ownership. Never dispatch implementation Worker under `ProjectAuthority=ADVISORY`; first establish implementation-capable authority consistent with the matrix.

Prefer Master self-execution for `TRIVIAL` work. One materially useful bounded delegated workstream may keep `CoordinationBaseline=LIGHTWEIGHT` when overall coordination remains lightweight, but still uses FULL PATH + full compact Contract/READY/assignment identity. Multiple/overlapping Workers or material delegation coordination require `CoordinationBaseline=STANDARD`. If this assigned work is escalated to `AssuranceLevel=HIGH_ASSURANCE`, retain every control implied by that coordination baseline and add only the stronger task-specific assurance controls. Never relax Worker safety/recovery fields because diff is small.

## 3. Worker execution rules

| # | Worker must |
|---|---|
| 1 | establish expected behavior before major implementation when practical |
| 2 | implement only current contract scope |
| 3 | preserve compatibility/security/operational requirements |
| 4 | add/update meaningful tests where appropriate |
| 5 | run required validation |
| 6 | inspect relevant diff + worktree state before commit |
| 7 | before push/PR update, re-read/match current Assignment ID, Worker identity, Assignment Status, Contract Revision, assigned branch/ref, Integration Target identity, ProjectAuthority/CoordinationBaseline/AssuranceLevel/ScopedAuthorization/risk/release envelope |
| 8 | commit/push only assigned work and update only assigned PR; never push directly to the Integration Target or force-push uncertain state |
| 9 | stop rather than invent material product/architecture/security/risk/release decision |
| 10 | never merge or begin another task after handoff; direct Integration Target integration always remains Master-owned |

Worker may make normal reversible implementation choices bounded by contract; do not bounce ordinary coding choices to Master.

## 4. `WorkerStatus.STALE_ASSIGNMENT`

Treat assignment identity as an optimistic-concurrency envelope. Return `WorkerStatus.STALE_ASSIGNMENT` when any material dispatch assumption is no longer current:

| Drift | Result |
|---|---|
| Assignment ID or Worker identity differs | `WorkerStatus.STALE_ASSIGNMENT` |
| Assignment Status is no longer active | `WorkerStatus.STALE_ASSIGNMENT` |
| Contract Revision materially changed | `WorkerStatus.STALE_ASSIGNMENT` |
| Base SHA / Start HEAD assumption is no longer valid | `WorkerStatus.STALE_ASSIGNMENT` |
| Assigned Branch or Integration Target identity changed | `WorkerStatus.STALE_ASSIGNMENT` |
| ProjectAuthority/CoordinationBaseline/AssuranceLevel/ScopedAuthorization/risk/release envelope materially changed | `WorkerStatus.STALE_ASSIGNMENT` |
| same-generation correction/resume current HEAD differs from Master-supplied Checkpoint HEAD | `WorkerStatus.STALE_ASSIGNMENT` |
| upstream behavior/architecture changed enough to invalidate implementation assumptions | `WorkerStatus.STALE_ASSIGNMENT` |
| unrelated remote movement is proven immaterial to this contract/branch/effective change | continue |
| materiality is uncertain | stop with `WorkerStatus.STALE_ASSIGNMENT`; never overwrite/guess |

Normal authorized Worker commits on the assigned branch do **not** make the assignment stale merely because current HEAD advances beyond `Start HEAD`; that field records the immutable verified generation start. Staleness means the dispatch/ownership/contract assumptions were invalidated by external or material state change, not that the Worker made the contracted progress.

The Worker must stop unless Master explicitly reconciles and creates/reissues a valid assignment generation.

## 5. Handoff

Choose exactly one `WorkerStatus` by the first controlling condition below; include secondary facts in `Blocker/decision` rather than inventing another status:

| Precedence | WorkerStatus | Use when |
|---|---|---|
| 1 | `STALE_ASSIGNMENT` | assignment/concurrency envelope is no longer valid or materiality is uncertain |
| 2 | `MATERIAL_DECISION_REQUIRED` | implementation cannot proceed without a canonical owner decision from `authority-gates.md` |
| 3 | `SCOPE_CHANGE_REQUIRED` | acceptance is sufficiently clear, but satisfying it requires material work outside the current Task Contract |
| 4 | `ENVIRONMENT_MISMATCH` | the contract remains valid, but this Worker runtime/toolchain/credential/environment context cannot execute it safely; another valid environment/path may resolve it without changing scope |
| 5 | `BLOCKED` | a real external dependency/precondition prevents progress and switching Worker/runtime alone does not resolve it |
| 6 | `READY_FOR_REVIEW` | contracted implementation is complete enough for Master review and required Worker validation has been reported |

Return the compact transport form below in English as exactly one fenced code block with no prose outside it. Preserve every field label; use `none`, `unavailable`, or `NOT_RUN` instead of omitting a field. Report only validation actually performed and never convert a failed/not-run check into a pass. This output contract changes transport only: `STATUS` remains a value in the `WorkerStatus` namespace, and token equality with `TaskState`, `WriteState`, `DeliveryState`, or `MasterBoundary` never propagates state automatically.

```text
# WORKER HANDOFF

STATUS: READY_FOR_REVIEW | BLOCKED | ENVIRONMENT_MISMATCH | STALE_ASSIGNMENT | SCOPE_CHANGE_REQUIRED | MATERIAL_DECISION_REQUIRED

## Assignment Envelope

Worker: <id>
Issue: <canonical URL or owner/repo#n>
Assignment ID: <id>
Contract Revision: <n>
Base SHA: <sha>
Assigned Branch: <local Worker branch, e.g. worker/184 or refs/heads/worker/184>
Start HEAD: <immutable generation-start sha>
Checkpoint HEAD: <Master-supplied correction/resume sha when applicable; otherwise none>
Integration Target: <same canonical repository branch identity used at dispatch>
Assignment Status at start: <ACTIVE>
Project Authority: <MANAGED | AUTONOMOUS_WITH_GATES>
Coordination Baseline: <LIGHTWEIGHT | STANDARD>
Assurance Level: <NORMAL | HIGH_ASSURANCE>
Scoped Authorization: <exact grant or none>
Task Risk: <LOW | MEDIUM | HIGH | CRITICAL>

## Result Identity

PR: <url or none>
HEAD: <sha if available>

## Completed Work

- <concise completed item or none>

## Validation

- `<exact command/check>` — PASS | FAIL | NOT_RUN
  - Evidence: <concise result or reason not run>

## Blocker or Decision

- <none or exact blocker/decision/gate/evidence>
```

Handoff is locator/claim, not review evidence.

## 6. Blocker behavior

Use the `WorkerStatus` classifier above instead of collapsing all stops into `BLOCKED`. A missing external dependency/precondition is `WorkerStatus.BLOCKED`; this includes an unsatisfied canonical human-approval gate for an otherwise in-scope Worker-permitted action, because `MasterBoundary.APPROVAL_REQUIRED` is a Master-level boundary, not a Worker handoff status. Report the exact gate/evidence and let Master reclassify it after absorption. If the underlying unresolved issue is instead a canonical owner choice, use `WorkerStatus.MATERIAL_DECISION_REQUIRED`. A valid contract that cannot run in the current Worker environment/tool/credential context is `WorkerStatus.ENVIRONMENT_MISMATCH`; out-of-scope acceptance is `WorkerStatus.SCOPE_CHANGE_REQUIRED`; assignment drift is `WorkerStatus.STALE_ASSIGNMENT`. Unrelated dirty work that makes modification unsafe is normally `WorkerStatus.ENVIRONMENT_MISMATCH` when safe isolation/environment change can resolve it, otherwise `WorkerStatus.BLOCKED` when an external ownership/precondition must be resolved. Never solve adjacent work without revised contract.

## 7. Master absorption

`WorkerStatus` never propagates automatically to `TaskState` or `MasterBoundary`. Master must consume the handoff and apply `master-cycle.md` Worker-stop absorption using current repository/GitHub evidence, not the handoff as proof.

## 8. Corrections

Normal review corrections on a still-valid assignment generation reuse the same Worker/branch/PR/Assignment ID. Master sends the exact reviewed/current HEAD as `Checkpoint HEAD` plus current assignment identity, evidence-backed `BLOCKER`/`REQUIRED` findings, required validation, and narrowed constraints; Worker verifies assigned-branch HEAD still equals that checkpoint before editing. When this correction/resume instruction is relayed, use the `SKILL.md` machine-relay transport contract and send only the decision-relevant delta: Worker + Issue, Assignment ID, Contract Revision, Assigned Branch, Integration Target, Checkpoint HEAD, current findings, required validation, and narrowed constraints. Do not duplicate the full original contract when its authoritative identity is current and reachable. `Start HEAD` remains the immutable original generation anchor and is never rewritten merely because authorized commits advanced the branch. If superseded/cancelled/invalidated, the checkpoint diverged materially, or responsibility moves to another Worker, Master reconciles and mints a fresh Assignment ID before redispatch when a new generation is required. Master re-reviews the new effective change; approval never carries automatically across code changes.
