# Lossless Runtime Decision-Representation Optimization

Tracking: #35  
Baseline task: #36  
Prototype task: #37  
Migration task: #38  
Final proof/integration task: #39

## 1. Purpose

Optimize **how** the runtime expresses the existing orchestration semantics so an LLM can select and execute the correct path with less inference, reconstruction, irrelevant context traversal, and activation error.

This program is intentionally different from adding, removing, or changing orchestration policy. The candidate runtime is acceptable only when the current semantic contract is preserved losslessly and comparable **actual model/runtime A/B evidence** shows a material execution benefit.

The optimization target is:

```text
Semantic behavior:        IDENTICAL for protected baseline requirements
Safety/correctness:       >= baseline
Decision quality:         >= baseline on comparable actual model/runtime trials
Practical friction:       < baseline on at least one material observable paired metric
Maintenance/routing cost: no material net regression
```

Line count, token count, visual elegance, structural novelty, or manually shortened source-grounded traces are diagnostics only. They are never sufficient acceptance evidence.

## 2. Immutable comparison baseline

The baseline for this program is:

```text
Repository: ach1992/github-project-orchestrator
Integration target: main
Baseline commit: f98e8a242c720931e34aa7c4e8a799090e3d0495
Released version: v1.2.2
```

The baseline does not float if `main` advances. Target freshness is a separate integration concern.

Baseline semantics are derived from the canonical runtime/design/test owners at that commit, especially:

- `skill/SKILL.md`
- `skill/references/*.md`
- `design/RULE-MAP.md`
- `design/STATE-MODEL.md`
- `design/DECISION-GRAPHS.md`
- `skill/references/eval-scenarios.md`
- `tools/validate_skill.py`
- deterministic helper tests
- `benchmarks/phase7/*`

This document is not a second canonical rule registry. It defines the optimization/proof protocol; semantic truth remains with the existing canonical owners.

## 3. Evidence hierarchy

Keep evidence roles separate so a cleaner-looking representation cannot manufacture its own proof.

### 3.1 Mechanical equivalence

Baseline-derived deterministic checks may prove objective facts such as Rule/owner identity, Goal/state/router/eval coverage, configured predicate ownership, exact baseline identity, and selected representation invariants.

They do **not** prove prose/judgment equivalence or model performance.

### 3.2 Source-grounded policy simulation

Pinned source-grounded traces may verify expected protected behavior and report structural/context/friction diagnostics. Because a lossless representation should preserve the same normative behavior, a hand-authored synthetic trace difference is not evidence that an actual model reasons faster or more reliably.

Source-grounded representation comparisons are therefore always ineligible to prove the program's practical-improvement requirement.

### 3.3 Actual model/runtime paired A/B trials

Only comparable actual model/runtime paired A/B evidence may satisfy practical improvement. Trials use the exact immutable baseline and one exact candidate, equivalent model/runtime/settings/tool availability, balanced run order, auditable transcript/tool-log references, and observable metrics only. Do not request, store, or score private chain-of-thought.

The machine-readable contract and scorer live in:

- `benchmarks/phase7/MODEL-TRIAL-PROTOCOL.md`
- `benchmarks/phase7/model-trial-cases.json`
- `tools/score_model_trials.py`

### 3.4 Semantic/high-assurance review

Model-trial gains still require review for semantic completeness, benchmark construction, evidence authenticity, maintenance/routing cost, candidate/target freshness, and overfitting to one model or scenario set.

## 4. Core design principle

Optimize **decision inference depth**, not prose aesthetics.

For each runtime decision, prefer the cheapest representation that preserves all required semantics:

| Logic shape | Preferred representation when justified |
|---|---|
| lifecycle transition | state-transition table / finite-state relation |
| branching decision | ordered decision table or compact ASCII decision graph |
| authority/gate | canonical predicate + decision table |
| simultaneous consequences | set semantics + obligation union |
| precedence | ordered conditions with explicit first controlling condition |
| forbidden implication | compact non-edge / forbidden-inference matrix |
| source selection | direct router table |
| deterministic invariant | script/test rather than repeated prose reasoning |
| output/handoff shape | explicit schema |
| nuanced engineering/product judgment | concise prose, not brittle Boolean encoding |
| rare compatibility/edge behavior | event-triggered reference, not unconditional hot-path text |

A representation is not better merely because it is more graphical for a human. Mermaid and large visual diagrams may remain useful design documentation, while runtime tables/ASCII graphs/predicates may provide better token locality and traversal behavior for an LLM. That expected benefit remains a hypothesis until actual model/runtime trials support it.

## 5. Lossless-equivalence surface

Before any canonical runtime representation changes, preserve/check at least these classes.

### 5.1 Rule and goal identity

- exact baseline canonical Rule-ID set;
- one canonical owner per Rule ID;
- Goal-to-Rule and Rule-to-eval coverage;
- no orphan/duplicate owner introduced by restructuring.

### 5.2 Runtime dimensions

