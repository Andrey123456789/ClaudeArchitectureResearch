> Instruction map (human-facing; never auto-loaded) | Owns: navigation of the instruction system | Maintained by: `/template-maintenance` | Validated by: `node .claude/scripts/check-instructions.cjs`

# Instruction Map

## How the System Is Organized

Instructions are organized **by stability**. Ask: *how fundamental and stable is
this rule?*

```text
0 Core  ←  1 Architecture  ←  2 Technology  ←  3 Project
(most stable)                                 (most volatile)
```

- A **conformance dependency** (header field `Depends on:`) may point only to
  the same or a more stable level: Project → Technology → Architecture → Core.
- A **routing pointer** (`→ run X`, `→ see Y`) is not a dependency and may point
  anywhere.
- Levels 0 and 1 never name concrete technologies (only .NET, C#, TypeScript);
  technology bindings live at Level 2, project selections at Level 3.
- **Level does not decide loading.** Each level mixes always-loaded content,
  path-scoped rules, workflows, and knowledge skills.
- Product inputs (`SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, feature specs, task
  prompts) sit **outside** the levels; they can request a decision change but
  never override engineering policy.

Every file starts with a one-line header:
`> Level: <n> <Name> | Owns: … | Scope: … | Loads: … | Depends on: …`.
Paths below are relative to `.claude/` unless they start at the repository root.

Loading legend: **always** = CLAUDE.md or imported by it; **path** = rule loaded
when a file matching its `paths` is read; **workflow** = skill invoked for a
procedure (workflows read rules explicitly when path triggers may not have
fired); **knowledge** = skill loaded on demand by description; **private** =
read only by its owning skill; **user-only** = invoked only by the user.

## Level 0 — Core

| File | Owns (authoritative) | Scope | Loading | Enforcement | Add here when… |
|---|---|---|---|---|---|
| `CLAUDE.md` (repository root) | Normative vocabulary; precedence; product governance (specification authority, no invented behavior, ambiguity approval, delegated internals, string semantics, settings ownership, spec/settings conflict, no invented tunables, settings exclusions); scope and simplicity (focused scope, proportional simplicity, no speculative frameworks); challenge obligation; decision control (classes, Reserved list, five-question test, headless rule); version-control safety (no unrequested repository changes, parallel isolation); work routing | common | always | post-edit hook (spec/settings reminders) | the rule is technology-neutral and needed at planning time |
| `rules/0-core/security-principles.md` | Secrets in source; secret mechanisms; untrusted input; upload metadata; parameterized SQL; server authorization; deliberate anonymous access; token validation; enumeration-safe auth errors; TLS and certificate validation; no custom cryptography; CORS; CSRF with cookies; token storage; fail-safe checks; visible security-configuration failure | common, backend, frontend | path | — | a security invariant names no technology |
| `rules/0-core/logging-principles.md` | Never-log list and PII; no arbitrary payload logging | common | path | — | a logging-content rule names no technology |
| `rules/0-core/dependency-hygiene.md` | Dependencies only for current need | common | path | dependency-guard hook | a dependency-necessity rule |
| `rules/0-core/structure-principles.md` | Physical structure follows real responsibilities (no speculative projects, empty trees, Common/Helpers/Utils) | common | path | — | a repository-shape rule names no layout |
| `rules/0-core/testing-principles.md` | Narrowest useful test level; behavior over implementation; determinism and isolation; tests own data; provider fidelity; explicit cases; no coverage chasing; descriptive names | backend-tests | path | stop hook (tests reminder) | a test principle is framework-neutral |
| `rules/0-core/error-exposure.md` | No internals in public errors; client cancellation is not a server failure | backend | path | — | a public-failure rule names no framework |
| `rules/0-core/health-principles.md` | Cheap deterministic health checks; liveness vs. readiness; safe public health output | backend | path | — | a health semantics rule names no framework |
| `rules/0-core/performance-principles.md` | Correctness before optimization; efficient database access; evidence for advanced optimizations | backend | path | — | a performance principle |
| `rules/0-core/caching-principles.md` | Caching needs a reason; safe keys; invalidation after committed mutations; explicit lifetimes | backend | path | — | a cache-correctness principle |
| `rules/0-core/integration-principles.md` | Bounded outbound time; safe retries; Retry-After; acceptable fallback; caller cancellation is not transient | backend | path | — | an outbound-call principle |
| `skills/custom-settings/SKILL.md` | Settings synchronization across surfaces; schema-affecting settings co-change | common | workflow | post-edit and stop hooks route here | a settings-sync step |
| `skills/architecture-decision/SKILL.md` | Decision Request procedure and format; recording accepted decisions | common | workflow | — | a decision-procedure step |
| `skills/template-maintenance/SKILL.md` | Changing the instruction system; level assignment; extension guidance | repo/meta | user-only | check-instructions | a maintenance step |

## Level 1 — Architecture

| File | Owns (authoritative) | Scope | Loading | Enforcement | Add here when… |
|---|---|---|---|---|---|
| `rules/1-architecture/overview.md` | Adopted architecture; CQRS/mediator/VSA not adopted; consequential architecture gate; accepted architecture decisions | common | always (imported) | dependency policy (mediator packages) | an architecture decision is needed at planning time |
| `rules/1-architecture/backend-layers.md` | Inward dependencies; test-project reference breadth; Domain independence; simple domain default; rich domain needs approval; no decorative DDD; Application Services orchestrate; Application owns abstractions; no framework/transport types in Application; cache and remote-HTTP adapter boundaries; composition root; registration per layer | backend, backend-tests | path | check-manifests (reference direction) | a rule presupposes the layers |
| `rules/1-architecture/persistence-boundary.md` | Specific repositories; no query leakage; generic repository Infrastructure-only; Unit of Work commit boundary; shared context, no repository container; explicit transactions only for need | backend | path | — | a repository/UoW rule |
| `rules/1-architecture/entry-points.md` | Thin entry points; no business/persistence in entry points; HTTP semantics in Api; no gratuitous DTO duplication; no per-version inner models; success statuses; empty collections; 401/403; 409/412; versioning only for need; breaking changes; one versioning strategy; documentation matches runtime | backend | path | — | an HTTP entry-point rule |
| `rules/1-architecture/outcomes.md` | Expected outcomes, no forced Result, no HTTP-named categories; exceptions not branch control; centralized unexpected failures; log once; validation boundaries | backend | path | — | an outcome or exception-flow rule |
| `rules/1-architecture/frontend-structure.md` | Focused presentation; explicit HTTP boundary; feature-oriented structure; simple state first; documented error contract; frontend validation is UX | frontend | path | — | a frontend structural rule names no framework |

## Level 2 — Technology

| File | Owns (authoritative) | Scope | Loading | Enforcement | Add here when… |
|---|---|---|---|---|---|
| `rules/2-technology/csharp.md` | Follow conventions/.editorconfig; no unrelated style rewrites; file, namespace, Async naming | backend | path | `.editorconfig` | a C# convention |
| `rules/2-technology/dotnet-runtime.md` | Async without blocking; CancellationToken propagation; TimeProvider; HttpClient lifetime; constructor injection; valid DI lifetimes; typed validated options | backend | path | — | a .NET runtime rule |
| `rules/2-technology/aspnet-core.md` | ProblemDetails/ValidationProblemDetails contracts; Swagger UI environment exposure; Identity over custom auth security; bindings (Controllers, transport types, IExceptionHandler, authorization attributes, Data Protection scope) | backend | path | — | an ASP.NET Core rule or binding |
| `rules/2-technology/ef-core.md` | EF Core is an Infrastructure detail; bindings (persistence-framework types, scoped context, DbContext as boundary) | backend | path | — | an EF Core rule or binding |
| `rules/2-technology/backend-testing.md` | NUnit default, no second framework; WebApplicationFactory integration tests; bindings (InMemory fidelity, Testcontainers, FakeTimeProvider) | backend-tests | path | — | a test-technology rule |
| `rules/2-technology/logging.md` | ILogger structured templates; Serilog AddSerilog integration | backend | path | dependency policy (deprecated sinks) | a logging-technology rule |
| `rules/2-technology/package-management.md` | NuGet Central Package Management; npm lockfile and dependency categories | backend, frontend | path (manifests) | check-manifests, `Directory.Packages.props` | a package-manager rule |
| `rules/2-technology/angular.md` | Standalone APIs and feature organization; Signals vs. RxJS; lazy routes; functional interceptors; no nested subscriptions; subscription lifetime; bindings (HttpClient services, guards, reactive forms) | frontend | path | — | an Angular rule |
| `rules/2-technology/containers.md` | Production runtime image; no root to bypass permissions | backend, delivery | path (container files) | — | a container rule |
| `skills/ef-core/SKILL.md` | technique | backend | knowledge | — | EF Core examples/depth |
| `skills/http-api/SKILL.md` | technique | backend | knowledge | — | status-code depth |
| `skills/aspnet-error-handling/SKILL.md` | technique | backend | knowledge | — | error-handling examples |
| `skills/dotnet-testing/SKILL.md` | technique | backend-tests | knowledge | — | test examples |
| `skills/logging/SKILL.md` + `skills/logging/references/serilog.md` (private) | technique | backend | knowledge | — | logging and Serilog depth |
| `skills/httpclient-factory/SKILL.md` + `skills/httpclient-factory/references/resilience.md` (private) | technique | backend | knowledge | — | outbound HTTP and resilience depth |
| `skills/configuration/SKILL.md` | technique | backend | knowledge | — | options/secrets examples |
| `skills/dependency-injection/SKILL.md` | technique | backend | knowledge | — | DI examples |
| `skills/caching/SKILL.md` | technique | backend | knowledge | — | caching examples |
| `skills/swagger/SKILL.md` | technique | backend | knowledge | — | Swagger examples |
| `skills/api-versioning/SKILL.md` | technique | backend | knowledge | — | versioning examples |
| `skills/health-check/SKILL.md` | technique | backend | knowledge | — | health examples |
| `skills/docker/SKILL.md` | technique | delivery, backend | knowledge | — | container examples |
| `skills/ci-cd/SKILL.md` | technique | delivery | knowledge | — | pipeline examples |
| `skills/angular/SKILL.md` | technique | frontend | knowledge | — | Angular examples |
| `skills/modern-csharp/SKILL.md` | technique | backend | knowledge | — | language-feature examples |
| `skills/authentication/SKILL.md` | technique | backend, frontend | knowledge | — | auth examples |

## Level 3 — Project

| File | Owns (authoritative) | Scope | Loading | Enforcement | Add here when… |
|---|---|---|---|---|---|
| `rules/3-project/decisions.md` | Approved technology not silently replaced; platform; persistence; validation and logging; Swagger baseline; backend test stack and placement; Angular baseline; conditional mapping/resilience/E2E/versioning; no overlapping Angular libraries; Docker optional; mediator libraries; `.slnx`; repository-level build files; layout; accepted project decisions | common | always (imported) | check-manifests + `scripts/dependency-policy.json` | a project selection or default is needed at planning time |
| `rules/3-project/data-lifecycle.md` | Usable non-secret Development connection; representative seed data; seeding in Infrastructure; dedicated internal seeder; Development-only seeding; seeder never migrates; no auto-sync of existing data; seed validity | backend | path | stop hook (seed reminder) | a development-data rule |
| `skills/develop/SKILL.md` | Read the specification first; inspect code and apply rules; greenfield rule reads; durable-source sync; seeder co-change; migration review; regression tests; performance changes; API deprecation; CI truthfulness; frontend CI commands; production migrations; review before verify; verify before completion | common | workflow | stop hook | a step of the implementation procedure |
| `skills/verify/SKILL.md` | Final diff and scope; builds; relevant tests; probe preservation; runtime smoke; risk-scoped checks; using cleanup in changed C# files; fix-and-retry; honest reporting | common | workflow | — | a verification step |
| `skills/code-review/SKILL.md` | Review procedure; defect-first priorities; no manufactured findings; output | common | workflow | — | a review step |
| `agents/code-reviewer.md` | Independent read-only review delegated to `code-review` | common | agent | read-only tool restriction | — (keep thin) |
| `skills/build-fix/SKILL.md` | Reproduce and diagnose; bounded iterations; no weakened verification; regenerate generated output | common | workflow | — | a repair step |
| `skills/add-dependency/SKILL.md` | Latest stable compatible version; due diligence; license approval; versioning/resilience packages; npm peer conflicts | common | workflow | dependency-guard hook | a dependency procedure step |
| `skills/security-scan/SKILL.md` + `skills/security-scan/references/scan-layers.md` (private) | Evidence and contextual severity; tool independence; scan procedure | common | workflow | — | a security-review step |
| `skills/project-structure/SKILL.md` + `skills/project-structure/references/solution-layout.md`, `skills/project-structure/references/backend-layout.md`, `skills/project-structure/references/technology-stack.md` (private) | Scaffolding and restructuring procedure | common | workflow | dependency-guard hook (references) | a scaffolding step |
| `skills/git-workflow/SKILL.md` | Never discard user work; state-aware minimal operations; focused staging | repo/meta | workflow | — | a Git procedure step |

## Split Statements

Mixed statements are split so each part sits at the level of its most volatile
dependency:

| Stable part (owner) | Volatile part (binding) |
|---|---|
| Domain is independent of persistence and web frameworks (`backend-layers.md`) | EF Core / ASP.NET Core are those frameworks (`ef-core.md`, `aspnet-core.md`) |
| Application uses no framework or transport types; repository contracts expose no persistence types (`backend-layers.md`, `persistence-boundary.md`) | `DbContext`, `DbSet<T>`, EF expressions, provider types, `IActionResult`, `HttpContext` (`ef-core.md`, `aspnet-core.md`) |
| Thin HTTP entry points (`entry-points.md`) | Controllers are the entry points (`aspnet-core.md`; selection in `decisions.md`) |
| Centralized unexpected failures (`outcomes.md`) | `IExceptionHandler` (`aspnet-core.md`) |
| Validation boundaries (`outcomes.md`) | FluentValidation selection (`decisions.md`) |
| No custom cryptography (`security-principles.md`) | Data Protection is not database encryption (`aspnet-core.md`) |
| Server authorization; guards are UX (`security-principles.md`) | Angular guards, reactive forms, HttpClient services (`angular.md`) |
| Provider fidelity in tests (`testing-principles.md`) | InMemory is not SQL Server fidelity; Testcontainers optional (`backend-testing.md`) |
| Not-adopted patterns and architecture gate (`overview.md`) | MediatR/Kommand are mediator libraries; DbContext as persistence boundary (`decisions.md`, `ef-core.md`) |
| Swagger UI as Development surface (`decisions.md`) | Environment exposure (`aspnet-core.md`) |
| Test framework selection (`decisions.md`) | NUnit usage default (`backend-testing.md`) |

## Enforcement and Delivery Assets

| File | Level | Purpose | Points to |
|---|---|---|---|
| `settings.json` | 3 | Registers hooks with shell-neutral `node -e` launchers (project dir resolved in Node) | hooks below |
| `hooks/lib.cjs` | 3 | Shared hook helpers: root resolution, input, command classification, exit codes | — |
| `hooks/dependency-guard.cjs` | 3 | PreToolUse: blocks unmarked package and project-reference commands, npm force flags | `add-dependency`, `project-structure` |
| `hooks/post-edit.cjs` | 3 | PostToolUse: spec/settings reminders, manifest checks, instruction checks | CLAUDE.md, `custom-settings`, `check-*` |
| `hooks/stop-cochange.cjs` | 3 | Stop: one-time seed, migration, test, and product-source reminders (no loop) | `develop`, `verify`, `custom-settings` |
| `scripts/check-instructions.cjs` | 3 | Structural predicates of this system; `--rules-for <path>` lookup | this map |
| `scripts/check-manifests.cjs` | 3 | Central package management, versions, deny/approval lists, reference direction | `package-management.md`, `backend-layers.md` |
| `scripts/dependency-policy.json` | 3 | Denied and approval-required packages; approved exceptions | `decisions.md`, `add-dependency` |
| `.editorconfig` (root) | 2 | Formatting and C# style | `csharp.md` |
| `Directory.Build.props` (root) | 3 | Shared .NET settings | `decisions.md` |
| `Directory.Packages.props` (root) | 2 | Central Package Management | `package-management.md` |
| `.gitignore` (root) | 3 | Generated/local artifacts and hook state | `project-structure` |

## Where New Content Belongs

1. Normative? → a rule. Procedure? → a workflow. Technique? → a knowledge skill.
   Product behavior or value? → `SPECIFICATION.md` / `CUSTOM_SETTINGS.md`.
2. Pick the level with the four-question test in `template-maintenance`; split
   mixed statements.
3. Pick the trigger: planning-time → `CLAUDE.md`, `overview.md`, or
   `decisions.md`; file-area → path rule; step → workflow.
4. Keep one owner; elsewhere use `→` pointers or check-by-reference items.
5. Update this map and run `node .claude/scripts/check-instructions.cjs`.
