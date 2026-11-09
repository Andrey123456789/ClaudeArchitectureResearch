> **Instruction map** · Owns: human-facing index of every instruction artifact — owner, scope, loading, enforcement, extension point · Scope: repo/meta · Loading: never auto-loaded (maintainers; read by `template-maintenance`)

# Instruction Map

## How the System Works

- **Policy** lives in `CLAUDE.md` and its imported planning records (always
  loaded) and in flat path-scoped rules under `.claude/rules/` (loaded with
  matching files). Each policy has exactly one owner; other files only point to it.
- **Procedures** live in workflow skills; **technique** lives in knowledge skills
  and their private `references/`; **product inputs** are `SPECIFICATION.md` and
  `CUSTOM_SETTINGS.md`; **deterministic enforcement** is the hooks, scripts, and
  build configuration.
- **Capabilities**: four replaceable slots (architecture frame, persistence,
  backend-testing, optional frontend). Their selection is the always-loaded
  `docs/capability-selection.md`; implementation-owned files carry
  `Capability: <slot>/<implementation>` in their header. Everything else is
  embedded and refers to slots by role.
- **Where a new rule belongs**: needed while planning → `CLAUDE.md` or a `docs/`
  planning record; needed while editing certain files → the topical rule whose
  `paths` match (or a new flat rule); specific to a capability implementation →
  that implementation's facet; a procedure → a workflow; examples → a knowledge
  skill. Run `node .claude/scripts/check-instructions.mjs` afterwards.

## Normal View

### Always Loaded

| File | Owns | Scope | Loading | Enforcement | Extend here |
|---|---|---|---|---|---|
| `CLAUDE.md` | product-source authority, engineering defaults, challenge obligation, decision control (Reserved list, Decision Requests, headless rule), procedure routing, Git boundary | common, repo/meta | always (root) | instruction checker | operating policy needed at planning time |
| `docs/technology-stack.md` | approved stack, conditional technologies, solution/build configuration, repository layout | common, backend, backend-tests | always (`@` import from `CLAUDE.md`) | `check-dependencies.mjs` deny-list | approved or conditional technology decisions |
| `docs/capability-selection.md` | slot → selected implementation, declared properties, facet roles, imports of always-loaded facets | common | always (`@` import from `CLAUDE.md`) | instruction checker (selection, facets, leaks) | selection changes (Reserved, ADR) |
| `docs/architecture.md` | adopted architecture, stable-role mapping, patterns not adopted | backend | always (`@` import from the selection record) | instruction checker | frame-level architecture decisions |
| `docs/frontend-stack.md` | frontend technology baseline, default-excluded libraries, conditional E2E | frontend | always (`@` import from the selection record) | `check-dependencies.mjs` (default-excluded packages) | frontend technology decisions |

### Path-Scoped Rules (`.claude/rules/`, flat)

| File | Owns | Scope | Loading (paths) | Enforcement | Extend here |
|---|---|---|---|---|---|
| `.claude/rules/architecture-style.md` | dependency direction, layer responsibilities, repositories and Unit of Work, registration, transport contracts, test-project references | backend, backend-tests | `backend/**/*.cs`, `backend/**/*.csproj` | `check-architecture.mjs` | layer and placement rules |
| `.claude/rules/persistence-technology.md` | persistence-technology usage, development seeding, provider configuration, mechanisms | backend | backend code, project files, appsettings | `check-architecture.mjs` (package placement), stop hook (seeder/migration co-change) | persistence-technology rules |
| `.claude/rules/api.md` | HTTP status semantics, API versioning, Swagger accuracy/exposure, health endpoints | backend | backend code, appsettings, launchSettings | — | HTTP API surface rules |
| `.claude/rules/error-handling.md` | expected outcomes, exception flow, error logging boundary, HTTP error contracts, cancellation, validation boundaries | backend | `backend/**/*.cs` | — | error and validation rules |
| `.claude/rules/backend-runtime.md` | DI usage, typed configuration, logging, outbound calls and retries, cache correctness | backend | backend code, appsettings | — | runtime behavior rules |
| `.claude/rules/performance.md` | correctness-first optimization, async/cancellation, TimeProvider, HttpClient lifetime, database efficiency, when to cache, measured optimizations | backend | `backend/**/*.cs` | — | performance rules |
| `.claude/rules/coding-style.md` | C# conventions, file/namespace and async naming, style-scope discipline | backend | `backend/**/*.cs` | `.editorconfig`, `Directory.Build.props` | C# style rules |
| `.claude/rules/security.md` | secrets, input trust, SQL parameterization, authorization/authentication, transport, cryptography, CORS, browser credentials, fail-safe checks, uploads, sensitive logging, containers | common, backend, frontend | backend, frontend, configuration, manifests, container files | `check-dependencies.mjs` (deny-list) | security invariants |
| `.claude/rules/testing.md` | framework-independent test policy | backend-tests | backend test projects | stop hook (test co-change) | neutral test policy |
| `.claude/rules/test-framework.md` | default test framework, packages, vocabulary binding | backend-tests | backend test projects | `check-architecture.mjs` (test markers) | framework-specific test rules |
| `.claude/rules/frontend.md` | framework-independent frontend structure, data access, state, API errors, forms | frontend | `frontend/**/*` | — | neutral frontend rules |
| `.claude/rules/frontend-framework.md` | framework API style, Signals/RxJS, interceptors, subscriptions | frontend | `frontend/**/*` | — | framework-specific frontend rules |
| `.claude/rules/dependencies.md` | dependency need, NuGet Central Package Management, npm lockfile and categories | common, backend, frontend | `**/*.csproj`, `**/Directory.Packages.props`, `**/package.json`, `**/package-lock.json` | `check-dependencies.mjs`, PostToolUse hook | dependency rules |
| `.claude/rules/repository-structure.md` | structure follows actual responsibilities | common | backend, frontend, docs, solution and build files | — | structural rules |

