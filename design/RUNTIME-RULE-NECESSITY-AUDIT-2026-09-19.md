# Runtime Rule-Necessity Audit — 2026-09-19

Tracking: #116
Candidate: PR #115 / `issue-112-outcome-flow-hardening`
Baseline: `v1.3.7@8ac3ffc1ae982fe7f1a5b01a8d78b1caf0c20156`

## Method and scope

This is a design/evidence artifact for the standalone field-derived optimization tracked by #116, not a runtime owner. Canonical semantics remain in `skill/`; Rule/Goal/eval identity remains in `RULE-MAP.md` and `GOAL-MAP.md`.

Every current canonical Rule ID in sections 2–9 of `RULE-MAP.md` is classified for this optimization. These verdicts are necessity/representation classifications, not claims that every owner file was rewritten in this PR. A rule may remain as a traceability ID while its runtime wording is derived/merged; the goal is fewer decision concepts/reminders for the model, not deletion of evidence identity for its own sake.

Evidence shorthand:
- `eval:<ids>` = existing regression scenarios proving the failure is material enough to protect.
- Goal IDs come from `GOAL-MAP.md`.
- `HOT` = always-loaded `SKILL.md`; `WARM` = direct event-triggered operational reference; `COLD` = specialized/recovery/release/engineering path.

State column answers whether explicit state vocabulary is needed to apply the protected behavior. `optional` means the concept may remain implicit on routine paths.

## Complete inventory

