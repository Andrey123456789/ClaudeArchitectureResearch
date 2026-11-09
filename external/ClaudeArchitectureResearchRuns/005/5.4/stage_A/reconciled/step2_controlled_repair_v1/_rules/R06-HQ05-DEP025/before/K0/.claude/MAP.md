> Instruction map | Scope: repo/meta | Owner: maintainers' index of the instruction system | Loading: not loaded — read by humans and by /template-maintenance

# Instruction System Map

The instruction system is organized by two questions:

1. **What is it?** — the Kind decides the mechanism, location and loading.
2. **Where does it apply?** — the Scope decides the directory and path globs.

## Kinds

| Kind | Responsibility | Mechanism and location | Loading | Extend here |
|---|---|---|---|---|
| OP — Operating Policy | precedence, product governance, decision protocol, challenge obligation, Git safety, workflow routing | `CLAUDE.md` | always | only agent-behavior policy needed at planning time |
| DEC — Project Decisions | architecture, patterns not adopted, stack, conditional technologies, project defaults | `docs/architecture/decision-register.md` (one register, `D-xx` IDs); optional ADRs in `docs/decisions/` | always (imported by `CLAUDE.md`) | new or changed decision via `architecture-decision` |
| STD — Standards | normative must/default/prefer rules for one scope | `.claude/rules/<scope>/<topic>.md` with `paths:` | path-scoped | the rule file of the matching scope and topic |
| KNW — Knowledge | technique, examples, trade-offs | `.claude/skills/<name>/SKILL.md` (+ private `references/`) | on demand | the skill for that technology |
| WF — Workflows | procedures, steps, stop conditions, outputs | `.claude/skills/<name>/SKILL.md`, `.claude/agents/` | workflow invocation | the workflow that owns the procedure |
| ENF — Enforcement | hooks, permissions, scripts, build/format assets | `.claude/settings.json`, `.claude/hooks/`, `.claude/scripts/`, root `.editorconfig` and `Directory.*.props` | event or check | the script or setting that checks the owning rule |
| IN — Product inputs | product behavior and approved tunable values | `SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, feature/task inputs | read as input | product content only — never engineering policy |

Conformance dependencies point WF → KNW → STD → DEC → OP, and ENF → STD/DEC; enforcement declares its conformance in its header and in `Conforms to:` comment lines. Routing pointers may point anywhere reliably invocable: references after `See also:`, `Workflow:`, `Technique:`, `Procedure:` or `Enforced by:`, workflow invocations (run, use, invoke, switch to, `→`, slash commands, agent delegation), the `CLAUDE.md` routing table, and the register's **Details in** / **Affects** cells. Every other reference is a conformance dependency, checked for direction and acyclicity by `check-instructions.cjs`; references to product inputs and enforcement files name inputs and tools, not owners. A skill's `references/` files are read only by that skill. Standards cite decision IDs instead of restating decisions; decision summaries exist only in the register.

## Scopes and path territories

| Scope | Covers | Standard globs start with |
|---|---|---|
| `common` | everything | any glob |
| `backend` | `backend/<Name>.<Layer>/...` and root .NET build files | `backend/`, `Directory.Build.props`, `Directory.Packages.props`, `global.json`, `*.slnx` |
| `backend-tests` | backend test projects (`backend/<Name>.<Layer>.Tests/`, `backend/<Name>.IntegrationTests/`) | `backend/` and containing `Tests` |
| `frontend` | `frontend/<Name>.Web/...` | `frontend/` |
| `delivery` | Dockerfiles, Compose, CI/CD definitions | Docker, Compose or CI paths |
| `repo/meta` | repository and instruction-system operations | (no standards; workflows and enforcement only) |

No `delivery` or `repo/meta` standard exists yet: no path-triggered rule of those scopes is needed. Create `.claude/rules/delivery/<topic>.md` when one is.

## Kind × Scope view

| Kind | common | backend | backend-tests | frontend | delivery | repo/meta |
|---|---|---|---|---|---|---|
| OP | `CLAUDE.md` | | | | | |
| DEC | `docs/architecture/decision-register.md` | | | | | |
| STD | `rules/common/security.md`, `rules/common/dependencies.md`, `rules/common/repository-layout.md` | `rules/backend/architecture.md`, `persistence.md`, `api.md`, `error-handling.md`, `csharp.md`, `integrations.md`, `caching.md`, `hosting.md`, `security.md` | `rules/backend-tests/testing.md` | `rules/frontend/angular.md` | | |
| KNW | | `ef-core`, `http-api`, `aspnet-error-handling`, `logging`, `httpclient-factory`, `configuration`, `dependency-injection`, `caching`, `swagger`, `api-versioning`, `health-check`, `modern-csharp`, `authentication` | `dotnet-testing` | `angular` | `docker`, `ci-cd` | |
| WF | `development-workflow`, `verify`, `code-review` + agent `code-reviewer`, `build-fix`, `project-structure`, `custom-settings`, `add-dependency`, `architecture-decision`, `security-scan` | | | | `delivery-pipeline` | `git-workflow`, `template-maintenance` |
| ENF | `.editorconfig`, `scripts/check-dependencies.cjs` | `Directory.Build.props`, `Directory.Packages.props` | | | | `settings.json`, `hooks/hook.cjs`, `scripts/repo.cjs`, `scripts/check-instructions.cjs` |
| IN | `SPECIFICATION.md`, `CUSTOM_SETTINGS.md` | | | | | |

## Artifacts

Loading: **always** = project memory; **path** = loads when Claude reads a file matching `paths`; **on demand** = model-invoked knowledge; **workflow** = model- or user-invoked procedure; **user** = user-invoked only.

| File | Kind | Scope | Owner / responsibility | Loading | Enforcement | Extend here |
|---|---|---|---|---|---|---|
| `CLAUDE.md` | OP | common | precedence, product sources, engineering defaults, challenge, decisions, Git, routing | always | pre-command hook (Git confirmation, dependency and project-reference gates); hooks route to workflows | new agent-behavior policy |
| `docs/architecture/decision-register.md` | DEC | common | all project/architecture decisions with Details in / Affects | always (import) | `check-instructions.cjs` (IDs, Affects, no restatement) | `architecture-decision` |
| `SPECIFICATION.md` | IN | common | product behavior (empty in the template) | input | post-change reminder | product requirements |
| `CUSTOM_SETTINGS.md` | IN | common | approved tunable values | input | post-change and stop reminders | approved settings rows |
| `.claude/rules/common/security.md` | STD | common | secrets, input trust, server-side authorization, TLS, sensitive logging, fail-safe controls | path | — | cross-cutting security rules |
| `.claude/rules/common/dependencies.md` | STD | common | dependency need, NuGet CPM, npm manifests | path (manifests) | `check-dependencies.cjs`; pre-command hook | manifest rules |
| `.claude/rules/common/repository-layout.md` | STD | common | physical structure discipline | path | `check-dependencies.cjs` (project naming notice) | structure rules |
| `.claude/rules/backend/architecture.md` | STD | backend | layers, Domain, Application, Controllers, repositories, Unit of Work, EF boundary, DI | path | `check-dependencies.cjs` (project references) | backend boundary rules |
| `.claude/rules/backend/persistence.md` | STD | backend | database access, Development connection string, development seeding | path | stop hook (seeder reminder) | persistence behavior rules |
| `.claude/rules/backend/api.md` | STD | backend | HTTP semantics, error contract, versioning, Swagger accuracy and exposure | path | — | HTTP contract rules |
| `.claude/rules/backend/error-handling.md` | STD | backend | exceptions, expected outcomes, validation boundaries, error exposure, cancellation | path | — | failure-handling rules |
| `.claude/rules/backend/csharp.md` | STD | backend | C# conventions, async, cancellation, time, optimization discipline | path | `.editorconfig` | C# code rules |
| `.claude/rules/backend/integrations.md` | STD | backend | outbound HTTP, time limits, retries, fallback, cancellation | path | `check-dependencies.cjs` (deprecated Polly packages) | outbound dependency rules |
| `.claude/rules/backend/caching.md` | STD | backend | caching need, boundaries, keys, lifetime, invalidation | path | — | caching rules |
| `.claude/rules/backend/hosting.md` | STD | backend | options, logging, health checks, container images | path | — | hosting/operations rules |
| `.claude/rules/backend/security.md` | STD | backend | SQL safety, authentication/authorization configuration, crypto, CORS, uploads | path | — | backend security rules |
| `.claude/rules/backend-tests/testing.md` | STD | backend-tests | framework, level, behavior, isolation, data, fidelity, naming, coverage, test references | path | `check-dependencies.cjs` (test reference notices); stop hook | backend test rules |
| `.claude/rules/frontend/angular.md` | STD | frontend | structure, components, HTTP boundary, state, routing, errors, forms, RxJS, CSRF, token storage | path | `check-dependencies.cjs` (D-10 notices) | Angular rules |
| `.claude/skills/development-workflow/SKILL.md` | WF | common | development procedure and change-specific co-change obligations | workflow | stop hook reminders | development steps |
| `.claude/skills/verify/SKILL.md` | WF | common | completion verification and reporting | workflow | `check-dependencies.cjs`, `dotnet format` | verification steps |
| `.claude/skills/code-review/SKILL.md` | WF | common | review procedure, priorities, finding format | workflow | — | review steps |
| `.claude/agents/code-reviewer.md` | WF | common | independent read-only review role (delegates to `code-review`) | agent | write tools disallowed | agent settings only |
| `.claude/skills/build-fix/SKILL.md` | WF | common | build/test repair loop | workflow | — | repair steps |
| `.claude/skills/project-structure/SKILL.md` | WF | common | scaffolding, restructuring, project-reference changes | workflow | pre-command hook (reference gate); `check-dependencies.cjs` | scaffolding steps |
| `.claude/skills/project-structure/references/solution-layout.md` | WF | common | repository layout reference (private) | read by project-structure | — | layout examples |
| `.claude/skills/project-structure/references/backend-layout.md` | WF | backend | backend project layout and references (private) | read by project-structure | — | backend layout examples |
| `.claude/skills/project-structure/references/baseline-setup.md` | WF | common | baseline packages and Development configuration (private) | read by project-structure | — | scaffold defaults |
| `.claude/skills/custom-settings/SKILL.md` | WF | common | settings synchronization | workflow | post-change and stop reminders | synchronization steps |
| `.claude/skills/add-dependency/SKILL.md` | WF | common | dependency selection, due diligence, licensing, installation | workflow | pre-command hook; `check-dependencies.cjs` | package choices |
| `.claude/skills/architecture-decision/SKILL.md` | WF | common | Decision Requests, recording, propagation | workflow | `check-instructions.cjs` (Affects) | decision procedure |
| `.claude/skills/security-scan/SKILL.md` | WF | common | security scan procedure and report | workflow | — | scan procedure |
| `.claude/skills/security-scan/references/scan-layers.md` | WF | common | per-layer investigation prompts (private) | read by security-scan | — | scan prompts |
| `.claude/skills/delivery-pipeline/SKILL.md` | WF | delivery | CI/CD, container and deployment changes | workflow | — | pipeline steps |
| `.claude/skills/git-workflow/SKILL.md` | WF | repo/meta | Git operation procedure | workflow | pre-command hook (confirmation of repository-changing Git commands) | Git steps |
| `.claude/skills/template-maintenance/SKILL.md` | WF | repo/meta | instruction-system maintenance | user | `check-instructions.cjs` | maintenance steps |
| `.claude/skills/ef-core/SKILL.md` | KNW | backend | EF Core technique | on demand | — | EF Core examples |
| `.claude/skills/http-api/SKILL.md` | KNW | backend | HTTP status reference | on demand | — | HTTP examples |
| `.claude/skills/aspnet-error-handling/SKILL.md` | KNW | backend | error-handling technique | on demand | — | error-handling examples |
| `.claude/skills/dotnet-testing/SKILL.md` | KNW | backend-tests | backend testing technique | on demand | — | test examples |
| `.claude/skills/logging/SKILL.md` | KNW | backend | logging technique | on demand | — | logging examples |
| `.claude/skills/logging/references/serilog.md` | KNW | backend | Serilog configuration depth (private) | read by logging | — | Serilog examples |
| `.claude/skills/httpclient-factory/SKILL.md` | KNW | backend | outbound HTTP technique | on demand | — | HttpClient examples |
| `.claude/skills/httpclient-factory/references/resilience.md` | KNW | backend | resilience depth (private) | read by httpclient-factory | — | resilience examples |
| `.claude/skills/configuration/SKILL.md` | KNW | backend | options and secrets technique | on demand | — | configuration examples |
| `.claude/skills/dependency-injection/SKILL.md` | KNW | backend | DI technique | on demand | — | DI examples |
| `.claude/skills/caching/SKILL.md` | KNW | backend | caching technique | on demand | — | caching examples |
| `.claude/skills/swagger/SKILL.md` | KNW | backend | Swagger technique | on demand | — | Swagger examples |
| `.claude/skills/api-versioning/SKILL.md` | KNW | backend | versioning technique | on demand | — | versioning examples |
| `.claude/skills/health-check/SKILL.md` | KNW | backend | health-check technique | on demand | — | probe examples |
| `.claude/skills/docker/SKILL.md` | KNW | delivery | container technique | on demand | — | Docker examples |
| `.claude/skills/ci-cd/SKILL.md` | KNW | delivery | pipeline technique | on demand | — | CI examples |
| `.claude/skills/angular/SKILL.md` | KNW | frontend | Angular technique | on demand | — | Angular examples |
| `.claude/skills/modern-csharp/SKILL.md` | KNW | backend | modern C# features | on demand | — | language examples |
| `.claude/skills/authentication/SKILL.md` | KNW | backend | authentication/authorization technique | on demand | — | auth examples |
| `.claude/settings.json` | ENF | repo/meta | exec-form hook wiring (fail-closed pre-command hook) | session | `check-instructions.cjs` (hook properties) | new hook events |
| `.claude/hooks/hook.cjs` | ENF | repo/meta | hook dispatcher: pre-command gates, actual-state checks after edits and shell commands, stop reminders | hook events | — | new hook checks |
| `.claude/scripts/repo.cjs` | ENF | repo/meta | shared helpers: active repository/worktree root, Git calls, text decoding, hashes | required by the hook and checkers | — | shared helper code |
| `.claude/scripts/check-dependencies.cjs` | ENF | common | CPM, versions, deny-lists, npm categories, project references | verify, hooks | — | manifest checks |
| `.claude/scripts/check-instructions.cjs` | ENF | repo/meta | structural predicates of this instruction system | maintenance, hooks | — | structural checks |
| `.editorconfig` | ENF | common | formatting and code-style configuration | IDE, `dotnet format` | — | formatting rules |
| `Directory.Build.props` | ENF | backend | shared .NET build settings | MSBuild | — | shared build settings |
| `Directory.Packages.props` | ENF | backend | Central Package Management versions | MSBuild | `check-dependencies.cjs` | package versions (via `add-dependency`) |

## Where does a rule live?

| Topic | Owner |
|---|---|
| Which source wins; vocabulary | `CLAUDE.md` § Precedence |
| Specification authority, invented behavior, ambiguity approval, string semantics, custom-settings ownership, conflicts, new tunable values, what must not go into `CUSTOM_SETTINGS.md` | `CLAUDE.md` § Product sources |
| Simplicity, speculative frameworks, scope and behavior preservation, challenge obligation | `CLAUDE.md` § Engineering defaults |
| Decided/Delegated/Reserved, Reserved list, unclear-case test, Decision Request, headless runs, approved technologies | `CLAUDE.md` § Decisions |
| Repository-changing Git operations and their authority, task-start check, parallel work isolation | `CLAUDE.md` § Git |
| Project-reference changes (procedure and approval marker) | `.claude/skills/project-structure/SKILL.md` |
| Architecture style, patterns not adopted, stack, conditional technologies, solution format, build files, layout | `docs/architecture/decision-register.md` |
| Secrets, secret mechanisms, untrusted input, server-side authorization, TLS, certificate validation, sensitive and payload logging, fail-safe checks, insecure fallback | `.claude/rules/common/security.md` |
| Dependency need, Central Package Management, narrow package references, npm lockfile and categories | `.claude/rules/common/dependencies.md` |
| Speculative projects, empty trees, generic buckets | `.claude/rules/common/repository-layout.md` |
| Layer dependencies, Domain, Application, Controllers, composition root, DTO duplication, repositories, generic repository, Unit of Work, transactions, EF Core boundary, DI lifetimes and registration | `.claude/rules/backend/architecture.md` |
| Efficient queries and pagination, Development connection string, development seeding | `.claude/rules/backend/persistence.md` |
| Status codes, ProblemDetails, empty collections, 401/403/404, 409/412, API versioning, Swagger accuracy and exposure | `.claude/rules/backend/api.md` |
| Centralized exception handling, error exposure, logging exceptions once, expected outcomes and Result, business exceptions, validation boundaries, client cancellation | `.claude/rules/backend/error-handling.md` |
| C# conventions, style-only rewrites, file/namespace/Async naming, constructors, records, visibility, `var`, async I/O, cancellation tokens, `TimeProvider`, optimization evidence | `.claude/rules/backend/csharp.md` |
| HttpClient lifetime, remote transport leaks, time limits, retries, Retry-After, fallback, caller cancellation | `.claude/rules/backend/integrations.md` |
| Caching need, cache boundaries, keys, expiration, invalidation | `.claude/rules/backend/caching.md` |
| Typed options, structured logging, Serilog integration, health checks, liveness/readiness, health output, container runtime images | `.claude/rules/backend/hosting.md` |
| SQL parameterization, authorization configuration, anonymous access, authentication mechanisms, token validation, account enumeration, cryptography, Data Protection, CORS, upload metadata | `.claude/rules/backend/security.md` |
| Test framework, test level, integration tests, behavior focus, explicit cases, naming, coverage, isolation, test data, provider fidelity, test-project references | `.claude/rules/backend-tests/testing.md` |
| Angular structure, components, HTTP boundary, interceptors, Signals/RxJS, state, subscriptions, lazy loading, API errors, forms, CSRF, token storage | `.claude/rules/frontend/angular.md` |
| Reading the specification, inspecting code, regression tests, seeder co-change, migration review, performance changes, API deprecation, review before verify, verify before completion | `.claude/skills/development-workflow/SKILL.md` |
| Diff inspection, builds, tests, runtime smoke, preserving behavioral probes, risk-scoped checks, unused usings, fix-and-retry, verification report | `.claude/skills/verify/SKILL.md` |
| Review priorities, specification conformance, finding format, no manufactured findings | `.claude/skills/code-review/SKILL.md` |
| Independent read-only reviewer | `.claude/agents/code-reviewer.md` |
| Reproduce first, bounded iteration, no weakened verification, generated output fixed at source | `.claude/skills/build-fix/SKILL.md` |
| Custom-settings propagation, schema-affecting settings | `.claude/skills/custom-settings/SKILL.md` |
| Version selection, deprecation/vulnerability/license checks, commercial licenses, resilience and versioning packages, npm force flags, dependency removal | `.claude/skills/add-dependency/SKILL.md` |
| Decision Requests, recording approved behavior in `SPECIFICATION.md`, register entries, ADRs, Affects propagation | `.claude/skills/architecture-decision/SKILL.md` |
| Protecting user work, minimal state-aware Git operations, focused staging and commits | `.claude/skills/git-workflow/SKILL.md` |
| Security evidence and severity, scanner independence | `.claude/skills/security-scan/SKILL.md` |
| CI truthfulness, frontend CI scripts and `npm ci`, production migrations | `.claude/skills/delivery-pipeline/SKILL.md` |
| Scaffolding and restructuring steps | `.claude/skills/project-structure/SKILL.md` |
| Instruction-system changes | `.claude/skills/template-maintenance/SKILL.md` |

## Decision → Affects

Generated from the register; `check-instructions.cjs` verifies that this view matches it.

- D-01 (Clean Architecture) → rules/backend-tests/testing.md, rules/backend/api.md, rules/backend/architecture.md, skills/build-fix, skills/code-review, skills/dependency-injection, skills/project-structure, scripts/check-dependencies.cjs
- D-02 (mediator patterns not adopted) → rules/backend/architecture.md, skills/code-review, skills/project-structure, scripts/check-dependencies.cjs
- D-03 (backend platform) → rules/backend/csharp.md, skills/ci-cd, skills/docker, skills/modern-csharp, skills/project-structure, Directory.Build.props
- D-04 (persistence) → rules/backend/architecture.md, rules/backend/persistence.md, skills/ef-core, skills/project-structure
- D-05 (validation) → rules/backend/error-handling.md, skills/add-dependency, skills/aspnet-error-handling, skills/project-structure, scripts/check-dependencies.cjs
- D-06 (logging) → rules/backend/hosting.md, skills/logging, skills/project-structure
- D-07 (Swagger UI) → rules/backend/api.md, skills/project-structure, skills/swagger, skills/verify
- D-08 (backend tests) → rules/backend-tests/testing.md, skills/dotnet-testing, skills/project-structure
- D-09 (frontend stack) → rules/common/dependencies.md, rules/frontend/angular.md, skills/angular, skills/build-fix, skills/ci-cd, skills/project-structure
- D-10 (frontend libraries not by default) → rules/frontend/angular.md, skills/angular, skills/project-structure, scripts/check-dependencies.cjs
- D-11 (mapping) → skills/project-structure, scripts/check-dependencies.cjs
- D-12 (resilience) → rules/backend/integrations.md, skills/add-dependency, skills/httpclient-factory, scripts/check-dependencies.cjs
- D-13 (frontend E2E) → skills/angular, skills/project-structure
- D-14 (containers) → rules/backend/hosting.md, skills/ci-cd, skills/delivery-pipeline, skills/docker
- D-15 (API versioning) → rules/backend/api.md, skills/add-dependency, skills/api-versioning, skills/project-structure
- D-16 (solution format) → rules/common/repository-layout.md, skills/project-structure
- D-17 (shared build configuration) → rules/common/dependencies.md, rules/common/repository-layout.md, skills/project-structure, scripts/check-dependencies.cjs, Directory.Build.props, Directory.Packages.props
- D-18 (repository layout) → rules/common/repository-layout.md, skills/project-structure, scripts/check-dependencies.cjs

## Enforcement summary

Hooks run in exec form (`node` + `args`, no shell): `${CLAUDE_PROJECT_DIR}` only locates `hook.cjs`; every check runs against the active repository or linked worktree, resolved from the hook input `cwd` (or the edited file) through Git, and keeps its state per worktree in `.claude/.hook-state/` (ignored by Git). Hook input may carry a UTF-8 byte-order mark; manifests may be UTF-8 or BOM-tagged UTF-16, and unreadable content is reported as a finding.

| Mechanism | Trigger | Checks | Points to |
|---|---|---|---|
| Pre-command hook (fail-closed: a missing script, crash, timeout or unreadable input blocks the command) | Bash/PowerShell command, before execution | npm/pnpm/yarn/ng/dotnet/NuGet package additions, updates and removals (global options and `--force`/`--legacy-peer-deps` included) are denied without `# add-dependency: reviewed`; `dotnet` project-reference additions and removals are denied without `# project-references: approved`; repository-changing Git commands (table-driven classifier after global options such as `-C`) ask the user to confirm, read-only Git commands run | `add-dependency`, `project-structure`, `architecture-decision`, `CLAUDE.md` § Git |
| Post-change hook | Edit/Write of a manifest, instruction file or product input | `check-dependencies.cjs` on that manifest (project-reference changes flagged as Reserved), `check-instructions.cjs`, synchronization reminders | dependency and architecture standards, this map, `custom-settings` |
| Post-change hook | every Bash/PowerShell command, successful or failed | actual worktree state: the first observation of a worktree validates every tracked manifest and the instruction files; later observations validate only paths Git reports as changed (working tree, index, HEAD transitions) — additions, rewrites, removals and moves of `*.csproj`, `Directory.Packages.props` and `package.json`, project-reference changes, instruction files, product inputs; build output, `node_modules` and nested repositories are not observed | as above |
| Stop hook | end of a turn (once per material state of the changed files, never on its own continuation) | model change without seeder change, migrations to review, code without test changes, changed custom settings | `development-workflow`, `verify`, `custom-settings` |
| `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-dependencies.cjs"` | `verify`, `add-dependency`, `project-structure` | repository-wide manifest scan | dependency and architecture standards |
| `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.cjs"` | `template-maintenance`, post-change hook | structural predicates of this system, including the Kind direction and the hook configuration | this map |

The command classifier only routes the command forms it recognizes, before they run (nested `bash -c`, `pwsh -Command` and `cmd /c` strings included); package, reference or Git changes made indirectly by scripts or other programs are not routed. What any command actually changed is checked afterwards from the worktree state. The manual commands work from any directory of the repository or a linked worktree, in Bash and PowerShell.
