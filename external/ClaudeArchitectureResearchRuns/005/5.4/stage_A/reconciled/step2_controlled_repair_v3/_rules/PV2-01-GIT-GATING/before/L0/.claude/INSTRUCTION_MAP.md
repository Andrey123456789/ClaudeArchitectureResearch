> Level: 3 Project · Owns: human-facing map of the instruction system (not auto-loaded) · Scope: repo/meta · Loads: never automatically; read by maintainers and template-maintenance · Depends on: none

# Instruction Map

This file is for maintainers. Claude does not load it automatically.

## How the system is organized

Instructions are organized by **stability**. Ask of any statement: *how fundamental and stable is it?*

```text
3 Project  ──depends on──▶  2 Technology  ──depends on──▶  1 Architecture  ──depends on──▶  0 Core
(this repo's choices,       (concrete frameworks,          (Clean Architecture roles,       (governance, decisions,
 layout, commands)           libraries, languages)          boundaries, contracts)           neutral principles)
```

- A **conformance dependency** (a rule that builds on another rule) may point only to the same or a more stable level. It is declared in each file's header (`Depends on:`) and checked mechanically.
- A **routing pointer** ("run `verify`", "see `layout.md`") is not a conformance dependency and may point in any direction.
- Levels 0 and 1 name no concrete technology beyond the fixed platform (.NET, C#, TypeScript; Git for repository safety). Protocols and standards (HTTP, TLS, OIDC, CSRF, SQL) are vocabulary, not technologies.
- **Product inputs** — `SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, feature specifications, task prompts — sit outside the levels. They define behavior and values; they are not instruction layers.

**Loading** is independent of level: CLAUDE.md and its two imports are always loaded; rule files load when Claude reads a file matching their `paths`; skills load when invoked; workflows explicitly read the rules they depend on (path rules may not have fired in a new repository).

**Responsibilities:** rule = normative constraint · workflow skill = procedure · knowledge skill = technique · product files = inputs · hooks/scripts/config = deterministic enforcement. Each rule has exactly one owner; other files point to it.

## Level 0 — Core

| File | Owns | Scope | Loads | Enforcement | Extend here when… |
|---|---|---|---|---|---|
| `CLAUDE.md` | precedence, vocabulary, product governance, decision control (classes, Reserved list, Decision Request, headless rule), challenge obligation, simplicity and scope, Git safety, work routing | common | always | product-input edit reminder (hook); structure checker | a technology-neutral rule must be known at planning time |
| `0-core/security-principles.md` | secrets, trust boundaries, SQL parameterization, server-side authorization, anonymous access, auth facilities, token validation, enumeration, CSRF, token storage, TLS, custom crypto, CORS, failing safely, error and health-response exposure | common | path: code, config, manifests, env, Dockerfiles | `security-scan` workflow | a stack-independent security rule is needed |
| `0-core/logging-principles.md` | never-log data, payload logging, log-once | common | path: `backend/**`, `frontend/**` | — | a stack-independent logging rule is needed |
| `0-core/testing-principles.md` | test level, behavior focus, provider fidelity, determinism and isolation, test-owned data, explicit cases, naming, coverage | backend-tests (+ frontend tests) | path: backend test projects, `*.spec.ts`, `e2e/` | stop-hook test reminder | a framework-neutral test rule is needed |
| `0-core/dependency-hygiene.md` | current need, narrowest scope, removal | common | path: manifests | manifest hook | a package-manager-neutral dependency rule is needed |
| `0-core/runtime-principles.md` | optimization evidence, data-access efficiency, caching semantics, external-call bounds/retries/fallback, cancellation, health-check semantics | backend | path: `backend/**/*.cs` | — | a stack-independent runtime rule is needed |
| `.claude/skills/git-workflow/SKILL.md` | Git procedure: state inspection, focused staging/commits, branches, worktrees, push, merge/rebase, PRs, destructive operations | repo/meta | on invocation | — | Git procedure changes |
| `.claude/skills/template-maintenance/SKILL.md` | maintaining this instruction system (user-only) | repo/meta | user invocation only (`disable-model-invocation`) | runs the structure checker | the maintenance procedure changes |

## Level 1 — Architecture

| File | Owns | Scope | Loads | Enforcement | Extend here when… |
|---|---|---|---|---|---|
| `1-architecture/overview.md` | adopted architecture, patterns not adopted (CQRS/mediator/VSA owned here), accepted architecture decisions — **decision summary** | backend, frontend | always (imported) | manifest hook flags mediator packages | an architecture decision is accepted (`architecture-decision`) |
| `1-architecture/backend-layers.md` | dependency direction, Domain and Application responsibilities, adapter boundaries (remote HTTP, cache), composition root, DI | backend | path: `backend/**/*.cs`, `*.csproj` | manifest hook rejects outward project references | a layer responsibility or composition rule changes |
| `1-architecture/persistence-boundary.md` | persistence framework as Infrastructure detail, specific repositories, no queryable/framework leakage, generic repository, Unit of Work, explicit transactions | backend | path: backend | — | repository/UoW/boundary rules change |
| `1-architecture/entry-points.md` | thin entry points, transport contracts, problem-details contract shape, status semantics (2xx, empty collection, 401/403/404, 409/412), versioning, documentation truth | backend | path: backend | — | Api boundary or public HTTP contract rules change |
| `1-architecture/outcomes.md` | expected outcomes vs exceptions, no forced Result, centralized unexpected-failure handling, catching, validation boundaries | backend | path: `backend/**/*.cs` | — | error-flow or validation-boundary rules change |
| `1-architecture/frontend-structure.md` | feature organization, lazy loading, presentation focus, frontend HTTP boundary, simple state, API error contract, frontend validation role | frontend | path: `frontend/**` | — | frontend structural rules change |
| `1-architecture/code-organization.md` | physical structure by responsibility, type-role naming, narrow test-project references | common, backend-tests | path: `backend/**`, `frontend/**`, `docs/**`, `*.slnx` | — | physical organization rules change |
| `.claude/skills/architecture-decision/SKILL.md` | Decision Request preparation, recording accepted decisions in the two summaries, API version deprecation | common | on invocation | — | the decision procedure changes |

## Level 2 — Technology

| File | Owns | Scope | Loads | Enforcement | Extend here when… |
|---|---|---|---|---|---|
| `2-technology/csharp.md` | C#/.NET conventions: style scope, files and naming, async, `CancellationToken`, `TimeProvider`, `HttpClient` lifetime, typed options | backend | path: `backend/**/*.cs` | `.editorconfig`, `Directory.Build.props` (IDE0005 in build) | a C#/.NET convention changes |
| `2-technology/aspnet-core.md` | Controllers, transport types, ProblemDetails/ValidationProblemDetails, `IExceptionHandler`, Swagger UI exposure, authentication/Identity and Data Protection facilities | backend | path: backend code, appsettings, launchSettings | — | an ASP.NET Core binding changes |
| `2-technology/ef-core.md` | which types are persistence-framework types, entity configurations, UoW over `DbContext`, Infrastructure-only base repository | backend | path: backend | — | the persistence framework binding changes |
| `2-technology/fluentvalidation.md` | FluentValidation use at the owning boundary, registration, single invocation mechanism | backend | path: `backend/**/*.cs` | manifest hook flags legacy integration package | the validation library binding changes |
| `2-technology/dotnet-testing.md` | NUnit, `WebApplicationFactory` integration tests, EF InMemory limits | backend-tests | path: backend test projects | — | the backend test stack changes |
| `2-technology/angular.md` | standalone APIs, Signals vs RxJS, subscriptions, interceptors, reactive forms, test runner discovery | frontend | path: `frontend/**` | — | an Angular binding changes |
| `2-technology/logging.md` | `ILogger<T>` structured templates, Serilog `AddSerilog` integration | backend | path: backend code, appsettings | manifest hook flags deprecated sink | the logging API/provider binding changes |
| `2-technology/containers-ci.md` | production runtime image, non-root, external configuration; routes CI/container work to `delivery-pipeline` | backend, delivery | path: Dockerfiles, Compose, CI definitions | — | a container/CI binding changes |
| Knowledge skills (technique only, never sole owners of a rule) | `.claude/skills/ef-core/SKILL.md`, `.claude/skills/http-api/SKILL.md`, `.claude/skills/aspnet-error-handling/SKILL.md`, `.claude/skills/dotnet-testing/SKILL.md`, `.claude/skills/logging/SKILL.md` (+ private `.claude/skills/logging/references/serilog.md`), `.claude/skills/httpclient-factory/SKILL.md` (+ private `.claude/skills/httpclient-factory/references/resilience.md`), `.claude/skills/configuration/SKILL.md`, `.claude/skills/dependency-injection/SKILL.md`, `.claude/skills/caching/SKILL.md`, `.claude/skills/swagger/SKILL.md`, `.claude/skills/api-versioning/SKILL.md`, `.claude/skills/health-check/SKILL.md`, `.claude/skills/docker/SKILL.md`, `.claude/skills/ci-cd/SKILL.md`, `.claude/skills/angular/SKILL.md`, `.claude/skills/modern-csharp/SKILL.md`, `.claude/skills/authentication/SKILL.md` | per skill | on invocation (descriptions are always listed) | — | technique, examples, or depth for a technology; a new rule goes to a rule file instead |

## Level 3 — Project

| File | Owns | Scope | Loads | Enforcement | Extend here when… |
|---|---|---|---|---|---|
| `3-project/decisions.md` | approved stack, conditional technologies, not-added-by-default libraries, repository defaults, accepted project decisions — **decision summary** | common | always (imported) | manifest hook review lists | a stack/default decision is accepted (`architecture-decision`) |
| `3-project/package-management.md` | NuGet Central Package Management, npm lockfile and dependency categories | backend, frontend | path: manifests | manifest hook (versions in csproj, CPM flag, floating/prerelease versions, tooling category, `.npmrc` bypass) | package-manager choices change |
| `3-project/data-lifecycle.md` | Development seeding (representative, Infrastructure-owned, dedicated seeder, Development-only, no schema changes, no overwrite, valid data), local Development database configuration | backend | path: backend code, appsettings | stop-hook seed reminder | Development data handling changes |
| `3-project/layout.md` | layer-to-project mapping, test projects and typical references, frontend workspace location | backend, backend-tests, frontend | path: `*.slnx`, backend `*.csproj`, `angular.json` | manifest hook (project-reference direction, reference-graph changes reported) | project naming or placement changes |
| `.claude/skills/development-workflow/SKILL.md` | implementation procedure: product-input reads, owner reads, inspection, bug-fix regression tests, performance changes, approved product decisions, seed/migration co-changes, review then verify | common | on invocation (routed from CLAUDE.md) | stop-hook co-change reminders | the development procedure changes |
| `.claude/skills/project-structure/SKILL.md` (+ private `.claude/skills/project-structure/references/solution-layout.md`, `.claude/skills/project-structure/references/backend-layout.md`) | scaffolding and restructuring procedure, directory examples | common | on invocation | pre-bash blocks project-reference commands; manifest hook reports project and reference changes | scaffolding steps change |
| `.claude/skills/verify/SKILL.md` | verification procedure, probe preservation, changed-file import cleanup, fix-and-retry, PASS/NOT RUN reporting | common | on invocation | — | verification steps change |
| `.claude/skills/code-review/SKILL.md` | review procedure, priorities, no manufactured findings, findings format | common | on invocation; read by the agent | — | review criteria change |
| `.claude/agents/code-reviewer.md` | independent read-only reviewer that follows `code-review` | common | on delegation | `disallowedTools` | reviewer role changes (criteria stay in `code-review`) |
| `.claude/skills/build-fix/SKILL.md` | bounded repair loop, no weakened verification, generated outputs fixed at the source | common | on invocation | — | repair procedure changes |
| `.claude/skills/custom-settings/SKILL.md` | tunable-setting synchronization, persistence impact | common | on invocation; hook reminder | product-input hook | synchronization steps change |
| `.claude/skills/add-dependency/SKILL.md` | version selection, due diligence, license approval, conditional package bindings (versioning, resilience), install, no peer-conflict bypass | common | on invocation; hook routing | pre-bash blocks npm/pnpm/yarn `--force`/`-f`/`--legacy-peer-deps`; post-bash (actual manifest state) and post-edit route dependency changes here | dependency procedure changes |
| `.claude/skills/security-scan/SKILL.md` (+ private `.claude/skills/security-scan/references/scan-layers.md`) | evidence-based security review, severity discipline, tool independence, report shape | common | on invocation | — | security review procedure changes |
| `.claude/skills/delivery-pipeline/SKILL.md` | CI truthfulness, frontend CI commands and lockfile installs, production migrations as deployment work | common, frontend, backend | on invocation (routed by `containers-ci.md`) | — | delivery procedure changes |

## Product inputs (not instruction layers)

| File | Role |
|---|---|
| `SPECIFICATION.md` | authoritative project-specific behavior when non-empty (empty in the template on purpose) |
| `CUSTOM_SETTINGS.md` | approved tunable values; changes run `custom-settings` |

## Enforcement assets

| File | What it does |
|---|---|
| `.claude/settings.json` | registers the hooks in exec form — `"command": "node"`, `"args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/claude-hook.mjs", "<event>"]` — so each hook starts from any working directory without shell expansion: PreToolUse `Bash\|PowerShell` → `pre-bash` with `"onFailure": "block"`; PostToolUse and PostToolUseFailure `Bash\|PowerShell` → `post-bash`; PostToolUse `Edit\|MultiEdit\|Write` → `post-edit`; Stop → `stop` |
| `.claude/hooks/claude-hook.mjs` | `pre-bash` (fails closed): blocks npm/pnpm/yarn force/legacy-peer flags and `dotnet add/remove … reference` / `dotnet reference add/remove` before they run, also behind global options such as `--prefix`, `--dir`, `--cwd` · `post-bash`, after successful and failed shell calls: compares the active worktree's manifests (tracked and untracked, not ignored) with a per-worktree snapshot kept in the Git directory, validates added and changed manifests, reports removals and moves, routes dependency and project-reference changes; the first observation of a worktree validates every manifest · `post-edit`: manifest checks, dependency and reference-change routing, product-input reminder, structure check after instruction edits · `stop`: co-change reminders (seed, migrations, tests, custom settings) repeated only when the changed files or their content differ, never loops |
| `.claude/hooks/manifest-checks.mjs` | central versions, `VersionOverride`, floating/prerelease versions, deny/review package lists (approved exceptions are read from the "Accepted" sections of the decision summaries), npm tooling category, `.npmrc` bypass, outward project references; reads UTF-8, UTF-8 with BOM, and BOM-tagged UTF-16 files and reports undecodable ones |
| `.claude/tools/check-instructions.mjs` | structure checker: `node "$(git rev-parse --show-toplevel)/.claude/tools/check-instructions.mjs"` (Bash or PowerShell, from any directory of the repository or worktree) — level-first layout, headers, `paths`, Level 0/1 neutrality, dependency direction and cycles, imports, references, private references, hook registrations (exec form, launcher placeholder, required events including PostToolUseFailure, fail-closed PreToolUse only), this map's completeness, always-loaded estimate |
| `.editorconfig`, `Directory.Build.props`, `Directory.Packages.props`, `.gitignore` | formatting/code style (IDE0005 surfaced in build), shared build settings, Central Package Management, ignored artifacts |

Hooks need Node.js (already required by the Angular workspace) and Git on `PATH`. The hook locates itself through the project-directory placeholder, but checks the repository Claude is working in — resolved through Git from the hook input `cwd` or the edited file — so nested directories and linked worktrees are checked against their own content; a repository without this instruction system (for example an unrelated nested clone) is not checked. If a check cannot run (no Git work tree, unreadable input), the hook exits with a visible message instead of skipping silently; the PreToolUse guard blocks the shell call instead. Outside a Git work tree there is no manifest snapshot, so `post-bash` scans every manifest only after a recognized dependency command.

## Split statements

Mixed statements are split so each part lives at the level of what it depends on:

| Neutral rule (stable level) | Technology binding (Level 2) | Project selection (Level 3) |
|---|---|---|
| Domain/Application free of persistence-framework and transport types (`backend-layers.md`) | `DbContext`, `DbSet<T>`, EF APIs are persistence-framework types (`ef-core.md`); `IActionResult`, `HttpContext`, … are transport types (`aspnet-core.md`) | EF Core + SQL Server, ASP.NET Core (`decisions.md`) |
| Repository contracts expose no framework query types (`persistence-boundary.md`) | EF expression and set types named (`ef-core.md`) | — |
| Thin HTTP entry points (`entry-points.md`) | ASP.NET Core Controllers; no Minimal API groups (`aspnet-core.md`) | Controllers approved (`decisions.md`) |
| Structured problem-details error contract (`entry-points.md`) | `ProblemDetails` / `ValidationProblemDetails` (`aspnet-core.md`) | — |
| Centralized unexpected-failure handling (`outcomes.md`) | `IExceptionHandler` (`aspnet-core.md`) | — |
| Validation at the owning boundary (`outcomes.md`) | FluentValidation usage (`fluentvalidation.md`) | FluentValidation approved (`decisions.md`) |
| No custom crypto/auth when platform facilities fit (`security-principles.md`) | ASP.NET Core Identity, Data Protection (`aspnet-core.md`) | — |
| Framework-neutral testing principles (`testing-principles.md`) | NUnit, `WebApplicationFactory`, EF InMemory (`dotnet-testing.md`) | NUnit, test placement (`decisions.md`, `layout.md`) |
| Mediator-based organization not adopted (`overview.md`) | — | MediatR/Kommand not added (`decisions.md`) |
| Frontend structure and validation role (`frontend-structure.md`) | standalone APIs, reactive forms (`angular.md`) | Angular baseline (`decisions.md`) |
| Logging principles (`logging-principles.md`) | `ILogger<T>`, Serilog integration (`logging.md`) | Serilog provider (`decisions.md`) |
| Dependency hygiene (`dependency-hygiene.md`) | — | NuGet CPM, npm (`package-management.md`) |
| Swagger UI exposure (`aspnet-core.md`) | — | Swashbuckle baseline (`decisions.md`) |

Replacing a technology (for example NUnit with xUnit) means editing its Level 2 module, the Level 3 selection, and the workflows or assets where the choice is embedded; Levels 0 and 1 stay unchanged.

## Where does a new rule go?

1. Depends on this repository's selection, layout, defaults, or commands → Level 3.
2. Names a technology beyond the fixed platform → Level 2.
3. Presupposes the architecture, a layer, role, or boundary → Level 1.
4. Otherwise → Level 0.

Then pick the artifact by responsibility and trigger: planning-time rule → CLAUDE.md or a decision summary; file-scoped rule → a path rule covering at least its scope; procedure → a workflow skill; technique → a knowledge skill; mechanical check → a hook or script. Run `template-maintenance`.
