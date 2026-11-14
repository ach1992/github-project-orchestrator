# Engineering Quality

Load before selecting a control that could change usable behavior or operational complexity, or when another engineering concern materially changes implementation or evidence. Do not turn this file into a universal checklist.

## Adaptability by default

Default to **no unnecessary hardcoding** before designing, assigning, or implementing code. A value being easy to encode is not evidence that the product should restrict itself to it. Check any proposed fixed tool/version/provider allowlist, file/transfer-size or item/rate/count ceiling, timeout/retention policy, path/environment assumption, or similar operational boundary against its actual source and effect:

- **Inherent constants and accepted protections:** keep protocol-defined values, correctness invariants, required input validation, and evidenced resource/security bounds in code as appropriate. Do not turn every constant into a setting or remove a real safety boundary for flexibility.
- **External versions and capabilities:** prefer actual API/protocol responses, capability detection, or documented compatibility requirements over guessed version ranges or allowlists. An unfamiliar, older, or newer version must not be rejected *solely* because it is absent from a list; attempt the supported operation when safe, and diagnose genuine incompatibility from observed behavior. Do not claim untested versions are verified compatible.
- **Data transfer and capacity:** do not mistake an internal buffer/message/frame limit for a product-wide maximum file size or payload count. Prefer streaming, chunking, pagination, or an existing supported transport when appropriate. Enforce a fixed bound only when required by an actual provider/protocol limit, accepted product policy, or evidenced safety/resource constraint; provide useful errors at that boundary.
- **Operator-variable behavior:** when a legitimate limit or policy varies by environment or operator, use the smallest suitable existing configuration surface (settings, environment, CLI, etc.) with a documented default and validation. Routine supported changes must not require source edits. Do not create speculative settings, a policy engine, or an unbounded adjustable value that defeats a required invariant.

If a proposed boundary is not required, omit it. If the necessary choice materially narrows accepted use, supported operations, compatibility, or lifecycle policy and is not already settled, present the concrete alternatives, operational trade-offs, and recommendation to the Owner **before** affected design/delegation/implementation. Keep independent authorized work moving; ordinary reversible technical details do not require approval. Apply [control decisions](#control-decisions) and [Owner-level anchors](authority-gates.md#4-owner-decisions-and-high-consequence-anchors) for the gate, not a universal questionnaire.

## Control decisions

Apply this decision before a restriction, extra prerequisite, persistent state, dependency, or compensating subsystem enters acceptance, an assignment, design, or code. A one-line limit or failure-policy change can be material.

Identify the accepted obligation or concrete failure path on the current product surface, the evidence, and the effect on the authorized workflow and operational burden. Source/configuration evidence can establish a real defect without an incident or successful exploit; a generic risk label or absence of a customary control cannot establish one by itself.

| Situation | Action |
|---|---|
| Necessary implementation of accepted behavior or a concrete material defect, within settled policy and authorized scope | Make the smallest maintainable correction and verify it; choose ordinary technical details autonomously. Enforcing accepted authorization, input safety, and duplicate-effect prevention does not require a new policy decision. |
| The proposed remedy leaves an unresolved trade-off in supported operations, access/lifetime/failure policy, or another [Owner-level anchor](authority-gates.md#4-owner-decisions-and-high-consequence-anchors) | Prepare the smallest concrete options, operational effects, and recommendation; resolve that decision before affected implementation. Reuse current decisions and continue unaffected work. |
| Worthwhile extra hardening without a required obligation or evidenced material defect | Keep it an optional proposal outside current execution and completion; ignore speculative or low-value additions. |

Investigate material uncertainty with the narrowest useful source check or reproduction. Missing evidence blocks only actions whose accepted requirement or safe execution depends on it; do not convert every unknown into a defect or an all-project stop.

If a control needs another control to compensate for its restrictions or failure states, reconsider the originating design before adding a layer. Prefer simplifying that design while preserving accepted protections and usable success, failure, manual recovery, and removal paths. Neither blanket fail-open nor fail-closed behavior replaces the product's accepted failure policy.

Keep genuinely operator-adjustable policy in the smallest suitable documented configuration surface. Do not hardcode an unresolved policy or add a general policy engine merely to make controls adjustable; keep correctness invariants required. Verify the representative operator workflow and the relevant failure path before extending the mechanism.

Other concerns—compatibility, performance/capacity/cost, accessibility/UX, localization/timezones, migration, and CI fitness—are selected from the actual surface and accepted outcome. Missing generic tests, logs, dashboards, or documents are not themselves defects.

## Implementation principles

- Fix the evidenced root cause with the smallest maintainable change that fits current architecture.
- Reuse a fit structure; make structural changes only when current work needs them or evidence shows clear net benefit.
- Verify version-sensitive APIs/dependencies/platform behavior against current primary documentation when material.
- Preserve required compatibility and data semantics; avoid unrelated cleanup/abstraction.
- For external/asynchronous/stateful/concurrent behavior, consider only the failure controls that actually apply: timeout, bounded retry/backoff, idempotency, transaction/concurrency boundary, partial failure, cleanup, graceful degradation, recovery.
- Backup existence is not restore proof when restoration matters.

## Security-sensitive continuity

These rules govern the agent's evidence acquisition and tool use; product-control choices use the decision above.

For security-sensitive work, state only the evidence-backed defensive purpose, scope, authorization, allowed actions, and prohibited effects. Technical access or authorization never overrides provider/platform policy. Use approved secret/runtime mechanisms and do not relay raw secret values. If a restricted detail cannot be supplied, continue safely allowed analysis, remediation, and verification with bounded redaction and an explicit limitation; never weaken controls merely to avoid a refusal. Bounded defensive regression tests remain available during explicitly scoped, isolated/reversible remediation when authorized and policy-permitted.

## Diagnosability

When the change creates a material production/support failure mode, add enough safe evidence to diagnose it: useful error context, correlation identifiers, logs, metrics, traces, health signals, or alerts as appropriate.

Preserve useful failure stage, provider error, correlation, and recovery context while redacting sensitive fields at the appropriate boundary. Do not remove an entire diagnostic object merely because one field may contain a secret. Add no telemetry by habit; bound unnecessary volume, retention, and operational cost.

## Performance, capacity, and cost

Do not optimize from intuition alone when performance/resource impact is an accepted concern.

Establish a representative baseline/constraint, identify the bottleneck with high-signal evidence when practical, make the smallest justified change, and compare the same workload afterward.

Consider CPU, memory, storage, network, database/connection, queue/backlog, telemetry volume, third-party quotas, and infrastructure cost only when the active change can materially affect them.

## User-facing quality

When the change affects a user-facing surface, preserve the intended interaction and applicable accessibility, responsive/adaptive behavior, loading/error/empty states, localization/internationalization, directionality, and timezone semantics.

For unresolved interface judgment that can materially change intended UX, use [interface-specialist.md](interface-specialist.md).

## CI and engineering-system fitness

Optimize CI/automation only when current evidence shows it materially slows delivery, duplicates work, weakens signal, creates repeated stale evidence, or consumes disproportionate resources.

Inspect the actual bottleneck. Prefer removing duplicate triggers/work, cancelling superseded runs, caching, and isolation-preserving parallelism/sharding before reducing meaningful coverage. Preserve aggregate completeness and isolation, and compare measured critical-path payoff when practical.

Do not create a recurring CI/process audit.
