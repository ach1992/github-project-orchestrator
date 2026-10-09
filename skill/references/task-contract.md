# Task Contract

Use an explicit Task Contract only when it materially improves coordination, delegation, risk control, or recovery. Routine Master-only work can use the accepted request plus current repository evidence; do not create an Issue or READY artifact merely because code changes behavior.

## When a contract is useful

Persist a contract for Worker assignments and when multi-actor or cross-session coordination, dependencies/decisions another actor or future session must know, high-consequence work, or repository policy needs durable identity. Otherwise keep the work implicit or transient. Reuse an existing suitable Issue/work item rather than creating a parallel contract.

Keep one contract for a cohesive outcome across partial commits or PRs. Do not close and recreate it at mechanical implementation seams.

## Compact contract

Include only decision-relevant fields:

```markdown
Contract Revision: <positive integer when persisted/delegated>

## Goal
<observable result>

## Scope
In: <material boundaries>
Out: <material exclusions>

## Acceptance
- [ ] <observable criterion>

## Validation
- <required evidence; separate targeted development checks from final required gates>

## Dependencies / Constraints
- <material items or none>

## Risk / Delivery
- <material risk, rollback, migration, release, or delivery requirements>
```

Do not copy repository-wide rules into every contract. Link the authoritative source when needed. Acceptance must be observable or verifiable rather than vague.

## Validation planning

Define minimum sufficient evidence, not every possible check.

- Bug: reproduce when practical, add or use a regression check, then run relevant required gates.
- Feature: prove changed behavior; add integration/end-to-end evidence when that boundary matters.
- Refactor: prove behavior is preserved with relevant tests/static checks.
- Infra/config: use syntax, plan, dry-run, staging, or equivalent evidence proportional to impact.
- High-consequence data, authorization, or migration work: include the relevant failure, compatibility, recovery, or rollback evidence.

During coding, use targeted checks when their result can influence the next step. Broad repository-required validation belongs on a sufficiently stable exact candidate unless policy or risk requires it earlier. Reuse evidence while the code/config/environment/requirement it proves remains materially unchanged. Never weaken checks to manufacture a pass.

## Contract revision

Increment the revision only when goal, scope, acceptance, required validation, material dependency, risk, or delivery expectation changes. Wording cleanup does not need a new revision.

When a revision invalidates a Worker assignment, stop that generation and issue a new assignment or correction through [worker-protocol.md](worker-protocol.md).

## Worker assignment identity

Before dispatch, persist enough identity for a replacement Master to reconstruct the assignment without chat:

- `Assignment ID`: unique current generation;
- exact `Repository` and assigned `Worker`;
- work item + `Contract Revision`;
- exact immutable `Base SHA` the assignment was framed against;
- `Assigned Branch`;
- immutable `Start HEAD` for a new generation, or exact `Checkpoint HEAD` for correction/resume;
- `Integration Target`;
- any exact action authorization or special release constraint not already clear from the contract.

The assigned branch must differ from the Integration Target. `Base SHA` remains the historical integration/stacking basis; `Start HEAD` is the immutable generation start and normally equals Base SHA unless intentional stacking/divergence is part of the assignment. Worktree paths are runtime locations, not assignment identity. Normal Worker commits may advance beyond `Start HEAD`; staleness means an external change invalidated assignment assumptions, not that the Worker made progress.

## Ready to execute

Before Worker dispatch or other coordination-heavy implementation, ensure scope is implementable, acceptance is observable, required validation is known, dependencies are satisfied or intentionally sequenced, and owner-level decisions are resolved.

This is a decision condition, not documentation ceremony. Discover safely knowable facts yourself instead of asking the user, and do not create an extra artifact when the facts are already authoritative elsewhere.
