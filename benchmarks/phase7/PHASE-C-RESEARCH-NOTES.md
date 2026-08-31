# Phase C Representation Engineering Notes

This note records the evidence model used to optimize the Skill without pretending that uncontrolled live-model A/B runs are decisive.

## Engineering conclusion

Optimize **semantic application cost**, not raw length. The useful question is not “can this prose be shorter or more structured?” but “what representation exposes this semantic function with the least retrieval, reconstruction, ambiguity, and maintenance cost while preserving every protected behavior?”

Use representation by semantic topology:

- nuanced judgment / trade-offs -> concise prose;
- fixed orthogonal dimensions or comparison -> compact table;
- true condition/action branching or precedence -> decision table / guarded algorithm;
- true lifecycle transitions -> state-transition representation;
- simultaneous independent effects -> set/union model, not a scalar precedence tree;
- event -> owner/reference routing -> direct router table;
- persisted structured handoff/identity -> schema/template;
- deterministic invariant -> executable validator/test where practical;
- rare/cold detail -> trigger-loaded reference via progressive disclosure;
- rationale -> short prose beside the decision, never a second normative owner.

`KEEP` is always a valid outcome. Ten paragraphs should not automatically become a table: first identify whether they encode duplicate ownership, a matrix, an ordered algorithm, a lifecycle, nuanced judgment, cold detail, or deterministic mechanics. The optimization unit is the **semantic function**, not the paragraph.

## Research principles reflected in the migration

1. **Lean active context:** remove repeated instruction/ontology only where the canonical owner remains clear and reachable.
2. **Progressive disclosure:** keep cold detail behind explicit triggers; do not move rare complexity into the always-active kernel merely to make files look smaller.
3. **Locality over duplication:** put a rule near the dimension/branch it governs when that reduces inference, but do not repeat the same normative rule in multiple owners.
4. **Structure only when structure is real:** tables and algorithms help when the semantics are genuinely tabular/branching; forced structure can erase nuance or invent precedence.
5. **One canonical owner:** consumers should reference/consume the owner instead of redeclaring its ontology.
6. **No hidden performance claim:** source-grounded structural evidence can support representation/locality/maintenance claims, not fabricated latency/accuracy claims.
7. **Lossless migration:** every selected change requires one-to-one semantic mapping, deterministic isolation/composition guards, full repository validation, and fresh independent review before HIGH-risk integration.

## Why live A/B is optional here

The available ChatGPT environment cannot currently guarantee an uncontaminated, identical model/runtime/tool/plugin context for baseline and candidate runs. A manual relay across fresh chats would also make complex multi-step orchestration difficult to instrument consistently. Such runs may be useful later as corroboration, but making them a mandatory gate would create false precision. The current migration therefore relies on research-backed representation fit, exact semantic ledgers, source-grounded operational walkthroughs, deterministic composition tests, full CI, and independent HIGH_ASSURANCE review.

This note is explanatory evidence only. `design/LOSSLESS-RUNTIME-OPTIMIZATION.md` remains the durable methodology owner and `skill/` remains the normative runtime owner.
