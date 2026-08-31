# Source-Grounded Operational Analysis

Experiment: `write-unknown-canonical-algorithm-v1`  
Issue: #58

This analysis compares decisions and safety guards, not wording. No live model/API claim is made.

## Scenario 1 — Equivalent write is present after ambiguous transport

State:
- issue creation transport result is ambiguous;
- authoritative re-read is decision-scoped and finds the equivalent issue.

Source decision:
- mark the attempted mutation UNKNOWN while reconciling;
- do not retry;
- verify the present write, mark known, continue.

Candidate decision:
- steps 1–3 preserve the same sequence.

Result: same decision, with the branch expressed once.

Protected anchor: `C`.

## Scenario 2 — Authoritative re-read proves absence and retry is safe

State:
- mutation result ambiguous;
- complete decision-scoped re-read proves absence;
- retry is idempotent or protected by stable correlation/deduplication.

Source decision:
- one retry may occur;
- no second blind retry is permitted.

Candidate decision:
- step 4 states proof-of-absence, safe-retry guard, and at-most-once bound together.

Result: same decision.

Protected anchors: `C`, `DD`.

## Scenario 3 — Discovery is incomplete/truncated

State:
- ambiguous write;
- lookup does not establish decision-scoped absence because results are incomplete/truncated.

Source decision:
- incomplete is not absence;
- no retry;
- freeze dependent mutation and continue independent safe work.

Candidate decision:
- step 5 owns all three consequences explicitly.

Result: same decision; candidate makes the most safety-critical forbidden inference local to its branch.

Protected anchors: `C`, `AU`, `DD`.

## Scenario 4 — Proven absence but retry is unsafe

State:
- authoritative re-read proves absence;
- mutation is not safely idempotent and lacks stable correlation/deduplication protection.

Source decision:
- do not retry merely because absence is proven;
- freeze dependent mutation and continue independent safe work.

Candidate decision:
- step 4 preserves the two-part gate: absence is necessary but not sufficient; retry safety must also hold.

Result: same decision.

Protected anchor: `DD`.

## Scenario 5 — One safe retry is still ambiguous

State:
- absence was proven;
- one safe correlated retry was attempted;
- retry result remains ambiguous.

Source decision:
- keep mutation UNKNOWN;
- no further retry;
- continue independent safe work;
- surface WRITE_OUTCOME_UNKNOWN only if it becomes sole/project-wide controlling blocker.

Candidate decision:
- step 6 preserves all four consequences.

Result: same decision.

Protected anchor: `DD`.

## Scenario 6 — Local UNKNOWN while independent work exists

State:
- one non-idempotent issue comment remains UNKNOWN;
- another accepted reversible task is executable.

Source decision:
- freeze only dependent mutation;
- continue independent work;
- do not propagate local WriteState token into a Master stop.

Candidate decision:
- steps 4–6 repeatedly preserve independent safe continuation and step 6 keeps the terminal boundary conditional.

Result: same namespace/propagation semantics.

Protected anchor: `DD`.

## Scenario 7 — Unknown becomes the sole/project-wide blocker

State:
- bounded recovery exhausted;
- no safe retry remains;
- outcome still ambiguous;
- independent useful work exhausted and the unresolved write controls completion.

Source decision:
- now surface `MasterBoundary.WRITE_OUTCOME_UNKNOWN` with exact resume evidence under normal boundary handling.

Candidate decision:
- step 6 permits the boundary only under the same sole/project-wide condition.

Result: same decision.

Protected anchor: `DD`.

## Maintenance/locality assessment

The current source uses two co-located representations for one algorithm: a compressed symbolic expression and a detailed numbered list. The symbolic version owns no unique semantic condition and requires the maintainer/model to reconcile its shorthand with the detailed safety guards below it.

The candidate keeps one canonical algorithm and makes branch discriminators explicit where they are applied. This reduces duplicate ownership without adding a file, router hop, state, schema, or abstraction.

Potential cost:
- the single algorithm is slightly more explicit than the old five-step list because `incomplete/unknown` receives its own step;
- removing the symbolic line removes a fast visual summary.

Assessment: the summary's retrieval benefit is outweighed by duplicate representation and shorthand ambiguity because §6 is already short and trigger-loaded only for ambiguous writes. The candidate keeps scanability through numbered steps and bold branch labels. This supports SELECT if deterministic isolation/equivalence remains green.