Preserve independent meanings and non-implications for:

- `Role`
- `ProjectAuthority`
- `ScopedAuthorization`
- `CoordinationBaseline`
- `AssuranceLevel`
- `RiskLevel`
- `ExecutionPath`
- `ContractPersistence` where applicable
- `ExecutionStrategy` where applicable
- `ApplicableEffects`

No representation optimization may reconstruct a scalar profile/action class that loses existing orthogonality.

### 5.3 Lifecycle namespaces

Preserve independent state namespaces and their valid meanings/transitions:

- `TaskState`
- `WorkerStatus`
- `WriteState`
- `DeliveryState`
- `MasterBoundary`

String equality across namespaces is never a semantic edge.

### 5.4 Canonical decision ownership

Preserve singular ownership and semantics for decisions such as:

- `CAN_EXECUTE(action)`
- `MASTER_STOP(boundary, independent_work)`
- `REVIEW_VALID(envelope)`
- delivery proof/readiness decisions owned by release semantics
- Worker assignment/staleness/absorption rules

A candidate may change the representation but must not create competing independently-derived versions.

### 5.5 Multi-effect obligations

`ApplicableEffects` remains a set and required controls remain the union of obligations for every actual/deterministic effect. A shortcut or decision table must not collapse `INTEGRATION + PRODUCTION + DESTRUCTIVE_OR_IRREVERSIBLE` into one scalar class or erase an independent gate.

### 5.6 Progressive loading and direct reachability

- every runtime domain required by an event remains directly reachable from `SKILL.md`;
- a rule must not depend on having accidentally loaded another reference first;
- cold/rare-path material must not become a new unconditional hot-path dependency without measured justification.

### 5.7 Compatibility

Legacy accepted inputs may be normalized once into the canonical vocabulary, but the resulting meaning must remain identical to the baseline. Representation optimization is not permission to remove compatibility behavior.

## 6. Forbidden-inference guard

Candidate representations must continue preventing at least these high-value false edges:

| Observed fact | Must not imply |
|---|---|
| `HIGH_ASSURANCE` | `FULL`, persistence, approval, or broader Authority by itself |
| `STANDARD` | `FULL` by itself |
| technical capability/access | broader `ProjectAuthority` |
| exact `ScopedAuthorization` | project-wide Authority upgrade |
| Worker `BLOCKED` | automatic `MasterBoundary.BLOCKED` |
| `TaskState.BLOCKED` | automatic `MasterBoundary.BLOCKED` |
| `WriteState.UNKNOWN` | automatic Master stop |
| `TaskState.INTEGRATED` | `DeliveryState.DELIVERED` |
| delivery target identity | delivery lifecycle state |
| no pre-existing READY Issue | permission to stop |
| existing explicit contract | `FULL` by itself |
| `FULL` | persisted Issue/contract by itself |
| environment name such as staging/test | proof of reversible/non-production effect |
| workflow-triggering push | `PRODUCTION` unless deterministic triggered effect actually is production |

This table is a proof target, not a new rule owner. Baseline canonical files remain normative.

## 7. Candidate representation families

Treat each as a hypothesis to test, not a planned rewrite.

### 7.1 Transient decision frame

A compact runtime frame may reduce repeated reconstruction of already-established facts:

```text
Role
ProjectAuthority
CoordinationBaseline
AssuranceLevel
ActiveOutcome identity
CurrentEvent
ExecutionPath
RiskLevel when decision-relevant
ProposedAction + ApplicableEffects
Required current evidence/freshness
IndependentUsefulWork
DeliveryRequirement / target when relevant
```

The frame is transient reasoning structure, not a persisted manager-memory artifact or new lifecycle state.

Expected benefit: fewer repeated classifications and fewer inconsistent re-derivations within one decision cycle. This remains an empirical hypothesis until paired model/runtime trials support it.

### 7.2 Decision card

For a bounded domain decision, co-locate:

```text
TRIGGER
INPUTS
DECIDE
TRUE/FALSE OR CONTROL OUTPUT
EXCEPTIONS / UNKNOWN HANDLING
LOAD DEEPER ONLY IF ...
```

Expected benefit: reduce reference hopping and hidden exception discovery while retaining a single canonical owner.

### 7.3 Ordered decision table / ASCII DAG

Use when the current behavior is fundamentally branching/precedence logic. Keep the common path short and route uncertainty/exceptional cases to deeper owner text.

Expected benefit: lower inference depth and more deterministic traversal.

### 7.4 Safe common-path short circuit

A shortcut is allowed only when it is mechanically demonstrated to be a safe subset/equivalent of the canonical decision. Example shape:

```text
FAST_SUBSET(action) == true  =>  CAN_EXECUTE(action) == true
```

If the implication cannot be proven/tested for every allowed input combination, do not adopt the shortcut.

### 7.5 Hot/warm/cold/DEV-only locality

Split or route content by actual activation frequency only when actual model/runtime evidence shows the saved context/traversal cost exceeds new routing/maintenance cost. File length alone is not evidence.

