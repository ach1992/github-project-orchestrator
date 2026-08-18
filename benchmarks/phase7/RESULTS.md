# Phase 7 Benchmark Results

Status: **PASS for the historical source-grounded operational benchmark of the refactored runtime pinned to `v1.1.0-rc.1`.** Phase 8 subsequently completed independent release-candidate review and delivered `v1.1.0-rc.1`. The later stable `v1.1.0` readiness work changed distribution/testing/documentation rather than the pinned runtime policy. A later candidate that changes runtime policy—including `v1.1.1` continuation maintenance—is outside this benchmark result and requires its own current regression specification, exact-head validation, source/diff review, and fresh independent review.

The refactored traces are pinned to immutable release commit `53182d5db086eef98ebaba757bb820b86e465845` (`v1.1.0-rc.1`). During final `v1.1.0` readiness, GitHub tree evidence verified that every top-level entry of `skill/` at this release commit has the same blob/tree SHA as the former intermediate runtime pin `262395df2bc20d3014238e3f40f7b3f02b4f0500`; therefore the re-pin changed provenance reachability, not evaluated runtime behavior. The eight fixed traces remain behaviorally unchanged; regression scenario `BC` separately covers the independent-review handoff boundary. They are historical Phase 7 evidence, not candidate-current execution evidence for later runtime-policy changes.

## A/B result

| Metric | `v1.0.0` baseline | Refactored runtime | Result |
|---|---:|---:|---|
| protected-behavior violations | 0 | 0 | preserved |
| steps before first useful action (aggregate) | 56 | 48 | **14.3% lower** |
| discovery/recovery steps (aggregate) | 13 | 6 | **53.8% lower** |
| activated reference domains (aggregate) | 14 | 13 | **7.1% lower** |
| unnecessary human confirmations | 0 | 0 | no regression |
| unnecessary artifacts | 0 | 0 | no regression |
| Worker churn | 0 | 0 | no regression |
| repeated discovery | 0 | 0 | no regression |
| stale integrations | 0 | 0 | preserved |
| wrong/premature Master stops | 0 | 0 | preserved |
| required production confirmations | 1/1 present | 1/1 present | preserved |
| required delivery verification | 1/1 present | 1/1 present | preserved |
| canonical Goal coverage | G01-G16 | G01-G16 | complete |

The friction gain is concentrated where the refactor intentionally changed operational structure: large/multi-repository work, cold recovery, bounded Worker context, and local-blocker continuation. Small and medium representative work does not become heavier. Review freshness and production release controls remain equally strict.

## Scenario observations

- **Small routine fix:** remains `LIGHTWEIGHT`; no extra confirmation/artifact and no protected regression.
- **Medium coordinated project:** remains `STANDARD` with one justified durable coordination artifact.
- **Large multi-repo critical path:** current trace uses the global coordination spine plus only the active workstream instead of traversing every repository before acting.
- **Cold recovery:** current trace reaches the active PR through orientation spine + active-path context and stops broad reading once the next action is decision-valid.
- **Bounded Worker delegation:** remains `LIGHTWEIGHT`; Worker loads only task/Worker domains by default instead of project-wide gate context when no gate question is triggered.
- **Review HEAD drift:** both versions invalidate stale review and re-review the current candidate before integration.
- **Auto-production release:** both versions gate the deterministic production effect before merge and require post-release delivery evidence.
- **Local blocker:** both continue independent work; the refactored trace removes one redundant discovery step.

## Adversarial scorer checks

The benchmark test suite intentionally corrupts valid traces and requires failures for:

1. stale integration after candidate drift;
2. missing post-release delivery verification;
3. premature global `BLOCKED` stop while independent work exists;
4. unnecessary human confirmation on routine reversible work;
5. unsafe shortcut/hidden-work style violations;
6. overweight coordination (`STANDARD` where the scenario contract requires `LIGHTWEIGHT`).

These negative fixtures passed before the release-candidate publication and remain part of CI for later candidates as regression checks for the historical benchmark/scorer contract.

## Interpretation boundary

This result demonstrates a lower-friction **policy execution path** for the runtime pinned to `v1.1.0-rc.1` while preserving the benchmarked guarantees. It does not claim independent model-performance statistics, wall-clock latency improvement, or production reliability from these eight traces alone. `LIVE-EVIDENCE.md` adds real repository execution evidence. Phase 8 supplied the independent review and verified prerelease delivery that were still pending when Phase 7 was first authored. Any later candidate must still satisfy its own current review, CI, release, and post-release evidence gates; when it changes runtime policy, these eight historical traces do not themselves evaluate that new policy unless explicitly regenerated for it.
