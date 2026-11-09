> Owner: human-facing map of the instruction system (navigation only, no policy) | Scope: repo/meta | Loads: never automatically — read by maintainers and `/template-maintenance` | Enforced: `.claude/scripts/check-instructions.mjs` (every artifact must be listed here)

# Instruction Map

How the instructions for this repository are organized, where each policy lives,
how it loads, and what is enforced mechanically. Policy text lives only in the
owner named here; this map never restates it.

## Loading Model

| Mechanism | What loads | When |
| --- | --- | --- |
| Always | `CLAUDE.md` + imported `docs/technology-stack.md` | every session, at planning time |
| Path | flat rules in `.claude/rules/` | when Claude works with files matching the rule's `paths` |
| Workflow read | rules named in a workflow's "Read First" step | greenfield, review, verify, and repair work where path loading may not have happened |
| On demand | skills in `.claude/skills/` (descriptions are listed; bodies load when invoked) | model- or user-invoked; `template-maintenance` is user-only |
| Private reference | `references/*.md` inside one skill | read only by that skill |
| Hook | `.claude/hooks/hooks.mjs` via `.claude/settings.json` | before/after shell and edit tools, and at stop |
| Tooling | `.editorconfig`, `Directory.Build.props`, `Directory.Packages.props` | IDE, `dotnet format`, MSBuild, NuGet restore |

Hooks and scripts need Node.js on `PATH`; without it they report a non-blocking
hook error and the instructions still apply.

## Always-Loaded Surface

| File | Owns | Scope | Enforced | Extend here when |
| --- | --- | --- | --- | --- |
| `CLAUDE.md` | vocabulary; product-source authority; core defaults and challenge obligation; architecture decisions (decided, not adopted, repository layout); decision control (classes, Reserved list, test, Decision Request, headless rule); workflow routing; Git limits | common, repo/meta | PreToolUse Git pause; PostToolUse product-input reminders | a policy is needed at planning time for any task; keep it one line |
| `docs/technology-stack.md` | approved backend and frontend stack, solution and build-file format, conditional technologies, not-by-default libraries | common | `.claude/scripts/check-dependencies.mjs` | a technology is adopted, replaced, or made conditional (via `architecture-decision`) |

## Product Inputs and Records (not instruction layers)

| File | Role | Loads | Enforced |
| --- | --- | --- | --- |
| `SPECIFICATION.md` | authoritative product behavior when non-empty (empty in the template) | read by workflows and before substantial work | PostToolUse reminder on change |
| `CUSTOM_SETTINGS.md` | approved tunable product values | read on demand | PostToolUse and Stop reminders → `custom-settings` |
| `docs/decisions/` | accepted decision records (created with the first ADR) | read when a decision is questioned | none |

## Rules (`.claude/rules/`, flat)