| Rule | Owner / Goal / evidence | Verdict · locality · state | Protected failure and overlap/replacement | Expected complexity effect |
|---|---|---|---|---|
| `OUTCOME-STABLE` | `SKILL.md` outcome kernel; G01,G02,G15; eval:AY, BA, CB, CY, DO | **KEEP** · HOT · state:no | Prevents loss of: Preserve accepted outcome/success criteria; do not shrink for convenience or expand to manufacture work. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `TRUTH-ONE-OWNER` | `SKILL.md` truth model; G13; eval:A, I, Z | **KEEP** · HOT · state:no | Prevents loss of: One authoritative owner per kind of live truth; avoid competing manager-memory artifacts. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `EVIDENCE-BEATS-NARRATIVE` | `SKILL.md` truth model; G07; eval:E, I, BH, CO | **KEEP** · HOT · state:no | Prevents loss of: Current Git/GitHub/CI/deployment evidence outranks summaries/chat. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `MUTATION-IDEMPOTENT` | `SKILL.md` mutation invariant; G14; eval:B, AU | **KEEP** · HOT · state:no | Prevents loss of: Discover/reuse/update/create-only-if-absent/verify; incomplete discovery is not absence. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `DRIFT-RECONCILE` | `SKILL.md` mutation invariant; G04,G14; eval:E, BH | **COMPRESS** · HOT · state:no | Prevents loss of: Re-read and reconcile before overwrite-sensitive/integration/release/production writes. Replacement/overlap: same canonical owner; compress duplicate/negative reminders into the positive invariant. | Same guarantee with fewer reminders/words or fewer hot-path reconstruction steps. |
| `PROTECT-UNRELATED` | `SKILL.md` safety invariant; G05; eval:X | **KEEP** · HOT · state:no | Prevents loss of: Never destroy/absorb unrelated user/contributor work to simplify execution. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `NO-FABRICATION` | `SKILL.md` evidence invariant; G07; eval:P, CO | **KEEP** · HOT · state:no | Prevents loss of: Never claim actions/evidence that were not performed and verified. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `ANTI-SPIN` | `SKILL.md` execution invariant; G16; eval:T, BG, DP | **COMPRESS** · HOT · state:no | Prevents loss of: Do not repeat materially identical failed actions without new evidence; change strategy or work. Replacement/overlap: same canonical owner; compress duplicate/negative reminders into the positive invariant. | Same guarantee with fewer reminders/words or fewer hot-path reconstruction steps. |
| `MACHINE-RELAY-PORTABLE` | `relay-transport.md` canonical transport owner + `SKILL.md` Output activation; G09,G11,G12,G16; eval:AT, BC, CK, DI | **KEEP** · HOT activation / COLD protocol · state:no | Prevents loss of: AI-to-AI relay prose is English by default, identity-bearing/decision-relevant literals stay exact unless safety/redaction requires otherwise, and every user-visible machine relay is the complete response as one copy target without requiring a separate copy-ready request, while domain owners retain payload semantics and no workflow state/control is weakened. Replacement/overlap: the always-loaded kernel keeps only classification/routing; the transport predicate is materialized only for relay output. | Preserve the guarantee while removing relay-only predicate detail from every non-relay turn. |
| `LEAN-ORCHESTRATION` | `governance.md`; G06,G13,G15; eval:K, AB, BT | **COMPRESS** · COLD / specialized · state:no | Prevents loss of: Create project/process artifacts only when they improve a future decision, execution, safety, or recovery. Replacement/overlap: same canonical owner; compress duplicate/negative reminders into the positive invariant. | Same guarantee with fewer reminders/words or fewer hot-path reconstruction steps. |
| `SUCCESSION-RECOVERABLE` | `continuity.md`; G12; eval:I, Z, AI, BB | **COMPRESS** · COLD / specialized · state:no | Prevents loss of: End at canonical boundaries with authoritative state sufficient for a replacement Master, subject to explicit USER_STOP. Replacement/overlap: same canonical owner; compress duplicate/negative reminders into the positive invariant. | Same guarantee with fewer reminders/words or fewer hot-path reconstruction steps. |
| `AUTHORITY-STABLE` | `authority-gates.md`; G10; eval:AH, CU | **COMPRESS** · WARM / triggered · state:no | Prevents loss of: Project Authority changes only from applicable explicit/higher authorization, never merely from access/risk/profile/environment. Replacement/overlap: same canonical owner; compress duplicate/negative reminders into the positive invariant. | Same guarantee with fewer reminders/words or fewer hot-path reconstruction steps. |
| `AUTHORIZATION-SCOPED` | `authority-gates.md`; G10; eval:CX, DQ | **KEEP** · WARM / triggered · state:no | Prevents loss of: Authorization remains exact to what was granted: one-off action grants do not upgrade project-wide Authority, and repository mutation is limited to the explicitly authorized repository set; relationships, dependencies, discovery, project membership, technical access, and delegation never widen it, ambiguous repository scope remains read-only until clarified, and required out-of-scope changes are handed off. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `CAPABILITY-NOT-AUTHORITY` | `authority-gates.md`; G10,G16; eval:N, CU | **DERIVE** · WARM / triggered · state:no | Prevents loss of: Capability affects feasibility and may constrain execution but cannot grant Authority. Replacement/overlap: derive from AUTHORITY-STABLE + AUTHORIZATION-SCOPED; keep only boundary wording where capability is evaluated. | Remove separate decision/reminder where the parent invariant is already active. |
| `EFFECT-ACTUAL` | `authority-gates.md`; G10; eval:H, BD, BO, CG, CH | **KEEP** · WARM / triggered · state:no | Prevents loss of: Classify by actual deterministic consequence, not labels, branch names, or nominal environment. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `EFFECT-MULTI` | `authority-gates.md`; G10; eval:H, CV | **KEEP** · WARM / triggered · state:no | Prevents loss of: Preserve every independently applicable effect/control when one mutation has multiple consequences. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `GATE-NO-INVENTION` | `authority-gates.md`; G10; eval:L, AJ, BP | **COMPRESS** · WARM / triggered · state:no | Prevents loss of: Do not invent human confirmation gates beyond the canonical matrix. Replacement/overlap: same canonical owner; compress duplicate/negative reminders into the positive invariant. | Same guarantee with fewer reminders/words or fewer hot-path reconstruction steps. |
| `GATE-UNION` | `authority-gates.md`; G10; eval:CV | **DERIVE** · WARM / triggered · state:no | Prevents loss of: Scoped authorization may satisfy one gate but cannot waive another independent effect gate. Replacement/overlap: derive from EFFECT-MULTI + CAN_EXECUTE/RequiredObligations union. | Remove separate decision/reminder where the parent invariant is already active. |
| `WRITE-UNKNOWN-RECONCILE` | `authority-gates.md`; G10; eval:C | **KEEP** · WARM / triggered · state:yes | Prevents loss of: Ambiguous mutation outcome becomes unknown; reconcile authoritatively before any retry. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `CONCURRENCY-OPTIMISTIC` | `authority-gates.md`; G04,G10; eval:D, E, AO, CR | **KEEP** · WARM / triggered · state:no | Prevents loss of: Overwrite-sensitive writes use expected identity/revision and reconcile drift rather than blind overwrite. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `MATERIAL-DECISION-BOUNDARY` | `authority-gates.md`; G02,G10; eval:S, BF | **KEEP** · WARM / triggered · state:no | Prevents loss of: Escalate only irreducible owner decisions that remain material after independent work is exhausted; ordinary technical choices remain agent-owned. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `COORDINATION-BASELINE` | `SKILL.md` state ontology; G08; eval:W, AB, CE | **KEEP** · HOT · state:yes | Prevents loss of: Coordination baseline is determined by coordination/recovery needs, not repository size alone. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `ASSURANCE-ADDITIVE` | `SKILL.md` state ontology; G10; eval:G, BP, CE, CF | **KEEP** · HOT · state:yes | Prevents loss of: HIGH_ASSURANCE adds justified assurance controls while preserving the coordination baseline; it does not create approval by itself. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `DIMENSIONS-ORTHOGONAL` | `SKILL.md` state ontology; G08; eval:AD, CE, CF, CM, CU | **KEEP** · HOT · state:no | Prevents loss of: Coordination, assurance, risk, execution path, persistence, strategy, capability, and Authority are independent inputs unless an explicit rule connects them. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `RISK-SCOPED` | `task-contract.md`; G10; eval:AC, AJ, CW | **KEEP** · WARM / triggered · state:yes | Prevents loss of: Reclassify change risk only when decision-relevant; risk is change-specific and not importance/project size. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `WORK-CLEAR-ENOUGH` | `task-contract.md`; G03; eval:K, L, BE | **KEEP** · WARM / triggered · state:no | Prevents loss of: Outcome, acceptance, validation, dependencies, and material risk must be clear enough for the next change; formalize only when useful. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `ENGINEERING-CONCERNS-PROPORTIONAL` | `engineering-quality.md`; G05,G06,G07,G11; eval:G, K, L, M, AB, AC, BS, BT, BU, CO, DH, DM | **KEEP** · COLD / specialized · state:no | Prevents loss of: Activate only engineering concerns material to the actual change/failure surface and carry them through implementation/evidence without a universal checklist, state field, artifact, dimension change, or new gate by default. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `DEFENSIVE-SECURITY-CONTINUATION` | `engineering-quality.md`; G07,G10,G11; eval:DJ | **KEEP** · COLD / specialized · state:no | Prevents loss of: Security-sensitive AI work states only evidence-backed defensive authorization/scope, preserves provider/platform policy and safety boundaries, uses approved secret/runtime mechanisms without relaying raw secret values when authorized credentialed access is needed, and continues safely allowed analysis/remediation/testing when a detail is restricted. Independent/read-only reviewers prefer source/diff, repository-owned existing tests, current CI/log/artifact evidence, and safe inspection instead of inventing novel adversarial probes; missing assurance becomes a finding/limitation without weakening security, while explicitly scoped defensive implementation/remediation testing remains available when authorized and policy-permitted. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `FAST-FULL-SELECT` | `master-cycle.md`; G03; eval:K, L, AB, CF, CM | **COMPRESS** · WARM / triggered · state:optional | Prevents loss of: FAST/FULL selection follows ambiguity/dependency/review/control need and routine clear Master-only work remains compatible with FAST. Replacement/overlap: `master-cycle.md` remains canonical when the selector is decision-relevant; `SKILL.md` routing may leave the label implicit when it is not. | Same guarantee with fewer hot-path reconstruction steps while preserving the canonical selector. |
| `CONTRACT-PERSISTENCE-INDEPENDENT` | `task-contract.md`; G03,G08; eval:CM | **DERIVE** · WARM / triggered · state:optional | Prevents loss of: FULL does not imply persistence; persistence depends on recovery/coordination value. Existing persistence does not imply FULL. Replacement/overlap: derive from WORK-CLEAR-ENOUGH plus the task-contract persistence test. | Remove separate decision/reminder where the parent invariant is already active. |
| `DELEGATION-PROPORTIONAL` | `master-cycle.md`; G08,G09; eval:Q, AN | **COMPRESS** · WARM / triggered · state:no | Prevents loss of: Delegate only when specialization/throughput/parallelism materially helps; bounded single delegation can remain LIGHTWEIGHT while still using full Worker envelope. Replacement/overlap: same canonical owner; compress duplicate/negative reminders into the positive invariant. | Same guarantee with fewer reminders/words or fewer hot-path reconstruction steps. |
| `SELF-EXECUTION-FALLBACK` | `master-cycle.md`; G05,G16; eval:Q | **DERIVE** · WARM / triggered · state:no | Prevents loss of: If direct Worker dispatch is unavailable, Master self-executes safe authorized work rather than stopping. Replacement/overlap: derive from DELEGATION-PROPORTIONAL + MASTER-STOP-CANONICAL. | Remove separate decision/reminder where the parent invariant is already active. |
| `WIP-FLOW` | `master-cycle.md`; G04,G08; eval:J, R, DL, BU | **COMPRESS** · WARM / triggered · state:no | Prevents loss of: Prefer review/integration/unblocking when they bottleneck; right-size homogeneous outcomes into reviewable candidates, preserve independent implementation/review work that remains fresh, and avoid parallel final acceptance paths that would stale required evidence. Replacement/overlap: same canonical owner; compress duplicate/negative reminders into the positive invariant. | Same guarantee with fewer reminders/words or fewer hot-path reconstruction steps. |
| `SYNTHESIZE-WORK` | `master-cycle.md`; G03,G04,G16; eval:O, AX, DL, DO | **COMPRESS** · WARM / triggered · state:no | Prevents loss of: Outcome incomplete + no READY item triggers refine/unblock/split/investigate, not automatic NO_READY_WORK; phase decomposition starts from current residual scope rather than speculative seams. Replacement/overlap: same canonical owner; compress duplicate/negative reminders into the positive invariant. | Same guarantee with fewer reminders/words or fewer hot-path reconstruction steps. |
| `MASTER-STOP-CANONICAL` | `master-cycle.md`; G04,G16; eval:O, P, R, AW, AX, AP, CN, CQ | **COMPRESS** · WARM / triggered · state:yes | Prevents loss of: Chat turn, commit, PR update, review, Worker handoff, tool batch, or missing delegation is not a Master stop; stop only at canonical boundary after continuation test. Replacement/overlap: same canonical owner; compress duplicate/negative reminders into the positive invariant. | Same guarantee with fewer reminders/words or fewer hot-path reconstruction steps. |
| `WORKER-BOUNDED` | `worker-protocol.md`; G09; eval:CC, CP | **KEEP** · COLD / specialized · state:no | Prevents loss of: Worker owns exactly one assignment and never reprioritizes, broadens scope, upgrades envelope, integrates target, or owns release. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `ASSIGNMENT-IDENTITY` | `task-contract.md`; G09,G12; eval:AK, AM, AV | **KEEP** · WARM / triggered · state:no | Prevents loss of: Dispatch persists exact assignment generation, contract revision, repository/base/branch/target/Worker/envelope identity before editing. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `START-HEAD-HISTORICAL` | `worker-protocol.md`; G09; eval:CR | **COMPRESS** · COLD / specialized · state:no | Prevents loss of: Initial `Expected Starting HEAD` is verified once; authorized Worker commits do not make the assignment stale. Replacement/overlap: same canonical owner; compress duplicate/negative reminders into the positive invariant. | Same guarantee with fewer reminders/words or fewer hot-path reconstruction steps. |
| `CORRECTION-CHECKPOINT` | `worker-protocol.md`; G09; eval:CR | **COMPRESS** · COLD / specialized · state:no | Prevents loss of: Same-generation correction/resume uses a fresh reviewed/current HEAD checkpoint as the concurrency guard. Replacement/overlap: same canonical owner; compress duplicate/negative reminders into the positive invariant. | Same guarantee with fewer reminders/words or fewer hot-path reconstruction steps. |
| `STALE-ASSIGNMENT` | `worker-protocol.md`; G09; eval:D, AV | **KEEP** · COLD / specialized · state:yes | Prevents loss of: Material assignment/envelope invalidation or uncertain materiality stops Worker with STALE_ASSIGNMENT; Worker never guesses/overwrites. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `WORKER-STOP-LOCAL` | `master-cycle.md`; G09,G16; eval:R, CK | **DERIVE** · WARM / triggered · state:optional | Prevents loss of: Worker stop/handoff does not automatically become Master stop; Master absorbs, corrects, redispatches, self-executes, or switches work when possible. Replacement/overlap: derive from WORKER-BOUNDED + MASTER-STOP-CANONICAL. | Remove separate decision/reminder where the parent invariant is already active. |
| `WORKER-HANDOFF-PRECEDENCE` | `worker-protocol.md`; G09; eval:CK | **COMPRESS** · COLD / specialized · state:yes | Prevents loss of: Handoff status is determined by explicit precedence so stale/blocking states cannot be mislabeled DONE. Replacement/overlap: same canonical owner; compress duplicate/negative reminders into the positive invariant. | Same guarantee with fewer reminders/words or fewer hot-path reconstruction steps. |
| `WORKER-TARGET-SEPARATION` | `worker-protocol.md`; G09; eval:AM, CP | **KEEP** · COLD / specialized · state:no | Prevents loss of: Assigned branch cannot be the canonical Integration Target; Worker does not integrate target. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `REVIEW-EFFECTIVE-CHANGE` | `review-integration.md`; G07,G11; eval:E | **KEEP** · WARM / triggered · state:no | Prevents loss of: Review current target-to-candidate effective change, not stale narrative or only author intent. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `REVIEW-IDENTITY-FRESH` | `review-integration.md`; G07,G11; eval:E, CJ, DN, BU | **KEEP** · WARM / triggered · state:no | Prevents loss of: Approval/evidence is bound to target, candidate, contract, and relevant SHA; material drift invalidates transfer; Draft/Ready may signal maturity only when repository/platform semantics make it useful and never replaces freshness evidence. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep one review owner and avoid a separate PR-maturity state/rule. |
| `UNTRUSTED-EXECUTION-SURFACE` | `review-integration.md`; G07,G11; eval:M | **KEEP** · WARM / triggered · state:no | Prevents loss of: Inspect changed hooks/scripts/workflows/supply-chain surfaces before executing untrusted candidate code. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `CI-CLASSIFY` | `review-integration.md`; G05,G07,G11; eval:F, CL, DM | **KEEP** · WARM / triggered · state:no | Prevents loss of: CI failure is classified by candidate/baseline/environment/transient cause before deciding the next action. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `CONFLICT-RECONCILE` | `review-integration.md`; G05,G11; eval:E | **COMPRESS** · WARM / triggered · state:no | Prevents loss of: Resolve conflicts against fresh target/effective change and revalidate affected evidence. Replacement/overlap: same canonical owner; compress duplicate/negative reminders into the positive invariant. | Same guarantee with fewer reminders/words or fewer hot-path reconstruction steps. |
| `INTEGRATION-GATE` | `review-integration.md`; G11; eval:H, CI, CJ | **KEEP** · WARM / triggered · state:no | Prevents loss of: Integrate only after current acceptance, review, CI/policy, target/candidate identity, and applicable action gates are satisfied. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `SELF-AUTHORED-FRESH-REVIEW` | `review-integration.md`; G07,G11; eval:BC | **COMPRESS** · WARM / triggered · state:no | Prevents loss of: Master-authored work still receives a fresh diff/acceptance review; independent review only when risk/profile requires it. Replacement/overlap: same canonical owner; compress duplicate/negative reminders into the positive invariant. | Same guarantee with fewer reminders/words or fewer hot-path reconstruction steps. |
| `POST-INTEGRATION-RECONCILE` | `review-integration.md`; G01,G11; eval:CO | **COMPRESS** · WARM / triggered · state:no | Prevents loss of: After integration, reconcile immutable result and continue to delivery only when required by outcome. Replacement/overlap: same canonical owner; compress duplicate/negative reminders into the positive invariant. | Same guarantee with fewer reminders/words or fewer hot-path reconstruction steps. |
| `RECOVERY-EVENT-DRIVEN` | `continuity.md`; G12; eval:U, BG, BH | **COMPRESS** · COLD / specialized · state:no | Prevents loss of: Full recovery happens on new/replacement Master or material invalidation, not on ordinary progress/tool batches/expected transitions. Replacement/overlap: same canonical owner; compress duplicate/negative reminders into the positive invariant. | Same guarantee with fewer reminders/words or fewer hot-path reconstruction steps. |
| `RECOVERY-AUTHORITATIVE` | `continuity.md`; G12,G13; eval:A, I | **KEEP** · COLD / specialized · state:no | Prevents loss of: Recovery reconstructs from authoritative repository/GitHub/release evidence, not old chat or Worker narrative. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `ROTATION-SIGNAL-DRIVEN` | `continuity.md`; G12; eval:U | **MERGE** · COLD / specialized · state:no | Prevents loss of: Long context alone does not require rotation; rotate when continuity/reliability signals justify it. Replacement/overlap: merge trigger wording into RECOVERY-EVENT-DRIVEN / continuity rotation section. | One trigger/decision representation instead of two overlapping reminders. |
| `ROTATION-SAFE-BOUNDARY` | `continuity.md`; G12; eval:AH, BB, CE | **COMPRESS** · COLD / specialized · state:no | Prevents loss of: Rotate only at a recoverable boundary and carry established Authority/current effective controls without becoming more permissive. Replacement/overlap: same canonical owner; compress duplicate/negative reminders into the positive invariant. | Same guarantee with fewer reminders/words or fewer hot-path reconstruction steps. |
| `CHAT-NONAUTHORITATIVE` | `continuity.md`; G12,G13; eval:I, Z | **DERIVE** · COLD / specialized · state:no | Prevents loss of: Conversation context is disposable and must not be the sole owner of project state. Replacement/overlap: derive from TRUTH-ONE-OWNER + RECOVERY-AUTHORITATIVE. | Remove separate decision/reminder where the parent invariant is already active. |
| `ROOT-SPEC-CANONICAL` | `governance.md`; G02; eval:BV, BW, BX, CD, CY | **KEEP** · COLD / specialized · state:no | Prevents loss of: First ownership resolves the project-defining prompt/spec and keeps one safe canonical repository copy, excluding unsafe material. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `ROOT-SPEC-OFF-HOT-PATH` | `governance.md`; G02,G13; eval:BY, BZ, CA | **DERIVE** · COLD / specialized · state:no | Prevents loss of: Normal cycles operate from nearer downstream authoritative sources; root spec is reread only when intent conflict/change makes it relevant. Replacement/overlap: derive from TRUTH-ONE-OWNER + progressive routing/recovery. | Remove separate decision/reminder where the parent invariant is already active. |
| `BOOTSTRAP-PROPORTIONAL` | `governance.md`; G06,G14; eval:AZ, BS, BT | **COMPRESS** · COLD / specialized · state:no | Prevents loss of: First ownership repairs only readiness that materially helps execution/recovery; stop bootstrapping when its completion test passes. Replacement/overlap: same canonical owner; compress duplicate/negative reminders into the positive invariant. | Same guarantee with fewer reminders/words or fewer hot-path reconstruction steps. |
| `ARTIFACT-FITNESS` | `governance.md`; G06,G14,G15; eval:BS, BU | **COMPRESS** · COLD / specialized · state:no | Prevents loss of: Reuse existing engineering systems when fit; repair/replace only when evidence shows material execution value, including CI critical-path improvements that preserve required signal. Replacement/overlap: same canonical owner; compress duplicate/negative reminders into the positive invariant. | Same guarantee with fewer reminders/words or fewer hot-path reconstruction steps. |
| `READY-DONE-SEMANTICS` | `governance.md`; G05,G14; eval:BE | **COMPRESS** · COLD / specialized · state:yes | Prevents loss of: READY/DONE represent executable/verified lifecycle semantics, not empty scaffolding or ceremony. Replacement/overlap: same canonical owner; compress duplicate/negative reminders into the positive invariant. | Same guarantee with fewer reminders/words or fewer hot-path reconstruction steps. |
| `RELEASE-MODEL-DISCOVER` | `release.md`; G11; eval:CS | **KEEP** · COLD / specialized · state:no | Prevents loss of: Discover the repository/deployment release model before assuming process or target semantics. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `INTEGRATED-NOT-DELIVERED` | `release.md`; G01,G11; eval:CO | **KEEP** · COLD / specialized · state:yes | Prevents loss of: Integration and delivery are separate completion states; production-required work remains open until delivery evidence proves it. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `PRODUCTION-DETERMINISTIC-EFFECT` | `release.md`; G11; eval:H, BO, CG | **COMPRESS** · COLD / specialized · state:no | Prevents loss of: An upstream action that deterministically causes production is classified/gated as production before action. Replacement/overlap: same canonical owner; compress duplicate/negative reminders into the positive invariant. | Same guarantee with fewer reminders/words or fewer hot-path reconstruction steps. |
| `MIGRATION-ROLLBACK` | `release.md`; G11; eval:G | **KEEP** · COLD / specialized · state:no | Prevents loss of: High-risk migration/production work requires proportionate rollback/recovery readiness before irreversible exposure. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `PRODUCTION-GATE` | `release.md`; G11; eval:H, CV | **KEEP** · COLD / specialized · state:no | Prevents loss of: Production mutation requires the canonical production authorization gate; pre-authorization is scope-bound. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `POST-RELEASE-EVIDENCE` | `release.md`; G01,G07,G11; eval:CO, CT | **KEEP** · COLD / specialized · state:optional | Prevents loss of: Deployment success alone is insufficient; verify intended artifact/environment/health/acceptance evidence. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `INCIDENT-CONTAINMENT` | `release.md`; G11; eval:CT | **KEEP** · COLD / specialized · state:no | Prevents loss of: When current production identity/state is wrong or unsafe, containment outranks normal delivery flow. Replacement/overlap: none; unique guarantee remains canonical. | No semantic reduction; keep single owner and avoid duplicate reminders. |
| `RELEASE-CLOSEOUT` | `release.md`; G01,G11; eval:P, CO | **COMPRESS** · COLD / specialized · state:no | Prevents loss of: Close only after required delivery, evidence, state reconciliation, and remaining risks/rollback obligations are resolved or explicitly owned. Replacement/overlap: same canonical owner; compress duplicate/negative reminders into the positive invariant. | Same guarantee with fewer reminders/words or fewer hot-path reconstruction steps. |

