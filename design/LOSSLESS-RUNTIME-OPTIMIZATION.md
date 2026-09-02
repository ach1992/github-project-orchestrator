# Lossless Runtime Decision-Representation Optimization

Tracking: #35  
Baseline task: #36  
Phase B: #37  
Research/audit task: #50  
Migration task: #38  
Final proof/integration task: #39
Post-v1.3.1 representation follow-up: #82

Status: **core program completed and integrated; bounded post-v1.3.1 follow-up tracked under #82**. Phase C was integrated through PR #63, with the bounded coordination-baseline follow-up completed through Issue #65 / PR #66. Current release state is tracked by `CHANGELOG.md`, GitHub Releases, and any active release Issue.

## 1. Purpose

Optimize **how** the runtime expresses the existing orchestration semantics so an LLM can retrieve, activate, combine, and execute the correct path with less irrelevant context, repeated reconstruction, duplication, reference hopping, and routing/activation error.

This program is intentionally different from adding, removing, or changing orchestration policy. It is also different from generic prompt shortening or visual cleanup. The optimization question is not:

> Can this text be made shorter or more structured?

It is:

> What representation makes this exact semantic easiest for an LLM to apply correctly at the moment it becomes relevant, while preserving every protected behavior and avoiding unnecessary active context?

The optimization target is:

```text
Semantic behavior:        IDENTICAL for protected baseline requirements
Safety/correctness:       >= baseline
Representation fit:       appropriate to the semantic shape and fragility
Activation locality:      relevant rules available with minimal unrelated context
Inference/retrieval cost: plausibly lower where a change is claimed to help
Maintenance/routing cost: no material net regression
```

Line count, token count, visual elegance, number of tables, structural novelty, or manually shortened traces are diagnostics only. They are never sufficient acceptance evidence.

### 1.1 Current proof-policy boundary

The program previously required comparable live actual-model/runtime A/B evidence as the only proof of practical improvement. Contract Revision 3 of #35/#37 changes that requirement for the current environment.

A trustworthy live A/B comparison requires a controlled uncontaminated runtime, equivalent model/settings/tool availability, stable model identity, broad enough coverage for this orchestration Skill, and evidence collection that does not itself alter the execution path. The current environment cannot guarantee that proof surface. Manual imitation would risk replacing one uncertain measurement with another.

Therefore live actual-model/runtime A/B evidence is now **optional corroboration**, not a mandatory gate. The existing runner/scorer remains useful infrastructure for a future trustworthy environment, but API/model availability no longer blocks research, representation analysis, deterministic equivalence, migration selection, or final assurance.

No optional empirical result can override a protected semantic/safety regression.

## 2. Immutable semantic comparison baseline

The semantic/equivalence baseline for this program remains:

```text
Repository: ach1992/github-project-orchestrator
Integration target: main
Baseline commit: f98e8a242c720931e34aa7c4e8a799090e3d0495
Released version: v1.2.2
```

The baseline never floats with `main`. It is comparison evidence, not a future integration target.

Baseline semantics are derived from canonical runtime/design/test owners at that commit, especially:

- `skill/SKILL.md`
- `skill/references/*.md`
- `design/RULE-MAP.md`
- `design/STATE-MODEL.md`
- `design/DECISION-GRAPHS.md`
- `skill/references/eval-scenarios.md`
- `tools/validate_skill.py`
- deterministic helper tests
- `benchmarks/phase7/*`

Later accepted target behavior must also be preserved during migration. In particular, verified `v1.2.3@ff7b23a25aac9721d515dbfd03c5b2546749a89d` added the accepted complete-response machine-relay copy-target behavior after v1.2.2. Phase C applies selected representation changes onto then-current `main`; it never materializes the old baseline wholesale.

This document is not a second canonical rule registry. It defines representation-engineering methodology; semantic truth remains with existing canonical owners.

## 3. Research foundation

