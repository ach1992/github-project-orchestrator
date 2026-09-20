# Independent Review Protocol

Load only for required independent-review dispatch/result/reconciliation. `review-integration.md` owns the separation trigger, ordinary review/freshness/findings/integration; `relay-transport.md` owns transport. This file owns only the handoff/result protocol and creates no lifecycle state.

## 1. Independence boundary

Independent review means **separation from the authoring review context**, not GitHub identity. A fresh chat/model instance, review agent/tool, or human qualifies when given bounded current evidence and reviewing independently. Platform-native reviewer identity is required only by repository/platform policy or an applicable canonical gate. Lack of an external GitHub reviewer alone is not `MISSING_CAPABILITY` when a fresh independent context can be relayed.

## 2. Review handoff

Keep the handoff bounded and evidence-addressable. Include at minimum:

- repository + PR/change identity;
- exact target/base identity + exact candidate HEAD SHA;
- accepted outcome/acceptance + current Contract Revision when present;
- RiskLevel + CoordinationBaseline/AssuranceLevel + reason independent review is required;
- exact review boundary + material architecture/security/data/performance/operational constraints;
- current validation/CI evidence identifiers tied to the reviewed change; for remediation re-review, also identify the prior reviewed candidate and exact delta to the current candidate so unchanged reviewed surface can be reused only when its assumptions remain valid;
- reviewer authority, read-only by default unless another bounded action is explicitly authorized;
- for security-sensitive work, the exact evidence-backed defensive purpose/scope and allowed/prohibited action boundary from `engineering-quality.md` without inventing authorization or implying that authorization overrides provider/platform policy; for independent/read-only review also carry the reviewer evidence-acquisition boundary: prefer authoritative source/diff, repository-owned existing tests, current CI/log/artifact evidence, and safe read-only inspection; do not request novel adversarial payload/probe generation or execution merely to prove robustness; missing required evidence becomes a finding or explicit review limitation rather than a reviewer-created probe;
- expected findings as `BLOCKER`, `REQUIRED`, or `OPTIONAL`, each tied to concrete evidence.

If direct reviewer tooling is unavailable but a fresh independent chat/model/human is usable, emit one `INDEPENDENT REVIEW CHAT` MachineRelay and return its result to Master. Lack of a GitHub reviewer username alone is not a blocker.

## 3. Result contract

An emitted `INDEPENDENT REVIEW RESULT` is a MachineRelay; before rendering it, load `relay-transport.md` and require `MACHINE_RELAY_OUTPUT_OK(response)`. The reviewer returns exactly this result contract. `Review Completion` and `Verdict` are transport/result fields, not orchestration lifecycle states:

```text
# INDEPENDENT REVIEW RESULT

Review Completion: COMPLETE | INCOMPLETE
Verdict: APPROVE | CHANGES_REQUIRED | NOT_ISSUED

## Review Envelope

- Repository: <owner/repository>
- Integration Target: <branch@sha>
- Candidate: <exact sha>
- Pull Request: <number/url or none>
- Contract Revision: <number or not applicable>
- Risk Level: <LOW | MEDIUM | HIGH | CRITICAL>
- Coordination Baseline: <LIGHTWEIGHT | STANDARD>
- Assurance Level: <NORMAL | HIGH_ASSURANCE>

## Evidence Reviewed

- <authoritative evidence inspected>

## Findings

### <BLOCKER | REQUIRED | OPTIONAL> F-001 — <finding title>

- Location: <path/lines/symbol/object>
- Evidence: <concrete current evidence>
- Impact: <why this matters>
- Action: <smallest required remediation for BLOCKER/REQUIRED; optional recommendation for OPTIONAL>
- Verification: <how Master can prove resolution for BLOCKER/REQUIRED; for OPTIONAL use not applicable only when verification is not meaningful>

## Residual Risks and Uncertainty

- <none or bounded residual risk/uncertainty>

## Scope or Policy Limitations

- <none or exact unreviewed/restricted surface and effect on completeness>
```

Use only these completion/verdict pairs:

| Review Completion | Verdict | Meaning |
|---|---|---|
| `COMPLETE` | `APPROVE` | the exact current review envelope was completely reviewed and no `BLOCKER` or `REQUIRED` finding remains |
| `COMPLETE` | `CHANGES_REQUIRED` | the exact current review envelope was completely reviewed and the candidate/evidence itself has at least one evidence-backed `BLOCKER` or `REQUIRED` deficiency |
| `INCOMPLETE` | `NOT_ISSUED` | a reviewer/tool/policy/evidence-access limitation prevented the required review from being completed |

`INCOMPLETE / NOT_ISSUED` may still report supported findings from inspected surfaces; they remain actionable but create no overall verdict. Reviewer inability to inspect evidence is neither candidate defect nor approval.

- when no finding exists, write `None.` under Findings rather than omitting the section; order actual findings `BLOCKER`, `REQUIRED`, then `OPTIONAL`;
- a candidate that fails to supply evidence required by acceptance may receive `COMPLETE / CHANGES_REQUIRED` when the required review itself is complete; evidence that exists but was unavailable only to this reviewer yields `INCOMPLETE / NOT_ISSUED`;
- security-sensitive results may describe defensive location, evidence, impact, remediation/recommendation, and verification while following `engineering-quality.md` redaction/minimization boundaries; a restricted detail does not justify suppressing otherwise safe useful findings.

## 4. Master reconciliation

Master verifies candidate/target/contract identity, effective-change freshness, result completeness, and every finding. Formatting defects in a received external review result do not manufacture a code finding: normalize safely recoverable formatting only for reconciliation, never missing identity/evidence into approval. Receive-side normalization never authorizes malformed relay emission.

Do not create a permanent reviewer role/state. Master retains evidence/finding reconciliation, required fixes/approvals, and integration.
