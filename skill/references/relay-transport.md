# Machine Relay Transport

Load this file only when the response includes a **MachineRelay**: a complete prompt or result intended for another agent/chat, including Worker dispatch/correction/handoff, independent-review prompt/result, or Master rotation/recovery bootstrap. The routed domain owns payload semantics; this file owns transport only and creates no lifecycle/state or second payload owner.

Render each MachineRelay as one self-contained copy/paste fenced block. User-facing explanation for the current user may appear before or after that block when useful, in the user's language. The destination agent/chat must need only the block itself; never put commentary meant only for the current user inside it or require surrounding prose to complete/reconstruct the relay.

Before send, require:

```text
MACHINE_RELAY_OUTPUT_OK(response) =
    exactly_one_complete_copy_target_fenced_block_for_the_relay(response)
    AND complete_domain_relay_inside_that_block(response)
    AND no_current_user_only_commentary_inside_relay_block(response)
    AND relay_is_self_sufficient_without_surrounding_prose(response)
    AND relay_prose_is_english_unless_explicit_language_override(response)
    AND identity-bearing_or_decision-relevant_literals_remain_exact_unless_safety_redaction_requires_otherwise(response)
    AND outer_fence_safely_contains_any_embedded_fences(response)
```

If false, repair before send. A separate copy-ready request is irrelevant. Surrounding explanation is optional and never part of the relay contract. Transport never weakens scope, authority, safety, evidence, review, integration, or release controls.
