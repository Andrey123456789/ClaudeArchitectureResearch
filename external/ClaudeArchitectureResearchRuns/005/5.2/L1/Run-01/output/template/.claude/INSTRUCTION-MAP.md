> Level: 3-project | Owns: human-facing map of the instruction system (maintainer documentation) | Scope: repo/meta | Loads: never (not imported, not a rule)

# Instruction Map

How this template's instructions are organized, where each rule lives, how it
loads, what is enforced mechanically, and where new content belongs. Run
`node .claude/scripts/check-instructions.cjs` after every change to the
instruction system; maintenance procedures are in the user-invoked
`template-maintenance` skill.

## Two questions decide placement

1. **Where does it belong by stability? → Level.**
   `0-core` (operating policy, technology-neutral engineering principles) →
   `1-architecture` (role vocabulary, architecture invariants, boundaries) →
   `2-technology` (concrete technique and bindings) → `3-project` (selection,
   defaults, layout, project decisions). First match wins: project-specific
   selection/layout/default → 3; concrete non-platform technology → 2; adopted
   architecture/role/boundary → 1; otherwise 0. Conformance dependencies (a
   binding, or content that must comply with another artifact) point only to
   the same or a more stable level; references toward less stable levels are
   routing pointers (run a workflow, read a facet, see a technique skill) or
   check-by-reference items only. Core and Architecture name no
   concrete technology beyond the fixed platform vocabulary (.NET, C#, the
   `dotnet` CLI, NuGet/MSBuild, ASP.NET Core and its built-in primitives,
   `TimeProvider`, HTTP/TLS/OIDC/OpenAPI standards, Git).
2. **Can it be replaced as one module? → Capability.** Only four slots exist:
   `architecture` (required frame), `persistence` (required leaf),
   `backend-testing` (required leaf), `frontend` (optional leaf). Everything
   else — logging, validation, API documentation, caching, containers — is
   embedded and organized by level only.

Every instruction file starts with a one-line header:
`> Level: … | [Capability: <slot>/<impl> (<facet>) |] Owns: … | Scope: … | Loads: …`.
JSON data files carry the same fields in `$comment`.

## Loading mechanisms

| Mechanism | What uses it |
|---|---|
| always — `CLAUDE.md` and its `@` imports | planning-time policy: operating policy, product governance, decision control, roles, project stack, capability selection, selected decision facets |
| path — rule loads when matching files are touched | every other file under `.claude/rules/` (each declares `paths`) |
| on demand — skill invoked by the model or routed from `CLAUDE.md` / a workflow | workflow and knowledge skills |
| explicit read — a workflow step names a facet role `<slot>.<facet>` | procedural capability facets under `.claude/capabilities/<slot>/<impl>/` |
| user-only | `template-maintenance` |
| deterministic | hooks in `.claude/settings.json`, scripts in `.claude/scripts/` |
| never | this map, slot `CONTRACT.md`, module `MODULE.md`, product inputs |

## Level view

Enforcement column: `hook` = `.claude/hooks/*`, `arch` =
`check-architecture.cjs`, `pkg` = `check-packages.cjs`, `struct` =
`check-instructions.cjs`, `edcfg` = `.editorconfig`/build props.

### Level 0 — Core

