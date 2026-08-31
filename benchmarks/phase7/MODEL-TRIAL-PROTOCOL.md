# Runtime Representation Model-Trial Protocol

Tracking: #35, #36 Contract Revision 2, #37

## Purpose

Use actual comparable model/runtime executions to decide whether a lossless representation change makes the Skill materially easier and more reliable for an LLM to execute.

This protocol exists because a source-grounded policy simulation cannot prove model-performance improvement. If two representations preserve the same semantics, the prescribed correct behavior may legitimately be identical. Manually shortening a synthetic trace would therefore be evidence about the trace author, not evidence that a model executes the candidate better.

The evidence hierarchy is:

1. **Mechanical equivalence** — objective baseline-derived invariants and regression tests.
2. **Source-grounded policy simulation** — expected protected behavior and diagnostic structural/context deltas; never practical-performance proof by itself.
3. **Actual model/runtime A/B trials** — the only evidence lane that may satisfy the practical-improvement requirement.
4. **Semantic/high-assurance review** — checks that measured gains did not hide behavior loss, benchmark gaming, or maintenance/routing regressions.

## Trial unit

A trial is a paired execution of the same case against:

- immutable baseline representation `v1.2.2@f98e8a242c720931e34aa7c4e8a799090e3d0495`; and
- one exact candidate representation SHA.

Within a trial suite, keep the model/runtime identity, model settings, available tool surface, case input, and scoring rubric equivalent. Alternate which representation runs first across pairs so order/system warming cannot systematically favor one side.

Do not inspect, request, store, or score private chain-of-thought. Score only observable behavior and evidence. The scored trial JSON uses a closed schema and rejects undeclared/private-reasoning fields.

## Required observable fields

Each scored run records only:

- `case_id` and unique paired `pair_id`;
- exact representation (`baseline` or `candidate`);
- within-pair order (`1` or `2`);
- a durable transcript/tool-log reference sufficient for audit;
- whether the first/selected next action was correct;
- any protected-behavior violations;
- observable steps before the first useful action;
- unnecessary user questions/confirmations;
- unnecessary actions/tool operations;
- unnecessary runtime-reference loads;
- whether a premature terminal response required a manual `continue`.

Optional latency/token measurements may be captured in a **separate diagnostic artifact** when measured comparably, but they are not fields in the scored trial JSON and are diagnostic by default because provider/runtime scheduling and tokenizer differences can confound them.

## Required case coverage

`runtime-optimization-scenarios.json` is the single semantic owner for the representation-comparison cases, including each case's protected behavior and eval anchors. `model-trial-cases.json` is only the actual-model scoring/selection manifest: it references that canonical semantic contract and selects the same eight case IDs without duplicating their meaning.

The selected cases cover:

- hot FAST Master path;
- consequential mutation/authority path;
- Worker dispatch/resume;
- cold Master recovery;
- review/integration freshness;
- pending external job continuation;
- integration versus delivery;
- namespace/effect isolation.

The default selection suite requires at least three paired runs per case. More runs are appropriate when results are noisy or near the decision boundary.

## Hard gates

A candidate cannot pass when any is true:

- candidate produces any protected-behavior violation in the selection suite;
- candidate worsens wrong-next-action decisions or any other primary metric in **any required case**;
- required cases/pairs are incomplete or baseline-first/candidate-first order is materially unbalanced within a case;
- baseline and candidate are not tied to exact representation identities;
- runtime/model/settings/toolset identity is missing;
- evidence lacks auditable transcript/tool-log references;
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
- review of trial construction/order/settings;
- repeat or broader trials when results are marginal, model-specific, or unstable.

If no candidate passes this protocol, the correct Phase B result is **no runtime migration**.