| File | Owns | Scope (`paths`) | Read explicitly by | Enforced | Extend here when |
| --- | --- | --- | --- | --- | --- |
| `.claude/rules/architecture.md` | dependency direction; Domain, Application, API responsibilities; cache and remote-HTTP boundaries; DTO duplication; repository contracts; DI | backend (`backend/**/*.cs`, `*.csproj`, `*.slnx`) | `project-structure`, `code-review`, `verify`, `build-fix` | `check-architecture.mjs` | a new backend layering or boundary constraint appears |
| `.claude/rules/persistence.md` | Unit of Work; EF Core inside Infrastructure; development seeding; migrations; Development DB configuration | backend (`backend/**/*.cs`, `appsettings*.json`) | `verify`, `code-review`, `project-structure`, `custom-settings` | Stop seed/migration reminder | persistence lifecycle, seeding, or migration policy changes |
| `.claude/rules/api.md` | HTTP status semantics; API versioning and deprecation; Swagger accuracy and exposure; health endpoints | backend (`backend/**/*.cs`) | `code-review` | review checks | an HTTP-contract-level constraint appears |
| `.claude/rules/error-handling.md` | expected outcomes; central exception handling; error contracts; validation boundaries; exception logging; cancellation; outbound dependency failures (timeouts, retries, fallback) | backend (`backend/**/*.cs`) | `code-review`, `security-scan` | review checks | failure, validation, or resilience semantics change |
| `.claude/rules/coding-style.md` | C# conventions; file, namespace, async naming; using hygiene; style scope; typed options; logging call style and Serilog registration | backend (`backend/**/*.cs`) | `verify` | `.editorconfig`; `verify` diff review | a C# convention needs a rule rather than an `.editorconfig` entry |
| `.claude/rules/performance.md` | optimization discipline; async and cancellation propagation; `TimeProvider`; `HttpClient` lifetime; database efficiency; caching correctness; performance-change procedure | backend (`backend/**/*.cs`) | `code-review` | review checks | a performance or caching constraint appears |
| `.claude/rules/security.md` | secrets; input trust; SQL parameterization; authn/authz; browser credentials (CSRF, token storage); TLS and cryptography; CORS; sensitive logging; fail-safe behavior | common (backend, frontend, config, delivery files) | `security-scan`, `code-review`, `verify` | `security-scan`, `verify` | a security invariant appears |
| `.claude/rules/testing.md` | NUnit; test levels; behavior focus; isolation and test data; provider fidelity; readability; regression and probe preservation; coverage; naming; test references | backend-tests (`backend/**/*Tests/**`) | `verify`, `code-review`, `build-fix`, `project-structure` | `check-architecture.mjs` (references); Stop test reminder | a backend test constraint appears |
| `.claude/rules/dependencies.md` | dependency necessity; NuGet Central Package Management; npm package manager, lockfile, categories | common (manifests) | `add-dependency`, `build-fix` | PreToolUse routing; `check-dependencies.mjs`; NuGet `NU1008` | a manifest-level constraint appears |
| `.claude/rules/angular.md` | Angular structure; components; HTTP boundary; interceptors; error contract; signals and RxJS; subscriptions; state; lazy loading; forms | frontend (`frontend/**/*`) | `project-structure`, `code-review`, `build-fix` | review checks | a frontend constraint appears |
| `.claude/rules/delivery.md` | CI truthfulness; frontend CI installs; production container image | delivery (CI, Compose, Docker files) | `verify` (delivery changes) | `verify` delivery check | a pipeline or container constraint appears |
| `.claude/rules/repository-structure.md` | proportional physical structure (no speculative projects, empty trees, generic buckets) | common (`backend/**`, `frontend/**`, `docs/**`) | `project-structure` | review checks | a repository-wide structural constraint appears |

## Workflow Skills (procedures)

| File | Owns | Scope | Loads | Enforced | Extend here when |
| --- | --- | --- | --- | --- | --- |
| `.claude/skills/project-structure/SKILL.md` | scaffolding and restructuring procedure | common | on demand; routed by `CLAUDE.md` | `check-architecture.mjs`, `check-dependencies.mjs` | a scaffolding step or command changes |
| `.claude/skills/project-structure/references/solution-layout.md` | repository layout examples (private) | common | read by `project-structure` | none | the repository-level example tree changes |
| `.claude/skills/project-structure/references/backend-layout.md` | backend internals, reference graph, type-role naming (private) | backend | read by `project-structure` | `check-architecture.mjs` | project internals or examples change |
| `.claude/skills/verify/SKILL.md` | completion verification procedure and report | common | on demand; required before completion | check scripts; Stop reminders | a verification step changes |
| `.claude/skills/code-review/SKILL.md` | canonical review procedure, priorities, finding discipline, output | common | on demand; preloaded by the agent | reviewer agent tool allowlist | review procedure or output changes |
| `.claude/skills/build-fix/SKILL.md` | build/test repair loop, no weakened verification, generated-output repair | common | on demand | PreToolUse npm-flag block | repair procedure changes |
| `.claude/skills/custom-settings/SKILL.md` | settings propagation and schema-affecting settings | common | on demand; hook-routed | PostToolUse and Stop reminders | synchronization steps change |
| `.claude/skills/git-workflow/SKILL.md` | Git safety, minimal operations, preservation of user work, focused commits | repo/meta | on demand; hook-routed | PreToolUse Git pause | Git procedure changes |
| `.claude/skills/security-scan/SKILL.md` | static security review procedure, evidence and severity discipline, tool independence, report | common | on demand | none | the scan procedure changes |
| `.claude/skills/security-scan/references/scan-layers.md` | per-layer investigation prompts (private) | common | read by `security-scan` | none | a new investigation heuristic is needed |
| `.claude/skills/add-dependency/SKILL.md` | dependency change procedure: version selection, due diligence, license approval, peer conflicts, removal | common | on demand; hook-routed | PreToolUse routing and npm-flag block; `check-dependencies.mjs` | the dependency procedure changes |
| `.claude/skills/architecture-decision/SKILL.md` | Reserved-decision procedure, ADR format, planning-time updates | common | on demand; routed by `CLAUDE.md` § Decision Control | human approval | the decision procedure changes |
| `.claude/skills/template-maintenance/SKILL.md` | instruction-system maintenance procedure and conventions | repo/meta | user-invoked only (`/template-maintenance`) | `check-instructions.mjs` | maintenance conventions change |

