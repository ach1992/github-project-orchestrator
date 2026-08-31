# Worker Assignment Owner Dedup v1

Tracking: #35 -> #37 -> #50 -> #54

Status: isolated representation prototype; **not canonical runtime**.

## Hypothesis

Worker execution already has a canonical persisted assignment-identity owner: `task-contract.md` §8. The kernel requires Workers to load both `task-contract.md` and `worker-protocol.md` before editing. `worker-protocol.md` §1 currently repeats most of that identity/envelope field list and the Start/Checkpoint semantics before stating the Worker-specific verification consequence.

This prototype separates ownership from use:

- `task-contract.md` §8 continues to own the exact assignment envelope and generation/concurrency semantics;
- `worker-protocol.md` §1 becomes the short pre-edit procedure for consuming/verifying that already-loaded envelope;
- dispatch/handoff schemas remain complete because they are transport artifacts, not explanatory duplication;
- staleness classification remains in Worker Protocol because it is Worker-specific behavior.

No Rule ID, state, assignment field, lifecycle, authority boundary, branch/target rule, handoff field, or routing edge changes.

## Frozen identities

- prototype source/current-target snapshot: `af4b2aa86d8a13ca5f45ecf6ed4aadc8f741c386`;
- immutable semantic comparison baseline: `f98e8a242c720931e34aa7c4e8a799090e3d0495` (`v1.2.2`);
- canonical assignment owner: `skill/references/task-contract.md` §8;
- candidate replacement target: `skill/references/worker-protocol.md` §1 only;
- canonical runtime remains current `main`; this prototype never writes `skill/`.

## Why the canonical-owner reference is safe

`SKILL.md` Worker entry already requires a Worker to load the current Task Contract/work item, `task-contract.md`, and `worker-protocol.md` before editing. The candidate therefore creates no new reference hop or optional dependency: it removes a second prose rendition of information that is already mandatory active context.

If that co-loading rule changes in a future runtime, this representation must be re-evaluated; the candidate does not assume deep transitive loading.

## One-to-one semantic ledger

| Source `worker-protocol.md` §1 semantic | Candidate / canonical location | Preservation |
|---|---|---|
| one Worker = one Task Contract + one assigned branch | candidate opening sentence | retained |
| dedicated worktree may be used for isolation | candidate opening sentence | retained |
| worktree path is runtime location, never assignment identity | candidate opening sentence + canonical `task-contract.md` §8 | retained |
| repository/working directory must be verified | candidate check 1 | retained |
| current worktree/branch attachment and safety must be verified | candidate check 1 | retained |
| Issue / Task Contract revision | canonical assignment envelope in `task-contract.md` §8; candidate check 2 requires every persisted assumption current | single owner retained |
| Assignment ID / Worker identity / active Assignment Status | canonical assignment envelope; candidate check 2 | single owner retained |
| exact Base SHA / Assigned Branch / distinct Integration Target | canonical assignment envelope; candidate check 2 | single owner retained |
| inherited ProjectAuthority / CoordinationBaseline / AssuranceLevel / ScopedAuthorization | canonical assignment envelope; candidate check 2 + final no-upgrade guard | single owner + Worker-specific guard retained |
| repository rules / required validation / task risk-release constraints | candidate check 2 | retained locally because these are pre-edit execution checks, not assignment-field ontology |
| initial dispatch HEAD equals immutable Start HEAD before first edit | candidate check 3 + canonical Start HEAD definition | retained |
| normal authorized same-generation commits may advance beyond Start HEAD | candidate check 3 + canonical Start HEAD semantics | retained |
| same-generation correction/resume current HEAD equals Master Checkpoint HEAD | candidate check 4 + canonical Checkpoint definition | retained |
| material identity/checkpoint mismatch -> `WorkerStatus.STALE_ASSIGNMENT` | candidate final paragraph | retained as Worker-specific consequence |
| never guess through mismatch | candidate final paragraph | retained |
| Worker never upgrades ProjectAuthority / ScopedAuthorization / CoordinationBaseline / AssuranceLevel | candidate final paragraph | retained |
| Worker never broadens assignment because Master unavailable | candidate final paragraph | retained |

## Content intentionally unchanged

The candidate does **not** touch:

- Task Contract §8 assignment table/generation rules;
- Worker dispatch prompt and all field labels;
- Worker execution rules;
- `WorkerStatus.STALE_ASSIGNMENT` classifier and drift table;
- Worker handoff precedence/schema;
- blocker classification;
- Master absorption;
- correction/resume semantics;
- direct Worker entry routing in `SKILL.md`;
- machine-relay transport behavior.

These are distinct semantic/transport owners and are not removed merely because some literals repeat.

## Representation rationale

The source §1 paragraph is doing two jobs at once:

1. re-declaring the persisted assignment ontology already owned by `task-contract.md`;
2. specifying the Worker's pre-edit verification procedure.

Under the #50 framework, ontology and procedure are different semantic shapes. The assignment envelope stays a table/schema in its canonical owner; Worker Protocol uses a short numbered verification procedure because sequence/before-edit action is the actual local behavior.

The candidate is therefore not "shorter prose for its own sake". It removes one competing rendition of the assignment envelope while keeping the exact Worker action local.

## Protected evidence surface

At minimum preserve:

- `AK` — replacement Master can recover Worker before first push;
- `AM` — Worker branch cannot be Integration Target and branch identities stay canonical;
- `AV` — replacement/reissue requires fresh assignment generation;
- `CR` — authorized Worker progress is not staleness;
- `DG` — immutable Start HEAD vs correction Checkpoint HEAD;
- `DB` — CoordinationBaseline + HIGH_ASSURANCE survive Worker dispatch/resume independently;
- `CP` — Worker never takes integration ownership;
- all current dispatch/handoff field labels;
- all current WorkerStatus/state namespace tokens;
- every non-target runtime byte from the source snapshot.

## Selection boundary

This prototype is eligible for later #38 migration only if mechanical isolation, semantic ledger review, source-grounded operational analysis, relevant regressions, and maintenance/routing analysis all support it. A live model/API trial is optional corroboration only under the current #35/#37 contract.