## Audit result

- Total canonical Rule IDs audited: **69**
- KEEP: **37**
- COMPRESS: **24**
- DERIVE: **7**
- MERGE: **1**
- MOVE_COLD Rule IDs: **0** — no Rule ID is classified into a separate MOVE_COLD semantic category. `MACHINE-RELAY-PORTABLE` retains **KEEP** semantics but its canonical runtime owner is intentionally relocated from the hot `SKILL.md` kernel to `relay-transport.md`; `SKILL.md` keeps only activation/routing. One bulky supporting protocol (`independent-review.md`) is moved colder so ordinary review/CI/integration does not materialize its relay/result schema.
- REMOVE: **0 semantic guarantees** — no protected guarantee had enough evidence to delete outright; the safe simplification is representation/routing/derivation rather than weakening semantics.

## Candidate decisions produced by this audit

1. **Routine Master hot path:** `ExecutionPath=FAST|FULL` does not need to be materialized merely to perform clear bounded Master-only work. The candidate removes unconditional `master-cycle.md` loading and keeps FAST semantics implicit until the control choice becomes decision-relevant.
2. **Outcome sizing:** existing `WIP-FLOW` is compressed/extended rather than adding a new fragmentation rule: one minimum meaningful slice normally maps to one reviewable candidate; multiple PRs require a material control boundary or genuine reviewability need.
3. **Contract lifecycle:** existing persistence semantics now keep one accepted-outcome contract open across cohesive partial PRs rather than creating sibling seam contracts; existing `TaskState` lifecycle remains the sole source of legitimate terminal states.
4. **Phase entry/cutline:** existing synthesis/cutline logic now starts from integrated residual scope; no new phase state is introduced.
5. **Candidate maturity:** Draft/Ready is used only when repository/platform semantics make it useful; it remains review presentation under existing freshness/WIP semantics, not a new `TaskState`.
6. **Acceptance WIP:** independent implementation and review work that remains fresh stays available; only affected final target-bound acceptance/integration is serialized when one integration would stale sibling evidence, unless intentional stacking/queue preserves freshness.
7. **CI fitness:** existing `ARTIFACT-FITNESS` / engineering-quality path covers measured isolation-preserving sharding; no shard count or project-specific CI recipe enters the Skill.
8. **Derived rules:** capability-vs-authority, obligation union, persistence independence, self-execution fallback, Worker-stop locality, chat non-authority, and root-spec hot-path avoidance remain protected Rule IDs/evals but need no additional standalone hot-path decision machinery.
9. **Rotation trigger:** signal-driven rotation is treated as the rotation face of event-driven recovery rather than another hot-path state.
10. **Review protocol locality:** ordinary review/CI/conflict/integration keeps `review-integration.md`; independent-review handoff/result machinery is a separate directly routed cold reference loaded only when separation is actually required.
11. **Selector ownership:** `master-cycle.md` remains the sole FAST/FULL selector; `task-contract.md` now contains only contract/READY consequences and persistence, avoiding a second examples/promotion rule block.
12. **MachineRelay locality:** `SKILL.md` keeps the universal output classifier/activation, while `relay-transport.md` owns the relay-only predicate and transport details; normal user-facing responses no longer materialize that protocol.
13. **Worker-entry locality:** the hot kernel keeps only the Worker pre-edit route and non-negotiable ownership guardrails; detailed dispatch/staleness/correction/handoff semantics stay in `worker-protocol.md` + `task-contract.md`.

