# Source-Grounded Operational Analysis

Experiment: `runtime-dimension-invariants-v2`
Tracking: #52

This analysis compares **representation application**, not private model reasoning. It does not fabricate model traces. For each existing protected scenario, it identifies the canonical input, required decision, baseline location of the relevant rule, candidate location, and structural difference.

## 1. Repeated bounded Master FAST work

Input shape:

- `Role=MASTER` already established;
- `ProjectAuthority=AUTONOMOUS_WITH_GATES` already established;
- `CoordinationBaseline=STANDARD` already established;
- `AssuranceLevel=NORMAL`;
- localized reversible MEDIUM change with clear acceptance/tests.

Protected decision:

- keep the established Role/Authority/Coordination values because their bases did not change;
- `STANDARD` does not force FULL;
- bounded work may use FAST when canonical FAST criteria fit.

Baseline application:

- dimension values are in the §1 table;
- orthogonality and `STANDARD`/FAST non-implication are in the first prose paragraph;
- stable carry-forward is in the next prose paragraph;
- FAST criteria remain in `master-cycle.md`.

Candidate application:

- the `CoordinationBaseline` row directly says `KEEP` until coordination basis changes and `STANDARD` remains FAST-compatible / does not imply FULL;
- Role and Authority rows directly carry their own KEEP conditions;
- FAST criteria remain in the same canonical `master-cycle.md` owner.

Decision result: **identical**.

Structural difference: stable-state and false-FULL rules are adjacent to the active dimension instead of reconstructed across the dimension table + two prose paragraphs. No second decision-frame abstraction is introduced.

Protected anchors: `AD`, `CZ`, `FAST-FULL-SELECT`, `COORDINATION-BASELINE`.

## 2. Zero-chat Master recovery

Input shape:

- replacement Master / zero chat;
- persisted `ProjectAuthority=MANAGED` or `AUTONOMOUS_WITH_GATES` is current;
- persisted `CoordinationBaseline=STANDARD` is current;
- HIGH_ASSURANCE may apply only to one affected chain.

Protected decision:

- recover and carry the current Authority and Coordination independently;
- chat loss/rotation alone never widens Authority;
- HIGH_ASSURANCE remains separate from CoordinationBaseline and returns to NORMAL outside the affected chain.

Baseline application:

- the stable/carry-forward paragraph in `SKILL.md` carries Role/Authority/Coordination and explicitly warns about Master rotation;
- `continuity.md` supplies the recovery sequence and again warns not to reconstruct Coordination from Assurance/risk/size/access.

Candidate application:

- `ProjectAuthority` row states KEEP-until-authorization-change and chat/Master rotation cannot make it more permissive;
- `CoordinationBaseline` row states KEEP-until-coordination-change including rotation;
- `AssuranceLevel` row states affected-work scope + return to NORMAL;
- `continuity.md` remains unchanged as the cold recovery owner.

Decision result: **identical**.

Structural difference: the orientation-state preservation needed before entering `continuity.md` is represented as a property of each current dimension, while detailed recovery procedure remains in the recovery domain.

Protected anchors: `AH`, `BG`, `BH`, `AUTHORITY-STABLE`, `ASSURANCE-ADDITIVE`.

## 3. Technical capability increases without Authority change

Input shape:

- repository/tool access becomes broader;
- no user or higher-level authorization changes the project-wide Authority.

Protected decision:

- capability may change what is technically possible but must not upgrade `ProjectAuthority`.

Baseline application:

- the §1 prose says technical capability/environment/risk/coordination/assurance never broadens ProjectAuthority;
- `authority-gates.md` repeats the same no-upgrade relationship before the gate model.

Candidate application:

- the `ProjectAuthority` row contains the no-upgrade guard next to the authority value;
- `authority-gates.md` consumes current dimensions and explicitly says it does not reclassify them.

Decision result: **identical**.

Structural difference: one always-active canonical ontology rule replaces two active restatements on consequential actions. Gate-specific logic still owns whether capability is required by `CAN_EXECUTE`.

Protected anchors: `CU`, `AUTHORITY-STABLE`, `DIMENSIONS-ORTHOGONAL`.

