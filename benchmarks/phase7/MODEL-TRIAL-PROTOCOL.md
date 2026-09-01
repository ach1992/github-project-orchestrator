# Runtime Representation Model-Trial Protocol

Tracking: #35 Contract Revision 3, #36, #37, #47, #38 Contract Revision 3, #39 Contract Revision 2

## Purpose

Use actual comparable model/runtime executions as optional empirical corroboration when a trustworthy controlled environment is available, without making this lane a prerequisite for migration or final assurance.

This protocol exists because a source-grounded policy simulation cannot prove model-performance improvement. If two representations preserve the same semantics, the prescribed correct behavior may legitimately be identical. Manually shortening a synthetic trace would therefore be evidence about the trace author, not evidence that a model executes the candidate better.

The evidence hierarchy is:

1. **Mechanical equivalence** — objective baseline-derived invariants and regression tests.
2. **Source-grounded policy simulation** — expected protected behavior and diagnostic structural/context deltas; never practical-performance proof by itself.
3. **Actual model/runtime A/B trials** — optional measured corroboration that may strengthen or challenge a structural/model-execution benefit assessment when the environment is trustworthy.
4. **Semantic/high-assurance review** — checks that claimed gains did not hide behavior loss, benchmark gaming, or maintenance/routing regressions.

Under the current #35/#38/#39 proof policy, live A/B is optional corroboration rather than a mandatory migration gate. Source-grounded structural evidence must still never be described as measured model/runtime performance, and any live A/B result that is used must satisfy this protocol.

## Trial unit

A trial is a paired execution of the same exact case input against:

- immutable baseline representation `v1.2.2@f98e8a242c720931e34aa7c4e8a799090e3d0495`; and
- one exact candidate representation SHA.

Within a trial suite, keep the model/runtime identity, model settings, available tool surface, case input, and scoring rubric equivalent. Each baseline/candidate pair carries the same non-empty `input_fingerprint`, and the scorer rejects mismatched paired inputs. Alternate which representation runs first across pairs so order/system warming cannot systematically favor one side.

Do not inspect, request, store, or score private chain-of-thought. Score only observable behavior and evidence. The scored trial JSON uses a closed schema and rejects undeclared/private-reasoning fields.

## Executable evidence lane

`tools/run_model_trials.py` is the single provider/paired-execution layer for this protocol. It does not own case semantics or scoring policy:

- `runtime-optimization-scenarios.json` remains the semantic owner and now carries each case's exact `trial_input` next to its existing protected behavior and measurement contract;
- `model-trial-cases.json` remains the selection/scoring manifest;
- the exact experiment descriptor at the candidate SHA owns how the candidate representation is materialized from the immutable baseline;
- `score_model_trials.py` remains the only deterministic scored-evidence gate.

The runner validates the exact baseline/candidate identities, materializes the candidate entrypoint from the frozen experiment descriptor, precomputes the full paired plan and exact input fingerprints before dispatch, and alternates baseline-first/candidate-first order deterministically. It exposes only one controlled function tool, `read_runtime_reference`, so progressive reference routing remains observable without adding project-specific orchestration tools. Raw tool audit records store path/hash/size/status rather than duplicating reference contents.

Default `--suite screening` consumes the experiment's declared screening IDs and `minimum_pairs_per_case` from the existing manifest. For the current first experiment this is exactly 3 pairs each for `hot-fast-master-path` and `cold-master-recovery`: 6 pairs / 12 representation executions. `--suite selection` consumes all eight case IDs from the manifest. Increasing pair count changes the frozen plan fingerprint and therefore the auditable trial identity.

Dry-run/plan mode needs no API credential and performs no provider call:

```bash
python3 tools/run_model_trials.py \
  --candidate-ref 9384b371264473b291fe815b5725ae64f44d4179 \
  --dry-run
```

The exact candidate commit must already exist in local Git object storage; dry-run never fetches it implicitly. This keeps candidate provenance/network activity outside trial execution.

For a live run, provision `RUNTIME_MODEL_API_KEY` only through an approved server-side secret/environment mechanism. The runner intentionally has no API-key command-line option and never writes request headers or the secret into evidence. Supply the non-secret runtime identity through `API_BASE_URL`, `MODEL_ID`, `MODEL_VERSION`, and explicit `MODEL_SETTINGS_JSON` (or the corresponding non-secret CLI options), then provide new, non-existing paths for `--raw-output` and `--annotation-template-output`. Evidence paths are create-only: the runner refuses to overwrite an existing trial artifact.

