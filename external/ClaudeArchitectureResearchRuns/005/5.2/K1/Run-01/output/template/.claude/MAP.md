Map: human-facing instruction map | Scope: repo/meta | Capability: — | Loading: not loaded (maintainers only)

# Instruction Map

Every instruction artifact is classified on three independent coordinates, decided in this order:

1. **Capability**: is the content specific to a replaceable implementation? Then the selected module owns it (`Capability: <slot>/<implementation>`); otherwise it is non-slot (`Capability: —`).
2. **Kind**: what responsibility it has, which decides its mechanism and location.
3. **Scope**: where it applies (`common`, `backend`, `backend-tests`, `frontend`, `delivery`, `repo/meta`), which decides the rules directory and `paths:`.

Each file starts with a one-line header `Kind: … | Scope: … | Capability: … | Loading: …`. Procedure for changes: the `template-maintenance` workflow (user-invoked). Structural check: `node .claude/scripts/check-instructions.mjs`.

## Kinds and mechanisms

| Kind | Responsibility | Mechanism | Location |
|---|---|---|---|
| OP | operating policy: product authority, decision control, challenge obligation, routing, Git boundary | always loaded | `CLAUDE.md` |
| DEC | decided choices: stack, repository defaults, conditional technologies, capability selection | always loaded (imported by `CLAUDE.md`); slot contracts and manifests on demand | `docs/architecture/decision-register.md`, `.claude/capabilities/` |
| STD | normative standards for files in a scope | auto-loaded when a matching file is read (`paths:`) | `.claude/rules/<scope>/` |
| KNW | technique, examples, depth | model-invoked skill | `.claude/skills/<name>/` |
| WF | procedures, stop conditions, output shapes | skill invoked by routing; module workflow facets read by workflow steps; thin agent | `.claude/skills/<name>/`, `<module>/workflow-facet.md`, `.claude/agents/` |
| ENF | deterministic enforcement | hooks, scripts, build and editor configuration | `.claude/settings.json`, `.claude/hooks/`, `.claude/scripts/`, `.editorconfig`, `Directory.*.props` |
| IN | product inputs (never instructions) | read when relevant | `SPECIFICATION.md`, `CUSTOM_SETTINGS.md` |

Conformance dependencies point WF → KNW → STD → DEC → OP, and ENF → STD/DEC. Product inputs may request a decision change but never override policy. Routing pointers may point in any direction. A skill's `references/` file is used only by that skill.

## Kind × Scope view

### Always loaded (OP, DEC)

| File | Kind / Scope / Capability | Owns | Enforcement | Extend here when |
|---|---|---|---|---|
| `CLAUDE.md` | OP / common / — | normative vocabulary; product behavior and string semantics; tunable settings; engineering defaults and the challenge obligation; Decision control (Decided/Delegated/Reserved, Reserved list, five questions, autonomous runs); workflow routing; Git boundary | PostToolUse product-input reminder; Stop co-change reminder | a rule must be known at planning time in every task |
| `docs/architecture/decision-register.md` | DEC / common / — plus one DEC section per module | approved stack, repository layout, solution format, shared build files, conditional technologies, capability selection table; module sections hold slot decisions (adopted style and not-adopted styles, persistence stack, test stack, frontend stack and libraries) | `check-instructions.mjs` (selection ↔ modules) | a project-level choice is decided or changed (via `architecture-decision`) |

### Standards (STD, path-scoped)

