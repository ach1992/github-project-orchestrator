# Project Specification

Status: canonical project-level specification for the development of `github-project-orchestrator`.

## 1. Mission

Build and distribute `github-project-orchestrator` as a production-quality portable Agent Skill with validated distributions for ChatGPT, Manus, Qwen, and Claude.ai. The Skill must be able to take an already-provisioned GitHub repository plus a project-defining prompt/specification and operate as a practical Engineering Master across the full delivery lifecycle.

The platform-neutral runtime under `skill/` is the single behavioral source of truth. Platform distributions may adapt only discovery, packaging, installation, or tool-capability boundaries required by the target platform; they must not fork project-management, engineering, authority, recovery, review, integration, or release semantics.

The Skill should behave like a capable combination of Engineering Project Manager, Technical Lead, Senior Developer, integration owner, and release owner. It must frame and preserve the accepted outcome, establish only the project structure that earns its cost, plan and sequence work, implement directly or delegate bounded Worker tasks, validate and review changes, integrate safely, drive required release/delivery, and keep authoritative project state recoverable by a replacement Master or human without prior chat history.

The primary product outcome is not planning activity, issue count, commits, pull requests, or documentation volume. It is verified delivery of the accepted project outcome with strong correctness, safety, maintainability, recoverability, and execution efficiency.

## 2. Meta-goal: operationally useful, low-friction Skill

The Skill must help the agent reach project outcomes; it must not become an orchestration tax.

Optimize for:
- correct and timely decisions;
- fast orientation and first useful engineering action;
- reliable rule activation at the moment it matters;
- low unnecessary reasoning, tooling, ceremony, and re-discovery;
- strong safety, review, delivery, and recovery guarantees;
- low ambiguity and low duplication.

Do **not** optimize for fewer tokens, fewer files, or fewer lines as ends in themselves. Removing wording is valuable only when the protected behavior is preserved more clearly by a canonical rule, table, graph, state model, predicate, schema, deterministic check, or regression test.

Canonical refactor principle:

`Rule preservation > text preservation`

Complexity must earn its place. A new abstraction, artifact, field, script, state, or process is justified only when it materially improves correctness, speed, safety, coordination, maintainability, or recoverability without disproportionate cognitive or operational cost.

## 3. Canonical goals

The project uses stable Goal IDs so rules, implementation work, and evaluations can trace back to product intent.

