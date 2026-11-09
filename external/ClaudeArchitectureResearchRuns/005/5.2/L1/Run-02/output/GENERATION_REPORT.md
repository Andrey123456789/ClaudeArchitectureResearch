# Generation Report

## Result

| Item | Value |
| --- | --- |
| Final acceptance result | **PASS** |
| Trigger-role delta count | 0 (196 policies: 194 inventory + 2 shared invariants) |
| Minimum-scope failures | 0 |
| Unresolved broken references | 0 |
| Known Windows-hook compatibility defects | 0 |
| Experimental isolation violations (directly observed) | 0 |
| Confirmation-audit result | 0 concrete template defects (final complete pass) |

## Implemented candidate model

Stability-first level hierarchy (`0-core` → `1-architecture` → `2-technology` → `3-project`) with first-class replaceable capabilities for exactly four slots: `architecture` (required frame, `clean-architecture`), `persistence` (required, `ef-core`, provider variant `sqlserver`), `backend-testing` (required, `nunit`), `frontend` (optional, `angular`). Rules are level-first under `.claude/rules/<level>/`; module-owned facets live in role-named subdirectories (`frame/`, `persistence/`, `backend-testing/`, `frontend/`) or in the module directory `.claude/capabilities/<slot>/<impl>/` and declare `Level:` plus `Capability:`/`Facet:`. Each slot has a maintainer `CONTRACT.md`, one selected implementation with `MODULE.md`, runtime facets, a row in the always-loaded selection record (`.claude/rules/3-project/decisions.md`), and mechanical leak/conformance checks. Composition is static; only selected modules ship. Product inputs (`SPECIFICATION.md`, `CUSTOM_SETTINGS.md`) stay outside the hierarchy.

## Runtime file count and tree

85 files (69 Markdown instruction/product files, 6 JSON, 6 JavaScript modules, 4 repository configuration files).

```text
template/
├── CLAUDE.md                     L0 entry: product inputs, defaults, decision control, challenge, routing, Git
├── SPECIFICATION.md              product input (empty by design)
├── CUSTOM_SETTINGS.md            product input
├── .editorconfig  .gitignore  Directory.Build.props  Directory.Packages.props
└── .claude/
    ├── INSTRUCTION_MAP.md        human map (not auto-loaded): levels, capability view, enforcement, policy locator
    ├── settings.json             hooks as plain `node <script>` commands
    ├── agents/code-reviewer.md
    ├── capabilities/
    │   ├── architecture/{CONTRACT.md, clean-architecture/{MODULE.md, layout.md, check.json}}
    │   ├── persistence/{CONTRACT.md, ef-core/{MODULE.md, workflow.md, commands.md, enforcement.json}}
    │   ├── backend-testing/{CONTRACT.md, nunit/{MODULE.md, commands.md, enforcement.json}}
    │   └── frontend/{CONTRACT.md, angular/{MODULE.md, commands.md, enforcement.json}}
    ├── rules/
    │   ├── 0-core/{security, engineering, backend-code, http-api, testing, frontend}.md
    │   ├── 1-architecture/{roles.md, frame/{adopted-style.md (always), boundaries.md}}
    │   ├── 2-technology/{backend-libraries.md, persistence/{access,seeding}.md, backend-testing/test-framework.md, frontend/framework.md}
    │   └── 3-project/{decisions.md (always), frontend-stack.md (always), package-management.md, development-database.md}
    ├── skills/
    │   ├── workflows: development-workflow, verify, code-review, build-fix, custom-settings, git-workflow,
    │   │   security-scan (+references/scan-layers.md), add-dependency, architecture-decision,
    │   │   project-structure (+references/solution-layout.md, baseline-packages.md), template-maintenance (user-only)
    │   └── knowledge: ef-core, dotnet-testing, angular (module-owned); http-api, aspnet-error-handling,
    │       logging (+references/serilog.md), httpclient-factory (+references/resilience.md), configuration,
    │       dependency-injection, caching, swagger, api-versioning, health-check, docker, ci-cd, modern-csharp, authentication
    ├── hooks/{pre-bash-dependency.mjs, post-edit-checks.mjs, stop-cochange.mjs, manifest-policy.json}
    └── scripts/{check-instructions.mjs, check-architecture.mjs, lib/project.mjs}
```

## Structural choices (where the candidate allowed freedom)

- **Always-loaded surface**: `CLAUDE.md` owns Core operating policy directly and imports three decision files (frame style, project decisions with the selection record, frontend stack). Always-loaded rules still declare `paths`. Estimated size ≈ 3.1k tokens of instructions + ≈ 2.1k tokens of skill/agent listings (≈ 5.2k total).
- **Role vocabulary** (`roles.md`) is neutral Level 1 content; the frame maps roles to `Domain`/`Application`/`Infrastructure`/`Api`. Non-frame artifacts use roles (use-case layer, implementation layer, entry point, commit boundary).
- **Facet resolution by convention**: workflow-read facets resolve to `.claude/capabilities/<slot>/<selected>/<facet>.md|json`; each selection row names the slot's knowledge skill. Workflows reference only `<slot>.<facet>` roles, never implementation names.
- **Persistence workflow facet** (`persistence.workflow`) owns model/seed co-change, migration review, and schema-affecting setting changes; `ef-core` declares `binds:` to the frame for project names in commands.
- **`development-workflow`** was added as the procedure owner of implementation-phase obligations (specification read, inspection, review-before-verify, verify-before-done, regression tests, performance changes, API deprecation, CI/CD and production-migration obligations); `CLAUDE.md` only routes to it.
- **Workflow levels**: workflows are Level 0 except `add-dependency` and `project-structure` (Level 3, they carry project package/layout choices).
- **Enforcement data split by ownership**: the frame supplies `check.json` (role patterns, allowed references, inner-role package/framework bans, mediator approval list); leaves supply adapters (`persistence` package prefixes and co-change globs, `backend-testing` test-project markers, `frontend` npm approval list); project-level deny lists live in `hooks/manifest-policy.json`.
- **Dependency hook** denies the first dependency command with a pointer to `add-dependency` and allows the identical retry within 30 minutes (state in `.claude/.hook-state/`, git-ignored); npm force flags trigger an `ask`.

