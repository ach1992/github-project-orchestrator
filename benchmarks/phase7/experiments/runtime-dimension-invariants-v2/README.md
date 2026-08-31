# Runtime Dimension Invariants v2

Tracking: #35 -> #37 -> #50 -> #52

Status: isolated representation prototype; **not canonical runtime**.

## Hypothesis

The current runtime already has the right six dimensions and the right semantics. The opportunity is representation locality, not policy change:

- `SKILL.md` declares the dimension ontology, then carries important stability/non-implication semantics in two separate prose paragraphs;
- `authority-gates.md`, which is loaded after the kernel for consequential actions, repeats the dimension ontology before applying gate-specific behavior;
- frozen PR #43 makes carry-forward more explicit but adds a second named decision-frame block instead of consolidating the existing owner.

This prototype replaces rather than layers:

1. `SKILL.md` §1 becomes one dimension matrix whose third column holds the stability/non-implication property of the dimension it belongs to;
2. `authority-gates.md` §1 becomes a short bridge from the already-active kernel dimensions to gate-specific evaluation and retains only semantics that are actually gate-local.

No new state, lifecycle, Rule ID, cache, persistent artifact, authorization shortcut, or routing edge is introduced.

## Frozen identities

- prototype source/current-target snapshot: `9e584166008567d71591d2a03bf7da713d3664a4`;
- immutable semantic comparison baseline: `f98e8a242c720931e34aa7c4e8a799090e3d0495` (`v1.2.2`);
- superseded exact prior representation experiment: PR #43 / `9384b371264473b291fe815b5725ae64f44d4179`;
- canonical runtime remains whatever current `main` contains; this prototype never writes `skill/`.

The source snapshot descends from the immutable semantic baseline and preserves the accepted v1.2.3 machine-relay behavior plus later repository-only benchmark/methodology changes. Future migration, if selected, must apply to then-current `main`, not this snapshot wholesale.

## One-to-one semantic ledger — `SKILL.md` §1

| Baseline semantic | Candidate location | Preservation |
|---|---|---|
| `Role` values/responsibilities | `Role` row, values/responsibility column | exact responsibility wording retained |
| Role remains stable until assignment basis changes | `Role` row, stability column | explicit `KEEP` property; no new state is created |
| `ProjectAuthority` values and end-to-end default | `ProjectAuthority` row, values/responsibility column | exact values/default retained |
| ProjectAuthority remains stable until authorization basis changes | `ProjectAuthority` row, stability column | explicit `KEEP` property |
| capability/environment/risk/coordination/assurance never broadens ProjectAuthority | `ProjectAuthority` row, stability column | co-located with the dimension the guard protects |
| chat/Master replacement does not become a more permissive Authority basis | `ProjectAuthority` row, stability column | explicit non-implication retained |
| `ScopedAuthorization` is exact action/target/effect | `ScopedAuthorization` row, values column | exact scope identity retained |
| ScopedAuthorization never becomes project-wide Authority | `ScopedAuthorization` row, stability/non-implication column | explicit guard retained |
| `CoordinationBaseline` values and LIGHTWEIGHT/STANDARD meanings | `CoordinationBaseline` row, values/responsibility column | current wording retained |
| CoordinationBaseline remains stable until coordination basis changes, including rotation | `CoordinationBaseline` row, stability column | explicit `KEEP` property |
| `STANDARD` remains compatible with FAST | `CoordinationBaseline` row, stability column | explicit compatibility retained |
| `STANDARD` never implies FULL | `CoordinationBaseline` row, stability column | explicit forbidden implication retained |
| `AssuranceLevel` values | `AssuranceLevel` row, values column | exact values retained |
| HIGH_ASSURANCE is additive and affected-work-only, justified by risk/policy/authorized control | `AssuranceLevel` row, stability column | additive scoped escalation is explicit rather than inferred |
| HIGH_ASSURANCE returns to NORMAL when escalation ends | `AssuranceLevel` row, stability column | de-escalation retained |
| HIGH_ASSURANCE never implies approval/FULL | `AssuranceLevel` row, stability column | explicit forbidden implication retained |
| `RiskLevel` values and per-change classification | `RiskLevel` row | exact values and decision-relevant per-change rule retained |
| project/repository size alone selects neither STANDARD nor HIGH_ASSURANCE | sentence immediately after matrix | retained once for both affected dimensions rather than repeated per row |
| dimensions are orthogonal unless a canonical rule connects them | sentence immediately after matrix | exact relation retained |
| infer safely instead of asking the user to choose ceremony | sentence immediately after matrix | behavior retained with equivalent wording |
| consequential-action canonical owner is `authority-gates.md` | final §1 paragraph | exact routing/ownership reminder retained |

## One-to-one semantic ledger — `authority-gates.md` §1