| File | Scope / Capability | `paths:` | Owns | Enforcement | Extend here when |
|---|---|---|---|---|---|
| `.claude/rules/common/security.md` | common / — | `**/*` | secrets, secret mechanisms, untrusted input, server-side authorization, TLS, sensitive data and payloads in logs, fail-safe and fail-visible security controls | — | a security rule applies to every file type |
| `.claude/rules/common/dependencies.md` | common / — | `**/*` | need for dependencies, removal, NuGet Central Package Management, npm usage and lockfile | PreToolUse dependency gate; PostToolUse manifest check; `check-manifests.mjs` | a package-management convention changes |
| `.claude/rules/common/repository-structure.md` | common / — | `**/*` | structure follows responsibilities; no speculative projects, empty trees or generic buckets | — | a repository-wide structure rule is needed |
| `.claude/rules/backend/architecture.md` | backend / — | `backend/**` | composition root, DI style and lifetimes, registration per layer, cache and remote-HTTP leakage, API contract duplication and versioned models | — | a backend boundary rule holds for any layered frame |
| `.claude/rules/backend/architecture-style.md` | backend / architecture/clean-architecture | `backend/**` | dependency direction, Domain modeling, Application Services and ports, thin controllers, repositories, Unit of Work, transactions, test-project references | `check-architecture.mjs`, PostToolUse, NUnit architecture test | the architecture frame's placement rules change |
| `.claude/rules/backend/persistence.md` | backend / — | `backend/**` | data-access efficiency, development seed-data policy | Stop co-change (seed) | a persistence rule is technology-neutral |
| `.claude/rules/backend/persistence-technology.md` | backend / persistence/ef-core | `backend/**` | role bindings (persistence types, session, provider fidelity), EF Core boundary, seeder placement and limits, development connection string | `check-architecture.mjs` (no persistence packages in inner layers) | an EF Core or provider-specific rule is needed |
| `.claude/rules/backend/http-api.md` | backend / — | `backend/**` | HTTP layer ownership, success/empty/auth/conflict status semantics, versioning, Swagger accuracy and exposure, health checks | — | an HTTP contract rule is needed |
| `.claude/rules/backend/error-handling.md` | backend / — | `backend/**` | error contracts, failure-detail exposure, central exception handling, logging once, client cancellation, expected outcomes, exceptions as control flow, validation boundaries | — | an error or validation rule is needed |
| `.claude/rules/backend/security.md` | backend / — | `backend/**` | SQL parameterization, anonymous access, auth mechanisms, token validation, enumeration-safe failures, cryptography and Data Protection, CORS, upload metadata | — | a backend-only security rule is needed |
| `.claude/rules/backend/performance.md` | backend / — | `backend/**` | optimization stance, measured optimizations, async, cancellation, `TimeProvider`, caching need, keys, expiration, invalidation | — | a runtime or caching rule is needed |
| `.claude/rules/backend/integrations.md` | backend / — | `backend/**` | `HttpClient` lifetime, timeouts, retry safety, Retry-After, fallback, caller cancellation | — | an outbound-call rule is needed |
| `.claude/rules/backend/coding-style.md` | backend / — | `backend/**` | conventions, no unrelated style rewrites, file/namespace/async naming, naming and visibility guidance | `.editorconfig`, `Directory.Build.props` (IDE0005, naming) | a C# style rule is needed (prefer `.editorconfig` when mechanical) |
| `.claude/rules/backend/operations.md` | backend / — | `backend/**`, container files | structured logging, Serilog integration, typed options, container runtime image | — | a logging, configuration or container rule is needed |
| `.claude/rules/backend-tests/testing.md` | backend-tests / — | `backend/**/*Tests/**` | test level, behavior focus, determinism and isolation, explicit cases, integration tests, provider fidelity, test-owned data, coverage, naming | Stop co-change (tests) | a framework-neutral test rule is needed |
| `.claude/rules/backend-tests/test-framework.md` | backend-tests / backend-testing/nunit | `backend/**/*Tests/**` | NUnit role bindings and the default framework | — | a test-framework-specific rule is needed |
| `.claude/rules/frontend/frontend.md` | frontend / — | `frontend/**` | feature structure, component focus, lazy loading, local state, data-access boundary, error contract, form validation stance, CSRF, token storage | Stop co-change (frontend tests) | a framework-neutral frontend rule is needed |
| `.claude/rules/frontend/frontend-framework.md` | frontend / frontend/angular | `frontend/**` | Angular role bindings, standalone APIs, Signals vs RxJS, interceptors, subscriptions | `check-manifests.mjs` (approval watch-list) | an Angular-specific rule is needed |

No `delivery`-scope standard exists: delivery obligations are workflow steps (`verify` → 6. Delivery and deployment changes) and delivery technique is knowledge (`ci-cd`, `docker`). Add a `delivery` rules directory only for a path-triggered delivery rule.

### Workflows (WF)

