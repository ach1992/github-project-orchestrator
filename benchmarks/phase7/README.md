# Phase 7 Operational Benchmark

This directory preserves repeatable operational evaluation of the `v1.1.0` refactor against the immutable `v1.0.0` baseline. The refactored-runtime traces are historical evidence pinned to immutable release commit `53182d5db086eef98ebaba757bb820b86e465845` (`v1.1.0-rc.1`) after verifying that its complete `skill/` tree is byte-identical to the former intermediate runtime pin. This keeps the original benchmark provenance reachable after feature-branch cleanup without changing the recorded trace behavior.

Phase 8 completed independent review and verified delivery of `v1.1.0-rc.1`. These traces intentionally do not float with later candidates. A later candidate that changes runtime policy—including the `v1.1.1` continuation maintenance—is not evaluated by these eight historical traces unless they are explicitly regenerated/re-pinned for that candidate. For `v1.1.1`, continuation semantics are specified by regression scenarios `AQ` and `CO`; candidate readiness relies on exact-head validation plus fresh source/diff and independent review. Phase 7 remains historical refactor evidence and must not be cited as execution evidence for the new continuation policy.

## Current lossless representation-optimization lane

Issue #35 reuses this Phase 7 benchmark system for a different comparison: immutable current baseline `v1.2.2` at `f98e8a242c720931e34aa7c4e8a799090e3d0495` versus a later candidate that changes **representation only**.

This lane does not rewrite the historical `v1.0.0 -> v1.1.0` evidence above. It adds:

- `runtime-optimization-baseline.json` — exact baseline identity and the mechanical semantic surfaces/predicate owners checked by `tools/check_runtime_equivalence.py`;
- `traces-v1.2.2.json` — source-grounded v1.2.2 policy-simulation traces for the existing eight Phase 7 scenarios;
- `runtime-optimization-scenarios.json` — the single semantic owner for the representation-comparison classes, protected behavior, eval anchors, exact model-trial inputs, and diagnostic measurements;
- `MODEL-TRIAL-PROTOCOL.md` — the observable paired actual-model/runtime A/B protocol that is the only benchmark lane eligible to prove practical representation improvement;
- `model-trial-cases.json` — the non-semantic scoring/selection manifest that references `runtime-optimization-scenarios.json` and selects the same canonical case IDs without duplicating their meaning;
- `tools/run_model_trials.py` — the auditable dry-run/live OpenAI-compatible paired execution and raw-evidence layer; it never self-scores semantic correctness;
- `tools/score_model_trials.py` — the deterministic scorer for explicitly annotated paired observable A/B records;
- `../../tests/test_runtime_equivalence.py`, `../../tests/test_run_model_trials.py`, and `../../tests/test_model_trial_scorer.py` — adversarial fixtures for the mechanical, executable-evidence, and scored-evidence gates.

### Evidence roles are intentionally separate

`tools/score_phase7_benchmark.py --comparison-mode candidate` compares two full-SHA-pinned **source-grounded policy simulations**. In the representation-optimization program this mode checks protected behavior and reports diagnostic friction/context deltas only. It always reports `optimization_claim_eligible: false`. An identical baseline/candidate trace can therefore be valid, and a manually shortened candidate trace can be diagnostically smaller, without either result proving that an LLM is faster, more accurate, or less error-prone.

Practical improvement may be accepted only from the separate paired actual-model/runtime A/B lane described in `MODEL-TRIAL-PROTOCOL.md`. That lane keeps model/runtime/settings/toolset identity fixed, alternates which representation runs first across pairs, scores only observable behavior, requires auditable transcript/tool-log references, hard-fails protected regressions, and requires a material paired improvement. It never requests or scores private chain-of-thought.

`tools/run_model_trials.py` is intentionally below that scoring boundary: it validates and freezes pair construction, exact candidate/baseline identities, runtime/settings/toolset identity, input fingerprints and balanced order; it then captures only audit-safe observable execution evidence. Its scorer-shaped annotation template contains `null` observed judgments and cannot pass `score_model_trials.py` until a reviewer explicitly annotates the raw evidence.

The mechanical equivalence checker likewise proves only objective representation invariants; semantic prose/judgment equivalence remains a review/evaluation responsibility.

## Historical source-grounded benchmark measures

The historical benchmark uses eight representative project traces covering small, medium, large/multi-repository, cold recovery, bounded delegation, review drift, production release, and local-blocker flow. Each scenario declares observable required behavior, proportional coordination, permitted human confirmation/artifact counts, delivery requirements, and the expected terminal boundary.

`tools/score_phase7_benchmark.py` scores source-grounded traces for:

- protected-behavior violations;
- steps before the first useful engineering action;
- unnecessary human confirmations;
- unnecessary project artifacts;
- Worker dispatch churn;
- repeated discovery/recovery;
- activated rule/reference domains;
- discovery/recovery steps;
- fresh review identity before integration;
- required delivery verification;
- correct Master stop behavior;
- operational coverage of every canonical Goal ID `G01` through `G16`.

The scorer treats unsafe shortcuts, hidden human work, stale integration, missing delivery verification, wrong stop boundaries, overweight coordination, and missing required controls as failures. It never gives safety credit in exchange for lower friction.

## Evidence types and limitations

### Source-grounded policy simulation

The source-grounded traces are produced by applying pinned runtime instructions to fixed scenarios and recording the prescribed/selected execution path. They are reproducible and auditable against cited runtime paths, but they are not independent model trials and do not measure actual model comprehension, routing reliability, latency, or execution quality.

