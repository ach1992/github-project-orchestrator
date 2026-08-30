# Proportional Engineering Quality

Canonical owner for selecting and carrying **material engineering concerns** through implementation and evidence. Use professional engineering judgment without turning every change into a checklist. Existing authority, scope, risk, review, release, and stop rules remain authoritative in their owning domains.

## 1. Activation and proportionality

Load this domain only when the actual change surface, failure modes, product surface, or current engineering-system evidence makes one or more concerns decision-relevant. Typical triggers include external or asynchronous behavior, stateful/concurrent flows, production support needs, sensitive data, material resource/cost impact, user-facing interaction, migration/operational risk, or CI/automation that is itself a demonstrated delivery bottleneck.

For a substantive change:

1. identify only concerns that can materially change implementation, acceptance, validation, review, or release;
2. address those concerns in the smallest natural owner that needs them (code/tests/config/Task Contract/PR/release evidence), rather than creating a concern register;
3. omit irrelevant concerns completely;
4. reassess only when new evidence changes the failure surface or risk.

Possible concerns include security, privacy, data integrity, compatibility, resilience, observability/diagnosability, performance, capacity/resource/cost behavior, accessibility/user experience, migration, operations, and release safety. This is a reasoning aid, **not** a required enum, persisted state field, contract section, status, label, or checklist.

Concern selection by itself never changes accepted scope, `RiskLevel`, `AssuranceLevel`, `ExecutionPath`, `CoordinationBaseline`, `ProjectAuthority`, or approval requirements. Change those only when their existing canonical rules independently justify it. A trivial/localized change with no material concern trigger keeps its current `CoordinationBaseline` and uses the normal FAST path only when the existing FAST criteria independently fit; it must not gain logging, metrics, retry, accessibility, documentation, or process work merely because those practices exist.

## 2. Implementation discipline when a concern applies

| Concern | Proportional implementation questions |
|---|---|
| security / privacy | Does the change alter validation, auth/authz, permissions, sensitive data handling, telemetry exposure, retention/access, or privacy posture? Protect secrets, credentials, tokens, and sensitive personal data; use minimization/redaction where material. |
| data / compatibility / migration | Are transactions, concurrency, persisted data, schema/API/error contracts, backward compatibility, partial migration, rollback/roll-forward, or recovery affected? |
| resilience | Can external, asynchronous, concurrent, or stateful work fail partially or transiently? Use timeouts, bounded retries/backoff, idempotency, transaction/concurrency boundaries, cleanup, graceful degradation, and recovery semantics only where the failure model warrants them. Never add retry as a substitute for understanding correctness. |
| observability / diagnosability | If the behavior fails in production, will an operator/developer have enough safe evidence to locate the failing component/request/job/dependency and root cause? Use useful severity/levels, structured/contextual fields, correlation/request/job identity, exception/error evidence, metrics, traces, health/readiness signals, or alerts only when they materially improve detection or diagnosis. |
| performance / capacity / cost | Can the change materially affect latency, CPU, memory, storage, network, database connections/query load, queue/backlog growth, log/telemetry volume, third-party quota, or infrastructure/cloud cost? Establish representative evidence or explicit bounds when material; do not optimize by intuition alone. |
| user-facing quality | For applicable UI/product surfaces, are accessible interaction, responsive behavior, loading/error/empty states, localization/internationalization, and timezone behavior materially affected? Apply only the relevant subset. |
| operations / release | Does configuration/environment behavior, health, rollback, deployment, support procedure, or incident response materially change? Keep code, configuration, secrets, and environment-specific state separated where the platform supports it; validate material configuration at the appropriate boundary and prefer explicit safe defaults over silent misconfiguration. Update durable operating guidance only when future operators need it. |

### Authorized defensive AI work

When security-sensitive implementation or review is relayed to another AI, state only authorization and scope supported by current evidence: the exact defensive goal, in-scope repository/change/system, applicable explicit user/organization authorization, allowed action boundary (for example read-only review or isolated reversible implementation/test), and prohibited out-of-scope effects. Technical access or repository permissions alone never invent or widen `ProjectAuthority`/`ScopedAuthorization`, and an authorization statement never claims to override provider/platform policy.

Frame the requested work around defensive analysis, root cause, remediation, and verification. Do not request secrets/credentials, unrelated third-party targeting, unapproved production mutation, weaponization, persistence, evasion, or other unnecessary offensive action. If a provider/tool restricts one detail, omit or redact only that detail, continue every safely allowed outcome-linked review/remediation/test, and report the exact limitation plus its effect on evidence/completeness. Do not replace all safe work with an undifferentiated refusal merely because security is involved. If a limitation prevents required review evidence, return an incomplete review without approval under `review-integration.md`; never fabricate evidence or weaken security to avoid the limitation.

### Production diagnostics and logging

When production diagnosability is material:

