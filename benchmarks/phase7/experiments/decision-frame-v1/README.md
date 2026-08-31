# Decision Frame v1 — Isolated Representation Experiment

Tracking: #35 / #37

## Hypothesis

The v1.2.2 runtime already says that `Role`, `ProjectAuthority`, and `CoordinationBaseline` remain stable until their actual basis changes. The experiment asks whether expressing that existing rule as an explicit transient `KEEP / reclassify-trigger` table improves actual model execution by reducing unnecessary reconstruction, reference loading, questions, or decision errors.

This is not a proposal to add caching, persistence, a new lifecycle state, or a new authority model. The decision frame is a reasoning representation only.

## Controlled variable

The experiment replaces only the content from:

```text
## 1. Role and runtime state
```

to immediately before:

```text
## 2. Universal invariants
```

inside the immutable v1.2.2 `skill/SKILL.md`. The materializer copies every other runtime file byte-for-byte from baseline `f98e8a242c720931e34aa7c4e8a799090e3d0495`.

No canonical file under repository `skill/` is changed during this prototype.

## One-to-one semantic ledger

| Baseline semantic | Candidate representation | Intended semantic delta |
|---|---|---|
| six runtime dimensions and their values/rules | dimension table retained verbatim | none |
| dimensions are orthogonal unless a canonical rule explicitly connects them | orthogonality paragraph retained verbatim | none |
| capability/environment/risk/coordination/assurance never broadens `ProjectAuthority` | same paragraph retained verbatim | none |
| `HIGH_ASSURANCE` does not imply approval or FULL | same paragraph retained verbatim | none |
| `STANDARD` remains compatible with FAST | same paragraph retained verbatim | none |
| project/repository size alone does not select `STANDARD` or `HIGH_ASSURANCE` | same paragraph retained verbatim | none |
| keep `Role` stable until actual assignment basis changes | `Role`: reclassify only when assignment basis changes; otherwise `KEEP` | representation only |
| keep `ProjectAuthority` stable until actual authorization basis changes | `ProjectAuthority`: reclassify only when authorization basis changes; otherwise `KEEP` | representation only |
| keep `CoordinationBaseline` stable until actual coordination basis changes | `CoordinationBaseline`: reclassify only when coordination basis changes; otherwise `KEEP` | representation only |
| carry `ProjectAuthority` and `CoordinationBaseline` across Master rotation | explicit sentence retained after the table | none |
| `HIGH_ASSURANCE` is scoped to affected work and returns to `NORMAL` after escalation | explicit sentence retained after the table | none |
| `RiskLevel` is classified per substantive change only when decision-relevant | explicit sentence retained after the table | none |
| `ScopedAuthorization` is exact action/target/effect and never project-wide upgrade | explicit sentence retained after the table | none |
| `authority-gates.md` owns `CAN_EXECUTE`, effects/union, authorization, boundaries, unknown write, concurrency | owner sentence retained verbatim | none |

The candidate additionally labels the `KEEP` table a **transient decision frame for reasoning only** and explicitly says it is not a persisted project artifact or lifecycle state. This is a defensive representation of existing zero-chat/no-manager-memory behavior, not a new project-state mechanism.

## Causal isolation

This experiment intentionally does **not** combine:

- an authority fast-path/short-circuit predicate;
- reference-file splitting;
- a centralized forbidden-inference rewrite;
- legacy normalization changes;
- state-machine changes;
- new Rule IDs;
- new eval semantics.

If actual A/B evidence shows no meaningful benefit, reject this representation and retain the v1.2.2 form. If it helps, Phase B may then test additional representation changes independently before deciding whether combinations are worthwhile.

## Proof stages

1. **Mechanical isolation** — materialization/test proves only Section 1 changes and all other runtime files remain baseline-identical.
2. **Skill validation** — materialized candidate passes normal Skill source validation.
3. **Source-grounded review** — check semantic ledger, protected behavior, routing, and expected diagnostic surface without making a performance claim.
4. **Actual paired model/runtime screening** — first exercise hot FAST path and cold recovery cases because they most directly expose repeated stable-state reconstruction.
5. **Full selection suite** — no migration selection unless the candidate passes the complete canonical eight-case model-trial contract, with protected non-regression and a material observable paired improvement.

## Result status

`NOT_YET_MEASURED`

Do not describe this prototype as an improvement until actual paired model/runtime evidence passes the Phase A Contract Revision 2 gate.
