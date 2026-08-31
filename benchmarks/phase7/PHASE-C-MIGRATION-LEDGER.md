# Phase C Lossless Runtime Migration Ledger

Tracking: #35 -> #37/#50 -> #38  
Phase C base: `0165bc2a26bdf7452f05160c3e91f47b4fa7ae9c`  
Immutable semantic comparison baseline: `f98e8a242c720931e34aa7c4e8a799090e3d0495` (`v1.2.2`)  
Public pre-optimization checkpoint: `v1.2.3@ff7b23a25aac9721d515dbfd03c5b2546749a89d`

This is evidence, not a second normative runtime owner. Canonical behavior remains in `skill/`. The migration is limited to the five representation families selected by Phase B research/audit. No live model/API A/B performance claim is made or required by the current contract.

## Selection principle

The optimization target is **semantic application cost**, not prose aesthetics, token count, or universal conversion to a structured format. A representation changes only when semantic shape, activation locality, fragility, canonical ownership, retrieval/inference cost, and maintenance cost support a better fit than `KEEP`.

A green mechanical composition test is necessary but not sufficient. Phase C therefore adds a clause-level authoring-side semantic audit before independent review: each baseline clause is decomposed by purpose/condition/exception/ownership, mapped to the final canonical representation, checked against neighboring owners and Rule Map boundaries, and exercised against protected scenario families. A Phase B prototype may be refined in Phase C when this deeper audit finds an ambiguity or representation defect; the selected **concept** remains the scope boundary, not the prototype wording.

## Self-audit correction boundary

The first exact Phase C candidate `2f36f3287629c1de71255c29ed04a6bef012b834` passed its exact-composition CI but was withdrawn **before independent review**. Deeper semantic/representation review found issues that byte-equivalence-to-prototype could not detect:

- P1 needed canonical authority ownership and baseline-control wording made explicit without restoring the duplicate six-row ontology;
- P2 had weakened `known worktree state` into generic worktree `safety` and had unnecessarily shortened the worktree-isolation criterion;
- P3 used overlapping table predicates that could require the model to infer precedence rather than read it directly;
- P5 preserved most meaning but encoded a progressive/conditionally widening procedure as a table with long mixed-purpose cells, contrary to the repository's own representation-fit rule;
- P4 survived the deeper review unchanged.

The withdrawn SHA is historical evidence only and must not be reviewed or integrated.

## Final-family disposition after clause-level self-audit

| Family | Baseline semantic shape | Phase B selected concept | Phase C final representation | Self-audit disposition | Why final form is preferable to baseline |
|---|---|---|---|---|---|
| P1 | six fixed runtime dimensions + stability/non-implication rules + gate-local authorization semantics | localize stability/non-implication beside dimensions and deduplicate gate ontology | three-column kernel dimension matrix plus concise canonical authorization/gate bridge | **REFINED / KEEP CONCEPT** | fixed dimensions remain matrix-shaped; stable-state and false-inference rules are local; `authority-gates.md` remains canonical for authorization interpretation instead of becoming a second full ontology |
| P2 | persisted assignment schema mixed with Worker pre-edit procedure | one schema owner + one Worker verification owner | `task-contract.md` §8 remains schema owner; Worker §1 is ordered pre-edit verification with explicit worktree state/safety | **REFINED / KEEP CONCEPT** | removes competing field enumeration while preserving every pre-edit concurrency/isolation check locally |
| P3 | dense branching pending-job paragraph | condition -> action decision structure | principle + discriminated condition/action table + namespace/anti-spin guard | **REFINED / KEEP CONCEPT** | branch predicates now encode independent-work precedence and safe-continuation versus terminal-blocked distinction rather than depending on row overlap or prose reconstruction |
| P4 | one safety-critical recovery algorithm represented twice | one guarded canonical algorithm | one six-step present/proven-absent/incomplete algorithm | **KEEP EXACT P4** | eliminates duplicate symbolic shorthand and makes the dangerous `incomplete != absent` rule local to its branch |
| P5 | eight-step recovery checklist plus overlapping three-layer progressive retrieval model | one progressive recovery procedure | Orientation + Active-path normal progression with Triggered-depth as an explicit conditional side path | **REFINED / KEEP CONCEPT** | removes two competing organizations without forcing a long-cell table or falsely making Triggered depth a mandatory third phase |

## P1 — runtime dimensions and authority ownership

### Baseline semantic atoms -> final canonical locations