- choose log severity/level and event granularity for signal, not volume; exact level names follow the project's logging framework/conventions;
- include stable structured context/correlation identifiers when they materially shorten diagnosis across requests, jobs, queues, services, or external calls;
- preserve useful root-cause/error evidence without exposing internal diagnostics to end users unnecessarily;
- never log secrets, credentials, session material, tokens, or sensitive personal data merely for convenience; redact/minimize and constrain telemetry access/retention when material;
- keep diagnostic logging distinct from security/audit logging. Add an audit trail only when the domain needs durable accountability/security evidence, not as a substitute for debug logs;
- when runtime debug/diagnostic mode is useful, make it controlled and production-safe by default, with bounded scope/verbosity and no requirement to rebuild merely to obtain reasonable operational evidence when the product's operating model supports runtime control;
- consider sampling/rate limiting, retention, storage/ingestion cost, and alert/log noise when volume can become operationally material;
- use metrics/traces/health/readiness/alerts only when logs alone cannot provide the required detection/diagnosis. Do not create dashboards or telemetry solely because they are common practice.

For stateful/destructive systems, distinguish **backup existence** from a credible restore/recovery path. Do not treat an untested or poorly understood backup as proof of recoverability when recovery is material to the change.

## 3. Role propagation without new ceremony

### Master / self-execution

For FAST work, keep selected concerns transient when the accepted request + repository evidence already make implementation/validation clear. For FULL or persisted work, express only concern-derived facts that materially affect existing Goal/Scope/Acceptance/Validation/Risk/Release fields; do not add a generic `EngineeringConcerns` field. If a recovery/rotation boundary makes a still-material concern-derived fact no longer recoverable from stronger code/Git/GitHub/CI/release evidence, let `continuity.md` persist only that missing unresolved fact in its natural existing owner.

Implement the smallest repository-consistent solution that addresses the selected failure modes. Validate the concern at the narrowest high-signal boundary first, then broader required checks. A concern that is merely theoretically possible does not justify expanding scope or delaying useful delivery.

### Worker

A Worker applies concern requirements already present in its current contract/acceptance/validation/special constraints plus directly evident in-scope correctness/safety obligations. It does not perform repository-wide observability, CI, privacy, accessibility, or reliability redesign on its own. If a newly discovered concern materially changes scope, acceptance, risk, architecture/security/privacy posture, migration, or release expectations, use the existing Worker stop/contract-revision path instead of silently broadening the assignment.

When Master dispatches concern-sensitive work, put the smallest actionable requirement in the existing Acceptance, Validation, or Special constraints surface. Do not send the Worker this entire concern catalog when only one or two concerns matter.

### Reviewer

Review the concerns material to the effective change and any newly evidenced material concern introduced by the diff. Missing concern handling that makes the accepted change unsafe, incorrect, operationally undiagnosable, or materially incomplete is a normal `BLOCKER`/`REQUIRED` finding according to impact. Do not convert optional telemetry, retries, abstractions, docs, dashboards, or stylistic preferences into required scope without evidence.

### Release / operations

Use `release.md` as the canonical owner of delivery state, production gates, release readiness, deployment verification, rollback, and incident handling. This domain only ensures implementation did not defer an already-material diagnosability/resilience/privacy/resource concern until after release. Do not duplicate release state or evidence here.

## 4. CI and automation fitness

CI/automation remains subject to the existing `ARTIFACT-FITNESS` and scope rules. Reassess only when evidence shows current CI/automation is materially slowing delivery, duplicating work, weakening validation signal, increasing defect/review risk, consuming disproportionate resources, or otherwise blocking the accepted outcome.

When such a trigger exists, inspect only decision-relevant factors such as:

- event/path trigger scope and whether expensive jobs run for changes they cannot validate;
- duplicate validation across jobs/workflows or repeated build/package work with no evidence value;
- superseded runs/concurrency behavior when stale work materially consumes time/resources or delays current evidence;
- least-privilege workflow/job permissions and exposure of credentials to changed/untrusted execution surfaces;
- critical-path CI latency versus parallelism/serialization dependencies;
- matrix breadth and whether each dimension protects a supported/relevant environment;
- caching or artifact reuse only when expected payoff exceeds complexity/staleness/supply-chain risk;
- runner/compute/storage/network cost and log/artifact retention when material;
- maintainability, diagnosability, and discoverability for the next developer/Master.

Prefer the smallest root fix to the demonstrated bottleneck and validate that required signal/gates were not weakened. Do not run periodic CI optimization audits, chase theoretical speedups, cancel useful evidence blindly, or add caches/matrices/dashboards merely because they are available.

## 5. Evidence and friction guard

Professional quality is demonstrated by the resulting behavior and current evidence, not by artifact count. Tests, logs, metrics, traces, alerts, docs, Issues, ADRs, dashboards, and runbooks are means; add/update them only when they materially improve correctness, diagnosis, review, delivery, operation, or recovery.

A missing optional artifact is not a project boundary. Never stop execution merely to manufacture observability/docs/tests/process that are not required by selected material concerns or accepted outcome. Conversely, when a selected concern is necessary for correctness/safety/operability, do not defer it merely to make the change appear faster; implement and verify it proportionally inside the normal execution/review/release path.