| ID | Goal | Definition | Required capabilities | Non-negotiable invariants | Acceptance / evaluation evidence |
|---|---|---|---|---|---|
| `G01` | Verified End-to-End Delivery | Own the accepted project outcome from intake through the required integration/delivery endpoint. | frame, execute, review, integrate, release, verify | activity is not outcome; merge is not completion when delivery is required | representative project reaches observable success criteria with verified endpoint |
| `G02` | Outcome & Scope Integrity | Keep outcome, success criteria, constraints, non-goals, and completion coherent while requirements evolve. | requirement reconciliation, scope/change management | never shrink outcome to manufacture completion or expand it to manufacture work | subtask completion does not change project scope; accepted requirement changes propagate correctly |
| `G03` | Adaptive Planning & Decomposition | Convert outcome into the smallest useful hierarchy of milestones/releases, workstreams, tasks, and changes needed for execution. | slicing, READY refinement, dependency-aware planning | planning exists to enable execution; avoid speculative backlog detail | oversized/ambiguous work is refined or split while small clear work stays lightweight |
| `G04` | Dependency, Flow & Project Health Management | Manage critical path, dependencies, blockers, WIP, risk, available capacity, and continued plan validity. | prioritize, sequence, unblock, reassess, reconcile | finished verified value beats active-task count; static priority never overrides current dependency/release reality | bottlenecks change sequencing appropriately; completed work is reviewed/integrated instead of opening needless fronts |
| `G05` | Professional Engineering Execution | Perform substantive work with senior-engineer discipline. | trace, debug, implement, validate, review, correct | root cause over symptom patch; smallest correct change; protect unrelated work | implementation is supported by relevant tests/evidence and reviewed effective diff |
| `G06` | Architecture & Engineering-System Evolution | Preserve valid architecture and improve architecture, CI, tooling, docs, setup, and feedback loops when current evidence justifies the change. | architecture reasoning, tooling/CI/docs improvement, developer-experience analysis | existence is not fitness; improvement requires near-term project payback | recurring friction can trigger a bounded root enabling fix; cosmetic optimization does not |
| `G07` | Engineering Quality & Evidence | Preserve correctness, security, reliability, compatibility, data integrity, performance, operations, and test quality using current evidence. | validation strategy, CI diagnosis, performance/security review | evidence beats narrative; never weaken checks merely to manufacture green | claims are bound to current SHA/object/environment and failures are classified before corrective mutation |
| `G08` | Scale-Adaptive Coordination | Keep small projects light, coordinate medium projects sufficiently, and handle large/multi-repository projects without a giant central context or unnecessary process. | proportional governance, workstream boundaries, progressive context loading, cross-repo dependency view | project size alone does not justify heavier controls | bounded work stays lean; multi-actor/multi-repo work remains coherent without duplicating every local backlog centrally |
| `G09` | Professional Delegation & Ownership | Use Workers only when specialization/parallelism repays coordination cost while Master remains accountable for project decisions and delivery. | bounded contracts, assignment identity, isolation, handoff/reconciliation | Worker never reprioritizes, broadens scope, integrates target, or owns release | Worker loss/staleness/blocker is absorbed without losing assignment state or automatically stopping Master |
| `G10` | Authority, Risk & Safety Integrity | Maximize autonomy inside the authorized envelope while applying controls to the actual effects and risk of each action. | project authority, scoped authorization, effect/risk gates, safe escalation | capability, environment, risk, and assurance cannot upgrade authority; independent effects retain independent obligations | one-off authorization does not widen project authority; multi-effect actions preserve every applicable obligation |
| `G11` | Verified Review, Integration, Release & Operations | Bind review and integration to fresh change identity and drive production-bound work through verified delivery and operational safety. | fresh review, CI, integration, release, deployment, migration, rollback, incident handling | self-review is not independent review; `INTEGRATED != DELIVERED` | changed HEAD invalidates stale approval; deployment transport success alone cannot prove delivery |
| `G12` | Zero-Chat Recoverability & Succession | Make previous chat history unnecessary for correct continuation by another Master or human. | durable authoritative state, recovery, reconciliation, safe rotation | chat is disposable and non-authoritative | cold replacement can determine purpose, active outcome, work, blockers, risks, delivery state, and next valid action |
| `G13` | Lean Navigable Project Knowledge | Organize project knowledge as a small, authoritative, navigable graph rather than duplicated manager memory. | Project Map/index, source-of-truth ownership, native relationships, progressive discovery | one owner per kind of truth; no manager-memory archive; avoid duplicate live status | replacement Master can traverse from project map/current outcome to relevant tasks, PRs, decisions, and release evidence without exhaustive reading |
| `G14` | Repository Readiness, Hygiene & Self-Repair | Keep repository docs/tasks/CI/workflows/navigation fit for current delivery and repair stale, missing, or harmful structure when justified. | readiness audit, reuse/update/simplify, stale-state reconciliation | reuse before parallel systems; management artifacts must earn maintenance cost | inadequate current structures are repaired proportionally and bootstrapping stops once safe execution/recovery is supported |
| `G15` | Proactive Improvement Without Scope Creep | Discover meaningful improvements while preserving accepted scope. | improvement classification, enabling work, proposals/follow-ups | required/in-scope improvements may execute; material adjacent improvements are proposed/tracked; low-value noise is ignored | mixed improvement scenarios are classified correctly without silent scope expansion or backlog inflation |
| `G16` | Persistent Progress Without Friction | Continue while a safe, authorized, materially useful action traceable to the accepted outcome exists. | next-work synthesis, local-boundary handling, anti-spin, minimal decision escalation | no artificial stop, no artificial work, no blind retry | commit/PR/tool batch/Worker stop does not end execution; local blockers do not stop independent work; real terminal boundaries stop cleanly |

### 3.1 Professional engineering completeness and proportionality

`G05`, `G06`, `G07`, and `G11` together require the Skill to behave like a mature engineering team from implementation through production operation, not merely to produce code that passes a happy-path test. This requirement remains **relevance-driven and proportional**: concerns are activated by the actual product surface, failure modes, risk, delivery model, and current evidence rather than by a universal checklist.

For any substantive change, Master should determine which engineering concerns are material to the change and carry only those concerns through framing/acceptance, implementation or Worker instructions, validation, review, integration, and release. Relevant concerns can include, without requiring a fixed runtime enum: security, privacy, data integrity, compatibility, resilience, observability/diagnosability, performance, capacity/resource/cost behavior, accessibility/user experience, migration, operations, and release safety.

When a change introduces material production or support failure modes, professional implementation includes proportionate **diagnosability** before release. As applicable this means choosing useful logging severity/levels and context; structured/correlatable identifiers when they materially help trace a request/job/workflow; safe exception/error evidence; controlled runtime diagnostic/debug capability when the product needs it; and appropriate metrics, traces, health/readiness signals, or alerts when logs alone are insufficient. Diagnostic logging and security/audit logging are distinct concerns and should be used only when the domain requires them. Observability must not leak secrets, credentials, tokens, or sensitive personal data; privacy, redaction/data minimization, retention/access, noise/volume, and operational cost must be considered when material.

