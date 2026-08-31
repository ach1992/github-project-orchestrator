For already-running CI/check/deployment/job, `pending` is dependency state, not failure. Continue independent useful work first; when the pending dependency becomes the only remaining dependency, prefer a real runtime-supported continuation mechanism over yielding control.

| Current condition | Required action |
|---|---|
| independent useful work still exists | Continue it before waiting. |
| pending is the sole dependency and bounded synchronous waiting is safe/proportionate | Use non-tight authoritative rechecks only when a transition is plausibly due; bound continuation by expected job duration, tool/runtime limits, and diminishing value. |
| pending is the sole dependency and a suitable real event/condition resume primitive exists | Use that primitive rather than fabricating monitoring/resume. |
| dependency resolves successfully | Immediately continue the existing workflow; do not require a user nudge. |
| dependency fails | Stop waiting immediately, classify the failure, and continue the applicable remediation or independent-work path. |
| dependency is still pending, is the sole remaining blocker, and autonomous continuation is unavailable, no longer reasonable, or exhausted | Use `MasterBoundary.BLOCKED` with the exact external object, current status, why autonomous continuation cannot safely continue, exact resume condition, and recoverable state. |

Never tight-poll, sleep indefinitely, fabricate background monitoring/resume, or manufacture work. `DeliveryState.PENDING` remains a lifecycle state, not a terminal boundary label; never use `MasterBoundary.NO_READY_WORK` merely because an already-running required dependency is unfinished.
