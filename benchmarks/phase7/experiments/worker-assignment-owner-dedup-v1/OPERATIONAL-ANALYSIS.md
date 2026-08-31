# Source-Grounded Operational Analysis

Experiment: `worker-assignment-owner-dedup-v1`
Tracking: #54

This analysis compares canonical decision/application paths, not private model reasoning. The supported benefit claim is ownership/locality: one persisted assignment-identity ontology plus concise Worker-owned verification behavior instead of repeating the persisted field list inside that behavior.

Canonical Rule Map boundary used throughout:

- `ASSIGNMENT-IDENTITY` -> `task-contract.md`;
- `START-HEAD-HISTORICAL` -> `worker-protocol.md`;
- `CORRECTION-CHECKPOINT` -> `worker-protocol.md`;
- `STALE-ASSIGNMENT` -> `worker-protocol.md`;
- `WORKER-TARGET-SEPARATION` -> `worker-protocol.md`.

The candidate must remove only duplicate persisted-field enumeration; it must not move these Worker-owned behaviors to Task Contract.

## 1. Initial Worker dispatch before first edit

Input:

- persisted ACTIVE assignment exists with Assignment ID, revision, Base SHA, Assigned Branch, Start HEAD, Integration Target, Worker identity, Authority/profile, risk/release and validation;
- Worker has not made the first contracted edit.

Protected behavior:

- load current contract + persisted assignment identity;
- verify repository/workdir/branch/worktree and the current envelope;
- current assigned-branch/worktree HEAD must equal immutable Start HEAD before first edit;
- mismatch -> `WorkerStatus.STALE_ASSIGNMENT`.

Baseline path:

- `task-contract.md` §8 canonically owns the persisted assignment generation/envelope identity;
- Worker Protocol canonically owns the initial Start HEAD behavior and mismatch consequence;
- source Worker §1 nevertheless re-lists most persisted envelope fields before applying that behavior.

Candidate path:

- `task-contract.md` §8 remains the single persisted identity/envelope definition;
- candidate Worker §1 verifies that current envelope without re-listing it;
- candidate check 3 remains the Worker-owned initial Start HEAD rule;
- mismatch consequence remains local in Worker Protocol.

Decision: **identical**.

Structural difference: the Worker no longer reconciles two normative persisted-field lists before applying the same Worker-owned concurrency rule.

Protected rules/evals: `ASSIGNMENT-IDENTITY`, `START-HEAD-HISTORICAL`, `AK`, `AM`, `DG`.

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

- Task Contract persists Start HEAD inside the assignment envelope;
- canonical `START-HEAD-HISTORICAL` behavior is owned by Worker Protocol and is represented in Worker §1 plus the staleness section.

Candidate path:

- Task Contract continues to persist Start HEAD unchanged;
- candidate Worker §1 check 3 explicitly preserves normal authorized same-generation advance;
- detailed Worker staleness classifier remains unchanged.

Decision: **identical**.

Structural difference: enough local Worker guidance remains to preserve the canonical historical-anchor rule, while the persisted assignment field ontology is not re-listed.

Protected rule/eval: `START-HEAD-HISTORICAL`, `CR`.

## 3. Same-generation correction/resume

Input:

- same Assignment ID / Worker / branch / PR generation remains valid;
- Master supplies reviewed/current Checkpoint HEAD.

Protected behavior:

- immutable Start HEAD is not rewritten;
- current assigned-branch HEAD must equal Checkpoint HEAD before editing;
- unexpected divergence -> `WorkerStatus.STALE_ASSIGNMENT`.

Baseline path:

- Task Contract persists assignment identity and provides the Checkpoint field in the envelope;
- canonical `CORRECTION-CHECKPOINT` behavior is owned by Worker Protocol;
- source Worker §1 states the pre-edit Checkpoint equality and Corrections section owns the detailed correction payload/flow.

Candidate path:

- Task Contract continues to persist the envelope field;
- candidate Worker §1 check 4 remains the Worker-owned pre-edit Checkpoint equality rule;
- Corrections section remains byte-identical and owns the detailed correction flow.

Decision: **identical**.

Structural difference: persisted identity, pre-edit Worker behavior, and detailed correction procedure each remain with their existing owners; only the duplicate persisted-field enumeration is removed.

Protected rule/evals: `CORRECTION-CHECKPOINT`, `DG`, `AV`, `CR`.

## 4. Assignment generation replaced or invalidated

Input:

- Assignment ID/Worker/status/revision/branch/target/envelope no longer matches current authoritative assignment, or materiality is uncertain.

Protected behavior:

- Worker stops with `WorkerStatus.STALE_ASSIGNMENT`;
- never guesses new scope/identity;
- Master reconciles/reissues as needed.

Baseline path:

- Task Contract owns persisted assignment-generation identity;
- Worker Protocol owns stale-assignment behavior and the exact drift classifier;
- source Worker §1 repeats the persisted field list before stating the mismatch consequence.

Candidate path:

- Task Contract remains the single persisted identity definition;
- candidate Worker §1 check 2 verifies the current envelope and maps material identity/checkpoint mismatch to STALE;
- exact downstream Worker drift classifier remains unchanged.

Decision: **identical**.

Structural difference: no competing persisted-field enumeration, while canonical Worker-specific stale classification remains local.

Protected rules/evals: `ASSIGNMENT-IDENTITY`, `STALE-ASSIGNMENT`, `AV`, `AK`.

## 5. Assigned branch versus Integration Target

Input:

- persisted envelope carries Assigned Branch and canonical Integration Target.

Protected behavior:

- assigned branch is distinct from Integration Target;
- Worker does not take target integration ownership.

Baseline path:

- Task Contract persists both identities and validates assignment shape;
- Worker Protocol owns target-separation/integration-boundary behavior.

Candidate path:

- candidate check 2 verifies the persisted envelope rather than re-listing both fields;
- all downstream Worker execution/target-separation/integration-owner text remains byte-identical.

Decision: **identical**.

Structural difference: identity values remain in the schema owner; behavior remains in Worker Protocol without duplicating the schema enumeration in Isolation.

Protected rule/evals: `WORKER-TARGET-SEPARATION`, `AM`, `CP`.

## 6. Master unavailable during Worker execution

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

- `task-contract.md` remains the single persisted `ASSIGNMENT-IDENTITY` owner;
- Worker Protocol remains the canonical owner of Start HEAD historical behavior, correction Checkpoint behavior, stale assignment, and target separation;
- candidate Worker §1 retains those relevant pre-edit behaviors but no longer re-declares the entire persisted envelope;
- no new reference hop is introduced because Worker entry already mandates both references;
- transport schemas remain complete and unchanged;
- no state, field, Rule ID, authority boundary, routing edge, canonical rule owner, or lifecycle changes.

The candidate does **not** claim live-model accuracy/latency improvement. Its Phase B value is reduced competing persisted-identity enumeration and more direct semantic-shape matching: schema/table for persisted assignment identity, ordered procedure for Worker-owned pre-edit verification.