## Policy preservation

All 194 inventory policies and both shared invariants have exactly one owner with the inventory trigger role and at least the declared scope. Overlapping inventory policies (for example `DEP-012`/`API-017`, `SEC-010`/`SEC-012`, `PST-004`/`TST-008`) keep one owner each; the overlapping clause is held by one owner and referenced by pointer from the other, preferring the always-loaded owner when trigger roles differ. No policy concerns remain open.

## Intentional wording and placement deltas

- Implementation names replaced by roles or generic terms outside modules: `ARC-002`/`ARC-008`/`ARC-011`/`ARC-017` (EF Core/DbContext → persistence-implementation types, persistence context; the persistence module binds the EF Core types); `ARC-009` and the Reserved list (MediatR/Kommand → mediator libraries; package IDs remain in the frame's enforcement data); `SEC-011` (Angular frontend → frontend framework); `TST-006` (EF Core → the ORM); `TST-007` (Testcontainers → isolated real-provider container); `WF-018` (`npm ci` → lockfile-based clean install resolved through `frontend.commands`).
- `ARC-020` is owned by the Reserved list of `GOV-017` decision control in `CLAUDE.md` (all its examples preserved); a capability-selection change was added to the Reserved list as required by the candidate.
- "normally" removed from MUST policies per the vocabulary rule (`API-012`, `API-014`, `API-019`, `DEP-006` — the latter keeps the exception explicitly as a reported `VersionOverride`).
- `RUN-010` (unused usings) is owned by `verify` step 8; `TST-010` by `verify` step 4; `GOV-007`, `GOV-002`, `TST-009`, `RUN-012`, `API-022`, `WF-001`–`WF-003`, `WF-017`–`WF-019` by `development-workflow`.

## Unresolved ambiguity

None blocking. Two platform mechanics are used conservatively: hook commands are relative to the project root (a wrong working directory fails loudly with "Cannot find module"; scripts resolve the root from their own location), and the agent's `skills:` preload is backed by an explicit instruction to load `code-review`.

## Broken references found and fixed

- Checker first run: a Level 0 workflow named `npm` and `Docker`; a false-positive skill-reference pattern in the checker — fixed.
- Confirmation audit: the decisions file named module knowledge skills outside the selection rows, and two Core rules pointed at module directories; both left dangling references when the optional frontend was cleared. Fixed by adding a knowledge-skill column to the selection record and using `frontend.framework` / `backend-testing.framework` facet pointers. A frontend-removal test now passes the checker.
- Final: 0 unresolved references (imports, paths, facets, skills, private references, hook scripts, map coverage).

## Primary-audit repairs that materially changed the template

- Fidelity: restored the conditional wall-clock clause (`TST-004`), token-logging pointer (`SEC-012`), moved the Swagger exposure clause to the always-loaded owner (`DEP-012`, with `API-017` pointing to it), explicit `VersionOverride` exception (`DEP-006`, hook message aligned), stream-composition condition (`FE-011`).
- Duplicate/restatement sweep: knowledge and workflow passages restating rules converted to technique plus pointers (`ef-core` transactions/compiled queries/raw SQL, `dotnet-testing` fidelity, `health-check`, `scan-layers` error responses, `code-review` conformance, `project-structure`, `add-dependency`, duplicated `--no-restore` advice).
- V2 preservation: restored allocation techniques, the Serilog decision guide, the Central Package Management XML example, security severity factors, and test-naming examples.
- Structure: frame layer names removed from non-frame Docker/CI examples; ambiguous "should/normally" removed from normative rules; explicit owner reads added to `persistence.workflow`; product-input header added to `CUSTOM_SETTINGS.md`.

## Audit evidence (in-workspace, scratch removed)

Scripted owner/trigger/scope mapping for all 196 policies; per-policy semantic-fidelity review of owner text; section-level V2 coverage (41 files, 612 sections, manual review of sections below 0.85 term recall); 8-word shingle duplicate sweep plus manual semantic review; instruction checker; 54 hook/script/checker tests in an in-workspace sandbox (launch via cmd, PowerShell, and Git Bash; deny-once routing; manifest, architecture, and co-change checks; loop guard; fail-clearly paths; checker negative cases; frontend removal); research-metadata, language, and budget scan.

## Workspace events (directly observed)

- Recoverable workspace-process incident (1, remediated): an audit shell pipeline accidentally targeted an outside path (`/tmp/../dev/null`) as a redirect; it failed, nothing was written or read, and later commands used `output/.work/` only.
- Platform-managed persistence events: the tool runtime saved one oversized command output (the V2 project-structure files) to its own tool-results storage; that file was not opened — the sources were re-read from `source/`. Claude Desktop also auto-discovered the generated template skills and listed them in the session; they were not used. Neither creates an external dependency.
- No network, parent, sibling, or excluded research material was accessed. Git tests used `GIT_CEILING_DIRECTORIES` inside the sandbox.
