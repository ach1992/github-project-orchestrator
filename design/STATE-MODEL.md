# State Model

Status: canonical design/traceability model for the current refactored runtime. Historical compatibility notes describe the immutable `v1.0.0` representation; runtime definitions live in their canonical owners under `skill/`.

## 1. Scope hierarchy

The Skill contains state at several different lifetimes. The current runtime model makes the scope explicit instead of relying on prose context.

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
| `CoordinationBaseline` | `LIGHTWEIGHT | STANDARD` | accepted outcome / coordination system | stable until material coordination/recovery needs change | Owns coordination weight independently from assurance. |
| `AssuranceLevel` | `NORMAL | HIGH_ASSURANCE` | affected change/dependency chain | recompute when risk, policy, or explicit control requirement changes | Additive to the coordination baseline. It never creates a human gate by itself. |
| `RiskLevel` | `LOW | MEDIUM | HIGH | CRITICAL` | substantive change/work item | recompute only when it can change a gate, review/validation depth, rollback, or release treatment | Not project size or importance. |
| `ExecutionPath` | `FAST | FULL` | work item / bounded cycle | select when work becomes executable; promote on new evidence | Independent from coordination baseline, assurance, and persistence. |
| `ContractPersistence` | `TRANSIENT | PERSISTED` | work item | decide from recovery/coordination value | FULL does not imply persisted. Existing persistence does not imply FULL. |
| `ExecutionStrategy` | `SELF_EXECUTE | DELEGATE | HYBRID` | work item | recompute when capability/dependency/throughput changes | Worker availability never creates a Master stop by itself. |
| `ApplicableEffects` | set of effect classes | individual action | classify immediately before consequential action | A set, not a scalar; one action may have multiple simultaneous effects. |
| `CapabilitySnapshot` | structured evidence | runtime / next action | new runtime, material access change, or decision-relevant invalidation | Capability is execution feasibility, not authorization. |
| `TaskState` | namespaced lifecycle | work item | lifecycle transitions | Separate from Worker handoff and Master boundary. |
| `WorkerStatus` | namespaced handoff status | assignment generation | handoff/reconciliation | Never automatically propagates to Master stop state. |
| `WriteState` | `KNOWN | UNKNOWN` plus evidence | individual mutation | immediately after ambiguous mutation result | `UNKNOWN` requires reconciliation before retry; it is not automatically a project stop. |
| `ReviewEnvelope` | target/candidate/contract identities + evidence | change set | invalidated by material identity/effective-change drift | Approval is identity-bound. |
| `DeliveryRequirement` | `INTEGRATION_ONLY | DELIVERY_REQUIRED` | accepted outcome / work item | set by accepted completion criteria | Separates completion requirement from environment. |
| `DeliveryTarget` | environment/deployment target | delivery operation | set by release model | Examples: staging, production, other explicit target. |
| `DeliveryState` | lifecycle state | immutable artifact/commit + environment | release/deployment evidence changes | `TaskState.INTEGRATED` must not imply `DeliveryState.DELIVERED`. |
| `MasterBoundary` | namespaced terminal/local boundary | dependency chain/project | after synthesis and boundary classification | Local boundaries do not automatically terminate the Master while independent useful work exists. |

## 3. Product type that replaced `Operating Profile`

`v1.0.0` used the scalar values `LIGHTWEIGHT | STANDARD | HIGH_ASSURANCE`, while its own rules treated `HIGH_ASSURANCE` as additive. The current lossless model is:

```text
CoordinationBaseline x AssuranceLevel

LIGHTWEIGHT x NORMAL
LIGHTWEIGHT x HIGH_ASSURANCE
STANDARD    x NORMAL
STANDARD    x HIGH_ASSURANCE
```

This makes `STANDARD + HIGH_ASSURANCE` persistable without reconstructing a missing coordination baseline after rotation or Worker handoff.

Compatibility retained for persisted `v1.0.0`-era inputs:

```text
legacy LIGHTWEIGHT    -> CoordinationBaseline=LIGHTWEIGHT, AssuranceLevel=NORMAL
legacy STANDARD       -> CoordinationBaseline=STANDARD,    AssuranceLevel=NORMAL
legacy HIGH_ASSURANCE -> AssuranceLevel=HIGH_ASSURANCE + recover/preserve the already-valid baseline
```

The last mapping intentionally cannot invent a baseline. Runtime recovery/helper logic must resolve it from authoritative persisted coordination state or preserve/reject the ambiguity until the baseline is known.

## 4. Action effects are a set

The legacy action classes describe effects that can coexist. The current runtime models them as a set:

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

The runtime execution predicate is:

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

The Worker model distinguishes immutable generation identity from a later same-generation concurrency checkpoint:

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

Do not use a bare status token as a cross-domain state. The current canonical vocabularies are:

```text
TaskState.DRAFT
TaskState.BLOCKED
TaskState.READY
TaskState.IN_PROGRESS
TaskState.IN_REVIEW
TaskState.CHANGES_REQUESTED
TaskState.INTEGRATION_READY
TaskState.INTEGRATED
TaskState.CANCELLED
TaskState.SUPERSEDED
TaskState.ROLLED_BACK

WorkerStatus.STALE_ASSIGNMENT
WorkerStatus.MATERIAL_DECISION_REQUIRED
WorkerStatus.SCOPE_CHANGE_REQUIRED
WorkerStatus.ENVIRONMENT_MISMATCH
WorkerStatus.BLOCKED
WorkerStatus.READY_FOR_REVIEW

WriteState.KNOWN
WriteState.UNKNOWN

DeliveryState.NOT_STARTED
DeliveryState.PENDING
DeliveryState.DELIVERED
DeliveryState.FAILED_OR_UNKNOWN

MasterBoundary.PROJECT_COMPLETE
MasterBoundary.APPROVAL_REQUIRED
MasterBoundary.MATERIAL_DECISION_REQUIRED
MasterBoundary.BLOCKED
MasterBoundary.RISK_ESCALATION
MasterBoundary.MISSING_CAPABILITY
MasterBoundary.NO_READY_WORK
MasterBoundary.WRITE_OUTCOME_UNKNOWN
MasterBoundary.USER_STOP
```

Legacy bare or old-domain tokens such as `TaskState.DONE` / `WorkerStatus.DONE` are not canonical runtime states. Compatibility aliases, where explicitly supported (for example legacy `MERGE_READY` input), are normalized at their owning boundary rather than added to the canonical state vocabulary.

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
