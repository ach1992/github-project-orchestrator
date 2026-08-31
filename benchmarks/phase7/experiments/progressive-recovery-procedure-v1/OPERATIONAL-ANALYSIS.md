# Source-Grounded Operational Analysis

Experiment: `progressive-recovery-procedure-v1`  
Issue: #60

This analysis compares recovery decisions and context activation, not wording. No live model/API claim is made.

## Scenario 1 — Zero-chat recovery with sufficient downstream current truth

State:
- replacement Master has no prior chat;
- repository and current parent/child Issue state are authoritative and current;
- current PR/CI/dependencies are sufficient to identify the next executable action;
- no project-level contradiction exists.

Source decision:
- enter RECOVER;
- establish orientation and active-path state;
- do not reread the root project specification merely because chat is absent;
- stop recovery once the next action is decision-valid;
- continue the valid plan.

Candidate decision:
- Orientation spine establishes repository/workstream/outcome/operating dimensions and applies the root-spec trigger condition;
- Active-path context loads the current task/PR/CI/dependencies needed for the next action;
- final stopping rule ends recovery as soon as the decision-valid set is complete.

Result: same cold-recovery behavior with the progressive depth rule and required evidence expressed in one structure.

Protected anchors: `I`, `BY`.

## Scenario 2 — Root specification becomes materially relevant

State:
- current downstream Issue/docs do not safely establish project-level intent, or a material contradiction/change affects the project-level outcome.

Source decision:
- root specification is now decision-relevant and may be loaded;
- do not load unrelated history merely for completeness.

Candidate decision:
- Orientation spine states the root-spec condition explicitly;
- Triggered depth owns broader/root-spec loading when the material trigger exists.

Result: same trigger; no eager root-spec dependency is introduced.

Protected anchor: `BY`.

## Scenario 3 — Planned branch/worktree transition after valid recovery baseline

State:
- recovery baseline is already decision-valid;
- Master creates/switches to the intended isolated branch/worktree;
- no material repository/authority/state drift occurred.

Source decision from unchanged later §2:
- do not rerun the full recovery sequence;
- verify only intended branch/base/HEAD/target/dirty-state identities as needed, then resume.

Candidate effect:
- the later rule is outside the replacement and remains byte-identical.

Result: same delta-recovery behavior. The progressive table governs cold recovery only; it does not become a mandatory per-transition ritual.

Protected anchor: `BG`.

## Scenario 4 — Preferred GitHub/tool route fails after baseline

State:
- repository/outcome baseline is valid;
- one preferred route fails;
- an equivalent authoritative route exists.

Source decision from unchanged later §2:
- update transient capability knowledge;
- use the equivalent authoritative route;
- do not restart repository-wide recovery.

Candidate effect:
- later route-failure rule remains byte-identical.

Result: no new recovery churn.

Protected anchor: `BG`.

## Scenario 5 — Material drift invalidates baseline

State:
- new evidence materially changes repository/target identity, authority/access, architecture/interface assumption, risk, ownership boundary, or release constraint needed for the next decision.

Source decision from unchanged later §2:
- reconcile the affected workstream/critical-path slice first;
- widen only when impact crosses that boundary.

Candidate effect:
- later material-drift rule remains byte-identical;
- Triggered depth is consistent with that bounded widening.

Result: same event-driven recovery expansion rather than either stale continuation or broad default reload.

Protected anchor: `BH`.

## Scenario 6 — Multi-repository outcome

State:
- accepted outcome spans several repositories with cross-repository interfaces/release ordering;
- only one local repository is currently on the critical path.

Source decision from unchanged later §2:
- recover small global coordination spine first;
- then enter only local repository contexts on active critical path;
- local Issues/PRs/CI/rules remain authoritative.

Candidate effect:
- the entire multi-repository rule is beyond the replacement boundary and byte-identical.

Result: same global-to-local progressive behavior.

Protected anchor: `I`.

## Scenario 7 — Large long-lived repository

State:
- repository has extensive historical/project state;
- current critical path is narrow.

Source decision:
- large/long-lived repository is a reason to narrow by workstream, not read more;
- stop when decision-valid state for the next action is established.

Candidate decision:
- final stopping paragraph preserves both rules directly.

Result: same anti-overload behavior with a single recovery representation.

Protected anchors: `I`, `BY`.

## Scenario 8 — Authority/profile recovery across rotation

State:
- replacement Master must recover ProjectAuthority, CoordinationBaseline, affected-chain AssuranceLevel, and a current ScopedAuthorization.

Source decision:
- recover these dimensions independently;
- do not reconstruct CoordinationBaseline from AssuranceLevel/risk/project size/access;
- legacy HIGH_ASSURANCE without baseline remains ambiguous until authoritative evidence resolves it.

Candidate decision/effect:
- Orientation spine explicitly recovers the independent current dimensions;
- the detailed legacy/non-implication paragraph remains byte-identical after the replacement boundary.

Result: same authority/profile semantics.

Protected anchor: `AH`.

## Maintenance/locality assessment

The original prefix asks the model to map an eight-step evidence sequence onto a second three-layer retrieval model immediately afterward. Neither representation is wrong, but their overlap creates a second organization to reconcile.

The candidate gives progressive disclosure one canonical structure and embeds every required cold-recovery evidence class in the appropriate layer. The decision-valid stop rule is local to the structure, while specialized later safeguards remain untouched.

Potential cost:
- table cells are denser than the original three bullets;
- the original eight numbered steps provided a visually obvious linear checklist.

Mitigation:
- rows are context-depth layers rather than pseudo-states;
- each row groups only evidence with the same activation depth;
- exact stop criteria remain outside the table and explicit;
- detailed delta/multi-repo/legacy/preflight safeguards stay as prose because they are conditional nuance, not part of the core three-layer mapping.

Assessment: the candidate reduces duplicate recovery representation without flattening conditional nuance. It is preferable to KEEP if deterministic isolation and semantic review remain green.