| File | Owns | Scope | Loading | Enforcement | Add here |
|---|---|---|---|---|---|
| `CLAUDE.md` | entry point, imports, workflow routing | common | always | struct (imports) | new routing rows only |
| `rules/0-core/operating-policy.md` | normative vocabulary, engineering defaults, challenge duty, Git boundary | common | always | settings `ask` for destructive Git | cross-cutting operating rules needed at planning time |
| `rules/0-core/product-governance.md` | authority of product inputs, product-behavior and tunable-value approval, string semantics | common | always | hook (product-input reminder) | product-input governance |
| `rules/0-core/decision-control.md` | Decided/Delegated/Reserved, Reserved list, Decision Request, headless behavior | common | always | — | approval-boundary rules |
| `rules/0-core/minimalism.md` | dependency necessity, responsibility-driven structure | common | path `**/*` | hook (dependency guard) | anti-speculation rules |
| `rules/0-core/security.md` | secrets, input trust, SQL parameterization, authN/Z, browser clients, TLS, crypto, fail-safe, uploads, sensitive logging | common | path `**/*` | pkg (deny list) | security invariants |
| `rules/0-core/coding.md` | C# conventions, style scope | backend | path `backend/**/*` | edcfg | C# conventions |
| `rules/0-core/performance.md` | correctness first, async, time, data-access efficiency, measured optimizations, cache semantics | backend | path | — | performance and caching rules |
| `rules/0-core/error-handling.md` | expected outcomes, exception flow, logging once, safe exposure, cancellation | backend | path | — | exception/failure rules |
| `rules/0-core/http-api.md` | error contracts, status semantics, compatibility and versioning need | backend | path | — | HTTP contract rules |
| `rules/0-core/outbound-calls.md` | client lifetime, timeouts, retries, fallback, caller cancellation | backend | path | — | outbound dependency rules |
| `rules/0-core/hosting.md` | DI lifetimes, logging API, typed configuration, health checks | backend | path | — | host composition rules |
| `rules/0-core/testing.md` | framework-neutral test policy | backend-tests | path `backend/**/*Tests/**/*` | hook (stop: test reminder) | test policy independent of the framework |
| `skills/develop` | development procedure | common | on demand | hook (stop) | implementation-flow steps |
| `skills/verify` | completion verification and reporting | common | on demand | arch, pkg | completion checks |
| `skills/custom-settings` | settings synchronization | common | on demand | hook (reminder) | settings sync steps |
| `skills/git-workflow` | Git procedure | repo/meta | on demand | settings `ask` | Git steps |
| `skills/architecture-decision` | ADR recording, API deprecation | common | on demand | — | decision-recording steps |
| `skills/delivery` | CI definitions, frontend CI install, deployment migrations | common | on demand | — | pipeline/deployment steps |
| `agents/code-reviewer.md` | independent read-only review role | common | subagent | `disallowedTools` | never — keep thin |

### Level 1 — Architecture

| File | Owns | Scope | Loading | Enforcement | Add here |
|---|---|---|---|---|---|
| `rules/1-architecture/roles.md` | stable role vocabulary | common | always | — | a new role (then map it in the frame) |
| `rules/1-architecture/role-boundaries.md` | role-level boundary invariants | backend, backend-tests | path `backend/**/*` | arch | architecture rules expressible in roles |
| `rules/1-architecture/frontend-structure.md` | framework-neutral frontend structure | frontend | path `frontend/**/*` | — | frontend rules not tied to the framework |
| architecture-frame facets (`architecture.*`) | see the capability view (by facet role) | — | — | — | — |
| `skills/code-review` | review procedure and output | common | on demand / agent | — | review steps |
| `skills/build-fix` | repair procedure | common | on demand | — | repair steps |

### Level 2 — Technology

| File | Owns | Scope | Loading | Enforcement | Add here |
|---|---|---|---|---|---|
| `rules/2-technology/backend-technologies.md` | FluentValidation, Swagger metadata/exposure, Serilog registration, container images | backend | path (backend + container files) | pkg | rules for embedded backend technologies |
| `skills/security-scan` (+ `references/scan-layers.md`) | security review procedure | common | on demand | — | scan steps / layer prompts |
| knowledge skills (see below) | technique | per skill | on demand | — | examples and how-to |
| leaf facets (`*.rules`, `*.knowledge`, `*.workflow`, `*.commands`) | see the capability view (by facet role) | — | — | — | — |

### Level 3 — Project

| File | Owns | Scope | Loading | Enforcement | Add here |
|---|---|---|---|---|---|
| `rules/3-project/stack.md` | approved stack, conditional technologies, layout and build defaults | common | always | pkg, edcfg | project technology decisions |
| `rules/3-project/capability-selection.md` | selection record, declared properties, facet resolution | common | always | struct | slot selections only |
| `rules/3-project/package-management.md` | NuGet CPM and npm conventions | backend, frontend | path (projects, manifests) | hook, pkg | package-manager conventions |
| `skills/project-structure` (+ `references/solution-layout.md`) | scaffolding procedure | common | on demand | arch | scaffolding steps |
| `skills/add-dependency` | dependency procedure (project package conventions) | common | on demand | hook (dependency guard), pkg | dependency steps |
| leaf facets (`*.decision`, `*.scaffold`) | see the capability view (by facet role) | — | — | — | — |
| `skills/template-maintenance` | instruction-system maintenance | repo/meta | user-only | struct | maintenance steps |
| `.claude/settings.json`, `.claude/hooks/*`, `.claude/scripts/*`, `.editorconfig`, `Directory.Build.props`, `Directory.Packages.props` | deterministic enforcement and build defaults | common | deterministic | — | new mechanical checks |

