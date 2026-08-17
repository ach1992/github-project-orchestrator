# State Model

Status: Phase 1 design model. It describes v1.0.0 semantics without changing runtime behavior.

## 1. Scope hierarchy

The current Skill contains state at several different lifetimes. The next runtime model should make the scope explicit instead of relying on prose context.

```text
Repository / Project
        |
        v
Accepted Outcome
        |
        v
Work Item / Task Contract
        |
        v
Change Set / Candidate / PR
        |
        v
Action / Mutation
        |
        v
Evidence -> Integration -> Delivery
```

Agent/runtime identity is orthogonal to that hierarchy:

```text
Agent Runtime
  |- Role
  |- ProjectAuthority
  |- CapabilitySnapshot
  `- RecoveryState
```

## 2. Canonical dimensions

| Dimension | Type | Scope | Lifetime / recompute trigger | Notes |
|---|---|---|---|---|
| `Role` | `MASTER | WORKER` | agent runtime | stable until explicit reassignment | Ownership boundary, not an authorization level. |
| `ProjectAuthority` | `ADVISORY | MANAGED | AUTONOMOUS_WITH_GATES` | project/runtime envelope | stable until explicit applicable authorization changes | Capability, risk, environment, and assurance can constrain it but never upgrade it. |
| `ScopedAuthorization` | structured grant | exact action/target/effect | expires with its stated scope | A one-off approval can satisfy an action gate without mutating `ProjectAuthority`. |
| `CoordinationBaseline` | `LIGHTWEIGHT | STANDARD` | accepted outcome / coordination system | stable until material coordination/recovery needs change | Replaces the coordination meaning currently overloaded into `Operating Profile`. |
| `AssuranceLevel` | `NORMAL | HIGH_ASSURANCE` | affected change/dependency chain | recompute when risk, policy, or explicit control requirement changes | Additive to the coordination baseline. It never creates a human gate by itself. |
| `RiskLevel` | `LOW | MEDIUM | HIGH | CRITICAL` | substantive change/work item | recompute only when it can change a gate, review/validation depth, rollback, or release treatment | Not project size or importance. |
| `ExecutionPath` | `FAST | FULL` | work item / bounded cycle | select when work becomes executable; promote on new evidence | Independent from coordination baseline, assurance, and persistence. |
| `ContractPersistence` | `TRANSIENT | PERSISTED` | work item | decide from recovery/coordination value | FULL does not imply persisted. Existing persistence does not imply FULL. |
| `ExecutionStrategy` | `SELF | DELEGATE | HYBRID` | work item | recompute when capability/dependency/throughput changes | Worker availability never creates a Master stop by itself. |
| `ApplicableEffects` | set of effect classes | individual action | classify immediately before consequential action | A set, not a scalar; one action may have multiple simultaneous effects. |
| `CapabilitySnapshot` | structured evidence | runtime / next action | new runtime, material access change, or decision-relevant invalidation | Capability is execution feasibility, not authorization. |
| `TaskState` | namespaced lifecycle | work item | lifecycle transitions | Separate from Worker handoff and Master boundary. |
| `WorkerStatus` | namespaced handoff status | assignment generation | handoff/reconciliation | Never automatically propagates to Master stop state. |
| `WriteState` | `KNOWN | UNKNOWN` plus evidence | individual mutation | immediately after ambiguous mutation result | `UNKNOWN` requires reconciliation before retry; it is not automatically a project stop. |
| `ReviewEnvelope` | target/candidate/contract identities + evidence | change set | invalidated by material identity/effective-change drift | Approval is identity-bound. |
| `DeliveryRequirement` | `INTEGRATION_ONLY | DELIVERY_REQUIRED` | accepted outcome / work item | set by accepted completion criteria | Separates completion requirement from environment. |
| `DeliveryTarget` | environment/deployment target | delivery operation | set by release model | Examples: staging, production, other explicit target. |
| `DeliveryState` | lifecycle state | immutable artifact/commit + environment | release/deployment evidence changes | `INTEGRATED` must not imply `DELIVERED`. |
| `MasterBoundary` | namespaced terminal/local boundary | dependency chain/project | after synthesis and boundary classification | Local boundaries do not automatically terminate the Master while independent useful work exists. |

## 3. Product type replacing `Operating Profile`

v1.0.0 uses the scalar values `LIGHTWEIGHT | STANDARD | HIGH_ASSURANCE`, but its own rules define `HIGH_ASSURANCE` as additive. The lossless model is therefore:

```text
CoordinationBaseline x AssuranceLevel

