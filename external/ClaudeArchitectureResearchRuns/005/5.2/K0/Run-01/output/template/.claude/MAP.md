<!-- Kind: none (human reference) | Scope: repo/meta | Owns: instruction-system map for maintainers | Loads: never auto-loaded -->
# Instruction Map

Human reference for maintainers; Claude does not load this file automatically. The system is organized by two questions: **what is it** (Kind) and **where does it apply** (Scope). The answers determine location, loading mechanism and owner. Structure is checked by `node .claude/scripts/check-instructions.mjs`; changes follow the user-invoked `template-maintenance` workflow.

## Placement

| Kind | Responsibility | Location | Loading |
|---|---|---|---|
| OP — Operating Policy | Agent behavior: precedence, product governance, decision protocol, challenge, completion, Git safety, routing | `CLAUDE.md` | Always (session start) |
| DEC — Decisions | Accepted architecture/stack choices, patterns not adopted, conditional technologies; summary + `Details in` + `Affects` | `docs/architecture/decision-register.md` (ADRs in a `decisions` folder under `docs/` when created) | Always (imported by `CLAUDE.md`) |
| STD — Standards | Normative must/default/prefer rules for one scope | `.claude/rules/<scope>/<responsibility>.md` | Path-scoped (`paths:`) |
| KNW — Knowledge | Technique, examples, trade-offs | `.claude/skills/<name>/SKILL.md` (+ private `references/`) | On demand (model-invoked) |
| WF — Workflows | Procedures, steps, stop conditions, outputs | `.claude/skills/<name>/SKILL.md`, `.claude/agents/` | Workflow invocation (routed by `CLAUDE.md`) |
| ENF — Enforcement | Hooks, scripts, build/format configuration | `.claude/settings.json`, `.claude/hooks/`, `.claude/scripts/`, root build files | Events and checks |
| IN — Product Inputs | Product behavior and approved values | `SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, feature specs | Read as input; never an instruction layer |

Ask "is it a decision, standard, knowledge, workflow, enforcement or input?", then "where does it apply?". Create a file only for a real responsibility — never to fill an empty Kind × Scope cell.

## Scopes

| Scope | Canonical standard `paths:` | Standards directory |
|---|---|---|
| common | `backend/**`, `frontend/**`, `*.slnx`, `*.props`, `global.json`, `**/*.yml`, `**/*.yaml`, `**/Dockerfile*`, `**/.env*` | `.claude/rules/common/` |
| backend | `backend/**` | `.claude/rules/backend/` |
| backend-tests | `backend/**/*Tests/**` | `.claude/rules/backend-tests/` |
| frontend | `frontend/**` | `.claude/rules/frontend/` |
| delivery | `**/Dockerfile*`, `**/*.yml`, `**/*.yaml`, `**/.dockerignore` | `delivery/` under `.claude/rules/` — not created yet: current delivery policy is workflow-triggered (`delivery-pipeline`) |
| repo/meta | — | none (repo/meta policy is OP or WF) |

Layout convention: `backend/<Name>.<Layer>/...` and `frontend/<Name>.Web/...`.

## Kind × Scope

| Kind \ Scope | common | backend | backend-tests | frontend | delivery | repo/meta |
|---|---|---|---|---|---|---|
| OP | `CLAUDE.md` | | | | | |
| DEC | decision register | | | | | |
| STD | security, dependencies, structure | architecture, persistence, api, error-handling, security, csharp, outbound-http, caching, operations | testing | angular, security | | |
| KNW | | ef-core, http-api, aspnet-error-handling, logging, httpclient-factory, configuration, dependency-injection, caching, swagger, api-versioning, health-check, modern-csharp, authentication | dotnet-testing | angular | docker, ci-cd | |
| WF | development-workflow, project-structure, verify, code-review, agent code-reviewer, build-fix, custom-settings, security-scan, add-dependency, architecture-decision | project-structure backend-layout reference | | | delivery-pipeline | git-workflow, template-maintenance |
| ENF | check-manifests, `.editorconfig` | `Directory.Build.props`, `Directory.Packages.props` | | | | `settings.json`, hooks, check-instructions |
| IN | `SPECIFICATION.md`, `CUSTOM_SETTINGS.md` | | | | | |

## Catalog

Paths below `.claude/` are written without that prefix.

### OP, DEC, IN

| File | Kind / Scope | Owns | Loading | Enforcement | Extend here |
|---|---|---|---|---|---|
| CLAUDE.md | OP / common | Precedence, product governance, engineering defaults, decision protocol, challenge, completion, Git safety, routing | Always | check-instructions (structure, references) | New agent-behavior policy or routing rows only; procedures go to workflows |
| docs/architecture/decision-register.md | DEC / common | All accepted decisions with `Details in` and `Affects` | Always (`@` import) | check-instructions (IDs, targets, Affects), check-manifests (gated packages) | New row via `architecture-decision` |
| SPECIFICATION.md | IN / common | Product behavior (empty in the template) | Read by `development-workflow` | post-edit reminder | Product requirements |
| CUSTOM_SETTINGS.md | IN / common | Approved tunable values | Read when limits/defaults matter | post-edit reminder → `custom-settings` | Approved settings rows |

### STD — Standards

Every standard is loaded path-scoped by its scope's canonical `paths:` (§ Scopes) and structure-checked by check-instructions.

| File | Scope | Owns | Loading | Enforcement | Extend here |
|---|---|---|---|---|---|
| rules/common/security.md | common | Secrets, input trust, server authority, TLS, sensitive and payload logging, fail-safe controls | Path: common globs | check-instructions; review/scan checklists | Cross-stack security invariants |
| rules/common/dependencies.md | common | Dependency need, Central Package Management, npm conventions | Path: common globs | check-manifests, pre-command guard | Manifest conventions |
| rules/common/structure.md | common | Physical structure follows responsibilities | Path: common globs | check-instructions | Repository-structure rules |
| rules/backend/architecture.md | backend | Layer dependencies, layer responsibilities, DI, boundary leaks | Path: `backend/**` | check-manifests (project references) | Layering rules |
| rules/backend/persistence.md | backend | Repositories, Unit of Work, EF Core boundary, database access, development seeding | Path: `backend/**` | stop co-change check | Persistence rules |
| rules/backend/api.md | backend | HTTP semantics ownership, status codes, API versioning, OpenAPI accuracy | Path: `backend/**` | check-instructions | HTTP contract rules |
| rules/backend/error-handling.md | backend | Error contracts, exception flow, expected outcomes, validation boundaries, cancellation outcomes | Path: `backend/**` | check-instructions | Error/validation rules |
| rules/backend/security.md | backend | Server-side authentication/authorization, cryptography, CORS, uploads | Path: `backend/**` | check-instructions | Server security rules |
| rules/backend/csharp.md | backend | C# conventions and style guidance, async/cancellation, time, optimization discipline | Path: `backend/**` | `.editorconfig` | C# code rules |
| rules/backend/outbound-http.md | backend | HttpClient lifetime, timeouts, retries, fallback, caller cancellation | Path: `backend/**` | check-manifests (deprecated resilience packages) | Outbound integration rules |
| rules/backend/caching.md | backend | Caching need, keys, expiration, invalidation | Path: `backend/**` | check-manifests (distributed cache gate) | Caching rules |
| rules/backend/operations.md | backend | Logging usage, typed configuration, Development connection string, Swagger exposure, health checks, container images | Path: `backend/**` | check-instructions | Hosting/operational rules |
| rules/backend-tests/testing.md | backend-tests | Test framework use, levels, behavior focus, isolation, readability, test references | Path: `backend/**/*Tests/**` | check-manifests (test references, second framework), stop co-change check | Test rules |
| rules/frontend/angular.md | frontend | Angular structure, components, state, HTTP boundary, errors, forms, RxJS | Path: `frontend/**` | check-manifests (default-excluded npm libraries) | Angular rules |
| rules/frontend/security.md | frontend | CSRF with cookie auth, token storage | Path: `frontend/**` | check-instructions | Browser security rules |

### WF — Workflows

Every workflow is structure-checked by check-instructions; standards it relies on are read explicitly inside the workflow.

| File | Scope | Owns | Loading (invoked by) | Enforcement | Extend here |
|---|---|---|---|---|---|
| skills/development-workflow/SKILL.md | common | Implementation procedure, co-change obligations, review/verify gates | `CLAUDE.md` routing | stop co-change check | Steps of normal implementation work |
| skills/project-structure/SKILL.md | common | Scaffolding and restructuring procedure | Routing | check-manifests | Scaffolding steps |
| skills/project-structure/references/solution-layout.md | common | Repository layout reference (private) | Read by project-structure | check-instructions | Top-level layout details |
| skills/project-structure/references/backend-layout.md | backend | Backend folders and reference commands (private) | Read by project-structure | check-manifests (references) | Backend folder conventions |
| skills/project-structure/references/scaffold-stack.md | common | Baseline packages and configuration (private) | Read by project-structure | check-manifests | Scaffolding package details |
| skills/verify/SKILL.md | common | Completion verification, probe preservation, using cleanup, reporting | development-workflow, routing | stop co-change check, `.editorconfig` | Verification steps |
| skills/code-review/SKILL.md | common | Review procedure, priorities, output | development-workflow, agent | check-instructions | Review checks |
| agents/code-reviewer.md | common | Independent read-only reviewer role (delegates to code-review) | Subagent: development-workflow or user | `disallowedTools` (no edits) | — (keep thin) |
| skills/build-fix/SKILL.md | common | Build/test repair loop | Routing | check-instructions | Repair technique |
| skills/custom-settings/SKILL.md | common | Settings synchronization | Routing | post-edit reminder | Synchronization steps |
| skills/git-workflow/SKILL.md | repo/meta | Requested Git operations, user-work protection, commit scope | Routing | pre-command guard (Git) | Git procedures |
| skills/security-scan/SKILL.md | common | Static security review procedure | Routing, code-review | check-instructions | Scan procedure |
| skills/security-scan/references/scan-layers.md | common | Layer investigation prompts (private) | Read by security-scan | check-instructions | Investigation prompts |
| skills/add-dependency/SKILL.md | common | Package selection, due diligence, license gate, installation | Routing | pre-command guard (packages), check-manifests | Dependency procedure |
| skills/architecture-decision/SKILL.md | common | Decision requests, recording, propagation, API version deprecation | Routing | check-instructions (register, Affects) | Decision procedure |
| skills/delivery-pipeline/SKILL.md | delivery | CI/CD, deployment and production migration procedure | Routing | check-instructions | Pipeline procedure |
| skills/template-maintenance/SKILL.md | repo/meta | Instruction-system maintenance | User only (`disable-model-invocation`) | check-instructions | Maintenance steps |

### KNW — Knowledge

Every knowledge skill loads on demand (model-invoked from its description); check-instructions rejects "must" statements in knowledge. Extend technique in the matching skill; a normative statement found while writing technique goes to the owning standard.

| File | Scope | Owns | Loading | Enforcement | Normative owner it serves |
|---|---|---|---|---|---|
| skills/ef-core/SKILL.md | backend | EF Core technique | On demand | check-instructions | rules/backend/persistence.md |
| skills/http-api/SKILL.md | backend | Status-code reference | On demand | check-instructions | rules/backend/api.md |
| skills/aspnet-error-handling/SKILL.md | backend | Exception handling and validation technique | On demand | check-instructions | rules/backend/error-handling.md |
| skills/dotnet-testing/SKILL.md | backend-tests | .NET testing technique | On demand | check-instructions | rules/backend-tests/testing.md |
| skills/logging/SKILL.md | backend | Logging technique | On demand | check-instructions | rules/backend/operations.md |
| skills/logging/references/serilog.md | backend | Serilog configuration (private) | Read by logging | check-instructions, check-manifests (deprecated sink) | rules/backend/operations.md |
| skills/httpclient-factory/SKILL.md | backend | Outbound HTTP technique | On demand | check-instructions | rules/backend/outbound-http.md |
| skills/httpclient-factory/references/resilience.md | backend | Resilience technique (private) | Read by httpclient-factory | check-instructions, check-manifests (Polly gates) | rules/backend/outbound-http.md |
| skills/configuration/SKILL.md | backend | Configuration technique | On demand | check-instructions | rules/backend/operations.md |
| skills/dependency-injection/SKILL.md | backend | DI technique | On demand | check-instructions | rules/backend/architecture.md |
| skills/caching/SKILL.md | backend | Caching technique | On demand | check-instructions | rules/backend/caching.md |
| skills/swagger/SKILL.md | backend | Swagger/OpenAPI technique | On demand | check-instructions | rules/backend/api.md, rules/backend/operations.md |
| skills/api-versioning/SKILL.md | backend | Versioning technique | On demand | check-instructions, check-manifests (versioning gate) | rules/backend/api.md |
| skills/health-check/SKILL.md | backend | Health-check technique | On demand | check-instructions | rules/backend/operations.md |
| skills/docker/SKILL.md | delivery | Container technique | On demand | check-instructions | rules/backend/operations.md, delivery-pipeline |
| skills/ci-cd/SKILL.md | delivery | CI/CD examples | On demand | check-instructions | delivery-pipeline |
| skills/angular/SKILL.md | frontend | Angular technique | On demand | check-instructions | rules/frontend/angular.md |
| skills/modern-csharp/SKILL.md | backend | C# feature technique | On demand | check-instructions | rules/backend/csharp.md |
| skills/authentication/SKILL.md | backend | Authentication/authorization technique | On demand | check-instructions | rules/backend/security.md |

### ENF — Enforcement

| File | Scope | Trigger | Checks | Points to |
|---|---|---|---|---|
| settings.json | repo/meta | Claude Code | Registers the hooks below (`node <script>` commands, no shell expansion) | — |
| hooks/pre-command-guard.mjs | repo/meta | PreToolUse (Bash, PowerShell) | Package-changing commands; repository-changing Git commands | add-dependency; CLAUDE.md § Git Safety, git-workflow |
| hooks/post-edit-checks.mjs | repo/meta | PostToolUse (Write, Edit, MultiEdit) | Manifests → check-manifests; product inputs → reminders; instruction files → check-instructions | dependencies standard, custom-settings, template-maintenance |
| hooks/stop-co-change-check.mjs | repo/meta | Stop (once per change set) | Model change without seeder change; migrations; production code without tests | development-workflow, verify |
| hooks/hook-io.mjs | repo/meta | Imported | Hook input parsing, project-root resolution, exit codes | — |
| scripts/check-manifests.mjs | common | CLI, post-edit hook, verify | CPM, versions, deprecated and gated packages, project references, npm lockfile/categories | dependencies, architecture and testing standards; register |
| scripts/check-instructions.mjs | repo/meta | CLI, post-edit hook, template-maintenance | Kind/Scope headers and placement, rule paths, procedures in standards, KNW must-statements, references, register, map, hooks, budget | this map, template-maintenance |
| .editorconfig | common | IDE, compiler, `dotnet format` | Formatting, namespace/using/naming preferences | rules/backend/csharp.md |
| Directory.Build.props | backend | MSBuild | Shared target framework, nullable, implicit usings | DEC-PLAT-01, DEC-BUILD-01 |
| Directory.Packages.props | backend | NuGet restore | Central Package Management | rules/common/dependencies.md |

Hooks resolve the project root from `CLAUDE_PROJECT_DIR` or the hook input inside Node, and exit with code 1 and a clear message when they cannot run, instead of skipping silently.

## Decision → Affects

- DEC-ARCH-01 → STD backend/architecture, STD backend/persistence, WF project-structure, WF code-review, KNW dependency-injection, KNW ef-core, ENF check-manifests
- DEC-PLAT-01 → ENF Directory.Build.props, WF project-structure, WF delivery-pipeline, KNW ci-cd, KNW docker, KNW modern-csharp
- DEC-DATA-01 → STD backend/persistence, STD backend/operations, KNW ef-core, KNW dotnet-testing, WF project-structure
- DEC-VAL-01 → STD backend/error-handling, KNW aspnet-error-handling, WF project-structure
- DEC-LOG-01 → STD backend/operations, KNW logging, WF project-structure
- DEC-DOCS-01 → STD backend/operations, STD backend/api, KNW swagger, WF verify, WF project-structure
- DEC-BUILD-01 → ENF Directory.Build.props, ENF Directory.Packages.props, ENF check-manifests, STD common/dependencies, WF project-structure
- DEC-LAYOUT-01 → STD common/structure, WF project-structure, KNW ci-cd, KNW docker, ENF check-instructions
- DEC-TEST-01 → STD backend-tests/testing, KNW dotnet-testing, WF project-structure, WF verify, ENF check-manifests
- DEC-WEB-01 → STD frontend/angular, KNW angular, WF project-structure, KNW ci-cd
- DEC-ARCH-02 → STD backend/architecture, STD backend/error-handling, WF code-review, WF project-structure, ENF check-manifests
- DEC-WEB-02 → STD frontend/angular, KNW angular, ENF check-manifests
- DEC-MAP-01 → WF add-dependency, WF project-structure
- DEC-RES-01 → STD backend/outbound-http, KNW httpclient-factory, WF add-dependency, ENF check-manifests
- DEC-VER-01 → STD backend/api, KNW api-versioning, KNW swagger, WF add-dependency
- DEC-WEB-03 → KNW angular, WF project-structure
- DEC-OPS-01 → KNW docker, KNW ci-cd, WF delivery-pipeline, STD backend/operations

## Policy Locator

| Topic | Authoritative owner |
|---|---|
| Specification authority; no invented behavior; product ambiguity approval; string semantics; settings consistency; tunable values; settings exclusions | `CLAUDE.md` § Product Inputs |
| Proportional simplicity; no speculative frameworks/infrastructure; focused scope and preserved behavior | `CLAUDE.md` § Engineering Defaults |
| Decided/Delegated/Reserved; Reserved list incl. consequential architecture changes; five-question test; Decision Request; headless behavior | `CLAUDE.md` § Decisions |
| Challenge questionable requests | `CLAUDE.md` § Challenge Before Implementing |
| Git mutations need an explicit request; branch/worktree isolation | `CLAUDE.md` § Git Safety |
| Approved technology not silently replaced; architecture, platform, persistence, validation, logging, Swagger, build files, layout, testing stack, Angular stack, not-adopted patterns and libraries, conditional technologies | decision register |
| Secrets; untrusted input; server-side authorization; TLS; sensitive and payload logging; fail-safe checks; visible security configuration failure | rules/common/security.md |
| Dependencies need a current requirement; Central Package Management; npm lockfile and categories | rules/common/dependencies.md |
| No speculative projects, folders or generic buckets | rules/common/structure.md |
| Inward dependencies; Domain independence; simple domain; Rich Domain approval; no decorative DDD; Application Services; Application abstractions; no EF/transport types in Application; thin controllers; composition root; DI defaults and lifetimes; cache/HTTP/version/DTO boundary leaks | rules/backend/architecture.md |
| Specific repositories; no IQueryable leaks; generic repository only in Infrastructure; Unit of Work; transactions; EF Core boundary; parameterized SQL; efficient queries; development seeding rules | rules/backend/persistence.md |
| HTTP semantics in Api; success statuses; empty collections; 401/403; 409/412; versioning need, compatibility and strategy; OpenAPI accuracy | rules/backend/api.md |
| ProblemDetails; no failure internals; central exception handling; no exception branching; expected outcomes; log exceptions once; validation boundaries; cancellation is not a 500 | rules/backend/error-handling.md |
| Deliberate anonymous access; platform authentication; Bearer validation; enumeration-safe failures; cryptography and Data Protection; CORS; upload metadata | rules/backend/security.md |
| C# conventions and style; file/async naming; no unrelated style rewrites; async I/O; cancellation propagation; TimeProvider; optimization evidence | rules/backend/csharp.md |
| HttpClient lifetime; bounded time; retry safety; Retry-After; fallback semantics; caller cancellation | rules/backend/outbound-http.md |
| Caching need; keys; expiration; invalidation | rules/backend/caching.md |
| Structured logging; Serilog integration; typed options; Development connection string; Swagger UI exposure; health checks; container runtime image | rules/backend/operations.md |
| Test framework; test level; integration tests; provider fidelity; behavior over implementation; isolation; owned test data; explicit cases; coverage; naming; narrow test references | rules/backend-tests/testing.md |
| Standalone/feature organization; focused components; signals vs RxJS; lazy loading; local state; HTTP boundary; interceptors; API error contract; forms; RxJS subscriptions | rules/frontend/angular.md |
| CSRF with cookie authentication; token storage | rules/frontend/security.md |
| Read the specification; inspect code; seeder co-change; migration review; regression tests; performance changes; record approved behavior; review before verify; verify before completion | skills/development-workflow § 1–7 |
| Final diff inspection; build/test; runtime smoke; preserve behavioral probes; risk-scoped checks; changed-file using cleanup; fix and retry; truthful reporting | skills/verify |
| Review priorities; no manufactured findings | skills/code-review |
| Independent read-only reviewer | agents/code-reviewer.md |
| Reproduce and diagnose; bounded iteration; never weaken verification; fix generated output at its source | skills/build-fix |
| Settings propagation; schema-affecting settings | skills/custom-settings |
| Never destroy user work; state-aware minimal Git operations; focused staging and commits | skills/git-workflow |
| Evidence-based severity; scanner independence | skills/security-scan |
| Latest stable compatible versions; due diligence; license approval; no npm force flags; resilience and versioning package choices | skills/add-dependency |
| Decision recording and propagation; API version deprecation | skills/architecture-decision |
| CI reproduces commands and keeps failures visible; frontend CI scripts and lockfile; production migrations | skills/delivery-pipeline |

## Dependency Direction

Conformance dependencies follow `WF → KNW → STD → DEC → OP`, with `ENF → STD / DEC` and `IN` able to request a DEC change without overriding OP/DEC. A standard cites DEC IDs instead of restating decision text; knowledge cites standards; workflows cite standards and knowledge as check-by-reference items and read the standards they rely on. Routing pointers — `Technique:` and `Workflow:` lines in standards, the routing table in `CLAUDE.md`, `Details in` and `Affects` in the register — may point in any direction. Skill-private `references/` are read only by their own skill.

## Changing a Technology

There is no replacement mechanism: a technology appears in several Kinds, each with its own responsibility (for NUnit: DEC-TEST-01 selects it, the testing standard holds framework rules, `dotnet-testing` holds technique, `project-structure`/`verify` hold commands, `check-manifests` holds gate rules). Replacing it is a Reserved decision: run `architecture-decision`, which updates the register row and every `Affects` target listed above.
