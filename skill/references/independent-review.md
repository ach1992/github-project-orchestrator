# Independent Review

An assigned Independent Reviewer inspects the review envelope with read-only authority unless expressly granted a specific additional action. Master owns dispatch, reconciliation, and integration. User-mediated dispatch or result is a MachineRelay.

Use the [Review standard](review-integration.md#2-review-standard) to classify findings and proposed remedies.

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
Return the Result contract at <receiver-accessible URL or installed-Skill reference to this revision's independent-review.md#result, or the inline contract supplied here>.
```

If the receiver cannot resolve the Result contract or its dependencies, include its fields, verdict rules, the [Review standard](review-integration.md#2-review-standard)'s finding classifications and evidence standard, and copy-block requirements inside the dispatch. For security-sensitive review, prefer authoritative source/diff, existing tests, current CI/log/artifact evidence, and safe read-only inspection. Do not generate or execute novel adversarial probes solely to demonstrate assurance.

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

Choose the result for this exact envelope:

| Review outcome | Completion / Verdict |
|---|---|
| Essential evidence or access is missing | `INCOMPLETE / NO_VERDICT` |
| Review complete with a confirmed BLOCKER or REQUIRED finding | `COMPLETE / CHANGES_REQUIRED` |
| Review complete with no BLOCKER or REQUIRED finding | `COMPLETE / APPROVE` |

Retain every confirmed finding even in an incomplete review. Identify what remains unverified under Limitations. Give each mandatory finding a concrete repair and verification path. Write `None.` when there are no findings.

## Master reconciliation

Master verifies candidate/target/acceptance identity, review completeness, and each finding against current authoritative evidence. Challenge an unsupported mandatory finding against the Review standard and seek a corrected independent result through the existing review process. Do not grow scope merely to satisfy a recommendation, silently self-approve, or bypass an unresolved review gate.

If the candidate changed after review, prior reasoning may be reused only where its assumptions remain valid; obtain a fresh verdict for the current candidate when independent approval is still required. Re-review the exact delta plus affected interactions, not unchanged surface without cause.

Formatting defects in a received result may be normalized only when the semantics/identity are unambiguous. Never normalize missing evidence into approval.
