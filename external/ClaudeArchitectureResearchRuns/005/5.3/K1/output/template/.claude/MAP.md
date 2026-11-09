> Kind: — (human map) | Scope: repo/meta | Capability: — | Loading: not loaded (maintainers; checked by `.claude/scripts/check-instructions.cjs`)

# Instruction System Map

Three coordinates classify every artifact, asked in this order:

1. **Capability** — does it belong to a replaceable capability slot (architecture, persistence, backend-testing, frontend)? Then the selected module owns it and its header says `Capability: <slot>/<implementation>`; otherwise `Capability: —`.
2. **Kind** — OP operating policy · DEC decisions · STD path-scoped standards · KNW knowledge · WF procedures · ENF enforcement · IN product inputs. Kind decides mechanism and location.
3. **Scope** — common · backend · backend-tests · frontend · delivery · repo/meta. Scope decides the rule directory and `paths:`.

Dependency direction: WF → KNW → STD → DEC → OP; ENF → STD/DEC, declared on each ENF artifact's `Conforms:` line (the line after its header); product inputs never override policy. Skill and agent references are routing pointers. Changing this system: `template-maintenance` (user-invoked); capability selection changes: `architecture-decision`.

## View 1 — Kind × Scope

### OP and DEC (always loaded)

| File | Owns | Scope | Capability | Loading | Enforcement | Extend here when |
|---|---|---|---|---|---|---|
| `CLAUDE.md` | Product-source authority and approvals, string semantics, custom-settings boundaries, decision control (Decided/Delegated/Reserved, Reserved list, five-question test, headless behavior), simplicity and scope defaults, challenge obligation, Git safety, normative vocabulary, workflow routing | common | — | always (project memory) | — | a rule must be known at planning time for every task |
| `docs/architecture/decision-register.md` | Capability selection and declared properties, approved platform and stack, conditional technologies, project layout default, accepted decisions | common | — (selection block per slot) | always (imported by `CLAUDE.md`) | structure checker (selection vs. modules) | a project decision is accepted, or a stack/default changes |

### STD (path-scoped standards)

