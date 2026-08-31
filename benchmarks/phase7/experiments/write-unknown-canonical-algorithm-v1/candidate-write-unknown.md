## 6. `WriteState.UNKNOWN`

For ambiguous mutation transport/API results, use one guarded recovery algorithm:

1. Mark only the individual mutation `WriteState.UNKNOWN`; do not blindly retry and do not automatically stop the Master.
2. Re-read the authoritative remote object/list using stable identity or semantic equivalence, with enough decision-scoped completeness to distinguish **present**, **proven absent**, and **incomplete/unknown**.
3. If the equivalent write is **present**, verify it, mark the action `WriteState.KNOWN`, and continue.
4. If the re-read **proves absence**, retry at most once and only when the retry is safely idempotent or protected by stable correlation/deduplication identity. If retry is not safe, freeze the dependent mutation and continue independent safe work.
5. If the re-read is **incomplete/truncated/unknown**, never treat that as absence and never use it to authorize a retry; freeze the dependent mutation and continue independent safe work.
6. After the one safe retry—or when no safe retry exists—if outcome remains ambiguous, keep that mutation at `WriteState.UNKNOWN`, continue independent safe work, and surface `MasterBoundary.WRITE_OUTCOME_UNKNOWN` only when it becomes the sole/project-wide controlling blocker.

Apply to Issue/PR creation, comments, labels, Project updates, pushes, releases, deployment triggers, and other non-idempotent writes.
