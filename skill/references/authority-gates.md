# Authority and Gates

Load when authority/effect is unclear or before integration, production, destructive/irreversible, access-boundary, or external-commitment actions. Gate the action being taken; future risky steps do not block safe preparation.

## 1. Authority and repository scope

Project authority may be:

- `ADVISORY`: read/analyze/recommend; no project mutation unless an exact action is separately authorized.
- `MANAGED`: perform reversible management/implementation implied by the accepted request; consequential integration/production actions still follow the gates below.
- `AUTONOMOUS_WITH_GATES`: execute end-to-end inside the accepted scope until a consequential gate or owner-level decision is reached.

A clear request to develop/manage a named repository authorizes its implied reversible work; do not ask for ceremonial confirmation. A one-off grant authorizes only that exact action/target/effect.

Repository mutation scope is an allowlist. Related repositories, dependencies, links, technical access, shared projects, or Worker delegation never make another repository writable. If writable scope is ambiguous, keep that repository read-only and ask only the exact scope question needed.

Repository/platform permissions and policy can always be stricter than this Skill.

## 2. Classify the actual effects

One action can have several simultaneous effects; satisfy every applicable obligation.

| Effect | Examples / default treatment |
|---|---|
| read-only | inspect/analyze; allowed |
| reversible management | Issue/label/milestone/doc/project updates with straightforward rollback |
| reversible implementation | isolated edit/test/commit/push or clearly non-production validation mutation with straightforward recovery |
| integration | update the accepted target branch/release line |
| production | deploy/publish/promote/enable production, including deterministic auto-deploy caused by another action |
| destructive/irreversible | difficult-to-recover deletion/overwrite/data/access-boundary change |
| external commitment | significant cost or legal/compliance/business/public/vendor commitment |

For reversible management/implementation, proceed when accepted authority implies the action. High-consequence code may still be prepared safely before a later integration/release approval.

Integration:
- low/ordinary impact: proceed when integration authority is clear, repository policy passes, and all current acceptance/review gates pass;
- high-consequence integration under the anchors in section 4: require human approval unless the exact integration action was validly pre-authorized.

Production requires human approval unless the exact rollout was validly pre-authorized and remains current.

Destructive/irreversible and external-commitment actions require the applicable human decision/approval. A current explicit instruction directing that exact action may satisfy the gate when target/effect remain unchanged.

Never let approval for one effect waive another simultaneous effect. Example: approval to deploy does not authorize an irreversible data operation hidden inside the same action.

## 3. Execute only when all applicable conditions hold

Before a consequential mutation, confirm only what matters:

- accepted scope allows it;
- every repository it will mutate is authorized;
- current role allows it;
- project/repository/platform policy allows it;
- actual/deterministic effects are understood;
- required approvals or exact scoped authorizations are current;
- required capability exists;
- mutable identity that could be overwritten/integrated/deployed is fresh enough.

If capability appears missing, inspect current tools/connectors/actions, prefer the authoritative native route, then try reasonable supported equivalents. Declare it unavailable only after those routes are ruled out. Reconcile other uncertainty directly.

## 4. Owner decisions and high-consequence anchors

Master makes ordinary reversible technical choices: naming, local refactor shape, test structure, bounded module organization, error handling, and repository-consistent implementation strategy.

Treat an unresolved choice as owner-level when it changes one of these anchors:

- accepted product behavior or business policy;
- a durable public/compatibility contract, such as a public API or protocol;
- security, privacy, or access posture, including authentication/authorization;
- destructive/stateful migration, data-loss, or recovery semantics;
- production, release, or infrastructure rollout/rollback posture;
- significant cost/vendor commitment, legal/compliance posture, or explicit risk acceptance.

These anchors are not exhaustive. Reversible choices inside accepted behavior stay with Master. Integration is high-consequence when it can change an anchor's posture or blast radius.

When asking, present the smallest decision with relevant trade-off, evidence, risk, and rollback/roll-forward.

## 5. Ambiguous write outcome

When a non-idempotent mutation returns an ambiguous transport/API result:

1. do not blindly retry;
2. re-read the authoritative object using stable identity/semantic equivalence;
3. if the intended write is present, verify and continue;
4. if a sufficiently complete lookup proves absence, retry at most once only when the write is safely idempotent/deduplicated;
5. if lookup is incomplete or absence is not proven, freeze only dependent mutation and continue independent work;
6. stop only when the unresolved write is the controlling blocker and report the exact object/action/evidence needed.

Apply this to Issue/PR creation, comments, pushes, releases, deployment triggers, and similar writes.

## 6. Optimistic concurrency

Before overwrite-sensitive/integration/release writes, refresh the identity/revision that protects against stale overwrite. Use an enforced expected SHA/revision precondition when the available API genuinely supports it.

If state drifted or a precondition rejects the write, inspect the delta, preserve concurrent work, recompute the intended mutation, and act only if still correct. Never remove the guard just to force the write.

Absence of an atomic precondition is not a reason to invent one or create a new approval ceremony; use read/reconcile/verify and narrow the write where possible.