## Knowledge Skills (technique; no normative ownership)

| File | Technique for | Scope | Policy owner |
| --- | --- | --- | --- |
| `.claude/skills/ef-core/SKILL.md` | DbContext, mappings, repositories, UoW, queries, transactions, interceptors, seeding pattern, migration commands | backend | `persistence.md`, `architecture.md` |
| `.claude/skills/http-api/SKILL.md` | status-code reference, idempotency, conditional requests | backend | `api.md` |
| `.claude/skills/aspnet-error-handling/SKILL.md` | `IExceptionHandler`, ProblemDetails, FluentValidation, typed outcomes | backend | `error-handling.md` |
| `.claude/skills/dotnet-testing/SKILL.md` | NUnit, WebApplicationFactory, test databases, fakes, probe conversion | backend-tests | `testing.md` |
| `.claude/skills/logging/SKILL.md` | message templates, levels, scopes, correlation | backend | `coding-style.md`, `error-handling.md`, `security.md` |
| `.claude/skills/logging/references/serilog.md` | Serilog setup, sinks, enrichers, request logging (private) | backend | `coding-style.md` |
| `.claude/skills/httpclient-factory/SKILL.md` | typed/named/keyed clients, handlers, response mapping | backend | `performance.md`, `error-handling.md`, `architecture.md` |
| `.claude/skills/httpclient-factory/references/resilience.md` | resilience pipelines, retry, circuit breaker, hedging, fallback (private) | backend | `error-handling.md`, `docs/technology-stack.md` |
| `.claude/skills/configuration/SKILL.md` | Options pattern, validation, secrets mechanics | backend | `coding-style.md`, `security.md` |
| `.claude/skills/dependency-injection/SKILL.md` | lifetimes, layer registration, keyed services, decorators, scanning | backend | `architecture.md` |
| `.claude/skills/caching/SKILL.md` | HybridCache, output caching, keys, invalidation | backend | `performance.md`, `architecture.md` |
| `.claude/skills/swagger/SKILL.md` | Swashbuckle setup, metadata, auth schemes | backend | `api.md` |
| `.claude/skills/api-versioning/SKILL.md` | Asp.Versioning setup, strategies, deprecation mechanics | backend | `api.md` |
| `.claude/skills/health-check/SKILL.md` | liveness/readiness endpoints, checks, exposure | backend | `api.md` |
| `.claude/skills/docker/SKILL.md` | Dockerfiles, Compose, non-root, probes | delivery | `delivery.md` |
| `.claude/skills/ci-cd/SKILL.md` | pipeline shapes, artifacts, audits, deployment | delivery | `delivery.md`, `persistence.md` |
| `.claude/skills/angular/SKILL.md` | Angular components, signals/RxJS, HTTP, forms, tests | frontend | `angular.md` |
| `.claude/skills/modern-csharp/SKILL.md` | C# 14 features, constructor/record/var/visibility style | backend | `coding-style.md` |
| `.claude/skills/authentication/SKILL.md` | schemes, policies, resource authorization, current user | backend | `security.md`, `api.md` |

