# Canonical Goal Map

Status: current development-only traceability layer. Canonical goal definitions live in `../docs/PROJECT-SPEC.md`; canonical rule definitions live in `RULE-MAP.md`. This file maps the completed refactored runtime to those owners and does not redefine either.

## Purpose

Use this map to prevent maintenance/refactors from optimizing local wording while losing project-level intent. Every material runtime change should identify the Goal IDs it advances and the Rule IDs/evaluations it can affect.

Goal rows may emphasize primary families rather than every secondary relationship, but **Rule ID coverage is mechanically exhaustive**: every canonical Rule ID in `RULE-MAP.md` must appear in at least one Goal row below. Every explicit eval anchor in this file and `RULE-MAP.md` must resolve to a real scenario in `skill/references/eval-scenarios.md`.

| Goal | Primary rule families / Rule IDs | Existing evaluation anchors | Broader operational focus |
|---|---|---|---|
| `G01` Verified End-to-End Delivery | `OUTCOME-STABLE`, `POST-INTEGRATION-RECONCILE`, `INTEGRATED-NOT-DELIVERED`, `POST-RELEASE-EVIDENCE`, `RELEASE-CLOSEOUT` | P, AY, CO, CT | end-to-end project from intake through required delivery |
| `G02` Outcome & Scope Integrity | `OUTCOME-STABLE`, `ROOT-SPEC-CANONICAL`, `ROOT-SPEC-OFF-HOT-PATH`, `MATERIAL-DECISION-BOUNDARY` | AY, BA, BZ, CA, CB, CD, CY | cross-workstream requirement change with unaffected work continuing |
| `G03` Adaptive Planning & Decomposition | `WORK-CLEAR-ENOUGH`, `FAST-FULL-SELECT`, `CONTRACT-PERSISTENCE-INDEPENDENT`, `SYNTHESIZE-WORK` | K, L, O, AB, AZ, CM | decomposition quality across small/medium/large outcomes |
| `G04` Dependency, Flow & Project Health Management | `WIP-FLOW`, `SYNTHESIZE-WORK`, `MASTER-STOP-CANONICAL`, `DRIFT-RECONCILE`, `CONCURRENCY-OPTIMISTIC` | J, O, R, AP, AQ, CN, BH | plan validity, critical-path change, and project-health response |
| `G05` Professional Engineering Execution | `PROTECT-UNRELATED`, `SELF-EXECUTION-FALLBACK`, `ENGINEERING-CONCERNS-PROPORTIONAL`, `CI-CLASSIFY`, `CONFLICT-RECONCILE`, `READY-DONE-SEMANTICS` | X, Y, G, L, AB, AC, CL, Q, BE, DH | root-cause implementation with concern-aware but proportionate validation/review |
| `G06` Architecture & Engineering-System Evolution | `ARTIFACT-FITNESS`, `ENGINEERING-CONCERNS-PROPORTIONAL`, `BOOTSTRAP-PROPORTIONAL`, `LEAN-ORCHESTRATION` | AZ, BS, BT, BU | evidence-triggered architecture/tooling/CI improvement without speculative cleanup |
| `G07` Engineering Quality & Evidence | `EVIDENCE-BEATS-NARRATIVE`, `NO-FABRICATION`, `ENGINEERING-CONCERNS-PROPORTIONAL`, `DEFENSIVE-SECURITY-CONTINUATION`, `REVIEW-EFFECTIVE-CHANGE`, `REVIEW-IDENTITY-FRESH`, `UNTRUSTED-EXECUTION-SURFACE`, `CI-CLASSIFY`, `SELF-AUTHORED-FRESH-REVIEW`, `POST-RELEASE-EVIDENCE` | E, F, G, M, AB, AC, CL, BC, CO, DH, DJ | correctness/security/privacy/resilience/diagnosability/performance/operations evidence proportional to the change |
| `G08` Scale-Adaptive Coordination | `COORDINATION-BASELINE`, `DIMENSIONS-ORTHOGONAL`, `DELEGATION-PROPORTIONAL`, `CONTRACT-PERSISTENCE-INDEPENDENT`, `WIP-FLOW` | W, AB, AN, CE, CF, CZ | large/multi-repo bounded context and component/workstream ownership |
| `G09` Professional Delegation & Ownership | `MACHINE-RELAY-PORTABLE`, `WORKER-BOUNDED`, `ASSIGNMENT-IDENTITY`, `START-HEAD-HISTORICAL`, `CORRECTION-CHECKPOINT`, `STALE-ASSIGNMENT`, `WORKER-STOP-LOCAL`, `WORKER-HANDOFF-PRECEDENCE`, `WORKER-TARGET-SEPARATION`, `DELEGATION-PROPORTIONAL` | D, R, AK, AM, AT, AV, CK, CP, CR | multiple independent Workers and Master replacement without ownership drift |
| `G10` Authority, Risk & Safety Integrity | `AUTHORITY-STABLE`, `AUTHORIZATION-SCOPED`, `CAPABILITY-NOT-AUTHORITY`, `EFFECT-ACTUAL`, `EFFECT-MULTI`, `GATE-NO-INVENTION`, `GATE-UNION`, `WRITE-UNKNOWN-RECONCILE`, `CONCURRENCY-OPTIMISTIC`, `MATERIAL-DECISION-BOUNDARY`, `ASSURANCE-ADDITIVE`, `RISK-SCOPED`, `DEFENSIVE-SECURITY-CONTINUATION` | H, AH, AJ, BP, CG, CH, CU, CV, CX, C, CW, DJ | multi-effect obligation union and authority/assurance orthogonality |
| `G11` Verified Review, Integration, Release & Operations | `MACHINE-RELAY-PORTABLE`, `ENGINEERING-CONCERNS-PROPORTIONAL`, `DEFENSIVE-SECURITY-CONTINUATION`, `REVIEW-EFFECTIVE-CHANGE`, `REVIEW-IDENTITY-FRESH`, `UNTRUSTED-EXECUTION-SURFACE`, `CI-CLASSIFY`, `CONFLICT-RECONCILE`, `INTEGRATION-GATE`, `SELF-AUTHORED-FRESH-REVIEW`, `POST-INTEGRATION-RECONCILE`, `RELEASE-MODEL-DISCOVER`, `INTEGRATED-NOT-DELIVERED`, `PRODUCTION-DETERMINISTIC-EFFECT`, `MIGRATION-ROLLBACK`, `PRODUCTION-GATE`, `POST-RELEASE-EVIDENCE`, `INCIDENT-CONTAINMENT`, `RELEASE-CLOSEOUT` | E, G, H, M, AC, AT, BC, CJ, CO, CT, CS, BO, CV, DH, DI, DJ | complete release path tied to immutable artifact, operational supportability, and delivery evidence |
| `G12` Zero-Chat Recoverability & Succession | `MACHINE-RELAY-PORTABLE`, `SUCCESSION-RECOVERABLE`, `RECOVERY-EVENT-DRIVEN`, `RECOVERY-AUTHORITATIVE`, `ROTATION-SIGNAL-DRIVEN`, `ROTATION-SAFE-BOUNDARY`, `CHAT-NONAUTHORITATIVE`, `ASSIGNMENT-IDENTITY` | I, Z, U, AH, AK, AT, BB, BG, BH | cold recovery with zero conversation context and bounded discovery cost |
| `G13` Lean Navigable Project Knowledge | `TRUTH-ONE-OWNER`, `LEAN-ORCHESTRATION`, `RECOVERY-AUTHORITATIVE`, `CHAT-NONAUTHORITATIVE`, `ROOT-SPEC-OFF-HOT-PATH` | A, I, Z, AZ, BT, BY | bounded recovery cost and stale/duplicate information reconciliation |
| `G14` Repository Readiness, Hygiene & Self-Repair | `BOOTSTRAP-PROPORTIONAL`, `ARTIFACT-FITNESS`, `MUTATION-IDEMPOTENT`, `DRIFT-RECONCILE`, `READY-DONE-SEMANTICS` | A, B, AU, AZ, BS, BT, BU, BE | stale project-system repair without parallel duplicate mechanisms |
| `G15` Proactive Improvement Without Scope Creep | `OUTCOME-STABLE`, `LEAN-ORCHESTRATION`, `ARTIFACT-FITNESS` | Y, AX, AY, BA, BT, BU, CB | proposal/execute/ignore classification for discovered improvements |
| `G16` Persistent Progress Without Friction | `MACHINE-RELAY-PORTABLE`, `ANTI-SPIN`, `SYNTHESIZE-WORK`, `MASTER-STOP-CANONICAL`, `WORKER-STOP-LOCAL`, `SELF-EXECUTION-FALLBACK`, `CAPABILITY-NOT-AUTHORITY` | O, Q, R, T, AP, AQ, AT, AW, AX, CN, CQ | useful-action latency and continuation across local blockers/tool-route failures |

