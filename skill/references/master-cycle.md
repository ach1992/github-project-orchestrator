# Master Cycle

Use this reference for Master decisions that affect sequencing, provenance, pending work, recovery, or completion.

## 1. Recover only what changed

Do not restart project discovery on every turn, tool batch, commit, PR, or Worker handoff. Retain verified repository identity, accepted outcome, authority, and stable constraints until evidence invalidates them.

On first ownership, use [governance.md](governance.md) to locate the project-defining specification, resolve/reuse or safely create the intended repository, reconcile repository reality, and establish only the structure needed for safe execution/recovery.

For later work, inspect only evidence that can affect the next decision: current work/acceptance, relevant code and refs, dependencies, blockers, required checks, release state, and material risks. Expand discovery only when evidence exposes a broader dependency or ambiguity.

### PR provenance

Before adopting a PR, dispatching independent review, or merging, establish or reuse provenance for its current HEAD. Check creator, source repository/branch, authors and committers of PR-introduced commits, available authenticated push actors, and fit with authorized work. Git metadata and green CI alone cannot establish origin. If provenance conflicts or remains unexplained, hold the PR and alert Owner. A merge approval request identifies origin, material changes and risks, and exact HEAD.

## 2. Choose work by finished value

Prefer in this order when applicable:

1. contain active correctness/security/data/production incidents;
2. review/integrate completed work that unlocks value;
3. unblock the critical path;
4. execute the highest-value ready outcome slice;
5. improve the engineering system only when a demonstrated bottleneck is materially slowing the remaining outcome.

Priority labels are inputs, not substitutes for current dependency/release reality. Apply [governance.md](governance.md) before treating an Owner-parked idea as executable. Do not create work merely to keep a queue full.

Use **minimum meaningful slices**, not minimum possible slices. Keep related implementation together when acceptance, ownership, dependency, risk, rollback, review, and release boundaries align. Split only where one of those boundaries materially improves execution or reviewability. For foundation-heavy work, prioritize the earliest safe, authorized, representative non-production end-to-end consumer/operator check when feasible; mocks alone do not prove integration.

Classify discovered improvements before expanding the work package. Apply [control decisions](engineering-quality.md#control-decisions) when a proposed improvement adds a restriction, prerequisite, or recovery layer. Correct evidenced acceptance/material defects through normal gates; prefer better in-scope implementation when benefit exceeds cost/risk. Propose worthwhile adjacent work without making it a completion condition, and ignore cosmetic, speculative, duplicate, or low-value additions.

## 3. Delegation

Self-execute when delegation would cost as much as it saves. Delegate only a bounded workstream whose specialization or genuine parallelism is likely to reduce end-to-end completion time after dispatch, review, and reconciliation overhead.

Parallel work must not compete on the same unstable surface or knowingly create repeated stale review/CI evidence. If integration of one candidate would invalidate another candidate's required target-bound evidence, keep implementation parallel when safe but serialize only the affected final acceptance/integration path.

Master always retains priority, acceptance, contract changes, integration, release, and risk acceptance.

## 4. Development and validation economics

During implementation, trace the affected path and batch related edits. Check earlier when delay would make failures hard to isolate or a dependent, high-consequence change would be costly to undo. If a check fails, classify the cause, repair within scope, and rerun the discriminating check. Follow through on required validation until acceptance is satisfied or a real gate blocks progress.

## 5. Pending work and failures

### Pending jobs

Pending checks, deployments, and external jobs block only dependent work. Do useful independent work first. Reuse the run identity while it progresses. On drift, a stall, or before relying on a terminal result, confirm the target's current revision, required checks, and run attempt. Reuse an observation that already proves this binding.

| Observation | Next action |
|---|---|
| Pending | Keep the task active with a supported watch, confirmed event-based resume, or spaced authoritative reads. If an interval expires or a read still shows pending, wait and check again while progress is plausible. Pace reads by expected duration, provider hints, and runtime limits. |
| Superseded or finished | Follow the replacement run when superseded. On current success take the next authorized action. On current failure [diagnose or repair within scope](review-integration.md#3-validation-and-ci). Respect applicable review, integration, and release approvals. |
| Stalled, missing, or gated | Diagnose the missing trigger, stall, or approval. Hand back only when human action is necessary or [available alternatives](authority-gates.md#capability-selection) leave no reasonable continuation. Give the job identity, last state, blocker, and exact resume condition. Claim background follow-up only after runtime confirmation. |

### After a failure

After a failure, do not repeat the same action with materially identical inputs just to keep moving. Capture useful evidence and check whether state changed. For tool rejections or `Safety Check` responses, follow [rejected execution](authority-gates.md#rejected-execution-and-safety-checks). Otherwise narrow/reproduce, inspect logs/diff, repair the environment, use another authorized route, or switch to independent work.

Repeated broad validation/review-remediation cycles with the same controlling cause are a signal to fix the work-package, environment, validation ownership, or review strategy—not to start another identical cycle.

Report substantive outcomes, Owner decisions, exact external blockers, required gates and unverified acceptance/risks with their source identity. Keep required progress updates useful and concise; do not narrate every tool/test or repeat status while useful work remains.

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
- an approval or owner-level decision is required before the next useful dependent action;
- an external dependency/precondition blocks all useful progress;
- required capability remains unavailable after [authority-gates.md](authority-gates.md) rules out reasonable equivalents;
- a mutation outcome remains unsafe to resolve;
- new risk requires human containment/decision before further useful work.

A local blocker does not stop unrelated independent work unless delay materially increases risk. On explicit user stop, stop new consequential mutation immediately; do not cleanup, sync, commit, push, or persist solely as end-of-cycle ceremony unless requested.

Before a normal terminal handoff, persist only unresolved future-useful state that is not already recoverable from Git/GitHub/CI/release systems. Do not create a manager-memory archive merely because the chat may end.

## 9. Resource lifecycle

Apply this to any temporary resource, regardless of provider or resource type. Recover/reuse through [continuity.md](continuity.md) before provisioning. Know its purpose, owning task/principal where determinable, dependencies and retention need; record only information that safe continuation cannot recover better elsewhere.

At a real purpose/completion/validation/integration/handoff boundary, reconcile only the task's relevant resources:

1. Verify identity/ownership, actual consumers, in-flight work and unique uncommitted/unpushed state. Check pending review, tests, deployment, diagnostic/audit evidence, rollback and other-project dependencies.
2. Preserve needed unique state and transfer minimal valuable evidence to its natural durable GitHub owner where appropriate. Completion or merge alone does not prove a resource is no longer needed.
3. Release/stop/remove only resources proved task-owned, no longer needed and safely disposable under [authority-gates.md](authority-gates.md). Never destroy dirty/shared state, force-delete or stop another actor's service for tidiness.
4. Verify the effect before claiming cleanup succeeded. If ownership, safety, outcome or authority is uncertain, retain the resource and report its exact reason/decision at the boundary.

Use bounded cleanup within ordinary work, without global scans, a runtime database, recurring audits or a separate cleanup project. Explicit user stop takes precedence over optional cleanup.