Representation choices must be informed by current model guidance, the Agent Skills format, credible empirical research, and this project's own real failure/correction history. No single source is universal authority over every model or task.

### 3.1 Current OpenAI model guidance

Current OpenAI GPT-5.6 guidance recommends favoring leaner prompts, stating each instruction once, removing repeated instructions/examples that do not encode a real requirement, exposing only relevant tools, and keeping tool descriptions concise and precise. OpenAI reports directional internal coding-agent results in which leaner system prompts improved evaluation scores while substantially reducing tokens/cost; those numbers are workload-specific and are not treated here as universal performance guarantees.

The same guidance warns that repeated approval language can itself cause unnecessary approval requests. This is directly relevant to an orchestration Skill whose safety rules must be strong without creating duplicate stop pressure.

Current OpenAI model-migration guidance also favors specifying outcomes, success criteria, allowed side effects, evidence rules, and required output shape while reducing unnecessary step-by-step process instructions unless the exact path is itself part of the contract.

Implications for this Skill:

- keep true invariants explicit and singular;
- do not repeat the same control in several hot-path paragraphs merely for emphasis;
- encode exact process only where sequence is actually semantic;
- do not confuse more instructions with more reliability;
- keep generic model competence out of the Skill unless project-specific behavior would otherwise be wrong.

### 3.2 Agent Skills standard and authoring guidance

The Agent Skills specification loads content progressively:

1. metadata for discovery;
2. full `SKILL.md` when activated;
3. references/scripts/resources only when needed.

The specification recommends keeping the main `SKILL.md` under roughly 500 lines / 5,000 tokens, keeping reference files focused, and avoiding deep reference chains.

Agent Skills creator guidance adds several high-value principles:

- effective Skills come from real domain/project expertise, runbooks, issues, corrections, and failure history rather than generic advice;
- every token in activated `SKILL.md` competes for attention with conversation/system/tool context;
- add what the agent would otherwise get wrong; omit what it already knows;
- overly comprehensive Skills can cause irrelevant paths to activate;
- moderate, stepwise detail often beats exhaustive documentation;
- tell the agent exactly **when** to load deeper references;
- match specificity to fragility: allow judgment where several approaches are valid, but prescribe exact mechanics when sequence/consistency is fragile;
- provide a default path rather than a menu of equal options;
- favor reusable procedures over instance-specific answers;
- use gotchas, templates, checklists, validation loops, and scripts only where the task shape justifies them.

These principles strongly support the existing project goal of a compact control kernel plus direct event-specific references.

### 3.3 Long-context locality and retrieval

Long-context research such as *Lost in the Middle* shows that models do not necessarily use information equally well at every context position; retrieval and use of relevant information can degrade when required facts are buried inside long context.

This does **not** mean every important rule must be placed at the beginning or duplicated at the end. Duplication creates its own attention and contradiction cost. The engineering implication is instead:

- reduce unrelated active context;
- route directly to the relevant owner;
- keep decision-critical inputs/conditions sufficiently local;
- avoid long chains where a rule depends on material accidentally loaded earlier;
- prefer progressive disclosure over unconditional loading of rare-path detail.

### 3.4 Prompt and instruction sensitivity

Peer-reviewed and recent empirical work shows that meaning-preserving wording and formatting changes can affect instruction following, sometimes substantially. Other research shows that part of apparent format sensitivity can come from brittle evaluation methods. Together these results argue against a universal claim such as "Markdown is best", "JSON is best", or "tables are always clearer for an LLM".

Instruction-reliability research also shows that high benchmark accuracy does not guarantee robustness to nuanced prompt variants, and lexical-sensitivity studies show semantically similar instruction wording can produce different downstream behavior.

Engineering implication:

- semantic equivalence must be protected explicitly when wording/format changes;
- representation changes should be chosen from semantic shape, not fashion;
- one representation should not be generalized from one model/task/study to every Skill domain;
- deterministic regression/property checks are valuable because surface equivalence is not enough.