Reliability engineering starts during implementation rather than being deferred to review. Relevant external, asynchronous, concurrent, or stateful behavior should consider failure handling such as timeouts, bounded retries/backoff, idempotency, partial failure, transaction/concurrency boundaries, resource cleanup, graceful degradation, and recovery semantics when those concerns apply. Stateful/destructive systems must treat backup existence and credible restore/recovery capability as different questions.

Engineering-system fitness includes CI and repository automation. When current evidence shows CI/automation is materially slowing delivery, duplicating work, weakening signal, increasing defect/review risk, or consuming disproportionate resources, `G06` permits a bounded root enabling improvement. The assessment should consider only decision-relevant factors such as trigger scope, duplicate validation, superseded runs/concurrency, least-privilege permissions, critical-path latency, matrix breadth, caching payoff, runner/compute cost, artifact/log retention, maintainability, and discoverability. This does **not** create a periodic CI optimization audit, and a theoretically better workflow is not sufficient reason to change a fit current system.

Production engineering is broader than latency. Material CPU, memory, storage, network, database/connection, queue/backlog, telemetry/log-volume, third-party quota, and infrastructure/cloud-cost effects should be measured or bounded when the active change can materially affect them. Likewise, when the product surface is user-facing, applicable quality includes accessible interaction, responsive behavior, usable loading/error/empty states, localization/internationalization, and timezone behavior where those concerns are actually relevant.

Documentation, tests, logs, metrics, tracing, alerts, dashboards, Issues, ADRs, and other artifacts are **means, not goals**. Add or update them only when they materially improve correctness, diagnosis, safety, review, delivery, operation, or recovery. The absence of a generic artifact is not itself a defect, and no artifact should exist merely to record that a checklist was considered. Prefer the smallest authoritative evidence at the natural owner: code/tests for behavior, Git/PR for implementation/review history, CI for validation, Issues/Projects/milestones for unresolved work, durable docs/ADR for lasting knowledge/decisions, and release/deployment/observability systems for production evidence.

## 4. Goal architecture

The development model is intentionally layered:

```text
MISSION
  -> CANONICAL GOALS
  -> REQUIRED CAPABILITIES
  -> NON-NEGOTIABLE INVARIANTS
  -> DECISION MODELS
  -> RUNTIME MECHANISMS
  -> REGRESSION / OPERATIONAL TESTS
```

This separation is deliberate. Runtime mechanisms may evolve without silently changing the goals or guarantees they serve.

Development traceability from goals to the v1.0.0 rule inventory and evaluations lives in `../design/GOAL-MAP.md`. Canonical baseline rule ownership lives in `../design/RULE-MAP.md`; typed runtime design lives in `../design/STATE-MODEL.md`; decision relationships live in `../design/DECISION-GRAPHS.md`; phased implementation lives in `../design/MIGRATION.md`.

## 5. Representation policy

Use the representation that makes a rule easiest to apply correctly, not the representation that merely looks shortest.

| Logic | Preferred representation |
|---|---|
| state/lifecycle | state graph |
| branching decision | decision tree |
| authority/approval | gate matrix |
| simultaneous action consequences | set/effect model + obligation union |
| persisted structure | typed schema |
| precedence | ordered table |
| dependency/artifact relationships | graph/native links |
| invalid implications | forbidden-inference matrix |
| deterministic invariant | script/linter |
| event-specific behavior | trigger/router table |
| nuanced engineering judgment | concise prose |
| edge/failure behavior | regression scenario |

An abstraction replaces prose only when it reduces ambiguity, duplication, execution cost, or error probability. Do not add graphs, schemas, scripts, or states merely for stylistic consistency.

## 6. Runtime loading and decision-friction target

The future `SKILL.md` should remain a compact control kernel containing only the state/role model, universal invariants, Master control loop, source-of-truth model, event router, and terminal rules necessary for orientation.

Detailed domains should load when their event becomes decision-relevant, for example:
- governance/readiness when repository or project structure needs assessment or repair;
- Task Contract/Worker rules when delegation or durable coordination is needed;
- review/integration rules when a candidate reaches review/integration;
- release rules when deterministic production/delivery effects enter the action frontier;
- continuity rules on new/replacement Master or material recovery triggers;
- eval/refactor rules only while modifying this Skill.

Rules are not removed to achieve this. Activation is made more precise so unrelated rules do not occupy the normal decision frontier.

## 7. Project scale model

Scale controls are driven by actual coordination, dependency, recovery, risk, and release complexity rather than repository size alone.

- **Small/bounded project:** prefer direct Master execution, FAST path where valid, minimal persistent management artifacts, and no Project/ADR ceremony without demonstrated need.
- **Medium/coordinated project:** use persistent work identity, dependencies, milestones/releases, PR/review/CI coordination, and Workers where useful.
- **Large/multi-repository project:** preserve one coherent global outcome and release/dependency view while keeping local work authoritative in its natural repository/workstream. Use explicit component/workstream ownership boundaries and progressive loading so Master does not need the entire project in active context.

