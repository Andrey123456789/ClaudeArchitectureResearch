> Level: meta (all levels) · Owns: human-facing map of the instruction system · Scope: repo/meta · Loads: never (not imported, not path-scoped)

# Instruction Map

For maintainers. Claude does not load this file automatically. Changes to the instruction system follow the user-invoked `template-maintenance` workflow and end with `node .claude/scripts/check-instructions.mjs`.

## How the system is organized

The primary axis is **stability** — ask "how fundamental and stable is this rule?":

```text
0 Core          precedence, product governance, decision control, completion contract, Git safety,
                technology-neutral principles (testing, security, logging, runtime, dependencies)
1 Architecture  adopted Clean Architecture, layer roles and boundaries, outcomes, entry points,
                frontend structure, patterns not adopted          (platform vocabulary only)
2 Technology    C#/.NET, ASP.NET Core, EF Core, Angular/npm, containers and CI — rules and knowledge skills
3 Project       stack selection, conditional technologies, layout, conventions, data lifecycle,
                stack-specific workflows, hooks and scripts
```

**Dependency direction.** A conformance reference points only to the same or a more stable level:

```text
3 Project  →  2 Technology  →  1 Architecture  →  0 Core
```

Routing pointers ("run `verify`", "technique: `ef-core` skill") may point anywhere. `CLAUDE.md` `@` imports are loading edges, not conformance dependencies.