| Baseline meaning / purpose | Final owner/location | Lossless check / ambiguity guard |
|---|---|---|
| `Role` MASTER/WORKER responsibilities | `SKILL.md` Role row | responsibility wording retained; Role retains until actual assignment basis changes |
| ProjectAuthority values + end-to-end default | `SKILL.md` ProjectAuthority row | values/default unchanged |
| Role stability until assignment changes | `SKILL.md` Role stability cell | explicit retain rule; no `KEEP` pseudo-state/token introduced |
| ProjectAuthority stability until authorization basis changes | `SKILL.md` ProjectAuthority stability cell + canonical authorization interpretation in `authority-gates.md` §1 | kernel gives local carry-forward reminder; gate owner defines applicable explicit user/higher-level authorization change |
| capability/environment/risk/coordination/assurance may constrain but never broaden Authority | `SKILL.md` ProjectAuthority cell + `authority-gates.md` §1 | both local pre-gate non-inference and canonical gate-domain authorization meaning preserved |
| chat/Master rotation cannot make Authority more permissive | `SKILL.md` ProjectAuthority cell | explicit; protects AH/CU and zero-chat recovery |
| ScopedAuthorization is exact action/target/effect and never project-wide upgrade | `SKILL.md` ScopedAuthorization row | exact scope identity retained |
| ScopedAuthorization may authorize exact action or satisfy only its applicable gate when matrix permits | `authority-gates.md` §1 | separates action authorization from gate satisfaction; no blanket gate waiver |
| CoordinationBaseline LIGHTWEIGHT/STANDARD meanings | `SKILL.md` Coordination row | value definitions retained |
| CoordinationBaseline remains stable until coordination basis changes, including rotation | `SKILL.md` Coordination stability cell | explicit carry-forward; no downgrade/upgrade from chat loss |
| STANDARD remains FAST-compatible and does not imply FULL | `SKILL.md` Coordination row + concise gate reminder | false implication remains local and gate-safe |
| Coordination affects coordination/persistence controls | `authority-gates.md` §1 gate-consumer bridge | old effect meaning retained without redeclaring value ontology |
| Assurance NORMAL/HIGH_ASSURANCE; additive only for affected work when justified | `SKILL.md` Assurance row | baseline wording retained |
| HIGH_ASSURANCE returns to NORMAL after escalation | `SKILL.md` Assurance stability cell | explicit de-escalation retained |
| HIGH_ASSURANCE never removes baseline controls | `SKILL.md` Assurance cell + `authority-gates.md` §1 | made explicit; avoids treating assurance as replacement profile |
| HIGH_ASSURANCE does not by itself imply approval or FULL/different Authority | `SKILL.md` Assurance cell + gate bridge | `by itself` retained so separately applicable risk/effect gates are not accidentally prohibited |
| RiskLevel values and per-substantive-change decision relevance | `SKILL.md` Risk row | unchanged meaning; no project-wide risk default |
| Risk determines proportional gate/evidence depth for the specific change | `authority-gates.md` §1 | old gate-domain effect retained |
| dimensions are orthogonal unless explicit canonical rule connects them | sentence after matrix | retained |
| project/repository size alone selects neither STANDARD nor HIGH_ASSURANCE | sentence after matrix | retained |
| infer safely rather than asking user to choose ceremony | sentence after matrix | retained |
| gate domain owns `CAN_EXECUTE`, effects, authorization, boundaries, unknown writes, concurrency | final §1 route | unchanged ownership route |

### P1 representation verdict

The baseline's six dimensions are genuinely fixed/comparative, so a matrix is the correct primary shape. The improvement is **locality**, not compression: dimension value + carry-forward/non-implication can be read together. The final version deliberately does **not** move canonical authorization semantics out of `authority-gates.md`; it removes the duplicate six-row ontology while retaining the gate-specific meanings that the Rule Map assigns to that domain. This is preferable to both the baseline and the withdrawn Phase B exact wording.

Protected scenario families: `AD`, `AH`, `CE`, `CF`, `CU`, `CX`, `CZ`, plus `AUTHORITY-STABLE`, `COORDINATION-BASELINE`, `ASSURANCE-ADDITIVE`, `DIMENSIONS-ORTHOGONAL`, `FAST-FULL-SELECT`.

## P2 — Worker assignment owner dedup