## Representation-cost check

At the candidate point immediately before this audit:
- always-loaded `skill/SKILL.md` was already smaller than v1.3.7 and no new state/rule namespace had been added;
- the field-derived semantics were compressed into existing owners instead of creating a new runtime rule family;
- tests/evals/design evidence may grow because #112 explicitly permits evidence growth to protect runtime simplification.

This audit does not by itself prove model-level improvement. #116 requires exact-candidate validation plus fresh GPT-5.6 Sol evaluation when needed to substantiate behavioral/decision-quality claims, with targeted replication of any material strategy divergence before merge/release.

## Structural representation audit — decision architecture

The second-pass audit evaluates the runtime as a model decision system rather than as prose. The preferred representation follows these constraints:

1. **Hot kernel = invariants + routing, not specialist protocol payloads.** Always-loaded text should establish Role/stable dimensions, universal invariants, source authority, minimal Master/Worker entry behavior, and direct event routing. Large result schemas/templates belong behind the event that needs them.
2. **One selector/owner per decision.** A consumer may carry the exact field/result it needs, but it should not restate another domain's selection algorithm. `master-cycle.md` therefore remains the FAST/FULL selector; `task-contract.md` owns only contract/READY consequences and persistence.
3. **Direct reachability beats hidden prerequisite chains.** Every operational domain remains directly routable from `SKILL.md`; moving a block colder must not require the model to remember an indirect load order.
4. **Split only when locality saves common-path reconstruction.** A new reference is justified when a large block is irrelevant to a more common sibling event. The independent-review handoff/result protocol qualifies; the tightly coupled authority gate/boundary algorithm does not currently justify another split.
5. **Transport/schema repetition is not semantic ownership duplication.** Exact Worker assignment fields legitimately appear in the canonical persisted assignment schema and in dispatch/handoff transport. The schema owner remains singular; consumers do not redefine its semantics.
6. **Safety boundary reminders may repeat effects, not algorithms.** Release/review/Worker domains may remind the model that a canonical gate/lifecycle applies, but the gate/state transition algorithm stays with its owner.
7. **Cold evidence may grow to protect a smaller operational representation.** Evaluation text is not a normal execution reference and may carry comparison variants that prove the routing/representation change does not narrow behavior.

