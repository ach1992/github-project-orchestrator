# Interface Specialist Composition

Caller-side contract for composing GitHub Project Orchestrator with an optional interface-decision specialist. Compatibility was validated against **Product Interface Designer v0.2.1** at `7aeef3475f160a000e0ec9ab1a6618b41d63f70a`; this is contract evidence, not a runtime version pin. Keep invocation provider-neutral and do not copy the specialist's design rulebook into this Skill.

## 1. Consultation gate

Consult a compatible interface specialist only when **all** are true:

1. accepted work has a user-facing interface surface;
2. current authoritative product/design truth plus any existing decision packet still leaves an unresolved interface judgment or distinct user-facing critique;
3. specialist judgment could materially change the intended user experience.

Relevant judgment can include hierarchy, interaction, visual direction, responsive/adaptive intent, user-facing accessibility/UX intent, locale presentation, or material interface critique. Frontend/UI code alone, trivial/local presentation edits, implementation inside already-returned implementation latitude, or settled interface truth are not triggers.

Material interface impact alone is neither `MasterBoundary.MATERIAL_DECISION_REQUIRED` nor an approval or Master code/integration-review trigger. Load `authority-gates.md` or `review-integration.md` only when their own triggers independently apply.

## 2. Exchange contract

Request interface decision/critique only; do not implicitly delegate repository mutation or implementation. Send only the accepted outcome and exact interface question/critique target, relevant authoritative product/business/design truth and constraints, target platform/surface and active language/direction/locale when material, relevant source/artifact/rendered evidence and limitations, and the ownership boundary. Do not send full project history or unrelated repository state.

Expect the compatible interface specialist's canonical interface-decision packet. The specialist contract exclusively owns its schema and field semantics; this Skill consumes the returned packet only as bounded interface-decision input. Preserve the implementation latitude it returns, and route unresolved assumptions to their existing owners instead of inventing answers.

Treat the packet as interface-decision input, never as project priority, repository plan, platform mechanism, integration decision, or release plan.

## 3. Ownership and return control

GitHub Project Orchestrator retains accepted scope/priority, dependencies, repository mutation authority, implementation orchestration, CI/validation coordination, integration, release/deployment, and continuity. The implementation/platform owner retains platform mechanism. The interface specialist owns only the active interface intent/critique. There is no nested Master or authority transfer.

After a returned packet, control returns immediately to GitHub Project Orchestrator or its assigned implementation/platform owner. Work inside the returned implementation latitude continues locally; the packet never triggers another specialist call by itself. Re-consult only when new evidence creates a genuinely new unresolved interface judgment or justifies a distinct user-facing critique.

If a Worker encounters an interface question outside its current packet/Task Contract and cannot resolve it inside existing latitude, use the existing Worker status/contract-revision path; do not widen Worker scope or create a direct specialist loop.

## 4. Fallback

If specialist consultation is unavailable or not triggered, continue from current authoritative product/design truth and ordinary bounded engineering judgment; `engineering-quality.md` remains the owner for material engineering realization/evidence. Specialist unavailability alone is not a Master stop. Independently unresolved product/business/security/privacy/legal/platform decisions still follow their existing owners and gates.