The transport boundary is the OpenAI-compatible Chat Completions endpoint (`POST /chat/completions`) with one response choice and function-tool calling. `API_BASE_URL` may be the API root (for example an endpoint ending in `/v1`) or the full `/chat/completions` route. HTTPS is required except for loopback/local mocked HTTP. There is no automatic retry: transport/provider-schema failure stops the suite, writes only incomplete raw evidence, produces no scorer-input template, and cannot be claimed as scored evidence.

A successful raw artifact contains exact representation/runtime/settings/toolset identity, the frozen plan, unique `trial://...` per-run audit references, user-visible model output/refusal, safe provider response identity/status, timestamps, and observable runtime-reference tool operations. Unknown provider fields are not copied into evidence; private reasoning is never requested or persisted.

After every planned run completes, the runner can emit an **annotation template** shaped like the scorer input. Its `observed` fields are intentionally `null`: the runner does not silently judge semantic correctness, protected violations, useful-action steps, or unnecessary activity. The unannotated template is deliberately rejected by `score_model_trials.py`. A reviewer/explicit annotation step must fill only observable fields from the raw evidence before the scorer is run.

## Required observable fields

Each scored run records only:

- `case_id` and unique paired `pair_id`;
- `input_fingerprint` identifying the exact case input seen by both sides of the pair;
- exact representation (`baseline` or `candidate`);
- within-pair order (`1` or `2`);
- a unique durable transcript/tool-log reference sufficient to audit that run;
- whether the first/selected next action was correct;
- any protected-behavior violations;
- observable steps before the first useful action;
- unnecessary user questions/confirmations;
- unnecessary actions/tool operations;
- unnecessary runtime-reference loads;
- whether a premature terminal response required a manual `continue`.

Optional latency/token measurements may be captured in a **separate diagnostic artifact** when measured comparably, but they are not fields in the scored trial JSON and are diagnostic by default because provider/runtime scheduling and tokenizer differences can confound them.

## Required case coverage

`runtime-optimization-scenarios.json` is the single semantic owner for the representation-comparison cases, including each case's exact model-trial input, protected behavior and eval anchors. `model-trial-cases.json` is only the actual-model scoring/selection manifest: it references that canonical semantic contract and selects the same eight case IDs without duplicating their meaning.

The selected cases cover:

- hot FAST Master path;
- consequential mutation/authority path;
- Worker dispatch/resume;
- cold Master recovery;
- review/integration freshness;
- pending external job continuation;
- integration versus delivery;
- namespace/effect isolation.

The default selection suite requires at least three paired runs per case. More runs are appropriate when results are noisy or near the decision boundary, but any post-output plan/input/settings/threshold change is a new auditable trial identity rather than an in-place rewrite of observed evidence.

## Hard gates

A claimed passing empirical A/B result cannot satisfy this protocol when any is true:

- candidate produces any protected-behavior violation in the selection suite;
- candidate worsens wrong-next-action decisions or any other primary metric in **any required case**;
- required cases/pairs are incomplete or baseline-first/candidate-first order is materially unbalanced within a case;
- the two sides of a pair do not have the same exact `input_fingerprint`;
- baseline and candidate are not tied to exact representation identities;
- runtime/model/settings/toolset identity is missing;
- evidence lacks unique auditable transcript/tool-log references;
- scored evidence contains undeclared/private-reasoning fields;
- no material paired improvement is demonstrated.

A better token count, prettier table, shorter file, or hand-authored source trace cannot compensate for one of these failures.

## Material improvement rule

For paired observable metrics, the deterministic scorer uses an exact one-sided sign test over non-tied pairs. By default, `alpha = 0.05`.

The candidate must:

1. pass every hard gate; and
2. show statistically directional paired improvement (`p <= alpha`) on at least one primary metric:
   - protected-violation count;
   - wrong-next-action count;
   - observable steps before first useful action; or
   - composite avoidable events = unnecessary questions + unnecessary actions + unnecessary reference loads + manual-continue events.

The sign test deliberately ignores improvement magnitude when testing direction, so the scorer also reports aggregate totals for review. Final selection still checks whether the measured gain is operationally meaningful enough to repay maintenance/routing complexity.

## What the scorer proves and does not prove

A passing score proves only that the supplied paired observable trial records satisfy this protocol and show a directional improvement without the configured protected regressions. It does not prove that transcripts are authentic, that a provider/model implementation is unbiased, or that every future model/runtime will improve.

Therefore final adoption also requires:

- exact candidate identity;
- raw evidence availability;
- semantic/equivalence checks;
- review of trial construction/order/settings and input-fingerprint provenance;
- repeat or broader trials when results are marginal, model-specific, or unstable.

If no candidate passes this protocol, no passing empirical A/B corroboration has been established. Under the current program proof policy that absence does not by itself block migration; the governing structural/equivalence/review evidence must still independently justify any practical-benefit conclusion.
