# Lossless Runtime Decision-Representation Optimization

Tracking: #35  
Baseline task: #36  
Prototype task: #37  
Migration task: #38  
Final proof/integration task: #39

## 1. Purpose

Optimize **how** the runtime expresses the existing orchestration semantics so an LLM can select and execute the correct path with less inference, reconstruction, irrelevant context traversal, and activation error.

This program is intentionally different from adding, removing, or changing orchestration policy. The candidate runtime is acceptable only when the current semantic contract is preserved losslessly and comparable evidence shows a material execution benefit.

The optimization target is:

```text
Semantic behavior:       IDENTICAL for protected baseline requirements
Safety/correctness:      >= baseline
Decision quality:        >= baseline
Practical friction:      < baseline on at least one material comparable metric
Maintenance/routing cost: no material net regression
```

Line count, token count, visual elegance, or structural novelty are diagnostics only. They are never sufficient acceptance evidence.

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

## 3. Core design principle

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

A representation is not better merely because it is more graphical for a human. Mermaid and large visual diagrams may remain useful design documentation, while runtime tables/ASCII graphs/predicates may provide better token locality and traversal behavior for an LLM.

## 4. Lossless-equivalence surface

Before any canonical runtime representation changes, preserve/check at least these classes.

### 4.1 Rule and goal identity

- exact baseline canonical Rule-ID set;
- one canonical owner per Rule ID;
- Goal-to-Rule and Rule-to-eval coverage;
- no orphan/duplicate owner introduced by restructuring.

### 4.2 Runtime dimensions

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

### 4.3 Lifecycle namespaces

Preserve independent state namespaces and their valid meanings/transitions:

- `TaskState`
- `WorkerStatus`
- `WriteState`
- `DeliveryState`
- `MasterBoundary`

String equality across namespaces is never a semantic edge.

### 4.4 Canonical decision ownership

Preserve singular ownership and semantics for decisions such as:

- `CAN_EXECUTE(action)`
- `MASTER_STOP(boundary, independent_work)`
- `REVIEW_VALID(envelope)`
- delivery proof/readiness decisions owned by release semantics
- Worker assignment/staleness/absorption rules

A candidate may change the representation but must not create competing independently-derived versions.

### 4.5 Multi-effect obligations

`ApplicableEffects` remains a set and required controls remain the union of obligations for every actual/deterministic effect. A shortcut or decision table must not collapse `INTEGRATION + PRODUCTION + DESTRUCTIVE_OR_IRREVERSIBLE` into one scalar class or erase an independent gate.

### 4.6 Progressive loading and direct reachability

- every runtime domain required by an event remains directly reachable from `SKILL.md`;
- a rule must not depend on having accidentally loaded another reference first;
- cold/rare-path material must not become a new unconditional hot-path dependency without measured justification.

### 4.7 Compatibility

Legacy accepted inputs may be normalized once into the canonical vocabulary, but the resulting meaning must remain identical to the baseline. Representation optimization is not permission to remove compatibility behavior.

## 5. Forbidden-inference guard

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

## 6. Candidate representation families

Treat each as a hypothesis to test, not a planned rewrite.

### 6.1 Transient decision frame

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

Expected benefit: fewer repeated classifications and fewer inconsistent re-derivations within one decision cycle.

### 6.2 Decision card

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

### 6.3 Ordered decision table / ASCII DAG

Use when the current behavior is fundamentally branching/precedence logic. Keep the common path short and route uncertainty/exceptional cases to deeper owner text.

Expected benefit: lower inference depth and more deterministic traversal.

### 6.4 Safe common-path short circuit

A shortcut is allowed only when it is mechanically demonstrated to be a safe subset/equivalent of the canonical decision. Example shape:

```text
FAST_SUBSET(action) == true  =>  CAN_EXECUTE(action) == true
```

If the implication cannot be proven/tested for every allowed input combination, do not adopt the shortcut.

### 6.5 Hot/warm/cold/DEV-only locality

