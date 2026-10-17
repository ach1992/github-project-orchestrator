# Governance and Repository Readiness

Load for first ownership, repository readiness, project structure, documentation/Issue decisions, Projects/milestones, or evidenced management friction.

## First ownership

Resolve the project definition and exact repository target before substantial work. Recover and reuse suitable execution state through [continuity.md](continuity.md).

Apply the kernel Mutation rule to repository and management objects. Avoid duplicate repositories, Issues, labels, milestones, Projects, branches, and documents; incomplete search never proves absence.

When a repository must be created, apply [authority-gates.md](authority-gates.md), resolve material settings not already fixed by policy, create once, and verify the resulting identity.

## Canonical project specification

Keep one canonical repository source for durable project-level intent: purpose, Owner-approved vision, stable success criteria, constraints/non-goals, supported-environment commitments, and completion criteria.

Reuse an established equivalent and location. If none exists and repository convention does not provide a stronger home, use `docs/PROJECT-SPEC.md`. Before persisting project knowledge, exclude secrets/credentials, prohibited sensitive data, and transient chat/runtime instructions; keep needed sensitive values in authorized secure/runtime sources. If sensitive material is already tracked, deletion alone is not remediation—handle rotation/history exposure through the applicable security gates.

Keep release history, PR/Issue indexes, running checklists and chat/status narration out of the specification; their natural Git/GitHub/CI/release sources own them. Update the specification only when durable project-level intent changes, not merely because an implementation, release or chat ends.

## README and technical documentation

Keep `README.md` a truthful user/developer entrypoint: purpose, relevant setup/use, and navigation to authoritative details. Link the specification, technical references and native release/evidence sources rather than copying them or maintaining a management log.

Before creating or expanding documentation, identify its reader, the decision/action it supports, and necessary information missing from existing code, tests, GitHub evidence or docs. Reuse, edit or link sources that already answer the need. The absence of a generic document is not a defect.

Architecture, public contracts, runbooks, testing guides and API references earn their place through useful decisions, implementation, operation, diagnosis, recovery, review or reproducibility. Preserve useful long references and operational procedures; length alone is no reason to remove them. For model-facing instructions, preserve triggers, conditions, exceptions and actions; choose a sentence, paragraph, table, link or diagram by decision clarity and retrieval cost, not appearance or minimum word count.

| Situation | Action |
|---|---|
| Touched work changes enduring truth | Update the nearest authoritative location and affected links within the coherent change. |
| Existing content answers the need | Reuse, edit or link it; keep one definition at its natural owner. |
| Documents overlap or contradict | Reconcile at the current owner, transfer useful unique content and remove superseded repetition. |
| A document is obsolete | Preserve useful obligations, rationale, procedures, evidence and consumer links before removing it. |
| Only implementation status or transient evidence changed | Use the owning Git/PR/check/release record; do not create a parallel snapshot. |

Do not create documentation tasks or handoff archives solely because work occurred or a chat ends. Improve touched knowledge when it affects the work, without recurring audits or a separate cleanup project.

## Bootstrap only what execution needs

Inspect enough to determine whether:

- relevant setup is reproducible;
- repository instructions/conventions are discoverable;
- important build/test/quality/deployment commands are authoritative when applicable;
- current CI provides required gates;
- active work/dependency/release state is recoverable;
- durable architecture/operations rules live in a natural source.

Repair only gaps that materially affect execution, coordination, review, delivery, or recovery. Do not add Projects, templates, labels, ADRs, codeowners, agent instruction files, CI, or release automation merely because they are common.

Bootstrapping is complete once current work can proceed safely and a replacement contributor can recover the necessary state.

## Issues, Projects, milestones, and labels

Use the smallest native structure that improves execution. Find and reuse the existing work owner before creating another Issue.

A new work item must carry a meaningful unresolved outcome, acceptance, dependency, ownership, risk, decision, delivery, coordination or cross-session need that existing sources do not adequately preserve. Routine bounded Master work can stay in the request plus branch/PR evidence. Do not create an Issue for each file, test, phase or routine action.

Prefer one coherent work package; apply the kernel split criteria rather than implementation-layer boundaries. Use [task-contract.md](task-contract.md) only when its coordination value justifies it, not as a template for every Issue.

Keep the current contract easy to recover: accepted outcome, useful non-goals, outstanding acceptance, dependencies, unresolved Owner gates and evidence links. Replace superseded instructions instead of stacking dated reports. Keep unmet criteria and active decisions visible; preserve unique accepted obligations, completion evidence and important rationale in their natural current or historical sources.

When Issues overlap, reconcile unique criteria, dependencies, decisions and evidence at the existing canonical work owner and link the relationship. Consolidation neither proves completion nor authorizes dropping obligations.

Close only when accepted completion is proved or an explicitly authorized not-planned decision applies. Merge alone is not completion when post-integration or delivery evidence remains required. Separate completed component acceptance from pending program/release gates without dropping or duplicating obligations.

### Owner-parked ideas

An Owner-stated future idea or deferred-decision item stays recoverable and inactive. Open state, ready-looking labels, elapsed time or an empty executable queue does not authorize activation. Do not implement, close, delete or reclassify it without a new explicit Owner decision.

Use an existing meaningful `type:idea` label/convention when appropriate, but preserve the Owner gate even when labels are absent or misleading. A wording or organization edit must not change that decision. Accepted dependency-blocked work may become executable through its existing gates when the dependency is satisfied; an Owner-parked idea still needs the Owner decision.

### Coordination structures

Keep labels sparse and operationally useful. Use Projects/milestones when they reduce coordination cost across substantive items/releases. For multi-repository outcomes, keep one small global outcome/dependency/release spine while local Issues/PRs/CI remain authoritative in each repository; coordination never widens repository mutation scope. Do not mirror every local task into a central management artifact.

## Project navigation

If authoritative knowledge is materially fragmented, add or improve one lightweight project map/index in the most natural durable location. If no established location exists, prefer a short `README.md` section; otherwise use `docs/project-map.md`. Point to where truth lives—specification, architecture, active work, decisions, release/runbook—rather than copying status.

Prefer native GitHub relationships/closing links for work-item, dependency, PR, and release traceability instead of mirroring live state in prose. Do not maintain a parallel manager-memory archive.

## Durable decisions and agent instructions

Create an ADR/equivalent only when a lasting architectural/product/operational decision needs future rationale or constraints. Capture context, decision, important trade-offs/consequences, and status; do not use ADRs as meeting minutes.

When durable coding-agent instructions are needed and no established equivalent exists, prefer one root `AGENTS.md`; add nested files only for genuinely different subtree rules. Keep them to stable setup/commands/conventions/boundaries, never live backlog or handoff state.

## Engineering-system repair

Treat repeated management or CI friction as an engineering problem when evidence shows recurring cost. Examples include repeated duplicate discovery, repeated stale acceptance cycles caused by poor slicing, a long CI critical path, or navigation that repeatedly blocks recovery.

Fix the root mechanism with the smallest maintainable change. Do not create a recurring process-audit obligation.

When the evidenced bottleneck is CI/automation, use [engineering-quality.md](engineering-quality.md) for the optimization mechanism; governance only decides whether that repair earns current scope.

For complex local Git safety/identity inspection, `scripts/repo_preflight.py` is an optional deterministic helper; use it when its bounded read-only evidence is more reliable than ad-hoc shell inspection, not as mandatory ceremony.