## Traceability rule

Before removing, consolidating, or relocating runtime behavior:

```text
Goal ID
  -> affected Rule IDs
  -> current source occurrences
  -> target canonical representation
  -> regression / operational evidence
```

A shorter implementation is not a successful refactor if any link in that chain is lost.

Mechanically enforceable development-time invariants are:

- every canonical Goal ID in `../docs/PROJECT-SPEC.md` appears exactly once in this table;
- every canonical Rule ID in `RULE-MAP.md` appears in at least one Goal row and no unknown Rule ID is introduced here;
- every canonical Rule ID has one Rule Map row with one non-empty canonical owner and at least one eval anchor;
- every explicit Goal/Rule eval anchor resolves to a real unique scenario ID;
- scenario IDs are unique and contiguous so accidental deletion/duplication is visible.

These checks prove traceability structure only; they do not prove semantic quality, READY, review sufficiency, architecture correctness, or risk judgment.

## Historical coverage gaps and current evidence

The Phase 1 map identified broader project-level behaviors that single-rule regression scenarios could not prove alone. Phases 5-8 added runtime mechanisms, source-grounded operational scenarios, live repository delivery evidence, deterministic checks, and independent release-candidate review. The current status is:

| Historical gap | Current evidence / remaining interpretation boundary |
|---|---|
| Project health / plan validity | `master-cycle.md` and `governance.md` use event-driven critical-path/plan reconciliation; the medium, large, and local-blocker Phase 7 scenarios exercise sequencing and continuation without rebuilding the whole plan. |
| Architecture evolution | `governance.md` and `master-cycle.md` require evidence-triggered enabling improvements and reject speculative cleanup; G06 is exercised operationally, while whether a specific architecture change is worthwhile remains professional judgment rather than a mechanical lint rule. |
| Large-project bounded context | Phase 5 established workstream/global-spine rules and the large multi-repository benchmark verifies progressive context loading without a duplicate central backlog. |
| Cold recovery cost | Phase 5 established orientation-spine/active-path recovery and the cold-recovery benchmark measures prescribed discovery steps; the benchmark remains a source-grounded policy simulation, not an independent wall-clock model trial. |
| Information entropy | Canonical one-owner/reconciliation rules plus deterministic duplicate Rule ownership checks prevent known semantic forks; there is intentionally no synthetic scalar "entropy score" that could substitute for repository judgment. |
| End-to-end operational benchmark | Phase 7 provides eight fixed scenarios with G01-G16 coverage and adversarial negative fixtures, supplemented by `LIVE-EVIDENCE.md`; it does not claim multi-model statistics, wall-clock latency, or production reliability beyond the evidence actually observed. |

Future evidence may strengthen these areas, but none of the historical rows above is an unresolved permission slip for broad refactoring. New work must still be justified by a current Goal/Rule/evidence gap.
