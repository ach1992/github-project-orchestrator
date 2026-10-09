# Goal Map

This map proves that the simplified runtime still covers every canonical goal in `docs/PROJECT-SPEC.md`. It maps goals to behavior, not to historical implementation vocabulary.

| Goal | Canonical rules | Eval anchors | Coverage |
|---|---|---|---|
| `G01` Verified End-to-End Delivery | `OUTCOME-INTEGRITY`, `INTEGRATION-GATE`, `DELIVERY-PROOF`, `PERSISTENT-PROGRESS` | D, AB, W | Own work through the accepted integration/delivery endpoint and prove completion. |
| `G02` Outcome & Scope Integrity | `OUTCOME-INTEGRITY`, `IMPROVEMENT-SCOPE` | U, W, Y | Preserve accepted scope; reconcile genuine requirement change; do not manufacture work/completion. |
| `G03` Adaptive Planning & Decomposition | `MEANINGFUL-SLICING`, `PROPORTIONAL-PROCESS`, `PERSISTENT-PROGRESS` | B, S, X | Use the smallest meaningful hierarchy/slice needed for execution instead of micro-management. |
| `G04` Dependency, Flow & Project Health Management | `PERSISTENT-PROGRESS`, `MEANINGFUL-SLICING`, `DELEGATION-VALUE` | O, R, S, T | Prioritize critical path, unblock, manage WIP, and continue independent work. |
| `G05` Professional Engineering Execution | `ENGINEERING-FITNESS`, `VALIDATION-ECONOMICS`, `MUTATION-SAFETY`, `INTERFACE-COMPOSITION` | A, C, E, AE | Trace root cause, implement coherent maintainable changes, validate proportionally, protect unrelated work. |
| `G06` Architecture & Engineering-System Fitness | `ENGINEERING-FITNESS`, `IMPROVEMENT-SCOPE` | F, Y | Preserve fit architecture and improve systems only when evidence/payoff justifies it. |
| `G07` Engineering Quality & Evidence | `EVIDENCE-TRUTH`, `VALIDATION-ECONOMICS`, `REVIEW-FRESHNESS`, `MUTATION-SAFETY`, `DEFENSIVE-SECURITY-CONTINUITY`, `SECURITY-REVIEW-BOUNDARY` | C, D, E, F, AG, AA, AJ | Use current evidence, required validation, and relevance-driven quality controls. |
| `G08` Scale-Adaptive Coordination | `PROPORTIONAL-PROCESS`, `MEANINGFUL-SLICING`, `DELEGATION-VALUE`, `LEAN-KNOWLEDGE` | B, N, O, X | Keep bounded work light while supporting multi-actor/project coordination when it repays cost. |
| `G09` Professional Delegation & Ownership | `DELEGATION-VALUE`, `WORKER-BOUNDED`, `ASSIGNMENT-IDENTITY`, `WORKER-HANDOFF-PRECEDENCE` | N, O, P, Q, R | Delegate only for net value; Worker stays bounded; Master retains integration/release ownership. |
| `G10` Authority, Risk & Safety Integrity | `AUTHORITY-SCOPE`, `MUTATION-SAFETY`, `UNKNOWN-WRITE`, `OPTIMISTIC-CONCURRENCY`, `MATERIAL-DECISION`, `DEFENSIVE-SECURITY-CONTINUITY` | G, H, I, J, K, L, M, AG | Apply controls to actual effects/authorization without turning capability or risk into authority. |
| `G11` Verified Review, Integration, Release & Operations | `REVIEW-FRESHNESS`, `INDEPENDENT-REVIEW-SEPARATION`, `INTEGRATION-GATE`, `RELEASE-MODEL-DISCOVER`, `DELIVERY-PROOF`, `INCIDENT-CONTAINMENT`, `SECURITY-REVIEW-BOUNDARY` | Z, AA, AB, AC, AH, AI, AK | Bind review/integration to current change identity and verify release/delivery. |
| `G12` Zero-Chat Recoverability & Succession | `RECOVERY-AUTHORITATIVE`, `RECOVERY-PROPORTIONAL`, `ASSIGNMENT-IDENTITY`, `LEAN-KNOWLEDGE`, `MACHINE-RELAY` | P, V, AD, AL | Recover correct continuation from authoritative systems without old chat. |
| `G13` Lean Navigable Project Knowledge | `LEAN-KNOWLEDGE`, `REPOSITORY-READINESS` | V, X | Keep a small authoritative knowledge graph/index and avoid manager-memory duplication. |
| `G14` Repository Readiness, Hygiene & Self-Repair | `REPOSITORY-READINESS`, `ENGINEERING-FITNESS`, `MUTATION-SAFETY`, `MUTATION-IDEMPOTENT` | A, X, Y, AF | Discover/reuse safely, bootstrap proportionally, and repair demonstrated execution-system defects. |
| `G15` Proactive Improvement Without Scope Creep | `IMPROVEMENT-SCOPE`, `OUTCOME-INTEGRITY` | U, Y, W | Classify required/in-scope/adjacent/speculative improvements without silent scope growth. |
| `G16` Persistent Progress Without Friction | `PERSISTENT-PROGRESS`, `PROPORTIONAL-PROCESS`, `USER-STOP` | M, R, S, T, W | Continue while safe useful work exists, stop at real boundaries, and avoid blind/redundant process. |

## Coverage rule

A runtime change is acceptable only when:

1. every G01-G16 remains mapped to at least one current canonical rule;
2. every mapped rule has a current runtime owner;
3. representative evaluation scenarios cover the changed behavior and its dangerous counterexample;
4. validation checks semantics/structure rather than exact historical wording unless literal output is itself the contract.
