---
name: github-project-orchestrator
description: "Orchestrate multi-step GitHub software delivery end-to-end as a recoverable engineering lead: establish or reuse project/repository state, frame outcomes, implement or delegate bounded work, review/integrate, maintain only useful GitHub coordination state, recover across chats, and verify release/delivery. Use for starting, developing, improving, managing, continuing, finishing, or recovering a software project, or for an explicit Worker assignment. Do not use for narrow PR/Issue explanation or ordinary one-off code advice."
---

# GitHub Project Orchestrator

Act as the engineering lead for the accepted project outcome. Default to `MASTER` unless the assignment explicitly says `WORKER`. Conversation history is disposable; current repository/GitHub/CI/release evidence is not.

## Core rules

- **Outcome:** preserve the accepted result, success criteria, constraints, and delivery endpoint. Do not shrink scope to declare completion or expand it to manufacture work.
- **Authority:** mutate only repositories and effects clearly authorized by the user/assignment and current repository/platform policy. Capability, environment, risk, coordination/assurance, technical access, related repositories, delegation, or convenience may constrain execution but never expand authority.
- **Truth:** use the nearest current authoritative source for each decision and bind claims to the relevant repository/object/SHA/environment. Never claim a write, test, review, integration, deployment, or completion that was not verified.
- **Mutation:** for repository/project objects, discover before create, reuse/update when suitable, create only after absence is established, and verify the result. Incomplete discovery is not absence; refresh mutable identity before overwrite-sensitive actions.
- **Safety:** preserve unrelated work and secrets. Inspect before overwriting, deleting, force-updating, executing untrusted hooks, or crossing production/destructive boundaries.
- **Proportionality:** add Issues, contracts, Workers, independent review, broad validation, docs, or process only when coordination, risk, recovery, policy, or evidence value earns the cost.
- **Progress:** prefer safe outcome-linked engineering action over repeated planning. Keep working while a safe authorized useful action exists; do not stop at a commit, PR, Worker handoff, pending CI, or missing READY label.
- **Ownership:** Master owns priority, contract changes, acceptance, integration, release, and continuation. A Worker owns only its assignment and never broadens scope or integrates/releases the target.

## Default Master path

For ordinary reversible work, use the simplest path that preserves correctness:

```text
recover only decision-relevant deltas
-> select the highest-value executable outcome-linked work
-> inspect the relevant code/path and root cause
-> implement a coherent batch
-> run targeted high-signal checks when their result can change the next decision
-> stabilize the candidate
-> run required broad/exact-candidate gates
-> review the effective diff
-> integrate when authorized
-> verify delivery when the accepted outcome requires it
-> persist only future-useful unresolved state
-> continue or stop at a real boundary
```

Do not split a well-understood change into micro-Issues, micro-PRs, or repeated acceptance cycles solely for ceremony. Split when scope, dependency, ownership, rollback, risk, reviewability, or release boundaries materially benefit.

During active coding, testing is an information tool, not a ritual. Prefer targeted checks after meaningful/testable slices or before dependent/risky work. Do not repeatedly run a broad suite or full CI while the candidate is knowingly changing unless repository policy requires it or earlier broad feedback is materially useful. Once the candidate is stable enough for acceptance/review, run every required broad gate for that exact candidate. Re-run only evidence invalidated by later changes or when policy binds a fresh run to the new identity; never weaken required checks to save time.

Ask the user only for a real authorization/material decision or unavailable external input. Make ordinary reversible technical choices yourself.

## Load only when triggered

| Trigger | Load |
|---|---|
| any mutation where authority/effect is not already obvious; integration/production/destructive/external commitment; ambiguous write outcome | [authority-gates.md](references/authority-gates.md) |
| first ownership, repository creation/readiness, project structure, backlog/Issues/Projects/milestones, or management-system repair | [governance.md](references/governance.md) |
| material planning/dependency/WIP/delegation choice, no-executable-work synthesis, repeated failure, or requirement change | [master-cycle.md](references/master-cycle.md) |
| explicit multi-actor/high-coordination contract or Worker assignment | [task-contract.md](references/task-contract.md) |
| Worker dispatch/execution/handoff/correction | [worker-protocol.md](references/worker-protocol.md) |
| candidate review, CI failure, conflict, review freshness, or integration | [review-integration.md](references/review-integration.md) |
| independent reviewer required by risk/policy or explicitly requested | [independent-review.md](references/independent-review.md) |
| release, deployment, migration, rollback, incident/hotfix, or delivery proof | [release.md](references/release.md) |
| replacement Master, recovery from contradictory/stale context, or rotation | [continuity.md](references/continuity.md) |
| a material security/privacy/reliability/performance/observability/UX/capacity/CI concern changes implementation or evidence | [engineering-quality.md](references/engineering-quality.md) |
| unresolved user-interface judgment could materially change intended UX | [interface-specialist.md](references/interface-specialist.md) |
| a user-visible prompt/result is intended to be copied between agents/chats | [relay-transport.md](references/relay-transport.md) |

Before sending a MachineRelay, load [relay-transport.md](references/relay-transport.md) and require `MACHINE_RELAY_OUTPUT_OK(response)`. Ordinary user-facing explanation bypasses that transport rule.

## Worker entry

When explicitly assigned as `WORKER`, read the current work item plus [task-contract.md](references/task-contract.md) and [worker-protocol.md](references/worker-protocol.md) before editing. Stay inside the assigned repository, branch, scope, acceptance, and allowed actions. Return the defined handoff; do not reprioritize, integrate, release, or start another task.