| File | Owns | Scope | Capability | Loading | Enforcement | Extend here when |
|---|---|---|---|---|---|---|
| `.claude/rules/common/security.md` | Secrets, untrusted input, server-side authorization, TLS and certificate validation, sensitive and payload logging, fail-safe checks, visible security-configuration failure | common | — | `**/*` | — | a security rule applies to all code and configuration |
| `.claude/rules/common/structure.md` | Physical structure follows responsibilities (no speculative projects, empty trees, generic buckets) | common | — | `**/*` | — | a repository-wide structure rule is added |
| `.claude/rules/common/dependencies.md` | Dependencies only for a current requirement | common | — | `**/*` | dependency hook | an ecosystem-neutral dependency rule is added |
| `.claude/rules/backend/architecture.md` | Thin controllers, DI style and lifetimes, cache and remote-HTTP boundaries (role level) | backend | — | `backend/**/*` | — | a role-level backend boundary rule is independent of the frame |
| `.claude/rules/backend/architecture-style.md` | Frame role map, inward dependency direction, domain modeling and DDD gating, Application Services, Application abstractions, commit-boundary placement, composition root, layer registration, transport-contract duplication | backend | architecture/clean-architecture | `backend/**/*` | `architecture-style.cjs` | a rule depends on the selected architecture frame |
| `.claude/rules/backend/persistence.md` | Repository contracts, generic repositories, parameterized data access, Development seeding semantics | backend | — | `backend/**/*` | — | a persistence rule holds for any persistence technology |
| `.claude/rules/backend/persistence-technology.md` | EF Core boundary, Unit of Work binding, explicit transactions, seeding mechanism, sqlserver Development connection string | backend | persistence/ef-core | `backend/**/*` | `persistence-technology.cjs` | a rule is specific to the persistence technology or provider |
| `.claude/rules/backend/api.md` | HTTP status semantics, ProblemDetails, centralized exceptions, error leakage, log-once, cancellation, expected outcomes, validation boundaries, exception control flow | backend | — | `backend/**/*` | — | an HTTP, error, or validation rule is added |
| `.claude/rules/backend/api-contracts.md` | API versioning need, breaking changes, version strategy, version-independent inner models, Swagger accuracy and exposure | backend | — | `backend/**/*` | — | a contract-evolution or API-documentation rule is added |
| `.claude/rules/backend/operations.md` | Health checks, structured logging, Serilog integration, typed options, production container image | backend | — | `backend/**/*`, `**/Dockerfile*` | — | an operational (health, logging, configuration, container) rule is added |
| `.claude/rules/backend/security.md` | Anonymous access, platform authentication, Bearer validation, enumeration leaks, cryptography and Data Protection, CORS, upload metadata | backend | — | `backend/**/*` | — | a backend-specific security rule is added |
| `.claude/rules/backend/runtime.md` | Optimization evidence, async and cancellation, TimeProvider, database efficiency, HttpClient lifetime, timeouts, retries, fallback, caching rules | backend | — | `backend/**/*` | — | a runtime-behavior or performance rule is added |
| `.claude/rules/backend/coding-style.md` | Repository conventions, file/namespace/async naming defaults, no unrelated style rewrites | backend | — | `backend/**/*` | `.editorconfig` | a C# style rule must be policy rather than editorconfig |
| `.claude/rules/backend/dependencies.md` | NuGet Central Package Management, narrow package references | backend | — | `backend/**/*`, `Directory.*.props` | manifest hook | a NuGet-specific rule is added |
| `.claude/rules/backend-tests/testing.md` | Test level, behavior focus, integration-test use, provider fidelity, determinism, test-owned data, explicit cases, naming, no coverage chasing | backend-tests | — | `backend/**/*Tests/**/*` | — | a framework-neutral test rule is added |
| `.claude/rules/backend-tests/test-framework.md` | Default test framework | backend-tests | backend-testing/nunit | `backend/**/*Tests/**/*` | `test-framework.cjs` | a rule is specific to the test framework |
| `.claude/rules/backend-tests/test-projects.md` | Test-project production references | backend-tests | architecture/clean-architecture | `backend/**/*Tests/**/*` | `architecture-style.cjs` | a test-placement rule depends on the frame |
| `.claude/rules/frontend/frontend.md` | Feature structure, focused components, lazy loading, simple state, HTTP boundary, API error contract | frontend | — | `frontend/**/*` | — | a frontend rule holds for any SPA framework |
| `.claude/rules/frontend/frontend-framework.md` | Standalone APIs, Signals vs RxJS, functional interceptors, reactive forms, subscription composition and lifecycle | frontend | frontend/angular | `frontend/**/*` | `frontend-framework.cjs` | a rule is specific to the frontend framework |
| `.claude/rules/frontend/security.md` | Cookie authentication and CSRF, token storage | frontend | — | `frontend/**/*` | — | a frontend security rule is added |
| `.claude/rules/frontend/dependencies.md` | npm, lockfile, dependency categories | frontend | — | `frontend/**/*` | manifest hook | an npm rule is added |

### WF (procedures)

