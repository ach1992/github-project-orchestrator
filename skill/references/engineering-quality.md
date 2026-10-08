# Engineering Quality

Load only when a cross-cutting engineering concern can materially change the current implementation, validation, review, or release. Do not turn this file into a universal checklist.

## Select only material concerns

Possible concerns include security/privacy, data integrity, compatibility, reliability/concurrency, observability/diagnosability, performance/capacity/cost, accessibility/UX, localization/timezone behavior, migration, operations, and CI/automation fitness.

Select from the actual product surface, failure modes, environment, and accepted outcome. The absence of a generic test/log/metric/dashboard/document is not itself a defect.

## Implementation principles

- Fix the evidenced root cause with the smallest maintainable change that fits current architecture.
- Reuse a fit structure; make structural changes only when current work needs them or evidence shows clear net benefit.
- Verify version-sensitive APIs/dependencies/platform behavior against current primary documentation when material.
- Preserve required compatibility and data semantics; avoid unrelated cleanup/abstraction.
- For external/asynchronous/stateful/concurrent behavior, consider only the failure controls that actually apply: timeout, bounded retry/backoff, idempotency, transaction/concurrency boundary, partial failure, cleanup, graceful degradation, recovery.
- Backup existence is not restore proof when restoration matters.

## Security-sensitive continuity

For security-sensitive work, state only the evidence-backed defensive purpose, scope, authorization, allowed actions, and prohibited effects. Technical access or authorization never overrides provider/platform policy. Use approved secret/runtime mechanisms and do not relay raw secret values. If a restricted detail cannot be supplied, continue safely allowed analysis, remediation, and verification with bounded redaction and an explicit limitation; never weaken controls merely to avoid a refusal. Bounded defensive regression tests remain available during explicitly scoped, isolated/reversible remediation when authorized and policy-permitted.

## Diagnosability

When the change creates a material production/support failure mode, add enough safe evidence to diagnose it: useful error context, correlation identifiers, logs, metrics, traces, health signals, or alerts as appropriate.

Do not add telemetry by habit. Avoid secrets/sensitive personal data, unnecessary volume/retention, and operational cost.

## Performance, capacity, and cost

Do not optimize from intuition alone when performance/resource impact is an accepted concern.

Establish a representative baseline/constraint, identify the bottleneck with high-signal evidence when practical, make the smallest justified change, and compare the same workload afterward.

Consider CPU, memory, storage, network, database/connection, queue/backlog, telemetry volume, third-party quotas, and infrastructure cost only when the active change can materially affect them.

## User-facing quality

When the change affects a user-facing surface, preserve the intended interaction and applicable accessibility, responsive/adaptive behavior, loading/error/empty states, localization/internationalization, directionality, and timezone semantics.

For unresolved interface judgment that can materially change intended UX, use [interface-specialist.md](interface-specialist.md). Do not invoke it for trivial/local presentation choices already inside established design latitude.

## CI and engineering-system fitness

Optimize CI/automation only when current evidence shows it materially slows delivery, duplicates work, weakens signal, creates repeated stale evidence, or consumes disproportionate resources.

Inspect the actual bottleneck. Prefer removing duplicate triggers/work, cancelling superseded runs, caching, and isolation-preserving parallelism/sharding before reducing meaningful coverage. Preserve aggregate completeness and isolation, and compare measured critical-path payoff when practical.

Do not create a recurring CI/process audit.
