# Decision Graphs

Status: Phase 1 design model with Phase 3 runtime kernel ownership recorded. The graphs remain design/traceability artifacts; runtime definitions live in their canonical owners under `skill/`.

## 1. Master execution graph

```text
ROOT SPECIFICATION
       |
       v
ACTIVE OUTCOME <-------------------------------+
       |                                        |
       v                                        |
ASSESS DECISION-RELEVANT DELTAS                 |
       |                                        |
       v                                        |
SELECT HIGHEST-VALUE WORK                       |
       |                                        |
       +-- no executable work --> SYNTHESIZE ---+
       |                            |
       |                            +-- work found
       |                            |
       |                            `-- none --> BOUNDARY TEST
       v
PREPARE WORK
(path / contract / strategy)
       |
       v
NEXT ACTION
       |
       v
CLASSIFY APPLICABLE EFFECTS
       |
       v
AUTHORITY + GATES + CAPABILITY + FRESHNESS
       |
       +-- cannot act --> classify boundary
       |
       `-- can act
             |
             v
            ACT
             |
             v
           VERIFY
             |
             v
        REVIEW / INTEGRATE / DELIVER as required
             |
             v
          RECONCILE ----------------------------+
```

The graph removes chat-turn, commit, PR-update, Worker-handoff, and tool-batch boundaries from the control loop. They are events, not terminal states.

Phase 3 runtime owner for action execution is `skill/references/authority-gates.md` via `CAN_EXECUTE(action)`.

## 2. Boundary propagation

```text
Boundary detected
      |
      +-- USER_STOP ------------------------------> STOP
      |
      +-- PROJECT_COMPLETE -----------------------> STOP
      |
      +-- urgent/project-wide --------------------> STOP / relay exact need
      |
      `-- local
            |
            +-- independent safe useful work? yes -> freeze branch -> CONTINUE
            `-- no -------------------------------> STOP / relay exact need
```

Phase 3 runtime owner: `skill/references/master-cycle.md`.

```text
MASTER_STOP(boundary, independent_work) =
    USER_STOP
    OR PROJECT_COMPLETE
    OR (
        CanonicalBoundaryExists
        AND (
            BoundaryIsUrgent
            OR BoundaryIsProjectWide
            OR NOT IndependentSafeUsefulWorkExists
        )
    )
```

`WorkerStatus.BLOCKED`, a queued external job, missing Worker dispatch capability, or absence of a pre-existing READY Issue cannot directly satisfy `MASTER_STOP`.

## 3. Authorization graph

Phase 3 runtime owner: `skill/references/authority-gates.md`.

```text
Accepted scope --------+
Role ------------------+
ProjectAuthority ------+
Repository policy -----+--> CAN_EXECUTE(action)
ApplicableEffects -----+        |
ScopedAuthorization ---+        +-- yes -> mutate -> verify/reconcile
Capability ------------+        `-- no  -> boundary/alternative path
Fresh evidence --------+
```

Forbidden edge:

```text
Capability -X-> ProjectAuthority
Risk       -X-> ProjectAuthority
Assurance  -X-> ProjectAuthority
Environment label -X-> safe/reversible classification
```

## 4. Effect and obligation graph

```text
Actual deterministic consequences
              |
              v
      ApplicableEffects (SET)
       /       |       \
      v        v        v
INTEGRATION PRODUCTION DESTRUCTIVE ...
      \        |        /
       \       |       /
        v      v      v
       UNION OF OBLIGATIONS
              |
              v
     GateDecision for action
```

No single effect classification is allowed to suppress an independently applicable obligation.

## 5. Review and delivery proof kernels

Phase 3 records two additional canonical runtime predicates without moving their domain rules into this design artifact:

```text
REVIEW_VALID(envelope)
    owner -> skill/references/review-integration.md
    purpose -> determine whether existing review remains valid for the exact current effective change

DELIVERY_PROVEN(artifact, target, evidence)
    owner -> skill/references/release.md
    purpose -> determine whether delivery-required completion is actually proven
```

These predicates do not absorb CI, integration-gate, production-gate, or incident semantics that remain separate inputs in their canonical runtime owners.

## 6. Work-control dimensions

```text
CoordinationBaseline ----> coordination / persistence / WIP controls

RiskLevel ---------------> may raise AssuranceLevel
AssuranceLevel ----------> evidence / validation / review depth

Work ambiguity/dependency/review need ---> ExecutionPath FAST|FULL
Recovery/coordination value ------------> ContractPersistence
Capability/throughput/dependency --------> ExecutionStrategy SELF|DELEGATE|HYBRID
```

Forbidden shortcuts:

```text
STANDARD       -X-> FULL
LIGHTWEIGHT    -X-> FAST
HIGH_ASSURANCE -X-> FULL
HIGH_ASSURANCE -X-> human approval
FULL           -X-> persisted contract
persisted contract -X-> FULL
repository size -X-> STANDARD/HIGH_ASSURANCE by itself
```

## 7. Event-to-rule activation

Phase 4, not Phase 3, owns progressive event routing. The later runtime should activate proof obligations by event rather than treating every invariant as equally active on every step.

| Event | Required rule domains |
|---|---|
| new/replacement Master | recovery, identity, authority, capability, outcome |
| first ownership | root specification, proportional readiness, outcome, source-of-truth |
| before consequential mutation | accepted scope, role, authority, effects, gates, capability, fresh mutable identity |
| before delegation | contract/READY, assignment identity, Worker envelope, target separation |
| Worker correction/resume | assignment generation + `CheckpointHEAD` concurrency |
| before review | target/candidate identity, effective change, untrusted execution surface |
| before integration | fresh review envelope, CI classification, target/candidate drift, integration gate |
| before production | deterministic production effect, explicit production gate, rollback/migration readiness |
| after ambiguous write | `WriteState.UNKNOWN`, authoritative reconciliation, no blind retry |
| before terminal response | synthesis, local-vs-project boundary, independent useful work, recoverability |
| rotation consideration | continuity signals and safe rotation boundary only |

## 8. Forbidden inference matrix

| Observed fact | Must NOT infer | Correct relation |
|---|---|---|
| technical access exists | broader Authority | access only affects feasibility |
| risk increases | broader Authority | risk can strengthen controls |
| `HIGH_ASSURANCE` | human approval required | approval depends on action/gate, not assurance alone |
| `HIGH_ASSURANCE` | `FULL` path | assurance and execution path are orthogonal |
| `FULL` | persistent contract | persistence requires recovery/coordination value |
| persistent Issue/contract exists | `FULL` | reuse may remain FAST if work qualifies |
| Worker is blocked/stale | Master is blocked | Master absorbs and searches alternatives |
| PR/target integrated | delivery complete | delivery requires target-specific evidence |
| deployment command succeeded | delivery proven | verify immutable artifact/environment/health as required |
| environment says `staging` | reversible/non-production effect | classify actual deterministic effect |
| one tool route fails | capability is absent | distinguish route failure from capability absence |
| no READY item exists | `NO_READY_WORK` | synthesize/refine/unblock first |
| context is long | rotate Master | rotate only on continuity signals |
| root spec exists | reread it every cycle | normal execution uses nearer authoritative sources |
| one-off action approval | project-wide Authority upgrade | represent it as `ScopedAuthorization` |
| Worker current HEAD advanced through its commits | stale assignment | `StartHEAD` is historical; staleness requires invalidated envelope |
