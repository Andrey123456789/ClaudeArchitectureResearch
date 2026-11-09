> Owns: human-facing map of the instruction system (never loaded into Claude's context) | Scope: repo/meta | Loads: never (read by maintainers)

# Instruction Map

How this repository's Claude instructions are organized, where each rule lives,
how it loads, and what is enforced mechanically. Nothing imports this file.

## How Content Loads

| Mechanism | Content | When it reaches Claude |
| --- | --- | --- |
| Always | `CLAUDE.md` + `@docs/technology-stack.md` | Every session, at planning time |
| Path-scoped | `.claude/rules/*.md` (flat, each with `paths`) | When Claude reads or edits a file matching the rule's `paths` |
| Workflow | Workflow skills in `.claude/skills/` | When `CLAUDE.md`, another workflow, or a hook routes to them, or the user invokes them |
| On demand | Knowledge skills in `.claude/skills/` | When the task matches the skill description |
| Private reference | `.claude/skills/<skill>/references/*.md` | Read only by the owning skill |
| Subagent | `.claude/agents/code-reviewer.md` | When the main session delegates a review |
| Hooks | `.claude/settings.json` → `.claude/hooks/*.mjs` | On shell commands, file edits, and session stop |
| Product inputs | `SPECIFICATION.md`, `CUSTOM_SETTINGS.md` | Read by workflows; never instructions |
| Never | This map | Maintainers only |

Responsibility split: rules and `CLAUDE.md` hold normative policy (must / must
not / default / requires approval); workflow skills hold procedures, stop
conditions, and output shape; knowledge skills hold technique and examples only;
hooks, scripts, and configuration enforce what is mechanically checkable. A
pointer ("run X", "see Y") or a yes/no check-by-reference is never a second owner.

## Files

### Always loaded

| File | Owns | Scope | Enforcement | Extend here when… |
| --- | --- | --- | --- | --- |
| `CLAUDE.md` | Product-source governance, custom-settings governance, core defaults, challenge obligation, architecture defaults (decision summary, layout, patterns not adopted), decision control, Git boundaries, workflow routing | common | `check-instructions.mjs` (imports, header) | A rule must be known while planning, before any file is opened |
| `docs/technology-stack.md` | Approved stack, conditional technologies, solution format, shared build files | common | `check-manifests.mjs` (deprecated packages, CPM) | A technology is adopted, replaced, or a conditional one is activated (via `architecture-decision`) |

### Path-scoped rules (`.claude/rules/`)

| File | Owns | Scope | `paths` | Enforcement | Extend here when… |
| --- | --- | --- | --- | --- | --- |
| `.claude/rules/architecture.md` | Dependency direction, project and test references, Domain/Application/API responsibilities, repositories, Unit of Work, EF Core boundary, composition and DI, typed options, Serilog registration, boundary contracts | backend, backend-tests | `backend/**/*.cs`, `backend/**/*.csproj` | Project references checked by `check-manifests.mjs` | A backend layering, composition, or boundary constraint |
| `.claude/rules/persistence.md` | Development seeding, local Development database configuration | backend | `backend/**/*.cs`, `backend/**/appsettings*.json` | Stop hook seed reminder | Data-lifecycle or seeding constraint |
| `.claude/rules/api.md` | HTTP status semantics, API versioning, Swagger accuracy and exposure, health endpoints | backend | `backend/**/*.cs` | — | HTTP contract or endpoint-surface constraint |
| `.claude/rules/error-handling.md` | Error contracts, exception flow, expected outcomes, validation boundaries, failure logging, cancellation, dependency-failure and resilience semantics | backend | `backend/**/*.cs` | — | Failure-handling or validation-boundary constraint |
| `.claude/rules/performance.md` | Optimization discipline, async/cancellation, `TimeProvider`, `HttpClient` lifetime, database efficiency, caching semantics | backend | `backend/**/*.cs` | — | Runtime-efficiency or caching constraint |
| `.claude/rules/coding-style.md` | C# conventions, file/async naming, language-feature choices, logging-call style, style-change scope | backend | `backend/**/*.cs` | `.editorconfig` | C# convention not expressible in `.editorconfig` |
| `.claude/rules/security.md` | Secrets, trust boundaries, SQL safety, authentication/authorization, transport, cryptography, CORS, sensitive logging, fail-safe behavior, container runtime images | common | backend, frontend, config, manifests, scripts, Dockerfiles | — | Security invariant for code, config, or delivery files |
| `.claude/rules/testing.md` | Test framework, level, behavior focus, isolation, provider fidelity, test data, readability, coverage, naming | backend-tests | `backend/**/*Tests/**/*.cs`, `backend/**/*Tests/*.csproj` | — | Backend test constraint |
| `.claude/rules/dependencies.md` | Dependency need, NuGet Central Package Management, npm manager/lockfile/categories | common (manifests) | `**/*.csproj`, `**/Directory.Packages.props`, `**/package.json`, `**/package-lock.json` | `check-manifests.mjs` via manifest hooks | Manifest-level dependency constraint |
| `.claude/rules/angular.md` | Angular structure, components, HTTP boundary, state, routing, forms, interceptors, RxJS lifetime, API error handling | frontend | `frontend/**/*.ts`, `*.html`, `*.scss` | — | Frontend constraint (never only in the `angular` skill) |
| `.claude/rules/repository-structure.md` | Restraint in physical structure (no speculative projects, empty trees, generic buckets) | common | `backend/**`, `frontend/**`, `docs/**`, solution and build files | — | Repository-wide structural constraint |

### Workflow skills (`.claude/skills/`)

| File | Owns | Scope | Loads | Enforcement | Extend here when… |
| --- | --- | --- | --- | --- | --- |
| `.claude/skills/development-workflow/SKILL.md` | Implementation step order, specification read, behavior-source sync, persistence co-change and migration review, regression tests, performance-change procedure, generated output, API deprecation, CI/CD and production migrations, review and verify gates | common | Routed from `CLAUDE.md` | Stop hook reminders | A step or obligation of implementing a kind of change |
| `.claude/skills/verify/SKILL.md` | Verification procedure, behavioral-probe preservation, using cleanup in changed files, fix-and-retry, honest reporting | common | Routed from `CLAUDE.md`, `development-workflow` | — | A completion check |
| `.claude/skills/code-review/SKILL.md` | Review procedure, independence, priorities, findings format | common | Routed; preloaded by `code-reviewer` | Agent is read-only (`disallowedTools`) | A review step or output rule |
| `.claude/skills/build-fix/SKILL.md` | Repair procedure, diagnosis before editing, bounded iteration, no weakening of verification | common | Routed | — | A repair step |
| `.claude/skills/custom-settings/SKILL.md` | Settings propagation, database impact of settings | common | Routed; file-change hook reminder | `file-change.mjs` | A settings-synchronization step |
| `.claude/skills/git-workflow/SKILL.md` | Git procedure, user-work protection, commit scope | repo/meta | Routed | — | A Git procedure step |
| `.claude/skills/security-scan/SKILL.md` | Security review procedure, evidence and severity discipline, report format | common | Routed | — | A scan step or report rule |
| `.claude/skills/security-scan/references/scan-layers.md` | Per-layer investigation prompts (private) | common | Read by `security-scan` | — | A new investigation prompt |
| `.claude/skills/add-dependency/SKILL.md` | Version selection, due diligence, license approval gate, package-choice defaults, removal | common | Routed; dependency hooks | `dependency-guard.mjs` blocks npm force flags; manifest checks | A dependency-procedure step |
| `.claude/skills/architecture-decision/SKILL.md` | Decision Request format, decision recording | common | Routed from `CLAUDE.md` § Decision Control | — | Decision-recording procedure |
| `.claude/skills/project-structure/SKILL.md` | Scaffolding and restructuring procedure | common | Routed | `check-manifests.mjs` | A scaffolding step |
| `.claude/skills/project-structure/references/solution-layout.md` | Repository-level target layout and file conventions (private) | common | Read by `project-structure` | — | Repository-level scaffolding detail |
| `.claude/skills/project-structure/references/backend-layout.md` | Backend project contents, naming heuristics, Development configuration example (private) | backend | Read by `project-structure` | — | Backend scaffolding detail |
| `.claude/skills/template-maintenance/SKILL.md` | Maintenance procedure and structural invariants of this instruction system | repo/meta | User-invoked only (`disable-model-invocation`) | `check-instructions.mjs` | Changing how the instruction system itself is maintained |

### Knowledge skills (technique only)

Every knowledge skill loads on demand (when the task matches its description),
owns no policy, and has no mechanical enforcement; its `references/` files are
read only by that skill. Each starts by naming the rule files that own the
related policy.

| File | Technique for | Scope | Extend here when… |
| --- | --- | --- | --- |
| `.claude/skills/ef-core/SKILL.md` | DbContext, repositories/UoW implementation, queries, migrations commands, seeder implementation | backend | EF Core how-to or example |
| `.claude/skills/http-api/SKILL.md` | Status-code reference, idempotency, ETags, headers | backend | HTTP example or less-common status detail |
| `.claude/skills/aspnet-error-handling/SKILL.md` | `IExceptionHandler`, ProblemDetails, outcome mapping, FluentValidation wiring, Result technique | backend | Error-handling example |
| `.claude/skills/dotnet-testing/SKILL.md` | NUnit, test doubles, `WebApplicationFactory`, test databases, probes to tests | backend-tests | Test technique |
| `.claude/skills/logging/SKILL.md` | Log levels, scopes, correlation, `LoggerMessage` | backend | Logging technique |
| `.claude/skills/logging/references/serilog.md` | Serilog bootstrap, configuration, sinks, enrichers (private) | backend | Serilog detail |
| `.claude/skills/httpclient-factory/SKILL.md` | Client models, handlers, timeouts, response mapping, adapter tests | backend | Outbound HTTP technique |
| `.claude/skills/httpclient-factory/references/resilience.md` | Resilience pipelines, retry, circuit breaker, fallback, hedging (private) | backend | Resilience detail |
| `.claude/skills/configuration/SKILL.md` | Options pattern, validation, secrets providers | backend | Configuration example |
| `.claude/skills/dependency-injection/SKILL.md` | Lifetimes, layer registration, keyed services, decorators, Scrutor | backend | DI example |
| `.claude/skills/caching/SKILL.md` | HybridCache, output caching, keys, invalidation strategies | backend | Caching example |
| `.claude/skills/swagger/SKILL.md` | Swashbuckle setup, metadata, security definitions | backend | OpenAPI example |
| `.claude/skills/api-versioning/SKILL.md` | Asp.Versioning setup, strategies, deprecation mechanics | backend | Versioning example |
| `.claude/skills/health-check/SKILL.md` | Liveness/readiness setup, probes, exposure | backend | Health-check example |
| `.claude/skills/docker/SKILL.md` | Dockerfiles, Compose, non-root, probes | backend, frontend | Container example |
| `.claude/skills/ci-cd/SKILL.md` | Pipeline shapes, artifacts, scans, deployment | backend, frontend | Pipeline example |
| `.claude/skills/angular/SKILL.md` | Standalone components, signals/RxJS, data access, routing, tests | frontend | Angular example |
| `.claude/skills/modern-csharp/SKILL.md` | C# 14 features, modernization procedure | backend | Language-feature example |
| `.claude/skills/authentication/SKILL.md` | Schemes, policies, roles, resource authorization, current user | backend, frontend | Auth example |

### Agent

| File | Owns | Loads | Enforcement |
| --- | --- | --- | --- |
| `.claude/agents/code-reviewer.md` | Nothing normative; runs `code-review` in an isolated read-only context | Delegated subagent | `disallowedTools: Write, Edit, NotebookEdit` |

### Enforcement and delivery

| File | Purpose | Triggered by |
| --- | --- | --- |
| `.claude/settings.json` | Registers the hooks with shell-neutral `node …` commands | Claude Code |
| `.claude/hooks/hook-io.mjs` | Shared hook helpers (stdin JSON, project root, responses) | Imported by hooks |
| `.claude/hooks/dependency-guard.mjs` | Blocks npm force/legacy-peer-deps installs; after dependency commands, runs manifest checks and routes to `add-dependency` | PreToolUse/PostToolUse on Bash and PowerShell |
| `.claude/hooks/file-change.mjs` | Settings/specification sync reminders; manifest checks after editing `.csproj`, `Directory.Packages.props`, `package.json` | PostToolUse on Edit/Write/MultiEdit |
| `.claude/hooks/stop-co-change.mjs` | Once-per-change-set reminders: seeder co-change, migration review, tests for changed production code | Stop |
| `.claude/scripts/check-manifests.mjs` | CPM, version forms, deprecated/approval-gated packages, npm hygiene, project-reference direction | Hooks, `verify`, `add-dependency`, `project-structure`, CI |
| `.claude/scripts/check-instructions.mjs` | Structural checks of this instruction system | `template-maintenance`, CI |
| `.editorconfig` | Formatting, naming, unused-using diagnostics | IDE, `dotnet format`, build |
| `Directory.Build.props` | Shared .NET build settings | MSBuild |
| `Directory.Packages.props` | Central Package Management | NuGet restore |

### Product inputs (not instructions)

| File | Role |
| --- | --- |
| `SPECIFICATION.md` | Authoritative product behavior when non-empty; empty in the template |
| `CUSTOM_SETTINGS.md` | Approved tunable values table |

## Where Is the Rule For…?

| Topic | Authoritative owner |
| --- | --- |
| Normative vocabulary (must, default, prefer, requires approval) | `CLAUDE.md` § Normative Vocabulary |
| Specification authority, no invented behavior, product ambiguity, string semantics | `CLAUDE.md` § Product Specification |
| Product inputs cannot silently override engineering policy | `CLAUDE.md` § Product Specification |
| What belongs in `CUSTOM_SETTINGS.md`, spec/settings conflicts, inventing tunable values | `CLAUDE.md` § Custom Settings |
| Simplicity, no speculative frameworks, scope and behavior preservation | `CLAUDE.md` § Core Defaults |
| Challenging questionable requests | `CLAUDE.md` § Core Defaults |
| Adopted architecture, repository layout, CQRS/mediator not adopted | `CLAUDE.md` § Architecture Defaults |
| Decided/Delegated/Reserved, Reserved list, five-question test, headless runs | `CLAUDE.md` § Decision Control |
| Git mutations need an explicit request; parallel work isolation | `CLAUDE.md` § Git |
| Approved stack, Angular libraries, conditional technologies, Docker optional, `.slnx`, shared build files | `docs/technology-stack.md` |
| Layer dependencies, project and test references | `architecture.md` § Dependency Direction, § Project References |
| Simple vs. rich Domain, decorative DDD | `architecture.md` § Domain |
| Application Services, Application abstractions, no EF/transport types in Application | `architecture.md` § Application |
| Thin Controllers, composition root | `architecture.md` § API |
| Specific repositories, no `IQueryable` leaks, generic repository | `architecture.md` § Repositories, § Generic Repository |
| Unit of Work commit boundary, shared context, transactions | `architecture.md` § Unit of Work |
| EF Core inside Infrastructure | `architecture.md` § EF Core Boundary |
| Constructor injection, lifetimes, registration placement, typed options, Serilog registration | `architecture.md` § Composition and Dependency Injection |
| Cache/HTTP transport leaks, versioned models, DTO duplication | `architecture.md` § Boundary Contracts |
| Development seeding rules, local connection string | `persistence.md` |
| Status codes, empty collections, 401/403, 409/412 | `api.md` § HTTP Semantics |
| When to version an API, breaking changes, strategy | `api.md` § API Versioning |
| Swagger accuracy and environment exposure | `api.md` § Swagger / OpenAPI |
| Health checks | `api.md` § Health Checks |
| ProblemDetails, central exception handling, no leaked internals | `error-handling.md` § Error Contracts, § Unexpected Exceptions |
| Expected outcomes, Result pattern, business exceptions | `error-handling.md` § Expected Outcomes |
| Validation boundaries, FluentValidation use | `error-handling.md` § Validation Boundaries |
| Log exceptions once | `error-handling.md` § Failure Logging |
| Client cancellation is not a 500 | `error-handling.md` § Cancellation |
| Timeouts, retry safety, Retry-After, fallback, caller cancellation | `error-handling.md` § Dependency Failures and Resilience |
| Clarity before optimization, measured optimizations | `performance.md` |
| Async I/O, cancellation propagation, `TimeProvider`, `HttpClient` lifetime | `performance.md` |
| Database efficiency | `performance.md` § Database Access |
| Caching need, keys, invalidation, expiration | `performance.md` § Caching |
| C# conventions, file/async naming, structured logging calls, style-only rewrites | `coding-style.md` |
| Secrets, input trust, upload metadata, SQL parameterization | `security.md` |
| Server authorization, anonymous access, auth mechanisms, token validation, enumeration, CSRF, token storage | `security.md` § Authentication and Authorization |
| TLS, cryptography, CORS | `security.md` |
| Sensitive data and payloads in logs | `security.md` § Logging and Sensitive Data |
| Fail-safe checks, visible security misconfiguration | `security.md` § Failure Behavior |
| Production container image and root user | `security.md` § Containers |
| Test framework, level, behavior, isolation, provider fidelity, data, readability, coverage, naming | `testing.md` |
| Dependency need, Central Package Management, npm lockfile and categories | `dependencies.md` |
| Angular structure, components, signals/RxJS, HTTP boundary, interceptors, errors, lazy loading, forms, subscriptions | `angular.md` |
| No speculative projects, empty trees, or generic buckets | `repository-structure.md` |
| Read the specification first; inspect code first; sync durable product sources | `development-workflow` § 1–2 |
| Seeder co-change, migration review | `development-workflow` § Persistence model and migrations |
| Regression tests for bug fixes | `development-workflow` § Bug fixes |
| Performance-change procedure | `development-workflow` § Performance-motivated changes |
| Generated output fixed at the source | `development-workflow` § Generated output |
| API version deprecation | `development-workflow` § API version deprecation |
| CI truthfulness, frontend CI commands, production migrations | `development-workflow` § CI/CD and deployment |
| Review before verify; verify before completion | `development-workflow` § 4 |
| Verification steps, behavioral probes to tests, unused usings, fix-and-retry, reporting | `verify` |
| Review independence, priorities, no manufactured findings | `code-review` |
| Diagnose before fixing, bounded iteration, no weakened verification | `build-fix` |
| Settings propagation and database impact | `custom-settings` |
| Never discard user work, state-aware minimal Git operations, focused commits | `git-workflow` |
| Security findings need evidence; no single-scanner dependency | `security-scan` |
| Version selection, due diligence, license approval, npm force flags, resilience and versioning packages | `add-dependency` |
| Decision Request format and recording | `architecture-decision` |

## Where New Content Goes

1. Needed while planning, before any file is opened (governance, approval
   boundary, architecture or technology decision) → `CLAUDE.md` or
   `docs/technology-stack.md`. Keep these compact.
2. A constraint on files of an area → the matching rule in `.claude/rules/`; add
   a new flat rule only when no existing rule's topic and `paths` fit, and
   declare `paths` covering at least the scope that needs it.
3. A multi-step procedure, stop condition, or output format → the owning
   workflow skill (or a new workflow skill for a new kind of task).
4. Technique, examples, or depth → the matching knowledge skill; long
   skill-specific depth → that skill's `references/`.
5. Something mechanically checkable → `.claude/scripts/` or a hook, plus a
   concise rule that names the constraint.
6. Then update this map and run `node .claude/scripts/check-instructions.mjs`
   (`/template-maintenance`).
