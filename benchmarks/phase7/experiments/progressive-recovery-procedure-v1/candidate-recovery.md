## 2. Recovery sequence

A new/replacement Master enters `RECOVER` before consequential project mutation. Recover progressively and stop reading as soon as current authoritative state is decision-valid for the next action:

| Recovery layer | Required work |
|---|---|
| **Orientation spine** | Identify repository/repositories, target/default branches, checkout/worktrees, repository rules, and current capabilities. Read an existing lightweight Project Map/index if present, then only durable docs relevant to current work. Establish the current project outcome/completion model, recover `ProjectAuthority` and `CoordinationBaseline` independently, recover any affected `AssuranceLevel` and exact current `ScopedAuthorization`, and identify the active critical path/workstream. Treat the canonical root project specification as triggered depth: do not load it merely because chat is absent. |
| **Active-path context** | Inspect active Issues/milestones/Projects/risks/assignments and open PRs/reviews/checks/branches/dependencies; inspect recent Git/release/deployment state only as needed. Enter only the current Issue/contract, PR/branch/CI, direct dependencies/interfaces, blockers/risks, and integration/delivery state needed for the next decision. Reconcile contradictions and stale assignments. Determine the review queue, controlling blockers, `DeliveryRequirement`/`DeliveryTarget`/`DeliveryState`, current candidate/review state, and next executable action. |
| **Triggered depth** | Load broader architecture, other workstreams, the canonical root project specification, historical decisions, or release history only when a contradiction, dependency, interface, risk, or project-level decision makes that context materially relevant. Load the root specification when project-level intent cannot be established safely from current downstream authoritative state or when material contradiction/change makes it decision-relevant. |

Once repository/target identity, active outcome, controlling dependencies/blockers, current `ProjectAuthority`/`CoordinationBaseline`/affected `AssuranceLevel`, current candidate/review/delivery state, and the next executable action are decision-valid, continue the valid plan instead of rebuilding it because chat history is absent. A large repository or long-lived project is a reason to narrow recovery by workstream, not to read more by default.