| File | Scope / Capability | Owns | Loading | Enforcement | Extend here when |
|---|---|---|---|---|---|
| `.claude/skills/development-workflow/SKILL.md` | common / — | reading the specification before substantial work, inspecting code, classification, seeder co-change, performance-change procedure, review gate, verify gate, stop conditions | routed from `CLAUDE.md` | Stop co-change reminders | the implementation procedure changes |
| `.claude/skills/verify/SKILL.md` | common / — | diff inspection, build and tests, runtime smoke, preserving probes as tests, regression tests, risk-scoped checks, delivery obligations (CI, frontend CI, production migrations), using cleanup, fix-and-retry, reporting | routed from `CLAUDE.md` | runs `check-architecture.mjs` and `check-manifests.mjs` | a completion check is added |
| `.claude/skills/code-review/SKILL.md` | common / — | review priorities, specification conformance check, review steps, no manufactured findings, severity output | routed; preloaded by the agent | — | review criteria change |
| `.claude/agents/code-reviewer.md` | common / — | independent read-only review delegated to `code-review` | subagent | `disallowedTools` blocks file edits | agent tooling changes |
| `.claude/skills/build-fix/SKILL.md` | common / — | reproduce and diagnose first, bounded iterations, no weakened verification, generated output fixed at its source, repair loop | routed | — | the repair procedure changes |
| `.claude/skills/custom-settings/SKILL.md` | common / — | synchronization obligation and procedure for `CUSTOM_SETTINGS.md` | routed | PostToolUse reminder on product-input edits | the settings procedure changes |
| `.claude/skills/add-dependency/SKILL.md` | common / — | version selection, due diligence, license and commercial approval, conditional package choices (API versioning, resilience), npm force flags, install and verification | routed | PreToolUse dependency gate; PostToolUse manifest checks | the dependency procedure changes |
| `.claude/skills/architecture-decision/SKILL.md` | common / — | Decision Request format, recording (register, decision records, specification, settings), API version deprecation | routed | `check-instructions.mjs` keeps register and modules aligned | the decision procedure changes |
| `.claude/skills/project-structure/SKILL.md` | repo/meta / — | scaffolding and restructuring sequence through the module workflow facets | routed | `check-architecture.mjs` | the scaffolding sequence changes |
| `.claude/skills/git-workflow/SKILL.md` | repo/meta / — | user-work safety, state-aware minimal operations, focused staging and commits, branches, push, merge, PRs | routed | — | the Git procedure changes |
| `.claude/skills/security-scan/SKILL.md` + `.claude/skills/security-scan/references/scan-layers.md` | common / — | evidence and contextual severity, tool independence, layers, report shape | routed | `check-manifests.mjs` as evidence | the audit procedure changes |
| `.claude/skills/template-maintenance/SKILL.md` | repo/meta / — | classification of new content, authoring rules, module replacement, checks | user-invoked only | `check-instructions.mjs` | the instruction system's maintenance rules change |
| `<module>/workflow-facet.md` (four modules) | slot scope / module | slot-specific procedures: placement, setup, migrations and migration review, schema-affecting settings, test projects and commands, frontend scaffolding, build-fix and security cues | read by workflow steps through the register | slot enforcement facets (see capability view) | an implementation-specific step is needed |

### Knowledge (KNW, model-invoked)

All knowledge skills load when the model invokes them from their description, carry no enforcement of their own (the rules they point to are enforced where noted above), and are extended by adding technique to the skill whose topic matches.

| Skill | Scope / Capability | Technique for | Rules it points to |
|---|---|---|---|
| `ef-core` | backend / persistence/ef-core | EF Core: context, configuration, repositories, Unit of Work, queries, transactions, transient faults, seeding code, raw SQL, testing implications | persistence, persistence-technology, architecture-style |
| `dotnet-testing` | backend-tests / backend-testing/nunit | NUnit tests, `WebApplicationFactory`, test databases, time, stubs, naming | testing, test-framework |
| `angular` | frontend / frontend/angular | Angular structure, Signals, RxJS, HTTP, interceptors, forms, routing, Material, testing | frontend, frontend-framework |
| `http-api` | backend / — | status-code definitions, less common codes, idempotency, optimistic concurrency | http-api |
| `aspnet-error-handling` | backend / — | `IExceptionHandler`, outcomes, controller mapping, FluentValidation wiring, catching | error-handling |
| `logging` + `.claude/skills/logging/references/serilog.md` | backend / — | levels, scopes, correlation, `LoggerMessage`; Serilog bootstrap, sinks, request logging | operations, common/security |
| `httpclient-factory` + `.claude/skills/httpclient-factory/references/resilience.md` | backend / — | client models, handlers, mapping, testing; retries, circuit breakers, hedging, fallback | integrations |
| `configuration` | backend / — | options, validation, named options, secrets | operations, common/security |
| `dependency-injection` | backend / — | layer registration, keyed services, decorators, Scrutor, factories | architecture |
| `caching` | backend / — | cache layers, HybridCache, output caching, invalidation | performance, architecture |
| `swagger` | backend / — | Swashbuckle setup, metadata, security definitions | http-api |
| `api-versioning` | backend / — | Asp.Versioning, breaking vs compatible changes | http-api, architecture |
| `health-check` | backend / — | liveness, readiness, probes | http-api |
| `docker` | delivery / — | Dockerfiles, Compose, probes, images | operations |
| `ci-cd` | delivery / — | pipelines, artifacts, migrations in deployment | `verify` step 6 |
| `modern-csharp` | backend / — | C# 14 features | coding-style |
| `authentication` | backend / — | schemes, policies, resource authorization, current user | backend/security, frontend |

