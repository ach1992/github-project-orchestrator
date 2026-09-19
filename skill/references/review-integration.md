# Review and Integration

Master owns acceptance and integration decisions. Worker handoff and self-authorship are never proof of correctness.

## 1. Establish review target

Before review, verify:

- current outcome/acceptance and Issue/Task Contract revision when present;
- PR base + current HEAD, or for recognized repository-normal non-PR path exact Integration Target + exact candidate commit/HEAD;
- dependencies + target-branch state;
- actual target-to-candidate diff + commits;
- current pre-integration CI/checks; merge-queue/merge-group checks become authoritative only after enrollment creates merge-group identity;
- applicable effective repository/platform integration rules for current target when decision-relevant;
- `RiskLevel`/`AssuranceLevel`-required independent approvals/evidence.

Keep the review evidence inside an explicit identity envelope: repository, Integration Target/base, candidate/HEAD, relevant Contract Revision, environment when applicable, and evidence freshness. Candidate/target/contract/effective-change drift invalidates affected approval rather than being normalized away by narrative.

When the repository/platform gives Draft/Ready meaningful review or automation semantics, use it only to signal candidate maturity and avoid knowingly stale acceptance work; otherwise add no ceremony. Draft/Ready remains presentation, adds no `TaskState`, and skips no exact-candidate gate.

### `REVIEW_VALID(envelope)`

Use one validity predicate for whether an existing review can still authorize the exact effective change:

```text
REVIEW_VALID(envelope) =
    RepositoryIdentityIsCurrent(envelope)
    AND IntegrationTargetIsCurrent(envelope)
    AND CandidateIdentityIsCurrent(envelope)
    AND ApplicableContractRevisionIsCurrent(envelope)
    AND EffectiveTargetToCandidateChangeWasReviewed(envelope)
    AND MaterialReviewAssumptionsRemainCurrent(envelope)
```

`ApplicableContractRevisionIsCurrent` is true when no explicit Task Contract applies; it requires an exact current revision only when the review is contract-bound. When `REVIEW_VALID=false`, refresh the affected evidence and re-review the changed effective surface before integration. Current CI/checks, required approvals, unresolved findings, repository rules, and applicable action gates are separate integration-gate inputs; they are not hidden inside review freshness.

For a changed candidate that still requires independent review, use the prior reviewed candidate only as an evidence baseline:

| Delta effect | Required review action |
|---|---|
| exact candidate changed | obtain a fresh verdict bound to the new exact candidate |
| delta leaves prior assumptions/evidence for an unchanged surface valid | inspect the exact prior-candidate-to-current-candidate delta and affected interactions; reuse still-valid analysis/evidence |
| delta changes a shared interface, control flow, dependency, architecture boundary, security/data assumption, acceptance proof, or another dependency of an unchanged surface | widen review to that affected surface |

Prior analysis/evidence may transfer only while its assumptions remain valid; prior verdict/approval never transfers.

### Integration path selection

Choose mechanism from authoritative repository/platform workflow, not from technical write permission:

```text
INTEGRATION PATH
  |
  +-- repository/platform requires PR or Merge Queue? ---> use required PR/queue path
  |
  +-- otherwise, is a non-PR path genuinely recognized?
  |      |
  |      +-- established repository workflow/policy/history supports it
  |      +-- exact reviewed candidate + Integration Target are identifiable
  |      +-- equivalent review/validation/freshness/audit evidence is possible
  |      +-- active CoordinationBaseline/AssuranceLevel controls remain satisfied
  |      +-- no stricter rule requires PR
  |             |
  |             +-- all true ---> recognized non-PR path
  |             +-- any false/unknown
  |                    -> use a required/established controlled path when one is known
  |                    -> otherwise RECONCILE BEFORE INTEGRATION; never invent/bypass a path
  |
  +-- technical direct-write capability alone -----------------> never sufficient
```

| Path | Candidate / target / effective change |
|---|---|
| PR | PR HEAD / PR base / base-to-HEAD diff |
| Recognized non-PR | exact reviewed candidate commit/HEAD / authoritative Integration Target / target-to-candidate diff |

`CoordinationBaseline=LIGHTWEIGHT` uses PR when practical or required. `CoordinationBaseline=STANDARD` normally uses PR-based integration, but do not invent a parallel PR process when an established repository-normal non-PR workflow provides equivalent control and no stricter rule requires PR. `AssuranceLevel=HIGH_ASSURANCE` is additive: retain the coordination path that would otherwise apply and add stronger independent evidence/review as justified. When PR-based, keep PR identity as the review envelope. On a recognized non-PR path, apply the same freshness, optimistic concurrency, validation, review, RiskLevel/AssuranceLevel, and `ApplicableEffects` gates. Direct integration remains Master responsibility; Worker direct target push/merge remains prohibited.

