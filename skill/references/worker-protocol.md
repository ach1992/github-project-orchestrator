# Worker Protocol

Workers are bounded implementation agents. Master keeps priority, contract changes, acceptance, integration, release, and project continuation.

## 1. Before editing

Read the current work item/contract and repository instructions. Verify:

- exact assigned repository;
- active Assignment ID + Contract Revision;
- assigned branch and Integration Target;
- `Start HEAD` for a new assignment, or Master-supplied `Checkpoint HEAD` for correction/resume;
- scope, acceptance, required validation, and any explicit action constraints.

If a material assignment assumption changed, return `STALE_ASSIGNMENT`; do not guess or broaden scope. Repositories mentioned only as dependencies/context remain read-only unless this assignment explicitly targets them.

Use an isolated worktree when useful, but never persist the worktree path as assignment identity.

## 2. Dispatch

Persist the assignment identity in [task-contract.md](task-contract.md) before dispatch. Send a compact standalone prompt:

```text
# WORKER DISPATCH

Repository: <exact repository>
Issue/Work item: <canonical identity>
Assignment ID: <unique generation>
Contract Revision: <integer>
Assigned Branch: <branch>
Start HEAD: <sha for new generation>
Checkpoint HEAD: <sha for correction/resume, otherwise none>
Integration Target: <branch>
Allowed actions: <bounded implementation/branch/PR actions>
Goal / Scope / Acceptance: <or instruct Worker to read the current work item>
Required validation: <checks>
Special constraints: <only task-specific items>

Use github-project-orchestrator as WORKER.
Verify the assignment before editing. Implement only this scope on the assigned branch.
Do not integrate/release the Integration Target or start another task.
Return the handoff defined below.
```

Do not repeat the full project history or repository-wide rules when their authoritative sources are reachable.

Legacy dispatches may contain fields such as Project Authority, Coordination Baseline, Assurance Level, or Task Risk. Honor their material constraints, but do not require or propagate those labels into a new dispatch when the concrete allowed actions/constraints above carry the same meaning.

## 3. Execute

Worker should:

1. understand expected behavior and the relevant implementation path;
2. make the smallest correct contract-bounded change using repository conventions;
3. validate proportionally using the required evidence and useful targeted checks;
4. inspect the final relevant diff/worktree state;
5. commit/push only assigned work to the assigned branch/PR;
6. stop instead of inventing a material product, architecture, data, authorization, release, or scope decision.

Ordinary reversible implementation choices stay with the Worker; do not bounce them to Master.

## 4. Staleness and blockers

Return `STALE_ASSIGNMENT` when Assignment ID/Worker/revision/repository/assigned branch/Integration Target/checkpoint no longer matches, or when upstream/contract drift materially invalidates the implementation assumptions.

Normal authorized commits on the assigned branch do not make `Start HEAD` stale.

Use one controlling status:

| Status | Use when |
|---|---|
| `STALE_ASSIGNMENT` | assignment identity or material assumptions changed |
| `MATERIAL_DECISION_REQUIRED` | a Master/owner decision is required to continue |
| `SCOPE_CHANGE_REQUIRED` | acceptance requires material work outside the contract |
| `ENVIRONMENT_MISMATCH` | another valid runtime/environment can likely execute the same contract |
| `BLOCKED` | an external prerequisite prevents progress |
| `READY_FOR_REVIEW` | implementation is complete enough for Master review and required Worker validation is reported |

Do not solve adjacent work after a blocker without a revised assignment.

## 5. Handoff

When the handoff is copied between chats/agents, apply [relay-transport.md](relay-transport.md).

```text
# WORKER HANDOFF

STATUS: READY_FOR_REVIEW | BLOCKED | ENVIRONMENT_MISMATCH | STALE_ASSIGNMENT | SCOPE_CHANGE_REQUIRED | MATERIAL_DECISION_REQUIRED
Repository: <exact repository>
Issue/Work item: <identity>
Assignment ID: <id>
Contract Revision: <n>
Assigned Branch: <branch>
HEAD: <current sha or unavailable>
Integration Target: <branch>
PR: <url or none>

Completed:
- <concise result or none>

Validation:
- <exact check> — PASS | FAIL | NOT_RUN — <evidence/reason>

Blocker/Decision:
- <none or exact blocker/decision>
```

The handoff is a locator and claim, not review proof. Master verifies current Git/GitHub/CI evidence before relying on it.

## 6. Correction/resume

Reuse the same assignment generation only while the same Worker/branch/contract remains valid. Send the exact Repository, work item, Assignment ID, Contract Revision, Assigned Branch, Integration Target, reviewed current `Checkpoint HEAD`, and only the changed findings/constraints/required validation. Worker verifies that checkpoint before editing.

If responsibility, branch, contract assumptions, or generation validity materially changed, Master issues a fresh Assignment ID.
