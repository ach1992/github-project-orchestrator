# Refactor Migration Plan

Status: **completed historical migration record** for the v1.0.0 -> v1.1.0 refactor. Phases 0-8 are complete; `v1.1.0-rc.1` was independently reviewed and delivered. Historical stable-release readiness after that candidate was tracked in GitHub Issue #19; current release state lives in `CHANGELOG.md`, GitHub Releases, and any active release Issue rather than by reopening these phases.

The phase descriptions and exit gates below are retained as design provenance. Their imperative wording records what each phase was required to achieve; it is not a current backlog.

## Objective

Convert the v1.0.0 prose-heavy defensive specification into a low-friction, typed, event-routed decision system that is easier for an agent to execute correctly **without losing behavioral guarantees**.

The optimization target is operational usefulness, not token count. Each phase must improve one or more canonical Goal IDs while preserving traceability through `GOAL-MAP.md`, `RULE-MAP.md`, regression scenarios, and repository validation.

## Completion status

| Phase | Status | Durable outcome |
|---|---|---|
| 0 | complete | immutable `v1.0.0` baseline + installable release |
| 1 | complete | canonical Goal/Rule/state/decision traceability established without runtime change |
| 2 | complete | lossless runtime ontology + compatibility safeguards |
| 3 | complete | canonical decision predicates and rule ownership |
| 4 | complete | compact one-step role/event routing and bounded Worker context |
| 5 | complete | scale-adaptive workstream/multi-repository coordination and progressive recovery |
| 6 | complete | deterministic state/traceability/contract validation |
| 7 | complete | source-grounded operational benchmark + adversarial fixtures + live delivery evidence |
| 8 | complete | stabilized architecture, independent review, deterministic packaging/release publisher, delivered `v1.1.0-rc.1` |

## Invariants during migration

1. Tag/release `v1.0.0` remains the immutable pre-refactor baseline.
2. No runtime rule is removed merely to reduce text, files, or context size.
3. Every material semantic/runtime change identifies affected Goal IDs, Rule IDs, and evaluation scenarios before implementation.
4. Duplicate prose is removed only after canonical ownership and equivalent behavior are explicit.
5. Compatibility state is never guessed when the legacy representation is lossy.
6. Refactors do not add human confirmation to normal authorized low/medium reversible work.
7. Helpers/scripts enforce mechanical invariants only; they do not replace necessary agent judgment.
8. A new abstraction/table/graph/schema/script must reduce ambiguity, duplication, execution cost, or error probability enough to justify its maintenance/cognitive cost.
9. `SKILL.md` trends toward a compact control kernel; detailed rules remain available through direct event/role routing rather than being deleted.
10. Documentation and design artifacts stay outside `skill/` unless runtime execution genuinely needs them.

## Phase sequence

### Phase 0 - Immutable baseline

Status: complete.

Deliver:
- original runtime preserved under `skill/`;
- baseline hash manifest and repository validator;
- installable GitHub Release `v1.0.0` with `skill.zip` and SHA-256 evidence.

Purpose:
- provide rollback/reference behavior for every later refactor.

### Phase 1 - Semantic, state, and goal freeze

Status: complete.

Primary goals: all, especially `G02`, `G07`, `G10`, `G12`, `G13`, `G16`.

Deliver:
- `RULE-MAP.md`: semantic Rule IDs, proposed canonical owners, source/eval anchors;
- reproducible v1.0.0 rule-source index manifest/generator;
- `STATE-MODEL.md`: typed state, scope, lifetime, and compatibility model;
- `DECISION-GRAPHS.md`: execution, authorization, effect, boundary, and forbidden-inference relationships;
- `GOAL-MAP.md`: Goal -> Rule -> evaluation traceability and broader operational coverage gaps;
- finalized canonical project mission/goals in `docs/PROJECT-SPEC.md`;
- lightweight repository Project Map/navigation in `README.md`.

Exit gate:
- no path under `skill/` changes from v1.0.0;
- every mapped normative rule has one proposed canonical owner;
- canonical goals and their acceptance evidence are explicit;
- no known critical representation defect lacks a proposed lossless model;
- repository validation/CI passes.

### Phase 2 - Lossless runtime ontology

Status: complete.

Primary goals: `G07`, `G09`, `G10`, `G11`, `G12`.

Change representation, not policy:
- legacy `Operating Profile` -> `CoordinationBaseline + AssuranceLevel`;
- scalar action classification -> simultaneous `ApplicableEffects` set + obligation union;
- `ProjectAuthority` separate from exact `ScopedAuthorization`;
- lifecycle namespaces for task, Worker, write, delivery, and Master boundary;
- delivery requirement, target, and state separated;
- immutable Worker `StartHEAD` separate from correction/resume `CheckpointHEAD`.

Compatibility rule:
- read legacy fields only through an explicit safe compatibility path; never guess the missing LIGHTWEIGHT/STANDARD baseline from legacy `HIGH_ASSURANCE` without authoritative evidence.

Exit gate:
- all baseline eval scenarios preserve intended behavior;
- ontology-specific regressions cover orthogonal coordination/assurance/path combinations, multi-effect obligations, namespace isolation, delivery dimensions, and Worker start/checkpoint semantics;
- runtime terminology is internally consistent;
- no new approval gate or policy weakening is introduced.

### Phase 3 - Low-friction decision kernel and canonical rule ownership

Status: complete.

Primary goals: `G01`, `G02`, `G07`, `G10`, `G16`, plus the project meta-goal.