Immediately before each Master-controlled integration step, refresh the review envelope and mutable gate evidence. `REVIEW_VALID=false` or any unexpected required-check/approval/rule/queue-state drift stops that integration action for reconciliation; approval never transfers automatically to a different effective change.

## 2. Review standard

Review only concerns material to the task and repository, as applicable:

| Area | Inspect |
|---|---|
| scope/architecture | acceptance, unintended scope, module boundaries |
| security | validation/escaping, auth/authz, permissions, injection, SSRF/CSRF/path traversal, secrets/sensitive logging |
| data/compatibility | integrity, transactions, concurrency, migration/rollback/backward compatibility, API/schema/error compatibility |
| reliability/tests | idempotency, retries/timeouts/failure behavior, regression/edge tests, false-pass risk |
| performance/operations | material resource/performance impact, observability, operational behavior |
| docs/release | docs/config/release implications |
| supply chain/execution | dependency/lockfile/package-source/build-workflow, provenance and license compatibility when material; inspect untrusted `.github/workflows/*`, package/install scripts, Docker/Make hooks, CI configuration, and deployment scripts before execution |
| hygiene | repository hygiene + generated artifacts |

Do not turn style preference into mandatory scope when formatting/lint policy passes. For untrusted contributor changes, inspect execution/supply-chain surfaces before running them. Use isolated least-privilege validation and do not expose production credentials, repository write tokens beyond necessity, or other sensitive secrets to changed setup/install/build hooks.

| Finding | Gate effect |
|---|---|
| `BLOCKER` | unsafe/incorrect; integration prohibited |
| `REQUIRED` | acceptance/quality requirement must be fixed before integration |
| `OPTIONAL` | useful but not required by contract |

Finding labels are review severity only; a review `BLOCKER` does not become `TaskState.BLOCKED`, `WorkerStatus.BLOCKED`, or `MasterBoundary.BLOCKED` by token equality. Master reconciles the actual dependency/action state.

## 3. Evidence authority and freshness

Apply the `SKILL.md` §3 source-of-truth model to the exact review envelope.

| Question | Current authoritative evidence |
|---|---|
| code/change identity | freshly fetched refs + inspected target-to-candidate diff |
| GitHub workflow/contract | current Issue/PR/Project/milestone objects |
| validation | actual local output and/or current CI/check tied to relevant SHA |
| deployment | current environment/deployment record + artifact/commit identity |
| lasting rules | current recognized repository governance/docs |

Worker/human summaries and old chat are locators only. On conflict, test staleness, SHA/environment mismatch, and scope before deciding a source is wrong.

At review/integration, evaluate the **freshness of evidence already produced** rather than redesigning the validation plan: reuse only evidence whose proof identity and material assumptions remain current, and never transfer a verdict/approval to a changed candidate. Repository-required checks bound to the current candidate remain mandatory. Do not rerun broad validation solely to make otherwise-current evidence look newer.

## 4. CI failures

Classify before code change, then take the action implied by evidence:

| Class | Default response |
|---|---|
| `WORK_REGRESSION` | trace the failure to the active effective change; fix root cause; rerun the narrowest discriminating check, then required broader checks |
| `BASELINE_FAILURE` | prove it also exists on the relevant target/baseline; keep it outside active scope unless it blocks acceptance/integration, creates material safety risk, or belongs to the accepted outcome; continue independent work where possible |
| `FLAKY_TEST` | establish evidence of nondeterminism/transience; use only a bounded rerun justified by that evidence; do not treat eventual green-by-retry as proof that the change is correct |
| `INFRASTRUCTURE_FAILURE` | diagnose runner/service/environment/tooling state; do not mutate product code without evidence that code caused the failure |
| `INTEGRATION_FAILURE` | inspect candidate x current-target interaction, conflict, dependency, and compatibility; reconcile effective change before editing |
| `UNKNOWN` | gather the smallest discriminating evidence before changing code or weakening checks |

Never disable/skip/loosen/rewrite checks merely to get green CI unless the check itself is demonstrably wrong and its correction is separately justified/reviewed. Apply `master-cycle.md` anti-spin rules to retries. After classification, prefer the narrowest check/job that can discriminate the suspected cause before paying for another broad suite when repository policy allows; a new SHA still runs every repository-required gate.

## 5. Conflicts

| Class | Rule |
|---|---|
| `MECHANICAL` | low-risk textual integration, unchanged intent; resolve only when intent is clear |
| `BEHAVIORAL` | both sides change behavior that must be reconciled; return to active outcome/explicit contract/required decision before edit |
| `ARCHITECTURAL` | incompatible design/contract assumptions; return to active outcome/explicit contract/required decision before edit |

