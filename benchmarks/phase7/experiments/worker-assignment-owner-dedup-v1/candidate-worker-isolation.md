## 1. Isolation

One Worker = one Task Contract + one assigned branch at a time. Use a dedicated worktree when useful; its path is runtime location, never assignment identity.

[task-contract.md](task-contract.md) §8 owns the persisted Worker assignment/concurrency envelope. Before editing:

1. verify repository/working directory, assigned branch/worktree safety, repository rules, required validation, and task risk/release constraints;
2. verify the current persisted assignment envelope from §8;
3. on initial dispatch before the first contracted edit, require current assigned-branch/worktree HEAD = immutable `Start HEAD`; later authorized same-generation commits may advance beyond it without staleness;
4. on same-generation correction/resume, require current assigned-branch HEAD = Master-supplied `Checkpoint HEAD` before editing.

Any material identity/checkpoint mismatch -> `WorkerStatus.STALE_ASSIGNMENT`; never guess. Worker never upgrades `ProjectAuthority`, `ScopedAuthorization`, `CoordinationBaseline`, or `AssuranceLevel`, and never broadens assignment because Master is unavailable.