LIGHTWEIGHT x NORMAL
LIGHTWEIGHT x HIGH_ASSURANCE
STANDARD    x NORMAL
STANDARD    x HIGH_ASSURANCE
```

This makes `STANDARD + HIGH_ASSURANCE` persistable without reconstructing the missing coordination baseline after rotation or Worker handoff.

Compatibility during migration:

```text
legacy LIGHTWEIGHT   -> CoordinationBaseline=LIGHTWEIGHT, AssuranceLevel=NORMAL
legacy STANDARD      -> CoordinationBaseline=STANDARD,    AssuranceLevel=NORMAL
legacy HIGH_ASSURANCE -> AssuranceLevel=HIGH_ASSURANCE + recover/preserve the already-valid baseline
```

The last mapping is intentionally not allowed to invent a baseline. Phase 2 must resolve it from authoritative persisted coordination state or preserve legacy representation until the baseline is known.

## 4. Action effects are a set

The current action classes describe effects that can coexist. Model them as a set:

```text
ApplicableEffects(action) = {
  REVERSIBLE_IMPLEMENTATION,
  INTEGRATION,
  PRODUCTION,
  DESTRUCTIVE_OR_IRREVERSIBLE,
  EXTERNAL_COMMITMENT,
  ...
}
```

The required controls are the union of independently applicable obligations:

```text
RequiredObligations(action) = union(Gate(effect) for effect in ApplicableEffects(action))
```

Example:

```text
merge -> protected branch
      -> deterministic production deploy
      -> irreversible migration

ApplicableEffects = {INTEGRATION, PRODUCTION, DESTRUCTIVE_OR_IRREVERSIBLE}
```

Production pre-authorization may satisfy the production obligation but cannot erase the destructive obligation.

## 5. Authorization model

```text
ProjectAuthority
      |
      +-----------------------------+
      |                             |
      v                             v
normal reversible envelope    ScopedAuthorization
                                    |
                                    v
                             exact action/target/effect
```

A useful executable predicate for later phases is:

```text
CAN_EXECUTE(action) =
    InAcceptedScope(action)
    AND RoleAllows(action)
    AND ProjectAuthorityAllows(action)
    AND RepositoryPolicyAllows(action)
    AND RequiredGatesSatisfied(action)
    AND CapabilityAvailable(action)
    AND RequiredEvidenceFresh(action)
```

`CapabilityAvailable` is one conjunct. It cannot make `ProjectAuthorityAllows` true.

## 6. Assignment identity

The Worker model should distinguish immutable generation identity from a later same-generation concurrency checkpoint:

```text
AssignmentEnvelope
  AssignmentID
  ContractRevision
  WorkerID
  BaseSHA
  AssignedBranch
  IntegrationTarget
  StartHEAD              # immutable verified generation start
  AssignmentStatus
  ProjectAuthority
  CoordinationBaseline
  AssuranceLevel
  Risk/ReleaseConstraints

CorrectionEnvelope
  AssignmentID
  CheckpointHEAD          # reviewed/current HEAD for correction/resume
```

`StartHEAD` advancing because the Worker made authorized commits is not staleness. `CheckpointHEAD` mismatch during a correction/resume is a concurrency conflict.

## 7. Namespaced lifecycles

Do not use a bare status token as a cross-domain state.

```text
TaskState.DRAFT
TaskState.READY
TaskState.BLOCKED
TaskState.INTEGRATION_READY
TaskState.DONE

WorkerStatus.DONE
WorkerStatus.BLOCKED
WorkerStatus.STALE_ASSIGNMENT

WriteState.KNOWN
WriteState.UNKNOWN

DeliveryState.NOT_STARTED
DeliveryState.PENDING
DeliveryState.DELIVERED
DeliveryState.FAILED_OR_UNKNOWN

MasterBoundary.USER_STOP
MasterBoundary.PROJECT_COMPLETE
MasterBoundary.BLOCKED
MasterBoundary.MATERIAL_DECISION_REQUIRED
MasterBoundary.WRITE_OUTCOME_UNKNOWN
MasterBoundary.NO_READY_WORK
```

A boundary can be local, urgent, or project-wide. Namespace equality never implies propagation between domains.

## 8. Evidence identity

Evidence is valid only inside its identity envelope:

```text
EvidenceEnvelope
  RepositoryIdentity
  TargetIdentity
  CandidateIdentity
  RelevantSHA
  Environment
  ContractRevision (when applicable)
  ObservedAt / freshness semantics
```

Review, CI, integration, release, and production claims must bind to the relevant immutable identity rather than to narrative summaries.
