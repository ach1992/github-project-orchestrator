# Canonical Rule Map

Status: current development traceability map for the refactored runtime, preserving immutable `v1.0.0` source anchors for historical equivalence evidence. No row below independently changes runtime behavior; canonical runtime definitions live in the listed owners under `skill/`.

## 1. Mapping contract

- A semantic Rule ID represents one behavior guarantee even when v1.0.0 repeated it in several files.
- `Canonical owner` is the single current location/domain that defines the rule. Other runtime references may keep short boundary reminders but must not redefine it.
- `Source anchors` refer to the immutable `v1.0.0` runtime paths/lines. The deterministic source-index generator can reproduce `RULE-SOURCES-v1.0.0.tsv`; `RULE-SOURCES-v1.0.0.manifest` locks its expected row count and SHA-256 for mechanical traceability.
- For a Rule introduced by an accepted post-v1.0.0 requirement, `Source anchors` identify that project-level requirement/change instead of inventing a historical v1.0.0 location.
- Eval IDs are regression anchors, not the full proof of equivalence.
- Historical migration state is not a second source of current truth. If a future requirement deliberately supersedes a Rule ID, record the decision and update its canonical owner/evaluation evidence rather than creating competing definitions.

## 2. Foundation and truth

| Rule ID | Guarantee | Canonical owner | Source anchors | Eval anchors |
|---|---|---|---|---|
| `OUTCOME-STABLE` | Preserve accepted outcome/success criteria; do not shrink for convenience or expand to manufacture work. | `SKILL.md` outcome kernel | `SKILL.md:40`; `master-cycle.md:174+` | AY, BA, CB, CY |
| `TRUTH-ONE-OWNER` | One authoritative owner per kind of live truth; avoid competing manager-memory artifacts. | `SKILL.md` truth model | `SKILL.md:41,61-73`; `governance.md:47+` | A, I, Z |
| `EVIDENCE-BEATS-NARRATIVE` | Current Git/GitHub/CI/deployment evidence outranks summaries/chat. | `SKILL.md` truth model | `SKILL.md:42,59-79` | E, I, BH, CO |
| `MUTATION-IDEMPOTENT` | Discover/reuse/update/create-only-if-absent/verify; incomplete discovery is not absence. | `SKILL.md` mutation invariant | `SKILL.md:43` | B, AU |
| `DRIFT-RECONCILE` | Re-read and reconcile before overwrite-sensitive/integration/release/production writes. | `SKILL.md` mutation invariant | `SKILL.md:44`; `authority-gates.md:156+` | E, BH |
| `PROTECT-UNRELATED` | Never destroy/absorb unrelated user/contributor work to simplify execution. | `SKILL.md` safety invariant | `SKILL.md:50` | X |
| `NO-FABRICATION` | Never claim actions/evidence that were not performed and verified. | `SKILL.md` evidence invariant | `SKILL.md:52` | P, CO |
| `ANTI-SPIN` | Do not repeat materially identical failed actions without new evidence; change strategy or work. | `SKILL.md` execution invariant | `SKILL.md:53`; `master-cycle.md:157+` | T, BG |
| `LEAN-ORCHESTRATION` | Create project/process artifacts only when they improve a future decision, execution, safety, or recovery. | `governance.md` | `SKILL.md:49`; `governance.md:9+` | K, AB, BT |
| `SUCCESSION-RECOVERABLE` | End at canonical boundaries with authoritative state sufficient for a replacement Master, subject to explicit USER_STOP. | `continuity.md` | `SKILL.md:56`; `continuity.md:49+` | I, Z, AI, BB |

## 3. Authority, effects, and gates

