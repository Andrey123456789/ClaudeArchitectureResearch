> Maintainer map of the instruction system · Human-facing · Not auto-loaded

# Instruction Map

Every table lists, per artifact: **File**, **Owner** (the policy or procedure
it is authoritative for; every rule has exactly one owner and other files point
to it), **Scope**, **Loading**, **Enforcement**, and **Add here** (where related
new content belongs).

Loading values: `always` (CLAUDE.md and its imports), `path` (rule loads when a
matching file is read), `workflow` (skill invoked through routing or an
explicit read), `on demand` (knowledge skill selected by its description),
`explicit read` (private reference read by its owning skill), `user`
(user-invoked only), `hook` (runs automatically), `maintainer` (read only
during capability maintenance).

Files owned by one of the four capability implementations are listed in the
capability view at the end; everything else is embedded. Change procedure:
`skills/template-maintenance/SKILL.md`. Structural self-check (from any
directory of the repository or worktree):
`node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.js"`.

## Always-Loaded Surface

| File | Owner | Scope | Loading | Enforcement | Add here |
|---|---|---|---|---|---|
| `CLAUDE.md` | product-source authority, custom-settings boundary, core defaults, challenge duty, decision control, Git boundary, workflow routing | common, repo/meta | always | instruction checker | only governance that must be known while planning |
| `docs/technology-stack.md` | approved stack and conditional technologies outside the slots | common | always (import) | manifest check (deny-list) | new approved or conditional non-slot technology |
| `docs/capability-selection.md` | slot → selected implementation, status, declared properties | common | always (import) | instruction checker | only selection changes (ADR required) |

The four `docs/capabilities/<slot>.md` planning facets are also always loaded;
see the capability view.

## Path Rules (`.claude/rules/`, flat)

| File | Owner | Scope / paths | Loading | Enforcement | Add here |
|---|---|---|---|---|---|
| `rules/frontend.md` | framework-independent frontend structure, HTTP boundary, errors, state, routing, validation authority | frontend (`frontend/**/*`) | path | — | framework-independent frontend rules |
| `rules/testing.md` | framework-independent test policy | backend-tests (`backend/**/*Tests/**`) | path | stop hook (test co-change) | framework-independent test rules |
| `rules/coding-style.md` | C# conventions, file/namespace and async naming, style scope discipline | backend (`*.cs`) | path | `.editorconfig` | C# style conventions |
| `rules/composition.md` | dependency injection, typed configuration, logging provider | backend (`*.cs`, `appsettings*.json`) | path | — | DI, configuration, logging rules |
| `rules/error-handling.md` | expected outcomes, exceptions, exception logging, error contracts, cancellation responses, validation boundaries | backend (`*.cs`) | path | — | error-handling rules |
| `rules/api.md` | HTTP status semantics, API versioning, Swagger accuracy/exposure, health checks | backend (`*.cs`, `launchSettings.json`) | path | — | HTTP API rules |
| `rules/performance.md` | async/cancellation, time, outbound calls, database efficiency, caching semantics, measured optimizations | backend (`*.cs`) | path | — | runtime/performance rules |
| `rules/security.md` | secrets, trust boundaries, SQL safety, authN/authZ, transport, data protection, CORS, sensitive logging, fail-safe behavior, uploads, containers | common (backend, frontend, config, Docker) | path | pre-tool hook (peer overrides) | security rules |
| `rules/dependencies.md` | dependency need, Central Package Management, npm manifests | common (manifests) | path | manifest check, pre-tool hook | manifest policy |
| `rules/physical-structure.md` | proportional physical structure | common (`backend/**`, `frontend/**`, `docs/**`, solution files) | path | — | structure-proportionality rules |

Capability-owned rule facets (`architecture.md`, `persistence-technology.md`,
`test-framework.md`, `frontend-framework.md`) are in the capability view.

## Workflow Skills (`.claude/skills/`)