### Structural changes retained

- `SKILL.md`: removed duplicate independent-review semantics and duplicate `HUMAN OPERATION REQUIRED` payload fields; both remain directly routable to their canonical domains.
- `review-integration.md`: ordinary review/freshness/CI/conflict/integration remains warm; the bulky independent-review relay/result protocol moved to directly routed `independent-review.md`.
- `task-contract.md`: removed the second FAST examples/promotion block; `master-cycle.md` remains the sole FAST/FULL selector.
- `master-cycle.md`: self-review now routes to the review domain rather than restating the independence selector.
- Eval BC now includes a routine self-authored comparison variant so independent-review machinery is required only when separation is actually triggered.

### Multi-scenario load check

Word counts model materialized orchestration/reference text, not model latency. Baseline Master scenarios include v1.3.7's unconditional `master-cycle.md` load. `133a` is the previous exact candidate before this structural pass. Relay-only references are counted only for user-visible MachineRelay output.

| Scenario archetype | v1.3.7 words | `133a` words | structural candidate words | vs `133a` |
|---|---:|---:|---:|---:|
| routine bounded Master implementation | 5,118 | 1,833 | 1,513 | **-320** |
| routine Master + current review | 7,950 | 4,703 | 3,502 | **-1,201** |
| routine Master + integration gate | 10,669 | 7,422 | 6,221 | **-1,201** |
| CI failure triage | 7,950 | 4,703 | 3,502 | **-1,201** |
| independent HIGH_ASSURANCE review + relay | 7,950 | 4,703 | 4,392 | **-311** |
| FULL Master planning + contract | 7,148 | 7,099 | 6,704 | **-395** |
| Worker execution before handoff | 5,611 | 5,622 | 5,217 | **-405** |
| Worker handoff MachineRelay | 5,611 | 5,622 | 5,331 | **-291** |
| human-relayed Worker dispatch | 8,893 | 8,844 | 8,559 | **-285** |
| first ownership + planning | 7,678 | 7,615 | 7,301 | **-314** |
| recovery/resume only | 7,246 | 3,927 | 3,606 | **-321** |
| Master rotation MachineRelay | 7,246 | 3,927 | 3,720 | **-207** |
| release/production gate | 9,118 | 5,833 | 5,513 | **-320** |
| CI/automation fitness + review | 9,668 | 6,455 | 5,254 | **-1,201** |