Replace repeated defensive definitions where a clearer canonical model exists:
- predicates for common execution decisions;
- gate/precedence matrices;
- state/branch graphs;
- forbidden-inference matrix;
- typed schemas for persisted identity;
- short boundary reminders outside the canonical owner.

Canonical predicates implemented include:

```text
CAN_EXECUTE(action)
MASTER_STOP(boundary, independent_work)
REVIEW_VALID(envelope)
DELIVERY_PROVEN(artifact, target, evidence)
```

Exit gate:
- every removed/reduced paragraph is traceable through Goal + Rule IDs;
- no semantic rule has competing canonical definitions;
- representative decisions require less irrelevant reasoning without weaker behavior;
- regression suite remains green.

### Phase 4 - Role/event routing and progressive loading

Status: complete.

Primary goals: `G05`, `G08`, `G09`, `G11`, `G12`, `G16`.

Make `SKILL.md` a compact control kernel:
- resolve Role and universal state/authority model;
- run the Master control loop;
- route to domain references only when the corresponding event becomes decision-relevant;
- keep Worker context bounded to its Task Contract and targeted repository instructions;
- avoid evaluating release, rotation, delegation, or governance logic continuously when irrelevant.

Target event families:
- first ownership / governance readiness;
- consequential mutation;
- delegation / Worker correction;
- review / integration;
- production / release / incident;
- recovery / Master replacement;
- terminal decision;
- modification of this Skill.

Exit gate:
- required rules remain reachable from `SKILL.md` in one routing step;
- no important behavior depends on deep reference chains or implicit chat memory;
- bounded implementation reaches useful action with lower decision/context overhead.

### Phase 5 - Scalable coordination and lean project knowledge

Status: complete.

Primary goals: `G03`, `G04`, `G06`, `G08`, `G12`, `G13`, `G14`, `G15`.

Strengthen behaviors that are present in v1.0.0 but need explicit operational coverage:
- continuous/event-driven plan validity and project-health reassessment;
- architecture and engineering-system fitness correction when accepted work or evidence-backed material net value justifies it;
- component/workstream ownership boundaries for large projects;
- multi-repository dependency/release coherence without duplicate central backlog;
- bounded cold-recovery cost;
- information-entropy control: stale/duplicate project artifacts are reconciled instead of accumulating;
- Project Map/navigation remains an index of authoritative truth, not a status database.

Exit gate:
- small projects stay lightweight;
- medium projects retain sufficient durable coordination;
- large/multi-repository synthetic projects recover and navigate progressively without giant Master context;
- recovery and project-system improvements do not create manager-memory archives or documentation bloat.

### Phase 6 - Mechanical enforcement

Status: complete.

Primary goals: `G07`, `G09`, `G10`, `G12`, `G13`, `G14`.

Add deterministic lint/checks only where code is more reliable than prose:
- unknown/legacy state tokens and invalid enum/schema combinations;
- duplicate canonical Rule owners and orphan Rule IDs;
- Goal/Rule/eval traceability integrity where mechanically expressible;
- broken runtime references and routing targets;
- eval ID gaps/duplicates;
- Worker contract/assignment identity invariants;
- release package cleanliness and version/baseline rules.

Exit gate:
- deterministic failures are caught before runtime packaging;
- linter output is specific/actionable;
- scripts remain optional runtime accelerators unless a runtime capability explicitly depends on them;
- no subjective engineering judgment is accidentally encoded as a brittle mechanical gate.

### Phase 7 - Operational benchmarks and adversarial evaluation

Status: complete.

Primary goals: all; especially the meta-goal, `G01`, `G08`, `G12`, `G13`, `G16`.

Compare baseline and refactored versions on fixed scenarios plus representative small, medium, large, recovery, delegation, review, and release projects.

Primary metrics:
- verified task/outcome completion rate;
- wrong/premature Master stop rate;
- unnecessary human confirmation rate;
- duplicate/ambiguous mutation rate;
- stale review/integration rate;
- Worker redispatch/churn caused by state confusion;
- unnecessary project artifact creation;
- decision/tool steps before first useful engineering action;
- repeated discovery/recovery work;
- cold-recovery correctness and navigation cost;
- unnecessary context/rule activation;
- correct release/delivery verification.

Token count remains diagnostic, not the primary success metric.

Exit gate:
- no material regression against v1.0.0 behavioral guarantees;
- refactored runtime demonstrates lower friction on representative work, not just fewer lines;
- new canonical goals have operational acceptance evidence.

### Phase 8 - Architecture stabilization and release candidate

Status: complete; delivered as `v1.1.0-rc.1` after independent review and post-release verification.

Primary goals: all.

Deliver:
- final canonical runtime ownership/routing structure;
- stale compatibility scaffolding removed only when migration evidence permits;
- documentation reconciled to actual runtime architecture;
- full regression/lint/package validation;
- independent review of rule preservation, safety, usability, recovery, and release behavior;
- versioned release candidate followed by normal release verification.

Exit gate:
- project-level definition of done in `docs/PROJECT-SPEC.md` is satisfied;
- release artifact is tied to the reviewed commit and published with checksum;
- next Master can support/extend the Skill from repository state without chat history.

## Change acceptance template

Future substantial runtime changes should still be able to state:

```text
Goal IDs improved:
Rule IDs affected:
Representation/mechanism changed:
Expected friction/correctness benefit:
Regression/operational evidence:
```

If those fields cannot be answered concretely, the change is not ready merely because it appears cleaner.
