# Independent Review

Load only when an independent reviewer is required by repository policy, explicit instruction, or material risk/assurance. Master remains integration owner.

Prefer one independent review after the candidate is stable enough for acceptance. Do not use repeated reviewer cycles as an implementation loop.

## Dispatch

When relayed between agents/chats, apply [relay-transport.md](relay-transport.md).

Give the reviewer only what is needed to reproduce the review envelope:

```text
# INDEPENDENT REVIEW

Repository: <exact repository>
Integration Target/Base: <branch + current sha>
Candidate: <exact sha/PR>
Work item / acceptance: <identity or concise criteria>
Risk-specific concerns: <only material items>
Current validation evidence: <checks/CI tied to candidate>
Reviewer authority: READ_ONLY unless an exact additional action is explicitly authorized

Review the effective target-to-candidate change for acceptance, correctness, relevant quality/safety concerns, validation sufficiency, and integration readiness.
Do not modify the repository or invent missing evidence.
```

For security-sensitive read-only review, prefer authoritative source/diff, existing repository tests, current CI/log/artifact evidence, and safe read-only inspection. Do not generate or execute novel adversarial probes solely to demonstrate assurance; missing required evidence becomes a finding or explicit limitation.

For a remediation re-review, include the prior reviewed candidate and current candidate so the reviewer can focus on the exact delta and affected interactions rather than redoing unchanged analysis.

## Result

Return:

```text
# INDEPENDENT REVIEW RESULT

Completion: COMPLETE | INCOMPLETE
Verdict: APPROVE | CHANGES_REQUIRED | NO_VERDICT

Envelope:
- Repository:
- Integration Target/Base:
- Candidate:
- Work item/acceptance:

Findings:
- BLOCKER | REQUIRED | OPTIONAL — <evidence-backed finding>
  Evidence: <file/diff/check/current source>

Limitations:
- <none or exact missing evidence/access>
```

`APPROVE` is valid only when the exact current envelope was completely reviewed and no BLOCKER/REQUIRED finding remains. Missing access/evidence yields `INCOMPLETE / NO_VERDICT`, not an invented defect or approval.

## Master reconciliation

Master verifies candidate/target/acceptance identity, review completeness, and each finding against current authoritative evidence.

If the candidate changed after review, prior reasoning may be reused only where its assumptions remain valid; obtain a fresh verdict for the current candidate when independent approval is still required. Re-review the exact delta plus affected interactions, not unchanged surface without cause.

Formatting defects in a received result may be normalized only when the semantics/identity are unambiguous. Never normalize missing evidence into approval.
