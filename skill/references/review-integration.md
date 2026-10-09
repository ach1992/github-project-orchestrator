# Review and Integration

Master owns acceptance and integration. A Worker handoff, green CI, or self-authorship is not proof that the current effective change is correct.

## 1. Review the exact candidate

Before review/integration, establish the current envelope:

- repository;
- Integration Target/base;
- exact candidate/HEAD;
- current acceptance/contract when one exists;
- effective target-to-candidate diff;
- required checks/approvals/policy;
- environment when it materially affects evidence.

A review applies only while the effective change and material assumptions it reviewed remain current. If the candidate or target changes, inspect the exact delta and refresh only affected analysis/evidence. Prior reasoning may remain useful; prior approval/verdict never automatically transfers to a different candidate.

Use Draft/Ready only when the repository/platform gives it useful semantics. Do not spend independent review or broad acceptance CI repeatedly on a candidate known to be changing unless that feedback is needed now or policy requires it.

## 2. Review standard

Inspect only concerns material to the change: acceptance/scope, architecture fit, correctness, security, data/compatibility, reliability, tests, performance/operations, release/config implications, supply-chain/execution surfaces, and unintended artifacts.

Classify findings simply:

- `BLOCKER`: unsafe or fundamentally incorrect; cannot integrate.
- `REQUIRED`: acceptance/quality defect that must be fixed.
- `OPTIONAL`: useful but not required for current completion.

Style preference is not a required finding when repository policy is satisfied.

Before executing untrusted contributor changes, inspect changed workflows/install/build/deploy hooks and use least privilege.

## 3. Validation and CI

Evidence is valid only for the code/config/environment/requirement it actually proves.

During authoring, follow the validation economics in `SKILL.md`: targeted checks first when informative; broad required gates on a stable candidate. Do not rerun broad validation solely because time passed or an unrelated identity moved.

When later changes occur:

- rerun the narrow check that discriminates the changed behavior;
- rerun any broader evidence whose assumptions/surface were invalidated;
- always satisfy repository-required exact-candidate checks at the point policy requires them.

Classify CI failures before changing product code:

| Class | Response |
|---|---|
| regression from current work | trace root cause, fix, run narrow discriminating check, then invalidated/required broader gates |
| baseline failure | prove it exists on the relevant target; keep out of scope unless it blocks current acceptance/integration or creates immediate material risk |
| flaky/transient | establish evidence before a bounded rerun; eventual green-by-retry is not proof |
| infrastructure/environment | diagnose the environment; do not change product code without causal evidence |
| integration/target interaction | inspect current target x candidate interaction |
| unknown | gather the smallest discriminating evidence first |

Never disable or loosen a check merely to get green.

## 4. Conflicts

Resolve mechanical conflicts only when intent is clear. Behavioral/architectural conflicts require reconciliation against current acceptance and authoritative design before editing.

Avoid unnecessary rebases/force-pushes that destroy useful history or stale evidence.

## 5. Integration gate

Use the repository/platform's normal controlled integration path. Technical permission to push directly is not enough to bypass a required PR, queue, protection rule, approval, or policy.

Before Master-controlled integration require, as applicable:

- acceptance satisfied and current;
- exact current effective diff reviewed;
- no unresolved `BLOCKER`/`REQUIRED`;
- required tests/CI/approvals complete for the current candidate;
- dependencies/target compatibility current;
- material security/data/migration/operations concerns resolved;
- repository/platform rules satisfied;
- every action-level authorization from [authority-gates.md](authority-gates.md) satisfied.

Immediately before integration, refresh mutable candidate/target/rule/approval state that could invalidate the action. Unexpected drift means reconcile; never integrate through stale assumptions.

If a merge queue creates a distinct merge-group commit, required queue evidence belongs to that identity. Routine regrouping needs no new human decision unless it materially changes the reviewed/authorized effective change, target, risk, or rollout assumptions.

## 6. Self-authored and independent review

Self-authored work still gets an exact-diff reviewer mindset. When the current envelope requires independent review, load [independent-review.md](independent-review.md); self-review never satisfies that separation.

Prefer one independent review after candidate stabilization. If remediation changes the candidate, re-review the exact delta plus any affected interactions; do not restart analysis of unchanged surfaces without reason.

## 7. After integration

Verify that the intended change actually reached the Integration Target. Then reconcile the owning Issue/work item against its real acceptance criteria and required post-integration evidence.

Do not close work merely because a PR merged. If delivery is required, completion waits for [release.md](release.md) delivery proof. Record only actionable follow-up that is outside current completion, update durable docs only when a lasting rule/decision changed, and clean temporary branches/worktrees only when no useful work can be lost.