### Workflow Skills (procedures)

| File | Owns | Scope | Loading | Enforcement | Extend here |
|---|---|---|---|---|---|
| `.claude/skills/development-workflow/SKILL.md` | implementation procedure and change-specific obligations (spec sync, seeder, migrations, performance, regression, API deprecation, CI/CD, deployment migrations) | common | routed from `CLAUDE.md` | stop hook reminders | new implementation-time obligations |
| `.claude/skills/verify/SKILL.md` | completion verification, behavioral-probe preservation, changed-file using hygiene, reporting | common | routed from `development-workflow` | checkers it runs | completion checks |
| `.claude/skills/code-review/SKILL.md` | review procedure, priorities, findings format | common | routed; preloaded by the reviewer agent | — | review steps |
| `.claude/skills/build-fix/SKILL.md` | build/test repair loop | common | routed from `CLAUDE.md` | — | repair procedure |
| `.claude/skills/custom-settings/SKILL.md` | settings synchronization, schema-affecting setting co-changes | common, backend | routed; settings hook reminder | PostToolUse and stop hooks | settings procedure |
| `.claude/skills/git-workflow/SKILL.md` | Git procedure, protection of user work, focused commits | repo/meta | routed from `CLAUDE.md` | — | Git procedure |
| `.claude/skills/security-scan/SKILL.md` | static security review procedure, severity discipline, report shape | common | routed from `CLAUDE.md` / `code-review` | — | security review procedure |
| `.claude/skills/project-structure/SKILL.md` | scaffolding and restructuring procedure | common | routed from `CLAUDE.md` / `development-workflow` | `check-architecture.mjs` | scaffolding steps |
| `.claude/skills/add-dependency/SKILL.md` | dependency change procedure, license approval, conditional package choice | common | routed; dependency hook | PostToolUse hook, `check-dependencies.mjs` | dependency procedure |
| `.claude/skills/architecture-decision/SKILL.md` | Decision Requests, ADRs (`docs/decisions/`), decision-source synchronization | common | routed from `CLAUDE.md` | — | decision procedure |
| `.claude/skills/template-maintenance/SKILL.md` | instruction-system maintenance, capability replacement | repo/meta | user-invoked only | `check-instructions.mjs` | maintenance procedure |

Private workflow references: `.claude/skills/project-structure/references/solution-layout.md` (repository layout technique), `.claude/skills/project-structure/references/backend-layout.md` (backend layout; architecture facet), `.claude/skills/security-scan/references/scan-layers.md` (per-layer investigation prompts).

### Knowledge Skills (technique, on demand)

| File | Owns | Scope |
|---|---|---|
| `.claude/skills/ef-core/SKILL.md` | persistence technique (persistence facet) | backend |
| `.claude/skills/http-api/SKILL.md` | HTTP status-code reference | backend |
| `.claude/skills/aspnet-error-handling/SKILL.md` | error-handling and validation technique | backend |
| `.claude/skills/dotnet-testing/SKILL.md` | backend testing technique; private `.claude/skills/dotnet-testing/references/test-framework.md` (backend-testing facet) | backend-tests |
| `.claude/skills/logging/SKILL.md` | logging technique; private `.claude/skills/logging/references/serilog.md` | backend |
| `.claude/skills/httpclient-factory/SKILL.md` | outbound HTTP technique; private `.claude/skills/httpclient-factory/references/resilience.md` | backend |
| `.claude/skills/configuration/SKILL.md` | configuration technique | backend |
| `.claude/skills/dependency-injection/SKILL.md` | DI technique | backend |
| `.claude/skills/caching/SKILL.md` | caching technique | backend |
| `.claude/skills/swagger/SKILL.md` | Swagger/OpenAPI technique | backend |
| `.claude/skills/api-versioning/SKILL.md` | API versioning technique | backend |
| `.claude/skills/health-check/SKILL.md` | health-check technique | backend |
| `.claude/skills/docker/SKILL.md` | container technique | backend, frontend |
| `.claude/skills/ci-cd/SKILL.md` | CI/CD technique | common |
| `.claude/skills/angular/SKILL.md` | frontend technique, scaffold/verify commands (frontend facet) | frontend |
| `.claude/skills/modern-csharp/SKILL.md` | modern C# technique | backend |
| `.claude/skills/authentication/SKILL.md` | authentication/authorization technique | backend, frontend |

