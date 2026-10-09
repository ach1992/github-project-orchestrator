# Machine Relay Transport

Load only when the response includes a **MachineRelay** intended for another agent/chat. Domain references own payload semantics; this file owns transport.

Render each relay as exactly one self-contained fenced copy block. Current-user explanation may appear outside it.

Before sending, verify all four:

1. the block contains the complete relay and no current-user-only text;
2. the destination can act from the block alone, without surrounding prose;
3. use English unless explicitly overridden, and preserve exact repository/object/SHA/decision literals unless safety redaction requires otherwise;
4. the outer fence safely contains any embedded fences.

Do not send the relay until every check passes. Transport never weakens domain authority, safety, evidence, review, integration, or release rules.
