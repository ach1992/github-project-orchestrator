# Source-Grounded Operational Analysis

Experiment: `worker-assignment-owner-dedup-v1`
Tracking: #54

This analysis compares canonical decision/application paths, not private model reasoning. The supported benefit claim is ownership/locality: one assignment ontology plus one Worker verification procedure instead of two prose renditions of the same envelope.

## 1. Initial Worker dispatch before first edit

Input:

- persisted ACTIVE assignment exists with Assignment ID, revision, Base SHA, Assigned Branch, Start HEAD, Integration Target, Worker identity, Authority/profile, risk/release and validation;
- Worker has not made the first contracted edit.

Protected behavior:

- load current contract + assignment identity;
- verify repository/workdir/branch/worktree and every persisted envelope assumption;
- current assigned-branch/worktree HEAD must equal immutable Start HEAD before first edit;
- mismatch -> `WorkerStatus.STALE_ASSIGNMENT`.

Baseline path:

- `task-contract.md` §8 defines the exact persisted envelope and Start HEAD semantics;
- `worker-protocol.md` §1 lists almost the same fields again and repeats initial Start HEAD equality before applying the Worker consequence.

Candidate path:

- `task-contract.md` §8 remains the single envelope definition;
- candidate Worker §1 says to read/verify that current envelope, then performs the local branch/worktree and initial Start HEAD check;
- mismatch consequence remains local.

Decision: **identical**.

Structural difference: the Worker does not have to reconcile two normative field lists before editing.

Protected evals: `AK`, `AM`, `DG`.

## 2. Normal authorized Worker progress

Input:

- same valid assignment generation;
- Worker has made authorized commits on Assigned Branch;
- current HEAD advanced beyond Start HEAD;
- no external/material assignment drift.

Protected behavior:

- Start HEAD remains historical generation anchor;
- normal progress is not `STALE_ASSIGNMENT` merely because current HEAD advanced.

Baseline path:

- this rule exists in canonical `task-contract.md` §8 and is repeated in Worker §1 and Worker staleness section.

Candidate path:

- canonical identity owner retains the full Start HEAD semantics;
- Worker §1 check 3 explicitly preserves normal authorized same-generation advance;
- detailed Worker staleness classifier remains unchanged.

Decision: **identical**.

Structural difference: enough local Worker guidance remains to prevent false staleness, but the full assignment field ontology is not re-listed.

Protected eval: `CR`.

## 3. Same-generation correction/resume

Input:

- same Assignment ID / Worker / branch / PR generation remains valid;
- Master supplies reviewed/current Checkpoint HEAD.

Protected behavior:

- immutable Start HEAD is not rewritten;
- current assigned-branch HEAD must equal Checkpoint HEAD before editing;
- unexpected divergence -> `WorkerStatus.STALE_ASSIGNMENT`.

Baseline path:

- canonical Task Contract identity owner defines Checkpoint semantics;
- Worker §1 repeats them;
- Worker Corrections section owns the detailed correction payload/flow.

Candidate path:

- Task Contract remains the canonical Checkpoint definition;
- candidate Worker §1 check 4 applies the pre-edit concurrency check;
- Corrections section remains byte-identical and owns the detailed correction flow.

Decision: **identical**.

Structural difference: definition, pre-edit verification, and detailed correction procedure each have one distinct owner rather than Worker §1 redefining the identity field.

Protected evals: `DG`, `AV`, `CR`.

## 4. Assignment generation replaced or invalidated

Input:

- Assignment ID/Worker/status/revision/branch/target/envelope no longer matches current authoritative assignment, or materiality is uncertain.

Protected behavior:

- Worker stops with `WorkerStatus.STALE_ASSIGNMENT`;
- never guesses new scope/identity;
- Master reconciles/reissues as needed.

Baseline path:

- Task Contract defines generation identity/stale assumptions;
- Worker §1 repeats field list and mismatch rule;
- Worker staleness classifier gives the exact drift matrix.

Candidate path:

- Task Contract stays the single persisted identity definition;
- Worker §1 requires every persisted assumption current and maps material mismatch to STALE;
- exact drift classifier remains unchanged.

Decision: **identical**.

Structural difference: no competing field enumeration, while detailed Worker-specific classification remains local.

Protected evals: `AV`, `AK`.

## 5. Master unavailable during Worker execution

Input:

- current assignment is still valid;
- Master is temporarily unavailable;
- Worker encounters temptation to broaden task or reinterpret Authority/profile.

Protected behavior:

- Worker never upgrades ProjectAuthority, ScopedAuthorization, CoordinationBaseline, or AssuranceLevel;
- Worker never broadens assignment because Master is unavailable;
- integration ownership remains Master-only.

Baseline path:

- no-upgrade/no-broaden guard is at end of Worker §1 and is reinforced elsewhere in Worker role/execution.

Candidate path:

- the exact guard remains at end of candidate §1;
- dispatch/execution/integration-owner rules remain unchanged.

Decision: **identical**.

Protected evals: `DB`, `CP`.

## Net operational assessment

Supported claim:

- `task-contract.md` remains the single exact assignment envelope owner;
- Worker Protocol retains a local before-edit verification procedure and Worker-specific mismatch consequence;
- no new reference hop is introduced because Worker entry already mandates both references;
- transport schemas remain complete and unchanged;
- no state, field, Rule ID, authority boundary, routing edge, or lifecycle change is introduced.

The candidate does **not** claim live-model accuracy/latency improvement. Its Phase B value is reduced competing normative ownership and more direct semantic-shape matching: schema/table for assignment identity, ordered procedure for Worker verification.