Knowledge skills own no policy; each starts with a pointer to the rules it
illustrates. Add new technique to the matching skill, or create a skill only for
a new technology area.

### Agent

| File | Owns | Scope | Loading | Extend here |
|---|---|---|---|---|
| `.claude/agents/code-reviewer.md` | independent read-only review role; preloads `code-review` | common | on demand (delegated review) | review criteria go to `code-review`, not here |

### Product Inputs (not instruction layers)

| File | Holds | Read by |
|---|---|---|
| `SPECIFICATION.md` | product behavior (empty in the template by design) | `development-workflow`, `code-review` |
| `CUSTOM_SETTINGS.md` | approved tunable values | `custom-settings`, `development-workflow` |

### Deterministic Enforcement

| File | Purpose | Trigger |
|---|---|---|
| `.claude/settings.json` | hook registration; shell-neutral `node` commands | Claude Code |
| `.claude/hooks/post-tool-use.mjs` | dependency-command routing, manifest checks, product-source reminders, instruction checks after edits | PostToolUse (Edit, Write, MultiEdit; Bash, PowerShell) |
| `.claude/hooks/stop.mjs` | seeder/migration/test/settings co-change reminders from the Git working tree; once per change set | Stop |
| `.claude/scripts/check-instructions.mjs` | instruction structure, references, capability conformance, leak check, always-loaded estimate | manual, hooks, `verify` |
| `.claude/scripts/check-architecture.mjs` | project-reference graph and technology-package placement from the frame/leaf manifests | manual, hooks, `verify` |
| `.claude/scripts/check-dependencies.mjs` | Central Package Management, floating/prerelease versions, deny-list, default-excluded frontend packages, lockfiles | manual, hooks, `verify` |
| `.claude/scripts/dependency-policy.json` | deny/warn package data | read by `check-dependencies.mjs` |
| `.claude/scripts/lib/template.mjs` | shared helpers (root resolution, parsing, globbing) | imported by checkers and hooks |
| `.claude/.gitignore` | keeps hook state (`.claude/.cache/`) out of Git | Git |
| `.editorconfig` | formatting and code style (including IDE0005 unused usings) | IDE, `dotnet format`, build |
| `Directory.Build.props` | shared .NET build settings | MSBuild |
| `Directory.Packages.props` | Central Package Management | MSBuild |

Hooks and scripts require Node.js 18+ on `PATH`; they resolve the project root
from `CLAUDE_PROJECT_DIR` or the hook input and fail with a clear message when it
cannot be found.

## Capability View

| Slot | Status | Selected | Runtime facets (role → file, loading) | Declared bindings / properties |
|---|---|---|---|---|
| architecture | required frame | clean-architecture | architecture-decision → `docs/architecture.md` (always); architecture-rule → `.claude/rules/architecture-style.md` (path); backend-layout → `.claude/skills/project-structure/references/backend-layout.md` (workflow read) | stable roles and their mapping; layers Domain/Application/Infrastructure/Api; test-project reference limits |
| persistence | required | ef-core (provider sqlserver) | persistence-rule → `.claude/rules/persistence-technology.md` (path); persistence-knowledge → `.claude/skills/ef-core/SKILL.md` (on demand) | uses frame roles only (no `binds:`); string comparison follows database collation; migration and seeding mechanisms; relational-testing binding; co-change patterns |
| backend-testing | required | nunit | test-framework-rule → `.claude/rules/test-framework.md` (path); test-framework-reference → `.claude/skills/dotnet-testing/references/test-framework.md` (on demand) | uses the frame's test-project role; packages; test-project markers; vocabulary binding |
| frontend | optional (enabled) | angular | frontend-stack → `docs/frontend-stack.md` (always); frontend-framework-rule → `.claude/rules/frontend-framework.md` (path); frontend-knowledge → `.claude/skills/angular/SKILL.md` (on demand) | workspace `frontend/<Name>.Web`; npm; default-excluded packages; framework CLI dependency commands |

Maintainer metadata (not loaded in normal sessions):
`.claude/capabilities/architecture/CONTRACT.md`,
`.claude/capabilities/architecture/clean-architecture/MODULE.md`,
`.claude/capabilities/persistence/CONTRACT.md`,
`.claude/capabilities/persistence/ef-core/MODULE.md`,
`.claude/capabilities/backend-testing/CONTRACT.md`,
`.claude/capabilities/backend-testing/nunit/MODULE.md`,
`.claude/capabilities/frontend/CONTRACT.md`,
`.claude/capabilities/frontend/angular/MODULE.md`.

Replacing an implementation: `template-maintenance` (after an ADR through
`architecture-decision`).