## Capability view

Every facet is owned by the module in its row; extend a facet in place, and put
new implementation-specific content into the facet of the matching role. A
cleared optional slot keeps its contract and loses its rows here.

| Slot | Selected | Facet | Level | File | Owns | Scope | Loading | Enforcement |
|---|---|---|---|---|---|---|---|---|
| architecture (required frame) | clean-architecture | `architecture.decision` | 1 | `rules/1-architecture/adopted-architecture.md` | adopted architecture, patterns not adopted | backend | always | — |
| | | `architecture.boundaries` | 1 | `rules/1-architecture/layering.md` | role mapping, dependency direction, layer responsibilities | backend | path | arch |
| | | `architecture.layout` | 1 | `capabilities/architecture/clean-architecture/layout.md` | physical layout and placement | backend | explicit read | — |
| | | `architecture.check` | — | `capabilities/architecture/clean-architecture/check.json` | check specification and named locations | backend | scripts, stop hook | arch, stop hook |
| persistence (required leaf) | ef-core, variant sqlserver | `persistence.decision` | 3 | `rules/3-project/persistence-stack.md` | persistence stack decision | backend | always | — |
| | | `persistence.rules` | 2 | `rules/2-technology/data-access.md` | role binding, seeding, Development DB configuration | backend | path | stop hook |
| | | `persistence.knowledge` | 2 | `skills/ef-core` | implementation technique | backend | on demand | — |
| | | `persistence.workflow` | 2 | `capabilities/persistence/ef-core/workflow.md` | model/migration/seed procedure | backend | explicit read | stop hook |
| | | `persistence.scaffold` | 3 | `capabilities/persistence/ef-core/scaffold.md` | initial setup | backend | explicit read | — |
| | | `persistence.co-change` | — | `capabilities/persistence/ef-core/co-change.json` | co-change reminder rules | backend | stop hook | stop hook |
| backend-testing (required leaf) | nunit | `backend-testing.decision` | 3 | `rules/3-project/backend-testing-stack.md` | test stack decision | backend-tests | always | — |
| | | `backend-testing.rules` | 2 | `rules/2-technology/test-framework.md` | framework rules | backend-tests | path | arch |
| | | `backend-testing.knowledge` | 2 | `skills/dotnet-testing` | test technique | backend-tests | on demand | — |
| | | `backend-testing.commands` | 2 | `capabilities/backend-testing/nunit/commands.md` | test commands | backend-tests | explicit read | — |
| | | `backend-testing.scaffold` | 3 | `capabilities/backend-testing/nunit/scaffold.md` | test-project creation | backend-tests | explicit read | — |
| | | `backend-testing.check` | — | `capabilities/backend-testing/nunit/check.json` | framework adapter for the architecture check | backend-tests | architecture check | arch |
| frontend (optional leaf) | angular | `frontend.decision` | 3 | `rules/3-project/frontend-stack.md` | frontend stack decision, library limits | frontend | always | pkg |
| | | `frontend.rules` | 2 | `rules/2-technology/frontend-framework.md` | framework rules | frontend | path | — |
| | | `frontend.knowledge` | 2 | `skills/angular` | framework technique | frontend | on demand | — |
| | | `frontend.commands` | 2 | `capabilities/frontend/angular/commands.md` | workspace commands, build-fix notes | frontend | explicit read | — |
| | | `frontend.scaffold` | 3 | `capabilities/frontend/angular/scaffold.md` | workspace creation | frontend | explicit read | — |
| | | `frontend.check` | — | `capabilities/frontend/angular/check.json` | dependency commands, packages not by default | frontend | dependency hook, package check | hook, pkg |