Add a knowledge skill only for a distinct body of technique; it must never be the only home of a must-rule.

### Capability artifacts (DEC, on demand)

| File | Scope / Capability | Owns | Loading | Enforcement | Extend here when |
|---|---|---|---|---|---|
| `.claude/capabilities/architecture/CONTRACT.md` | backend / architecture | frame role vocabulary, required facets and properties, replacement | read by `architecture-decision`, `template-maintenance` | `check-instructions.mjs` (slot structure) | the frame contract changes |
| `.claude/capabilities/persistence/CONTRACT.md` | backend / persistence | required mechanisms, facets, variants and replacement | as above | as above | the persistence contract changes |
| `.claude/capabilities/backend-testing/CONTRACT.md` | backend-tests / backend-testing | required facets and replacement | as above | as above | the test-framework contract changes |
| `.claude/capabilities/frontend/CONTRACT.md` | frontend / frontend | role vocabulary, required facets, "none" and replacement | as above | as above | the frontend contract changes |
| `.claude/capabilities/<slot>/<implementation>/MODULE.md` (four) | slot scope / module | manifest: slot, implementation, aliases, binds, facet table, implementation facts | read by workflows and maintainers | `check-instructions.mjs` (manifest completeness, leak rule) | a facet is added, moved or removed |

### Enforcement (ENF)

| File | Scope / Capability | What it does | Loading | Extend here when |
|---|---|---|---|---|
| `.claude/settings.json` | common / — (JSON, no header line) | registers the hooks below with shell-neutral `node -e` commands that locate `.claude/hooks/` from the current directory upward | Claude Code settings | a hook event is added |
| `.claude/hooks/pre-tool-use.mjs` | common / — | holds each distinct dependency command (NuGet, npm, .NET tools, frontend CLI add) once per session and routes it to `add-dependency`; same for npm force flags | PreToolUse (Bash, PowerShell) | a command must be routed to a workflow first |
| `.claude/hooks/post-tool-use.mjs` | common / — | after manifest edits or dependency/reference commands runs `check-manifests.mjs` and `check-architecture.mjs`; reminds on `SPECIFICATION.md`/`CUSTOM_SETTINGS.md` edits | PostToolUse | an edit must trigger a check |
| `.claude/hooks/stop.mjs` | common / — | co-change reminders (seed data, migrations, tests, product inputs) from read-only `git status`, once per distinct set per session, never twice in a row | Stop | a co-change reminder is needed (add a `coChange` rule to enforcement data, not code) |
| `.claude/hooks/lib/dependency-commands.mjs`, `.claude/scripts/lib/common.mjs` | common, repo/meta / — | shared helpers (command classification, root resolution from the script location, globs, project-file parsing) | imported | shared logic changes |
| `.claude/scripts/check-architecture.mjs` | backend / — | neutral engine: project roles, allowed references, inner-layer packages, frameworks and SDKs | hooks, `verify`, NUnit adapter, manual | a new kind of reference check is needed (rule data belongs in the facet) |
| `.claude/scripts/check-manifests.mjs` | common / — | Central Package Management, exact and stable versions, denied and watched packages, npm floating versions, tooling category, lockfile | hooks, `verify`, `add-dependency`, manual | a new manifest check is needed |
| `.claude/scripts/check-instructions.mjs` | repo/meta / — | headers, Kind/Scope locations, `paths:`, required workflows and knowledge, slot composition, manifest completeness, leak rule, references, hook commands, budget estimate | `template-maintenance`, manual | a structural predicate of the instruction system changes |
| `.claude/scripts/enforcement.json` | common / — | non-slot command patterns, messages, NuGet/npm policy data, product-input co-change | read by hooks and scripts | non-slot enforcement data changes |
| `.claude/scripts/facets/<slot>/…` | slot scope / module | slot enforcement data and the NUnit adapter (see capability view) | read by hooks and scripts | implementation-specific enforcement data changes |
| `.editorconfig` | common / — | formatting, file-scoped namespaces, IDE0005, naming | editors, `dotnet format`, build | a mechanical style rule can be enforced by tooling |
| `Directory.Build.props` | backend / — | target framework, nullable, implicit usings, code-style enforcement in build | MSBuild | a genuinely shared build setting is needed |
| `Directory.Packages.props` | backend / — | Central Package Management switch and versions | MSBuild | `add-dependency` adds a version |