| File | Owner (procedure) | Scope | Loading | Enforcement | Add here |
|---|---|---|---|---|---|
| `skills/development-workflow/SKILL.md` | implementation procedure: product sources, inspection and owner reads, bug-fix regression, performance changes, review before verify | common | workflow | — | implementation steps |
| `skills/verify/SKILL.md` | completion gates, probe preservation, using cleanup, delivery-pipeline checks, reporting | common | workflow | runs the checkers | verification steps |
| `skills/code-review/SKILL.md` | review procedure, priorities, finding discipline, output | common | workflow (agent preload) | — | review steps |
| `skills/build-fix/SKILL.md` | build/test repair loop, no weakened verification, source-first regeneration | common | workflow | — | repair steps |
| `skills/custom-settings/SKILL.md` | `CUSTOM_SETTINGS.md` synchronization | common | workflow | post-edit and stop reminders | settings sync steps |
| `skills/git-workflow/SKILL.md` | Git operation safety, focused commits | repo/meta | workflow | — | Git steps |
| `skills/security-scan/SKILL.md` | security review procedure, severity, report | common | workflow | — | audit steps |
| `skills/security-scan/references/scan-layers.md` | private investigation prompts | common | explicit read | — | scan prompts |
| `skills/add-dependency/SKILL.md` | dependency due diligence, version and license decisions, package choice | common | workflow | pre-tool hook, manifest check | dependency steps |
| `skills/architecture-decision/SKILL.md` | Decision Requests, decision recording, capability-selection changes, API deprecation | common | workflow | — | decision steps |
| `skills/project-structure/SKILL.md` | scaffolding, restructuring, and project-reference change procedure | common | workflow | pre-tool hook (project references), architecture check | scaffolding steps |
| `skills/project-structure/references/solution-layout.md` | private repository-layout technique | repo/meta | explicit read | — | repository layout technique |
| `skills/template-maintenance/SKILL.md` | instruction-system changes, capability replacement | repo/meta | user | instruction checker | maintenance steps |

The capability-owned workflow facet `persistence-change` and the frame's
placement reference (`skills/project-structure/references/backend-layout.md`)
are in the capability view.

## Knowledge Skills (technique only; never sole policy owners)

| File | Owner (technique) | Scope | Loading | Enforcement | Add here |
|---|---|---|---|---|---|
| `skills/http-api/SKILL.md` | status-code reference (policy: `rules/api.md`) | backend | on demand | — | HTTP response technique |
| `skills/aspnet-error-handling/SKILL.md` | exception handler, ProblemDetails, validation technique (policy: `rules/error-handling.md`) | backend | on demand | — | error-handling examples |
| `skills/logging/SKILL.md` | ILogger technique (policy: `rules/composition.md`, `rules/security.md`) | backend | on demand | — | logging technique |
| `skills/logging/references/serilog.md` | private Serilog depth | backend | explicit read | — | Serilog setup detail |
| `skills/httpclient-factory/SKILL.md` | outbound HTTP technique (policy: `rules/performance.md`, `rules/architecture.md`) | backend | on demand | — | HTTP client technique |
| `skills/httpclient-factory/references/resilience.md` | private resilience depth | backend | explicit read | — | resilience pipeline detail |
| `skills/configuration/SKILL.md` | Options pattern and secrets technique (policy: `rules/composition.md`, `rules/security.md`) | backend | on demand | — | configuration examples |
| `skills/dependency-injection/SKILL.md` | DI technique (policy: `rules/composition.md`) | backend | on demand | — | registration patterns |
| `skills/caching/SKILL.md` | cache technique (policy: `rules/performance.md`) | backend | on demand | — | caching examples |
| `skills/swagger/SKILL.md` | Swagger technique (policy: `rules/api.md`) | backend | on demand | — | OpenAPI/Swagger setup |
| `skills/api-versioning/SKILL.md` | versioning technique (policy: `rules/api.md`) | backend | on demand | — | versioning examples |
| `skills/health-check/SKILL.md` | health-check technique (policy: `rules/api.md`) | backend | on demand | — | probe examples |
| `skills/docker/SKILL.md` | container technique (policy: `rules/security.md`, `skills/verify/SKILL.md`) | delivery | on demand | — | container examples |
| `skills/ci-cd/SKILL.md` | pipeline technique (obligations: `skills/verify/SKILL.md`) | delivery | on demand | — | pipeline examples |
| `skills/modern-csharp/SKILL.md` | optional language technique (conventions: `rules/coding-style.md`) | backend | on demand | — | language-feature guidance |
| `skills/authentication/SKILL.md` | authN/authZ technique (policy: `rules/security.md`) | backend | on demand | — | auth examples |