| Rule ID | Guarantee | Canonical owner | Source anchors | Eval anchors |
|---|---|---|---|---|
| `AUTHORITY-STABLE` | Project Authority changes only from applicable explicit/higher authorization, never merely from access/risk/profile/environment. | `authority-gates.md` | `SKILL.md:21`; `authority-gates.md:16-20` | AH, CU |
| `AUTHORIZATION-SCOPED` | Exact one-off approval/grant applies only to its scope and does not upgrade project-wide Authority. | `authority-gates.md` | `SKILL.md:21`; `authority-gates.md:20` | CX |
| `CAPABILITY-NOT-AUTHORITY` | Capability affects feasibility and may constrain execution but cannot grant Authority. | `authority-gates.md` | `SKILL.md:77-79`; `authority-gates.md:20` | N, CU |
| `EFFECT-ACTUAL` | Classify by actual deterministic consequence, not labels, branch names, or nominal environment. | `authority-gates.md` | `authority-gates.md:22-97` | H, BD, BO, CG, CH |
| `EFFECT-MULTI` | Preserve every independently applicable effect/control when one mutation has multiple consequences. | `authority-gates.md` | `authority-gates.md:50-97` | H, CV |
| `GATE-NO-INVENTION` | Do not invent human confirmation gates beyond the canonical matrix. | `authority-gates.md` | `SKILL.md:33`; `authority-gates.md:34+` | L, AJ, BP |
| `GATE-UNION` | Scoped authorization may satisfy one gate but cannot waive another independent effect gate. | `authority-gates.md` | `authority-gates.md:50-97` | CV |
| `WRITE-UNKNOWN-RECONCILE` | Ambiguous mutation outcome becomes unknown; reconcile authoritatively before any retry. | `authority-gates.md` | `authority-gates.md:140-155` | C |
| `CONCURRENCY-OPTIMISTIC` | Overwrite-sensitive writes use expected identity/revision and reconcile drift rather than blind overwrite. | `authority-gates.md` | `authority-gates.md:156-161`; `task-contract.md:102` | D, E, AO, CR |
| `MATERIAL-DECISION-BOUNDARY` | Escalate only irreducible owner decisions that remain material after independent work is exhausted; ordinary technical choices remain agent-owned. | `authority-gates.md` | `authority-gates.md:99-114` | S, BF |

## 4. Coordination, assurance, work preparation

| Rule ID | Guarantee | Canonical owner | Source anchors | Eval anchors |
|---|---|---|---|---|
| `COORDINATION-BASELINE` | Coordination baseline is determined by coordination/recovery needs, not repository size alone. | `SKILL.md` state ontology | `SKILL.md:23-31` | W, AB, CE |
| `ASSURANCE-ADDITIVE` | HIGH_ASSURANCE adds justified assurance controls while preserving the coordination baseline; it does not create approval by itself. | `SKILL.md` state ontology | `SKILL.md:21,29`; repeated in protocol refs | G, BP, CE, CF |
| `DIMENSIONS-ORTHOGONAL` | Coordination, assurance, risk, execution path, persistence, strategy, capability, and Authority are independent inputs unless an explicit rule connects them. | `SKILL.md` state ontology | `SKILL.md:12-31`; `authority-gates.md:9-20`; `task-contract.md:19-36` | AD, CE, CF, CM, CU |
| `RISK-SCOPED` | Reclassify change risk only when decision-relevant; risk is change-specific and not importance/project size. | `task-contract.md` | `SKILL.md:21`; `task-contract.md:87-98` | AC, AJ, CW |
| `WORK-CLEAR-ENOUGH` | Outcome, acceptance, validation, dependencies, and material risk must be clear enough for the next change; formalize only when useful. | `task-contract.md` | `SKILL.md:46`; `task-contract.md:19+` | K, L, BE |
| `ENGINEERING-CONCERNS-PROPORTIONAL` | Activate only engineering concerns material to the actual change/failure surface and carry them through implementation/evidence without a universal checklist, state field, artifact, dimension change, or new gate by default. | `engineering-quality.md` | post-v1.1.1 requirement: `docs/PROJECT-SPEC.md` §3.1 | G, K, L, M, AB, AC, BS, BT, BU, CO |
| `FAST-FULL-SELECT` | FAST/FULL is selected from ambiguity/dependency/review/control need; routine behavior changes may remain FAST. | `master-cycle.md` | `master-cycle.md:61-73`; `task-contract.md:23-36` | K, L, AB, CF, CM |
| `CONTRACT-PERSISTENCE-INDEPENDENT` | FULL does not imply persistence; persistence depends on recovery/coordination value. Existing persistence does not imply FULL. | `task-contract.md` | `task-contract.md:23-36` | CM |
| `DELEGATION-PROPORTIONAL` | Delegate only when specialization/throughput/parallelism materially helps; bounded single delegation can remain LIGHTWEIGHT while still using full Worker envelope. | `master-cycle.md` | `SKILL.md:27`; `master-cycle.md:74-85`; `worker-protocol.md:58-60` | Q, AN |
| `SELF-EXECUTION-FALLBACK` | If direct Worker dispatch is unavailable, Master self-executes safe authorized work rather than stopping. | `master-cycle.md` | `SKILL.md:113`; `master-cycle.md:74-102` | Q |
| `WIP-FLOW` | Prefer review/integration/unblocking when they bottleneck; parallelize only genuinely independent surfaces. | `master-cycle.md` | `SKILL.md:48`; `master-cycle.md:119-130` | J, R |
| `SYNTHESIZE-WORK` | Outcome incomplete + no READY item triggers refine/unblock/split/investigate, not automatic NO_READY_WORK. | `master-cycle.md` | `SKILL.md:93-94`; `master-cycle.md:131-156` | O, AX |
| `MASTER-STOP-CANONICAL` | Chat turn, commit, PR update, review, Worker handoff, tool batch, or missing delegation is not a Master stop; stop only at canonical boundary after continuation test. | `master-cycle.md` | `SKILL.md:55,83-95`; `authority-gates.md:115-139`; `master-cycle.md:186+` | O, P, R, AW, AX, AP, CN, CQ |