Hooks need Node.js on `PATH`. Each hook command finds `.claude/hooks/<hook>.mjs` from the current directory upward, so it works from subdirectories and in cmd, PowerShell and bash without environment-variable expansion; the scripts resolve the project root from their own location and report a clear error instead of skipping silently when an assumption does not hold.

### Product inputs (IN)

| File | Role | Loading | Enforcement | Extend here when |
|---|---|---|---|---|
| `SPECIFICATION.md` | authoritative product behavior when non-empty; empty in the template on purpose | read before substantial work (`development-workflow`) | PostToolUse and Stop reminders | approved product behavior is recorded |
| `CUSTOM_SETTINGS.md` | approved tunable values; rules in `CLAUDE.md` → Tunable settings | read when tunable values matter | PostToolUse and Stop reminders | an approved tunable value is added (`custom-settings`) |

## Capability view

Selection lives in `docs/architecture/decision-register.md` → Capability selection. Static composition: one implementation per required slot, zero or one for `frontend`; changing a selection or variant is Reserved; unselected implementations are absent.

### architecture → clean-architecture (required frame)

Contract: `.claude/capabilities/architecture/CONTRACT.md` (role vocabulary: Domain, Application, Infrastructure, Api, persistence port, commit boundary, persistence area, test projects). Manifest: `.claude/capabilities/architecture/clean-architecture/MODULE.md`.

| Kind | Facet | Scope | Loading |
|---|---|---|---|
| DEC | register section "architecture → clean-architecture" | common | always |
| STD | `.claude/rules/backend/architecture-style.md` | backend | path-scoped |
| WF | `.claude/capabilities/architecture/clean-architecture/workflow-facet.md` | backend | read by `project-structure`, `development-workflow` |
| ENF | `.claude/scripts/facets/architecture/enforcement.json` | backend | `check-architecture.mjs`, Stop hook |

Declared properties: layer projects `backend/<Name>.<Layer>`, Application Services, `IUnitOfWork`, persistence area `Infrastructure/Persistence/`, test-project placement, not adopted: CQRS, MediatR, Kommand, Vertical Slice Architecture. binds: —.

### persistence → ef-core, variant sqlserver (required leaf)

Contract: `.claude/capabilities/persistence/CONTRACT.md`. Manifest: `.claude/capabilities/persistence/ef-core/MODULE.md`. binds: architecture (Infrastructure, persistence port, commit boundary, persistence area).

| Kind | Facet | Scope | Loading |
|---|---|---|---|
| DEC | register section "persistence → ef-core (sqlserver)" | common | always |
| STD | `.claude/rules/backend/persistence-technology.md` | backend | path-scoped |
| KNW | `.claude/skills/ef-core/SKILL.md` | backend | model-invoked |
| WF | `.claude/capabilities/persistence/ef-core/workflow-facet.md` | backend | read by workflow steps |
| ENF | `.claude/scripts/facets/persistence/enforcement.json` | backend | `check-architecture.mjs`, Stop hook |

Declared properties: SQL Server provider, `UnitOfWork` → `AppDbContext.SaveChangesAsync`, EF Core migrations, `DbSeeder` in Development only, collation-based (usually case-insensitive) string comparison, provider-fidelity tests against SQL Server.

### backend-testing → nunit (required leaf)

Contract: `.claude/capabilities/backend-testing/CONTRACT.md`. Manifest: `.claude/capabilities/backend-testing/nunit/MODULE.md`. binds: architecture (test-project placement and references).

