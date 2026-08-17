# Project Specification

## Purpose

Develop and distribute `github-project-orchestrator` as a production-quality ChatGPT Skill that can take an already-provisioned GitHub repository plus a project-defining prompt/specification and own the engineering project end to end.

The Skill must be capable of establishing proportional repository/docs/task readiness, framing and preserving the accepted outcome, planning dependency-aware work, implementing directly or delegating bounded Worker tasks, validating and reviewing changes, integrating safely, recovering without chat history, and driving the project through its required release/delivery endpoint.

## Product goals

1. Deliver excellent real-world execution quality rather than process ceremony.
2. Preserve recoverability so a replacement Master can continue from authoritative repository/GitHub evidence without depending on prior chat.
3. Make decisions quickly, consistently, and with minimal ambiguity while retaining strong safety, correctness, security, review, integration, and release guarantees.
4. Keep orchestration lean: create only artifacts and process controls that materially improve execution, safety, coordination, delivery, or recovery.
5. Preserve end-to-end autonomy inside the authorized envelope; do not introduce artificial stops or unnecessary confirmations.
6. Keep Worker scope and authority bounded while allowing useful specialization and parallelism.

## Refactoring objective

Optimize the Skill's operational decision model without losing behavioral guarantees.

Token count is not the primary objective. Prefer semantic normalization that makes the model easier to execute correctly:

- explicit typed state and state scope/lifetime;
- one canonical owner for each normative rule;
- decision tables, state graphs, branch trees, predicates, and schemas where they communicate relationships more precisely than prose;
- event/role-specific routing so only relevant rules participate in a decision;
- deterministic validators/scripts for mechanical invariants;
- regression scenarios that preserve edge-case behavior during simplification.

Do not remove a rule merely to reduce size. A rule may be removed from prose only after its behavior is preserved by an equivalent canonical representation, deterministic check, or deliberately revised requirement with regression coverage.

## Baseline and release strategy

- `v1.0.0` is the immutable pre-refactor behavioral baseline copied from the existing installed/uploaded Skill.
- Runtime source lives under `skill/`.
- Development-only design, validation, and regression artifacts live outside `skill/` unless they are intentionally needed by the runtime Skill.
- Each release must be tied to an immutable commit and ship a reproducible `skill.zip` plus SHA-256 checksum.
- Refactoring proceeds incrementally with reviewable phases rather than a big-bang rewrite.

## Current refactor direction

The first development phase must build a rule/state map before changing runtime semantics. It should make explicit:

- Project/runtime authority versus exact scoped authorization;
- coordination baseline versus assurance level;
- action effects when a single mutation has multiple simultaneous consequences;
- state namespaces such as task state, Worker status, write state, delivery state, and Master stop boundary;
- the scope/lifetime of each state variable;
- forbidden inference relationships such as capability not upgrading authority and integration not implying delivery;
- mapping from existing clauses to canonical owners and regression scenarios.

## Non-goals

- Do not turn the Skill into a heavyweight project-management framework for every repository.
- Do not require Workers, GitHub Projects, Issues, ADRs, or additional documents when they do not materially help the active outcome.
- Do not optimize merely for fewer files, fewer lines, or fewer tokens.
- Do not sacrifice correctness, security, maintainability, review freshness, rollback safety, or recoverability for apparent speed.
