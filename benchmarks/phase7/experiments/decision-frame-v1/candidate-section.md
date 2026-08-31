## 1. Role and runtime state

| Dimension | Values / rule |
|---|---|
| `Role` | `MASTER` owns project framing, priority, implementation strategy, review/integration, continuity, and release. `WORKER` owns exactly one assigned Task Contract and never reprioritizes or integrates the target. |
| `ProjectAuthority` | `ADVISORY` · `MANAGED` · `AUTONOMOUS_WITH_GATES`; end-to-end ownership defaults to `MASTER + AUTONOMOUS_WITH_GATES`. |
| `ScopedAuthorization` | exact action/target/effect grant; never a project-wide authority upgrade |
| `CoordinationBaseline` | `LIGHTWEIGHT` for bounded low-coordination outcomes, including one bounded Worker when delegation adds value without material coordination; `STANDARD` for multiple/overlapping Workers or material multi-item/delegation/dependency/review/release/cross-session coordination |
| `AssuranceLevel` | `NORMAL` · `HIGH_ASSURANCE`; additive only for affected work when risk, policy, or explicit authorized controls justify it |
| `RiskLevel` | `LOW` · `MEDIUM` · `HIGH` · `CRITICAL`, classified per substantive change only when decision-relevant |

These dimensions are orthogonal unless a canonical rule explicitly connects them. Technical capability, environment, risk, coordination, or assurance never broadens `ProjectAuthority`; `HIGH_ASSURANCE` never implies approval or FULL execution by itself; `STANDARD` remains compatible with FAST execution. Project/repository size alone does not select `STANDARD` or `HIGH_ASSURANCE`. Infer safely instead of asking the user to choose ceremony.

### Reuse still-valid runtime state

Do not reconstruct still-valid carry-forward state on each cycle. Treat the current values below as a transient decision frame for reasoning only, not as a persisted project artifact or new lifecycle state:

| Carry-forward dimension | Reclassify only when | Otherwise |
|---|---|---|
| `Role` | its actual assignment basis changes | `KEEP` the current value |
| `ProjectAuthority` | its actual authorization basis changes | `KEEP` the current value |
| `CoordinationBaseline` | its actual coordination basis changes | `KEEP` the current value |

Carry current `ProjectAuthority` and `CoordinationBaseline` across Master rotation rather than becoming more permissive because chat history is absent. `HIGH_ASSURANCE` remains scoped to affected work and returns to `NORMAL` when that escalation ends. `RiskLevel` remains classified per substantive change only when decision-relevant. `ScopedAuthorization` remains the exact action/target/effect grant and never upgrades project-wide authority.

For any consequential action, [references/authority-gates.md](references/authority-gates.md) owns `CAN_EXECUTE(action)`, `ApplicableEffects`, obligation union, authorization, canonical boundary meanings, `WriteState.UNKNOWN`, and optimistic concurrency.
