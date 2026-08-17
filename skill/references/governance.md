# Project Governance and Repository Readiness

Use this reference to establish a professional project system without imposing unnecessary ceremony.

## Contents

[Principle](#1-governance-principle) · [Project brief](#2-project-brief) · [Planning](#3-planning-hierarchy) · [GitHub state](#4-github-state-model) · [Project navigation](#5-project-navigation-and-link-discipline) · [Labels](#6-label-taxonomy) · [Ready/Done](#7-definition-of-ready-and-done) · [Risk](#8-risk-management) · [Decisions](#9-decision-management) · [Readiness audit](#10-repository-readiness-audit) · [Agent instructions](#11-agent-instructions) · [Coordination/assurance](#12-coordination-and-assurance-minimums) · [Bootstrap test](#13-bootstrap-completion-test)

## 1. Governance principle

Audit the existing repository and GitHub workflow first. Preserve good conventions, but do not equate existence or basic functionality with fitness for the current delivery outcome. Add, repair, simplify, or improve only when current evidence shows a concrete execution, quality, coordination, release, security, recovery, or recurring-delivery friction and the expected benefit over the remaining accepted work justifies implementation, maintenance, cognitive/operational complexity, and regression risk. Prefer improving or reusing an existing mechanism over adding a parallel system.

A management artifact or engineering-system improvement must earn its maintenance cost. Do not run periodic optimization audits; reassess fitness when evidence exposes a bottleneck, recurring manual/review/CI cost, repeated defect blind spot, recovery friction, or a material change in project scale, architecture, or delivery constraints.

## 2. Project brief

For first end-to-end ownership, treat the user-supplied or already-repository-resident project-defining prompt/specification as the root input from which the project is shaped. It may be concise or detailed and may have any name. Keep one canonical durable repository copy: reuse an existing equivalent when it already represents the accepted project intent; otherwise persist the supplied source in the most natural documentation location. Preserve its substantive project intent rather than replacing it with a lossy summary merely for orchestration convenience.

Before establishing or updating the canonical root specification, exclude material that should not live in the repository, such as credentials/private keys/tokens, repository-policy-prohibited sensitive data, or temporary operational/chat instructions whose persistence would be unsafe or misleading. Do not silently discard needed information: tell the user what was excluded and why, place it in an appropriate authorized secure/runtime source when available, or identify the exact alternative handling needed. If unsafe material is already tracked, do not assume deleting the current file removes prior exposure; handle any required credential rotation/history remediation under the existing security/ProjectAuthority/ApplicableEffects gates. Continue independent safe work instead of turning sanitation or remediation into a new global stop.

Use the root specification for project-level intent and durable high-level requirements, then derive the minimum useful repository/docs/task/engineering system from it plus current repository reality. Detailed architecture, engineering rules, live backlog/status, Task Contracts, validation, and deployment truth stay in their natural authoritative sources; do not mirror them back into the root specification. The root specification is a living project-level document only when accepted project intent materially changes, not a daily work log or status dashboard.

Ensure future contributors can discover, from durable sources where appropriate:

- problem/opportunity and intended users;
- current outcome and measurable success criteria;
- non-goals and durable constraints;
- supported environments/platforms and important compatibility boundaries;
- material assumptions that would change the plan if false.

Use existing README/docs when adequate. Create another project-context document only if this information is otherwise fragmented or missing and will remain useful; do not create a second root specification merely to satisfy a filename/template convention.

## 3. Planning hierarchy

Prefer:

`Project outcome -> Milestone/Release -> Issue/Task Contract -> PR/Commit`

Use epics/parent Issues only when the milestone is too broad to coordinate directly.

When ordering READY work, consider critical-path impact, blocker unlocks, correctness/security risk, user/business value, cost of delay, reversibility, and available capacity. Use explicit priority fields/labels only when they improve coordination; do not let a static priority label override current dependency or production reality.

Milestones should represent coherent outcomes or release boundaries, not arbitrary time buckets unless the team already uses time-boxed planning. Treat a requested date as a constraint, not proof of feasibility: do not invent ETAs. Forecast from current scope, dependencies, risk, and available capacity; when date, scope, and required quality/risk controls conflict, surface the trade-off instead of silently promising all three.

If one outcome spans multiple repositories/services, keep one coherent cross-repository outcome/release view while preserving each repository's own rules, Issues/PRs, CI, and ownership. The cross-repository view should contain only the global outcome/completion model, material cross-repository dependencies, release/integration order, and ownership/handoff links needed to coordinate them. Keep implementation status and local backlog in each repository's natural authoritative sources; do not create a duplicate central backlog that mirrors every repo.

Scale coordination by **coordination shape**, not repository size. When a large project has separable components or workstreams, partition execution into bounded workstream contexts instead of loading the full project into every decision. Persist a workstream boundary only when it materially improves coordination or recovery, and keep it minimal: the outcome slice, responsible owner/Worker or component boundary, authoritative local work source, material interfaces/dependencies, and integration/release handoff. Do not mirror local task status into a central workstream document.

Reassess plan validity when a material dependency, risk, architecture/interface assumption, ownership boundary, or release constraint changes. Revalidate only the affected workstream(s), critical-path relationships, and integration/release assumptions first; widen only when the change actually propagates. Do not turn plan-health checking into a recurring audit program.

## 4. GitHub state model

Use GitHub features intentionally:

- **Issues**: authoritative unit of persisted unresolved actionable work when a durable work item is warranted.
- **Milestones**: outcome/release grouping with clear completion criteria.
- **Projects**: use when cross-Issue workflow/roadmap visibility materially helps; do not create one for a tiny backlog merely for formality.
- **Labels**: classification and filtering, not a duplicate database of every attribute.
- **PRs**: implementation/review/integration record.
- **Discussions**: only when deliberation/community workflow fits better than an Issue.

Do not represent the same `TaskState` simultaneously in labels, Issue title prefixes, Project fields, and docs unless an existing integration requires it.

Before mutating GitHub management state, use the default idempotent pattern:

`DISCOVER -> REUSE/UPDATE -> CREATE ONLY IF ABSENT -> VERIFY`

When creation depends on absence, a bounded, paginated, truncated, or explicitly incomplete result is not proof of absence. Narrow the authoritative lookup to the relevant object identity or semantic equivalence first; stop as soon as an equivalent object is found; refine the query or follow pagination only as far as needed to establish decision-scoped absence. Do not exhaustively crawl unrelated repository state when a targeted lookup can answer the decision, and do not create merely because the first bounded/page result contains no match.

For ambiguous write outcomes or overwrite-sensitive updates, use the canonical `WriteState.UNKNOWN` and optimistic-concurrency protocols in `authority-gates.md`; do not duplicate them here. Examples: reuse an equivalent open Issue, update an existing compatible label/milestone instead of cloning it, verify branch/PR identity before push/retarget, and never overwrite newer project/contract/priority state from a stale read.

## 5. Project navigation and link discipline

Make the project understandable as a navigable graph of authoritative artifacts, not as a duplicated manager-memory document.

If discovery is materially fragmented, add one lightweight **Project Map** in the most natural durable location (prefer a short README section; otherwise a small `docs/project-map.md` or existing equivalent). The map is an index of **where truth lives**, not a status report. Point only to durable locations such as product/purpose, architecture, engineering rules, active GitHub Project/backlog, milestones/releases, ADR/decision area, release runbook, and deployment/operations source.

Update the Project Map only when the information topology changes: an authoritative system/file is introduced, moved, renamed, replaced, or retired. Do **not** update it for routine task progress, changing percentages, transient blockers, individual commits, or information already discoverable from GitHub/Git. Remove stale pointers when their target stops being authoritative.

Maintain relationship links as work evolves, using native GitHub relationships/closing keywords/URLs where possible: milestone or parent -> Issue, Issue -> dependency/blocker, PR -> Issue/Task Contract, Issue/PR -> lasting ADR when relevant, and release/deployment -> immutable commit/artifact identity. Add only links that improve navigation, dependency reasoning, review, release traceability, or recovery; do not mirror the same state in prose.

When the Project Map or a relationship is stale or duplicated, repair/remove the pointer and correct the underlying authoritative owner if its state is wrong. Do not add compensating notes, shadow status, or another index to explain stale truth. A replacement Master should be able to start from the Project Map (when present), select the relevant workstream/repository, and traverse authoritative links to current work without reading historical chat or the entire project corpus.

## 6. Label taxonomy

Prefer the repository's existing coherent taxonomy. If one is missing, introduce the smallest useful namespaced set.

Recommended dimensions:

- `type:bug`, `type:feature`, `type:chore`, `type:docs`, `type:spike`;
- `priority:p0` through `priority:p3` only when priority needs explicit filtering;
- `risk:high` / `risk:critical` only when materially useful; normal RiskLevel can remain in the Task Contract;
- `area:<component>` only for stable ownership/component boundaries;
- `blocked` only if blockage is not already represented cleanly by the repository's TaskState/Project state;
- `security` for security-sensitive work where discovery/filtering matters.

Avoid decorative labels, overlapping synonyms, and status labels when a Project status field already owns workflow state. A label named `blocked` is a repository filtering convention; it does not imply `MasterBoundary.BLOCKED` or `WorkerStatus.BLOCKED` by token equality.

Document label meaning only when not self-evident or when automation depends on it.

## 7. Definition of Ready and Done

Keep controls proportional to `CoordinationBaseline`, `AssuranceLevel`, and RiskLevel.

Use the execution-path and READY rules in `task-contract.md`; do not maintain a second checklist here. Bounded low/medium-risk Master-only behavioral work may stay on `ExecutionPath=FAST` when it is already clear enough to execute safely, including within `CoordinationBaseline=STANDARD` when FAST criteria still hold.

Treat integration and delivery as separate facts. A task becomes `TaskState.INTEGRATED` when its accepted implementation is merged/applied to the intended Integration Target and verified there. Final closeout depends on `DeliveryRequirement`: integration is enough for `INTEGRATION_ONLY`; `DELIVERY_REQUIRED` work remains open until the intended artifact reaches its explicit `DeliveryTarget` and is verified `DeliveryState.DELIVERED`.

Do not keep an Issue open merely for ceremony when delivery is explicitly out of scope, and do not close delivery-required work merely because its PR merged. `TaskState`, `DeliveryState`, `WorkerStatus`, and `MasterBoundary` are independent namespaces. Represent actionable follow-ups separately.

`CoordinationBaseline=LIGHTWEIGHT` Master-only FAST work needs no separate contract artifact when intent is already clear and recoverable. `CoordinationBaseline=STANDARD`, delegated work, or other cross-session/recovery needs should persist only the contract/state needed for coordination or recovery. `AssuranceLevel=HIGH_ASSURANCE` adds risk-control evidence to affected work but does not by itself force FULL, a new persistent contract, or a new human confirmation.

## 8. Risk management

Track only active material RiskLevel-related risk. For each material risk, maintain:

- condition/cause;
- impact/blast radius;
- mitigation or contingency;
- owner/next action when relevant;
- trigger that requires escalation or approval.

Do not retain resolved risk logs unless the consequence remains a durable operating constraint.

## 9. Decision management

Create an ADR or equivalent durable decision record only when the accepted decision has lasting architectural/product/operational consequences and future maintainers need the rationale or constraints.

Small reversible implementation choices belong in code/PR review, not ADRs.

An ADR should capture context, decision, key alternatives/tradeoffs, consequences, and status. Do not use ADRs as meeting minutes.

## 10. Repository readiness audit

Check only what the project actually needs. Presence is not enough when a current mechanism repeatedly slows, obscures, or weakens the accepted delivery path; improve it only when the near-term net benefit is material:

- README/setup is reproducible enough for a new developer;
- dependency/runtime/tool versions are discoverable;
- build/test/lint/type/security commands are authoritative and runnable;
- environment variables and secret handling are documented safely;
- generated files and local artifacts are ignored appropriately;
- CI runs the important validation for target branches;
- branch/PR conventions and required checks are discoverable;
- release/deployment path is understood for delivery-required projects;
- ownership or escalation route exists where the project needs it;
- automated agents can discover relevant repository instructions without conflicting copies;
- dependency/lockfile, package-source, and CI/workflow changes are reviewable enough to detect unexpected supply-chain changes when material.

Do not add CI, templates, `AGENTS.md`, codeowners, ADRs, Projects, or release automation just because they are common. Add them only when they solve a current durable need.

## 11. Agent instructions

If coding agents are part of the workflow, prefer one root `AGENTS.md` plus narrowly scoped nested files only where a subtree genuinely needs different rules.

Keep agent instructions stable and implementation-oriented: setup, commands, conventions, boundaries, test expectations, generated files, unsafe actions, and relevant architecture invariants.

Do not turn `AGENTS.md` into a live backlog, worker registry, or Master handoff store.

## 12. Coordination and assurance minimums

### `CoordinationBaseline=LIGHTWEIGHT`

Use for a bounded outcome with low coordination overhead and no material multi-item dependency, migration, production/release coordination, or security/data blast radius. One bounded delegated workstream may fit when delegation materially improves specialization or throughput without creating material coordination; it still uses the full Worker contract/READY/identity envelope and `ExecutionPath=FULL`. Prefer existing repo docs, transient or compact persisted work descriptions only when useful, targeted tests, and minimal labels. Use PRs for code when practical or when repository policy requires them. Avoid Projects/ADRs/process docs unless they solve a real need.

### `CoordinationBaseline=STANDARD`

Use when multiple substantive items, dependencies, multiple/overlapping Workers, material delegation coordination, review/release coordination, or broader cross-session project coordination materially benefit from persistent project state. Expect reproducible setup, CI for core checks, PR-based code integration when that is the repository-normal/practical control path, or an established equivalent non-PR path only when it preserves the same review/freshness/audit/gate outcomes; clear persisted contracts where coordination requires them; milestone/release tracking where useful; current engineering/release docs; and explicit active risks/decisions when material. A bounded independent change may still use `ExecutionPath=FAST` when FAST criteria hold.

Select the baseline from actual coordination needs rather than size labels:

| Representative shape | Default behavior |
|---|---|
| small/bounded | stay `LIGHTWEIGHT` while one clear path remains independently recoverable and low-coordination |
| medium/multi-item | use `LIGHTWEIGHT` for genuinely independent bounded work; select `STANDARD` when dependencies, shared ownership, review/release coordination, or cross-session state materially benefit from it |
| large/multi-repository | normally retain/select `STANDARD` when coordination needs justify it, but partition into bounded component/workstream contexts; do not create a larger profile, global task mirror, or exhaustive context load merely because the system is large |

For `STANDARD` work at scale, persist only coordination edges that change decisions: cross-workstream dependencies, ownership/handoff boundaries, shared interface assumptions, integration order, and release constraints. Local implementation truth remains in each natural repository/Issue/PR/CI source.

### `AssuranceLevel=HIGH_ASSURANCE`

Treat HIGH_ASSURANCE as an additive escalation for affected work, not a replacement for CoordinationBaseline. Retain every LIGHTWEIGHT/STANDARD coordination, persistence, and integration control that would otherwise apply, then add controls appropriate to the actual threat/blast radius: independent review, security test/review, migration rehearsal, backup/restore or rollback validation, environment separation, staged rollout, auditability, stronger release evidence, and supply-chain/provenance/license review when dependency or build-chain risk is material. Use explicit approvals only where the canonical ApplicableEffects matrix, repository/platform policy, or the authorized stronger-control requirement specifically requires them; AssuranceLevel alone is not a blanket confirmation gate.

Do not claim compliance with a regulation or standard solely because these controls exist.

## 13. Bootstrap completion test

Bootstrap is complete when the next competent developer or replacement Master can discover how to work safely and the next READY task can be executed and verified without inventing missing process.

Stop bootstrapping at that point and deliver product work.
