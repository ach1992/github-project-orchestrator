# Release and Production Operations

A project is not complete because code integrated. Drive delivery-required work through a verified release outcome appropriate to the project's risk and delivery model, keeping `DeliveryRequirement`, `DeliveryTarget`, and `DeliveryState` independent.

## Contents

[Release model](#1-discover-release-model) · [Readiness](#2-release-readiness) · [Deployment safety](#3-deployment-safety) · [Migrations](#4-migration-rules) · [Approval](#5-production-approval-gate) · [Verification](#6-post-release-verification) · [Incident/hotfix](#7-incident-and-hotfix-mode) · [Closeout](#8-closeout)

## 1. Discover release model

Before prescribing release steps, determine current reality:

- accepted `DeliveryRequirement` (`INTEGRATION_ONLY` or `DELIVERY_REQUIRED`);
- explicit `DeliveryTarget` when delivery is required, including exact account/project/region/environment identity and promotion flow;
- current `DeliveryState` for that immutable artifact/commit + target;
- versioning/tag/release convention;
- build/package artifact model, immutable artifact/commit identity, and whether promotion reuses the same artifact or rebuilds it;
- deployment mechanism and required credentials/approvals;
- database/data migration behavior;
- feature flags/configuration dependencies;
- monitoring/health signals;
- rollback/roll-forward capability;
- changelog/release-note requirements.

Preserve established safe automation rather than inventing a parallel deployment path. If pushing, merging, tagging, publishing, or another upstream mutation automatically triggers production deployment, classify the upstream action with `ApplicableEffects.PRODUCTION` in addition to any other simultaneous effects and satisfy every applicable obligation before performing it.

`DeliveryTarget` names the environment/target; it never determines lifecycle state. A production target can still have `DeliveryState.NOT_STARTED`, and a non-production target can be `DeliveryState.DELIVERED`.

## 2. Release readiness

Before production delivery, verify as applicable:

- milestone/release scope is intentionally complete;
- required PRs/changes are integrated into the intended target;
- target branch CI and release build are green/current and tied to the intended commit/artifact;
- known high-severity defects/risks are resolved or explicitly accepted;
- versioning/changelog/release metadata are correct;
- environment/config/secrets are present through approved mechanisms;
- migrations are compatible, ordered, and rehearsed when risk warrants;
- monitoring/logging/alerting can detect important failure modes;
- rollback or safe roll-forward plan is credible;
- required backups/snapshots exist and restore assumptions are understood for destructive data risk;
- RiskLevel/AssuranceLevel-required approvals/evidence are complete;
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

For `AssuranceLevel=HIGH_ASSURANCE`, require stronger independent evidence proportional to actual blast radius while retaining the current CoordinationBaseline and canonical approval matrix.

## 4. Migration rules

For schema/data migrations:

- prefer backward-compatible expand/migrate/contract sequencing when practical;
- understand transaction/locking/runtime impact;
- avoid coupling irreversible data change to an unproven application rollout;
- define what happens on partial failure;
- verify backup/restore or compensating strategy when rollback is not straightforward;
- do not call a migration reversible unless reversal has been realistically assessed.

If one rollout action both deploys production and performs an irreversible mutation, classify both `ApplicableEffects.PRODUCTION` and `ApplicableEffects.DESTRUCTIVE_OR_IRREVERSIBLE`; satisfy the union of their independent obligations.

## 5. Production approval gate

Apply `authority-gates.md` exactly as the canonical gate. For an action containing `ApplicableEffects.PRODUCTION` and for high/critical `ApplicableEffects.INTEGRATION`, an exact valid `ScopedAuthorization` substitutes for current confirmation only where that matrix permits it. Under the default matrix, an applicable `DESTRUCTIVE_OR_IRREVERSIBLE` effect still requires the stated human approval and `EXTERNAL_COMMITMENT` the stated human decision/approval; a still-current explicit user instruction that directly approves the exact effect can be the applicable ScopedAuthorization satisfying that human gate, but production/integration authorization alone cannot.

Complete safe independent readiness work and any authorized isolated reversible implementation/preparation before asking, except that an urgent human decision/containment must not be delayed when delay itself materially increases risk.

Provide the decision compactly:

```text
PRODUCTION APPROVAL REQUIRED
Release: <version/commit>
Delivery Target: <exact production target>
Applicable Effects: <all effects for the exact action>
Change/risk: <material summary>
Verified: <key evidence>
Remaining risk: <known residual risk>
Rollback/roll-forward: <strategy>
Exact approval requested: <action>
```

## 6. Post-release verification

After deployment, verify the release actually reached the explicit DeliveryTarget and assess applicable signals: deployment/version/commit identity; service/application health; critical user-path smoke test; error/log anomalies; migration/data correctness; performance/resource regression; and business/domain success signal where observable.

Use this state decision:

| Evidence | DeliveryState / action |
|---|---|
| delivery has not started | `DeliveryState.NOT_STARTED` |
| intended artifact/commit did not reach the intended DeliveryTarget, or identity is unknown | `DeliveryState.FAILED_OR_UNKNOWN`; do not mark delivered; freeze further rollout and reconcile deployment identity/path. If unintended production artifact/state may be user-impacting, security-sensitive, or otherwise hazardous, enter incident/containment while reconciling. |
| intended artifact reached target but health/acceptance signal is unacceptable | `DeliveryState.FAILED_OR_UNKNOWN`; stop further rollout; execute the pre-agreed rollback/roll-forward/incident path |
| immediate health is acceptable but required soak/delayed migration/reliability/business signal is not yet observable | `DeliveryState.PENDING`; persist the exact completion condition in the authoritative Issue/release source |
| all required delivery acceptance/verification is current and satisfied | `DeliveryState.DELIVERED`; proceed to closeout |

Deployment transport success alone is never sufficient evidence for `DeliveryState.DELIVERED`. Legacy `PENDING_DELIVERY` maps to `DeliveryState.PENDING`; it is a lifecycle state, not a canonical Master stop condition. If delayed required delivery evidence becomes the sole remaining external dependency after independent useful work is exhausted, normally stop at `MasterBoundary.BLOCKED` with the exact evidence/object/resume condition unless another boundary more precisely describes the cause. Do not invent DeliveryState as a terminal boundary or use `MasterBoundary.NO_READY_WORK` merely because the required signal is not yet observable.

## 7. Incident and hotfix mode

When a production regression, security issue, data-integrity problem, or severe operational failure appears:

1. prioritize stabilization over planned feature work and stop further rollout when appropriate;
2. establish blast radius, affected version/artifact, symptoms, explicit DeliveryTarget, and the safest immediate containment option;
3. use rollback, feature disablement, traffic isolation, configuration reversal, or a minimal hotfix according to verified current capability, ProjectAuthority, ScopedAuthorization, ApplicableEffects, and RiskLevel;
4. preserve evidence needed to understand the incident, but never delay necessary containment merely to produce documentation;
5. validate recovery in the affected environment and monitor for recurrence;
6. after stabilization, create only concrete corrective/preventive follow-up work and capture a durable RCA/decision only when it will improve future operation or architecture.

Hotfixes still require the strongest practical review/validation for their urgency and blast radius. Emergency authorization may change applicable ScopedAuthorization/gates, but it does not make evidence optional or silently upgrade broader ProjectAuthority.

## 8. Closeout

After stable verification:

- mark release/milestone state accurately;
- close delivery-required work only when the intended artifact is verified `DeliveryState.DELIVERED` for the required DeliveryTarget; keep `TaskState.INTEGRATED` and DeliveryState distinct;
- for `DeliveryRequirement=INTEGRATION_ONLY`, do not manufacture a deployment requirement after verified integration;
- create/reuse follow-up Issues for unresolved defects/debt discovered during release only when actionable and worth tracking;
- update durable runbooks/docs only when operating behavior changed;
- keep release evidence in native release/deployment/CI systems instead of copying it into manager logs;
- run the continuity test so the next Master can support the production system.
