# Continuity and Recovery

The project must survive loss of the current chat or Master. Recover from authoritative project systems; do not build a second manager-memory archive.

## 1. Persist only what cannot be recovered better elsewhere

Persist information when a future contributor needs it to decide or continue safely **and** it is not already clear from stronger Git/GitHub/CI/release evidence.

Good candidates:
- durable project constraints/decisions in their natural docs;
- unresolved dependencies/risks in the owning work item;
- minimum active Worker assignment identity before the first push/PR/handoff;
- non-obvious unfinished intent when code/PR/Issue evidence alone would be ambiguous.

Do not persist transient narration, repeated status summaries, tool history, or facts recoverable from commits/PRs/checks.

## 2. Recovery sequence

On replacement Master or contradictory/stale context:

1. resolve exact repository/target identity and current user/assignment authority;
2. locate the current accepted outcome and active work;
3. inspect only current Git/GitHub/CI/release evidence that can change the next decision;
4. identify blockers/dependencies/material risks and any active Worker assignment;
5. reject stale chat/handoff claims when fresher authoritative evidence conflicts;
6. choose the next valid action and continue.

Do not reread the whole repository or reconstruct the full historical plan unless current evidence makes that necessary.

A prior chat/summary is a locator, not authority.

## 3. Reconciliation

When sources disagree, first check whether they refer to the same repository, object, candidate/SHA, target, environment, and time. Preserve concurrent work; never overwrite newer authoritative state with an old handoff.

A closed Issue, old green CI, previous review, or old delivery claim does not prove current completion when its identity/criteria no longer match.

### Runtime recovery and reuse

Before cloning, creating a task worktree/environment/job/session, or repeating uncertain execution, discover relevant existing state through available authorized tools. Scope discovery to the repository/task and likely resources. A truncated, filtered, failed or unavailable lookup does not prove absence.

Verify what determines a safe match: canonical remote/repository; Issue/PR/assignment; branch and HEAD/lineage; dirty/conflict state and in-flight operations; owning task/principal where determinable; actual environment and active consumers. A familiar path, clean checkout or shared account alone proves neither freshness nor ownership.

Reuse a verified matching safe resource. For branch/task isolation, prefer a worktree over another full clone unless repository-level isolation or tooling requires one. Preserve unrelated or ambiguous state; use verified isolation when authorized, or report the exact blocker. Do not overwrite, reset, stash, stop another actor or duplicate uncertain work to make progress.

Exactly one Master is active per project outcome. A replacement chat is its sequential successor; other projects may have their own Masters on the same host. Workers, reviewers, jobs and services can survive chat rotation. Two connectors may reach the same host; neither a connector identity nor a working directory proves isolated filesystem, browser profile, port, service or database ownership. Respect existing coordination; add no global Master registry, election or cross-project lock.

For an uncertain operation, recover its stable identity and inspect existing state/output before deciding to resume, reconcile or retry. Apply [authority-gates.md](authority-gates.md) to any reconciliation effects and ambiguous mutation; do not repeat a non-idempotent action merely because the chat or connection was lost. Distinguish running/readiness observations from verified completion and exit evidence.

Keep verified locators while useful and refresh only facts invalidated by evidence or the next action. If a host is lost or unavailable, recover pushed GitHub truth and state exactly which ephemeral/unpushed work is unverified or unrecoverable. Persist a minimal runtime locator or retention reason in the owning work item only when needed for safe continuation and not recoverable better elsewhere.

## 4. Recoverability test

Before leaving materially unfinished work at a real boundary, a replacement Master should be able to determine from authoritative sources:

- what outcome is active;
- what remains;
- which repository/candidate/target is current;
- material dependencies/blockers/decisions;
- any active Worker assignment and necessary verified runtime locator/retention reason;
- required review/integration/release evidence;
- the next valid action or exact external resume condition.

If one non-obvious fact is missing, persist only that fact in the natural owner.

## 5. Rotation

Rotate chats/Masters only when useful; context length alone is not a project boundary. A rotation must not change authority, scope, risk, or accepted outcome.

A user-relayed new-Master prompt should be compact and use [relay-transport.md](relay-transport.md):

```text
Use github-project-orchestrator as MASTER.
Repository(s): <exact active repository(s)>
Mode: RECOVER, then continue the accepted outcome from current authoritative state.
Project authority: <ADVISORY | MANAGED | AUTONOMOUS_WITH_GATES>
Repository mutation scope: <exact authorized repositories>
Scoped approvals: <exact active grants or none>
Current locator: <active Issue/PR/milestone/release when useful>

Do not rely on this relay as live truth. Reconcile current repository/GitHub/CI/release evidence first, then continue until a real boundary.
```

Do not copy full project history into the rotation prompt.
