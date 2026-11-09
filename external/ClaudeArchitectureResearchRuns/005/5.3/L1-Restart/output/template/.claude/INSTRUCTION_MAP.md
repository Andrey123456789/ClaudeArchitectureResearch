> Level: 3-project · Owns: human-facing map of the instruction system · Scope: repo/meta · Loading: never auto-loaded (maintainers only)

# Instruction Map

Two questions place every piece of content:

1. **Where does it belong by stability?** → Level: `0-core` (operating policy, technology-neutral principles) → `1-architecture` (role vocabulary, boundaries) → `2-technology` (concrete technique and bindings) → `3-project` (selection, defaults, layout). Conformance dependencies point only to the same or a more stable level; Core and Architecture name no concrete implementation technology in any form, a pure pointer included (`Technique: ...`, `area → skill`, a `(technique: ...)` aside); the only fixed-platform vocabulary is .NET, C#, TypeScript, Git, and HTTP as protocol vocabulary (ASP.NET Core and NuGet are not exempt). They refer to Level 2 only by role, capability, facet (`backend-testing.framework`), or a technique skill whose name identifies no technology (`http-api`); concrete technique, API bindings and selections live in Level 2/3 or the owning capability facet.
2. **Can it be replaced as one module?** → Capability: only the four slots `architecture` (frame), `persistence`, `backend-testing`, `frontend` (optional). Module-owned artifacts declare `Capability:` and appear in their `MODULE.md`.