No sampled archetype regresses in materialized word count. Normal review/CI/integration avoids the cold independent-review protocol; non-relay turns avoid the MachineRelay transport predicate. Relay paths add their cold transport reference only when needed and still remain smaller than `133a` because the always-loaded kernel shrank more than the cold protocol costs.

Final representation totals after protocol compression:

| Surface | v1.3.7 | `133a` | structural candidate |
|---|---:|---:|---:|
| always-loaded kernel | 1,836 words | 1,833 | **1,513** |
| operational refs excluding eval | 20,295 | 20,287 | **20,216** |
| kernel + operational refs | 22,131 | 22,120 | **21,729** |
| all refs including cold eval evidence | 32,926 | 33,316 | **33,295** |
| kernel + all refs | 34,762 | 35,149 | **34,808** |

The normal operational corpus is smaller than both v1.3.7 and `133a`. The small remaining aggregate increase versus v1.3.7 is entirely cold evaluation/evidence growth, not normal execution materialization.

### Duplicate classification after the structural pass

A whole-runtime lexical/TF-IDF scan found no exact repeated operational line across files. High-similarity cross-file pairs remain, but the inspected high-score groups are intentional boundary/transport relationships rather than competing owners:

- `task-contract.md` ↔ `worker-protocol.md`: persisted assignment schema versus exact dispatch/staleness/handoff consumption;
- `engineering-quality.md` ↔ `review-integration.md`: implementation concern activation versus reviewer inspection surface;
- `authority-gates.md` ↔ `master-cycle.md`/`release.md`: canonical boundary/effect definitions versus terminal-timing and production-path reminders; the explicit `MasterBoundary.USER_STOP` authority-domain binding was retained after a regression guard proved it is not disposable prose;
- `task-contract.md`/`release.md`/`review-integration.md`: separate lifecycle dimensions and boundary reminders, not duplicate transition ownership;
- `continuity.md` ↔ assignment/Worker files: recoverability inventory carries exact authoritative assignment fields so a replacement Master can reconstruct state.

The removable owner-like overlaps found by this pass were the independent-review definition/protocol in the hot/common review surfaces, duplicate FAST/FULL examples/promotion logic, duplicate USER_STOP execution wording, and duplicate self-review independence selection. Those were compressed or moved to one owner.

### Structural changes considered but not retained

- **Split `authority-gates.md` further:** rejected for now. It could save words on a simple mutation, but `ApplicableEffects`, `CAN_EXECUTE`, approval obligations, boundary meaning, unknown-write recovery, and optimistic concurrency are safety-coupled. Another file boundary would add routing/reconstruction risk for a safety-critical domain without enough evidence yet.
- **Move Worker assignment identity out of `task-contract.md`:** rejected. The persisted assignment is part of the contract's recoverable identity; the repeated Worker fields are transport consumption, not a competing owner. Moving them would add another hop on every Worker path.
- **Split the New Master relay template from `continuity.md`:** rejected for now. Continuity is already cold/event-triggered; the potential saving is smaller and would add another direct router target for a comparatively rare path.
- **Reorder `SKILL.md` solely for aesthetics:** rejected. The entrypoint is materialized as one unit, so moving the router earlier would not reduce tokens or reference hops; the current Role → invariants → truth → role kernel/router organization is coherent and changing order without behavioral evidence would create review churn.

This structural analysis supports a theoretical **general decision-cost improvement** across distinct task families while preserving the same rule/state/eval inventory. It is not a measured claim about GPT latency, token billing, or decision-quality percentage; live-model A/B evidence would still be required for such claims.

## Final old-vs-new semantic-preservation audit