| File | Owns | Scope | Capability | Loading | Enforcement | Extend here when |
|---|---|---|---|---|---|---|
| `.claude/skills/development-workflow/SKILL.md` | Implementation sequence: read specification, inspect code, plan, regression tests, performance changes, API deprecation, durable-source sync, review, verify, report | common | — | on-demand workflow | — | an implementation-time obligation is added |
| `.claude/skills/verify/SKILL.md` | Completion verification: diff/scope review, build, tests, runtime smoke, probe preservation, risk-scoped checks, changed-file usings, fix-and-retry, truthful report | common | — | on-demand workflow | runs the checkers | a completion check is added |
| `.claude/skills/code-review/SKILL.md` | Independent read-only review procedure, priorities, check-by-reference architecture review, no manufactured findings, output shape | common | — | on-demand workflow; preloaded by the agent | — | a review step is added |
| `.claude/agents/code-reviewer.md` | Thin read-only reviewer delegating to `code-review` | common | — | subagent | tool restrictions | never; extend `code-review` instead |
| `.claude/skills/build-fix/SKILL.md` | Reproduce-diagnose-fix loop, no weakened verification, generated-output fixes, iteration limits | common | — | on-demand workflow | — | a repair procedure is added |
| `.claude/skills/custom-settings/SKILL.md` | Settings propagation across surfaces, schema-relevant settings, verification | common | — | on-demand workflow | settings-edit hook | a settings-synchronization step is added |
| `.claude/skills/git-workflow/SKILL.md` | Safe execution of requested Git operations, no discarded work, minimal state-aware operations, focused staging | repo/meta | — | on-demand workflow | — | a Git procedure is added |
| `.claude/skills/security-scan/SKILL.md` | Static security review procedure, evidence and contextual severity, tool independence, report shape | common | — | on-demand workflow | — | a scan step is added |
| `.claude/skills/security-scan/references/scan-layers.md` | Layer-by-layer investigation prompts (private to `security-scan`) | common | — | read by `security-scan` | — | a new investigation prompt is added |
| `.claude/skills/add-dependency/SKILL.md` | Version selection, due diligence, license approval, conditional packages, peer conflicts, removal | common | — | on-demand workflow | dependency-command hook, manifest hook | a dependency procedure step is added |
| `.claude/skills/architecture-decision/SKILL.md` | Decision Request shape, recording accepted decisions, capability selection and provider-variant changes | common | — | on-demand workflow | — | the decision procedure changes |
| `.claude/skills/template-maintenance/SKILL.md` | Changing this instruction system (classification, ownership, leak rule, checks) | repo/meta | — | user-invoked only | structure checker | the maintenance procedure changes |
| `.claude/skills/project-structure/SKILL.md` | Scaffolding and restructuring procedure | common | — | on-demand workflow | `check-manifests.cjs` | a scaffolding step is added |
| `.claude/skills/project-structure/references/solution-layout.md` | Repository layout, shared build files, docs, ignore list (private) | common | — | read by `project-structure` | — | repository-level layout guidance changes |
| `.claude/skills/project-structure/references/backend-layout.md` | Backend project folders and references (private) | backend | architecture/clean-architecture | read by `project-structure` | `architecture-style.cjs` | frame scaffolding changes |
| `.claude/skills/project-structure/references/test-setup.md` | Test project creation (private) | backend-tests | backend-testing/nunit | read by `project-structure` | — | test scaffolding changes |
| `.claude/skills/project-structure/references/frontend-setup.md` | Frontend workspace creation (private) | frontend | frontend/angular | read by `project-structure` | — | frontend scaffolding changes |
| `.claude/skills/delivery-change/SKILL.md` | CI reproducing supported commands, visible failures, frontend CI scripts and lockfile installs, deliberate production migrations, pipeline verification | delivery | — | on-demand workflow | — | a CI/CD or deployment obligation is added |
| `.claude/skills/persistence-change/SKILL.md` | Persistence setup, migration creation and review, seed co-change, local database update | backend | persistence/ef-core | on-demand workflow | Stop hook reminders | a persistence-change step is added |

### KNW (technique, on demand)

