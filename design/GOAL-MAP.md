# Canonical Goal Map

Status: development-only traceability layer. Canonical goal definitions live in `../docs/PROJECT-SPEC.md`; canonical rule definitions live in `RULE-MAP.md`. This file does not redefine either.

## Purpose

Use this map to prevent refactors from optimizing local wording while losing project-level intent. Every material runtime change should identify the Goal IDs it advances and the Rule IDs/evaluations it can affect.

Goal rows may emphasize primary families rather than every secondary relationship, but **Rule ID coverage is mechanically exhaustive**: every canonical Rule ID in `RULE-MAP.md` must appear in at least one Goal row below. Every explicit eval anchor in this file and `RULE-MAP.md` must resolve to a real scenario in `skill/references/eval-scenarios.md`.

| Goal | Primary rule families / Rule IDs | Existing evaluation anchors | Additional coverage to add during refactor |
|---|---|---|---|
| `G01` Verified End-to-End Delivery | `OUTCOME-STABLE`, `POST-INTEGRATION-RECONCILE`, `INTEGRATED-NOT-DELIVERED`, `POST-RELEASE-EVIDENCE`, `RELEASE-CLOSEOUT` | P, AY, CO, CT | end-to-end synthetic project from intake through required delivery |
| `G02` Outcome & Scope Integrity | `OUTCOME-STABLE`, `ROOT-SPEC-CANONICAL`, `ROOT-SPEC-OFF-HOT-PATH`, `MATERIAL-DECISION-BOUNDARY` | AY, BA, BZ, CA, CB, CD, CY | cross-workstream requirement change with unaffected work continuing |
| `G03` Adaptive Planning & Decomposition | `WORK-CLEAR-ENOUGH`, `FAST-FULL-SELECT`, `CONTRACT-PERSISTENCE-INDEPENDENT`, `SYNTHESIZE-WORK` | K, L, O, AB, AZ, CM | decomposition quality across small/medium/large outcomes |
| `G04` Dependency, Flow & Project Health Management | `WIP-FLOW`, `SYNTHESIZE-WORK`, `MASTER-STOP-CANONICAL`, `DRIFT-RECONCILE`, `CONCURRENCY-OPTIMISTIC` | J, O, R, AP, CN, BH | explicit plan-validity/critical-path-change and project-health scenarios |
| `G05` Professional Engineering Execution | `PROTECT-UNRELATED`, `SELF-EXECUTION-FALLBACK`, `CI-CLASSIFY`, `CONFLICT-RECONCILE`, `READY-DONE-SEMANTICS` | X, Y, AC, CL, Q, BE | root-cause vs symptom-patch representative coding benchmark |
| `G06` Architecture & Engineering-System Evolution | `ARTIFACT-FITNESS`, `BOOTSTRAP-PROPORTIONAL`, `LEAN-ORCHESTRATION` | AZ, BS, BT, BU | architecture-drift and developer-feedback-loop improvement scenarios |
| `G07` Engineering Quality & Evidence | `EVIDENCE-BEATS-NARRATIVE`, `NO-FABRICATION`, `REVIEW-EFFECTIVE-CHANGE`, `REVIEW-IDENTITY-FRESH`, `UNTRUSTED-EXECUTION-SURFACE`, `CI-CLASSIFY`, `SELF-AUTHORED-FRESH-REVIEW`, `POST-RELEASE-EVIDENCE` | E, F, M, AC, CL, BC, CO | quality benchmark spanning correctness/security/performance/operations |
| `G08` Scale-Adaptive Coordination | `COORDINATION-BASELINE`, `DIMENSIONS-ORTHOGONAL`, `DELEGATION-PROPORTIONAL`, `CONTRACT-PERSISTENCE-INDEPENDENT`, `WIP-FLOW` | W, AB, AN, CE, CF, CZ | large/multi-repo bounded-context and component/workstream ownership test |
| `G09` Professional Delegation & Ownership | `WORKER-BOUNDED`, `ASSIGNMENT-IDENTITY`, `START-HEAD-HISTORICAL`, `CORRECTION-CHECKPOINT`, `STALE-ASSIGNMENT`, `WORKER-STOP-LOCAL`, `WORKER-HANDOFF-PRECEDENCE`, `WORKER-TARGET-SEPARATION`, `DELEGATION-PROPORTIONAL` | D, R, AK, AM, AV, CK, CP, CR | multiple independent Workers with Master replacement mid-flight |
| `G10` Authority, Risk & Safety Integrity | `AUTHORITY-STABLE`, `AUTHORIZATION-SCOPED`, `CAPABILITY-NOT-AUTHORITY`, `EFFECT-ACTUAL`, `EFFECT-MULTI`, `GATE-NO-INVENTION`, `GATE-UNION`, `WRITE-UNKNOWN-RECONCILE`, `CONCURRENCY-OPTIMISTIC`, `MATERIAL-DECISION-BOUNDARY`, `ASSURANCE-ADDITIVE`, `RISK-SCOPED` | H, AH, AJ, BP, CG, CH, CU, CV, CX, C, CW | ontology-normalized multi-effect obligation-union tests |
| `G11` Verified Review, Integration, Release & Operations | `REVIEW-EFFECTIVE-CHANGE`, `REVIEW-IDENTITY-FRESH`, `UNTRUSTED-EXECUTION-SURFACE`, `CI-CLASSIFY`, `CONFLICT-RECONCILE`, `INTEGRATION-GATE`, `SELF-AUTHORED-FRESH-REVIEW`, `POST-INTEGRATION-RECONCILE`, `RELEASE-MODEL-DISCOVER`, `INTEGRATED-NOT-DELIVERED`, `PRODUCTION-DETERMINISTIC-EFFECT`, `MIGRATION-ROLLBACK`, `PRODUCTION-GATE`, `POST-RELEASE-EVIDENCE`, `INCIDENT-CONTAINMENT`, `RELEASE-CLOSEOUT` | E, G, H, CJ, CO, CT, CS, BO, CV | complete release path tied to immutable artifact and delivery evidence |
| `G12` Zero-Chat Recoverability & Succession | `SUCCESSION-RECOVERABLE`, `RECOVERY-EVENT-DRIVEN`, `RECOVERY-AUTHORITATIVE`, `ROTATION-SIGNAL-DRIVEN`, `ROTATION-SAFE-BOUNDARY`, `CHAT-NONAUTHORITATIVE`, `ASSIGNMENT-IDENTITY` | I, Z, U, AH, AK, BB, BG, BH | formal cold-recovery benchmark with zero conversation context |
| `G13` Lean Navigable Project Knowledge | `TRUTH-ONE-OWNER`, `LEAN-ORCHESTRATION`, `RECOVERY-AUTHORITATIVE`, `CHAT-NONAUTHORITATIVE`, `ROOT-SPEC-OFF-HOT-PATH` | A, I, Z, AZ, BT, BY | bounded recovery-cost test; stale/duplicate information entropy test |
| `G14` Repository Readiness, Hygiene & Self-Repair | `BOOTSTRAP-PROPORTIONAL`, `ARTIFACT-FITNESS`, `MUTATION-IDEMPOTENT`, `DRIFT-RECONCILE`, `READY-DONE-SEMANTICS` | A, B, AU, AZ, BS, BT, BU, BE | stale project-system cleanup without parallel duplicate mechanisms |
| `G15` Proactive Improvement Without Scope Creep | `OUTCOME-STABLE`, `LEAN-ORCHESTRATION`, `ARTIFACT-FITNESS` | Y, AX, AY, BA, BT, BU, CB | improvement proposal/execute/ignore classification benchmark |
| `G16` Persistent Progress Without Friction | `ANTI-SPIN`, `SYNTHESIZE-WORK`, `MASTER-STOP-CANONICAL`, `WORKER-STOP-LOCAL`, `SELF-EXECUTION-FALLBACK`, `CAPABILITY-NOT-AUTHORITY` | O, Q, R, T, AP, AQ, AW, AX, CN, CQ | decision/tool-step benchmark before first useful action and across local blockers |

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

## Known project-level coverage gaps

The v1.0.0 regression suite is strong on safety and edge behavior, but the finalized goals require additional operational tests that are broader than one rule at a time:

1. **Project health / plan validity:** a dependency, risk, or release constraint materially changes and Master updates sequencing without rebuilding the whole project plan.
2. **Architecture evolution:** repeated current friction or architectural drift justifies a bounded enabling change; theoretical elegance alone does not.
3. **Large-project bounded context:** a multi-component or multi-repository outcome remains globally coherent while local work stays authoritative and Master progressively loads only needed context.
4. **Cold recovery cost:** a replacement Master with zero chat identifies current outcome, work graph, blockers, evidence, and next action without exhaustive reading or manager-memory files.
5. **Information entropy:** stale/duplicate project artifacts are reconciled or removed so navigation remains trustworthy as the project grows.
6. **End-to-end operational benchmark:** compare baseline and refactored Skill on useful-action latency, unnecessary tool/decision steps, ceremony, correctness, recovery, and verified completion.

These gaps are roadmap inputs, not permission to change runtime behavior before the corresponding phase and regression coverage are ready.
