# Phase 7 Operational Benchmark

This directory provides repeatable operational evaluation for the refactor against the immutable `v1.0.0` baseline. Phase 7 originally pinned the refactored runtime to the exact intermediate commit that carried the current runtime. During final stable-release readiness, the benchmark was re-pinned to immutable release commit `53182d5db086eef98ebaba757bb820b86e465845` (`v1.1.0-rc.1`) after verifying that its complete `skill/` tree is byte-identical to the former intermediate runtime pin. This keeps provenance reachable after feature-branch cleanup without changing any trace behavior.

Phase 8 completed independent review and verified delivery of `v1.1.0-rc.1`. Stable-release readiness is a separate current candidate: because the runtime policy has not changed in that readiness work, these historical traces stay pinned to the immutable prerelease runtime rather than floating to packaging/documentation commits. The exact stable candidate still receives current CI and fresh independent review before publication.

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
- `traces-current.json` — refactored source-grounded traces pinned to immutable prerelease commit `53182d5db086eef98ebaba757bb820b86e465845`.
- `RESULTS.md` — checked-in Phase 7 interpretation and acceptance result.
- `LIVE-EVIDENCE.md` — real GitHub delivery evidence from integrated refactor phases.
- `../../tests/test_phase7_benchmark.py` — adversarial negative fixtures for the scorer.

## Run

```bash
python3 tools/score_phase7_benchmark.py \
  --scenarios benchmarks/phase7/scenarios.json \
  --baseline benchmarks/phase7/traces-v1.0.0.json \
  --current benchmarks/phase7/traces-current.json \
  --repo-root . \
  --baseline-ref v1.0.0

python3 tests/test_phase7_benchmark.py
```

A passing score requires zero protected-behavior violations in both baseline and current traces, full `G01`-`G16` scenario coverage, correct proportional coordination for declared scale scenarios, and a measurable aggregate friction reduction without worsening confirmation/artifact/churn/re-discovery metrics.