Owner of every facet: the module named in the row (`MODULE.md` lists its
facets, declared properties, and `binds:`). Slot requirements:
`capabilities/<slot>/CONTRACT.md`. Placement belongs to the frame; technique
belongs to the leaf; leaves bind to roles and the frame's named location
`persistence implementation`.

## Skills

Workflows (procedures): `develop`, `verify`, `code-review`, `build-fix`,
`add-dependency`, `custom-settings`, `project-structure`, `delivery`,
`architecture-decision`, `git-workflow`, `security-scan`,
`template-maintenance` (user-only). Agent: `code-reviewer` (preloads
`code-review`).

Knowledge (technique, Level 2, never the sole owner of a rule): `http-api`,
`aspnet-error-handling`, `logging` (private `references/serilog.md`),
`httpclient-factory` (private `references/resilience.md`), `configuration`,
`dependency-injection`, `caching`, `swagger`, `api-versioning`, `health-check`,
`docker`, `ci-cd`, `modern-csharp`, `authentication`; module-owned: the
`<slot>.knowledge` facet of each selected module (capability view).

## Enforcement view

| Artifact | Trigger | Checks | Points to |
|---|---|---|---|
| `hooks/dependency-guard.cjs` | PreToolUse Bash | package commands without explicit version, update commands, `--prerelease`, npm `--force`/`--legacy-peer-deps`, module-declared commands (`frontend.check`) | `add-dependency` |
| `hooks/post-edit-check.cjs` | PostToolUse Edit/MultiEdit/Write/Bash | manifests → pkg + arch; `SPECIFICATION.md` / `CUSTOM_SETTINGS.md` edits → reminder | `package-management.md`, `architecture.boundaries`, `custom-settings` |
| `hooks/stop-co-change.cjs` | Stop (once; honors `stop_hook_active`) | seed/migration co-change (`persistence.co-change`), production code without test changes | `persistence.workflow`, `develop`, `verify` |
| `scripts/check-architecture.cjs` | manual, `verify`, hook | project classification, allowed references, test-framework packages | `architecture.check`, `backend-testing.check` |
| `scripts/check-packages.cjs` | manual, `verify`, hook | CPM, versionless references, floating/prerelease versions, deny/review list, lockfile, not-by-default frontend packages | `scripts/package-policy.json`, `frontend.check` |
| `scripts/check-instructions.cjs` | manual, `template-maintenance` | headers, levels, `paths`, imports, slots/modules/facets, leak and platform-vocabulary rules, references, hook commands, hygiene | this map |
| `scripts/lib/project.cjs` | shared library | project-root resolution (fails loudly), selected modules, globbing, MSBuild parsing | — |
| `settings.json` permissions | destructive Git commands | asks before force-push, hard reset, clean, branch deletion | `git-workflow` |
| `.editorconfig`, `Directory.Build.props`, `Directory.Packages.props` | build/format | formatting, file-scoped namespaces, IDE0005, shared settings, CPM | `coding.md`, `stack.md` |

Hook commands are shell-neutral: a `node -e` bootstrap without shell
metacharacters or variable expansion resolves the project directory inside Node,
and hooks report decisions as Claude Code JSON on stdout with exit code 0, so
cmd, PowerShell, and POSIX shells behave the same. Exit code 1 with a message
means a hook could not run its check.

## Where is the rule about …?

