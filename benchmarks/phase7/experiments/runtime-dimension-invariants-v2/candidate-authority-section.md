## 1. Decision dimensions

Use the current `Role`, `ProjectAuthority`, `ScopedAuthorization`, `CoordinationBaseline`, `AssuranceLevel`, and `RiskLevel` established in `SKILL.md` as independent inputs to gate evaluation. This domain does not reclassify those dimensions; it applies current action effects, obligations, repository/platform policy, and gate evidence.

Repository/platform permissions still apply. When explicit user or higher-level authorization changes the permitted project envelope, scope the change only to what it clearly grants. An exact one-off instruction/approval is `ScopedAuthorization`: it may satisfy only the applicable gate for that action without converting the broader project to a more permissive `ProjectAuthority`.

Use the lightest safe controls. Importance alone does not make risk high; consider blast radius, reversibility, security/data impact, compatibility, and production consequences.