| Baseline meaning / purpose | Final owner/location | Lossless check / ambiguity guard |
|---|---|---|
| one Worker = one Task Contract + one assigned branch | Worker §1 opening | retained |
| dedicated worktree is used when useful **for isolation** | Worker §1 opening | exact isolation criterion restored after self-audit |
| worktree filesystem path is runtime location, not assignment identity | Worker §1 opening | exact distinction retained |
| repository/working directory known before edit | Worker check 1 | retained |
| current assigned branch/worktree attachment and **state** known before edit | Worker check 1 | explicit `attachment, state, and safety`; fixes the withdrawn candidate's weaker `safety` wording |
| repository rules, required validation, risk/release constraints checked | Worker check 1 | retained locally because these are execution prerequisites, not persisted identity ontology |
| Issue/contract revision, Assignment ID, Base SHA, branch, Integration Target, Worker, status, Authority/Coordination/Assurance/ScopedAuthorization | `task-contract.md` §8 + Worker check 2 | one persisted schema owner; Worker still verifies the entire current envelope before editing |
| initial HEAD equals immutable Start HEAD before first contracted edit | Worker check 3 | explicit |
| authorized same-generation commits may advance beyond Start HEAD | Worker check 3 | explicit; prevents false staleness |
| same-generation correction/resume current HEAD equals Master Checkpoint HEAD | Worker check 4 | explicit |
| material identity/checkpoint mismatch => STALE_ASSIGNMENT | Worker final §1 sentence + unchanged downstream classifier | retained |
| Worker never guesses through mismatch | Worker final §1 sentence | retained |
| Worker never upgrades Authority/ScopedAuthorization/Coordination/Assurance | Worker final §1 sentence | retained |
| Master unavailability never broadens assignment | Worker final §1 sentence | retained |
| dispatch/handoff schemas remain complete transport artifacts | unchanged §2+ | byte identity outside §1 |

P2 is better only because schema identity and ordered pre-edit behavior are different semantic shapes and are now owned once each. It would be worse if Worker had to follow a new optional hop; it does not, because Worker entry already mandates both `task-contract.md` and `worker-protocol.md` before editing.

Protected scenario families: `AK`, `AM`, `AV`, `CR`, `DB`, `DG`, `CP`, plus dirty-worktree/isolation protections such as `X` where applicable.

## P3 — pending external-job continuation

| Baseline condition/consequence | Final representation | Lossless / precedence check |
|---|---|---|
| pending is dependency state, not failure | opening principle | retained |
| independent useful work precedes waiting | opening + first row | explicit |
| only after independent work is exhausted and pending is sole dependency should autonomous continuation be considered | opening + safe-continuation row predicate | discriminator added during self-audit; no row-order inference required |
| bounded non-tight authoritative rechecks allowed only when transition plausibly due and synchronous waiting safe/proportionate | safe-continuation row alternative (a) | every guard retained locally |
| bound continuation by expected duration, tool/runtime limits, diminishing value | same row | retained |
| genuine suitable event/condition resume primitive is alternative path | same row alternative (b) | retained |
| source defines no strict precedence between the two continuation mechanisms | same row: `without inventing precedence` | explicit to prevent table order from inventing policy |
| success => immediately continue existing workflow, no user nudge | success row | retained |
| failure => stop waiting, classify, remediation/independent work | failure row | retained |
| BLOCKED only while still pending, no independent work remains, it is sole blocker, and continuation is unavailable/unreasonable/exhausted | terminal row | conjunctive predicate made explicit and distinct from safe-continuation row |
| BLOCKED payload includes object/status/reason/resume condition/recoverable state | terminal row | retained |
| no tight poll/indefinite sleep/fabricated background resume/manufactured work | final guard | retained |
| DeliveryState.PENDING is lifecycle, not terminal boundary | final guard | retained |
| pending alone never means NO_READY_WORK | final guard | retained |

The baseline paragraph carried real branching, so a decision structure remains a better shape. The withdrawn table was not yet optimal because row predicates overlapped. The refined table encodes the discriminator in the condition itself, reducing the chance that a model treats rows as competing first-match rules.

Protected scenario families: `AQ`, `AW`, `CN`, `CO`, `CL`.

## P4 — `WriteState.UNKNOWN`

The exact Phase B P4 candidate is retained. Clause-level review confirmed that the removed symbolic line owned no unique semantic. The single guarded algorithm preserves: individual UNKNOWN scope; no blind retry; authoritative stable-identity/semantic-equivalence reread; decision-scoped completeness; explicit `present`, `proven absent`, and `incomplete/unknown` outcomes; absence as necessary but insufficient for retry; one safe idempotent/correlated retry maximum; local freeze + independent work; unresolved UNKNOWN after retry/no-safe-retry; and terminal `WRITE_OUTCOME_UNKNOWN` only when sole/project-wide controlling blocker.

This is the clearest case where the new representation is strictly better structurally: one fragile algorithm should have one ordered owner, and the most dangerous forbidden inference (`incomplete/unknown != proven absent`) is now adjacent to the branch where it matters.

