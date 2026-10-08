# Release, Delivery, and Operations

Load when accepted work requires release/deployment, migration, rollback/roll-forward, incident/hotfix handling, or delivery verification.

## 1. Integration is not delivery

A merge/target update proves only integration. When the accepted outcome requires delivery, verify the intended artifact/commit/config actually reached the named environment and that required post-deploy acceptance evidence is satisfied.

Transport success, a green deploy job, or a release record is not enough when artifact identity or environment state is missing/contradictory.

Record delivery state in the natural deployment/release system when possible rather than duplicating it in a manager document.

## 2. Before production

Use [authority-gates.md](authority-gates.md) for the exact production action and any simultaneous integration/destructive/external effects.

Before a production mutation, establish as applicable:

- exact candidate/artifact/config identity;
- exact target/environment;
- current required review/CI/release approvals;
- rollout and verification method;
- rollback or roll-forward path;
- migration/compatibility ordering;
- operational health evidence needed after the action.

Do safe preparation before an approval gate when it reduces uncertainty without crossing the gate.

## 3. Release candidate stability

Do not repeatedly spend broad acceptance/release validation on a candidate that is knowingly changing unless policy or risk requires the feedback earlier.

Once the release candidate is stable, run the required exact-candidate gates. If later changes occur, rerun only evidence they invalidate plus every gate that policy requires for the new identity.

## 4. Migration and stateful changes

For material schema/data/state transitions, reason about compatibility window, ordering, partial failure, concurrency/lock effects, backup vs actual recovery capability, rollback feasibility, and roll-forward when rollback is unsafe.

Rehearse or stage when risk justifies it. Never assume reversibility merely because a backup exists.

A migration that is destructive/irreversible or materially changes access boundaries keeps its separate human gate even when the deployment itself was pre-authorized.

## 5. Delivery proof

After deployment/release, verify the smallest authoritative evidence that proves the accepted endpoint, such as:

- environment reports the intended immutable artifact/commit/config identity;
- required health/readiness checks pass;
- migration/version state matches expectation;
- required smoke/acceptance behavior is observed;
- no blocking operational signal contradicts success.

If evidence is unavailable or contradictory, report delivery as unproven/failed rather than declaring project completion.

## 6. Incident and hotfix

During an active incident, prioritize containment and restoration of safe service over ordinary backlog/ceremony. Preserve enough evidence for root-cause work without delaying urgent containment.

Apply the same authority boundaries: diagnosis/read-only work proceeds; production/destructive actions still need their applicable authorization unless current incident policy already grants it.

After stabilization, reconcile temporary changes into normal source/review/release state and capture only future-useful remediation.