Avoid unnecessary rebase/force-push; preserve repository history conventions.

## 6. Integration gate

A substantive change is `TaskState.INTEGRATION_READY` only when all applicable pre-integration conditions hold. Legacy `MERGE_READY` is the compatibility name for this state: on a recognized non-PR path it means ready for that exact Master-owned integration, not permission to bypass repository, CoordinationBaseline, AssuranceLevel, RiskLevel, or ApplicableEffects controls. Merge-queue checks that can exist only after enrollment are platform-controlled post-enrollment conditions, not pre-enrollment evidence.

Before Master-controlled integration, require as applicable:

- acceptance satisfied; explicit contract current;
- `REVIEW_VALID(envelope)` for the exact current target/candidate/contract;
- no unresolved review `BLOCKER`/`REQUIRED`;
- required tests/checks/CI that can and must pass before the Master-controlled integration action pass, or a deliberate exception is authorized and documented in the appropriate place;
- required dependencies are integrated or the stacking model is intentional and safe;
- target compatibility current;
- security/data/migration/operational concerns resolved;
- required docs/config/release notes complete;
- no unexplained scope expansion;
- effective target rules respected: branch protection/rulesets, required checks/deployments, merge queue, allowed method/path; technical bypass capability alone does not authorize bypass;
- RiskLevel/AssuranceLevel-required independent review + human approvals complete;
- every `ApplicableEffects` obligation for the exact integration action is satisfied under `authority-gates.md`.

Immediately before next Master-controlled integration action, re-read candidate/target identity, mergeability/equivalent target-update preconditions, effective rules, required pre-action checks/approvals, and any Task Contract revision that could invalidate decision. Unexpected drift -> reconcile; never overwrite/integrate through it.

### Merge Queue

| Stage | Rule |
|---|---|
| Before enrollment | Use normal queue path. If queue can later cause a consequential effect without another interceptable authorization decision, resolve **every** canonical gate that must precede that effect before enrollment. This includes required `INTEGRATION` approval/ScopedAuthorization and, when deterministic, `PRODUCTION`; `DESTRUCTIVE_OR_IRREVERSIBLE` or `EXTERNAL_COMMITMENT` effects retain their current-human approval/decision requirement under the default matrix and are never waived merely by integration/production authorization. Scope any permitted authorization to queue-mediated integration of the reviewed candidate into the identified target subject to required queue checks. Never enroll while a required gate would become non-interceptable, and never require queue evidence that cannot exist yet. |
| After enrollment | Verify created merge-group identity + required queue checks for current candidate/target. PR-head evidence does not substitute when platform evaluates a distinct merge-group commit. |
| Complete | Mark `TaskState.INTEGRATED` only after platform reports target update and current target identity confirms intended change reached it. |
| Regroup / target drift | For each new merge-group identity, require the current queue checks that apply to that identity. Routine regroup that stays within the reviewed/authorized effective-change and risk envelope needs no new human gate. If regroup or target movement—whether operationally normal for the queue or not—materially changes assessed action, target, risk, effective change, or review/approval assumptions, reconcile and re-review/re-apply applicable gates before integration when an intercept remains; never treat the word `normal` as proof that material drift is already authorized. |

Apply `authority-gates.md`: high/critical `ApplicableEffects.INTEGRATION` needs defined approval unless the exact action is validly authorized with current evidence. An integration action that deterministically deploys production has both `INTEGRATION` and `PRODUCTION`; both independent obligations must be satisfied.

## 7. Self-authored work

Self-authored work still receives the same current-diff/acceptance review and finding severity as delegated work. Self-review is not independent review. When RiskLevel, policy, or AssuranceLevel requires separation, load [independent-review.md](independent-review.md) and obtain a separate reviewer context/person/tool; otherwise do not add independent-review ceremony. Master retains integration ownership.

## 8. Post-integration

After integration, in order:

1. verify the intended candidate/change actually reached the authoritative Integration Target;
2. verify target CI/checks when applicable/currently available;
3. mark engineering work `TaskState.INTEGRATED`; update/close Issue/parent/milestone/Project/dependencies/active risk only according to whether the active outcome or explicit contract also has `DeliveryRequirement=DELIVERY_REQUIRED`;
4. capture only actionable follow-up work;
5. update durable docs/ADR only when a lasting rule/decision changed;
6. clean branch/worktree only when no useful uncommitted/unpushed work can be lost;
7. update release readiness when delivery is affected.

`TaskState.INTEGRATED` never implies `DeliveryState.DELIVERED`; delivery is proven separately for the explicit DeliveryTarget. Do not copy integrated-change history into manager documents.
