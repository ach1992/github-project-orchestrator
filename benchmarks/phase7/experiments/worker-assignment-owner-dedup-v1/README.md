# Worker Assignment Owner Dedup v1

Tracking: #35 -> #37 -> #50 -> #54

Status: isolated representation prototype; **not canonical runtime**.

## Hypothesis

Worker execution already has a canonical persisted assignment-identity owner: `task-contract.md` §8. The kernel requires Workers to load both `task-contract.md` and `worker-protocol.md` before editing. `worker-protocol.md` §1 currently repeats most of that identity/envelope field list while also carrying Worker-owned Start/Checkpoint verification behavior.

The Rule Map boundary is explicit and must not drift during deduplication:

- `ASSIGNMENT-IDENTITY` is canonically owned by `task-contract.md`;
- `START-HEAD-HISTORICAL` and `CORRECTION-CHECKPOINT` are canonically owned by `worker-protocol.md`;
- `STALE-ASSIGNMENT` and `WORKER-TARGET-SEPARATION` remain Worker Protocol behavior.

This prototype separates persisted identity ownership from Worker use without moving behavioral ownership:

- `task-contract.md` §8 continues to own the exact persisted assignment generation/envelope identity;
- candidate `worker-protocol.md` §1 becomes the short pre-edit procedure for consuming that already-loaded envelope while still defining the Worker's initial Start HEAD, normal-progress, correction Checkpoint, and mismatch behavior;
- dispatch/handoff schemas remain complete because they are transport artifacts, not explanatory duplication;
- the detailed staleness classifier remains in Worker Protocol because it is Worker-specific behavior.

No Rule ID, state, assignment field, lifecycle, authority boundary, branch/target rule, handoff field, canonical behavior owner, or routing edge changes.

## Frozen identities

- prototype source/current-target snapshot: `af4b2aa86d8a13ca5f45ecf6ed4aadc8f741c386`;
- immutable semantic comparison baseline: `f98e8a242c720931e34aa7c4e8a799090e3d0495` (`v1.2.2`);
- canonical persisted assignment-identity owner: `skill/references/task-contract.md` §8;
- Worker-owned Start/Checkpoint/staleness behavior remains in `skill/references/worker-protocol.md`;
- candidate replacement target: `skill/references/worker-protocol.md` §1 only;
- canonical runtime remains current `main`; this prototype never writes `skill/`.

## Why the canonical-owner reference is safe

`SKILL.md` Worker entry already requires a Worker to load the current Task Contract/work item, `task-contract.md`, and `worker-protocol.md` before editing. The candidate therefore creates no new reference hop or optional dependency: it removes a second prose rendition of persisted assignment fields that are already mandatory active context.

This does **not** mean Worker Protocol becomes a passive consumer. Worker-owned concurrency/staleness behavior remains explicit in the candidate §1 and in the unchanged downstream Worker sections. If the mandatory co-loading rule changes in a future runtime, this representation must be re-evaluated.

## One-to-one semantic ledger

| Source `worker-protocol.md` §1 semantic | Candidate / canonical location | Preservation |
|---|---|---|
| one Worker = one Task Contract + one assigned branch | candidate opening sentence | retained |
| dedicated worktree may be used for isolation | candidate opening sentence | retained |
| worktree path is runtime location, never assignment identity | candidate opening sentence + persisted identity owner `task-contract.md` §8 | retained |
| repository/working directory must be verified | candidate check 1 | retained |
| current worktree/branch attachment and safety must be verified | candidate check 1 | retained |
| Issue / Task Contract revision | persisted assignment envelope in `task-contract.md` §8; candidate check 2 verifies current envelope | single persisted owner retained |
| Assignment ID / Worker identity / active Assignment Status | persisted assignment envelope; candidate check 2 | single persisted owner retained |
| exact Base SHA / Assigned Branch / distinct Integration Target | persisted assignment envelope; candidate check 2 | single persisted owner retained; Worker target-separation behavior remains downstream unchanged |
| inherited ProjectAuthority / CoordinationBaseline / AssuranceLevel / ScopedAuthorization | persisted assignment envelope; candidate check 2 + final no-upgrade guard | single persisted owner + Worker-specific guard retained |
| repository rules / required validation / task risk-release constraints | candidate check 1 | retained locally because these are pre-edit execution checks |
| initial dispatch HEAD equals immutable Start HEAD before first edit | candidate check 3 | Worker Protocol retains canonical `START-HEAD-HISTORICAL` behavior |
| normal authorized same-generation commits may advance beyond Start HEAD | candidate check 3 | Worker Protocol retains canonical `START-HEAD-HISTORICAL` behavior |
| same-generation correction/resume current HEAD equals Master Checkpoint HEAD | candidate check 4 | Worker Protocol retains canonical `CORRECTION-CHECKPOINT` behavior |
| material identity/checkpoint mismatch -> `WorkerStatus.STALE_ASSIGNMENT` | candidate final paragraph + unchanged detailed classifier | Worker Protocol behavior retained |
| never guess through mismatch | candidate final paragraph | retained |
| Worker never upgrades ProjectAuthority / ScopedAuthorization / CoordinationBaseline / AssuranceLevel | candidate final paragraph | retained |
| Worker never broadens assignment because Master unavailable | candidate final paragraph | retained |

## Content intentionally unchanged

The candidate does **not** touch:

- Task Contract §8 persisted assignment table/generation rules;
- Worker dispatch prompt and all field labels;
- Worker execution rules;
- `WorkerStatus.STALE_ASSIGNMENT` classifier and drift table;
- Worker handoff precedence/schema;
- blocker classification;
- Master absorption;
- correction/resume detail;
- direct Worker entry routing in `SKILL.md`;
- machine-relay transport behavior.

These are distinct semantic/transport owners and are not removed merely because some literals repeat.

## Representation rationale

The source §1 paragraph is doing two jobs at once:

1. re-declaring the persisted assignment field ontology already owned by `task-contract.md`;
2. defining Worker-specific pre-edit concurrency/staleness behavior.

Under the #50 framework, persisted identity/schema and ordered Worker verification are different semantic shapes. The assignment envelope stays a table/schema in its canonical persisted owner; Worker Protocol keeps a concise numbered verification procedure because before-edit concurrency behavior is the actual local semantic.

The result is a **single exact assignment envelope owner** plus Worker-owned verification behavior, rather than two normative field-list renditions. The candidate is therefore not "shorter prose for its own sake"; it removes competing identity enumeration without moving Worker-owned behavioral rules.

## Protected evidence surface

At minimum preserve:

- `ASSIGNMENT-IDENTITY` canonical owner in `task-contract.md`;
- `START-HEAD-HISTORICAL`, `CORRECTION-CHECKPOINT`, `STALE-ASSIGNMENT`, and `WORKER-TARGET-SEPARATION` behavior in Worker Protocol;
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

This prototype is eligible for later #38 migration only if mechanical isolation, Rule Map ownership review, semantic ledger review, source-grounded operational analysis, relevant regressions, and maintenance/routing analysis all support it. A live model/API trial is optional corroboration only under the current #35/#37 contract.