## 5. Worker and assignment

| Rule ID | Guarantee | Canonical owner | Source anchors | Eval anchors |
|---|---|---|---|---|
| `WORKER-BOUNDED` | Worker owns exactly one assignment and never reprioritizes, broadens scope, upgrades envelope, integrates target, or owns release. | `worker-protocol.md` | `SKILL.md:16`; `worker-protocol.md:9-15,58+` | CC, CP |
| `ASSIGNMENT-IDENTITY` | Dispatch persists exact assignment generation, contract revision, repository/base/branch/target/Worker/envelope identity before editing. | `task-contract.md` | `task-contract.md:104-123`; `worker-protocol.md:13-60` | AK, AM, AV |
| `START-HEAD-HISTORICAL` | Initial `Expected Starting HEAD` is verified once; authorized Worker commits do not make the assignment stale. | `worker-protocol.md` | `task-contract.md:119-123`; `worker-protocol.md:13,95` | CR |
| `CORRECTION-CHECKPOINT` | Same-generation correction/resume uses a fresh reviewed/current HEAD checkpoint as the concurrency guard. | `worker-protocol.md` | `task-contract.md:119`; `worker-protocol.md:13,145+` | CR |
| `STALE-ASSIGNMENT` | Material assignment/envelope invalidation or uncertain materiality stops Worker with STALE_ASSIGNMENT; Worker never guesses/overwrites. | `worker-protocol.md` | `worker-protocol.md:79-97` | D, AV |
| `WORKER-STOP-LOCAL` | Worker stop/handoff does not automatically become Master stop; Master absorbs, corrects, redispatches, self-executes, or switches work when possible. | `master-cycle.md` | `SKILL.md:54`; `master-cycle.md:104-118`; `worker-protocol.md:137-145` | R, CK |
| `WORKER-HANDOFF-PRECEDENCE` | Handoff status is determined by explicit precedence so stale/blocking states cannot be mislabeled DONE. | `worker-protocol.md` | `worker-protocol.md:99-136` | CK |
| `WORKER-TARGET-SEPARATION` | Assigned branch cannot be the canonical Integration Target; Worker does not integrate target. | `worker-protocol.md` | `task-contract.md:112+`; `worker-protocol.md:13,58+` | AM, CP |

## 6. Review and integration