## 4. STANDARD coordination on bounded FAST work

Input shape:

- `CoordinationBaseline=STANDARD` because the broader project is coordinated;
- current bounded task independently satisfies FAST criteria.

Protected decision:

- keep STANDARD;
- choose FAST for the bounded task when canonical FAST conditions fit;
- do not create a FULL contract merely from STANDARD.

Baseline application:

- §1 prose says STANDARD remains compatible with FAST;
- `master-cycle.md` FAST/FULL section repeats the same false implication in the local execution-path domain.

Candidate application:

- `CoordinationBaseline` row makes `STANDARD` FAST-compatibility and no-FULL implication local to the dimension;
- `master-cycle.md` remains unchanged because the local FAST/FULL matrix is the actual execution-path decision owner.

Decision result: **identical**.

Structural difference: the kernel no longer requires mapping a dimension table row to a separate prose non-implication. The specialist retains its decision-local reminder because it directly protects FAST/FULL selection rather than redeclaring the dimension ontology.

Protected anchors: `CZ`, `FAST-FULL-SELECT`, `COORDINATION-BASELINE`.

## 5. HIGH_ASSURANCE on bounded work

Input shape:

- an affected bounded task is explicitly/risk-justifiably `HIGH_ASSURANCE`;
- current CoordinationBaseline remains independently valid;
- no separate action gate requires human confirmation.

Protected decision:

- add stronger assurance evidence/review only to affected work;
- do not infer FULL, persistence, human approval, or broader Authority solely from HIGH_ASSURANCE;
- return unrelated/later work to NORMAL when escalation ends.

Baseline application:

- Assurance row says additive for affected work;
- §1 prose says HIGH_ASSURANCE does not imply approval/FULL and returns to NORMAL;
- specialist references repeat the particular no-FULL/no-approval relation where it drives execution/gates.

Candidate application:

- `AssuranceLevel` row co-locates affected-work scope, justification, de-escalation, and no-approval/no-FULL implication;
- execution/gate specialists remain unchanged where their local decision uses the rule.

Decision result: **identical**.

Structural difference: the dimension's lifecycle/non-implication no longer requires joining the table row with two separate prose locations; specialist reminders are retained only where they drive a distinct downstream decision.

Protected anchors: `ASSURANCE-ADDITIVE`, `CF`, `BP`, `CE` (broader regression protection) and #52 minimum anchor set.

## 6. Scoped one-off approval

Input shape:

- project-wide Authority remains unchanged;
- user gives one exact instruction/approval for one action/target/effect.

Protected decision:

- represent it as exact `ScopedAuthorization`;
- it may satisfy only the applicable gate where allowed;
- it never upgrades project-wide Authority.

Baseline application:

- kernel ScopedAuthorization row carries exact-grant/no-upgrade semantics;
- `authority-gates.md` repeats exact-grant/no-upgrade and explains gate substitution.

Candidate application:

- kernel row keeps exact-grant/no-upgrade ontology;
- authority bridge keeps the gate-local rule: one-off approval may satisfy only the applicable gate without converting broader Authority.

Decision result: **identical**.

Structural difference: the ontology and gate effect are separated by owner instead of both owners repeating the whole concept.

Protected anchors: `CX`, `CV`, `AUTHORITY-STABLE`.

## Net operational assessment

The candidate does **not** claim fewer hidden reasoning steps or better model accuracy from a synthetic trace. The supported claim is narrower and structural:

1. stable/non-implication semantics become local properties of the dimensions they govern;
2. the kernel word count for the replaced section does not increase;
3. when `authority-gates.md` is activated, the specialist no longer re-declares the six-value ontology and repeated non-implications;
4. gate-specific semantics remain in the gate owner;
5. every protected decision above is unchanged;
6. no new reference hop, state, Rule ID, schema, router edge, or persistent artifact is introduced.

This is sufficient to keep the prototype eligible for Phase B selection review under the revised #35/#37 evidence model. It is not by itself authorization to migrate canonical runtime; #38/#39 remain the migration and final assurance boundaries.
