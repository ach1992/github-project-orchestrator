# Machine Relay Transport

Load only when the response includes a **MachineRelay** intended for another agent/chat. Domain references own payload semantics; this file owns transport.

Render each relay as exactly one self-contained fenced copy block. The block contains only destination-facing content and must be sufficient by itself. Explanation for the current user may appear outside it, in the user's language.

```text
MACHINE_RELAY_OUTPUT_OK(relay) =
    one_complete_fenced_copy_block(relay)
    AND no_current_user_only_text_inside(relay)
    AND self_sufficient_without_surrounding_prose(relay)
    AND english_unless_explicitly_overridden(relay)
    AND exact_identity_or_decision_literals_unless_safety_redaction_requires_otherwise(relay)
    AND safe_outer_fence_for_embedded_fences(relay)
```

If false, repair before send. Surrounding explanation is optional and never part of the relay. Transport never weakens domain authority, safety, evidence, review, integration, or release rules.