| Rule ID | Guarantee | Canonical owner | Source anchors | Eval anchors |
|---|---|---|---|---|
| `REVIEW-EFFECTIVE-CHANGE` | Review current target-to-candidate effective change, not stale narrative or only author intent. | `review-integration.md` | `SKILL.md:106`; `review-integration.md:9-77` | E |
| `REVIEW-IDENTITY-FRESH` | Approval/evidence is bound to target, candidate, contract, and relevant SHA; material drift invalidates transfer. | `review-integration.md` | `review-integration.md:9-21,78-91` | E, CJ |
| `UNTRUSTED-EXECUTION-SURFACE` | Inspect changed hooks/scripts/workflows/supply-chain surfaces before executing untrusted candidate code. | `review-integration.md` | `SKILL.md:106`; `review-integration.md:55-77` | M |
| `CI-CLASSIFY` | CI failure is classified by candidate/baseline/environment/transient cause before deciding the next action. | `review-integration.md` | `review-integration.md:92-106` | F, CL |
| `CONFLICT-RECONCILE` | Resolve conflicts against fresh target/effective change and revalidate affected evidence. | `review-integration.md` | `review-integration.md:107-116` | E |
| `INTEGRATION-GATE` | Integrate only after current acceptance, review, CI/policy, target/candidate identity, and applicable action gates are satisfied. | `review-integration.md` | `review-integration.md:117-147` | H, CI, CJ |
| `SELF-AUTHORED-FRESH-REVIEW` | Master-authored work still receives a fresh diff/acceptance review; independent review only when risk/profile requires it. | `review-integration.md` | `SKILL.md:47`; `review-integration.md:148-166` | BC |
| `POST-INTEGRATION-RECONCILE` | After integration, reconcile immutable result and continue to delivery only when required by outcome. | `review-integration.md` | `review-integration.md:167+` | CO |

## 7. Continuity and recovery

| Rule ID | Guarantee | Canonical owner | Source anchors | Eval anchors |
|---|---|---|---|---|
| `RECOVERY-EVENT-DRIVEN` | Full recovery happens on new/replacement Master or material invalidation, not on ordinary progress/tool batches/expected transitions. | `continuity.md` | `SKILL.md:57`; `continuity.md:21-48` | U, BG, BH |
| `RECOVERY-AUTHORITATIVE` | Recovery reconstructs from authoritative repository/GitHub/release evidence, not old chat or Worker narrative. | `continuity.md` | `SKILL.md:8,42`; `continuity.md:21-48` | A, I |
| `ROTATION-SIGNAL-DRIVEN` | Long context alone does not require rotation; rotate when continuity/reliability signals justify it. | `continuity.md` | `SKILL.md:95`; `continuity.md:63-86` | U |
| `ROTATION-SAFE-BOUNDARY` | Rotate only at a recoverable boundary and carry established Authority/current effective controls without becoming more permissive. | `continuity.md` | `SKILL.md:21,56`; `continuity.md:63-113` | AH, BB, CE |
| `CHAT-NONAUTHORITATIVE` | Conversation context is disposable and must not be the sole owner of project state. | `continuity.md` | `SKILL.md:8,73`; `continuity.md:9+` | I, Z |

## 8. Governance and root specification

| Rule ID | Guarantee | Canonical owner | Source anchors | Eval anchors |
|---|---|---|---|---|
| `ROOT-SPEC-CANONICAL` | First ownership resolves the project-defining prompt/spec and keeps one safe canonical repository copy, excluding unsafe material. | `governance.md` | `SKILL.md:8,87`; `governance.md:15+` | BV, BW, BX, CD, CY |
| `ROOT-SPEC-OFF-HOT-PATH` | Normal cycles operate from nearer downstream authoritative sources; root spec is reread only when intent conflict/change makes it relevant. | `governance.md` | `SKILL.md:8`; `governance.md:15+` | BY, BZ, CA |
| `BOOTSTRAP-PROPORTIONAL` | First ownership repairs only readiness that materially helps execution/recovery; stop bootstrapping when its completion test passes. | `governance.md` | `SKILL.md:103`; `governance.md:129-175` | AZ, BS, BT |
| `ARTIFACT-FITNESS` | Reuse existing engineering systems when fit; repair/replace only when material execution value justifies it. | `governance.md` | `governance.md:9-15,129+` | BS, BU |
| `READY-DONE-SEMANTICS` | READY/DONE represent executable/verified lifecycle semantics, not empty scaffolding or ceremony. | `governance.md` | `governance.md:97-108`; `task-contract.md:125+` | BE |

