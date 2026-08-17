# Refactor Migration Plan

## Objective

Convert the v1.0.0 prose-heavy defensive specification into a typed, event-routed decision model without losing behavioral guarantees.

## Invariants during migration

1. Tag `v1.0.0` remains the immutable pre-refactor baseline.
2. Phase 1 changes only development artifacts outside `skill/`.
3. Every semantic change in later phases must identify affected Rule IDs and eval scenarios before changing runtime text.
4. Duplicate prose may be removed only after canonical ownership is explicit.
5. Compatibility state must not be silently inferred when the legacy representation is lossy.
6. Refactors must not add human confirmation to normal authorized low/medium reversible work.
7. Helpers remain optional unless the runtime explicitly has the capability and the helper materially improves deterministic execution.

## Phase sequence

### Phase 1 - Semantic freeze and model

Deliver:
- reproducible `RULE-SOURCES-v1.0.0.tsv`: exhaustive non-empty line index generated on demand, with expected digest/count locked in `RULE-SOURCES-v1.0.0.manifest`;
- `RULE-MAP.md`: semantic Rule IDs, proposed canonical owners, source/eval anchors;
- `STATE-MODEL.md`: typed state, scope, lifetime, and compatibility model;
- `DECISION-GRAPHS.md`: execution, authorization, effect, boundary, and inference relationships.

Exit gate:
- `python3 tools/validate_skill.py skill` passes;
- `skill/` remains byte-identical to the v1.0.0 baseline manifest;
- no known critical representation defect lacks a proposed lossless model.

### Phase 2 - Ontology normalization

Change runtime representation, not policy:
- `Operating Profile` -> `CoordinationBaseline + AssuranceLevel`;
- scalar action classification -> `ApplicableEffects` set + obligation union;
- `ProjectAuthority` separate from `ScopedAuthorization`;
- lifecycle namespaces for task/Worker/write/delivery/Master boundary;
- delivery requirement/target/state separation;
- `StartHEAD` separate from correction `CheckpointHEAD`.

Compatibility rule:
- persist or read legacy fields only through an explicit adapter; never guess the missing STANDARD/LIGHTWEIGHT baseline from legacy `HIGH_ASSURANCE` without authoritative evidence.

Exit gate:
- all existing eval scenarios preserve intended behavior;
- new regression scenarios cover `STANDARD + FAST`, `STANDARD + HIGH_ASSURANCE` persistence, multi-effect actions, namespace isolation, and delivery state/target separation.

### Phase 3 - Decision-kernel compression

Replace repeated definitions with:
- canonical predicates;
- decision matrices;
- state/branch graphs;
- forbidden-inference matrix;
- short boundary reminders at phase-specific files.

Candidate predicates:

```text
CAN_EXECUTE(action)
MASTER_STOP(boundary, independent_work)
REVIEW_VALID(envelope)
DELIVERY_PROVEN(artifact, environment, evidence)
```

Exit gate:
- every removed paragraph is traceable through Rule IDs;
- no canonical rule has multiple definition owners;
- routing is simpler without weakening edge-case behavior.

### Phase 4 - Role/event routing

Make `SKILL.md` a small control kernel:
- resolve Role;
- load universal state/authority model;
- dispatch Master vs Worker path;
- activate event-specific proof obligations only when relevant.

Examples:
- Worker does not need Master prioritization/release strategy unless a boundary requires relay.
- routine implementation does not continuously evaluate rotation rules;
- release rules activate when deterministic delivery/production effects enter the action frontier.

### Phase 5 - Mechanical enforcement

Add deterministic lint/checks for representation invariants where code is more reliable than prose:
- unknown/legacy state tokens;
- duplicate canonical Rule owners;
- unmapped/superseded Rule IDs;
- broken references;
- eval ID gaps/duplicates;
- Worker contract schema invariants;
- release package cleanliness.

### Phase 6 - Operational benchmark

Compare baseline and refactored versions on fixed scenarios and representative repositories.

Primary metrics:
- wrong/premature Master stop rate;
- unnecessary human confirmation rate;
- duplicate/ambiguous mutation rate;
- stale review/integration rate;
- Worker redispatch/churn caused by state confusion;
- unnecessary project artifact creation;
- number of decision/tool steps before first useful engineering action;
- recovery correctness after Master replacement.

Token count is diagnostic, not the primary success metric.
