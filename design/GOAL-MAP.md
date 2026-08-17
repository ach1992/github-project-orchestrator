# Canonical Goal Map

Status: development-only traceability layer. Canonical goal definitions live in `../docs/PROJECT-SPEC.md`; canonical rule definitions live in `RULE-MAP.md`. This file does not redefine either.

## Purpose

Use this map to prevent refactors from optimizing local wording while losing project-level intent. Every material runtime change should identify the Goal IDs it advances and the Rule IDs/evaluations it can affect.

Mappings below are representative, not exhaustive. Rule-level completeness remains owned by `RULE-MAP.md` and evaluation completeness by `skill/references/eval-scenarios.md` plus later regression additions.

| Goal | Primary rule families / Rule IDs | Existing evaluation anchors | Additional coverage to add during refactor |
|---|---|---|---|
| `G01` Verified End-to-End Delivery | `OUTCOME-STABLE`, `POST-INTEGRATION-RECONCILE`, release/delivery rules | P, AY, CO, CT | end-to-end synthetic project from intake through required delivery |
| `G02` Outcome & Scope Integrity | `OUTCOME-STABLE`, requirement/root-spec change rules | AY, BA, BZ, CA, CB, CD, CY | cross-workstream requirement change with unaffected work continuing |
| `G03` Adaptive Planning & Decomposition | `WORK-CLEAR-ENOUGH`, `FAST-FULL-SELECT`, `SYNTHESIZE-WORK`, governance planning hierarchy | K, L, O, AB, AZ | decomposition quality across small/medium/large outcomes |
| `G04` Dependency, Flow & Project Health Management | `WIP-FLOW`, `SYNTHESIZE-WORK`, `MASTER-STOP-CANONICAL` | J, O, R, AP, CN | explicit plan-validity/critical-path-change and project-health scenarios |
| `G05` Professional Engineering Execution | self-execution discipline, `PROTECT-UNRELATED`, validation/review rules | X, Y, AC, CL | root-cause vs symptom-patch representative coding benchmark |
| `G06` Architecture & Engineering-System Evolution | `ARTIFACT-FITNESS`, `BOOTSTRAP-PROPORTIONAL`, `LEAN-ORCHESTRATION` | AZ, BS, BT, BU | architecture-drift and developer-feedback-loop improvement scenarios |
| `G07` Engineering Quality & Evidence | `EVIDENCE-BEATS-NARRATIVE`, `REVIEW-EFFECTIVE-CHANGE`, `REVIEW-IDENTITY-FRESH`, `CI-CLASSIFY` | E, F, M, AC, CL | quality benchmark spanning correctness/security/performance/operations |
| `G08` Scale-Adaptive Coordination | `COORDINATION-BASELINE`, `DIMENSIONS-ORTHOGONAL`, `DELEGATION-PROPORTIONAL`, `WIP-FLOW` | W, AB, AN, CE, CF | large/multi-repo bounded-context and component/workstream ownership test |
| `G09` Professional Delegation & Ownership | `WORKER-BOUNDED`, `ASSIGNMENT-IDENTITY`, `STALE-ASSIGNMENT`, `WORKER-STOP-LOCAL`, `WORKER-TARGET-SEPARATION` | D, R, AK, AM, AV, CK, CP, CR | multiple independent Workers with Master replacement mid-flight |
| `G10` Authority, Risk & Safety Integrity | `AUTHORITY-STABLE`, `AUTHORIZATION-SCOPED`, `CAPABILITY-NOT-AUTHORITY`, `EFFECT-ACTUAL`, `EFFECT-MULTI`, `GATE-UNION` | H, AH, AJ, BP, CG, CH, CU, CV, CX | ontology-normalized multi-effect obligation-union tests |
| `G11` Verified Review, Integration, Release & Operations | review/integration family, delivery/release rules | E, G, H, CJ, CO, CT | complete release path tied to immutable artifact and delivery evidence |
| `G12` Zero-Chat Recoverability & Succession | `SUCCESSION-RECOVERABLE`, `RECOVERY-EVENT-DRIVEN`, `RECOVERY-AUTHORITATIVE`, `CHAT-NONAUTHORITATIVE`, `ROTATION-SAFE-BOUNDARY` | I, Z, U, AH, AK, BB, BG, BH | formal cold-recovery benchmark with zero conversation context |
| `G13` Lean Navigable Project Knowledge | `TRUTH-ONE-OWNER`, `LEAN-ORCHESTRATION`, governance Project Map/link discipline, continuity retention test | A, I, Z, AZ, BT | bounded recovery-cost test; stale/duplicate information entropy test |
| `G14` Repository Readiness, Hygiene & Self-Repair | `BOOTSTRAP-PROPORTIONAL`, `ARTIFACT-FITNESS`, `MUTATION-IDEMPOTENT` | A, B, AU, AZ, BS, BT, BU | stale project-system cleanup without parallel duplicate mechanisms |
| `G15` Proactive Improvement Without Scope Creep | `OUTCOME-STABLE`, improvement classifier, `LEAN-ORCHESTRATION` | Y, AX, AY, BA, BT, BU, CB | improvement proposal/execute/ignore classification benchmark |
| `G16` Persistent Progress Without Friction | `ANTI-SPIN`, `SYNTHESIZE-WORK`, `MASTER-STOP-CANONICAL`, `WORKER-STOP-LOCAL` | O, Q, R, T, AP, AQ, AW, AX, CN, CQ | decision/tool-step benchmark before first useful action and across local blockers |

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

## Known project-level coverage gaps

The v1.0.0 regression suite is strong on safety and edge behavior, but the finalized goals require additional operational tests that are broader than one rule at a time:

1. **Project health / plan validity:** a dependency, risk, or release constraint materially changes and Master updates sequencing without rebuilding the whole project plan.
2. **Architecture evolution:** repeated current friction or architectural drift justifies a bounded enabling change; theoretical elegance alone does not.
3. **Large-project bounded context:** a multi-component or multi-repository outcome remains globally coherent while local work stays authoritative and Master progressively loads only needed context.
4. **Cold recovery cost:** a replacement Master with zero chat identifies current outcome, work graph, blockers, evidence, and next action without exhaustive reading or manager-memory files.
5. **Information entropy:** stale/duplicate project artifacts are reconciled or removed so navigation remains trustworthy as the project grows.
6. **End-to-end operational benchmark:** compare baseline and refactored Skill on useful-action latency, unnecessary tool/decision steps, ceremony, correctness, recovery, and verified completion.

These gaps are roadmap inputs, not permission to change runtime behavior before the corresponding phase and regression coverage are ready.
