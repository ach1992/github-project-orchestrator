# Pending External-Job Decision-Structure Prototype

Tracking: #56  
Parent: #37  
Methodology: `design/LOSSLESS-RUNTIME-OPTIMIZATION.md`

## Hypothesis

The current already-running pending-job policy in `master-cycle.md` is a genuine branching/precedence rule encoded as one dense paragraph. Re-expressing only that policy as one local condition -> action decision table should reduce branch reconstruction while preserving every existing continuation, failure, stop, namespace, and anti-spin semantic.

This is a Phase B representation prototype only. It does **not** modify canonical `skill/` runtime and does not claim live-model performance improvement.

## Frozen identities

- source/current-target snapshot: `b5c2574f50821de7133119f27f5abf69f10b2624`
- immutable semantic comparison baseline: `f98e8a242c720931e34aa7c4e8a799090e3d0495`
- target owner: `skill/references/master-cycle.md` §9
- candidate fragment: `candidate-pending-job.md`

## Representation fit

`design/LOSSLESS-RUNTIME-OPTIMIZATION.md` distinguishes nuanced judgment from real branching/precedence. This target contains an ordered decision over observable conditions:

1. whether independent useful work remains;
2. whether pending has become the sole dependency;
3. whether bounded synchronous continuation is safe/proportionate;
4. whether a real event/condition resume primitive exists;
5. whether the dependency succeeds or fails;
6. whether autonomous continuation is unavailable/unreasonable/exhausted while pending remains the sole blocker.

That shape is closer to a decision table than to free-form explanatory prose. The candidate therefore uses one principle sentence, one ordered condition/action table, and one explicit anti-spin/namespace guard. It does not introduce a lifecycle state machine.

## One-to-one semantic ledger

| Source semantic | Candidate owner |
|---|---|
| `pending` is dependency state, not failure | opening sentence |
| independent useful work happens before waiting | opening sentence + first row |
| when pending becomes sole dependency, prefer real runtime-supported continuation over yielding control | opening sentence |
| bounded synchronous continuation uses non-tight authoritative rechecks | second row |
| re-read only when transition is plausibly due | second row |
| bound continuation by expected duration, tool/runtime limits, diminishing value | second row |
| suitable event/condition resume primitive may replace synchronous rechecks | third row |
| success immediately resumes the existing workflow without user nudge | fourth row |
| failure stops waiting immediately, is classified, then enters remediation/independent work | fifth row |
| no tight polling / indefinite sleep / fabricated monitoring-resume / manufactured work | final guard |
| `MasterBoundary.BLOCKED` only when pending is sole remaining blocker and autonomous continuation is unavailable/no longer reasonable/exhausted | sixth row |
| BLOCKED report includes exact object/status/reason/resume condition/recoverable state | sixth row |
| `DeliveryState.PENDING` is lifecycle state, not terminal boundary | final guard |
| pending alone never implies `MasterBoundary.NO_READY_WORK` | final guard |

No condition, implication, precedence relation, state token, or boundary is added or removed.

## Scope proof

The deterministic test materializes the candidate from the frozen source snapshot and requires:

- only the exact pending-job fragment in `skill/references/master-cycle.md` changes;
- all text earlier in §9 remains byte-identical;
- `## 10. Requirement changes` and every later byte remain unchanged;
- every other canonical runtime path remains byte-identical;
- the runtime state/boundary token surface remains unchanged;
- `MASTER_STOP(...)` remains byte-identical;
- the materialized Skill passes the normal validator;
- this ledger and source-grounded operational analysis are present.

Word/line counts are diagnostic only and cannot select the candidate by themselves.

## Selection boundary

Select this representation for later #38 migration only if semantic review, deterministic checks, source-grounded walkthroughs, and maintenance/locality analysis all support a net improvement over `KEEP`. A live model/API trial is optional corroboration, not a gate.