Split or route content by actual activation frequency only when measurement shows the saved context/traversal cost exceeds new routing/maintenance cost. File length alone is not evidence.

### 6.6 Legacy normalization layer

When compatibility inputs are encountered, map them once to canonical current terms before ordinary reasoning. Do not repeatedly carry legacy vocabulary through the hot path.

### 6.7 Machine-readable semantic IR

Consider only for deterministic mechanics whose machine representation can be validated/generated without becoming a competing semantic owner. Do not encode nuanced judgment merely to obtain a cleaner schema.

## 7. Experiment protocol

For each candidate mechanism:

1. **Hypothesis** — name the concrete recurring inference/traversal problem.
2. **Baseline path** — identify exact canonical owners and representative scenarios.
3. **Candidate representation** — change the smallest possible surface first, preferably outside the canonical runtime during prototype stage.
4. **Equivalence check** — map every affected baseline semantic to candidate form.
5. **Protected tests** — run deterministic/eval/adversarial checks before measuring speed/friction.
6. **Comparable run** — compare the same workload/scenario and evidence availability.
7. **Benefit check** — record only material metrics, not aesthetic observations.
8. **Maintenance check** — account for new router nodes, files, generated artifacts, validator burden, and future change cost.
9. **Decision** — `ADOPT`, `REJECT`, or `REVISE`; rejection is a valid successful experiment.

Never bundle many representation changes before the source of benefit is understood.

## 8. Measurement model

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

### Optimization metrics

Use comparable evidence where practical:

- steps/tool calls before first useful action;
- number of runtime references activated before the decisive action;
- approximate instruction/context surface activated;
- repeated reconstruction/reclassification of stable dimensions;
- unnecessary confirmations;
- unnecessary Issue/ADR/process artifact creation;
- repeated discovery/recovery reads;
- Worker startup/handoff/recovery steps;
- review/integration steps before a valid decision;
- false router activation or unnecessary cold-reference load;
- terminal-turn errors requiring a manual user `continue`.

Token/line count may be recorded as explanatory diagnostics but is not a success metric by itself.

## 9. One-to-one migration ledger

During Phase C, every changed canonical surface must be reviewable with a ledger row like:

| Baseline owner/semantic | Candidate owner/representation | Equivalence evidence | Benefit evidence | Status |
|---|---|---|---|---|
| exact current rule/decision | exact candidate form | eval/property/review reference | comparable benchmark evidence | unchanged / adopted / rejected |

The ledger may be kept in the active Issue/PR if that is sufficient for recovery; do not create a permanent duplicate runtime registry solely to host it.

## 10. Phase gates

### Phase A — baseline/equivalence (#36)

No canonical runtime representation change. Establish exact baseline, deterministic equivalence inventory/checks, and current comparable benchmark protocol.

### Phase B — experiments (#37)

Prototype and measure. Reject non-beneficial ideas even if they look cleaner.

### Phase C — lossless migration (#38)

Apply only winners. Require one-to-one semantic mapping and rerun the benchmark on the actual final implementation.

### Phase D — final proof/integration (#39)

Freeze exact candidate/target identity, run full validation, complete semantic review and fresh independent HIGH_ASSURANCE review, then integrate through the repository-normal controlled path only when all gates pass.

Public version/release publication remains a separate consequential action.

## 11. Acceptance rule

A candidate representation is eligible for integration only if all are true:

```text
ProtectedBehavior(candidate) >= ProtectedBehavior(baseline)
SemanticCoverage(candidate) == RequiredBaselineCoverage
MaterialFrictionOrDecisionMetric(candidate) < baseline on comparable evidence
NetMaintenanceAndRoutingCost(candidate) does not erase the measured gain
ExactCandidateValidation == PASS
FreshIndependentReview == COMPLETE / APPROVE
```

If the experiments show that the current representation is already the better trade-off, the correct result is **no runtime refactor**. The purpose of this program is a better operating Skill, not a larger change set.