The scorer rejects floating/malformed provenance and, when run with `--repo-root`, verifies every declared `ref:path` directly from Git. This prevents later `main` drift from silently changing evidence. For representation candidates, trace friction differences are diagnostics only and cannot satisfy the program's practical-improvement requirement.

Historical Phase 7 legitimately uses its source-grounded traces to document the prescribed operational effects of the v1.1.0 refactor. That historical result is preserved as historical evidence and is not retroactively reinterpreted as actual model-performance proof.

### Actual model/runtime paired A/B evidence

`MODEL-TRIAL-PROTOCOL.md` defines the evidence needed for a current representation-optimization claim. Each paired run compares the exact immutable v1.2.2 representation and one exact candidate on the same case under equivalent runtime identity/settings/tool availability. Only observable run behavior is scored.

`runtime-optimization-scenarios.json` remains the semantic owner for those cases and for the exact `trial_input` delivered to both sides of each pair. `model-trial-cases.json` only selects their IDs and defines scoring parameters such as minimum pair count, primary metrics, and sign-test alpha; CI requires both manifests to remain aligned.

Primary metrics are:

- protected-behavior violation count;
- wrong next-action decision count;
- observable steps before first useful action;
- composite avoidable events: unnecessary questions + unnecessary actions + unnecessary reference loads + manual-continue events.

The default contract requires at least three pairs per case, balanced baseline-first/candidate-first order within each case, zero candidate protected violations, no per-case worsening on a primary metric, and at least one directional paired improvement meeting the configured exact one-sided sign-test threshold. Passing the scorer still requires evidence review of transcript authenticity, trial construction, model/runtime identity, and operational significance before migration.

Optional token/latency measurements may be kept in a separate diagnostic artifact when measured comparably; the scored trial JSON intentionally has a closed observable schema and does not accept them. Token/word/line reduction cannot compensate for a correctness/safety regression and cannot establish an optimization win by itself.

## Files

- `scenarios.json` — fixed historical Phase 7 scenario contract and Goal coverage.
- `traces-v1.0.0.json` — historical baseline source-grounded traces pinned to `v1.0.0`.
- `traces-current.json` — historical refactored source-grounded traces pinned to immutable prerelease commit `53182d5db086eef98ebaba757bb820b86e465845`; the filename is phase-relative and does not mean the traces follow later release candidates.
- `runtime-optimization-baseline.json` — immutable v1.2.2 representation-comparison baseline configuration.
- `traces-v1.2.2.json` — immutable v1.2.2 source-grounded policy-simulation baseline for representation candidates.
- `runtime-optimization-scenarios.json` — canonical representation-comparison semantic/input/diagnostic case contract.
- `MODEL-TRIAL-PROTOCOL.md` — actual model/runtime A/B evidence protocol and executable runner boundary.
- `model-trial-cases.json` — scoring/selection manifest referencing the canonical semantic case contract; not a second semantic owner.
- `RESULTS.md` — checked-in historical Phase 7 interpretation and acceptance result.
- `LIVE-EVIDENCE.md` — real GitHub delivery evidence from integrated refactor phases.
- `../../tests/test_phase7_benchmark.py` — adversarial fixtures for historical and source-grounded representation-comparison behavior.
- `../../tests/test_runtime_equivalence.py` — adversarial fixtures for the immutable runtime-equivalence gate and semantic-case manifest alignment.
- `../../tests/test_run_model_trials.py` — mocked transport/identity/order/secret/fail-closed fixtures for the executable trial lane.
- `../../tests/test_model_trial_scorer.py` — adversarial fixtures for observable paired model/runtime evidence scoring.

## Run

Historical benchmark:

```bash
python3 tools/score_phase7_benchmark.py \
  --scenarios benchmarks/phase7/scenarios.json \
  --baseline benchmarks/phase7/traces-v1.0.0.json \
  --current benchmarks/phase7/traces-current.json \
  --repo-root . \
  --baseline-ref v1.0.0
```

Validate the immutable v1.2.2 representation baseline without claiming an improvement:

```bash
python3 tools/score_phase7_benchmark.py \
  --comparison-mode validate-baseline \
  --scenarios benchmarks/phase7/scenarios.json \
  --baseline benchmarks/phase7/traces-v1.2.2.json \
  --repo-root .

python3 tools/check_runtime_equivalence.py --repo-root .
```

Compare a future candidate source-grounded trace set for protected behavior and diagnostics only:

```bash
python3 tools/score_phase7_benchmark.py \
  --comparison-mode candidate \
  --scenarios benchmarks/phase7/scenarios.json \
  --baseline benchmarks/phase7/traces-v1.2.2.json \
  --current <candidate-traces.json> \
  --repo-root .
```

Render the frozen first-screening execution plan without network access or a credential:

```bash
python3 tools/run_model_trials.py \
  --candidate-ref 9384b371264473b291fe815b5725ae64f44d4179 \
  --dry-run
```

After a complete live run and explicit observable annotation, score the annotated paired evidence:

```bash
python3 tools/score_model_trials.py \
  --cases benchmarks/phase7/model-trial-cases.json \
  --trials <annotated-model-trials.json>
```

Run adversarial fixtures:

```bash
python3 tests/test_phase7_benchmark.py
python3 tests/test_runtime_equivalence.py
python3 tests/test_run_model_trials.py
python3 tests/test_model_trial_scorer.py
```

A historical passing score still requires zero protected-behavior violations in both historical trace sets, full `G01`-`G16` scenario coverage, correct proportional coordination, and the historical friction result. A current representation candidate must preserve the immutable v1.2.2 semantic/protected-behavior gate **and separately pass actual comparable model/runtime A/B evidence before any practical optimization claim or migration is accepted**.
