# Interface Specialist Composition

Canonical owner for composing GitHub Project Orchestrator with an optional interface-decision specialist. The current reference contract is **Product Interface Designer v0.2.1** at immutable release commit `7aeef3475f160a000e0ec9ab1a6618b41d63f70a`. Keep the invocation mechanism provider-neutral and do not copy or import the specialist's runtime rulebook into this Skill.

## 1. Activate only when specialist judgment is material

Consult a compatible interface specialist only when accepted project work contains a **material interface decision, material interface creation/redesign, user-facing quality decision, or interface review** and specialist judgment can materially improve the result.

Materiality can come from unresolved hierarchy/interaction/visual/UX intent, durable cross-surface design impact, meaningful responsive/adaptive/accessibility/locale presentation choices, user consequence, or an interface review whose findings can change accepted implementation. Size or the mere presence of frontend code is not enough.

Do not consult merely because work touches a frontend/UI, for trivial/local edits, for direct implementation of an already-resolved interface decision, or for unrelated backend/infrastructure/data/deployment work. Do not re-ask a question already settled by current authoritative product/design truth.

## 2. Pass only decision-relevant context

Provide the smallest context that can materially change the active interface decision/review:

| Context | Minimum content |
|---|---|
| accepted outcome | user/product outcome plus the exact interface question or review target |
| authoritative truth | relevant product/business rules, terminology, existing interface/design-system truth, and constraints that must survive |
| target context | platform/surface and active language/direction/locale when material |
| evidence | relevant source/rendered artifacts plus material evidence limitations |
| ownership boundary | GitHub Project Orchestrator retains project/repository/integration/release authority; identify any separate platform/implementation owner when relevant |

Do not pass full project history, unrelated repository state, or a duplicate project brief merely because the specialist is available.

## 3. Consume one bounded interface-decision packet

The specialist returns the smallest packet needed for execution:

| Field | Required content |
|---|---|
| **Intent** | user-facing outcome the interface must preserve |
| **Decision** | concrete hierarchy/interaction/visual/UX decision or review conclusion |
| **Constraints** | only material mandatory/product/platform/locale/interface constraints |
| **Implementation latitude** | what the implementation owner may vary without changing intended experience |
| **Evidence** | product/source/rendered/measured/user-task evidence actually used plus material limitations |
| **Open assumptions** | unresolved material facts/decisions another owner must resolve |

Treat this as interface decision input, not as a project plan, repository plan, platform mechanism, integration decision, or release plan. Do not add parallel packet fields locally unless a future accepted contract revision requires them.

## 4. Retain ownership and return control immediately

GitHub Project Orchestrator retains accepted scope/priority, dependencies, repository mutation authority, implementation orchestration, CI/validation coordination, integration, release/deployment, and continuity. The interface specialist owns only the active interface decision/review. There is **no nested Master** and no authority transfer.

After the packet is returned, control returns immediately to GitHub Project Orchestrator or its assigned implementation/platform owner. A Worker or platform owner may use the packet as implementation input but does not inherit broader authority from the specialist.

A returned packet does not itself trigger another specialist call. Correct issues that remain inside **Implementation latitude** locally. Re-consult only when current evidence introduces a genuinely new material interface question or when accepted work/current evidence makes a distinct material interface review necessary. This prevents automatic back-and-forth loops while preserving useful review when evidence changes.

If a Worker encounters a new material interface decision outside its current packet/Task Contract, use the existing Worker stop/contract-revision path and return the decision to the Master; do not widen Worker scope or create a direct specialist-coordination loop.

## 5. Split shared concerns without duplicate authority

When the specialist is active, it owns user-facing interface intent/critique for the active question. `engineering-quality.md` remains complementary for engineering realization/evidence such as implementation correctness, performance/capacity, system safety, validation, and other material engineering concerns. A platform specialist/implementation owner remains responsible for realizing the interface safely in its platform mechanism.

When the interface specialist is unavailable or not invoked, continue from current authoritative product/design truth and the existing proportional `engineering-quality.md` user-facing guidance. Specialist unavailability alone is not a Master stop. Do not claim specialist review occurred, invent a decision packet, or grow this fallback into a copied generic UI/UX rulebook.
