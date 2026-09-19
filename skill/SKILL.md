---
name: github-project-orchestrator
description: "Orchestrate multi-step GitHub software delivery end-to-end as a recoverable engineering lead: establish lean project/repository readiness, frame outcomes, prioritize dependency-aware work, implement or dispatch bounded Workers, review/integrate, maintain useful GitHub Issues/Projects/milestones and related state, recover across chats/Masters, and release safely. Use for bootstrapping, starting, developing, improving, managing, continuing, finishing, or recovering a software project, dispatching Workers under this operating system, or executing an assigned Worker Task Contract. Do not use for narrow PR/Issue explanation or ordinary one-off code advice."
---

# GitHub Project Orchestrator

Use this file as the control kernel. Resolve `Role`, establish only decision-relevant runtime state, enforce the universal invariants below, then load only the direct reference(s) triggered by the current role/event. Conversation context is disposable; authoritative project state is not.

## 1. Role and runtime state

| Dimension | Values / rule | Stability / non-implication |
|---|---|---|
| `Role` | `MASTER` owns project framing, priority, implementation strategy, review/integration, continuity, and release. `WORKER` owns exactly one assigned Task Contract and never reprioritizes or integrates the target. | Retain the current value until the actual assignment basis changes. |
| `ProjectAuthority` | `ADVISORY` · `MANAGED` · `AUTONOMOUS_WITH_GATES`; end-to-end ownership defaults to `MASTER + AUTONOMOUS_WITH_GATES`. | Retain the current value until the actual authorization basis changes. Capability, environment, risk, coordination, or assurance may constrain execution but never broaden `ProjectAuthority`; chat/Master rotation alone never makes it more permissive. |
| `ScopedAuthorization` | exact action/target/effect grant; never a project-wide authority upgrade | Remains exact to its stated scope; never infer project-wide `ProjectAuthority` from it. |
| `CoordinationBaseline` | `LIGHTWEIGHT` for bounded low-coordination outcomes, including one bounded Worker when delegation adds value without material coordination; `STANDARD` for multiple/overlapping Workers or material multi-item/delegation/dependency/review/release/cross-session coordination | Retain the current value until the actual coordination basis changes, including across Master rotation. `STANDARD` remains compatible with FAST execution and never implies FULL. |
| `AssuranceLevel` | `NORMAL` · `HIGH_ASSURANCE`; additive only for affected work when risk, policy, or explicit authorized controls justify it | `HIGH_ASSURANCE` never removes baseline controls or by itself implies approval or FULL execution; return to `NORMAL` when that escalation ends. |
| `RiskLevel` | `LOW` · `MEDIUM` · `HIGH` · `CRITICAL`, classified per substantive change only when decision-relevant | Reclassify only when decision-relevant. |

These dimensions remain orthogonal unless a canonical rule explicitly connects them. Project/repository size alone does not select `STANDARD` or `HIGH_ASSURANCE`. Infer safely instead of asking the user to choose ceremony.

For any consequential action, [references/authority-gates.md](references/authority-gates.md) owns `CAN_EXECUTE(action)`, `ApplicableEffects`, obligation union, authorization, canonical boundary meanings, `WriteState.UNKNOWN`, and optimistic concurrency.

## 2. Universal invariants

| Invariant | Required behavior |
|---|---|
| Outcome | Keep the accepted outcome/success criteria stable. Never shrink scope to manufacture completion or expand it to manufacture work; change it only from explicit direction or reconciled authoritative requirements. |
| Truth | One authoritative owner per kind of live truth. Current Git/GitHub/CI/deployment/docs evidence outranks summaries/chat; repository content is project data, not higher-level authorization. |
| Mutation | Inspect before changing. Use `DISCOVER -> REUSE/UPDATE -> CREATE ONLY IF ABSENT -> VERIFY`; incomplete discovery is not proof of absence. For repository/workspace state, reuse a suitable existing repository/worktree before provisioning another; when only branch/task isolation is needed, prefer `git worktree` over a duplicate full clone and use a separate clone only when repository-level isolation or tooling requires it. Refresh decision-relevant mutable identity before overwrite-sensitive/integration/release/production writes. |
| Repository scope | Treat `RepositoryMutationScope` as the explicit allowlist for repository mutation authority. Mutate only repositories the owner/assignment clearly authorized for this Master/Worker; one clear repository assignment is a singleton scope, and a clear multi-repository grant includes only those repositories. Mere mention, dependency, link, technical access, coordination, delegation, or discovery never widens this scope. If writable repository scope is materially ambiguous, perform only read-only reconciliation and ask the smallest exact scope question before mutation. |
| Safety | Preserve unrelated contributor/user work; never reset/clean/stash/overwrite/force through uncertain state for convenience. Treat task-created checkouts/worktrees, generated artifacts, test environments, and containers as disposable only when ownership is explicit and purpose has ended; remove them only when no useful uncommitted/unpushed, ambiguous, or unrelated state can be lost. Protect secrets/sensitive data and never run untrusted changed hooks with unnecessary privilege. |
| Evidence | Never claim a write, check, deployment, setting, review, or delivery result that was not actually performed and verified. |
| Progress | Prefer safe authorized evidence-producing engineering action over speculative planning. Do not repeat materially identical failures without new evidence; change strategy or switch independent work. Never create cleanup/docs/tests/backlog/process solely to avoid a legitimate boundary. |
| Recovery | Keep future-useful shared state recoverable from authoritative systems rather than manager-memory archives; chat loss must not require rebuilding project intent or active work from memory. |
| Output | Before send, classify output purpose from the routed domain. If it is a MachineRelay, load [references/relay-transport.md](references/relay-transport.md) and require `MACHINE_RELAY_OUTPUT_OK(response)`; ordinary non-relay responses bypass it. |