| Topic | Owner |
|---|---|
| specification authority, invented behavior, product ambiguity, string semantics | `0-core/product-governance.md` |
| custom-settings content, conflicts, new tunable values | `0-core/product-governance.md` |
| settings synchronization, schema-affecting settings | `custom-settings` |
| reading the specification first, inspecting code, review before verify, verify before completion, approved rules → durable sources, regression tests, performance-change steps | `develop` |
| simplicity, no speculative frameworks, scope preservation, challenge duty, Git mutations only on request, parallel work isolation | `0-core/operating-policy.md` |
| decision classes, Reserved list, consequential architecture approval, Decision Request, headless runs | `0-core/decision-control.md` |
| CQRS/mediator/Vertical Slice not adopted | `architecture.decision` |
| dependency direction, layer mapping, use-case orchestration and contract placement | `architecture.boundaries` |
| domain simplicity, DDD restraint, use-case and contract purity, thin entry points, composition root, registration ownership, persistence-access contracts, commit boundary, generic repository, transactions, persistence technology confinement, cache/remote leakage, DTO duplication, per-version models, test-project references, HTTP semantics at entry points | `1-architecture/role-boundaries.md` |
| physical structure, dependency necessity | `0-core/minimalism.md` |
| secrets, input trust, SQL, authorization, anonymous access, auth mechanisms, token validation, enumeration, CSRF, token storage, CORS, TLS, crypto, fail-safe, uploads, sensitive logging, payload logging | `0-core/security.md` |
| C# conventions, file/namespace/async naming, style-only rewrites | `0-core/coding.md` |
| unused usings in changed files, diff/scope review, build/test, runtime smoke, probe-to-test, risk-scoped checks, fix-and-retry, reporting | `verify` |
| correctness-first optimization, async, cancellation, `TimeProvider`, data-access efficiency, measured optimizations, caching need/lifetime/keys/invalidation | `0-core/performance.md` |
| `HttpClient` lifetime, timeouts, retries, `Retry-After`, fallback, caller cancellation | `0-core/outbound-calls.md` |
| DI injection and lifetimes, structured logging, typed options, health checks | `0-core/hosting.md` |
| `ProblemDetails`, success/401/403/409/412 semantics, empty collections, versioning need, breaking changes, versioning strategy | `0-core/http-api.md` |
| expected outcomes, central exception handling, exposure of internals, logging once, exceptions as control flow, cancellation as 500 | `0-core/error-handling.md` |
| FluentValidation boundaries, Swagger accuracy and exposure, Serilog registration, container runtime image | `2-technology/backend-technologies.md` |
| API version deprecation, ADRs | `architecture-decision` |
| test level, behavior focus, determinism, isolation, explicit cases, integration tests, provider fidelity, test data ownership, coverage, naming | `0-core/testing.md` |
| test framework choice | `backend-testing.rules` |
| persistence stack, provider | `persistence.decision` |
| seeding (representative, bootstrap concern, dedicated seeder, Development only, no schema creation, no resync, valid data), Development connection string | `persistence.rules` |
| seeder co-change, migration review | `persistence.workflow` |
| production migrations in deployment, CI definitions, frontend CI install | `delivery` |
| approved stack, platform, validation/logging/Swagger baseline, mapping and resilience conditions, Docker optional, `.slnx`, shared build files, layout | `3-project/stack.md` |
| backend testing stack | `backend-testing.decision` |
| frontend stack, libraries not by default, E2E | `frontend.decision` |
| CPM, npm lockfile and dependency categories | `3-project/package-management.md` |
| version selection, due diligence, license approval, conditional packages, resilience packages, npm force flags | `add-dependency` |
| frontend feature structure, presentation focus, HTTP boundary, error contract, lazy loading, local state | `1-architecture/frontend-structure.md` |
| framework-specific frontend rules (component model, reactive state, interceptors, forms, subscriptions) | `frontend.rules` |
| independent read-only review | `agents/code-reviewer.md` |
| review priorities, no manufactured findings | `code-review` |
| build-fix diagnosis, bounded iteration, no weakened verification, generated output at source | `build-fix` |
| security-review evidence/severity, tool independence | `security-scan` |
| destructive Git safety, minimal state-aware operations, focused staging | `git-workflow` |

## Where new content goes

- A rule needed while planning any task → an always-loaded file (keep it short;
  check the token budget). Otherwise a path-scoped rule at its level.
- A rule tied to a capability implementation → that module's rule facet
  (`Capability:` header) — never a non-module file.
- Steps of a procedure → the owning workflow skill; implementation-specific
  steps → a module procedural facet referenced by role.
- Examples and how-to → a knowledge skill (or a module-owned knowledge skill).
- A mechanical check → a script or hook that points to the rule's owner.
- A new slot is not added without a justified reason; concerns outside the four
  slots stay embedded.

## Product inputs (not instruction layers)

`SPECIFICATION.md` (empty in the template), `CUSTOM_SETTINGS.md`, optional
feature specifications, and task prompts. Their authority is defined by
product governance.