| Kind | Facet | Scope | Loading |
|---|---|---|---|
| DEC | register section "backend-testing → nunit" | common | always |
| STD | `.claude/rules/backend-tests/test-framework.md` | backend-tests | path-scoped |
| KNW | `.claude/skills/dotnet-testing/SKILL.md` | backend-tests | model-invoked |
| WF | `.claude/capabilities/backend-testing/nunit/workflow-facet.md` | backend-tests | read by workflow steps |
| ENF | `.claude/scripts/facets/backend-testing/ArchitectureConformanceTests.cs` | backend-tests | scaffold asset; runs in `dotnet test` |

Declared properties: NUnit, NUnit3TestAdapter, NUnit.Analyzers, `WebApplicationFactory<Program>`, `FakeTimeProvider`, Testcontainers conditional.

### frontend → angular (optional leaf)

Contract: `.claude/capabilities/frontend/CONTRACT.md`. Manifest: `.claude/capabilities/frontend/angular/MODULE.md`. binds: —.

| Kind | Facet | Scope | Loading |
|---|---|---|---|
| DEC | register section "frontend → angular" | common | always |
| STD | `.claude/rules/frontend/frontend-framework.md` | frontend | path-scoped |
| KNW | `.claude/skills/angular/SKILL.md` | frontend | model-invoked |
| WF | `.claude/capabilities/frontend/angular/workflow-facet.md` | frontend | read by workflow steps |
| ENF | `.claude/scripts/facets/frontend/enforcement.json` | frontend | hooks, `check-manifests.mjs`, Stop hook |

Declared properties: workspace `frontend/<Name>.Web/`, npm with lockfile, colocated `*.spec.ts`, Vitest for new projects, Playwright for E2E when required.

## Topic → owner index

| Topic | Owner |
|---|---|
| Specification authority, invented behavior, product ambiguity, string semantics | `CLAUDE.md` → Product behavior |
| Reading the specification before substantial work | `development-workflow` → 1. Read the inputs |
| Recording approved behavior in durable sources | `architecture-decision` → 3. Record the approved decision |
| Tunable values, settings conflicts, settings exclusions | `CLAUDE.md` → Tunable settings |
| Settings synchronization | `custom-settings` |
| Simplicity, no speculative frameworks, scope discipline, challenge obligation | `CLAUDE.md` → Engineering defaults |
| Decided/Delegated/Reserved, consequential changes, Decision Requests | `CLAUDE.md` → Decision control; `architecture-decision` |
| Git boundary and parallel work | `CLAUDE.md` → Git; procedure `git-workflow` |
| Approved stack, layout, solution format, conditional technologies | decision register |
| Selected architecture, persistence, test and frontend stacks | decision register → Capability selection |
| Layer dependencies, Domain modeling, Application Services, controllers, repositories, Unit of Work | `architecture-style.md` |
| DI, composition root, leakage of cache and remote HTTP, API contract duplication | `architecture.md` |
| Seed-data policy, data-access efficiency | `persistence.md` |
| EF Core boundary, seeder placement, development connection string | `persistence-technology.md` |
| Migration review, schema-affecting settings changes | persistence workflow facet |
| HTTP status semantics, versioning, Swagger, health checks | `http-api.md` |
| Errors, validation, cancellation mapping | `error-handling.md` |
| Security (all files / backend / browser) | `common/security.md`, `backend/security.md`, `frontend/frontend.md` |
| Performance, async, time, caching | `performance.md` |
| Outbound calls and resilience | `integrations.md` |
| C# style | `coding-style.md` |
| Logging, configuration, containers | `operations.md` |
| Dependencies and package management | `common/dependencies.md`; procedure `add-dependency` |
| Tests (neutral / framework) | `testing.md`, `test-framework.md`; completion duties `verify` |
| Frontend (neutral / framework) | `frontend.md`, `frontend-framework.md` |
| Inspect-first, review and verify gates, performance-change procedure, seeder co-change | `development-workflow` |
| Verification, behavioral probes, regression tests, using cleanup, CI and production-migration duties | `verify` |
| Review priorities and findings | `code-review`; agent `code-reviewer` |
| Build repair and generated output | `build-fix` |
| Security review evidence and tool independence | `security-scan` |
| Physical structure discipline | `repository-structure.md`; scaffolding `project-structure` |