| File | Owns | Scope | Capability | Loading | Enforcement | Extend here when |
|---|---|---|---|---|---|---|
| `.claude/skills/ef-core/SKILL.md` | EF Core technique, seeding code, migrations commands, raw SQL, SQL Server provider, EF Core testing | backend | persistence/ef-core | on-demand | via standards and checks of its slot facet | EF Core technique or examples change |
| `.claude/skills/dotnet-testing/SKILL.md` | NUnit test technique, integration tests, time, stubs, data, naming, probe conversion | backend-tests | backend-testing/nunit | on-demand | via standards and checks of its slot facet | test technique changes |
| `.claude/skills/angular/SKILL.md` | Angular technique, security notes, testing, build-fix patterns | frontend | frontend/angular | on-demand | via standards and checks of its slot facet | Angular technique changes |
| `.claude/skills/http-api/SKILL.md` | Status-code catalogue, idempotency, conditional requests | backend | — | on-demand | — | HTTP semantics guidance changes |
| `.claude/skills/aspnet-error-handling/SKILL.md` | Exception handler, outcome mapping, validation placement, Result pattern | backend | — | on-demand | — | error-handling technique changes |
| `.claude/skills/logging/SKILL.md` | ILogger technique, levels, scopes, correlation | backend | — | on-demand | — | logging technique changes |
| `.claude/skills/logging/references/serilog.md` | Serilog setup (private to `logging`) | backend | — | read by `logging` | — | Serilog configuration guidance changes |
| `.claude/skills/httpclient-factory/SKILL.md` | Outbound HTTP technique | backend | — | on-demand | — | outbound HTTP technique changes |
| `.claude/skills/httpclient-factory/references/resilience.md` | Resilience pipelines (private to `httpclient-factory`) | backend | — | read by `httpclient-factory` | — | resilience guidance changes |
| `.claude/skills/configuration/SKILL.md` | Options pattern, providers, secrets setup | backend | — | on-demand | — | configuration technique changes |
| `.claude/skills/dependency-injection/SKILL.md` | Registration, lifetimes, keyed services, decorators, scanning | backend | — | on-demand | — | DI technique changes |
| `.claude/skills/caching/SKILL.md` | Cache layers, HybridCache, keys, expiration, invalidation | backend | — | on-demand | — | caching technique changes |
| `.claude/skills/swagger/SKILL.md` | Swashbuckle setup and metadata | backend | — | on-demand | — | API documentation technique changes |
| `.claude/skills/api-versioning/SKILL.md` | Versioning setup, compatibility, deprecation mechanics | backend | — | on-demand | — | versioning technique changes |
| `.claude/skills/health-check/SKILL.md` | Health endpoints and probes | backend | — | on-demand | — | health-check technique changes |
| `.claude/skills/docker/SKILL.md` | Dockerfiles, Compose, images | delivery | — | on-demand | — | container technique changes |
| `.claude/skills/ci-cd/SKILL.md` | Pipeline shapes and commands | delivery | — | on-demand | — | pipeline technique changes |
| `.claude/skills/modern-csharp/SKILL.md` | Modern C# features and style conventions | backend | — | on-demand | — | language-feature guidance changes |
| `.claude/skills/authentication/SKILL.md` | Authentication and authorization technique | backend | — | on-demand | — | auth technique changes |

### ENF (deterministic enforcement and delivery)