| Baseline semantic | Candidate location | Preservation / ownership reason |
|---|---|---|
| Role/Authority/ScopedAuthorization/Coordination/Assurance/Risk are independent decision inputs | first paragraph | references the already-active kernel ontology instead of re-declaring values |
| technical capability/environment remain independent execution constraints rather than Authority | kernel `ProjectAuthority` row + first paragraph | gate bridge explicitly preserves these as separate constraints while the kernel owns the no-upgrade rule |
| repository/platform permissions still apply | second paragraph | retained verbatim in meaning |
| explicit user/higher-level authorization changes only what it clearly grants | second paragraph | retained |
| one-off exact instruction/approval is ScopedAuthorization, not project-wide Authority | second paragraph | retained |
| ScopedAuthorization may authorize or satisfy only its bounded applicable gate/action where the canonical matrix permits | second paragraph | both authorization and gate-satisfaction effects are explicit without broadening project-wide Authority |
| use lightest safe controls | third paragraph | retained |
| importance alone does not make risk high | third paragraph | retained |
| risk classification considers blast radius, reversibility, security/data, compatibility, production | third paragraph | retained |
| STANDARD does not imply FULL | kernel `CoordinationBaseline` row | removed only as duplicate ontology; kernel is always active before this reference |
| HIGH_ASSURANCE does not imply human approval or different Authority | kernel `AssuranceLevel` + `ProjectAuthority` rows | removed only as duplicate ontology; detailed gate effects remain in later authority-gates sections |

No gate-matrix row, `ApplicableEffects` meaning, obligation-union rule, `CAN_EXECUTE`, action-classification flow, edge case, ScopedAuthorization validity rule, MasterBoundary, WriteState, concurrency, or human-operation rule is changed by this experiment.

## Self-review corrections before selection

The first prototype draft exposed two small but material semantic edges during one-to-one review, and both were corrected before any migration decision:

1. `AssuranceLevel` now states explicitly that `HIGH_ASSURANCE` is **additive**, not merely affected-work scoped. This protects the existing rule that stronger assurance never replaces the underlying coordination/control baseline.
2. the gate bridge now preserves technical capability/environment as separate execution constraints and explicitly preserves both bounded ScopedAuthorization effects: it may **authorize** the exact action or **satisfy** its applicable gate where the canonical matrix permits.

These corrections are evidence that the ledger is serving its intended purpose: representation compression is rejected or revised whenever a small baseline implication is lost.

## Structural diagnostics — not acceptance proof

Using whitespace-delimited word counts on the two replaced source sections:

| Surface | Baseline | Candidate |
|---|---:|---:|
| `SKILL.md` §1 | 255 | 255 |
| `authority-gates.md` §1 | 232 | 135 |
| combined when authority gates is activated | 487 | 390 |

Interpretation:

- the always-active kernel is **not enlarged by word count**;
- the consequential-action path removes roughly one fifth of the words in these two sections because the specialist no longer repeats the ontology;
- these counts are diagnostics only. The candidate is acceptable only if the semantic ledger, mechanical isolation, eval protection, and source-grounded operational analysis remain lossless.

## Why this is different from PR #43

PR #43 correctly identified repeated stable-state reconstruction as a problem hypothesis. Its exact representation adds:

- a new `Reuse still-valid runtime state` subheading;
- explanatory prose describing a transient decision frame;
- a second three-row carry-forward table;
- another prose paragraph for related dimension rules.

That additive form makes the hot kernel longer and introduces a named abstraction that is not a real lifecycle/persisted state. This v2 prototype keeps the useful idea (`KEEP` until basis changes) but places it as a property of the existing dimension in the existing owner. Therefore the exact #43 representation is classified **REVISE / superseded by this prototype**, not selected for migration.

## Protected evaluation surface

At minimum this prototype must preserve:

- `AUTHORITY-STABLE`;
- `COORDINATION-BASELINE`;
- `ASSURANCE-ADDITIVE`;
- `DIMENSIONS-ORTHOGONAL`;
- `FAST-FULL-SELECT`;
- evals `AD`, `AH`, `CZ`, `BG`, `BH`, `CU`, `CX`;
- all direct `SKILL.md` runtime routes;
- all existing state namespaces/tokens and canonical predicates;
- all unrelated source-snapshot runtime bytes;
- accepted v1.2.3 relay behavior because no relay surface is modified.

## Selection boundary

This prototype can be selected for #38 only after:

1. mechanical isolation/equivalence checks pass;
2. this one-to-one ledger survives semantic review;
3. source-grounded walkthroughs show identical decisions and a real locality/reconstruction improvement;
4. maintenance/routing complexity does not increase materially.

No live model/API trial is required by the current #35/#37 contract. If trustworthy controlled model evidence exists later, it may corroborate but cannot override a protected regression.
