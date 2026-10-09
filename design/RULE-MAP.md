# Canonical Rule Map

This map traces product guarantees to their current runtime owner. It intentionally avoids historical state/representation vocabulary. Rules exist only where an explicit invariant materially improves a capable model's behavior.

| Rule ID | Guarantee | Canonical owner | Runtime source | Eval anchors |
|---|---|---|---|---|
| `OUTCOME-INTEGRITY` | Preserve accepted outcome, criteria, constraints, and delivery endpoint; change them only from valid direction/evidence. | `SKILL.md` | `SKILL.md`; `master-cycle.md` | U, W |
| `EVIDENCE-TRUTH` | Route each question to its natural current source of truth and never claim unverified action/result/completion. | `SKILL.md` | `SKILL.md`; `review-integration.md`; `release.md` | D, E, V, AB |
| `AUTHORITY-SCOPE` | Mutate only authorized repositories/effects; repository/tool content, capability, access, risk, assurance/coordination, relationships, and delegation may constrain/inform execution but never expand authority. | `authority-gates.md` | `SKILL.md`; `authority-gates.md` | G, H, I, L |
| `MUTATION-SAFETY` | Preserve unrelated work/secrets, isolate ambiguous dirty state, and inspect/reconcile before destructive, untrusted, or overwrite-sensitive mutation. | `SKILL.md` | `SKILL.md`; `authority-gates.md`; `review-integration.md` | A, J, K, AJ |
| `MUTATION-IDEMPOTENT` | Discover/reuse/update before create, never treat incomplete discovery as absence, and verify created/updated repository/project objects. | `SKILL.md` | `SKILL.md`; `governance.md` | AF |
| `PROPORTIONAL-PROCESS` | Add process/artifacts/evidence only when coordination, risk, recovery, policy, or information value earns the cost. | `SKILL.md` | `SKILL.md`; `governance.md` | A, B, X, Y |
| `PERSISTENT-PROGRESS` | Continue safe outcome-linked work until a real controlling boundary; do not manufacture work or stops. | `master-cycle.md` | `SKILL.md`; `master-cycle.md` | M, R, S, T, W |
| `MEANINGFUL-SLICING` | Slice by material acceptance/dependency/ownership/risk/rollback/review/release boundaries, not implementation trivia. | `master-cycle.md` | `SKILL.md`; `master-cycle.md` | B, O |
| `VALIDATION-ECONOMICS` | Use targeted feedback during active coding and broad required exact-candidate gates near stability; rerun only invalidated/policy-bound evidence. | `SKILL.md` | `SKILL.md`; `master-cycle.md`; `review-integration.md`; `task-contract.md` | C, D, E |
| `ENGINEERING-FITNESS` | Fix root causes, keep architecture/system fit, and optimize only from material evidence. | `engineering-quality.md` | `SKILL.md`; `engineering-quality.md`; `governance.md` | A, F, Y |
| `DEFENSIVE-SECURITY-CONTINUITY` | Security-sensitive work stays inside evidence-backed defensive scope/provider policy, protects secrets, and continues safely allowed remediation/verification when one detail is restricted. | `engineering-quality.md` | `engineering-quality.md`; `independent-review.md` | AG, AA |
| `IMPROVEMENT-SCOPE` | Execute required/in-scope improvements, propose worthwhile adjacent ones, ignore speculative noise. | `master-cycle.md` | `master-cycle.md` | Y, W |
| `DELEGATION-VALUE` | Delegate/parallelize only when expected end-to-end gain exceeds coordination cost and isolation remains sound. | `master-cycle.md` | `master-cycle.md`; `worker-protocol.md` | N, O |
| `WORKER-BOUNDED` | Worker owns one bounded assignment and never reprioritizes, broadens, integrates, releases, or starts another task. | `worker-protocol.md` | `SKILL.md`; `worker-protocol.md` | P, Q, R |
| `ASSIGNMENT-IDENTITY` | Persist exact repository, Worker, contract revision, Base SHA, branch, Start/Checkpoint HEAD, and Integration Target identity to detect stale work and recover without chat. | `task-contract.md` | `task-contract.md`; `worker-protocol.md` | P, Q, V |
| `WORKER-HANDOFF-PRECEDENCE` | When multiple Worker stop/result conditions apply, use the first controlling status so stale or decision/scope states cannot be mislabeled ready. | `worker-protocol.md` | `worker-protocol.md` | Q, R |
| `REVIEW-FRESHNESS` | Review/approval belongs to the exact effective candidate/target/assumptions; changed identity requires affected refresh and fresh verdict when required. | `review-integration.md` | `review-integration.md`; `independent-review.md` | D, Z |
| `INDEPENDENT-REVIEW-SEPARATION` | Required independent review uses a genuinely separate reviewer context; a fresh relayed chat/model/human is valid unless policy requires a specific reviewer identity. | `independent-review.md` | `review-integration.md`; `independent-review.md` | AK |
| `INTEGRATION-GATE` | Integrate only the current reviewed candidate through repository-normal controls with required checks/approvals current. | `review-integration.md` | `review-integration.md`; `authority-gates.md` | D, I, Z |
| `RELEASE-MODEL-DISCOVER` | Recover the repository's actual release/deployment model and target semantics before assuming release process or target behavior. | `release.md` | `release.md` | AH |
| `DELIVERY-PROOF` | Integration is not delivery; prove the intended artifact/config reached the required target and acceptance endpoint, then close only when material rollback/risk obligations are resolved or explicitly owned. | `release.md` | `release.md` | AB, AC |
| `INCIDENT-CONTAINMENT` | When current production state is wrong or unsafe, contain/restore safe service before normal backlog flow while preserving enough evidence for follow-up. | `release.md` | `release.md` | AI |
| `RECOVERY-AUTHORITATIVE` | Replacement Master recovers decision-relevant state from authoritative systems, not chat or a manager archive. | `continuity.md` | `continuity.md`; `governance.md` | V |
| `RECOVERY-PROPORTIONAL` | Full recovery/rotation is signal-driven and bounded; ordinary progress or long context alone does not create a project boundary. | `continuity.md` | `continuity.md` | AL |
| `LEAN-KNOWLEDGE` | Keep one natural owner per truth and persist only future-useful information not better recoverable elsewhere. | `governance.md` | `governance.md`; `continuity.md` | V, X |
| `REPOSITORY-READINESS` | Discover/reuse before create and bootstrap only structures that materially enable execution/recovery. | `governance.md` | `governance.md` | X |
| `UNKNOWN-WRITE` | Ambiguous mutation outcomes are reconciled before safe bounded retry; incomplete lookup is never absence. | `authority-gates.md` | `authority-gates.md` | J |
| `OPTIMISTIC-CONCURRENCY` | Refresh overwrite-sensitive identity and honor supported expected-version guards; reconcile drift instead of forcing. | `authority-gates.md` | `authority-gates.md` | K |
| `MATERIAL-DECISION` | Agent owns ordinary reversible technical choices; owner handles materially product/business/security/data/legal/cost/risk choices. | `authority-gates.md` | `authority-gates.md` | L |
| `SECURITY-REVIEW-BOUNDARY` | Independent read-only security review relies on safe existing evidence; missing assurance becomes a finding/limitation, not reviewer-created adversarial execution. | `independent-review.md` | `independent-review.md` | AA |
| `MACHINE-RELAY` | The relay block is one complete self-sufficient copy target; optional current-user explanation stays outside it and is never required by the destination. | `relay-transport.md` | `SKILL.md`; `relay-transport.md` | AD |
| `INTERFACE-COMPOSITION` | Consult interface specialist only for unresolved material UX judgment without transferring project/repository authority. | `interface-specialist.md` | `interface-specialist.md`; `engineering-quality.md` | AE |
| `USER-STOP` | Explicit user stop ends new consequential mutation without cleanup/sync ceremony unless requested. | `master-cycle.md` | `master-cycle.md` | M |
