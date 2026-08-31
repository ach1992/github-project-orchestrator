# Progressive Recovery Procedure Prototype

Tracking: #60  
Parent: #37  
Methodology: `design/LOSSLESS-RUNTIME-OPTIMIZATION.md`

## Hypothesis

`continuity.md` §2 currently represents cold Master recovery twice: an eight-step evidence sequence and an immediately following three-layer progressive-context model. Both contain useful semantics, but the model/maintainer must reconcile two overlapping organizations. A single progressive recovery procedure should reduce duplicate mapping while retaining every required recovery fact, trigger, and stop condition.

This is a Phase B representation prototype only. It does **not** modify canonical `skill/` runtime and does not claim live-model performance improvement.

## Frozen identities

- source/current-target snapshot: `9cfbc9bc57be4690796d3d9996a517cd257746c5`
- immutable semantic comparison baseline: `f98e8a242c720931e34aa7c4e8a799090e3d0495`
- target owner: `skill/references/continuity.md` §2
- candidate fragment: `candidate-recovery.md`

## Representation fit versus KEEP

The source semantic has two simultaneous properties:

1. **progressive retrieval depth** — orientation -> active path -> triggered depth;
2. **required cold-recovery evidence** — repository identity/capabilities, work-management state, PR/CI/dependencies, selective Git/release/deployment history, contradiction reconciliation, operating dimensions, delivery state, and next action.

The three-layer model is the better top-level representation because it directly expresses progressive disclosure. The eight-step list contains important required evidence but partly replays the same path in a second organization. The candidate therefore keeps the three layers as the single structure and absorbs every required item from the eight-step list into the appropriate layer.

`KEEP` would be preferable if layer consolidation weakened sequence, caused broad eager loading, hid a required evidence class, or made the decision-valid stopping rule less explicit. The candidate preserves those guards directly.

## One-to-one semantic ledger

| Source semantic | Candidate owner |
|---|---|
| replacement Master enters `RECOVER` before consequential mutation | opening sentence |
| identify repository/repositories and target/default branches | Orientation spine |
| establish checkout/worktrees, repository rules, current capabilities | Orientation spine |
| use lightweight Project Map/index when present | Orientation spine |
| load only durable docs relevant to current work | Orientation spine |
| root specification only when project-level intent is unresolved or material contradiction/change makes it relevant | Orientation spine + Triggered depth |
| establish current project outcome/completion | Orientation spine |
| recover `ProjectAuthority` and `CoordinationBaseline` independently | Orientation spine |
| recover affected `AssuranceLevel` and exact current `ScopedAuthorization` | Orientation spine |
| identify active critical path/workstream | Orientation spine |
| inspect active Issues/milestones/Projects/risks/assignments | Active-path context |
| inspect open PRs/reviews/checks/branches/dependencies | Active-path context |
| inspect recent Git/release/deployment only as needed | Active-path context |
| enter only current Issue/contract, PR/branch/CI and direct dependencies/interfaces needed for next decision | Active-path context |
| inspect blockers/risks and integration/delivery state | Active-path context |
| reconcile contradictions/stale assignments | Active-path context |
| determine review queue and controlling blockers | Active-path context |
| determine `DeliveryRequirement`/`DeliveryTarget`/`DeliveryState` | Active-path context |
| determine current candidate/review state and next executable action | Active-path context |
| broader architecture/other workstreams only on material trigger | Triggered depth |
| historical decisions/release history only on material trigger | Triggered depth |
| stop once repository/target, outcome, blockers/dependencies, operating dimensions, candidate/review/delivery state, and next action are decision-valid | final stopping paragraph |
| continue valid plan instead of rebuilding because chat is absent | final stopping paragraph |
| large/long-lived repository narrows by workstream rather than causing broader reads | final stopping paragraph |

All later §2 rules beginning with multi-repository recovery remain outside the replacement and byte-identical in materialization. This protects multi-repository global-spine/local-context behavior, legacy operating-profile recovery, bounded preflight semantics, planned branch-transition behavior, route-failure fallback, and material-drift re-recovery.

## Important semantic choice

The table rows are **progressive context layers**, not a rigid first-match state machine. Work inside a layer may use any source needed to make that layer decision-valid. The structure preserves the source rule that triggered depth is conditional rather than always loaded, while the existing later rules continue to govern when an established baseline should be retained or widened.

## Scope proof

The deterministic test must prove:

- only the overlapping recovery prefix is replaced in a materialized candidate;
- all text before §2 remains byte-identical;
- every byte beginning with `For multi-repository outcomes...` remains unchanged;
- every non-target canonical runtime file remains byte-identical;
- runtime state/boundary token surface remains unchanged;
- exactly one progressive layer table contains Orientation spine, Active-path context, Triggered depth;
- the prior duplicate eight-step sequence is not retained in the candidate;
- all protected recovery evidence/stop fragments are present;
- the materialized Skill passes normal validation;
- ledger and operational walkthrough evidence are present.

Word/line count is diagnostic only. Selection requires lower duplicate mapping with unchanged recovery correctness and progressive-disclosure boundaries.

## Selection boundary

Select for later #38 migration only if deterministic evidence and semantic review show that one progressive procedure carries the full cold-recovery contract more locally than `KEEP`. Otherwise retain the current two representations.