### 3.5 Structured representations: useful but not universally superior

Table-understanding research shows representation format affects LLM performance and that structured text can help when the underlying task is truly tabular/relational. However, studies of structured generation also show that rigid output-format restrictions can reduce reasoning performance in tasks where free-form reasoning is important.

This yields a crucial rule for this program:

> **Structure should expose existing structure, not impose artificial structure on nuanced semantics.**

A gate matrix is a strong candidate when the rule really is a matrix. A state transition table is useful when there is a real lifecycle. A schema is appropriate for an exact handoff record. But a paragraph expressing nuanced engineering judgment may become worse, not better, if forced into a Boolean table.

### 3.6 Public Skill implementations as supporting experience

Current OpenAI plugin Skills provide useful implementation examples but are supporting evidence, not universal templates. Strong recurring patterns include:

- short umbrella/router Skills that quickly dispatch to specialist domains;
- concise default workflows;
- explicit boundaries between what the current Skill owns and what should route elsewhere;
- focused references rather than a monolithic instruction file;
- deterministic scripts/validators where repeated mechanics would otherwise be reinvented.

Our runtime already follows much of this architecture. Optimization should improve the weak surfaces, not replace working progressive routing merely because another project uses a different layout.

### 3.7 Research sources

Starting primary/credible sources, reviewed for this revision on 2026-08-31:

- OpenAI, current model guidance: https://developers.openai.com/api/docs/guides/latest-model
- Agent Skills specification: https://agentskills.io/specification
- Agent Skills creator best practices: https://agentskills.io/skill-creation/best-practices
- Liu et al., *Lost in the Middle*: https://arxiv.org/abs/2307.03172
- Lou et al., *Large Language Model Instruction Following: A Survey of Progresses and Challenges*: https://aclanthology.org/2024.cl-3.7/
- Zhan et al., *Unveiling the Lexical Sensitivity of LLMs*: https://aclanthology.org/2024.emnlp-main.295/
- Dong et al., *Revisiting the Reliability of Language Models in Instruction-Following*: https://aclanthology.org/2026.acl-long.354/
- He et al., *Does Prompt Formatting Have Any Impact on LLM Performance?*: https://arxiv.org/abs/2411.10541
- Deng et al., *Tables as Texts or Images*: https://aclanthology.org/2024.findings-acl.23/
- Tam et al., *Let Me Speak Freely?*: https://aclanthology.org/2024.emnlp-industry.91/
- Qin et al., *InFoBench*: https://aclanthology.org/2024.findings-acl.772/

Use newer primary evidence when materially relevant. Treat single studies and vendor-specific measured percentages as bounded evidence, not immutable design laws.

## 4. Core design principle

Optimize **decision application cost**, not prose aesthetics.

For each semantic unit, choose the cheapest representation that makes the exact rule easy to retrieve and apply correctly while preserving nuance, precedence, exceptions, and ownership.

### 4.1 Representation-selection dimensions

Before changing a unit, classify it across six dimensions:

| Dimension | Question |
|---|---|
| semantic shape | What logic actually exists: invariant, branch, precedence, lifecycle, set of effects, judgment, schema, router, procedure? |
| activation locality | Is this hot, warm, cold, or DEV-only? |
| fragility | Can the agent choose among several valid approaches, or must sequence/shape be exact? |
| canonical ownership | Where is the single normative owner and what reminders/duplicates exist? |
| retrieval/inference cost | How many conditions/references must be reconstructed before the correct decision is available? |
| maintenance cost | Does a new abstraction/router/schema reduce future work or create another surface to keep synchronized? |

Paragraph count and file length are not classification dimensions by themselves.

### 4.2 Default representation mapping

