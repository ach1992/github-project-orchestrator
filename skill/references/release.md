# Release and Production Operations

A project is not complete because code merged. Drive production-bound work through a verified release outcome appropriate to the project's risk and delivery model.

## Contents

[Release model](#1-discover-release-model) · [Readiness](#2-release-readiness) · [Deployment safety](#3-deployment-safety) · [Migrations](#4-migration-rules) · [Approval](#5-production-approval-gate) · [Verification](#6-post-release-verification) · [Incident/hotfix](#7-incident-and-hotfix-mode) · [Closeout](#8-closeout)

## 1. Discover release model

Before prescribing release steps, determine current reality:

- versioning/tag/release convention;
- build/package artifact model, immutable artifact/commit identity, and whether promotion reuses the same artifact or rebuilds it;
- exact target account/project/region/environment identity and promotion flow;
- deployment mechanism and required credentials/approvals;
- database/data migration behavior;
- feature flags/configuration dependencies;
- monitoring/health signals;
- rollback/roll-forward capability;
- changelog/release-note requirements.

Preserve established safe automation rather than inventing a parallel deployment path. If pushing, merging, tagging, publishing, or another upstream mutation automatically triggers production deployment, treat that upstream mutation as the production rollout action and satisfy the production approval gate before performing it.

## 2. Release readiness

Before production release, verify as applicable:

- milestone/release scope is intentionally complete;
- required PRs are merged to the intended target;
- target branch CI and release build are green/current and tied to the intended commit/artifact;
- known high-severity defects/risks are resolved or explicitly accepted;
- versioning/changelog/release metadata are correct;
- environment/config/secrets are present through approved mechanisms;
- migrations are compatible, ordered, and rehearsed when risk warrants;
- monitoring/logging/alerting can detect important failure modes;
- rollback or safe roll-forward plan is credible;
- required backups/snapshots exist and restore assumptions are understood for destructive data risk;
- profile/risk-required approvals are complete;
- dependency/build-chain provenance or license concerns introduced by the release are resolved when material.

Do not manufacture a generic checklist when many items do not apply; use the applicable subset and explain any material exception.

## 3. Deployment safety

For risky releases prefer incremental exposure when supported:

- staging/pre-production validation;
- canary, percentage rollout, region/tenant cohort, or feature flag;
- backward-compatible schema/API sequencing;
- deploy-before-enable when feature flags reduce blast radius;
- explicit stop conditions based on health/error/business signals.

Prefer promoting the same reviewed/built immutable artifact across environments. If the platform necessarily rebuilds, verify that the production artifact is reproducibly tied to the approved source commit and expected build inputs. The principle is: review one intended change, deploy that identified change.

For HIGH_ASSURANCE changes, require stronger independent evidence proportional to actual blast radius.

## 4. Migration rules

For schema/data migrations:

- prefer backward-compatible expand/migrate/contract sequencing when practical;
- understand transaction/locking/runtime impact;
- avoid coupling irreversible data change to an unproven application rollout;
- define what happens on partial failure;
- verify backup/restore or compensating strategy when rollback is not straightforward;
- do not call a migration reversible unless reversal has been realistically assessed.

## 5. Production approval gate

Apply `authority-gates.md` exactly as the canonical gate. For `PRODUCTION` and high/critical `INTEGRATION`, an exact valid pre-authorization substitutes for current confirmation only where that matrix permits it. Under the default matrix, a `DESTRUCTIVE_OR_IRREVERSIBLE` effect still requires the stated human approval and an `EXTERNAL_COMMITMENT` the stated human decision/approval; a still-current explicit user instruction that directly approves the exact effect can satisfy that human gate, but production/integration pre-authorization alone cannot. Complete safe independent readiness work and any authorized isolated reversible implementation/preparation before asking, except that an urgent human decision/containment must not be delayed when delay itself materially increases risk.

Provide the decision compactly:

```text
PRODUCTION APPROVAL REQUIRED
Release: <version/commit>
Change/risk: <material summary>
Verified: <key evidence>
Remaining risk: <known residual risk>
Rollback/roll-forward: <strategy>
Exact approval requested: <action>
```

## 6. Post-release verification

After deployment, verify the release actually reached the target and assess applicable signals: deployment/version/commit identity; service/application health; critical user-path smoke test; error/log anomalies; migration/data correctness; performance/resource regression; and business/domain success signal where observable.

Use this state decision:

| Evidence | State / action |
|---|---|
| intended artifact/commit did not reach the intended environment, or identity is unknown | do not mark delivered; freeze further rollout and reconcile deployment identity/path. If an unintended production artifact/state may be user-impacting, security-sensitive, or otherwise hazardous, enter the incident/containment path while reconciling. |
| intended artifact reached target but health/acceptance signal is unacceptable | stop further rollout; execute the pre-agreed rollback/roll-forward/incident path |
| immediate health is acceptable but required soak/delayed migration/reliability/business signal is not yet observable | `PENDING_DELIVERY`; persist the exact completion condition in the authoritative Issue/release source |
| all required delivery acceptance/verification is current and satisfied | `DELIVERED`; proceed to closeout |

Deployment success alone is never sufficient evidence for `DELIVERED`. `PENDING_DELIVERY` is a lifecycle state, not a canonical Master stop condition. If delayed required delivery evidence becomes the sole remaining external dependency after independent useful work is exhausted, normally stop at canonical `BLOCKED` with the exact evidence/object/resume condition unless another boundary more precisely describes the cause; do not invent `PENDING_DELIVERY` as a terminal boundary or use `NO_READY_WORK` merely because the required signal is not yet observable.

## 7. Incident and hotfix mode

When a production regression, security issue, data-integrity problem, or severe operational failure appears:

1. prioritize stabilization over planned feature work and stop further rollout when appropriate;
2. establish blast radius, affected version/artifact, symptoms, and the safest immediate containment option;
3. use rollback, feature disablement, traffic isolation, configuration reversal, or a minimal hotfix according to verified current capability and risk;
4. preserve evidence needed to understand the incident, but never delay necessary containment merely to produce documentation;
5. validate recovery in the affected environment and monitor for recurrence;
6. after stabilization, create only concrete corrective/preventive follow-up work and capture a durable RCA/decision only when it will improve future operation or architecture.

Hotfixes still require the strongest practical review/validation for their urgency and blast radius. Emergency authorization may change the gate, but it does not make evidence optional.

## 8. Closeout

After stable verification:

- mark release/milestone state accurately;
- close production-required work only when the intended release is verified `DELIVERED`; keep engineering integration and delivery status distinct;
- create/reuse follow-up Issues for unresolved defects/debt discovered during release only when actionable and worth tracking;
- update durable runbooks/docs only when operating behavior changed;
- keep release evidence in native release/deployment/CI systems instead of copying it into manager logs;
- run the continuity test so the next Master can support the production system.
