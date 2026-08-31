# Source-Grounded Operational Analysis

Experiment: `pending-job-decision-structure-v1`  
Issue: #56

This analysis compares decisions, not wording. Each scenario is evaluated against the frozen source semantics in `master-cycle.md` and the candidate decision structure. No live model/API claim is made.

## Scenario 1 — Independent work exists while CI is pending

State:
- required CI is healthy/pending;
- candidate identity is frozen;
- independent effective-diff review is executable without the CI result.

Source decision:
- pending is not failure;
- perform the independent review first;
- do not yield control merely because CI is pending.

Candidate decision:
- opening rule classifies pending as dependency state, not failure;
- first table row directs independent useful work before waiting.

Result: same decision and precedence. The candidate localizes the condition/action pair instead of requiring the reader to extract it from the paragraph.

Protected anchors: `AQ`, `AW`, `CN`.

## Scenario 2 — Pending becomes the sole dependency; short bounded wait is reasonable

State:
- all independent work is complete;
- CI is still healthy/pending within normal expected duration;
- runtime supports synchronous authoritative status reads;
- a transition is plausibly due soon.

Source decision:
- prefer runtime-supported continuation over yielding control;
- perform bounded non-tight authoritative rechecks;
- re-read only when transition is plausibly due;
- bound by expected duration, runtime/tool limits, and diminishing value.

Candidate decision:
- opening rule preserves the preference for runtime-supported continuation;
- second row carries all four synchronous-wait constraints together.

Result: same decision. Related constraints are more local and no new polling cadence/state is introduced.

Protected anchor: `AQ`.

## Scenario 3 — A real event/condition resume primitive exists

State:
- pending is the sole dependency;
- the runtime provides a genuine suitable event/condition resume mechanism.

Source decision:
- the real primitive is an allowed/preferred continuation path;
- do not fabricate background monitoring.

Candidate decision:
- third row uses the real primitive;
- final guard separately forbids fabricated monitoring/resume.

Result: same decision and safety boundary.

Protected anchor: `AQ`.

## Scenario 4 — Dependency resolves successfully

State:
- a bounded authoritative recheck observes CI success.

Source decision:
- immediately continue the existing workflow;
- do not require the user to send another message.

Candidate decision:
- success row states the same continuation and no-user-nudge behavior.

Result: same decision.

Protected anchors: `AQ`, `AW`.

## Scenario 5 — Dependency transitions to failure

State:
- an authoritative recheck observes failure.

Source decision:
- stop waiting immediately;
- classify the failure;
- continue the applicable remediation or independent-work path.

Candidate decision:
- failure row preserves this exact ordered response.

Result: same decision. The candidate does not redefine failure classes or retry policy.

Protected anchors: `AQ`, `CL`.

## Scenario 6 — Long or unsupported wait becomes the sole blocker

State:
- pending is still the sole remaining blocker;
- bounded autonomous continuation is unavailable, no longer reasonable, or exhausted.

Source decision:
- `MasterBoundary.BLOCKED` is now permitted;
- report exact external object, status, why autonomous continuation cannot safely continue, exact resume condition, recoverable state.

Candidate decision:
- final table row preserves the same conjunctive gate and report payload.

Result: same decision. The candidate does not allow BLOCKED while independent work exists or merely because one status read is pending.

Protected anchors: `AQ`, `CN`.

## Scenario 7 — DeliveryState.PENDING namespace separation

State:
- deployment completed;
- required soak/acceptance is not yet observable;
- `DeliveryState.PENDING` is current lifecycle state.

Source decision:
- DeliveryState.PENDING is not itself a terminal Master boundary;
- use the normal continuation/BLOCKED rules only when their independent conditions hold.

Candidate decision:
- final guard explicitly preserves lifecycle-vs-boundary separation.

Result: same namespace semantics; no new lifecycle transition is invented.

Protected anchor: `CO`.

## Scenario 8 — Pending must not become NO_READY_WORK

State:
- an already-running required external dependency is pending;
- there is no other ready implementation work.

Source decision:
- pending does not become `MasterBoundary.NO_READY_WORK`;
- use bounded continuation when appropriate or BLOCKED only under its specific conditions.

Candidate decision:
- final guard preserves the non-implication directly.

Result: same decision.

Protected anchors: `AQ`, `CN`.

## Maintenance and routing assessment

No new file is needed at runtime, no router edge changes, and no second owner is introduced. The decision table remains in the existing canonical owner (`master-cycle.md` §9). The candidate is therefore a representation change only.

Potential benefit:
- condition/action pairs become explicit and adjacent;
- success, failure, continued waiting, and terminal BLOCKED paths are visually separable;
- the namespace guards remain outside the table rather than being hidden as pseudo-branches.

Potential cost:
- table cells can become harder to scan if they grow into prose;
- future changes must preserve row precedence and the conjunctive BLOCKED condition.

Assessment: the current candidate stays compact enough that the table exposes real branching instead of merely rewrapping prose. This supports selection if deterministic/equivalence review remains green. `KEEP` remains valid if later review finds lost nuance or maintenance cost.
