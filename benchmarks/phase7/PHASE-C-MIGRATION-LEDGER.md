# Phase C Lossless Runtime Migration Ledger

Tracking: #35 -> #37/#50 -> #38  
Phase C base: `0165bc2a26bdf7452f05160c3e91f47b4fa7ae9c`  
Immutable semantic comparison baseline: `f98e8a242c720931e34aa7c4e8a799090e3d0495` (`v1.2.2`)  
Public pre-optimization checkpoint: `v1.2.3@ff7b23a25aac9721d515dbfd03c5b2546749a89d`

This is evidence, not a second normative runtime owner. Canonical behavior remains in `skill/`. The migration applies only the five representation families selected by completed Phase B research/audit. No live model/API A/B performance claim is made or required by the current contract.

## Selection principle

The optimization target is **semantic application cost**, not prose aesthetics, token count, or universal conversion to a structured format. A representation is changed only when its semantic shape, activation locality, fragility, canonical ownership, retrieval/inference cost, and maintenance cost support a better fit than `KEEP`.

| Family | Baseline owner / semantic | Selected prototype | Canonical migrated representation | Representation rationale | Equivalence / protection | Source-grounded benefit | Maintenance / routing cost | Status |
|---|---|---|---|---|---|---|---|---|
| P1 | `skill/SKILL.md` §1 dimension ontology/stability plus `authority-gates.md` §1 gate-consumer restatement | #52/#53 `runtime-dimension-invariants-v2` | one kernel dimension matrix with local stability/non-implication properties + short gate-consumer bridge | fixed orthogonal dimensions fit a matrix; stability guards belong beside the dimension; gate owner should consume rather than redeclare ontology | exact selected fragments; `DIMENSIONS-ORTHOGONAL`, `AUTHORITY-STABLE`, `COORDINATION-BASELINE`, `ASSURANCE-ADDITIVE`, FAST compatibility; no state/frame/cache | removes cross-paragraph reconstruction and duplicate specialist ontology while retaining one-hop routing | no new file/hop/runtime state; table remains compact | migrated |
| P2 | `worker-protocol.md` §1 repeats persisted assignment fields already canonical in `task-contract.md` §8 while also defining Worker pre-edit behavior | #54/#55 `worker-assignment-owner-dedup-v1` | persisted schema remains in Task Contract; Worker §1 becomes ordered verification procedure | schema identity and ordered pre-edit checks are different semantic shapes; keep one schema owner and one behavior owner | exact selected fragment; StartHEAD historical semantics, CheckpointHEAD correction guard, staleness and target separation preserved; §2+ unchanged | avoids reconciling two normative field enumerations in always-co-loaded context | no new reference hop because Worker entry already requires both owners | migrated |
| P3 | `master-cycle.md` §9 pending external-job policy encoded as one dense branching paragraph | #56/#57 `pending-job-decision-structure-v1` | principle sentence + condition/action decision table + anti-spin/namespace guard | genuine branching/precedence over observable conditions fits a decision table better than dense prose | exact selected fragment; independent-work-first, alternative continuation mechanisms, success/failure, BLOCKED condition and namespace guards preserved | branch conditions and actions become adjacent; no invented precedence between synchronous rechecks and event/condition resume | one local table; no new state/router/file | migrated |
| P4 | `authority-gates.md` §6 represents one recovery algorithm twice: symbolic flow then numbered procedure | #58/#59 `write-unknown-canonical-algorithm-v1` | one guarded numbered algorithm with explicit present/proven-absent/incomplete branches | ordered safety-critical algorithm fits one canonical procedure; duplicate shorthand adds reconciliation risk and hides branch distinctions | exact selected fragment; no blind retry, proof-of-absence gate, one safe retry, local freeze, independent continuation, terminal boundary condition preserved | removes duplicate ownership and makes the forbidden `incomplete != absent` inference local to its branch | simpler single owner; no new abstraction/state | migrated |
| P5 | `continuity.md` §2 duplicates recovery as an eight-step list plus a three-layer progressive model | #60/#61 `progressive-recovery-procedure-v1` | one Orientation -> Active-path -> Triggered-depth progressive procedure | progressive retrieval is the real semantic; layered table expresses activation locality directly | exact selected fragment; root-spec trigger, independent Authority/Coordination recovery, decision-valid stop and all later recovery safeguards preserved | reduces repeated recovery reconstruction and makes stopping condition/locality explicit | later multi-repo/delta/preflight/legacy safeguards remain unchanged | migrated |

## Composition safeguards

`tests/test_phase_c_runtime_migration.py` verifies the five canonical fragments equal the exact selected Phase B candidates and that bytes outside each selected surface remain equal to Phase C base. It also protects the accepted v1.2.3 machine-relay complete-response copy-target rule.

The existing runtime equivalence, eval/adversarial, package, runtime-cleanliness, prototype-isolation and repository validation suites remain independently required. Prototype evidence is not treated as proof that composition is safe; exact-candidate CI and semantic diff review are still required.

## Explicit non-goals

- no wholesale `SKILL.md` rewrite;
- no universal prose -> table/JSON/XML conversion;
- no new rule, lifecycle state, decision cache/frame, authority shortcut, router edge, or persistence mechanism;
- no migration of frozen/superseded PR #43 representation;
- no version or release publication;
- no fabricated live-model performance claim.

## Final status boundary

Migration implementation may be selected only if exact-candidate validation remains green and final fresh independent HIGH_ASSURANCE review finds no `BLOCKER`/`REQUIRED` semantic loss, new implication, routing regression, or maintenance cost that erases the representation benefit. Final HIGH-risk integration remains a separate human approval gate.