Protected scenario families: `C`, `AU`, `DD`.

## P5 — progressive cold recovery

| Baseline meaning / purpose | Final representation | Lossless / activation check |
|---|---|---|
| new/replacement Master enters RECOVER before consequential mutation | opening sentence | retained |
| progressive/bounded recovery rather than exhaustive reload | opening + three labeled layers | retained |
| Orientation first: repository/repositories, target/default, checkout/worktrees, rules, capabilities | Orientation | retained |
| Project Map **or equivalent truth-location index** if present; only relevant durable docs | Orientation | exact broader alternative restored |
| establish active outcome/completion condition | Orientation | retained |
| recover ProjectAuthority + Coordination independently | Orientation | retained |
| recover affected-chain Assurance + exact ScopedAuthorization | Orientation | affected-chain scope restored explicitly |
| identify active critical path/workstream | Orientation | retained |
| chat loss alone never triggers root-spec load | Orientation guard | retained |
| if project-level intent is already unresolved/materially contradicted at Orientation, root spec may be needed immediately | Orientation -> Triggered-depth side path | prevents a naive `1 -> 2 -> 3` rewrite from delaying required project-intent evidence |
| active Issues/milestones/Projects/risks/assignments | Active-path | retained |
| open PR/reviews/checks/branches/dependencies | Active-path | retained |
| recent Git/release/deployment only as needed | Active-path | retained |
| only current Issue/contract, PR/branch/CI, direct interfaces/dependencies, blockers/risks, integration/delivery needed for next decision | Active-path | retained |
| reconcile contradictions/stale assignments | Active-path | retained |
| review queue, controlling blockers, Delivery fields, candidate/review state, next action | Active-path | retained |
| broader architecture/other workstreams/root spec/history/release history only on material trigger | Triggered depth | retained |
| root-spec exact trigger: project-level intent not safely established or material contradiction/change makes it decision-relevant | Triggered depth | retained |
| Triggered depth is conditional, not mandatory third phase | opening + label | prevents false eager-loading/linear-stage interpretation introduced by a naive table/list conversion |
| once decision-valid state exists, stop reading and continue valid plan | final stop paragraph | retained |
| large/long-lived repo narrows by workstream | final stop paragraph | retained |
| later multi-repo/legacy/preflight/planned-transition/route-failure/material-drift safeguards | unchanged bytes after replacement boundary | protected outside migration region |

P5's final form is intentionally **not a table**. The semantic is progressive retrieval with a conditional widening branch; long multi-purpose table cells obscure that flow and violate the methodology's own warning against tables whose cells become paragraphs. The refined labeled procedure exposes the normal path and conditional side path without turning recovery into a new state machine.

Protected scenario families: `I`, `AH`, `BG`, `BH`, `BY`, `DA` and the existing multi-repository/large-repository recovery cases.

## Composition and regression safeguards

`tests/test_phase_c_runtime_migration.py` now reflects the stronger evidence boundary:

1. every byte outside the five declared canonical migration surfaces must remain equal to exact Phase C base;
2. only those five runtime paths may differ under `skill/`;
3. P4 must still equal the exact selected P4 prototype;
4. refined P1/P2/P3/P5 must contain the semantic discriminators identified by this self-audit, including negative/non-implication guards;
5. P5 must not regress to the long-cell recovery table;
6. state/boundary namespace token sets must remain unchanged per runtime file;
7. accepted v1.2.3 complete-response machine-relay copy-target behavior must remain present unchanged.

The existing immutable-runtime equivalence, eval/adversarial, package, runtime-cleanliness, prototype-isolation, helper/scorer, and repository validation suites remain independently required. Prototype tests prove their frozen experiment claims; they no longer force Phase C to retain exact P1/P2/P3/P5 wording after the deeper self-audit found a better representation of the same selected concepts.

## Explicit non-goals

- no wholesale `SKILL.md` rewrite;
- no universal prose -> table/JSON/XML conversion;
- no new rule, lifecycle state, decision cache/frame, authority shortcut, router edge, or persistence mechanism;
- no migration of frozen/superseded PR #43 representation;
- no version or release publication;
- no fabricated live-model performance claim.

## Final status boundary

The next review candidate may be frozen only after the refined branch passes exact-head validation and another complete effective-diff/semantic self-review confirms no unexplained semantic atom, ownership drift, precedence change, or representation cost remains. Only then may #39 receive a fresh independent HIGH_ASSURANCE review envelope. Final HIGH-risk integration remains a separate human approval gate.