### 7.6 Legacy normalization layer

When compatibility inputs are encountered, map them once to canonical current terms before ordinary reasoning. Do not repeatedly carry legacy vocabulary through the hot path.

### 7.7 Machine-readable semantic IR

Consider only for deterministic mechanics whose machine representation can be validated/generated without becoming a competing semantic owner. Do not encode nuanced judgment merely to obtain a cleaner schema.

## 8. Experiment protocol

For each candidate mechanism:

1. **Hypothesis** — name the concrete recurring inference/traversal problem.
2. **Baseline path** — identify exact canonical owners and representative scenarios.
3. **Candidate representation** — change the smallest possible surface first, preferably outside the canonical runtime during prototype stage.
4. **Equivalence check** — map every affected baseline semantic to candidate form.
5. **Protected tests** — run deterministic/eval/adversarial checks before measuring performance.
6. **Source-grounded diagnostic** — compare expected protected behavior and structural/context implications without making a performance claim.
7. **Actual paired trial** — compare the same case/workload under equivalent model/runtime/settings/tool conditions using the model-trial protocol.
8. **Benefit check** — require material observable paired improvement; record token/line/aesthetic changes only as diagnostics.
9. **Maintenance check** — account for new router nodes, files, generated artifacts, validator burden, and future change cost.
10. **Decision** — `ADOPT`, `REJECT`, or `REVISE`; rejection is a valid successful experiment.

Never bundle many representation changes before the source of benefit is understood.

## 9. Measurement model

### Protected metrics — hard gates

A candidate fails if any required protected behavior regresses, including:

- unsafe/stale mutation;
- authority/gate leakage;
- state namespace collapse;
- lost obligation from a multi-effect action;
- stale review/integration approval;
- incorrect Worker ownership/assignment behavior;
- false delivery completion;
- wrong/early terminal Master stop;
- loss of zero-chat recoverability;
- compatibility regression required by baseline.

Protected failures cannot be compensated by a weighted performance score.

### Primary actual-trial metrics

Measure only observable behavior; do not rely on hidden reasoning traces:

- protected-behavior violation count;
- wrong next-action decision count;
- observable steps before first useful action;
- unnecessary user questions/confirmations;
- unnecessary actions/tool operations;
- unnecessary runtime-reference loads;
- terminal-turn errors requiring a manual user `continue`.

The model-trial scorer also derives composite avoidable events from observable unnecessary questions/actions/reference loads/manual-continue events.

### Diagnostic metrics

The following can explain a result but are not optimization proof by themselves:

- source-grounded policy-trace step counts;
- source/reference surface size;
- line/word/token counts;
- expected hot/cold activation surface;
- optional latency/token measurements when runtime/provider conditions are not controlled enough for primary use.

## 10. One-to-one migration ledger

During Phase C, every changed canonical surface must be reviewable with a ledger row like:

| Baseline owner/semantic | Candidate owner/representation | Equivalence evidence | Actual benefit evidence | Status |
|---|---|---|---|---|
| exact current rule/decision | exact candidate form | eval/property/review reference | paired model/runtime trial reference | unchanged / adopted / rejected |

The ledger may be kept in the active Issue/PR if that is sufficient for recovery; do not create a permanent duplicate runtime registry solely to host it.

## 11. Phase gates

### Phase A — baseline/equivalence (#36)

No canonical runtime representation change. Establish exact baseline, deterministic equivalence inventory/checks, source-grounded diagnostic lane, and actual model/runtime A/B protocol/scorer.

### Phase B — experiments (#37)

Prototype and measure. Reject non-beneficial ideas even if they look cleaner. No representation may be selected from source-grounded traces alone.

### Phase C — lossless migration (#38)

Apply only winners supported by actual paired model/runtime evidence. Require one-to-one semantic mapping and rerun the evidence suite on the actual final implementation.

### Phase D — final proof/integration (#39)

Freeze exact candidate/target identity, run full validation, complete semantic review and fresh independent HIGH_ASSURANCE review, then integrate through the repository-normal controlled path only when all gates pass.

Public version/release publication remains a separate consequential action.

## 12. Acceptance rule

A candidate representation is eligible for migration/integration only if all are true:

```text
ProtectedBehavior(candidate) >= ProtectedBehavior(baseline)
SemanticCoverage(candidate) == RequiredBaselineCoverage
ActualPairedModelRuntimeEvidence == PASS
MaterialObservableMetric(candidate) < baseline on controlled paired evidence
NetMaintenanceAndRoutingCost(candidate) does not erase the measured gain
ExactCandidateValidation == PASS
FreshIndependentReview == COMPLETE / APPROVE
```

Source-grounded traces, token counts, line counts, or structural elegance can never substitute for `ActualPairedModelRuntimeEvidence == PASS`.

If the experiments show that the current representation is already the better trade-off, the correct result is **no runtime refactor**. The purpose of this program is a better operating Skill, not a larger change set.