| Semantic shape | Preferred representation when justified | Avoid when |
|---|---|---|
| nuanced engineering/product judgment | concise prose with purpose/constraints | rigid Booleanization would lose nuance/context |
| short unordered completeness set | bullets/checklist | items have precedence/branching semantics |
| fixed dimensions/comparisons | compact table | cells become long mixed-purpose paragraphs |
| authority/gate combinations | gate matrix + canonical predicate | obligations are hidden by one scalar class |
| branching/precedence/control flow | ordered decision table, predicate, pseudocode, or compact ASCII DAG | flow is mostly judgment rather than deterministic branching |
| lifecycle | state-transition relation/table/graph | no real state transition exists |
| simultaneous consequences | set/effect model + obligation union | ordering is mistakenly substituted for independent obligations |
| event -> domain owner | direct router table | routing requires several hidden intermediate references |
| structured handoff/persisted record | schema/template | free-form judgment is the actual requirement |
| deterministic invariant/validation | script/test/linter | behavior requires contextual professional judgment |
| rare-path detail | focused trigger-loaded reference | rule must be known before its trigger is recognizable |
| non-obvious recurring failure | concise gotcha near earliest reliable trigger | it merely restates a normal rule already easy to infer |
| explanatory rationale | concise prose, optionally adjacent to the decision it explains | rationale becomes a second normative owner |

`KEEP` is always a valid result.

### 4.3 Why not "convert ten paragraphs into a table" automatically?

Ten paragraphs can represent very different things:

- ten variations of the same duplicated rule -> consolidate;
- a true decision matrix -> table/matrix may be better;
- an ordered flow -> decision table/pseudocode may be better;
- a lifecycle -> state relation may be better;
- nuanced trade-offs -> concise prose may remain best;
- rare-path details -> move to a triggered reference rather than reformat in place;
- deterministic validation -> replace repeated prose reasoning with a script/test.

The optimization unit is the **semantic function**, not the paragraph.

## 5. Lossless-equivalence surface

Before any canonical runtime representation change, preserve/check at least these classes.

### 5.1 Rule and goal identity

- exact baseline canonical Rule-ID set;
- one canonical owner per Rule ID;
- Goal-to-Rule and Rule-to-eval coverage;
- no orphan/duplicate owner introduced by restructuring.

### 5.2 Runtime dimensions

Preserve independent meanings and non-implications for:

- `Role`
- `ProjectAuthority`
- `ScopedAuthorization`
- `CoordinationBaseline`
- `AssuranceLevel`
- `RiskLevel`
- `ExecutionPath`
- `ContractPersistence` where applicable
- `ExecutionStrategy` where applicable
- `ApplicableEffects`

No representation optimization may reconstruct a scalar profile/action class that loses existing orthogonality.

### 5.3 Lifecycle namespaces

Preserve independent namespaces and valid meanings/transitions:

- `TaskState`
- `WorkerStatus`
- `WriteState`
- `DeliveryState`
- `MasterBoundary`

String equality across namespaces is never a semantic edge.

### 5.4 Canonical decision ownership

Preserve singular ownership and semantics for decisions such as:

- `CAN_EXECUTE(action)`
- `MASTER_STOP(boundary, independent_work)`
- `REVIEW_VALID(envelope)`
- delivery proof/readiness decisions owned by release semantics
- Worker assignment/staleness/absorption rules

A candidate may change the representation but must not create competing independently-derived versions.

### 5.5 Multi-effect obligations

`ApplicableEffects` remains a set and required controls remain the union of obligations for every actual/deterministic effect. A shortcut or table must not collapse `INTEGRATION + PRODUCTION + DESTRUCTIVE_OR_IRREVERSIBLE` into one scalar class or erase an independent gate.

### 5.6 Progressive loading and direct reachability

- every runtime domain required by an event remains directly reachable from `SKILL.md`;
- a rule must not depend on accidentally loading another reference first;
- cold/rare-path material must not become an unconditional hot-path dependency without strong justification;
- `SKILL.md` stays a control kernel rather than a duplicate of domain references;
- reference splitting must not create deep chains or force multiple loads for one ordinary decision.