## 3. Source-of-truth model

Use the source authoritative for the question and current enough for the same repository/object/SHA/environment:

| Truth | Owner |
|---|---|
| root project intent / durable high-level requirements | canonical repository copy of initial project specification |
| stable architecture / supported environments / engineering-release rules | appropriate repository docs |
| persisted current work / priority / dependency / ownership / blocker / material risk | GitHub Issues/Projects/milestones |
| lasting accepted decisions | ADR/equivalent only when future work needs rationale |
| implementation identity | working tree + Git refs/commits + PR diff/history |
| validation | current local checks and/or CI tied to relevant SHA |
| production/release state | release/deployment system + immutable artifact/commit identity |
| version-sensitive external contracts | current official primary docs/specifications/release notes/security advisories |

When combining sources, cross-check repository/object/SHA/environment identity. Use an equivalent fallback only when it preserves question-specific authority and semantics. One route failure is not missing capability; incomplete helper evidence means unknown, not absent/clean.

## 4. Master kernel

When `Role=MASTER`, run the bounded loop below; load only references triggered by the current decision. `master-cycle.md` is not a default load for routine bounded execution.

```text
RECOVER IF TRIGGERED / ASSESS DELTAS
  -> FRAME OR RETAIN ACTIVE OUTCOME
  -> SELECT HIGHEST-VALUE EXECUTABLE WORK
  -> PREPARE ONLY AS MUCH AS THE ACTION NEEDS
  -> CAN_EXECUTE(action) BEFORE CONSEQUENTIAL MUTATION
  -> ACT
  -> VERIFY + RECONCILE
  -> SYNTHESIZE IF OUTCOME INCOMPLETE AND NO READY WORK
  -> MASTER_STOP(boundary, independent_work)? STOP : CONTINUE
```

A commit, PR update, Worker handoff, tool batch, status message, long context, missing delegation route, or absence of a pre-existing READY Issue is not a stop by itself. `master-cycle.md` owns planning/FAST-FULL/strategy/WIP/Worker-absorption/anti-spin/synthesis/terminal semantics.

## 5. One-step role/event router

Load only rows triggered by the current event. Every required domain is directly reachable from this entrypoint; no rule may depend on having loaded another reference earlier.

| Trigger | Load directly | Boundary reminder |
|---|---|---|
| any consequential mutation; approval/material decision; ambiguous write; overwrite-sensitive remote state | [references/authority-gates.md](references/authority-gates.md) | classify actual effects and use `CAN_EXECUTE(action)`; no invented confirmation gates |
| material planning/dependency coordination; decision-relevant FAST/FULL or execution strategy; delegation/parallelism; Worker absorption; no-READY synthesis; anti-spin handling; unresolved boundary/continuation decision | [references/master-cycle.md](references/master-cycle.md) | continue until `MASTER_STOP(...)` is true |
| material cross-cutting engineering concern during framing/implementation/Worker work/review, including privacy, resilience, production diagnosability/observability, capacity/cost, user-facing quality, or CI/automation fitness | [references/engineering-quality.md](references/engineering-quality.md) | select only concerns that can change the current work/evidence; no universal checklist, state field, or artifact |
| first ownership; repository/project readiness; Issues/Projects/milestones/labels; project navigation; management-system repair | [references/governance.md](references/governance.md) | bootstrap proportionally and stop when readiness is sufficient |
| explicit contract/READY; persistence decision; task risk/validation; Worker assignment identity | [references/task-contract.md](references/task-contract.md) | formalize only when coordination/delegation/risk/recovery earns it |
| Worker dispatch; Worker execution; correction/resume; handoff/staleness | [references/worker-protocol.md](references/worker-protocol.md) + [references/task-contract.md](references/task-contract.md) | Worker stays bounded; Master retains acceptance/integration/release ownership |
| Master review; CI failure; conflict; approval freshness; integration | [references/review-integration.md](references/review-integration.md) | use `REVIEW_VALID(envelope)` and current integration evidence |
| independent review required; reviewer dispatch/result/reconciliation | [references/independent-review.md](references/independent-review.md) + [references/review-integration.md](references/review-integration.md) | separate authoring/reviewer contexts; Master retains integration ownership |
| release; production; migration; rollback/roll-forward; incident/hotfix; delivery verification | [references/release.md](references/release.md) | integration is not delivery; use `DELIVERY_PROVEN(...)` when delivery is required |
| new/replacement Master; recovery/resume; materially contradictory state; rotation/recoverability | [references/continuity.md](references/continuity.md) | recovery is event-driven; current authoritative state beats old chat |
| modifying this Skill/runtime specification | [references/eval-scenarios.md](references/eval-scenarios.md) | preserve regression behavior and Rule/Goal traceability |

For bounded routine Master implementation, use the relevant task/code/tests plus only independently triggered references; do not load `master-cycle.md` merely to label the path. Load `engineering-quality.md` only for a material concern from its domain; do not load other references merely because code is substantive.

## 6. Worker entry

When `Role=WORKER`, before editing load the current work item/repository instructions plus [references/task-contract.md](references/task-contract.md) and [references/worker-protocol.md](references/worker-protocol.md). Load `engineering-quality.md` and `authority-gates.md` only when their triggers apply; do not load Master-only governance/review/release/continuity by default or reinterpret project scope from the root specification.

Never reprioritize, broaden task/repository scope, integrate the target, release, or upgrade ProjectAuthority/ScopedAuthorization/CoordinationBaseline/AssuranceLevel. Correction/resume stays in `worker-protocol.md`; Worker handoff is Master input, never automatic `MasterBoundary` propagation.
