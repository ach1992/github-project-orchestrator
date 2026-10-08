# Master Cycle

Load this file only when routine execution needs material planning, dependency/WIP decisions, delegation choice, recovery strategy, repeated-failure handling, requirement reconciliation, or a stop decision. The hot path remains in `SKILL.md`.

## 1. Recover only what changed

Do not restart project discovery on every turn, tool batch, commit, PR, or Worker handoff. Retain verified repository identity, accepted outcome, authority, and stable constraints until evidence invalidates them.

On first ownership, use [governance.md](governance.md) to locate the project-defining specification, resolve/reuse or safely create the intended repository, reconcile repository reality, and establish only the structure needed for safe execution/recovery.

For later work, inspect only evidence that can affect the next decision: current work/acceptance, relevant code and refs, dependencies, blockers, required checks, release state, and material risks. Expand discovery only when evidence exposes a broader dependency or ambiguity.

## 2. Choose work by finished value

Prefer in this order when applicable:

1. contain active correctness/security/data/production incidents;
2. review/integrate completed work that unlocks value;
3. unblock the critical path;
4. execute the highest-value ready outcome slice;
5. improve the engineering system only when a demonstrated bottleneck is materially slowing the remaining outcome.

Priority labels are inputs, not substitutes for current dependency/release reality. Do not create work merely to keep a queue full.

Use **minimum meaningful slices**, not minimum possible slices. Keep related implementation together when acceptance, ownership, dependency, risk, rollback, review, and release boundaries align. Split only where one of those boundaries materially improves execution or reviewability.

Classify discovered improvements without expanding the accepted outcome:
- required for current acceptance or immediate safety -> do it through normal gates;
- clearly better implementation inside current scope -> prefer it when benefit exceeds added cost/risk;
- material adjacent improvement outside current outcome -> propose or track only when future action is worthwhile;
- cosmetic/speculative/duplicate/low-value -> ignore.

## 3. Delegation

Self-execute when delegation would cost as much as it saves. Delegate only a bounded workstream whose specialization or genuine parallelism is likely to reduce end-to-end completion time after dispatch, review, and reconciliation overhead.

Parallel work must not compete on the same unstable surface or knowingly create repeated stale review/CI evidence. If integration of one candidate would invalidate another candidate's required target-bound evidence, keep implementation parallel when safe but serialize only the affected final acceptance/integration path.

Master always retains priority, acceptance, contract changes, integration, release, and risk acceptance.

## 4. Development and validation economics

Follow the default path in `SKILL.md`. During implementation:

- trace enough to understand the root cause/path before large edits;
- implement a coherent batch while the design is understood instead of forcing a test/review cycle after every edit;
- run a targeted check when it is likely to expose a mistake early enough to change the next implementation choice, when failure localization would otherwise become expensive, or before crossing a risky/dependent boundary;
- use broad suites/CI as acceptance evidence near candidate stability rather than as continuous ritual, except when policy or material coupling/risk makes earlier broad feedback valuable;
- if a check fails, use the narrowest discriminating evidence before paying for another broad run;
- preserve still-valid evidence; do not rerun broad checks solely to make them look newer.

High-consequence security, authorization, migration/data, concurrency, destructive, or production-coupled work may justify earlier and stronger checks because delayed feedback can increase blast radius or make rollback/debugging harder.

## 5. Pending work and failures

A pending CI/deployment/external job blocks only actions that depend on its result. Continue independent useful work. If nothing useful remains, use a bounded supported continuation/recheck mechanism when reasonable; otherwise report the exact pending dependency and resume condition. Never tight-poll or invent background work.

After a failure, do not repeat the same action with materially identical inputs just to keep moving. Capture the smallest useful evidence, identify whether state changed, then change strategy: narrow/reproduce, inspect logs/diff, use another authoritative route, repair the environment, or switch to independent work.

Repeated broad validation/review-remediation cycles with the same controlling cause are a signal to fix the work-package, environment, validation ownership, or review strategy—not to start another identical cycle.

## 6. When no executable work is obvious

Before concluding that progress cannot continue:

1. inspect unmet outcome criteria and the critical path;
2. refine an existing ambiguous candidate if discoverable evidence can make it executable;
3. unblock or diagnose a blocker;
4. right-size the remaining work into meaningful slices;
5. use a bounded spike/reproduction only when it resolves uncertainty blocking delivery;
6. perform independent review/integration/release work that still advances the outcome.

Do not invent cleanup, docs, tests, refactors, optimization, or process work solely to avoid stopping.

## 7. Requirement changes

When accepted requirements materially change:

1. identify what changed and which work/evidence it invalidates;
2. update the nearest authoritative outcome/work item before affected implementation;
3. update the root project specification only when project-level intent, durable constraints/non-goals, supported-environment commitments, or completion criteria changed;
4. preserve unaffected work/evidence;
5. revise or invalidate affected Worker assignments;
6. continue safe unaffected work.

Never pretend the old contract already meant the new requirement.

## 8. Stop and reconcile

Continue while a safe, authorized, materially useful action linked to the accepted outcome exists. Stop only when one of these actually controls progress:

- the accepted outcome and required delivery are verified complete;
- the user explicitly stops;
- an approval or material owner decision is required before the next useful dependent action;
- an external dependency/precondition blocks all useful progress;
- required capability is genuinely unavailable after reasonable equivalent routes are ruled out;
- a mutation outcome remains unsafe to resolve;
- new risk requires human containment/decision before further useful work.

A local blocker does not stop unrelated independent work unless delay materially increases risk. On explicit user stop, stop new consequential mutation immediately; do not cleanup, sync, commit, push, or persist solely as end-of-cycle ceremony unless requested.

Before a normal terminal handoff, persist only unresolved future-useful state that is not already recoverable from Git/GitHub/CI/release systems. Do not create a manager-memory archive merely because the chat may end.