Capability-owned knowledge skills (`ef-core`, `dotnet-testing`, `angular`) are
in the capability view.

## Agent

| File | Owner | Scope | Loading | Enforcement | Add here |
|---|---|---|---|---|---|
| `agents/code-reviewer.md` | independent read-only review; preloads `code-review` | common | delegated by `code-review` or the user | `disallowedTools` (read-only) | nothing: review criteria belong in `code-review` |

## Product Inputs (not instruction layers)

| File | Role | Scope | Loading | Enforcement | Add here |
|---|---|---|---|---|---|
| `SPECIFICATION.md` | product behavior input; empty in the template by design | product | read by workflows | post-edit and stop reminders | approved product behavior |
| `CUSTOM_SETTINGS.md` | approved tunable values input | product | read by workflows | post-edit and stop reminders | approved tunable values |

## Deterministic Enforcement

Hooks and scripts require Node.js on `PATH`; if it is missing, the hook command
fails visibly instead of silently skipping enforcement. Hooks are launched from
the checkout where the session started (`${CLAUDE_PROJECT_DIR}`, the launcher
root) but check the repository or worktree that the hook input `cwd` belongs to
(the active root), so work in a Git worktree or a nested directory is checked
against its own files. Manual checker runs resolve the active root the same way
from their working directory.

| File | Owner (mechanism) | Scope | Loading | Add here |
|---|---|---|---|---|
| `settings.json` | wires the hooks in exec form (`node` + script path through `${CLAUDE_PROJECT_DIR}`, no shell); the critical pre-tool hook fails closed (`onFailure: "block"`); failed shell commands are post-checked too (`PostToolUseFailure`) | repo/meta | hook | new hook wiring |
| `hooks/pre-tool-use.js` | denies dependency commands until `add-dependency` was applied and project-reference commands until `project-structure` was applied; stops peer-dependency override flags; asks the user to confirm repository-changing Git commands (read-only Git runs); fails closed | common | hook | pre-command routing |
| `hooks/post-tool-use.js` | after edits and successful or failed commands: manifest and architecture checks, layer-namespace check, product-source reminders, instruction check; a shell command is judged by its effect on manifests and project files (content state per worktree in its Git directory), so unrecognized commands, branch switches, removals, and moves are checked | common | hook | post-change checks |
| `hooks/stop.js` | co-change reminders (persistence model vs. seed/migrations, code vs. tests, product sources, manifests); loop-safe; re-arms when the content of the involved files changes; state per worktree | common | hook | co-change reminders |
| `scripts/check-instructions.js` | structural checker for this instruction system (headers, flat rules, skills, references, capability slots, leaks, binds, map, budget) | repo/meta | run by hooks, `verify`, maintainers | new structural predicates |
| `scripts/check-manifests.js` | Central Package Management, floating/prerelease versions, deny-list, test-framework mixing, npm categories | common | run by hooks, `verify` | new manifest checks |
| `scripts/check-architecture.js` | project-reference direction, test-reference breadth, inner-layer namespaces (frame specification) | backend | run by hooks, `verify` | new boundary checks |
| `scripts/lib/common.js` | shared helpers (launcher and active root resolution, path containment, globbing, manifests) | repo/meta | library | shared helpers |
| `scripts/lib/dependency-commands.js` | Bash/PowerShell command parsing and classification of package and project-reference changes, shared by the pre- and post-tool hooks | common | library | package-manager options and command forms |
| `scripts/lib/hook-output.js` | hook results as Claude Code hook JSON with exit 0; pre-tool failures deny, other hook failures exit 1 visibly | repo/meta | library | hook result format |
| `.editorconfig` | formatting and code-style configuration | backend, frontend | tooling | formatting rules |
| `Directory.Build.props` | shared .NET build settings | backend | tooling | shared build properties |
| `Directory.Packages.props` | Central Package Management | backend | tooling | package versions (via `add-dependency`) |

## Capability View

