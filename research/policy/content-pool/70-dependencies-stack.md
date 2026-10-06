# Dependencies & Technology Stack

> Shared normalized content pool. Research artifact, not a runtime candidate file.
> Each policy ID must map to exactly one runtime normative owner in every experimental candidate.

Dependency governance and approved/default technology choices.

## DEP-001 — Dependencies require current need

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** common
- **Source:** `templates/v2-baseline/.claude/rules/dependencies.md#General Principle`

Add a dependency only for a concrete current requirement; do not install packages for hypothetical future use.

## DEP-002 — Approved technology is not silently replaced

- **Origin:** v2
- **Strength:** MUST_NOT
- **Trigger class:** always
- **Scope:** common
- **Source:** `templates/v2-baseline/.claude/rules/dependencies.md#General Principle`, `templates/v2-baseline/.claude/skills/project-structure/references/technology-stack.md`

When the template/project has an approved technology, use it rather than silently selecting an alternative; consequential replacement requires approval.

## DEP-003 — Choose latest stable compatible version

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** workflow
- **Scope:** common
- **Source:** `templates/v2-baseline/.claude/rules/dependencies.md#Version Selection`

For NuGet/npm additions or updates, verify the current latest stable compatible version from the registry; avoid prerelease and floating versions unless explicitly requested.

## DEP-004 — Dependency due diligence

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** workflow
- **Scope:** common
- **Source:** `templates/v2-baseline/.claude/rules/dependencies.md#Version Selection`

Before installation, check deprecation, known vulnerabilities and the exact selected version's license.

## DEP-005 — Commercial/risky licenses require approval

- **Origin:** v2
- **Strength:** REQUIRES_APPROVAL
- **Trigger class:** workflow
- **Scope:** common
- **Source:** `templates/v2-baseline/.claude/rules/dependencies.md#Paid or Commercial Dependencies`

Do not automatically install paid/commercial or materially restrictive/unclear-license dependencies; explain the concern and reasonable alternatives without silently substituting.

## DEP-006 — Central Package Management

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/dependencies.md#NuGet`

Use NuGet Central Package Management; versions belong in Directory.Packages.props and project PackageReference entries are normally versionless and narrowly scoped.

## DEP-007 — npm lockfile and dependency category

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** frontend
- **Source:** `templates/v2-baseline/.claude/rules/dependencies.md#npm`

Use npm by default unless deliberately changed, keep package-lock consistent, and place build/test tooling in the appropriate dependency category.

## DEP-008 — Default backend platform

- **Origin:** v2
- **Strength:** DECIDED
- **Trigger class:** always
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/project-structure/references/technology-stack.md#Backend Platform`

Default platform is .NET 10 LTS, C# 14, ASP.NET Core and ASP.NET Core Controllers; do not move to preview/RC without approval.

## DEP-009 — Default persistence stack

- **Origin:** v2
- **Strength:** DECIDED
- **Trigger class:** always
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/project-structure/references/technology-stack.md#Persistence`

Default persistence is EF Core with Microsoft SQL Server/SqlServer provider; provider-specific concerns stay out of Application and Domain.

## DEP-010 — Default validation/logging

- **Origin:** v2
- **Strength:** DECIDED
- **Trigger class:** always
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/project-structure/references/technology-stack.md#Validation`

FluentValidation is the standard explicit request/use-case validation library; application logging uses ILogger<T> with Serilog as provider.

## DEP-011 — Conditional mapping/resilience

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** always
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/project-structure/references/technology-stack.md#Mapping`

Manual mapping is fine for simple cases; Mapster is approved when mapping volume warrants it. Microsoft resilience packages are approved only when real integrations need resilience.

## DEP-012 — Swagger baseline

- **Origin:** v2
- **Strength:** DECIDED
- **Trigger class:** always
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/project-structure/references/technology-stack.md#API Documentation and Interactive Testing`

Use Swashbuckle Swagger UI as the default Development interactive API documentation/testing surface; expose outside Development only when requirements justify it.

## DEP-013 — Backend testing stack/layout

- **Origin:** v2
- **Strength:** DECIDED
- **Trigger class:** always
- **Scope:** backend-tests
- **Source:** `templates/v2-baseline/.claude/skills/project-structure/references/technology-stack.md#Testing`

Use NUnit; backend test projects live under backend alongside production projects; WebApplicationFactory is the baseline for ASP.NET Core integration tests; Testcontainers is conditional.

## DEP-014 — Angular baseline stack

- **Origin:** v2
- **Strength:** DECIDED
- **Trigger class:** always
- **Scope:** frontend
- **Source:** `templates/v2-baseline/.claude/skills/project-structure/references/technology-stack.md#Angular Frontend`

Use current stable Angular with compatible TypeScript/RxJS, standalone APIs, strict mode, routing, zoneless mode when supported, SCSS, Angular Material/CDK and Vitest.

## DEP-015 — Avoid overlapping Angular libraries by default

- **Origin:** v2
- **Strength:** MUST_NOT
- **Trigger class:** always
- **Scope:** frontend
- **Source:** `templates/v2-baseline/.claude/skills/project-structure/references/technology-stack.md#Angular Libraries`

Do not add NgRx, Axios, Lodash, Bootstrap, Tailwind, extra form/component/state libraries by default; use built-in Angular capabilities first and add extras only for concrete needs.

## DEP-016 — Conditional E2E

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** always
- **Scope:** frontend
- **Source:** `templates/v2-baseline/.claude/skills/project-structure/references/technology-stack.md#Angular Libraries`

Playwright is the approved default when frontend E2E coverage is required, but it is not part of the minimal baseline scaffold.
