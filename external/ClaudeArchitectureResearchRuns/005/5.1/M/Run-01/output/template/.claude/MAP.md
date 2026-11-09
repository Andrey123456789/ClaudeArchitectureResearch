> Owns: human-facing map of the instruction system (files, owners, scopes, loading, enforcement, extension points) | Scope: repo/meta | Loads: never auto-loaded; read by maintainers and template-maintenance

# Instruction Map

How the system works:

- **Always loaded:** `CLAUDE.md` plus the imported `docs/technology-stack.md` —
  planning-time policy and decisions.
- **Path-loaded:** flat topical rules in `.claude/rules/`, loaded when matching
  files are touched. Workflows read the rules they depend on explicitly when the
  files may not have been touched yet.
- **Workflows:** procedure skills that `CLAUDE.md` routes to; they own steps,
  stop conditions, and output shape, and point to rules instead of restating them.
- **Knowledge skills:** on-demand technique and examples; never the owner of a
  must/default rule. Private `references/` files are read only by their skill.
- **Enforcement:** hooks, scripts, and build/format configuration check what is
  mechanical; their messages point to the owner.
- **Product inputs:** `SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, feature specs, and
  task prompts — inputs governed by `CLAUDE.md`, not instruction layers.

Every policy has exactly one owner. Elsewhere it appears only as a pointer or a
check-by-reference item. The one designated decision summary is the first
paragraph of `CLAUDE.md` — Architecture Defaults, which restates the adopted
architecture for planning; `architecture.md` owns those rules. Run
`node .claude/scripts/check-instructions.mjs` after any change.

## Where Each Policy Lives

| Topic | Owner |
|---|---|
| Specification authority, invented behavior, ambiguity approval, string semantics, durable-source sync, custom-settings ownership, exclusions, and conflicts | `CLAUDE.md` — Product Sources |
| Proportional simplicity, no speculative frameworks/infrastructure/structure, scope and behavior preservation | `CLAUDE.md` — Core Defaults |
| Adopted architecture and patterns not adopted | `CLAUDE.md` — Architecture Defaults |
| Decided/Delegated/Reserved, Reserved list (approval gate), five-question test, headless behavior | `CLAUDE.md` — Decision Control |
| Challenging questionable requests | `CLAUDE.md` — Challenge Before Implementing |
| Read specification first, inspect code first, review before verify, verify before completion, never weaken verification, workflow routing | `CLAUDE.md` — Development Workflow |
| Git consent, never destroying user work, parallel-work isolation | `CLAUDE.md` — Git |
| Platform, persistence, validation, logging, Swagger (including UI exposure), testing, Angular stacks; non-default libraries; conditional technologies; resilience packages; Docker optionality; repository layout; `.slnx`; shared build files | `docs/technology-stack.md` |
| Dependency direction, test-project references, Domain/Application/API boundaries, DTO duplication, repositories, generic repository, Unit of Work, EF Core boundary, cache and remote-HTTP boundaries, DI and typed configuration | `.claude/rules/architecture.md` |
| Development seeding, migration review, production migrations, local Development connection string | `.claude/rules/persistence.md` |
| C# conventions, file/namespace/async naming, using-directive hygiene, no unrelated style rewrites | `.claude/rules/coding-style.md` |
| Async and cancellation propagation, `TimeProvider`, `HttpClient` lifetime, database efficiency, caching need/keys/expiration/invalidation, measured optimizations, performance-change procedure | `.claude/rules/performance.md` |
| Expected outcomes, exceptions as control flow, centralized unexpected failures, validation boundaries, client cancellation, log-once, structured logging, Serilog registration, outbound timeouts/retries/Retry-After/fallback/caller cancellation | `.claude/rules/error-handling.md` |
| HTTP status ownership and semantics, `ProblemDetails`, no leaked internals, Swagger accuracy, API versioning and deprecation, health-check semantics | `.claude/rules/api.md` |
| Secrets, untrusted input, uploads, SQL parameterization, server authorization, anonymous access, platform auth mechanisms, token validation, enumeration-safe errors, CSRF, token storage, TLS, cryptography, CORS, sensitive and payload logging, fail-safe security behavior | `.claude/rules/security.md` |
| NUnit default, test level, behavior focus, readability, isolation, test-owned data, provider fidelity, coverage, naming | `.claude/rules/testing.md` |
| Dependency necessity, Central Package Management, npm lockfile and categories, npm force flags | `.claude/rules/dependencies.md` |
| Angular structure, components, HTTP boundary, interceptors, error contract, signals/RxJS, state, subscriptions, routing, forms | `.claude/rules/angular.md` |
| Container runtime image, CI truthfulness, frontend CI commands | `.claude/rules/delivery.md` |
| Final diff/scope inspection, build/test, runtime smoke, probe preservation, regression coverage, risk-scoped checks, fix-and-retry, PASS/NOT RUN reporting | `verify` workflow |
| Review priorities, no manufactured findings, review output | `code-review` workflow (`code-reviewer` agent: independent read-only execution) |
| Reproduce/diagnose first, bounded focused iteration, fixing generated output at its source | `build-fix` workflow |
| Propagating custom-setting changes, schema-impact co-changes | `custom-settings` workflow |
| State-aware minimal Git operations, focused staging and commits | `git-workflow` workflow |
| Security evidence and severity discipline, tool independence | `security-scan` workflow |
| Latest stable compatible versions, deprecation/vulnerability/license checks, commercial-license approval | `add-dependency` workflow |
| Decision Request format and decision recording | `architecture-decision` workflow |

## Files

Loading: **always** = loaded every session; **path** = loaded when matching files
are read or edited; **workflow** = invoked per the `CLAUDE.md` routing table;
**on demand** = model-invoked knowledge; **private** = read only by its owning
skill; **user-only** = never invoked automatically.

### Always-loaded policy

| File | Owns | Scope | Loading | Enforcement | Add here |
|---|---|---|---|---|---|
| `CLAUDE.md` | Product sources, core and architecture defaults, decision control, challenge duty, development workflow and routing, Git safety | common | always | Bash guard, Stop hook, git `ask` permissions in settings | New planning-time constraints that apply to all work |
| `docs/technology-stack.md` | Approved stack, conditional technologies, layout defaults | common | always (imported by `CLAUDE.md`) | `check-manifests.mjs` flags non-default packages | Approved/conditional technologies after an accepted decision |

### Path-loaded rules (`.claude/rules/`, flat)

| File | Owns | Scope | Paths | Enforcement | Add here |
|---|---|---|---|---|---|
| `.claude/rules/architecture.md` | Layer boundaries, references, repositories, UoW, EF boundary, DI/config | backend, backend-tests | `backend/**/*.cs`, `backend/**/*.csproj` | `check-manifests.mjs` (outward references) | New backend boundary constraints |
| `.claude/rules/persistence.md` | Seeding, migrations, production migration, local DB config | backend | `backend/**/*.cs`, `backend/**/appsettings*.json` | Stop hook (seeder/migration reminders) | Data lifecycle and migration constraints |
| `.claude/rules/coding-style.md` | C# conventions and hygiene | backend | `backend/**/*.cs` | `.editorconfig`, `Directory.Build.props` (IDE0005 in build) | Non-mechanical C# conventions (mechanical ones go to `.editorconfig`) |
| `.claude/rules/performance.md` | Async, time, HttpClient lifetime, DB efficiency, caching, optimization | backend | `backend/**/*.cs` | — | Performance and caching constraints |
| `.claude/rules/error-handling.md` | Outcomes, exceptions, validation boundaries, cancellation, logging, outbound failures | backend | `backend/**/*.cs` | — | Failure-handling and logging constraints |
| `.claude/rules/api.md` | HTTP semantics, error contracts, Swagger, versioning, health | backend | `backend/**/*.cs` | — | HTTP contract constraints |
| `.claude/rules/security.md` | Security invariants | common | backend, frontend, config, manifest, env, Docker files | `security-scan` workflow | Security constraints |
| `.claude/rules/testing.md` | Backend test policy | backend-tests | `backend/**/*Tests/**/*.cs`, `backend/**/*Tests/*.csproj` | Stop hook (test reminder) | Backend test constraints |
| `.claude/rules/dependencies.md` | Dependency necessity, CPM, npm | common | `**/*.csproj`, `**/Directory.Packages.props`, `**/package.json`, `**/package-lock.json` | Bash guard, post-edit manifest check | Manifest-level constraints |
| `.claude/rules/angular.md` | Frontend policy | frontend | `frontend/**/*` | — | Angular constraints |
| `.claude/rules/delivery.md` | Containers and CI | delivery | Dockerfiles, Compose, CI definitions | — | Delivery constraints |

### Workflow skills (`.claude/skills/`)

| File | Owns | Scope | Loading | Enforcement | Add here |
|---|---|---|---|---|---|
| `.claude/skills/project-structure/SKILL.md` | Scaffolding/restructuring procedure | common | workflow | `check-manifests.mjs` in completion | Scaffolding steps |
| `.claude/skills/project-structure/references/solution-layout.md` | Repository tree and repo-file examples | common | private (project-structure) | — | Layout examples |
| `.claude/skills/project-structure/references/backend-layout.md` | Backend trees, type-role naming, reference examples | backend | private (project-structure) | — | Backend layout examples |
| `.claude/skills/verify/SKILL.md` | Completion verification | common | workflow (mandatory before completion) | Stop hook reminders | Verification steps and report fields |
| `.claude/skills/code-review/SKILL.md` | Review procedure and output | common | workflow; preloaded by agent | — | Review steps and checks-by-reference |
| `.claude/skills/build-fix/SKILL.md` | Repair loop | common | workflow | — | Repair techniques and stop conditions |
| `.claude/skills/custom-settings/SKILL.md` | Settings synchronization | common | workflow | post-edit reminder on `CUSTOM_SETTINGS.md` | Propagation steps |
| `.claude/skills/git-workflow/SKILL.md` | Git procedure | repo/meta | workflow | git `ask` permissions in settings | Git conventions |
| `.claude/skills/security-scan/SKILL.md` | Security review procedure | common | workflow | — | Scan procedure and report shape |
| `.claude/skills/security-scan/references/scan-layers.md` | Layer investigation prompts | common | private (security-scan) | — | Investigation prompts |
| `.claude/skills/add-dependency/SKILL.md` | Dependency addition/update procedure | common | workflow | Bash guard routes dependency commands here | Version/license/vulnerability steps |
| `.claude/skills/architecture-decision/SKILL.md` | Decision Requests and records | common | workflow | — | Decision procedure; records go to `docs/decisions/` |
| `.claude/skills/template-maintenance/SKILL.md` | Instruction-system maintenance | repo/meta | user-only | `check-instructions.mjs` | Maintenance procedure |

### Knowledge skills (`.claude/skills/`)

All are on demand, own technique only, and point to the rules above.

| File | Technique for | Scope | Policy owners it serves |
|---|---|---|---|
| `.claude/skills/ef-core/SKILL.md` | EF Core implementation, seeder implementation | backend | architecture, persistence, performance |
| `.claude/skills/http-api/SKILL.md` | Status-code reference, conditional requests, idempotency | backend | api |
| `.claude/skills/aspnet-error-handling/SKILL.md` | Exception handler, ProblemDetails, outcomes, validators | backend | error-handling, api |
| `.claude/skills/dotnet-testing/SKILL.md` | NUnit, WebApplicationFactory, test databases, probes to tests | backend-tests | testing, verify |
| `.claude/skills/logging/SKILL.md` | ILogger technique | backend | error-handling, security |
| `.claude/skills/logging/references/serilog.md` | Serilog configuration (private to logging) | backend | error-handling |
| `.claude/skills/httpclient-factory/SKILL.md` | Outbound clients | backend | performance, error-handling, architecture |
| `.claude/skills/httpclient-factory/references/resilience.md` | Resilience pipelines (private to httpclient-factory) | backend | error-handling, technology stack |
| `.claude/skills/configuration/SKILL.md` | Options and secrets technique | backend | architecture, security |
| `.claude/skills/dependency-injection/SKILL.md` | Registration and lifetimes | backend | architecture |
| `.claude/skills/caching/SKILL.md` | Cache layers, keys, invalidation | backend | performance, architecture |
| `.claude/skills/swagger/SKILL.md` | Swashbuckle configuration | backend | api, technology stack |
| `.claude/skills/api-versioning/SKILL.md` | Asp.Versioning technique | backend | api |
| `.claude/skills/health-check/SKILL.md` | Health endpoints | backend | api |
| `.claude/skills/docker/SKILL.md` | Container technique | delivery | delivery, security, persistence |
| `.claude/skills/ci-cd/SKILL.md` | Pipeline technique | delivery | delivery, persistence |
| `.claude/skills/angular/SKILL.md` | Angular technique | frontend | angular, security |
| `.claude/skills/modern-csharp/SKILL.md` | Modern C# features | backend | coding-style |
| `.claude/skills/authentication/SKILL.md` | AuthN/AuthZ technique | backend | security, api |

Add new technique to the matching knowledge skill; create a new knowledge skill
only for a distinct technology with its own invocation cues.

### Agent

| File | Owns | Scope | Loading | Enforcement |
|---|---|---|---|---|
| `.claude/agents/code-reviewer.md` | Independent read-only execution of `code-review` | common | agent (delegated) | Write/Edit tools disallowed |

### Enforcement and configuration

| File | Purpose | Trigger | Points to |
|---|---|---|---|
| `.claude/settings.json` | Hook registration; `ask` permission for destructive/remote Git commands | session | `CLAUDE.md` (Git) |
| `.claude/hooks/guard-bash.mjs` | Blocks npm force flags; routes dependency commands to `add-dependency` | PreToolUse (Bash, PowerShell) | `dependencies.md`, `add-dependency` |
| `.claude/hooks/post-edit.mjs` | Product-source sync reminders; manifest check after manifest edits | PostToolUse (Edit, Write, MultiEdit) | `CLAUDE.md`, `custom-settings`, `check-manifests.mjs` |
| `.claude/hooks/stop-check.mjs` | One-time co-change reminders (seeder, migrations, tests); no loop | Stop | `persistence.md`, `verify` |
| `.claude/scripts/check-manifests.mjs` | CPM, pinned stable versions, non-default packages, outward references, npm categories | post-edit hook; `verify`, `add-dependency`, `project-structure` | `dependencies.md`, `architecture.md`, `docs/technology-stack.md` |
| `.claude/scripts/check-instructions.mjs` | Structural checks of this instruction system | manual; `template-maintenance` | this map |
| `.editorconfig` | Formatting and code-style severities | IDE, `dotnet format`, build | `coding-style.md` |
| `Directory.Build.props` | Shared .NET build settings; code style enforced in build | MSBuild | `docs/technology-stack.md` |
| `Directory.Packages.props` | Central package versions | NuGet | `dependencies.md` |

### Product inputs

| File | Role | Governed by |
|---|---|---|
| `SPECIFICATION.md` | Product behavior (empty in the template by design) | `CLAUDE.md` — Product Sources |
| `CUSTOM_SETTINGS.md` | Approved tunable product values | `CLAUDE.md` — Product Sources; `custom-settings` |

Accepted decision records, when they exist, live in `docs/decisions/` (history and
rationale; the active decision is reflected in `CLAUDE.md` or
`docs/technology-stack.md`).