## 9. Release and production

| Rule ID | Guarantee | Canonical owner | Source anchors | Eval anchors |
|---|---|---|---|---|
| `RELEASE-MODEL-DISCOVER` | Discover the repository/deployment release model before assuming process or target semantics. | `release.md` | `release.md:9-24` | CS |
| `INTEGRATED-NOT-DELIVERED` | Integration and delivery are separate completion states; production-required work remains open until delivery evidence proves it. | `release.md` | `SKILL.md:108`; `release.md:9-25,85+` | CO |
| `PRODUCTION-DETERMINISTIC-EFFECT` | An upstream action that deterministically causes production is classified/gated as production before action. | `release.md` | `SKILL.md:108`; `release.md:44-84` | H, BO, CG |
| `MIGRATION-ROLLBACK` | High-risk migration/production work requires proportionate rollback/recovery readiness before irreversible exposure. | `release.md` | `release.md:25-68` | G |
| `PRODUCTION-GATE` | Production mutation requires the canonical production authorization gate; pre-authorization is scope-bound. | `release.md` | `release.md:69-84`; `authority-gates.md` matrix | H, CV |
| `POST-RELEASE-EVIDENCE` | Deployment success alone is insufficient; verify intended artifact/environment/health/acceptance evidence. | `release.md` | `release.md:85-99` | CO, CT |
| `INCIDENT-CONTAINMENT` | When current production identity/state is wrong or unsafe, containment outranks normal delivery flow. | `release.md` | `release.md:100-112` | CT |
| `RELEASE-CLOSEOUT` | Close only after required delivery, evidence, state reconciliation, and remaining risks/rollback obligations are resolved or explicitly owned. | `release.md` | `release.md:113+` | P, CO |

## 10. Historical representation defects and resolution

Phase 1 identified the representation defects below before runtime migration. They are retained here for traceability, but **they are not current unresolved defects**:

| Historical defect | Current resolution |
|---|---|
| scalar `Operating Profile` mixed coordination and assurance | current runtime uses independent `CoordinationBaseline` + `AssuranceLevel`; legacy `HIGH_ASSURANCE` never invents a missing baseline |
| scalar `Action Class` could hide simultaneous consequences | `ApplicableEffects` is a set and `authority-gates.md` applies the union of independent obligations |
| bare `BLOCKED` / `WRITE_OUTCOME_UNKNOWN` could propagate across domains | task, Worker, write, delivery, and Master-boundary lifecycles are namespace-qualified |
| `Delivery endpoint` mixed completion state and environment | current model separates `DeliveryRequirement`, `DeliveryTarget`, and `DeliveryState` |
| project-wide Authority and one-off approval lacked separate state fields | current model separates `ProjectAuthority` from exact `ScopedAuthorization` |
| initial Worker HEAD and correction/resume checkpoint were overloaded | `Start HEAD` is immutable generation history; `Checkpoint HEAD` is the same-generation correction concurrency guard |
| `TRIVIAL | SUBSTANTIVE` had little independent decision power | retained only as a local descriptor when it materially affects delegation, validation, or helper behavior; it is not a RiskLevel, profile, execution-path, or contract gate by itself |

## 11. Coverage rule for current maintenance

A v1.0.0 clause may remain reduced/absent from current runtime prose only when at least one is true:

- its semantic Rule ID has a canonical definition elsewhere and the omitted text was duplicate definition;
- it is represented as a short event-bound boundary reminder that points to the canonical rule;
- a deterministic validator/script enforces the mechanical invariant and the runtime retains the trigger/meaning needed to invoke it;
- a deliberate requirement change marks the Rule ID `SUPERSEDED`, records rationale, and updates affected regression scenarios.

A rule is never considered safely migrated or maintained merely because a graph/table appears similar. Goal -> Rule -> current canonical owner -> evaluation evidence must remain intact, and `tools/validate_skill.py` mechanically checks the traceability structure it can prove.