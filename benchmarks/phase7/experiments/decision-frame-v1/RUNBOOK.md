# Decision Frame v1 — Actual Model/Runtime A/B Runbook

Tracking: #35 / #37 / PR #43

## Status

This runbook executes the **actual model/runtime evidence lane**. It is intentionally separate from source-grounded policy simulation and from deterministic Skill validation.

Do not run it merely because the candidate looks cleaner. Run it only with an authorized external model endpoint whose usage/cost is understood and accepted.

Never paste an API key into an Issue, PR, repository file, command history intended for sharing, benchmark artifact, or ChatGPT relay. Provision the credential through an approved secret/environment mechanism and expose only its environment variable name to the runner.

## Provider contract

The current harness expects an OpenAI-compatible Chat Completions endpoint with function/tool calling:

```text
<API_BASE_URL>/chat/completions
```

The provider/model must support the supplied function tools and the configured token limit parameter used by the harness. Baseline and candidate must use the **same endpoint, model ID/version, settings, and toolset** for a trial suite.

The benchmark does not require OpenAI specifically; any authorized endpoint implementing the contract may be used. GitHub Models is not a viable provider because GitHub retired that service on July 30, 2026.

## Freeze before execution

Record the exact experiment branch HEAD and do not change candidate representation, inputs, scorer, harness, or acceptance rules after seeing trial results. If any of those change materially, start a new trial identity and discard prior performance claims for selection purposes.

The immutable semantic baseline remains:

```text
f98e8a242c720931e34aa7c4e8a799090e3d0495
```

The runner hashes every exact model-visible input and uses the same fingerprint on baseline/candidate sides of a pair.

## Secure credential setup

Expose the key only to the process environment, for example through the host's approved secret manager/session mechanism:

```bash
export RUNTIME_MODEL_API_KEY='...'
```

Do not commit this value. Do not put it in CLI arguments because process listings/history can expose arguments.

## 1. Screening run

Screen only the two case classes directly targeted by this experiment:

- `hot-fast-master-path`
- `cold-master-recovery`

There are three frozen inputs per case, producing six baseline/candidate pairs = **12 model runs**.

```bash
rm -rf /tmp/decision-frame-screen
python3 tools/run_runtime_ab_trials.py \
  --repo-root . \
  --mode screen \
  --api-base-url '<API_BASE_URL>' \
  --model '<MODEL_ID>' \
  --model-version '<MODEL_VERSION_OR_SNAPSHOT_ID>' \
  --output-dir /tmp/decision-frame-screen

python3 tools/score_runtime_ab_screening.py \
  --trials /tmp/decision-frame-screen/actual-model-trials.json
```

### Screening decision

`advance_to_full_suite=false` means reject/revise this experiment; do not run the full suite merely to search for a favorable aggregate.

`advance_to_full_suite=true` means only that the candidate earned the right to a full trial. It is **not** migration evidence.

## 2. Full selection run

Only after screening passes, run all eight canonical case classes, three frozen inputs each: 24 pairs = **48 model runs**.

Use a fresh output directory and the same endpoint/model/settings/toolset identity used for screening unless the entire experiment is intentionally restarted.

```bash
rm -rf /tmp/decision-frame-full
python3 tools/run_runtime_ab_trials.py \
  --repo-root . \
  --mode full \
  --api-base-url '<API_BASE_URL>' \
  --model '<MODEL_ID>' \
  --model-version '<MODEL_VERSION_OR_SNAPSHOT_ID>' \
  --output-dir /tmp/decision-frame-full

python3 tools/score_model_trials.py \
  --cases benchmarks/phase7/model-trial-cases.json \
  --trials /tmp/decision-frame-full/actual-model-trials.json
```

A full scorer PASS still requires semantic/evidence review before Phase C migration.

## Observable evidence produced

The output directory contains:

```text
trial-manifest.json
actual-model-trials.json
transcripts/
  <input>-baseline.json
  <input>-candidate.json
```

The transcripts contain only observable assistant tool calls, loaded-reference identities, state-resolution calls, terminal decision, provider response-model identifiers, and derived observable metrics. The harness explicitly instructs the model not to reveal private chain-of-thought and does not persist hidden reasoning.

Primary scored evidence is:

- protected-behavior violations;
- correct/incorrect next control action;
- observable nonterminal tool calls before the terminal useful action;
- unnecessary user question;
- unnecessary state/action operations;
- unnecessary runtime-reference loads;
- premature stop requiring manual continuation.

Optional latency/token data is not part of this scored schema.

## Evidence preservation

For an accepted candidate, preserve the raw trial output with an immutable run/candidate identity before Phase C. Do not edit individual transcript/scorer records to clean up a result. If a harness/provider defect invalidates a run, document the invalidation and rerun the affected experiment under a new complete evidence identity.

## Stop conditions

Reject or revise instead of migrating when any occurs:

- screening shows no strict observable friction gain;
- candidate has a protected behavior violation;
- candidate has a wrong next-control action;
- any required case worsens a primary metric;
- pair inputs differ;
- run order/settings/model/toolset are not comparable;
- audit references are missing/ambiguous;
- full scorer does not pass;
- measured benefit is too small to repay the representation/maintenance cost.

If the candidate fails, retain v1.2.2 runtime semantics/representation and move to the next isolated hypothesis only if another evidence-backed experiment is worthwhile.