| File | Owns | Scope | Capability | Loading | Enforcement | Extend here when |
|---|---|---|---|---|---|---|
| `.claude/settings.json` | Hook registration in exec form (`node`, launcher `${CLAUDE_PROJECT_DIR}/.claude/hooks/dispatch.cjs`, event): dependency/reference guard (PreToolUse, fails closed), actual-state checks after edits and shell commands (PostToolUse, PostToolUseFailure), co-change reminders (Stop) | repo/meta | — | Claude Code settings | registers the hooks; validated by the structure checker | a new hook intention is added |
| `.claude/hooks/dispatch.cjs` | Hook entry point: launcher root locates code only, the active root comes from the hook input `cwd` (worktree-aware); BOM/UTF-16-safe input; routes events; messages point to owners | repo/meta | — | hook | PreToolUse, PostToolUse, PostToolUseFailure, Stop | hook routing changes |
| `.claude/scripts/classify-command.cjs` | Pre-execution, token-aware classification of dependency and project-reference commands (Bash and PowerShell text, shell wrappers, chains) | common | — | required by the dispatcher | PreToolUse (blocks before execution) | a dependency or reference command form is added |
| `.claude/scripts/actual-state.cjs` | Post-execution inspection of actual files per worktree (snapshot in the worktree's Git directory): manifests, Reserved project-reference changes, instruction structure, product inputs | repo/meta | — | required by the dispatcher | PostToolUse, PostToolUseFailure | a relevant file class is added |
| `.claude/scripts/lib.cjs` | Shared helpers | repo/meta | — | required by scripts | — | a helper is shared |
| `.claude/scripts/check-instructions.cjs` | Instruction-structure checker (headers, kinds, scopes, paths, imports, skills, agent, references, dependency direction incl. ENF conformance, slots, binding obligations, manifests, contracts and facet roles, leak rule, map, hook configuration, budget) | repo/meta | — | command, instruction-change hooks | instruction-change hooks (errors fed back), CLI exit code | a structural predicate is added |
| `.claude/scripts/check-manifests.cjs` | Central package management, version pinning, deprecated packages, npm categories; runs slot facet checks | common | — | command, manifest hook | manifest-edit hook (findings fed back), CLI exit code | a manifest check is added |
| `.claude/scripts/check-cochange.cjs` | Working-tree co-change reminders (tests; slot facet reminders) | common | — | command, Stop hook | Stop hook (once per content state of the triggering files), CLI report | a co-change reminder is added |
| `.claude/scripts/facets/architecture-style.cjs` | Frame role classification, project-reference direction, test references, inner-layer ASP.NET Core check | backend | architecture/clean-architecture | facet of `check-manifests.cjs` | manifest/Stop hooks via check-manifests or check-cochange | frame enforcement changes |
| `.claude/scripts/facets/persistence-technology.cjs` | EF Core packages outside Infrastructure; seed/migration co-change reminders | backend | persistence/ef-core | facet of manifest and co-change checks | manifest/Stop hooks via check-manifests or check-cochange | persistence enforcement changes |
| `.claude/scripts/facets/test-framework.cjs` | Additional test framework detection | backend-tests | backend-testing/nunit | facet of `check-manifests.cjs` | manifest/Stop hooks via check-manifests or check-cochange | test-framework enforcement changes |
| `.claude/scripts/facets/frontend-framework.cjs` | Non-default frontend libraries and misplaced build tooling | frontend | frontend/angular | facet of `check-manifests.cjs` | manifest/Stop hooks via check-manifests or check-cochange | frontend enforcement changes |
| `.editorconfig` | Formatting and C# code-style configuration | common | — | editors, `dotnet format` | IDE and dotnet format | a mechanical style preference changes |
| `Directory.Build.props` | Shared .NET build settings | backend | — | MSBuild | MSBuild | a genuinely shared build setting changes |
| `Directory.Packages.props` | Central package versions | backend | — | MSBuild | NuGet restore (CPM) | packages are added through `add-dependency` |

### IN (product inputs, not instruction layers)

| File | Owns | Scope | Capability | Loading | Enforcement | Extend here when |
|---|---|---|---|---|---|---|
| `SPECIFICATION.md` | Project-specific functional requirements and observable behavior (empty in the template) | common | — | read by workflows | edit hook: synchronization reminder | product behavior is approved |
| `CUSTOM_SETTINGS.md` | Approved tunable limits and defaults | common | — | read by workflows | edit hook: routes to `custom-settings` | a tunable value is approved |

### Maintenance metadata (not loaded)

| File | Owns | Scope | Capability | Loading | Enforcement | Extend here when |
|---|---|---|---|---|---|---|
| `.claude/MAP.md` | This map | repo/meta | — | not loaded | structure checker | any artifact is added, moved, or removed |
| `.claude/capabilities/architecture/CONTRACT.md` | Architecture slot contract | repo/meta | architecture | not loaded | structure checker | the slot contract changes (rare; Reserved) |
| `.claude/capabilities/architecture/clean-architecture/MODULE.md` | Architecture module manifest | repo/meta | architecture/clean-architecture | not loaded | structure checker | a facet of the module is added, moved, or removed |
| `.claude/capabilities/persistence/CONTRACT.md` | Persistence slot contract | repo/meta | persistence | not loaded | structure checker | the slot contract changes (rare; Reserved) |
| `.claude/capabilities/persistence/ef-core/MODULE.md` | Persistence module manifest | repo/meta | persistence/ef-core | not loaded | structure checker | a facet of the module is added, moved, or removed |
| `.claude/capabilities/backend-testing/CONTRACT.md` | Backend-testing slot contract | repo/meta | backend-testing | not loaded | structure checker | the slot contract changes (rare; Reserved) |
| `.claude/capabilities/backend-testing/nunit/MODULE.md` | Backend-testing module manifest | repo/meta | backend-testing/nunit | not loaded | structure checker | a facet of the module is added, moved, or removed |
| `.claude/capabilities/frontend/CONTRACT.md` | Frontend slot contract | repo/meta | frontend | not loaded | structure checker | the slot contract changes (rare; Reserved) |
| `.claude/capabilities/frontend/angular/MODULE.md` | Frontend module manifest | repo/meta | frontend/angular | not loaded | structure checker | a facet of the module is added, moved, or removed |

`docs/decisions/` holds optional detailed decision records created by `architecture-decision`.

## View 2 — Capabilities

Static composition: one implementation per required slot, zero or one for the optional slot; the selection lives in the decision register.

### architecture

- Selected: clean-architecture (required frame). Binds: —. Declared: roles Domain, Application, Infrastructure, Api; not-adopted mediator-based styles.

| Kind | Facet | Scope | Loading |
|---|---|---|---|
| DEC | `docs/architecture/decision-register.md` (selection block) | common | always |
| STD | `.claude/rules/backend/architecture-style.md` | backend | path |
| STD | `.claude/rules/backend-tests/test-projects.md` | backend-tests | path |
| WF | `.claude/skills/project-structure/references/backend-layout.md` | backend | read by `project-structure` |
| ENF | `.claude/scripts/facets/architecture-style.cjs` | backend | manifest hook, `verify` |

### persistence

- Selected: ef-core, provider variant sqlserver (required leaf). Binds: architecture (Infrastructure role, `IUnitOfWork` implementation). Declared: EF Core migrations, dedicated Development seeder, collation-driven string comparison.

| Kind | Facet | Scope | Loading |
|---|---|---|---|
| DEC | `docs/architecture/decision-register.md` (selection block) | common | always |
| STD | `.claude/rules/backend/persistence-technology.md` | backend | path |
| KNW | `.claude/skills/ef-core/SKILL.md` | backend | on-demand |
| WF | `.claude/skills/persistence-change/SKILL.md` | backend | on-demand |
| ENF | `.claude/scripts/facets/persistence-technology.cjs` | backend | manifest and Stop hooks, `verify` |

### backend-testing

- Selected: nunit (required leaf). Binds: architecture (test placement). Declared: `WebApplicationFactory<Program>` integration host; Testcontainers conditional.

| Kind | Facet | Scope | Loading |
|---|---|---|---|
| DEC | `docs/architecture/decision-register.md` (selection block) | common | always |
| STD | `.claude/rules/backend-tests/test-framework.md` | backend-tests | path |
| KNW | `.claude/skills/dotnet-testing/SKILL.md` | backend-tests | on-demand |
| WF | `.claude/skills/project-structure/references/test-setup.md` | backend-tests | read by `project-structure` |
| ENF | `.claude/scripts/facets/test-framework.cjs` | backend-tests | manifest hook, `verify` |

### frontend

- Selected: angular (optional leaf). Binds: —. Declared: Angular stack and libraries not added by default.

| Kind | Facet | Scope | Loading |
|---|---|---|---|
| DEC | `docs/architecture/decision-register.md` (selection block) | common | always |
| STD | `.claude/rules/frontend/frontend-framework.md` | frontend | path |
| KNW | `.claude/skills/angular/SKILL.md` | frontend | on-demand |
| WF | `.claude/skills/project-structure/references/frontend-setup.md` | frontend | read by `project-structure` |
| ENF | `.claude/scripts/facets/frontend-framework.cjs` | frontend | manifest hook, `verify` |

## Where does a topic live?

| Topic | Owner |
|---|---|
| Product authority, approvals, string semantics, tunable values | `CLAUDE.md` |
| Reserved decisions, Decision Requests | `CLAUDE.md` (policy), `.claude/skills/architecture-decision/SKILL.md` (procedure) |
| Selected technologies and defaults | `docs/architecture/decision-register.md` |
| Layer rules and dependency direction | `.claude/rules/backend/architecture-style.md` |
| Repositories, seeding semantics, SQL parameterization | `.claude/rules/backend/persistence.md` |
| Persistence technology boundary and seeding mechanism | `.claude/rules/backend/persistence-technology.md` |
| HTTP, errors, validation | `.claude/rules/backend/api.md` |
| Versioning and Swagger | `.claude/rules/backend/api-contracts.md` |
| Health, logging, configuration, containers | `.claude/rules/backend/operations.md` |
| Async, outbound calls, caching, optimization | `.claude/rules/backend/runtime.md` |
| Secrets, trust boundaries, sensitive logging | `.claude/rules/common/security.md` |
| Backend authentication, CORS, cryptography | `.claude/rules/backend/security.md` |
| Test rules | `.claude/rules/backend-tests/` |
| Frontend rules | `.claude/rules/frontend/` |
| Dependency rules / procedure | `.claude/rules/*/dependencies.md` / `.claude/skills/add-dependency/SKILL.md` |
| Implementation, review, verification, repair | `development-workflow`, `code-review`, `verify`, `build-fix` |
| CI/CD and production migrations | `.claude/skills/delivery-change/SKILL.md` |
| Git | `CLAUDE.md` (policy), `.claude/skills/git-workflow/SKILL.md` (procedure) |
