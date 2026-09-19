# Machine Relay Transport

Load this file only when the user-visible output is a **MachineRelay**: a complete prompt or result intended for another agent/chat, including Worker dispatch/correction/handoff, independent-review prompt/result, or Master rotation/recovery bootstrap. The routed domain owns payload semantics; this file owns transport only and creates no lifecycle/state or second payload owner.

Every user-visible MachineRelay is automatically one copy/paste artifact. Before send, require:

```text
MACHINE_RELAY_OUTPUT_OK(response) =
    exactly_one_copy_target_fenced_block(response)
    AND complete_domain_relay_inside_that_block(response)
    AND no_visible_content_before_or_after_block(response)
    AND relay_prose_is_english_unless_explicit_language_override(response)
    AND identity-bearing_or_decision-relevant_literals_remain_exact_unless_safety_redaction_requires_otherwise(response)
    AND outer_fence_safely_contains_any_embedded_fences(response)
```

If false, repair before send. A separate copy-ready request is irrelevant. Direct non-relay user-facing explanation bypasses this predicate and remains in the user's language. Transport never weakens scope, authority, safety, evidence, review, integration, or release controls.