The target is scalable coordination without making Master a central information bottleneck.

## 8. Zero-chat recovery and bounded recovery cost

Recoverability requires more than storing information somewhere. A replacement Master must be able to reconstruct correct operational state quickly and progressively.

Persist continuation-relevant truth, not transient reasoning. Documentation, tasks, and relationships must remain concise enough that a new Master or human can understand the project without reading all history.

A cold replacement should be able to answer, from authoritative repository/GitHub/Git/CI/release/deployment sources as applicable:
- what the project is and what outcome is currently accepted;
- what completion means;
- what is done, active, in review, blocked, or pending delivery;
- the material dependencies, risks, and lasting decisions;
- where current architecture/development/release rules live;
- the current candidate/PR/release identities and evidence;
- what action should be taken next.

If losing the current chat prevents correct continuation, required durable state is missing. If recovery requires reading the whole repository or a large manager-history archive, the information architecture is also failing.

## 9. Cross-cutting invariants

The following guarantees should survive representation changes unless explicitly revised with corresponding rule/eval changes:

- outcome before activity;
- evidence before narrative;
- one authoritative owner per kind of truth;
- inspect before consequential mutation;
- authority is independent from technical capability, risk, environment, and assurance;
- scope changes only through valid direction/evidence;
- Worker stop does not automatically become Master stop;
- integration does not imply delivery;
- unknown or incomplete evidence does not imply absence/cleanliness;
- no blind retries;
- no artificial stops;
- no artificial work;
- current evidence outranks stale state;
- process is proportional to actual need;
- improvements remain traceable to accepted outcome;
- durable state is sufficient but lean;
- complexity must earn its place.

## 10. Change acceptance for the Skill itself

Every material proposed change to the Skill should answer:

1. Which canonical Goal ID does this improve?
2. Which existing Rule IDs/invariants and eval scenarios can it affect?
3. Does it reduce or increase operational/cognitive friction in representative work?
4. What evidence demonstrates preserved or improved behavior?

Do not accept changes solely because they are shorter, more abstract, more elegant, or more automated.

## 11. Baseline and release strategy

- `v1.0.0` is the immutable pre-refactor runtime baseline originating from the Skill supplied before refactoring.
- Runtime source lives under `skill/` and remains the single behavioral source for every supported platform.
- Development-only project/design/validation artifacts live outside `skill/` unless intentionally required at runtime.
- `v1.0.0` must remain installable and unchanged while later releases evolve incrementally.
- Runtime releases are versioned, validated, tied to immutable commits, and publish deterministic ChatGPT, Manus, Qwen, and Claude.ai artifacts plus SHA-256 checksums from the same canonical source and commit. `skill.zip` remains the ChatGPT-compatible artifact name.
- Platform-specific distribution adapters must remain minimal and may not become independently maintained runtime forks.
- Refactoring is incremental and reviewable; no big-bang rewrite.

## 12. Non-goals

- Do not turn the Skill into a heavyweight project-management framework for every repository.
- Do not require Workers, GitHub Projects, Issues, ADRs, dashboards, reports, or additional documents when they do not materially help current delivery or recovery.
- Do not create periodic optimization workstreams merely because a better tool/process could exist.
- Do not centralize or duplicate state that is already authoritative and discoverable in Git/GitHub/CI/release/deployment systems.
- Do not maintain platform-specific forks of canonical orchestration behavior when a packaging/discovery adapter is sufficient.
- Do not sacrifice correctness, security, maintainability, review freshness, rollback safety, authority boundaries, or recoverability for apparent speed.
- Do not trade agent usability for theoretical formalism.

## 13. Project-level definition of done

The refactor program is successful when the Skill demonstrably gets a capable agent to verified engineering outcomes with less unnecessary friction while preserving or strengthening its behavioral protections.

At minimum:
- no known lossy runtime state model remains for critical decisions;
- no known ambiguous cross-namespace state propagation remains;
- canonical rule ownership is traceable and duplicate definitions do not fork semantics;
- routine work does not carry irrelevant project/release/recovery reasoning overhead;
- small, medium, and large representative projects receive proportionate coordination;
- replacement-Master cold recovery is correct and bounded;
- delegation, review, integration, release, and production evidence remain fresh and identity-safe;
- unauthorized authority escalation, artificial stops, artificial work, and blind retry regressions are covered by evaluation;
- supported ChatGPT, Manus, Qwen, and Claude.ai distributions are generated and validated from the same canonical runtime without semantic drift;
- runtime changes are measured against the immutable v1.0.0 baseline and the canonical goals above.
