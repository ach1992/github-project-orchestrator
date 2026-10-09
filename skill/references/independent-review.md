# Independent Review

Load only when independent review is required by repository policy, explicit instruction/assurance requirement, or high-consequence risk. Master remains integration owner. User-mediated review dispatch or result is a MachineRelay.

Prefer one independent review after the candidate is stable enough for acceptance. Do not use repeated reviewer cycles as an implementation loop. If direct reviewer tooling is unavailable but a fresh independent chat/model/human is usable, emit the complete review relay for that context; lack of a platform reviewer identity alone is not a blocker unless policy requires one.

## Dispatch

Give the reviewer only what is needed to reproduce the review envelope:

```text
# INDEPENDENT REVIEW

Repository: <exact repository>
Integration Target/Base: <branch + current sha>
Candidate: <exact sha> (PR <url/number if applicable>)
Work item / acceptance: <identity + current revision when persisted, or concise criteria>
Risk-specific concerns: <only material items>
Current validation evidence: <checks/CI tied to candidate>
Reviewer authority: READ_ONLY unless an exact additional action is explicitly authorized

Review the effective target-to-candidate change for acceptance, correctness, relevant quality/safety concerns, validation sufficiency, and integration readiness.
Do not modify the repository or invent missing evidence.
```

For security-sensitive read-only review, prefer authoritative source/diff, existing repository tests, current CI/log/artifact evidence, and safe read-only inspection. Do not generate or execute novel adversarial probes solely to demonstrate assurance; missing required evidence becomes a finding or explicit limitation.

For a remediation re-review, include the prior reviewed candidate and current candidate so the reviewer can focus on the exact delta and affected interactions rather than redoing unchanged analysis.

## Result

Emit `INDEPENDENT REVIEW RESULT` as a MachineRelay; load [relay-transport.md](relay-transport.md) before rendering:

```text
# INDEPENDENT REVIEW RESULT

Completion: COMPLETE | INCOMPLETE
Verdict: APPROVE | CHANGES_REQUIRED | NO_VERDICT

Envelope:
- Repository:
- Integration Target/Base:
- Candidate:
- Pull Request: <url/number or none>
- Work item/acceptance: <identity + current revision when persisted, or concise criteria>

Findings:
- BLOCKER | REQUIRED | OPTIONAL — <evidence-backed finding>
  Evidence: <file/diff/check/current source>
  Impact: <why it matters>
  Action: <smallest required fix, or optional recommendation>
  Verification: <how resolution can be proved>

Residual risk:
- <none or material residual risk not already represented by a finding>

Limitations:
- <none or exact missing evidence/access>
```

`APPROVE` is valid only when the exact current envelope was completely reviewed and no BLOCKER/REQUIRED finding remains. Missing access/evidence yields `INCOMPLETE / NO_VERDICT`, not an invented defect or approval. Write `None.` when no finding exists; BLOCKER/REQUIRED findings must provide a concrete repair and verification path.

## Master reconciliation

Master verifies candidate/target/acceptance identity, review completeness, and each finding against current authoritative evidence.

If the candidate changed after review, prior reasoning may be reused only where its assumptions remain valid; obtain a fresh verdict for the current candidate when independent approval is still required. Re-review the exact delta plus affected interactions, not unchanged surface without cause.

Formatting defects in a received result may be normalized only when the semantics/identity are unambiguous. Never normalize missing evidence into approval.
