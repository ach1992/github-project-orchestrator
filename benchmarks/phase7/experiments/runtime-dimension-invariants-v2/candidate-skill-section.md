## 1. Role and runtime state

| Dimension | Values / responsibility | Stability / non-implication |
|---|---|---|
| `Role` | `MASTER` owns project framing, priority, implementation strategy, review/integration, continuity, and release. `WORKER` owns exactly one assigned Task Contract and never reprioritizes or integrates the target. | `KEEP` until the actual assignment basis changes. |
| `ProjectAuthority` | `ADVISORY` · `MANAGED` · `AUTONOMOUS_WITH_GATES`; end-to-end ownership defaults to `MASTER + AUTONOMOUS_WITH_GATES`. | `KEEP` until the actual authorization basis changes. Capability, environment, risk, coordination, or assurance never widens it; chat/Master rotation never makes it more permissive. |
| `ScopedAuthorization` | exact action/target/effect grant | Never upgrades project-wide `ProjectAuthority`. |
| `CoordinationBaseline` | `LIGHTWEIGHT` for bounded low-coordination outcomes, including one bounded Worker when delegation adds value without material coordination; `STANDARD` for multiple/overlapping Workers or material multi-item/delegation/dependency/review/release/cross-session coordination | `KEEP` until the actual coordination basis changes, including across Master rotation. `STANDARD` remains FAST-compatible and never implies FULL. |
| `AssuranceLevel` | `NORMAL` · `HIGH_ASSURANCE` | Apply `HIGH_ASSURANCE` only to affected work when justified by risk, policy, or explicit authorized controls; return to `NORMAL` when that escalation ends. It never implies approval or FULL. |
| `RiskLevel` | `LOW` · `MEDIUM` · `HIGH` · `CRITICAL` | Classify per substantive change only when decision-relevant. |

Dimensions remain orthogonal unless a canonical rule explicitly connects them. Project/repository size alone selects neither `STANDARD` nor `HIGH_ASSURANCE`. Infer safely instead of asking the user to choose ceremony.

For any consequential action, [references/authority-gates.md](references/authority-gates.md) owns `CAN_EXECUTE(action)`, `ApplicableEffects`, obligation union, authorization, canonical boundary meanings, `WriteState.UNKNOWN`, and optimistic concurrency.
