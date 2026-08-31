# Phase C Lossless Runtime Representation Migration Ledger

Tracking: #35, #38  
Selection owner: #37 / #50  
Migration base: `0165bc2a26bdf7452f05160c3e91f47b4fa7ae9c`

Status: implementation evidence for the exact Phase C candidate. This document is **not** a normative runtime owner; canonical semantics remain in `skill/`.

## Migration rule

Apply only the representation concepts selected by Phase B. Before materialization, each selected target surface must still equal the exact surface reviewed in its frozen prototype source ref. Any target-surface drift invalidates blind application and requires reconciliation.

All non-target current-runtime bytes remain current-target bytes; immutable `v1.2.2@f98e8a242c720931e34aa7c4e8a799090e3d0495` is semantic comparison evidence only and is never materialized wholesale.

## P1 — runtime dimensions and gate input ownership

- Baseline/current owners: `skill/SKILL.md` §1; `skill/references/authority-gates.md` §1.
- Selected evidence: #52 / PR #53; prototype `runtime-dimension-invariants-v2`.
- Representation: six-dimension local stability/non-implication matrix in the kernel; gate owner consumes those current dimensions instead of redeclaring their ontology.
- Protected meaning: dimension orthogonality; Role/Authority/Coordination stability; additive/scoped HIGH_ASSURANCE; bounded ScopedAuthorization; capability/environment separation; FAST compatibility; no new state/frame/cache.
- Benefit: removes co-loaded ontology repetition and places stability/non-implication beside the dimension it constrains.
- Maintenance/routing cost: no new router edge/reference; one less competing ontology description.
- Status: ADOPTED for Phase C candidate.

## P2 — Worker assignment ownership

- Baseline/current owner: `skill/references/worker-protocol.md` §1; persisted assignment identity remains `task-contract.md` §8.
- Selected evidence: #54 / PR #55; prototype `worker-assignment-owner-dedup-v1`.
- Representation: concise ordered pre-edit verification procedure consuming the already-loaded Task Contract assignment envelope.
- Protected meaning: immutable StartHEAD generation anchor; CheckpointHEAD correction guard; stale assignment behavior; Worker target separation; Authority/profile non-upgrade; Dispatch/Handoff schemas unchanged.
- Benefit: removes duplicate persisted field ontology across references that Worker entry loads together.
- Maintenance/routing cost: no new reference; canonical persisted owner becomes clearer.
- Status: ADOPTED for Phase C candidate.

## P3 — pending external-job continuation

- Baseline/current owner: `skill/references/master-cycle.md` §9 pending-job paragraph.
- Selected evidence: #56 / PR #57; prototype `pending-job-decision-structure-v1`.
- Representation: one local condition/action decision structure.
- Protected meaning: pending != failure; independent work first; sole-dependency continuation; synchronous rechecks and event/condition resume are alternatives without invented precedence; immediate success continuation; immediate failure classification/remediation; bounded BLOCKED condition; anti-spin; DeliveryState/NO_READY_WORK namespace guards.
- Benefit: exposes real branching and precedence locally instead of requiring extraction from dense prose.
- Maintenance/routing cost: same owner, no new state/router; table row semantics must remain branch conditions rather than pseudo-state transitions.
- Status: ADOPTED for Phase C candidate.

## P4 — `WriteState.UNKNOWN`

- Baseline/current owner: `skill/references/authority-gates.md` §6.
- Selected evidence: #58 / PR #59; prototype `write-unknown-canonical-algorithm-v1`.
- Representation: one guarded ordered algorithm; remove duplicate symbolic flow.
- Protected meaning: local UNKNOWN; no blind retry/automatic Master stop; decision-scoped authoritative reread; present vs proven absent vs incomplete/unknown; one safe idempotent/correlated retry; incomplete != absence; dependent mutation freeze + independent work; terminal WRITE_OUTCOME_UNKNOWN only when sole/project-wide controlling blocker.
- Benefit: one canonical algorithm owns safety-critical branches; removes shorthand that duplicates and compresses fragile distinctions.
- Maintenance/routing cost: no new abstraction or hop; slightly more explicit branch labels inside one existing owner.
- Status: ADOPTED for Phase C candidate.

## P5 — progressive cold recovery

- Baseline/current owner: `skill/references/continuity.md` §2 overlapping recovery prefix.
- Selected evidence: #60 / PR #61; prototype `progressive-recovery-procedure-v1`.
- Representation: one progressive retrieval procedure with Orientation spine, Active-path context, Triggered depth.
- Protected meaning: RECOVER before consequential mutation; all prior eight-step evidence classes; Authority/Coordination recovered independently; affected Assurance/exact ScopedAuthorization; root spec only on material trigger, never merely chat loss; explicit decision-valid stop; continue valid plan; workstream narrowing; all later multi-repo/legacy/preflight/planned-transition/route-failure/material-drift rules unchanged.
- Benefit: one retrieval-depth model replaces two overlapping organizations of cold recovery.
- Maintenance/routing cost: dense table cells, mitigated by keeping conditional specialized safeguards outside the table and unchanged.
- Status: ADOPTED for Phase C candidate.

## Combined-candidate invariants

The combined materializer/test must prove before #39 handoff:

1. every selected source surface is unchanged from the exact prototype source surface before replacement;
2. only the five selected canonical files differ from Phase C base;
3. within each file, only selected ranges differ;
4. state/boundary namespaces are unchanged;
5. direct router/reference paths remain unchanged;
6. Rule/Goal maps remain valid and canonical owner uniqueness passes existing validators;
7. unconditional complete-response machine-relay copy-target behavior from v1.2.3 remains byte-identical outside P1 §1;
8. full Skill validation, equivalence, regression/eval, packaging, publisher and runtime-cleanliness checks pass on exact candidate;
9. no VERSION/CHANGELOG/release intent is introduced.

## Proof boundary

This migration claims lossless semantic ownership/locality/reconstruction improvement under the research-backed evidence model. It does not claim measured live-model latency/accuracy improvement in an uncontrolled environment. A protected regression invalidates migration regardless of structural benefit.