**Technology neutrality.** Levels 0 and 1 name no concrete technology beyond the fixed platform (.NET, C#, TypeScript). Concrete names appear only at Levels 2 and 3, which bind the neutral rules (see Split statements).

**Stratified decisions.** Planning-time decisions are split by level: adopted/not-adopted architecture in `.claude/rules/1-architecture/overview.md`; stack, conditional technologies and project defaults in `.claude/rules/3-project/decisions.md`. Both are imported by `CLAUDE.md`. There is no merged cross-level register.

**Product inputs are not levels.** `SPECIFICATION.md` (behavioral intent), `CUSTOM_SETTINGS.md` (approved tunable values), optional feature specifications and task prompts are inputs governed by `.claude/rules/0-core/product-governance.md`; they can request an engineering decision change but never silently override one.

### Loading legend

| Mechanism | Meaning |
|---|---|
| always | `CLAUDE.md` or a module it imports with `@` (always-loaded surface: `CLAUDE.md` + 5 imports + skill descriptions) |
| path | `.claude/rules/**` file loaded when Claude reads a file matching its `paths:` |
| workflow-read | named in a workflow's "Read first" list, so it is loaded even when its path trigger has not fired |
| on demand | skill invoked by the model (description match) or by the user (`/name`) |
| user-only | skill with `disable-model-invocation: true` |
| hook / script | deterministic enforcement configured in `.claude/settings.json` or run from a workflow |

### Header format

Every instruction artifact starts (after any frontmatter) with one line:
`> Level: <n> <Name> · Owns: <responsibility> · Scope: <scope> · Loads: <mechanism>`.
Scopes: common, backend, backend-tests, frontend, delivery, repo/meta.

## Level 0 — Core

| File | Owns | Scope | Loading | Enforcement | Add here |
|---|---|---|---|---|---|
| `CLAUDE.md` | precedence of levels and product inputs, normative vocabulary, operating principles (scope, simplicity, no speculative frameworks, challenge obligation), work loop (inspect first, review before verify, verify before completion), workflow routing, imports | common | always | instruction checker | entry-point principles only; anything topical goes to a module |
| `.claude/rules/0-core/product-governance.md` | specification authority, reading the specification, invented behavior, product ambiguity approval, string semantics, durable-source sync, CUSTOM_SETTINGS ownership/exclusions/conflicts/new values/propagation | common | always (imported) | post-edit hook reminders on `SPECIFICATION.md` / `CUSTOM_SETTINGS.md`; Stop reminder | product-input authority rules |
| `.claude/rules/0-core/decision-control.md` | Decided/Delegated/Reserved, approved-technology use, Reserved list, five-question test, Decision Request fields, recording obligation, headless behavior | common | always (imported) | — (procedure: `architecture-decision`) | decision-protocol rules (not individual decisions) |
| `.claude/rules/0-core/git-safety.md` | explicit-request Git mutations, parallel branches/worktrees, never destroying user work, state inspection, focused staging | repo/meta | always (imported) | `.claude/settings.json` `ask` permissions for repository-changing Git commands | Git safety rules (procedures go to `git-workflow`) |
| `.claude/rules/0-core/completion-contract.md` | verification obligations (diff first, build/test, runtime smoke, risk-scoped checks, fix-and-retry, truthful report), review obligations, repair obligations, generated output, CI truthfulness | common, delivery | path (code and CI files); workflow-read by `verify`, `code-review`, `build-fix` | Stop reminders; architecture checker used by `verify` | obligations that workflows must guarantee |
| `.claude/rules/0-core/testing-principles.md` | test level, behavior focus, explicit cases, naming, coverage, isolation, known state, provider fidelity, regression tests, probe preservation | backend-tests | path (`backend/**/*Tests/**`); workflow-read by `verify`, `build-fix`, `code-review` | Stop reminder (production change without test change) | framework-neutral testing rules |
| `.claude/rules/0-core/security-principles.md` | secrets, untrusted input, upload metadata, parameterized data access, server authorization, anonymous access, fail-safe checks, auth crypto, token validation, enumeration, CSRF, token storage, TLS, cryptography, CORS, visible security-config failure, error exposure, security-review discipline | common | path (code, config, Docker files); workflow-read by `security-scan` | — | technology-neutral security rules |
| `.claude/rules/0-core/logging-principles.md` | sensitive data in logs, payload logging, log-once for unexpected exceptions | common | path (`backend/**`, `frontend/**`) | — | what may be logged and where |
| `.claude/rules/0-core/runtime-principles.md` | clear-first performance, efficient data access, measured optimizations, performance-change procedure, caching need/lifetime/keys/invalidation, bounded external calls, retry safety, Retry-After, fallback, cancellation vs transient failure | backend | path (`backend/**`) | — | technology-neutral runtime rules |
| `.claude/rules/0-core/dependency-hygiene.md` | current need, latest stable compatible version, due diligence, license approval | common | path (manifests); workflow-read by `add-dependency` | pre-command hook routes dependency commands to `add-dependency`; manifest checks (floating/prerelease versions) | dependency-selection rules |
| `.claude/skills/git-workflow/SKILL.md` | Git procedures: inspection, branches, worktrees, commits, push, merge/rebase, PRs, high-risk operations, report | repo/meta | on demand | — | Git procedure detail |

## Level 1 — Architecture

| File | Owns | Scope | Loading | Enforcement | Add here |
|---|---|---|---|---|---|
| `.claude/rules/1-architecture/overview.md` | decision summary of the adopted architecture; owner of the not-adopted CQRS/mediator/VSA rule; list of other not-adopted patterns; where architecture decisions are recorded | backend, frontend | always (imported) | — | accepted/rejected architecture decisions (via `architecture-decision`) |
| `.claude/rules/1-architecture/backend-layers.md` | dependency direction, test-project references, Domain independence, simple domain default, rich-domain approval, no decorative DDD, Application Services, Application abstractions, no persistence/web types in Application, cache and remote-transport boundaries, constructor injection, lifetimes, registration placement, composition root | backend, backend-tests | path (`backend/**`); workflow-read by `project-structure` | `check-architecture.mjs` (references, namespaces, packages); manifest hook (project references) | layer roles and boundaries |
| `.claude/rules/1-architecture/persistence-boundary.md` | specific repositories, no queryable/framework types in contracts, generic repository only in Infrastructure, unit of work as commit boundary, shared context, no repository container, explicit transactions only when needed, persistence framework as Infrastructure detail | backend | path; workflow-read by `project-structure` | `check-architecture.mjs` (`IQueryable` in repository contracts, generic repository contracts) | persistence-boundary rules |
| `.claude/rules/1-architecture/entry-points.md` | thin entry points, no business/persistence in controllers, HTTP semantics in Api, success/401/403/409/412 semantics, empty collections, transport-contract duplication, documentation truthfulness, API versioning need/compatibility/strategy/inner models/deprecation, health checks | backend | path; workflow-read by `project-structure` | `check-architecture.mjs` (persistence context in controllers) | HTTP-surface and operational-endpoint rules |
| `.claude/rules/1-architecture/outcomes.md` | expected outcomes, Result not forced, outcome naming, exceptions not branch control, central failure handling, client cancellation, validation boundaries | backend | path; workflow-read by `project-structure` | — | outcome, exception and validation-boundary rules |
| `.claude/rules/1-architecture/frontend-structure.md` | feature organization, presentation focus, data-access boundary, error contract, validation as UX, lazy loading, simple state first | frontend | path (`frontend/**`); workflow-read by `project-structure` | — | frontend structural rules |
| `.claude/rules/1-architecture/code-organization.md` | no speculative projects/directories/generic buckets; role-revealing names (guidance) | common | path (`backend/**`, `frontend/**`); workflow-read by `project-structure` | — | physical-structure and naming-by-role guidance |

## Level 2 — Technology

### Rules

| File | Owns | Scope | Loading | Enforcement | Add here |
|---|---|---|---|---|---|
| `.claude/rules/2-technology/csharp.md` | C# conventions, file/async naming, changed-file using cleanup, no style-only rewrites, async/sync-over-async, cancellation tokens, TimeProvider, HttpClient lifetime, typed options, structured `ILogger<T>` | backend | path (`backend/**/*.cs`); workflow-read by `verify` | `.editorconfig` + `EnforceCodeStyleInBuild` (IDE0005) | C#/.NET language and runtime rules |
| `.claude/rules/2-technology/aspnet-core.md` | web-transport type bindings, controller binding, `IExceptionHandler` binding, auth facilities, problem-details contracts, Swagger UI exposure, Serilog host integration, Data Protection scope, `WebApplicationFactory` integration tests | backend, backend-tests | path (`backend/**`) | — | ASP.NET Core-specific rules and bindings |
| `.claude/rules/2-technology/ef-core.md` | EF Core bindings for the persistence boundary, InMemory is not relational, migration review | backend | path (`backend/**`) | Stop reminder on migration changes | EF Core-specific rules and bindings |
| `.claude/rules/2-technology/angular.md` | standalone APIs, Signals vs RxJS, reactive forms, functional interceptors, nested subscriptions, subscription lifecycle, npm force flags | frontend | path (`frontend/**`) | pre-command hook blocks `npm --force` / `--legacy-peer-deps` | Angular/npm-specific rules |
| `.claude/rules/2-technology/containers-ci.md` | container runtime image and non-root user, CI frontend scripts and `npm ci` | delivery | path (Docker, Compose, CI files) | — | container and CI tooling rules |

### Knowledge skills (technique; never sole owners of must-rules)

| File | Technique | Scope | Loading | Add here |
|---|---|---|---|---|
| `.claude/skills/ef-core/SKILL.md` | DbContext, repositories, queries, tracking, pagination, bulk ops, transactions, interceptors, raw SQL, seeder mechanics, migration commands | backend | on demand | EF Core examples |
| `.claude/skills/http-api/SKILL.md` | full status-code reference, idempotency, ETags, decision table | backend | on demand | HTTP response detail |
| `.claude/skills/aspnet-error-handling/SKILL.md` | global handler, outcome mapping, problem-details shape, FluentValidation wiring, catching patterns | backend | on demand | error-handling examples |
| `.claude/skills/dotnet-testing/SKILL.md` | NUnit, application-service tests, `WebApplicationFactory`, test databases, time, stubs, naming, probe conversion | backend-tests | on demand | test technique |
| `.claude/skills/logging/SKILL.md` | levels, scopes, correlation, `LoggerMessage` | backend | on demand | logging technique |
| `.claude/skills/logging/references/serilog.md` | Serilog bootstrap, configuration, request logging, sinks (private to `logging`) | backend | read by `logging` | Serilog detail |
| `.claude/skills/httpclient-factory/SKILL.md` | client models, handlers, timeouts, response mapping, adapter tests | backend | on demand | outbound HTTP technique |
| `.claude/skills/httpclient-factory/references/resilience.md` | resilience pipelines, retry, circuit breaker, hedging, fallback (private to `httpclient-factory`) | backend | read by `httpclient-factory` | resilience detail |
| `.claude/skills/configuration/SKILL.md` | options pattern, validation, secrets, precedence | backend | on demand | configuration technique |
| `.claude/skills/dependency-injection/SKILL.md` | layer registration, lifetimes, keyed services, decorators, factories, scanning | backend | on demand | DI technique |
| `.claude/skills/caching/SKILL.md` | cache layer choice, HybridCache, keys, invalidation, output caching | backend | on demand | caching technique |
| `.claude/skills/swagger/SKILL.md` | Swashbuckle setup, metadata, security definitions, documents, generated clients | backend | on demand | Swagger technique |
| `.claude/skills/api-versioning/SKILL.md` | Asp.Versioning setup, versioned controllers, compatibility, deprecation mechanics | backend | on demand | versioning technique |
| `.claude/skills/health-check/SKILL.md` | liveness/readiness endpoints, database checks, exposure | backend | on demand | health-check technique |
| `.claude/skills/docker/SKILL.md` | multi-stage images, non-root, Compose, probes, `.dockerignore` | delivery | on demand | container technique |
| `.claude/skills/ci-cd/SKILL.md` | backend/frontend jobs, GitHub Actions shape, artifacts, secrets, migration steps | delivery | on demand | pipeline technique |
| `.claude/skills/angular/SKILL.md` | structure, components, signals/RxJS, data access, interceptors, errors, forms, routing, tests | frontend | on demand | Angular technique |
| `.claude/skills/modern-csharp/SKILL.md` | C# 14 features and when to use them | backend | on demand | language technique |
| `.claude/skills/authentication/SKILL.md` | schemes, JWT/OIDC setup, policies, resource authorization, current user, CSRF, tests | backend | on demand | auth technique |

Asset: `.editorconfig` (Level 2) — formatting and analyzer severities for the C# rules.

## Level 3 — Project

### Rules

| File | Owns | Scope | Loading | Enforcement | Add here |
|---|---|---|---|---|---|
| `.claude/rules/3-project/decisions.md` | approved stack (platform, persistence, validation, logging, API documentation, backend tests, frontend, packages, solution/build), conditional technologies (incl. Docker), not-by-default libraries, repository layout | common | always (imported) | manifest checks (listed packages); `Directory.Build.props`, `Directory.Packages.props` | stack and project-default decisions (via `architecture-decision`) |
| `.claude/rules/3-project/conventions.md` | NuGet Central Package Management, npm lockfile and dependency categories, NUnit as test framework | backend, backend-tests, frontend | path; workflow-read by `add-dependency`, `project-structure` | manifest checks (versioned references, dev tooling in runtime dependencies) | project package and test conventions |
| `.claude/rules/3-project/data-lifecycle.md` | local Development database configuration, development seeding (default dataset, placement, Development-only, no schema changes, no overwrite, valid data, co-change), settings-driven schema changes, production migrations | backend, delivery | path (`backend/**`, Docker/CI files); workflow-read by `verify`, `custom-settings`, `project-structure` | Stop reminder (model changed without seeder change) | data-lifecycle rules |

### Workflows and agent

| File | Procedure | Reads first | Loading |
|---|---|---|---|
| `.claude/skills/project-structure/SKILL.md` | scaffolding and structural change (commands, packages, verification) | Level 1 modules, Level 2 rules, `conventions.md`, `data-lifecycle.md` | on demand |
| `.claude/skills/project-structure/references/solution-layout.md` | repository tree, shared build files, tests/docs placement (private) | — | read by `project-structure` |
| `.claude/skills/project-structure/references/backend-layout.md` | project internals, reference graph, test references (private) | — | read by `project-structure` |
| `.claude/skills/verify/SKILL.md` | verification steps and report | `completion-contract.md`, `testing-principles.md`, `csharp.md`, `data-lifecycle.md` | on demand |
| `.claude/skills/code-review/SKILL.md` | review steps, checklists by reference, severity, output | `completion-contract.md` + governing modules | on demand; preloaded by the agent |
| `.claude/skills/build-fix/SKILL.md` | repair loop, contract failures, iteration limits, report | `completion-contract.md`, `testing-principles.md` | on demand |
| `.claude/skills/custom-settings/SKILL.md` | settings synchronization | product governance, `data-lifecycle.md` | on demand |
| `.claude/skills/security-scan/SKILL.md` | seven-layer scan, severity, report | `security-principles.md`, `logging-principles.md` | on demand |
| `.claude/skills/security-scan/references/scan-layers.md` | per-layer investigation prompts (private) | — | read by `security-scan` |
| `.claude/skills/add-dependency/SKILL.md` | need/decision check, version, due diligence, license approval, install, report | `dependency-hygiene.md`, `conventions.md` | on demand; routed by the pre-command hook |
| `.claude/skills/architecture-decision/SKILL.md` | classification, Decision Request, recording table, ADR template | decision control (always loaded) | on demand |
| `.claude/skills/template-maintenance/SKILL.md` | placement, ownership, loading, map update, checker | this map | user-only |
| `.claude/agents/code-reviewer.md` | thin read-only reviewer that runs `code-review` | `code-review`, `completion-contract.md` | delegated subagent |

### Enforcement assets

| File | Does | Points to |
|---|---|---|
| `.claude/settings.json` | hook registration; `ask` permission for repository-changing Git commands | `git-safety.md` |
| `.claude/hooks/pre-command.mjs` | blocks dependency commands without the `# add-dependency` marker; blocks `npm --force` / `--legacy-peer-deps` | `add-dependency`, `dependency-hygiene.md`, `angular.md` |
| `.claude/hooks/post-edit.mjs` | reminders after `SPECIFICATION.md` / `CUSTOM_SETTINGS.md` edits; manifest checks; instruction-structure check after instruction edits | `product-governance.md`, `custom-settings`, `conventions.md` |
| `.claude/hooks/stop-co-change.mjs` | one-time reminders per changed-file set: seeder co-change, migration review, settings sync, tests for production changes (guards `stop_hook_active`) | `data-lifecycle.md`, `ef-core.md`, `product-governance.md`, `testing-principles.md` |
| `.claude/hooks/lib.mjs` | shared hook helpers | — |
| `.claude/scripts/check-architecture.mjs` | project-reference direction, forbidden namespaces/packages in Domain/Application, persistence access in controllers | `backend-layers.md`, `persistence-boundary.md`, `entry-points.md` |
| `.claude/scripts/check-manifests.mjs` | central versions, floating/prerelease versions, listed packages, dev tooling placement, project references | `conventions.md`, `dependency-hygiene.md`, `decisions.md` |
| `.claude/scripts/check-instructions.mjs` | this system's structural predicates: level folders, headers, `paths`, neutrality of Levels 0–1, reference direction, resolvable references, private references, skill names, user-only maintenance, thin reviewer, map coverage, absence of a kind taxonomy | `template-maintenance` |
| `Directory.Build.props` | shared .NET settings (target framework, nullable, implicit usings, code style on build) | `decisions.md` |
| `Directory.Packages.props` | Central Package Management switch and versions | `conventions.md` |

Hooks and scripts require Node.js on the PATH (the Angular toolchain already needs it). If Node is missing, hook commands fail without blocking work; install Node or run the checks manually.

## Split statements

Neutral rules live at the stable level; concrete bindings live where the technology or selection lives.

| Stable statement (owner) | Binding (owner) |
|---|---|
| Domain and Application free of persistence-framework types; persistence framework is an Infrastructure detail (`backend-layers.md`, `persistence-boundary.md`) | `DbContext`, `DbSet<T>`, EF APIs and provider types are the persistence-framework types; scoped `AppDbContext` is the shared context (`ef-core.md`); EF Core + SQL Server selected (`decisions.md`) |
| Application and Domain free of web-transport types; HTTP semantics in Api (`backend-layers.md`, `entry-points.md`) | `IActionResult`, `ProblemDetails`, `HttpContext`, … are the transport types (`aspnet-core.md`) |
| Thin HTTP entry points (`entry-points.md`) | ASP.NET Core Controllers selected; no Minimal API groups unless requested (`decisions.md`); `[ApiController]` binding (`aspnet-core.md`) |
| Central handler for unexpected failures; client cancellation is not a 500 (`outcomes.md`) | `IExceptionHandler` and `RequestAborted` handling (`aspnet-core.md`) |
| Validation at the owning boundary with the standard validation library (`outcomes.md`) | FluentValidation selected (`decisions.md`) |
| Mediator-based organization not adopted (`overview.md`) | MediatR and Kommand named as mediator libraries (`decisions.md`) |
| No custom password/token cryptography when platform facilities exist; no custom cryptography (`security-principles.md`) | ASP.NET Core authentication handlers and Identity; Data Protection is not universal database encryption (`aspnet-core.md`) |
| Local secret store for development (`security-principles.md`) | `dotnet user-secrets` for the local connection string (`data-lifecycle.md`) |
| Provider fidelity in tests (`testing-principles.md`) | EF Core InMemory is not relational (`ef-core.md`); Testcontainers conditional (`decisions.md`) |
| Integration tests when composition is the subject (`testing-principles.md`) | `WebApplicationFactory<Program>` (`aspnet-core.md`); NUnit as framework (`conventions.md`, `decisions.md`) |
| Frontend validation is UX; feature-oriented frontend (`frontend-structure.md`) | reactive forms; standalone Angular APIs (`angular.md`) |
| Published API documentation matches runtime (`entry-points.md`) | Swagger UI exposure in Development (`aspnet-core.md`); Swashbuckle selected (`decisions.md`) |
| Dependency need, stable versions, due diligence (`dependency-hygiene.md`) | NuGet Central Package Management, npm lockfile (`conventions.md`); npm force flags (`angular.md`) |
| What may be logged; log once (`logging-principles.md`) | structured `ILogger<T>` (`csharp.md`); Serilog host integration (`aspnet-core.md`); Serilog provider (`decisions.md`) |
| CI reproduces supported commands, failures visible (`completion-contract.md`) | `npm ci`, existing scripts only (`containers-ci.md`) |
| Docker introduced only when needed (`decisions.md`) | runtime image and non-root user (`containers-ci.md`) |

## Topic index

| Topic | Owner |
|---|---|
| 401/403, deliberate 404 hiding, 409/412, success statuses, empty collections | `entry-points.md` |
| Accepted-decision recording (obligation / procedure) | `decision-control.md` / `architecture-decision` |
| Anonymous access, server-side authorization, fail-safe checks | `security-principles.md` |
| API documentation truthfulness; versioning, breaking changes, deprecation | `entry-points.md` |
| Application Services, Application abstractions, layer dependency direction | `backend-layers.md` |
| Approved stack, conditional technologies, not-by-default libraries, Docker adoption, layout | `decisions.md` |
| Async, cancellation tokens, TimeProvider, HttpClient lifetime, typed options, usings, style scope | `csharp.md` |
| Authentication failure detail, token validation, CSRF, token storage, custom auth crypto | `security-principles.md` |
| Cache need, keys, lifetime, invalidation | `runtime-principles.md` |
| Cache/remote-transport types kept out of inner layers | `backend-layers.md` |
| Challenge obligation, scope discipline, simplicity, no speculative frameworks, precedence, vocabulary | `CLAUDE.md` |
| CI truthfulness | `completion-contract.md` |
| CI frontend commands, container runtime image | `containers-ci.md` |
| Client cancellation outcome, expected outcomes, Result, exceptions as control flow, validation boundaries | `outcomes.md` |
| Code review obligations | `completion-contract.md` |
| Composition root, DI lifetimes, constructor injection, registration placement | `backend-layers.md` |
| CORS, TLS, cryptography, secrets, untrusted input, uploads, SQL parameterization, error exposure | `security-principles.md` |
| `CUSTOM_SETTINGS.md` content, conflicts, new values, propagation | `product-governance.md` |
| Decision classes, Reserved list, five questions, Decision Request, headless runs | `decision-control.md` |
| Dependency need, version selection, due diligence, licenses | `dependency-hygiene.md` |
| Development database configuration, seeding, settings-driven schema changes, production migrations | `data-lifecycle.md` |
| Domain independence, simple domain, rich-domain approval, decorative DDD | `backend-layers.md` |
| DTO duplication between Api and Application | `entry-points.md` |
| EF Core bindings, InMemory, migration review | `ef-core.md` |
| Frontend structure, data access, error contract, validation role, lazy loading, state | `frontend-structure.md` |
| Angular APIs, Signals/RxJS, forms, interceptors, subscriptions, npm force flags | `angular.md` |
| Generated output fixed at its source; repair obligations | `completion-contract.md` |
| Git operations, parallel work, user changes, staging | `git-safety.md` |
| Health checks | `entry-points.md` |
| Inspect existing code; code-review before verify; verify before completion | `CLAUDE.md` |
| Logging content, payloads, log once | `logging-principles.md` |
| NuGet Central Package Management, npm lockfile, NUnit as framework | `conventions.md` |
| Patterns not adopted (CQRS, mediator, VSA, …) | `overview.md` |
| Performance, data-access efficiency, measured optimizations, external-call timeouts, retries, Retry-After, fallback | `runtime-principles.md` |
| Physical structure and role-revealing names | `code-organization.md` |
| Problem-details contracts, Swagger UI exposure, Serilog integration, Data Protection, integration tests | `aspnet-core.md` |
| Repositories, unit of work, transactions, persistence-framework boundary | `persistence-boundary.md` |
| Security review evidence and tool independence | `security-principles.md` |
| Specification authority, invented behavior, product ambiguity, string semantics, durable-source sync | `product-governance.md` |
| Test-project references | `backend-layers.md` |
| Testing level, behavior focus, isolation, provider fidelity, regression, probes, coverage, naming | `testing-principles.md` |
| Thin entry points, HTTP semantics in Api | `entry-points.md` |
| Verification obligations and reporting | `completion-contract.md` |

## Where new content goes

Use the `template-maintenance` workflow (user-invoked). In short: find the level with the level tests (most volatile dependency wins; split mixed statements), choose the artifact by responsibility (rule, decision summary, workflow, knowledge skill, hook/script), extend the existing owner instead of restating, choose the loading mechanism, add the header, update this map and run the checker.
