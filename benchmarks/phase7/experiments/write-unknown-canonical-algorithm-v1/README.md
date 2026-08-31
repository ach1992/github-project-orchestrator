# WriteState.UNKNOWN Canonical-Algorithm Prototype

Tracking: #58  
Parent: #37  
Methodology: `design/LOSSLESS-RUNTIME-OPTIMIZATION.md`

## Hypothesis

`authority-gates.md` §6 currently renders the same safety-critical recovery policy twice: first as a compressed symbolic flow, then as the actual guarded numbered algorithm. Because sequence and branch guards are semantic, one canonical ordered algorithm should reduce duplicate reconstruction and maintenance risk without losing the useful retrieval cues.

This is a Phase B representation prototype only. It does **not** modify canonical `skill/` runtime and does not claim live-model performance improvement.

## Frozen identities

- source/current-target snapshot: `f161c1b3d30b148b0418c585531dfbeaf7ffec04`
- immutable semantic comparison baseline: `f98e8a242c720931e34aa7c4e8a799090e3d0495`
- target owner: `skill/references/authority-gates.md` §6
- candidate fragment: `candidate-write-unknown.md`

## Representation fit versus KEEP

The source semantics are an ordered recovery algorithm with guarded branches, not nuanced free-form judgment. The current numbered list already carries the authoritative detail; the preceding symbolic flow duplicates it in a second notation and compresses safety-critical distinctions such as proven absence versus incomplete discovery.

Candidate strategy:

- remove the duplicate symbolic rendering;
- keep one numbered algorithm as canonical;
- make the three authoritative re-read outcomes (`present`, `proven absent`, `incomplete/unknown`) explicit inside that algorithm;
- keep independent-work continuation and the sole/project-wide terminal-boundary condition explicit;
- keep the scope/application note outside the algorithm.

`KEEP` would be preferable if the symbolic line supplied unique semantic or retrieval value. The one-to-one ledger below found no unique source semantic owned only by that line; every protected behavior is carried by the detailed algorithm and scope note.

## One-to-one semantic ledger

| Source semantic | Candidate owner |
|---|---|
| ambiguous outcome affects the individual mutation | step 1 |
| mark it `WriteState.UNKNOWN` | step 1 |
| no blind retry | step 1 |
| local unknown does not automatically stop Master | step 1 + step 6 |
| authoritative re-read uses stable identity/semantic equivalence | step 2 |
| decision-scoped completeness must distinguish present/absent/unknown | step 2 |
| present -> verify, mark known, continue | step 3 |
| retry requires authoritative proof of absence | step 4 |
| retry at most once | step 4 |
| retry requires idempotency or stable correlation/dedup protection | step 4 |
| unsafe retry -> freeze dependent mutation + continue independent work | step 4 |
| incomplete/truncated/unknown is never absence | step 5 |
| incomplete discovery never authorizes retry | step 5 |
| incomplete discovery -> freeze dependent mutation + continue independent work | step 5 |
| unresolved after safe retry/no-safe-retry remains UNKNOWN | step 6 |
| independent safe work continues while local unknown remains | steps 4–6 |
| `MasterBoundary.WRITE_OUTCOME_UNKNOWN` only when sole/project-wide controlling blocker | step 6 |
| applies to Issue/PR creation, comments, labels, Project updates, pushes, releases, deployment triggers, other non-idempotent writes | scope note |

No retry count, state, boundary, authority rule, or completion condition is added or removed.

## Scope proof

The deterministic test must require:

- only §6 is replaced in a materialized candidate;
- all bytes before §6 and from `## 7. Optimistic concurrency` onward remain unchanged;
- every non-target runtime file remains byte-identical;
- runtime state/boundary token surface remains unchanged;
- the duplicate symbolic flow is absent from the candidate;
- all protected semantic fragments remain present;
- the materialized Skill passes normal validation;
- ledger and operational walkthrough evidence are present.

Token/word reduction is diagnostic only; selection rests on single ownership, branch clarity, and lossless semantics.

## Selection boundary

Select for later #38 migration only if deterministic evidence and source-grounded review confirm that one guarded algorithm is strictly easier to maintain/apply without weakening the safety-critical unknown-write distinctions. Otherwise choose `KEEP`.
