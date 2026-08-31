# Phase 7 Operational Benchmark

This directory preserves repeatable operational evaluation of the `v1.1.0` refactor against the immutable `v1.0.0` baseline. The refactored-runtime traces are historical evidence pinned to immutable release commit `53182d5db086eef98ebaba757bb820b86e465845` (`v1.1.0-rc.1`) after verifying that its complete `skill/` tree is byte-identical to the former intermediate runtime pin. This keeps the original benchmark provenance reachable after feature-branch cleanup without changing the recorded trace behavior.

Phase 8 completed independent review and verified delivery of `v1.1.0-rc.1`. These traces intentionally do not float with later candidates. A later candidate that changes runtime policy—including the `v1.1.1` continuation maintenance—is not evaluated by these eight historical traces unless they are explicitly regenerated/re-pinned for that candidate. For `v1.1.1`, continuation semantics are specified by regression scenarios `AQ` and `CO`; candidate readiness relies on exact-head validation plus fresh source/diff and independent review. Phase 7 remains historical refactor evidence and must not be cited as execution evidence for the new continuation policy.

## Current lossless representation-optimization lane

Issue #35 reuses this Phase 7 benchmark system for a different comparison: immutable current baseline `v1.2.2` at `f98e8a242c720931e34aa7c4e8a799090e3d0495` versus a later candidate that changes **representation only**.

This lane does not rewrite the historical `v1.0.0 -> v1.1.0` evidence above. It adds:

- `runtime-optimization-baseline.json` — exact baseline identity and the mechanical semantic surfaces/predicate owners checked by `tools/check_runtime_equivalence.py`;
- `traces-v1.2.2.json` — source-grounded v1.2.2 policy-simulation traces for the existing eight Phase 7 scenarios;
- `runtime-optimization-scenarios.json` — the minimum comparison classes for Phase B, including the hot FAST path, consequential authority path, Worker resume, cold recovery, review freshness, pending dependency continuation, integration/delivery separation, and namespace/effect isolation;
- `../../tests/test_runtime_equivalence.py` — adversarial fixtures proving that Rule/owner/Goal/state/router/eval/predicate loss is rejected.

`tools/score_phase7_benchmark.py --comparison-mode candidate` compares two full-SHA-pinned source-grounded trace sets. Candidate acceptance is stricter than simple equivalence: protected behavior must stay clean, every measured friction field must be non-worse, and at least one material source-grounded decision-cost field must improve. An identical baseline/candidate pair is deliberately **not** an optimization win.

The source-grounded lane still does **not** prove actual LLM latency, comprehension quality, or cross-model reliability. Phase B must add comparable model/runtime trial evidence before a representation change is selected for migration. The mechanical equivalence checker likewise proves only objective representation invariants; semantic prose/judgment equivalence remains a review/evaluation responsibility.

## What this benchmark measures

The benchmark uses eight representative project traces covering small, medium, large/multi-repository, cold recovery, bounded delegation, review drift, production release, and local-blocker flow. Each scenario declares observable required behavior, proportional coordination, permitted human confirmation/artifact counts, delivery requirements, and the expected terminal boundary.

`tools/score_phase7_benchmark.py` scores both baseline and current traces for:

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

## Evidence types and limitation

The A/B traces in this phase are **source-grounded policy simulations**. They are produced by applying the pinned runtime instructions to fixed scenarios and recording the prescribed/selected execution path. They are reproducible and auditable against the cited runtime paths, but they are not independent multi-model trials and do not measure wall-clock model latency.

The scorer rejects floating/malformed provenance and, when run with `--repo-root`, verifies every declared `ref:path` directly from Git. This prevents later `main` drift from silently changing the historical Phase 7 evidence. Pinning to a reachable immutable release commit also prevents ordinary branch cleanup from making valid historical provenance unreadable in CI.

That limitation is deliberate and visible. Phase 7 uses these traces to prove that the refactored policy surface can preserve protected behavior while reducing prescribed operational work. `LIVE-EVIDENCE.md` separately records real repository delivery evidence. Regression scenario `BC` in `skill/references/eval-scenarios.md` covers the independent-review handoff semantics; Phase 8 then exercised independent review on a real release candidate rather than treating the synthetic scenario as sufficient evidence by itself.

Token/word/line size is diagnostic only. The scorer reports pinned baseline/current `SKILL.md` entrypoint size from Git when run with `--repo-root`, but entrypoint shrinkage cannot compensate for a protected-behavior regression.

## Files

- `scenarios.json` — fixed scenario contract and Goal coverage.
- `traces-v1.0.0.json` — baseline source-grounded traces pinned to `v1.0.0`.
- `traces-current.json` — historical refactored source-grounded traces pinned to immutable prerelease commit `53182d5db086eef98ebaba757bb820b86e465845`; the filename is phase-relative and does not mean the traces follow later release candidates.
- `runtime-optimization-baseline.json` — immutable v1.2.2 representation-comparison baseline configuration.
- `traces-v1.2.2.json` — immutable v1.2.2 source-grounded policy-simulation baseline for future representation candidates.
- `runtime-optimization-scenarios.json` — current representation-comparison case contract; it supplements rather than replaces the historical eight-scenario schema.
- `RESULTS.md` — checked-in historical Phase 7 interpretation and acceptance result.
- `LIVE-EVIDENCE.md` — real GitHub delivery evidence from integrated refactor phases.
- `../../tests/test_phase7_benchmark.py` — adversarial negative fixtures for historical and current candidate-comparison scorer behavior.
- `../../tests/test_runtime_equivalence.py` — adversarial negative fixtures for the immutable runtime-equivalence gate.

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

Compare a future candidate trace set only after it is pinned to the exact candidate SHA:

```bash
python3 tools/score_phase7_benchmark.py \
  --comparison-mode candidate \
  --scenarios benchmarks/phase7/scenarios.json \
  --baseline benchmarks/phase7/traces-v1.2.2.json \
  --current <candidate-traces.json> \
  --repo-root .
```

Run adversarial fixtures:

```bash
python3 tests/test_phase7_benchmark.py
python3 tests/test_runtime_equivalence.py
```

A historical passing score still requires zero protected-behavior violations in both historical trace sets, full `G01`-`G16` scenario coverage, correct proportional coordination, and the original friction reductions. A representation candidate additionally must preserve the immutable v1.2.2 semantic gate and demonstrate a material comparable improvement; source-grounded evidence alone is not sufficient proof of actual model performance.
