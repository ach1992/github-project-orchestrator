# Governance and Repository Readiness

Load for first ownership, repository readiness, project structure, Issues/Projects/milestones, or when the management system itself is slowing delivery.

## First ownership

Resolve the project definition and exact repository target before substantial work. Reuse a suitable existing checkout/worktree; for branch/task isolation prefer `git worktree` over another full clone unless repository-level isolation/tooling requires one.

Apply the kernel Mutation rule to repository and management objects. Avoid duplicate repositories, Issues, labels, milestones, Projects, branches, and documents; incomplete search never proves absence.

When a repository must be created, apply [authority-gates.md](authority-gates.md), resolve material settings not already fixed by policy, create once, and verify the resulting identity.

## Canonical project specification

Keep one canonical repository copy of the project-defining specification when durable project-level intent is needed. Preserve purpose, success criteria, durable constraints/non-goals, supported-environment commitments, and completion criteria.

Reuse an established equivalent and location. If none exists and repository convention does not provide a stronger home, use `docs/PROJECT-SPEC.md`. Keep `README.md` as the concise entry/setup/navigation surface rather than a duplicate specification. Before persisting the spec, exclude secrets/credentials, prohibited sensitive data, and transient chat/runtime instructions; keep needed sensitive values in authorized secure/runtime sources. If sensitive material is already tracked, deletion alone is not remediation—handle rotation/history exposure through the applicable security gates.

Do not turn the root specification into a live status document. Routine status belongs in Git/GitHub/CI/release systems. Update the root specification only when project-level intent actually changes.

Use README/setup/architecture/runbook documentation for developer and operational knowledge rather than duplicating the project specification.

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

Use the smallest native structure that improves execution.

Persist a work item when it carries useful unresolved scope/acceptance, dependency, ownership, risk, delivery, or cross-session context. Routine bounded Master work can stay in the request plus branch/PR evidence.

Prefer one meaningful work item over a convoy of implementation-layer Issues; apply the kernel split criteria to work-item boundaries.

Projects/milestones are useful when they reduce coordination cost across multiple substantive items/releases. For multi-repository outcomes, keep one small global outcome/dependency/release spine while local Issues/PRs/CI remain authoritative in each repository; coordination never widens repository mutation scope. Do not mirror every local task into a central management artifact.

Keep labels sparse and operationally useful. Close an Issue only when its accepted completion criteria are actually satisfied; merge alone is not completion when post-integration or delivery evidence remains required.

## Project navigation

If authoritative knowledge is materially fragmented, add or improve one lightweight project map/index in the most natural durable location. If no established location exists, prefer a short `README.md` section; otherwise use `docs/project-map.md`. Point to where truth lives—specification, architecture, active work, decisions, release/runbook—rather than copying status.

Prefer native GitHub relationships/closing links for work-item, dependency, PR, and release traceability instead of mirroring live state in prose. Do not maintain a parallel manager-memory archive.

## Decisions and durable docs

Create an ADR/equivalent only when a lasting architectural/product/operational decision needs future rationale or constraints. Capture context, decision, important trade-offs/consequences, and status; do not use ADRs as meeting minutes.

Documentation earns its cost when it materially improves reproducibility, operation, review, or future maintenance. The absence of a generic document is not itself a defect.

When durable coding-agent instructions are needed and no established equivalent exists, prefer one root `AGENTS.md`; add nested files only for genuinely different subtree rules. Keep them to stable setup/commands/conventions/boundaries, never live backlog or handoff state.

## Engineering-system repair

Treat repeated management or CI friction as an engineering problem when evidence shows recurring cost. Examples include repeated duplicate discovery, repeated stale acceptance cycles caused by poor slicing, a long CI critical path, or navigation that repeatedly blocks recovery.

Fix the root mechanism with the smallest maintainable change. Do not create a recurring process-audit obligation.

When the evidenced bottleneck is CI/automation, use [engineering-quality.md](engineering-quality.md) for the optimization mechanism; governance only decides whether that repair earns current scope.

For complex local Git safety/identity inspection, `scripts/repo_preflight.py` is an optional deterministic helper; use it when its bounded read-only evidence is more reliable than ad-hoc shell inspection, not as mandatory ceremony.