### 5.7 Compatibility and accepted target drift

Legacy accepted inputs may be normalized once into canonical vocabulary, but resulting meaning must remain identical. Later accepted runtime behavior after v1.2.2 must be preserved on the then-current integration target.

## 6. Forbidden-inference guard

Candidate representations must continue preventing at least these high-value false edges:

| Observed fact | Must not imply |
|---|---|
| `HIGH_ASSURANCE` | `FULL`, persistence, approval, or broader Authority by itself |
| `STANDARD` | `FULL` by itself |
| technical capability/access | broader `ProjectAuthority` |
| exact `ScopedAuthorization` | project-wide Authority upgrade |
| Worker `BLOCKED` | automatic `MasterBoundary.BLOCKED` |
| `TaskState.BLOCKED` | automatic `MasterBoundary.BLOCKED` |
| `WriteState.UNKNOWN` | automatic Master stop |
| `TaskState.INTEGRATED` | `DeliveryState.DELIVERED` |
| delivery target identity | delivery lifecycle state |
| no pre-existing READY Issue | permission to stop |
| existing explicit contract | `FULL` by itself |
| `FULL` | persisted Issue/contract by itself |
| environment name such as staging/test | proof of reversible/non-production effect |
| workflow-triggering push | `PRODUCTION` unless deterministic triggered effect actually is production |

This is a proof target, not a new normative owner.

## 7. Candidate representation families

Treat each family as a conditional tool, not a planned rewrite.

### 7.1 Compact decision frame

Use only when several already-established orthogonal inputs repeatedly need to be reassembled for one decision. It may reduce inconsistent re-derivation, but it must not become a new persisted state or duplicate canonical truth.

PR #43's stable-state `KEEP / reclassify-trigger` frame is one prior hypothesis in this family. #50 must reassess whether the actual recurring problem and representation fit justify it.

### 7.2 Decision card

For one bounded decision owner, co-locate only what materially reduces hidden lookup:

```text
TRIGGER
INPUTS
DECIDE
OUTPUT
UNKNOWN / EXCEPTION HANDLING
LOAD DEEPER ONLY IF ...
```

Use only when this improves locality without duplicating domain semantics elsewhere.

### 7.3 Ordered decision table / predicate / compact ASCII DAG

Use when behavior is genuinely branching or precedence-driven. Keep common paths short and uncertainty/rare exceptions routed to the canonical deeper owner.

### 7.4 Safe common-path subset

A shortcut is allowed only if it is a provable safe subset/equivalent of the canonical decision, for example:

```text
FAST_SUBSET(action) == true  =>  CAN_EXECUTE(action) == true
```

If the implication cannot be protected for every allowed input combination, do not adopt it.

### 7.5 Hot/warm/cold/DEV-only locality

Move detail by activation locality only when the rule remains directly discoverable at the right event and reference fragmentation does not increase total decision cost.

Do not split files merely because they are long.

### 7.6 Legacy normalization layer

When compatibility inputs appear, normalize once to current canonical terms before ordinary reasoning. Do not carry duplicate legacy vocabulary through every hot path.

### 7.7 Machine-readable semantic IR

Consider only for deterministic mechanics whose machine form can be validated/generated without becoming a competing semantic owner. Do not encode nuanced judgment merely to obtain a cleaner schema.

## 8. Research-first runtime audit protocol (#50)

No canonical `skill/` change occurs during the audit pass.

For each semantic unit in `skill/SKILL.md` and directly routed `skill/references/*.md`, record only enough information to support a decision:

| Field | Meaning |
|---|---|
| owner / semantic | exact canonical decision/rule being expressed |
| current representation | prose, bullets, table, predicate, schema, flow, etc. |
| semantic shape | classification from §4 |
| locality | hot / warm / cold / DEV-only |
| fragility | flexible judgment or exact/sequence-sensitive |
| duplication | repeated normative wording or justified local reminder? |
| retrieval/inference burden | reference hops, scattered conditions, reconstructed dimensions, hidden exceptions |
| recommendation | `KEEP`, `MOVE/ROUTE`, `TABLE/MATRIX`, `DECISION`, `STATE`, `PREDICATE/SET`, `SCHEMA`, `SCRIPT/TEST`, `PROSE` |
| rationale | why this representation should be more reliable/easier to apply for an LLM |
| protection | exact rules/evals/tests that prevent semantic loss |

Prioritize surfaces by expected payoff:

1. high-frequency decisions with repeated reconstruction/duplicate rules;
2. high-risk decisions whose semantics are scattered or easy to collapse incorrectly;
3. repeated reference hops that can be made direct without duplicating ownership;
4. deterministic mechanics currently re-derived in prose;
5. cold material occupying the unconditional kernel without justification;
6. only then lower-frequency stylistic opportunities.

Do not bundle multiple representation families merely for efficiency. The source of benefit should remain understandable.

## 9. Evidence hierarchy for adoption

A candidate representation may advance only when every applicable layer supports it.

### 9.1 Canonical semantic contract

Confirm exact owner and required behavior. No candidate may reinterpret the requirement to make optimization easier.

### 9.2 Research-backed representation rationale

Explain why the semantic shape, locality, fragility, and current evidence favor the candidate representation over the existing one. Cite current primary/credible guidance where useful, but do not turn a single source into a universal rule.

### 9.3 One-to-one semantic ledger

Map every affected baseline semantic to its candidate form. A paragraph boundary is presentation, not a semantic-unit boundary: one paragraph may contain several independently operative rules, conditions, modifiers, defaults, or overrides. A structured candidate must map each such atom separately and must not imply mutual exclusivity, precedence, exhaustiveness, or shared activation unless the baseline semantics already do.

Detect:

- omitted conditions or independently meaningful concepts;
- new implications or artificial branch exclusivity;
- precedence/default/override changes;
- state/effect/concept collapse;
- hidden exception or qualifier loss;
- duplicate canonical owners;
- new reference dependencies.

### 9.4 Deterministic equivalence and regression protection

Run applicable Rule/Goal/state/router/eval coverage, property/adversarial tests, validators, compatibility tests, packaging checks, and runtime-cleanliness checks.

Deterministic checks do not prove nuanced prose equivalence by themselves; semantic review still applies.

### 9.5 Source-grounded operational analysis

Walk representative existing scenarios through baseline and candidate semantics using only observable/canonical decisions. Confirm equal protected decisions and inspect the claimed structural benefit, such as:

- fewer duplicate normative rules active at once;
- fewer reference hops before the decisive owner;
- less repeated reconstruction of already-established dimensions;
- clearer precedence/exception locality;
- smaller unrelated hot-path activation surface;
- deterministic work moved from repeated reasoning to a validator/script.

Synthetic deletion of reasoning steps is not proof. The structural claim must follow from the actual representation and routing change.

### 9.6 Maintenance/routing cost

Account for:

- new files/router nodes;
- synchronization burden;
- schema/validator complexity;
- future edit locality;
- discoverability;
- compatibility burden;
- risk of two competing sources of truth.

A representation that is marginally cleaner but creates more ownership/routing complexity should be rejected.

### 9.7 Optional controlled model/runtime corroboration

If a trustworthy environment later exists, the integrated model-trial lane may provide additional observable evidence. The runner/scorer must preserve its identity/input/order/audit constraints.

Optional A/B evidence:

- is not required solely for historical consistency;
- must not be manufactured manually in an uncontrolled environment;
- cannot override any protected regression;
- should be interpreted as model/runtime-specific evidence, not a universal representation law.

### 9.8 Final independent assurance

Before high-risk canonical integration, freeze exact candidate/current target and obtain fresh independent HIGH_ASSURANCE review of the complete effective change and evidence envelope.