This pass supersedes the earlier third-pass conclusion where any claim conflicts with this section. The comparison is against exact pre-format candidate `88729e211873440542bd2dbd74a3cc2dc16a1441` and asks whether the **old wording/shape should have remained**, not whether the new representation is shorter.

The governing rule is: **semantic completeness first, decision locality second, context reduction third.** A formatting change is retained only when the protected decision remains at least as explicit as before.

### External Skill-design cross-check

The Skill-creator guidance independently supports:

- concise but explicit frontmatter triggers because metadata controls Skill invocation;
- progressive loading and direct one-level references;
- clear sequential steps for ordered workflows and explicit decision points for branches;
- scripts for deterministic fragile behavior;
- **a table of contents at the top of reference files longer than 100 lines**.

That last point invalidated the earlier assumption that all operational TOCs were disposable duplicate context. The eight TOCs removed in the third pass were restored. `engineering-quality.md` remains below 100 lines and therefore does not need one; `eval-scenarios.md` already has one.

### Pairwise representation verdict

| Surface | Old representation strength | New representation strength | Final decision |
|---|---|---|---|
| Skill frontmatter | explicitly named `improve/develop` and concrete GitHub management surfaces | more concise and easier to scan | **Hybrid:** keep concise description but explicitly restore bootstrapping/developing/improving/managing/continuing/finishing/recovering and GitHub Issues/Projects/milestones triggers. |
| Long-reference TOCs | gives the model a scope map before reading 100+ line references | removing them saved a small amount of context | **Old is better:** restore TOCs because scope preview is useful and recommended by Skill-design guidance. |
| Repository mutation scope | complete but encoded four branches in dense prose | case table exposes persistent expansion, one-off scope, delegation, and out-of-scope handoff directly | **New is better after repair:** retain table and preserve the canonical-matrix qualifier and all no-expansion semantics. |
| `MISSING_CAPABILITY` / stop guards | explicitly distinguished equivalent route, speculative probing, transient failure, retry evidence, and new-turn non-evidence | table gives Boundary → Guard lookup | **New is better only after repair:** keep table and restore every old operational discriminator. |
| Recovery sequence | exact semantics, but mixed numbered steps + prose + nested bullet branches created two mental organizations | one three-layer progressive table localizes Orientation / Active path / Triggered depth | **New is better only after repair:** retain table, restore the Triggered-depth interrupt, authoritative-workstream wording, and ambiguous-repository read-only + exact-scope-question behavior. |
| Retention / preflight completeness | complete but multi-clause prose | independent bullets separate independent obligations | **New is better:** retain bullets while restoring explicit completeness-flag authority and bounded high-cardinality-list semantics. |
| Engineering concern propagation | role headings are readable and complete | role/surface table makes the selector explicit | **New is better after repair:** retain table; restore `materially affect`, stronger-source recoverability, selected-failure-mode solution wording, no silent Worker broadening, and no whole-catalog dispatch. |
| Review delta freshness | complete prose bound to exact candidate and affected assumption surfaces | decision table makes transfer/widen decisions explicit | **New is better after repair:** retain table; restore `prior exact reviewed candidate` and `every affected interaction/assumption/evidence surface`. |
| Validation evidence plan | one long paragraph mixed three independent rules | bullets separate minimum proof, execution order, and reuse freshness | **New is better:** no semantic loss found. |
| Task assignment staleness | duplicated Worker-staleness classifier in `task-contract.md` | `task-contract.md` owns identity data; `worker-protocol.md` owns the classifier | **New is better:** intentional de-duplication; every old invalidation condition remains in the Worker owner. |
| `contract_check.py` behavior | detailed, non-obvious helper semantics were explicit | compression hid exact parser/rejection behavior | **Old detail is better, new form is better:** restore the full behavior as bullets rather than a lossy summary. |
| Worker handoff classifier | detailed prose repeated the status table | one precedence table is the canonical classifier | **New is better:** table retains all status distinctions; following prose keeps only cross-namespace approval/absorption nuance. |
| Worker correction/resume | complete but 174-word procedural paragraph | four ordered steps make generation → checkpoint → relay → reissue order explicit | **New is better after repair:** retain steps and restore explicit “correction/resume never broadens `RepositoryMutationScope`”. |
| Rule-map traceability | line numbers are precise until formatting changes | section anchors remain stable across formatting-only edits | **New is better:** section-level traceability avoids stale references without weakening ownership. |

### Semantic-loss findings caught by this re-check

The third-pass representation was **not fully lossless**. The following were found and repaired before accepting the representation:

1. Frontmatter no longer explicitly named `develop/improve`, which could reduce invocation recall for a primary Skill trigger.
2. Long-reference TOCs had been removed despite Skill-design guidance recommending them for >100-line references.
3. Recovery lost the explicit ability to jump from Orientation directly to Triggered depth before unrelated Active-path reading.
4. Recovery weakened the explicit “never reconstruct writable repository scope from repository/project artifacts; ask the smallest exact scope question when ambiguous” behavior.
5. `MasterBoundary.MISSING_CAPABILITY` compression dropped explicit equivalent-route use, anti-speculative-probing, transient-failure discrimination, and “new turn/tool batch alone is not evidence”.
6. `contract_check.py` compression dropped exact parser/rejection behavior including `--level`, `Issue:`/`--issue`, fenced examples/comments, branch/target constraints, zero object IDs, and compatibility ambiguity handling.
7. Worker correction wording no longer explicitly said correction/resume cannot broaden repository mutation scope.
8. Review-delta text weakened `prior exact reviewed candidate` to `prior reviewed candidate` and compressed the affected interaction/assumption/evidence surface wording.
9. Engineering-quality wording changed `materially affect` to `materially change`, weakened stronger-source recoverability language, and removed explicit no-whole-catalog/no-silent-broadening reminders.

All nine were restored without reverting the useful structural changes.

### Cross-scenario equivalence ledger

