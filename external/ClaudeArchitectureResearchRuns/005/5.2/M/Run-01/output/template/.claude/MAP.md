> Human-facing instruction map, not auto-loaded. Owns: navigation of the instruction system — what each file owns, its scope, how it loads, how it is enforced, and where new content goes · Scope: repo/meta · Loads: never automatically; open it when maintaining the template · Depends on: none

# Instruction Map

## Organization at a Glance

| Responsibility | Where it lives |
|---|---|
| Planning-time policy: product sources, change discipline, decision control, architecture decisions, Git, routing | `CLAUDE.md` |
| Approved stack, conditional technologies, layout defaults | `docs/technology-stack.md` (imported by `CLAUDE.md`) |
| Constraints that apply while working on certain files | flat topical rules in `.claude/rules/` |
| Multi-step procedures, stop conditions, output shapes | workflow skills in `.claude/skills/` |
| Technique, examples, depth | knowledge skills in `.claude/skills/` and their `references/` |
| Deterministic enforcement | `.claude/settings.json`, `.claude/hooks/`, `.claude/scripts/`, `.editorconfig`, `Directory.*.props` |
| Product inputs (not instructions) | `SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, feature specifications, task prompts |
| Accepted project decisions (history) | `docs/decisions/` (created by `architecture-decision`) |

The designated decision summary is `CLAUDE.md` (Architecture Decisions): it
summarizes adopted and not-adopted architecture for planning; the detailed rules
stay in `.claude/rules/`.

## Loading

| Mechanism | Artifacts | When |
|---|---|---|
| Always | `CLAUDE.md`, `docs/technology-stack.md` (`@` import), skill names and descriptions | every session |
| Path | `.claude/rules/*.md` | when files matching the rule's `paths` are in context |
| Workflow | workflow `SKILL.md` files | invoked per the `CLAUDE.md` routing table; workflows that create or review code read the relevant rules explicitly |
| On demand | knowledge `SKILL.md` files and their `references/` | when the task needs the technique |
| User only | `template-maintenance` | only through `/template-maintenance` |
| Hooks | `.claude/hooks/*.mjs` via `.claude/settings.json` | before/after shell commands and file edits, and at stop |
| Manual / verify | `.claude/scripts/*.mjs` | from workflows, hooks, or by hand |

## Dependency Direction

`CLAUDE.md` ← `docs/technology-stack.md` ← `.claude/rules/*` ← workflow and
knowledge skills ← private references (only their own skill); the
`code-reviewer` agent → `code-review`. Each instruction file declares its
conformance dependencies in its header (`Depends on`); always-loaded and
path-scoped policy depends only on always-loaded or path-scoped files, and the
graph is acyclic (checked by `check-instructions.mjs`). Routing pointers ("see
X", "run Y") may point in any direction.

## Header Format

Every instruction file starts — after its frontmatter, if any — with one line:

```text
> <what the file is>. Owns: <responsibility> · Scope: <scopes> · Loads: <mechanism> · Depends on: <files or none>[ · Enforced by: <checks>]
```

Scopes: `common`, `backend`, `backend-tests`, `frontend`, `delivery`,
`repo/meta`. Project paths follow `backend/<Name>.<Layer>/...` and
`frontend/<Name>.Web/...`.

## Vocabulary

**must / must not** (and plain imperatives) — violation is a defect;
**default** — deviation needs a concrete reason and must be reported;
**prefer / avoid** — guidance; **requires approval** — Reserved decision.
Defined in `CLAUDE.md`.

## Artifact Map

### Always-Loaded Policy

| File | Owns | Scope | Loads | Enforcement | Extend here when… |
|---|---|---|---|---|---|
| `CLAUDE.md` | vocabulary; product-source authority (specification, custom settings, string semantics, ambiguity); change discipline and challenge obligation; decision control (Decided / Delegated / Reserved, Reserved list, five-question test, headless behavior); architecture decisions (adopted, not adopted); workflow routing; Git boundaries | common, repo/meta | always | hooks route to workflows; `check-instructions.mjs` validates imports | a rule must be known while planning any task |
| `docs/technology-stack.md` | approved backend, persistence, validation, logging, API-documentation, testing, and Angular stack; libraries not added by default; conditional technologies; solution-layout defaults | common, backend, backend-tests, frontend, delivery | always (`@` import) | `check-manifests.mjs` (deprecated and review-required packages) | a technology is approved, made conditional, or replaced (through `architecture-decision`) |

### Path-Scoped Rules (`.claude/rules/`, flat)

| File | Owns | Scope | `paths` | Enforcement | Extend here when… |
|---|---|---|---|---|---|
| `rules/architecture.md` | dependency direction, test-project references, Domain/Application/API responsibilities, cache and remote-transport boundaries, DTO and versioned-contract boundaries, composition and configuration defaults | backend, backend-tests | `backend/**/*.cs`, `backend/**/*.csproj` | `check-manifests.mjs` (project references), `check-architecture.mjs` | a layer-boundary or composition constraint changes |
| `rules/persistence.md` | repository contracts, generic-repository limits, Unit of Work, transactions, EF Core boundary, Development seeding, local Development connection string | backend | `backend/**/*.cs`, `backend/**/appsettings*.json` | `check-architecture.mjs` | a persistence or seeding constraint changes |
| `rules/api.md` | HTTP response semantics, API versioning boundaries, Swagger accuracy and exposure, health endpoints | backend | `backend/**/*.cs` | — | an HTTP contract constraint changes |
| `rules/error-handling.md` | expected outcomes, exception flow, error contracts, validation boundaries, request cancellation, logging practice and Serilog registration, outbound-dependency failure handling | backend | `backend/**/*.cs`, `backend/**/appsettings*.json` | — | an error, validation, logging, or outbound-failure constraint changes |
| `rules/performance.md` | optimization discipline, async I/O, cancellation propagation, `TimeProvider`, `HttpClient` lifetime, database-access efficiency, caching semantics, measured optimizations | backend | `backend/**/*.cs` | — | a performance or caching constraint changes |
| `rules/coding-style.md` | C# conventions, files/namespaces/async naming, style guidance, style-change scope | backend | `backend/**/*.cs` | `.editorconfig`, `dotnet format` in `verify` | a C# convention changes (mechanical ones go to `.editorconfig`) |
| `rules/testing.md` | test framework use, test level, behavior focus, readability, doubles, provider fidelity, isolation, test data, coverage, naming | backend-tests | `backend/**/*Tests/**/*.cs`, `backend/**/*Tests/*.csproj` | — | a backend test constraint changes |
| `rules/security.md` | secrets, input trust, SQL safety, authentication/authorization, browser credentials (CSRF, token storage), TLS, cryptography, CORS, sensitive data in logs, fail-safe behavior, container hardening | common, backend, frontend, delivery | `backend/**/*`, `frontend/**/*`, `**/*.json`, `**/*.yml`, `**/*.yaml`, `**/*.csproj`, `**/*.props`, `**/*.targets`, `**/*.config`, `**/.env*`, `Dockerfile*`, `**/Dockerfile*` | — | a security invariant changes |
| `rules/dependencies.md` | dependency need, NuGet Central Package Management, npm package management | common, backend, frontend | `**/*.csproj`, `**/Directory.Packages.props`, `**/package.json`, `**/package-lock.json` | `check-manifests.mjs` via the post-tool hook | a manifest constraint changes (procedures go to `add-dependency`) |
| `rules/angular.md` | Angular structure, component responsibility, HTTP boundary, interceptors, error-contract use, state and reactivity, routing, forms | frontend | `frontend/**` | — | a frontend constraint changes |
| `rules/repository-layout.md` | proportional physical structure (no speculative projects, empty trees, or generic buckets) | common | `backend/**`, `frontend/**`, `docs/**`, `*.slnx`, `*.sln` | — | a physical-structure constraint changes |

### Workflow Skills (`.claude/skills/<name>/SKILL.md`)

| Skill | Owns | Scope | Loads | Enforcement | Extend here when… |
|---|---|---|---|---|---|
| `development-workflow` | implementation procedure: inputs (specification read, code inspection, rule reads), change-type obligations (product-source sync, seed data, migrations review, regression tests, performance changes, API deprecation, CI/CD, database deployment), review and verification steps | common | routed by `CLAUDE.md` | `stop.mjs` reminders (seed data, migrations, tests); `check-architecture.mjs` (startup migrations) | a step applies to every implementation or to a type of change |
| `project-structure` | scaffolding and structural changes, greenfield rule reads, completion checks | common | routed by `CLAUDE.md` | `check-manifests.mjs`, `check-architecture.mjs` | scaffolding steps change |
| `skills/project-structure/references/solution-layout.md` | repository layout examples, shared-file guidance | common | read by `project-structure` | — | repository-level examples change |
| `skills/project-structure/references/backend-layout.md` | backend directory examples, type-role naming heuristics | backend, backend-tests | read by `project-structure` | — | backend layout examples change |
| `add-dependency` | version selection, due diligence, license gate, conditional package choices (resilience, API versioning), peer conflicts, removal | common, backend, frontend | routed by `CLAUDE.md` and the post-tool hook | `pre-tool.mjs` (blocks peer-dependency bypass flags), `post-tool.mjs`, `check-manifests.mjs` | the dependency procedure or a package choice changes |
| `architecture-decision` | Decision Request format, approval wait, decision records in `docs/decisions/`, propagation to planning-time owners | common | routed by `CLAUDE.md` | — | the decision procedure or record format changes |
| `custom-settings` | settings propagation, schema-affecting settings, synchronization verification | common | routed by `CLAUDE.md` and the post-tool hook | `post-tool.mjs`, `stop.mjs` reminders | the settings procedure changes |
| `verify` | completion verification: diff inspection, build, tests, runtime smoke, behavioral-probe preservation, risk-scoped checks, import hygiene of changed C# files, fix-and-retry, reporting | common | required by `development-workflow` | runs the check scripts | a completion check changes |
| `code-review` | review procedure, priorities, conformance and architecture check-by-reference, finding discipline, output format | common | routed by `CLAUDE.md`; preloaded by `code-reviewer` | — | review procedure or criteria routing changes |
| `build-fix` | build/test repair: reproduce and diagnose, bounded iteration, no weakened verification, generated output fixed at the source | common | routed by `CLAUDE.md` | — | the repair procedure changes |
| `git-workflow` | protection of user work, state-aware minimal operations, focused staging and commits, branches, worktrees, push, merge/rebase, PRs | repo/meta | routed by `CLAUDE.md` | `pre-tool.mjs` (asks before destructive Git commands) | Git procedure changes |
| `security-scan` | static security-review procedure, evidence and severity discipline, tool independence, report format | common | routed by `CLAUDE.md` | — | the audit procedure changes |
| `skills/security-scan/references/scan-layers.md` | per-layer investigation prompts and examples | common | read by `security-scan` | — | investigation prompts change |
| `template-maintenance` | procedure for changing this instruction system | repo/meta | user only (`/template-maintenance`) | `check-instructions.mjs` | the maintenance procedure changes |

### Agent

| File | Owns | Scope | Loads | Enforcement | Extend here when… |
|---|---|---|---|---|---|
| `agents/code-reviewer.md` | reviewer independence and read-only role; delegates to `code-review` | common | when delegated to; preloads `code-review` | `disallowedTools` | the reviewer's tool restrictions change (criteria go to `code-review`) |

### Knowledge Skills (technique only; never sole owners of a rule)

| Skill | Technique | Scope | Rules it serves | Extend here when… |
|---|---|---|---|---|
| `ef-core` | DbContext, configurations, repository/UoW implementations, queries, tracking, pagination, bulk operations, transactions, interceptors, seeder and migration technique | backend | `persistence.md`, `architecture.md`, `performance.md` | EF Core technique or examples change |
| `http-api` | status-code reference, idempotency, conditional requests | backend | `api.md`, `error-handling.md` | HTTP reference material changes |
| `aspnet-error-handling` | global exception handler, ProblemDetails, outcome mapping, validation wiring, Result pattern | backend | `error-handling.md`, `api.md` | error-handling technique changes |
| `dotnet-testing` | NUnit, case tables, unit/integration tests, test databases, time, HTTP stubs, test data | backend-tests | `testing.md` | test technique changes |
| `logging` | message templates, levels, scopes, correlation, `LoggerMessage` | backend | `error-handling.md`, `security.md` | logging technique changes |
| `skills/logging/references/serilog.md` | Serilog bootstrap, configuration, sinks, request logging, destructuring, `LogContext` | backend | `error-handling.md` | Serilog depth changes |
| `httpclient-factory` | typed/named/keyed clients, handlers, response mapping, outbound tests | backend | `performance.md`, `error-handling.md`, `architecture.md` | outbound HTTP technique changes |
| `skills/httpclient-factory/references/resilience.md` | resilience pipelines, retry, circuit breaker, fallback, hedging, database and messaging retries | backend | `error-handling.md` | resilience depth changes |
| `configuration` | options pattern, validation, secret providers, named options | backend | `architecture.md`, `security.md` | configuration technique changes |
| `dependency-injection` | registration, lifetimes, keyed services, decorators, scanning, factories | backend | `architecture.md` | DI technique changes |
| `caching` | cache layers, HybridCache, keys, expiration, invalidation, output caching | backend | `performance.md`, `architecture.md` | caching technique changes |
| `swagger` | Swashbuckle setup, metadata, security definitions, generated clients | backend | `api.md` | Swagger technique changes |
| `api-versioning` | when to version, Asp.Versioning setup, versioned controllers, compatibility | backend | `api.md`, `architecture.md` | versioning technique changes |
| `health-check` | liveness/readiness setup, dependency checks, exposure | backend | `api.md` | health-check technique changes |
| `docker` | Dockerfiles, Compose, non-root, probes, image optimization | delivery, backend, frontend | `security.md` | container technique changes |
| `ci-cd` | pipeline shapes, artifacts, dependency audits, deployment | delivery | `security.md`; obligations in `development-workflow` | pipeline technique changes |
| `angular` | structure, components, signals/RxJS, data access, interceptors, forms, routing, testing | frontend | `angular.md`, `security.md` | Angular technique changes |
| `modern-csharp` | modern C# feature technique | backend | `coding-style.md` | language technique changes |
| `authentication` | schemes, Identity, policies, roles, resource authorization, current user, auth tests | backend, frontend | `security.md`, `api.md` | authentication technique changes |

### Deterministic Enforcement and Configuration

| File | Purpose | Owner it enforces | Runs |
|---|---|---|---|
| `.claude/settings.json` | registers the hooks with shell-neutral `node .claude/hooks/<file>.mjs` commands | — | read by Claude Code |
| `.claude/hooks/pre-tool.mjs` | blocks peer-dependency bypass flags; asks before destructive Git commands | `add-dependency`, `git-workflow` | before Bash/PowerShell commands |
| `.claude/hooks/post-tool.mjs` | manifest check and dependency routing; product-input reminder; instruction-structure check after instruction edits | `dependencies.md`, `add-dependency`, `custom-settings`, `template-maintenance` | after edits and shell commands |
| `.claude/hooks/stop.mjs` | one-time co-change reminders from the Git working tree (seed data, migrations, tests, product inputs, manifests) | `development-workflow`, `verify`, `custom-settings` | when Claude stops |
| `.claude/hooks/commands.mjs` | shell-command classification shared by the hooks | — | imported by hooks |
| `.claude/scripts/check-manifests.mjs` | Central Package Management, versions, deprecated and review-required packages, project-reference direction, npm lockfile and dependency categories | `dependencies.md`, `architecture.md`, `docs/technology-stack.md`, `add-dependency` | hooks, `verify`, `project-structure`, by hand |
| `.claude/scripts/check-architecture.mjs` | source-level layer-boundary heuristics (EF Core/ASP.NET Core in inner layers, leaked queryables, Controllers using DbContext, seeder migrating, startup migrations) | `architecture.md`, `persistence.md`, `development-workflow` | `verify`, `project-structure`, by hand |
| `.claude/scripts/check-instructions.mjs` | the instruction-structure predicates of this template (see Structure Checks) | `template-maintenance` | post-tool hook, `verify`, `template-maintenance` |
| `.claude/scripts/lib/repo.mjs` | shared helpers: project-root resolution, safe paths, file walking, glob matching | — | imported by hooks and scripts |
| `.editorconfig` | deterministic formatting and C# style configuration | `coding-style.md` | IDE, `dotnet format` |
| `Directory.Build.props` | shared .NET build settings (target framework, nullable, implicit usings) | `docs/technology-stack.md` | MSBuild |
| `Directory.Packages.props` | Central Package Management versions | `dependencies.md` | MSBuild |

All hooks and scripts are Node.js ES modules using only built-in modules, so
they run unchanged on Windows, macOS, and Linux. Hook commands are relative to
the project root and contain no shell variable expansion; scripts resolve the
project root from their own location (falling back to `CLAUDE_PROJECT_DIR` read
inside the script) and report a clear "checks were NOT run" error instead of
skipping silently.

### Product Inputs

| File | Role | Governing policy |
|---|---|---|
| `SPECIFICATION.md` | authoritative product behavior when non-empty; intentionally empty in the template | `CLAUDE.md` (Product Sources) |
| `CUSTOM_SETTINGS.md` | approved tunable product limits and defaults | `CLAUDE.md` (Product Sources), `custom-settings` |

## Policy Locator

Topic → authoritative owner (section). Other files may only point to these.

| Topic | Owner |
|---|---|
| Normative vocabulary | `CLAUDE.md` (Normative Vocabulary) |
| Specification authority, invented behavior, product ambiguity, internal details | `CLAUDE.md` (Product Sources) |
| String comparison and normalization semantics | `CLAUDE.md` (Product Sources) |
| Custom settings role, conflicts with the specification, new tunable values, exclusions | `CLAUDE.md` (Product Sources) |
| Product inputs cannot override instructions | `CLAUDE.md` (Product Sources) |
| Proportional simplicity, no speculative frameworks, scope and behavior preservation | `CLAUDE.md` (Change Discipline) |
| Challenging questionable requests | `CLAUDE.md` (Change Discipline) |
| Decision classes, Reserved list, five-question test, approvals, headless behavior | `CLAUDE.md` (Decision Control) |
| Adopted and not-adopted architecture (CQRS, mediators, VSA, Rich Domain, …) | `CLAUDE.md` (Architecture Decisions) |
| Git mutations only on request; parallel-work isolation | `CLAUDE.md` (Git) |
| Approved technologies and no silent substitution | `docs/technology-stack.md` |
| .NET platform, persistence, validation, logging, Swagger, testing, Angular stack | `docs/technology-stack.md` |
| Libraries not added by default (NgRx, Axios, …); Playwright; Mapster; resilience; Docker optionality | `docs/technology-stack.md` |
| Solution layout, `.slnx`, shared build files, no top-level `tests/` | `docs/technology-stack.md` (Solution Layout) |
| Dependency direction, test-project references | `rules/architecture.md` (Dependency Direction) |
| Domain independence, simple domain default, Rich Domain criterion, no decorative DDD | `rules/architecture.md` (Domain) |
| Application Services, Application-owned abstractions, no EF/transport/cache/HTTP leaks | `rules/architecture.md` (Application) |
| Thin Controllers, composition root, DTO duplication, per-version models | `rules/architecture.md` (API) |
| Constructor injection, lifetimes, registration placement, typed options | `rules/architecture.md` (Composition and Configuration) |
| Specific repositories, no leaked queryables, generic repository limits | `rules/persistence.md` (Repositories) |
| Unit of Work, shared context, explicit transactions | `rules/persistence.md` (Unit of Work) |
| EF Core as Infrastructure detail | `rules/persistence.md` (EF Core Boundary) |
| Development seeding (dataset, placement, Development-only, no schema changes, no overwrite, invariants) | `rules/persistence.md` (Development Seeding) |
| Usable non-secret local connection string | `rules/persistence.md` (Local Development Database Configuration) |
| Status codes belong to the API; success statuses; empty collections; 401/403; 409/412 | `rules/api.md` (HTTP Semantics) |
| API versioning need, published compatibility, single strategy | `rules/api.md` (API Versioning) |
| Swagger accuracy and environment exposure | `rules/api.md` (Swagger) |
| Health checks: cheap, liveness vs. readiness, safe responses | `rules/api.md` (Health Checks) |
| Expected outcomes, Result usage, business exceptions | `rules/error-handling.md` (Expected Outcomes) |
| Central exception handling, logging exceptions once | `rules/error-handling.md` (Unexpected Exceptions) |
| ProblemDetails contracts, no leaked internals | `rules/error-handling.md` (Error Contracts) |
| Validation boundaries, FluentValidation use | `rules/error-handling.md` (Validation Boundaries) |
| Client cancellation is not a server failure | `rules/error-handling.md` (Request Cancellation) |
| Structured log templates, Serilog registration | `rules/error-handling.md` (Logging) |
| Timeouts, retry safety, Retry-After, fallback, cancellation vs. retry | `rules/error-handling.md` (Outbound Dependencies) |
| Correctness first, async I/O, cancellation propagation, `TimeProvider`, `HttpClient` lifetime | `rules/performance.md` |
| Database-access efficiency, measured optimizations | `rules/performance.md` |
| When to cache, cache keys, cache lifetimes, invalidation consistency | `rules/performance.md` (Caching) |
| C# conventions, file/namespace/async naming, style-only rewrites | `rules/coding-style.md` |
| Test framework, level, behavior focus, readability, doubles, provider fidelity, isolation, test data, coverage, naming | `rules/testing.md` |
| Secrets and secret mechanisms | `rules/security.md` (Secrets) |
| Untrusted input, upload metadata | `rules/security.md` (Input Boundaries) |
| Parameterized SQL | `rules/security.md` (SQL and Persistence) |
| Server-side authorization, anonymous access, platform authentication, token validation, enumeration leaks | `rules/security.md` (Authentication and Authorization) |
| CSRF with cookies, token storage | `rules/security.md` (Browser Credentials) |
| TLS and certificate validation | `rules/security.md` (Transport Security) |
| Custom cryptography, Data Protection scope | `rules/security.md` (Cryptography and Data Protection) |
| CORS | `rules/security.md` (CORS) |
| Sensitive data and payloads in logs | `rules/security.md` (Logging and Sensitive Data) |
| Fail-safe security checks, visible security-configuration failure | `rules/security.md` (Failure Behavior) |
| Production container images, root | `rules/security.md` (Containers) |
| Dependency need, Central Package Management, npm lockfile and categories | `rules/dependencies.md` |
| Angular structure, components, HTTP boundary, interceptors, error contract, state, RxJS, routing, forms | `rules/angular.md` |
| Speculative projects, empty trees, generic buckets | `rules/repository-layout.md` |
| Reading the specification and code before implementing; review before verify; verify before completion | `development-workflow` (steps 1, 4, 5) |
| Updating durable product sources after approval | `development-workflow` (Approved product rules) |
| Seeder co-change, migration review, regression tests, performance-change procedure | `development-workflow` (Change-Type Obligations) |
| API version deprecation, CI/CD obligations, production migrations | `development-workflow` (Change-Type Obligations) |
| Diff inspection, build/test, runtime smoke, probe preservation, risk-scoped checks, fix-and-retry, reporting | `verify` |
| Unused `using` directives in changed C# files | `verify` (Final Diff Review) |
| Review priorities, no manufactured findings | `code-review` |
| Reviewer independence and read-only role | `agents/code-reviewer.md` |
| Build-fix diagnosis, bounded iteration, no weakened verification, generated output | `build-fix` |
| Settings propagation, schema-affecting settings | `custom-settings` |
| Never discarding user work, state-aware minimal Git operations, focused commits | `git-workflow` |
| Security-finding evidence and severity, scanner independence | `security-scan` |
| Version selection, due diligence, license gate, resilience and versioning packages, peer conflicts | `add-dependency` |
| Decision Request format, decision records | `architecture-decision` |
| Instruction-system changes | `template-maintenance` |

## Where New Content Goes

1. Is it product behavior or a tunable value? → `SPECIFICATION.md` /
   `CUSTOM_SETTINGS.md`.
2. Must it be known while planning any task? → `CLAUDE.md` (or
   `docs/technology-stack.md` for technology choices). Keep it compact.
3. Does it constrain work on particular files? → the topical rule whose `paths`
   cover them; create a new flat rule only for a new topic or scope, and give it
   `paths`.
4. Is it a sequence of steps, a stop condition, or an output format? → the
   workflow skill for that activity.
5. Is it technique, examples, or depth? → the knowledge skill (or its
   `references/` file).
6. Can it be checked mechanically? → `.claude/scripts/` or `.claude/hooks/`,
   while the rule stays in its owner.
7. Never restate an existing rule: point to its owner or add a
   check-by-reference item.

Run `/template-maintenance` for these changes; it ends with
`node .claude/scripts/check-instructions.mjs`.

## Structure Checks

`check-instructions.mjs` verifies: required files; `CLAUDE.md` imports; a flat
`.claude/rules/` where every rule declares `paths`; the one-line header on every
instruction file and valid scope names; required workflow and knowledge skills;
`template-maintenance` disabled for model invocation; no standalone competing
Serilog or resilience skills; the read-only `code-reviewer` delegating to
`code-review`; private references used only by their owning skill; resolvable
file, skill, and agent references; an acyclic `Depends on` graph in which
always-loaded and path-scoped policy depends only on always-loaded or
path-scoped files; shell-neutral hook commands pointing to existing scripts;
this map describing every instruction and enforcement file; no Level/Kind
classification fields. It also prints an estimate of the always-loaded surface.
