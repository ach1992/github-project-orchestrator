# Refactored Runtime Live Delivery Evidence

Phase 7 does not rely only on synthetic traces. The refactored runtime was used to continue this repository through multiple consecutive phases with authoritative GitHub/CI evidence, including the independently reviewed Phase 8 release candidate:

| Phase | Pull request | Pre-merge validation | Integrated result | Work-item / delivery result |
|---|---|---|---|---|
| Phase 4 progressive routing | [#14](https://github.com/ach1992/github-project-orchestrator/pull/14) | Actions run `32080103271`: `success` on candidate `8a0e3e7dbe1e213e05fde9edd6c35606166d5cbd` | `7acf72b3506518f8b0e2400806e83a07fe2cc31a` | Issue #7 closed `completed` |
| Phase 5 scalable coordination | [#15](https://github.com/ach1992/github-project-orchestrator/pull/15) | Actions run `32081387397`: `success` on candidate `fb900d5d6104c5ddceb99ecb5d572e54d0f495dd` | `dd07064efac22b791bb97701bbcf58cba45c53fd` | Issue #8 closed `completed` |
| Phase 6 deterministic lint | [#16](https://github.com/ach1992/github-project-orchestrator/pull/16) | Actions run `32081781238`: `success` on candidate `b964b38b7f39f23a83430aff863194ca27c03c15` | `23cceca37ba0353db5336970893419083de3b00b` | Issue #9 closed `completed` |
| Phase 7 operational benchmark | [#17](https://github.com/ach1992/github-project-orchestrator/pull/17) | Actions run `32082485477`: `success` on candidate `4cbda36c7afc4dad752276b819ee28f11f5db67d` | `df5b3a43e29452716ec3aca9677462f8dd91742b` | Issue #10 closed `completed`; benchmark accepted with explicit simulation limits |
| Phase 8 stabilization / release candidate | [#18](https://github.com/ach1992/github-project-orchestrator/pull/18) | Actions run `32084966044`: `success` on independently reviewed candidate `2a91c12088e163c9224936b94767674688d8d57d` | squash merge `53182d5db086eef98ebaba757bb820b86e465845` with the same tree as the reviewed candidate | Issue #11 closed `completed`; public prerelease `v1.1.0-rc.1` delivered and post-release verified |

This evidence establishes that the refactored runtime has driven real repository work through implementation, CI-backed verification, integration, independent review, gated release, and authoritative work-item reconciliation without treating a PR update, tool batch, or completed phase as an artificial project stop.

The Phase 8 squash merge changed commit identity but preserved the exact reviewed tree, so the release source was content-equivalent to the independently reviewed candidate while the release publisher bound the public tag/artifacts to the actual `main` merge commit.

This file is still not an A/B baseline trial: the `v1.0.0` comparison remains the fixed source-grounded benchmark in this directory. Its purpose is to keep real delivery evidence alongside the policy simulation without turning historical execution into a second live status database.