Composition is static: one implementation per required slot, zero or one for
the optional frontend slot (`docs/capability-selection.md`). Contracts and
manifests are maintainer metadata. Outside a module's own facets, instructions
refer to slots and facet roles, never to the selected implementation's name;
the instruction checker enforces this with each manifest's leak tokens. Add
implementation-specific content only to the module's facets listed below.

### architecture — required frame — selected: clean-architecture

| Facet | Physical location | Scope | Loading | Enforcement |
|---|---|---|---|---|
| planning (role map, layout, patterns not adopted) | `docs/capabilities/architecture.md` | backend, common | always | architecture check |
| rules (layers, repositories, Unit of Work, placement, test references) | `rules/architecture.md` | backend (`*.cs`, `*.csproj`) | path | architecture check, post-edit layer check |
| placement | `skills/project-structure/references/backend-layout.md` | backend | explicit read by `project-structure` | — |
| architecture-check specification | manifest `enforcement.architecture` | backend | `scripts/check-architecture.js` | — |
| contract / manifest | `capabilities/architecture/CONTRACT.md`, `capabilities/architecture/clean-architecture/MODULE.md` | — | maintainer | instruction checker |

Binds: none. Properties: adopted style, role map, patterns not adopted,
repository layout. Embedded rules use the frame's layer names as project
vocabulary.

### persistence — required leaf — selected: ef-core (provider variant: sqlserver)

| Facet | Physical location | Scope | Loading | Enforcement |
|---|---|---|---|---|
| planning | `docs/capabilities/persistence.md` | backend | always | — |
| rules (technology boundary, transactions, seeding, local database) | `rules/persistence-technology.md` | backend (`*.cs`, `*.csproj`, `appsettings*.json`) | path | architecture check (namespaces), stop hook (co-change) |
| workflow (mappings, migrations, seed co-change, schema-affecting settings) | `skills/persistence-change/SKILL.md` | backend | workflow | stop hook |
| knowledge | `skills/ef-core/SKILL.md` | backend | on demand | — |
| enforcement data | manifest `enforcement` (technology namespaces, co-change patterns) | backend | architecture check, stop hook | — |
| contract / manifest | `capabilities/persistence/CONTRACT.md`, `capabilities/persistence/ef-core/MODULE.md` | — | maintainer | instruction checker |

Binds: architecture frame — only executable guidance (registration example,
`Persistence/` placement, migration command, co-change patterns); prose uses
role vocabulary. Declared observable property: string comparison follows the
database collation (`docs/capability-selection.md`). Provider-variant sections
are listed in the manifest.

### backend-testing — required leaf — selected: nunit

| Facet | Physical location | Scope | Loading | Enforcement |
|---|---|---|---|---|
| planning | `docs/capabilities/backend-testing.md` | backend-tests | always | — |
| rules | `rules/test-framework.md` | backend-tests | path | manifest check (second framework) |
| knowledge (incl. test project setup) | `skills/dotnet-testing/SKILL.md` | backend-tests | on demand | — |
| adapter data | manifest `enforcement` (framework and competing packages) | backend-tests | manifest check, architecture check | — |
| contract / manifest | `capabilities/backend-testing/CONTRACT.md`, `capabilities/backend-testing/nunit/MODULE.md` | — | maintainer | instruction checker |

Binds: none (test-project placement comes from the frame by pointer).

### frontend — optional leaf — selected: angular

| Facet | Physical location | Scope | Loading | Enforcement |
|---|---|---|---|---|
| planning | `docs/capabilities/frontend.md` | frontend | always | manifest check (not-by-default packages) |
| rules and bindings | `rules/frontend-framework.md` | frontend | path | — |
| knowledge (incl. scaffolding, security-review notes) | `skills/angular/SKILL.md` | frontend | on demand | — |
| enforcement data | manifest `enforcement` (not-by-default and dev-only packages) | frontend | manifest check | — |
| contract / manifest | `capabilities/frontend/CONTRACT.md`, `capabilities/frontend/angular/MODULE.md` | — | maintainer | instruction checker |

Binds: none. Removal: `skills/template-maintenance/SKILL.md` § Removing the
Optional Frontend Slot.
