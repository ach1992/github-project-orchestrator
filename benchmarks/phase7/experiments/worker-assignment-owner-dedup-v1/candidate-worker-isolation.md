## 1. Isolation

One Worker = one Task Contract + one assigned branch at a time. Use a dedicated worktree when useful for isolation; its filesystem path is runtime location, never assignment identity.

[task-contract.md](task-contract.md) §8 owns the persisted Worker assignment/concurrency envelope. Before editing, read that current envelope and verify it rather than reconstructing its fields here:

1. repository/working directory and current worktree are the intended assigned branch and safe to modify;
2. every persisted assignment/envelope assumption is current, together with repository rules, required validation, and task risk/release constraints;
3. on initial dispatch before the first contracted edit, current assigned-branch/worktree HEAD equals immutable `Start HEAD`; normal authorized commits in the same valid generation may advance beyond it without staleness;
4. on same-generation correction/resume, current assigned-branch HEAD equals the Master-supplied `Checkpoint HEAD` before editing.

Any material identity/checkpoint mismatch -> `WorkerStatus.STALE_ASSIGNMENT`; never guess. Worker never upgrades `ProjectAuthority`, `ScopedAuthorization`, `CoordinationBaseline`, or `AssuranceLevel`, and never broadens assignment because Master is unavailable.