Product inputs (`SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, feature specs, task prompts) sit outside the hierarchy. Each artifact starts with a one-line header (`Level`, optional `Capability`/`Facet`, `Owns`, `Scope`, `Loading`). Run `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.mjs"` after any change (works from nested directories and linked worktrees).

Scopes → paths: common `**/*`; backend `backend/**/*`; backend-tests `backend/**/*Tests/**/*`; frontend `frontend/**/*`; delivery and repo/meta are handled by workflows and hooks.

## Level 0 — Core

| File | Owns | Scope | Loading | Enforcement | Extend here when |
| --- | --- | --- | --- | --- | --- |
| `CLAUDE.md` | product inputs, engineering defaults, decision control, challenge duty, workflow routing, Git safety | common | always (entry) | Stop hook (product-source sync) | a new always-needed operating rule |
| `.claude/rules/0-core/security.md` | secrets, trust boundaries, SQL safety, authn/authz, TLS, CORS, crypto, sensitive logs, fail-safe | common | path `**/*` | manifest hook (deprecated packages) | a technology-neutral security invariant |
| `.claude/rules/0-core/engineering.md` | dependency necessity, structure discipline | common | path `**/*` | dependency-command hook | a repository-wide engineering hygiene rule |
| `.claude/rules/0-core/backend-code.md` | performance, async, time, outbound calls, caching, options, DI, logging style, C# conventions | backend | path | `.editorconfig` | a backend runtime convention without concrete libraries |
| `.claude/rules/0-core/http-api.md` | HTTP responses, error contracts, exceptions, cancellation, versioning policy, health checks | backend | path | — | an HTTP/API semantics rule |
| `.claude/rules/0-core/testing.md` | framework-neutral backend test policy | backend-tests | path | Stop hook (test reminder) | a test rule independent of the test framework |
| `.claude/rules/0-core/frontend.md` | framework-neutral frontend structure, HTTP boundary, errors, forms | frontend | path | — | a frontend rule independent of the framework |
| `.claude/skills/development-workflow/SKILL.md` | implementation procedure and conditional co-change steps | — | on invocation (routed) | Stop hook | a new implementation-phase obligation |
| `.claude/skills/verify/SKILL.md` | completion verification, probe-to-test, import hygiene, reporting | — | on invocation | — | a new completion check |
| `.claude/skills/code-review/SKILL.md` | review procedure, priorities, severity, output | — | on invocation | — | review criteria |
| `.claude/skills/build-fix/SKILL.md` | build/test repair loop | — | on invocation | — | repair technique |
| `.claude/skills/custom-settings/SKILL.md` | settings synchronization | — | on invocation | post-edit hook | settings propagation steps |
| `.claude/skills/git-workflow/SKILL.md` | Git operation procedure | repo/meta | on invocation | — | Git procedure |
| `.claude/skills/security-scan/SKILL.md` | security review procedure and report | — | on invocation | — | audit procedure |
| `.claude/skills/architecture-decision/SKILL.md` | Decision Requests, ADRs, decision-file updates | — | on invocation | — | decision recording |
| `.claude/skills/template-maintenance/SKILL.md` | maintaining this system | repo/meta | user only | checker | maintenance procedure |
| `.claude/agents/code-reviewer.md` | independent read-only review role | — | on delegation | read-only tools | — (procedure stays in `code-review`) |

## Level 1 — Architecture

| File | Owns | Capability | Scope | Loading | Enforcement | Extend here when |
| --- | --- | --- | --- | --- | --- | --- |
| `.claude/rules/1-architecture/roles.md` | role vocabulary, frame-independent boundaries | — | backend | path | — | a boundary expressible with roles only |
| `.claude/rules/1-architecture/frame/adopted-style.md` | adopted style, role → project map, patterns not adopted | architecture/clean-architecture | backend | always (import) | manifest hook (mediator packages) | a frame-level adopted/not-adopted decision |
| `.claude/rules/1-architecture/frame/boundaries.md` | layer direction and responsibilities, repositories, Unit of Work, composition, test references | architecture/clean-architecture | backend | path | `check-architecture.mjs` | a frame-specific placement rule |
| `.claude/capabilities/architecture/clean-architecture/layout.md` | physical layout, reference graph | architecture/clean-architecture | backend | workflow-read | — | layout technique |

## Level 2 — Technology

| File | Owns | Capability | Scope | Loading | Enforcement | Extend here when |
| --- | --- | --- | --- | --- | --- | --- |
| `.claude/rules/2-technology/backend-libraries.md` | FluentValidation, Swagger, Serilog, container image rules | — | backend | path | manifest hook | a usage rule for a non-slot library |
| `.claude/rules/2-technology/backend-platform.md` | ASP.NET Core/.NET API bindings of neutral Core/Architecture backend rules (entry-point mechanism, error-contract types, exception handling, async, time, outbound HTTP, logging, options, authentication facilities, secrets) | — | backend | path | — | a concrete API binding for a neutral backend rule |
| `.claude/skills/security-scan/references/scan-layers.md` | layer investigation technique (private reference of `security-scan`) | — | — | read by owner skill | — | scan heuristics |
| `.claude/rules/2-technology/persistence/access.md` | EF Core confinement, repository leak rule, bindings | persistence/ef-core | backend | path | `check-architecture.mjs` | a persistence-implementation rule |
| `.claude/rules/2-technology/persistence/seeding.md` | Development seeding | persistence/ef-core | backend | path | Stop hook (seed reminder) | a seeding rule |
| `.claude/rules/2-technology/backend-testing/test-framework.md` | test framework rule, NUnit bindings | backend-testing/nunit | backend-tests | path | manifest hook (second framework) | a framework-specific test rule |
| `.claude/rules/2-technology/frontend/framework.md` | Angular framework rules | frontend/angular | frontend | path | — | a framework-specific frontend rule |
| `.claude/capabilities/persistence/ef-core/workflow.md` | persistence change procedure | persistence/ef-core | backend | workflow-read | Stop hook | a persistence procedure step |
| `.claude/capabilities/persistence/ef-core/commands.md` | persistence packages and commands | persistence/ef-core | backend | workflow-read | — | persistence commands |
| `.claude/capabilities/backend-testing/nunit/commands.md` | test packages and commands | backend-testing/nunit | backend-tests | workflow-read | — | test commands |
| `.claude/capabilities/frontend/angular/commands.md` | frontend commands, build-fix notes | frontend/angular | frontend | workflow-read | — | frontend commands |
| `.claude/skills/ef-core/SKILL.md` | EF Core technique | persistence/ef-core | — | on demand | — | EF Core examples |
| `.claude/skills/dotnet-testing/SKILL.md` | testing technique | backend-testing/nunit | — | on demand | — | test examples |
| `.claude/skills/angular/SKILL.md` | Angular technique | frontend/angular | — | on demand | — | Angular examples |
| `.claude/skills/http-api/SKILL.md` | HTTP status reference | — | — | on demand | — | status examples |
| `.claude/skills/aspnet-error-handling/SKILL.md` | exception/validation technique | — | — | on demand | — | error-handling examples |
| `.claude/skills/logging/SKILL.md` | logging technique | — | — | on demand | — | logging examples |
| `.claude/skills/logging/references/serilog.md` | Serilog depth (private) | — | — | read by owner skill | — | Serilog setup |
| `.claude/skills/httpclient-factory/SKILL.md` | outbound HTTP technique | — | — | on demand | — | client examples |
| `.claude/skills/httpclient-factory/references/resilience.md` | resilience depth (private) | — | — | read by owner skill | — | resilience strategies |
| `.claude/skills/configuration/SKILL.md` | options and secrets technique | — | — | on demand | — | configuration examples |
| `.claude/skills/dependency-injection/SKILL.md` | DI technique | — | — | on demand | — | composition examples |
| `.claude/skills/caching/SKILL.md` | caching technique | — | — | on demand | — | cache examples |
| `.claude/skills/swagger/SKILL.md` | Swagger technique | — | — | on demand | — | documentation examples |
| `.claude/skills/api-versioning/SKILL.md` | versioning technique | — | — | on demand | — | versioning examples |
| `.claude/skills/health-check/SKILL.md` | health-check technique | — | — | on demand | — | probe examples |
| `.claude/skills/docker/SKILL.md` | container technique | — | — | on demand | — | container examples |
| `.claude/skills/ci-cd/SKILL.md` | pipeline technique | — | — | on demand | — | pipeline examples |
| `.claude/skills/modern-csharp/SKILL.md` | C# language technique | — | — | on demand | `.editorconfig` | language-feature guidance |
| `.claude/skills/authentication/SKILL.md` | authn/authz technique | — | — | on demand | — | auth examples |
| `.claude/capabilities/persistence/CONTRACT.md` | persistence slot contract | (slot) | — | maintainer | checker | new required persistence facet |
| `.claude/capabilities/backend-testing/CONTRACT.md` | backend-testing slot contract | (slot) | — | maintainer | checker | new required test facet |
| `.claude/capabilities/frontend/CONTRACT.md` | frontend slot contract | (slot) | — | maintainer | checker | new required frontend facet |
| `.claude/capabilities/persistence/ef-core/MODULE.md` | module manifest | persistence/ef-core | — | maintainer | checker | facet added/removed |
| `.claude/capabilities/backend-testing/nunit/MODULE.md` | module manifest | backend-testing/nunit | — | maintainer | checker | facet added/removed |
| `.claude/capabilities/frontend/angular/MODULE.md` | module manifest | frontend/angular | — | maintainer | checker | facet added/removed |

`.claude/capabilities/architecture/CONTRACT.md` (slot contract) and `.claude/capabilities/architecture/clean-architecture/MODULE.md` (manifest) are Level 1 maintainer metadata, never auto-loaded.

## Level 3 — Project

| File | Owns | Capability | Scope | Loading | Enforcement | Extend here when |
| --- | --- | --- | --- | --- | --- | --- |
| `.claude/rules/3-project/decisions.md` | approved stack, conditional technologies, layout defaults, capability selection (decision summary) | — | common | always (import) | checker, manifest hook | a project-level decision or selection change |
| `.claude/rules/3-project/frontend-stack.md` | frontend stack decisions | frontend/angular | frontend | always (import) | manifest hook | a frontend stack decision |
| `.claude/rules/3-project/package-management.md` | NuGet CPM, npm conventions | — | backend, frontend | path | manifest hook | a package-management convention |
| `.claude/rules/3-project/development-database.md` | local Development database default | persistence/ef-core | backend | path | — | a Development configuration default |
| `.claude/skills/add-dependency/SKILL.md` | dependency procedure, conditional package choices | — | — | on invocation | dependency-command and manifest hooks | a package-selection step |
| `.claude/skills/project-structure/SKILL.md` | scaffolding/restructuring procedure | — | — | on invocation | `check-architecture.mjs` | a scaffolding step |
| `.claude/skills/project-structure/references/solution-layout.md` | repository layout (private) | — | — | read by owner skill | — | top-level layout |
| `.claude/skills/project-structure/references/baseline-packages.md` | baseline package list (private) | — | — | read by owner skill | — | baseline package mapping |
| `.claude/INSTRUCTION_MAP.md` | this map | — | repo/meta | never | checker (coverage) | every new artifact |

## Capability view

| Slot | Selected | Facet | File | Level | Loading | Owner of |
| --- | --- | --- | --- | --- | --- | --- |
| architecture (frame) | clean-architecture | `architecture.style` | `.claude/rules/1-architecture/frame/adopted-style.md` | 1 | always | adopted style, patterns not adopted |
| | | `architecture.boundaries` | `.claude/rules/1-architecture/frame/boundaries.md` | 1 | path | layer boundaries and placement |
| | | `architecture.layout` | `.claude/capabilities/architecture/clean-architecture/layout.md` | 1 | workflow-read | physical layout |
| | | `architecture.check` | `.claude/capabilities/architecture/clean-architecture/check.json` | 1 | scripts/hooks | check specification |
| persistence | ef-core (sqlserver) | `persistence.access` | `.claude/rules/2-technology/persistence/access.md` | 2 | path | EF Core boundary, bindings |
| | | `persistence.seeding` | `.claude/rules/2-technology/persistence/seeding.md` | 2 | path | seeding |
| | | `persistence.dev-config` | `.claude/rules/3-project/development-database.md` | 3 | path | Development connection default |
| | | `persistence.workflow` | `.claude/capabilities/persistence/ef-core/workflow.md` | 2 | workflow-read | migration/seed co-change procedure |
| | | `persistence.commands` | `.claude/capabilities/persistence/ef-core/commands.md` | 2 | workflow-read | commands |
| | | `persistence.enforcement` | `.claude/capabilities/persistence/ef-core/enforcement.json` | 2 | scripts/hooks | package boundary, co-change globs |
| | | `persistence.knowledge` | `.claude/skills/ef-core/SKILL.md` | 2 | on demand | technique |
| backend-testing | nunit | `backend-testing.framework` | `.claude/rules/2-technology/backend-testing/test-framework.md` | 2 | path | framework rule |
| | | `backend-testing.commands` | `.claude/capabilities/backend-testing/nunit/commands.md` | 2 | workflow-read | commands |
| | | `backend-testing.enforcement` | `.claude/capabilities/backend-testing/nunit/enforcement.json` | 2 | scripts | test-project adapter |
| | | `backend-testing.knowledge` | `.claude/skills/dotnet-testing/SKILL.md` | 2 | on demand | technique |
| frontend (optional) | angular | `frontend.framework` | `.claude/rules/2-technology/frontend/framework.md` | 2 | path | framework rules |
| | | `frontend.stack` | `.claude/rules/3-project/frontend-stack.md` | 3 | always | stack decisions |
| | | `frontend.commands` | `.claude/capabilities/frontend/angular/commands.md` | 2 | workflow-read | commands |
| | | `frontend.enforcement` | `.claude/capabilities/frontend/angular/enforcement.json` | 2 | hooks | manifest approval list |
| | | `frontend.knowledge` | `.claude/skills/angular/SKILL.md` | 2 | on demand | technique |

Selection record: `.claude/rules/3-project/decisions.md` § Capability selection (the only place outside modules that names implementations, besides this map). Changing a selection is Reserved and needs an ADR (`architecture-decision`).

## Deterministic enforcement

| Asset | Checks | Points to |
| --- | --- | --- |
| `.claude/settings.json` | registers hooks in exec form (`command: node`, `args: ["${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.mjs"]`, the placeholder is argument data, no shell); the critical PreToolUse gate sets `onFailure: "block"`; post and Stop hooks stay non-blocking | — |
| `.claude/hooks/pre-shell-command.mjs` | PreToolUse Bash/PowerShell, critical, fails closed (missing script, crash, timeout, empty or malformed input block the command): dependency changes (`dotnet add/remove package`, `dotnet package add/remove/update`, `dotnet tool install`, npm/pnpm/yarn mutations incl. global options such as `--prefix`, `--workspace`, `--dir`, `--cwd`, `ng add`) → deny once, route to `add-dependency`; project-reference changes (`dotnet add/remove ... reference`, `dotnet reference add/remove`) → ask (Reserved unless it implements the approved layout); peer-dependency bypass flags → ask. Deny-once state lives in the active worktree | `add-dependency`, `project-structure`, `architecture-decision` |
| `.claude/hooks/post-change-checks.mjs` + `.claude/hooks/manifest-policy.json` | PostToolUse Edit/Write/MultiEdit (edited file) and Bash/PowerShell, plus PostToolUseFailure Bash/PowerShell: validates the actual manifest state of the active worktree regardless of command text (per-worktree snapshot; first observation validates all manifests, later calls only added/changed/removed/moved ones, HEAD transitions included): versionless `PackageReference`, CPM switch, floating/prerelease versions, denied and approval-required packages (project + module lists), removed or moved project files, project-reference direction; UTF-8/UTF-16 BOM decoding with visible errors; product-source sync reminder | package-management rule, `add-dependency`, frame boundaries, `project-structure`, `custom-settings` |
| `.claude/hooks/stop-cochange.mjs` | Stop reminder per material change state of the active worktree (model change without seeder/migration change, production code without test change, product-source change); unchanged state stays silent, a further change to the same file reminds again; `stop_hook_active` prevents loops | `persistence.workflow`, `verify`, `custom-settings` |
| `.claude/scripts/check-architecture.mjs` | project-reference graph, persistence/transport packages in inner roles, test-reference narrowness, top-level `tests/` | frame boundaries, persistence access |
| `.claude/scripts/check-instructions.mjs` | headers and levels, rule paths, conformance direction, selection, slot contracts and manifests (required facets, `binds:`, leak tokens, frame terms), imports, leakage, Core/Architecture technology neutrality (no pointer exemption; case-, separator- and Markdown-insensitive vocabulary plus API shapes), references, required skills, exec-form hook registrations, map coverage | this map |
| `.claude/scripts/lib/project.mjs` | shared launcher/active-root resolution (hook input `cwd`, Git), BOM-aware decoding, hook input parsing, selection/facet/manifest parsing | — |
| `.editorconfig`, `Directory.Build.props`, `Directory.Packages.props`, `.gitignore` | formatting and naming, shared build settings, Central Package Management, ignored artifacts | backend code rule, package-management rule |

## Policy locator

| Topic | Authoritative owner |
| --- | --- |
| Specification authority, product invention, ambiguity approval, string semantics | `CLAUDE.md` § Product inputs |
| Custom settings content, conflicts, new values, exclusions | `CLAUDE.md` § Product inputs; propagation: `custom-settings` |
| Simplicity, no speculative frameworks, scope preservation | `CLAUDE.md` § Engineering defaults |
| Decided/Delegated/Reserved, Decision Requests, consequential changes, headless behavior | `CLAUDE.md` § Decision control |
| Challenge questionable requests | `CLAUDE.md` § Challenge before implementing |
| Git mutations and parallel work | `CLAUDE.md` § Git; procedure: `git-workflow` |
| Reading the specification, inspection, review-before-verify, verify-before-done, regression tests, performance changes, API deprecation, CI and production migrations | `development-workflow` |
| Diff inspection, builds/tests, smoke checks, probe-to-test, risk-scoped checks, fix-and-retry, reporting, unused usings | `verify` |
| Review priorities, no manufactured findings | `code-review`; independent read-only role: `code-reviewer` agent |
| Reproduction-first repair, bounded iteration, no weakened tests, generated code | `build-fix` |
| Security review evidence/severity, scanner independence | `security-scan` |
| Version selection, due diligence, license approval, resilience/versioning packages, npm force flags | `add-dependency` |
| Adopted architecture, mediator/CQRS/VSA not adopted | frame `adopted-style.md` |
| Layer direction, domain richness, Application Services, controllers, repositories, Unit of Work, DI registration placement, DTO duplication, test references | frame `boundaries.md` |
| HTTP semantics at the entry point, expected outcomes, cache/remote-HTTP leaks, versioned models | `roles.md` |
| EF Core confinement, repository contract leaks | `persistence/access.md` |
| Development seeding | `persistence/seeding.md`; co-change, migrations, schema-affecting settings: `persistence.workflow` |
| HTTP statuses, ProblemDetails, exceptions, cancellation, versioning, health checks | `0-core/http-api.md` |
| Validation boundaries, Swagger truthfulness/exposure, Serilog integration, runtime images | `2-technology/backend-libraries.md` |
| Async, cancellation, time, HttpClient, timeouts, retries, fallback, caching, options, DI lifetimes, logging style, C# conventions | `0-core/backend-code.md` |
| Concrete ASP.NET Core/.NET API bindings of the neutral Core/Architecture backend rules (entry-point mechanism, problem-details types, exception handler, async/time/HTTP-client/logging/options APIs, authentication facilities, local secrets) | `2-technology/backend-platform.md` (bindings only; the neutral rule stays the owner) |
| Secrets, input trust, SQL, authorization, TLS, CORS, crypto, sensitive logging, fail-safe | `0-core/security.md` |
| Test levels, behavior, isolation, explicit cases, integration tests, provider fidelity, test data, coverage, naming | `0-core/testing.md`; framework: `backend-testing/test-framework.md` |
| Frontend structure and boundaries | `0-core/frontend.md`; framework: `frontend/framework.md`; stack: `frontend-stack.md` |
| Stack, conditional technologies, layout, Docker optionality, capability selection | `3-project/decisions.md` |
| Central Package Management, npm | `3-project/package-management.md` |
| Local Development connection | `3-project/development-database.md` |
| Dependency necessity, physical structure | `0-core/engineering.md` |