All knowledge skills load on demand by description and enforce nothing. Extend a
knowledge skill when technique or examples are missing; never add a must-rule
there — put it in the owning rule.

## Agent

| File | Owns | Loads | Enforced |
| --- | --- | --- | --- |
| `.claude/agents/code-reviewer.md` | thin read-only reviewer that runs the preloaded `code-review` workflow | delegated subagent | tool allowlist without edit tools |

## Enforcement and Delivery Assets

| File | Purpose | Runs | Points to |
| --- | --- | --- | --- |
| `.claude/settings.json` | wires the hooks | Claude Code | `.claude/hooks/hooks.mjs` |
| `.claude/hooks/hooks.mjs` | PreToolUse: routes dependency commands to `add-dependency` and pauses repository-changing Git commands once per command; blocks npm peer-bypass flags. PostToolUse: manifest, architecture, and instruction checks after edits; product-input reminders. Stop: seed, migration, test, and settings co-change reminders (once per trigger, guarded against loops) | hooks | owners named in each message |
| `.claude/scripts/lib.mjs` | shared helpers | imported | — |
| `.claude/scripts/check-dependencies.mjs` | Central Package Management, version form, excluded and non-default packages, npm manifest hygiene | CLI, hook, `verify`, `add-dependency` | `dependencies.md`, `docs/technology-stack.md`, `add-dependency` |
| `.claude/scripts/check-architecture.mjs` | project reference direction, test reference scope, forbidden layer dependencies in sources | CLI, hook, `verify`, `project-structure` | `architecture.md`, `api.md`, `testing.md` |
| `.claude/scripts/check-instructions.mjs` | headers, flat rules with `paths`, skill set and front matter, private references, pointers, imports, map coverage, hook wiring, always-loaded estimate | CLI, hook after instruction edits, `template-maintenance` | `template-maintenance` |
| `.editorconfig` | formatting, using placement, naming and `var` suggestions | IDE, `dotnet format` | `coding-style.md` |
| `Directory.Build.props` | shared target framework, nullable, implicit usings, NuGet audit | MSBuild | `docs/technology-stack.md` |
| `Directory.Packages.props` | Central Package Management switch; the only place for versions | NuGet | `dependencies.md` |

## Policy Index

Where to find the authoritative owner of a policy topic.