| Scenario | Old decision | Final hybrid decision | Equivalent? |
|---|---|---|---|
| recovery trigger already visible during Orientation | enter only needed triggered depth before unrelated active-path reading | same, explicitly restored | **yes** |
| chat loss with no trigger | Orientation → Active path; do not load root spec merely for chat loss | same | **yes** |
| ambiguous writable repository on replacement Master | keep read-only and ask smallest exact scope question; never infer from project artifacts | same, explicitly restored | **yes** |
| preferred tool unavailable but equivalent authoritative route exists | use equivalent route; not `MISSING_CAPABILITY` | same | **yes** |
| transient operation failure / new chat turn | do not classify missing capability or blindly retry without new evidence | same, explicitly restored | **yes** |
| no pre-existing READY Issue | synthesize/refine/unblock/investigate before `NO_READY_WORK` | same | **yes** |
| engineering concern is merely theoretical | do not expand scope or delay useful delivery | same | **yes** |
| Worker discovers material concern outside current envelope | stop/revise contract; never silently broaden | same, explicitly restored | **yes** |
| exact candidate changes but assumptions on unchanged surfaces remain valid | fresh exact-candidate verdict; reuse still-valid prior analysis/evidence | same | **yes** |
| review delta changes shared interface/security/acceptance assumption | widen review to every affected dependent surface | same, more explicit in table | **yes** |
| local focused test + required CI prove different guarantees | keep minimum sufficient independent proof; do not duplicate no-value proof | same | **yes** |
| unchanged green proof assumptions remain current | reuse evidence; no ceremonial rerun | same | **yes** |
| Worker assignment ID/revision/repository/target/envelope drifts | `WorkerStatus.STALE_ASSIGNMENT` | same; single owner in Worker protocol | **yes** |
| unrelated dirty state can be safely isolated by runtime/environment switch | `ENVIRONMENT_MISMATCH` | same in precedence table | **yes** |
| unrelated dirty state requires external ownership/precondition | `BLOCKED` | same in precedence table | **yes** |
| in-scope Worker action is waiting on human approval | Worker returns `BLOCKED`; Master may classify `APPROVAL_REQUIRED` after absorption | same | **yes** |
| same-generation correction on exact reviewed checkpoint | keep assignment ID, verify checkpoint before edit | same, now sequential | **yes** |
| correction responsibility moves to another Worker / generation invalidated | mint fresh Assignment ID | same | **yes** |
| correction relay names another repository | preserve exact dispatch repository; never broaden mutation scope | same, explicitly restored | **yes** |
| `contract_check.py --worker --level ...` with malformed target/placeholder/zero OID | reject according to detailed helper semantics | same, restored as bullets | **yes** |
| long reference is loaded | model gets a compact scope map before detailed sections | restored old TOC behavior | **yes** |

### Representation diagnostics after semantic repair

Compared with `88729e2`:

| Diagnostic | `88729e2` | final hybrid working representation |
|---|---:|---:|
| exact repeated operational-line groups across files | 0 | **0** |
| semantic-similarity cross-file pairs ≥ 0.40 | 88 | **79** |
| high-similarity pairs ≥ 0.60 | 12 | **11** |
| prose paragraphs ≥65 words | 45 | **34** |
| words inside those long paragraphs | 4,062 | **2,864** |
| long references >100 lines lacking TOC | 1 | **0** |
| Rule IDs | 69 | **69** |
| canonical Rule-owner changes relative to `88729e2` | baseline | **1 intentional (`MACHINE-RELAY-PORTABLE` → `relay-transport.md`)** |
| standalone eval IDs | 121 | **121** |
| state namespace value sets | baseline-preserved | **unchanged** |

Historical TOC detail: at `88729e2`, `engineering-quality.md` had 102 newline-terminated lines (103 logical lines) and no `## Contents`; the current file has 91 newline-terminated lines (92 logical lines), so it is below the >100-line TOC threshold.

### Multi-scenario materialization after restoring semantics

These are actual words selected from runtime files, not a model-quality or latency metric.

| Scenario archetype | v1.3.7 | `88729e2` | final hybrid working | delta vs `88729e2` |
|---|---:|---:|---:|---:|
| routine bounded Master | 5,118 | 1,513 | **1,499** | **-14** |
| normal review | 7,950 | 3,502 | **3,493** | **-9** |
| integration gate | 10,669 | 6,221 | **6,203** | **-18** |
| CI failure triage | 7,950 | 3,502 | **3,493** | **-9** |
| independent HIGH_ASSURANCE review + relay | 7,950 | 4,392 | **4,383** | **-9** |
| FULL planning + contract | 7,148 | 6,704 | **6,646** | **-58** |
| Worker execution | 5,611 | 5,217 | **5,089** | **-128** |
| Worker handoff MachineRelay | 5,611 | 5,331 | **5,203** | **-128** |
| human-relayed Worker dispatch | 8,893 | 8,559 | **8,431** | **-128** |
| first ownership + planning | 7,678 | 7,301 | **7,287** | **-14** |
| recovery/resume | 7,246 | 3,606 | **3,539** | **-67** |
| Master rotation MachineRelay | 7,246 | 3,720 | **3,653** | **-67** |
| release/production gate | 9,118 | 5,513 | **5,490** | **-23** |
| CI/automation fitness + review | 9,668 | 5,254 | **5,210** | **-44** |

No sampled archetype is larger than `88729e2` after restoring the lost semantics and required TOCs. The savings are intentionally smaller than the earlier third-pass numbers because semantic completeness and recommended long-reference navigation were restored.

### Whole representation after semantic repair

| Surface | v1.3.7 | `88729e2` | final hybrid working |
|---|---:|---:|---:|
| always-loaded kernel | 1,836 | 1,513 | **1,499** |
| operational refs excluding eval | 20,295 | 20,216 | **20,010** |
| kernel + operational refs | 22,131 | 21,729 | **21,509** |
| all refs including cold eval evidence | 32,926 | 33,295 | **33,089** |
| kernel + all refs | 34,762 | 34,808 | **34,588** |

### Guard changes

`tests/test_phase_c_runtime_migration.py` now protects not just formatting but non-obvious semantics that were almost lost:

- TOC presence for every >100-line reference;
- explicit frontmatter trigger verbs;
- equivalent-route / transient-failure / no-new-evidence `MISSING_CAPABILITY` semantics;
- direct Triggered-depth interrupt and repository-scope recovery guards;
- exact `contract_check.py` behavior;
- Worker correction repository-scope non-expansion;
- engineering concern wording with no silent broadening / no whole-catalog relay;
- exact-candidate review baseline and affected assumption/evidence surfaces.

### Final evidence boundary

This final hybrid representation is a stronger theoretical candidate than either pure old prose or the initial pure-format compression because it preserves the old semantic contract while exposing more branch/precedence/order structure locally and reducing duplicate owner-like text.

It still does **not** prove that GPT-5.6 Sol has a measured accuracy, latency, or billed-token improvement. The server has no provisioned live model provider, so a live paired model A/B remains the evidence required for a numerical model-performance claim.