## 10. Measurement and diagnostic model

### Protected hard gates

A candidate fails if it causes any required protected regression, including:

- unsafe/stale mutation;
- authority/gate leakage;
- state namespace collapse;
- lost obligation from a multi-effect action;
- stale review/integration approval;
- incorrect Worker ownership/assignment behavior;
- false delivery completion;
- wrong/early terminal Master stop;
- loss of zero-chat recoverability;
- required compatibility regression;
- new duplicate/contradictory canonical owner.

### Structural/operational benefit indicators

These can substantiate a representation decision when tied directly to the changed runtime path:

- canonical instruction duplication removed;
- reference hops reduced without hiding required detail;
- conditions/precedence made local to the decision owner;
- hot-path unrelated context removed through direct progressive routing;
- deterministic re-derivation replaced by validated mechanics;
- stable dimension reconstruction avoided without introducing persistent state;
- fewer equally presented alternatives because a correct default is now explicit;
- rare exceptions moved out of the hot path while remaining directly triggerable.

### Diagnostics only

These cannot select a candidate by themselves:

- line/word/token count;
- number of files/tables/graphs;
- visual neatness;
- source-grounded trace length without a real representation/routing reason;
- one model/provider recommendation with no fit analysis;
- optional latency/token measurements from uncontrolled runtime conditions.

## 11. One-to-one migration ledger (#38)

Every changed canonical surface must be reviewable with a row like:

| Baseline owner/semantic | Candidate owner/representation | Representation rationale | Equivalence/protection evidence | Operational benefit evidence | Status |
|---|---|---|---|---|---|
| exact current rule/decision | exact candidate form | semantic-shape/locality/fragility reason | eval/property/review reference | structural/source-grounded evidence | unchanged / adopted / rejected |

Keep the ledger in the active Issue/PR when sufficient; do not create a permanent duplicate runtime registry merely to host it.

## 12. Phase gates

### Phase A — baseline/equivalence (#36)

Complete. Preserve exact immutable semantic baseline and deterministic equivalence inventory/checks.

### Phase B — research/audit/prototypes (#37 / #50)

1. synthesize current representation evidence and applicability limits;
2. audit runtime by semantic unit without canonical runtime changes;
3. rank actual opportunities by payoff/risk;
4. reassess PR #43 as one hypothesis;
5. prototype only the smallest justified candidate families;
6. reject ideas whose evidence does not beat `KEEP`.

No missing model API blocks this phase.

### Phase C — lossless migration (#38)

Apply only selected research/evidence-backed candidates onto then-current `main`. Preserve one-to-one semantic coverage and accepted target drift. Rerun complete deterministic/semantic/source-grounded protection.

### Phase D — final proof/integration (#39)

Freeze exact candidate/target, run full validation, prove semantic completeness and retained structural benefit, complete fresh independent HIGH_ASSURANCE review, and integrate through repository-normal controlled path only when all gates pass.

Public version/release publication remains a separate consequential action.

## 13. Acceptance rule

A candidate representation is eligible for final integration only if all are true:

```text
ProtectedBehavior(candidate) >= ProtectedBehavior(baseline)
SemanticCoverage(candidate) == RequiredBaselineCoverage
RepresentationRationale(candidate) == RESEARCH_BACKED_AND_SEMANTICALLY_FIT
DeterministicAndAdversarialProtection(candidate) == PASS
SourceGroundedOperationalAnalysis(candidate) == SUPPORTS_CLAIMED_BENEFIT
NetMaintenanceAndRoutingCost(candidate) does not erase the benefit
ExactCandidateValidation == PASS
FreshIndependentReview == COMPLETE / APPROVE
```

When trustworthy controlled model/runtime evidence exists, it may strengthen the case but is not mandatory under the current contract.

If research/audit shows that the current representation is already the better trade-off, the correct result is **no runtime refactor**. The purpose of this program is a better operating Skill, not a larger change set.