| Topic | Owner |
| --- | --- |
| Normative vocabulary | `CLAUDE.md` § Vocabulary |
| Specification authority, no invented behavior, ambiguity approval, string semantics, source synchronization | `CLAUDE.md` § Product Sources |
| Custom settings ownership, conflicts, new values, exclusions | `CLAUDE.md` § Product Sources |
| Custom settings propagation, schema-affecting settings | `.claude/skills/custom-settings/SKILL.md` § Propagation Obligation, § Database Impact |
| Proportional simplicity, no speculative frameworks, scope preservation, challenge obligation | `CLAUDE.md` § Core Defaults |
| Adopted architecture, patterns not adopted, repository layout | `CLAUDE.md` § Architecture Decisions |
| Decided/Delegated/Reserved, consequential-change approval, Decision Requests, headless behavior | `CLAUDE.md` § Decision Control |
| Inspect before change, read specification, review before verify, verify before completion, workflow routing | `CLAUDE.md` § Development Workflow |
| Git mutations only on request, parallel-work isolation | `CLAUDE.md` § Git |
| User work preserved, state-aware minimal Git operations, focused staging and commits | `.claude/skills/git-workflow/SKILL.md` § Safety, § Scope |
| Backend platform, persistence, validation, logging, Swagger, testing stack, solution format, build files | `docs/technology-stack.md` § Backend |
| Mapping, resilience packages, Testcontainers, API versioning package, Docker, Playwright | `docs/technology-stack.md` § Conditional Technologies |
| Angular baseline, overlapping libraries | `docs/technology-stack.md` § Frontend |
| Dependency direction and layer responsibilities | `.claude/rules/architecture.md` |
| Repository contracts, generic repositories | `.claude/rules/architecture.md` § Repositories |
| Constructor injection, lifetimes, registration ownership | `.claude/rules/architecture.md` § Dependency Injection |
| Unit of Work, transactions, EF Core inside Infrastructure | `.claude/rules/persistence.md` |
| Development seeding (default dataset, placement, Development-only, no schema changes, no overwrite, validity, co-change) | `.claude/rules/persistence.md` § Development Seeding |
| Migration review, production migrations | `.claude/rules/persistence.md` § Migrations |
| Development connection string | `.claude/rules/persistence.md` § Development Database Configuration |
| Status codes, empty collections, 401/403, 409/412 | `.claude/rules/api.md` § HTTP Semantics |
| When to version, breaking changes, strategy, deprecation | `.claude/rules/api.md` § Versioning |
| Swagger accuracy and exposure | `.claude/rules/api.md` § Swagger |
| Health-check cost, liveness/readiness, safe output | `.claude/rules/api.md` § Health Checks |
| Expected outcomes, exceptions as control flow, central handling, logging once | `.claude/rules/error-handling.md` |
| ProblemDetails contracts, no leaked internals | `.claude/rules/error-handling.md` § Error Contracts |
| Validation boundaries | `.claude/rules/error-handling.md` § Validation Boundaries |
| Client and caller cancellation | `.claude/rules/error-handling.md` § Cancellation |
| Timeouts, safe retries, Retry-After, fallback | `.claude/rules/error-handling.md` § External Dependency Failures |
| C# conventions, naming, usings, style scope, typed options, logging templates, Serilog registration | `.claude/rules/coding-style.md` |
| Optimization discipline, async I/O, cancellation propagation, `TimeProvider`, `HttpClient` lifetime, query efficiency | `.claude/rules/performance.md` |
| Caching need, keys, lifetimes, invalidation | `.claude/rules/performance.md` § Caching |
| Performance-change procedure | `.claude/rules/performance.md` § Performance Changes |
| Secrets, input trust, uploads, SQL, authn/authz, CSRF, token storage, TLS, crypto, CORS, sensitive logging, fail-safe behavior | `.claude/rules/security.md` |
| Test framework, levels, behavior, isolation, fidelity, readability, regression, probes, coverage, naming, references | `.claude/rules/testing.md` |
| Dependency necessity, Central Package Management, npm discipline | `.claude/rules/dependencies.md` |
| Version selection, due diligence, license approval, npm peer conflicts, removal | `.claude/skills/add-dependency/SKILL.md` |
| Angular structure and implementation constraints | `.claude/rules/angular.md` |
| CI truthfulness, frontend CI, container images | `.claude/rules/delivery.md` |
| Proportional physical structure | `.claude/rules/repository-structure.md` |
| Diff inspection, builds and tests, runtime smoke, risk-scoped checks, fix-and-retry, truthful reporting | `.claude/skills/verify/SKILL.md` |
| Independent read-only review, priorities, no manufactured findings | `.claude/skills/code-review/SKILL.md` |
| Build-fix diagnosis, bounded iteration, no weakened verification, generated outputs | `.claude/skills/build-fix/SKILL.md` |
| Security evidence and severity, scanner independence | `.claude/skills/security-scan/SKILL.md` § Principles |
| Decision records and planning-time updates | `.claude/skills/architecture-decision/SKILL.md` |

## Where New Content Belongs

1. Needed at planning time for every task → `CLAUDE.md` (or
   `docs/technology-stack.md` for technology).
2. A constraint tied to a file area → the matching rule above; a new flat rule
   only when no existing rule's scope and topic fit.
3. A multi-step procedure with stop conditions and output → a workflow skill.
4. Technique or examples → the knowledge skill for the topic, or its private
   reference when provider-specific.
5. A mechanically checkable obligation → a check in `.claude/scripts/` or a hook
   message in `.claude/hooks/hooks.mjs`, while the rule stays the owner.
6. Product behavior or values → `SPECIFICATION.md` / `CUSTOM_SETTINGS.md`.

Make structural changes through `/template-maintenance` and finish with
`node .claude/scripts/check-instructions.mjs`.
