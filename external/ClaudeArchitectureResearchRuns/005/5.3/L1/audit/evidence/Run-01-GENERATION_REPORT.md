# Generation Report — Candidate L1 (Stability-first + Replaceable Capabilities)

## Final acceptance result: **PASS**

| Gate | Result |
|---|---|
| Trigger-role delta count | **0** (196/196 policies mapped: 32 always, 123 path, 41 workflow) |
| Unresolved broken-reference count | **0** |
| Known Windows-hook compatibility defects | **0** (cmd, Windows PowerShell 5.1, Git Bash tested) |
| Directly observed experimental isolation violations | **0** |
| Confirmation-audit concrete template defects (final run) | **0** |

## Implemented model

- **Levels (stability-first):** `.claude/rules/{0-core,1-architecture,2-technology,3-project}/`; every artifact declares `Level:` in a one-line header; Core/Architecture use only the fixed platform vocabulary (.NET, C#, `dotnet` CLI, NuGet/MSBuild, ASP.NET Core primitives, `TimeProvider`, HTTP/TLS/OIDC/OpenAPI, Git).
- **Capabilities (exactly four slots):** `architecture` (frame → `clean-architecture`), `persistence` (leaf → `ef-core`, variant `sqlserver`), `backend-testing` (leaf → `nunit`), `frontend` (optional leaf → `angular`). Each slot has a maintainer `CONTRACT.md`; each selected implementation a `MODULE.md` (facets, declared properties, `binds:`, `leak terms:`). Static composition: one implementation directory per slot; module-owned artifacts declare `Capability: <slot>/<impl>`.
- **Role vocabulary** (`1-architecture/roles.md`, always loaded) is the stable interface; the frame maps roles to Domain/Application/Infrastructure/Api and owns placement (`layering.md`, `layout.md`, `check.json`); leaves bind to roles and the named location `persistence implementation`.
- **Facet roles:** workflows reference `<slot>.<facet>` (e.g. `backend-testing.commands`, `persistence.workflow`), never implementation names; the selection record defines resolution.
- **Decisions stratified:** frame decision (L1, always), project stack (L3, always), capability selection record (L3, always; designated decision summary for selections/declared properties), module decision facets (L3, always). No cross-level register; selection changes are Reserved + ADR.
- **Always-loaded surface:** `CLAUDE.md` + 10 imports (operating policy, product governance, decision control, roles, stack, capability selection, 4 selected decision facets) and 28 model-visible skill descriptions. Measured ≈ 19.1k chars / 2.5k words of files + 4.8k chars of descriptions ≈ **4.0k–6.0k tokens** (words×1.3 vs chars/4). No planning-time policy was moved out to reduce it.

## Runtime file count and tree

96 files under `output/template/` (27 rules, 29 skills + 4 skill-private references, 1 agent, 4 contracts, 4 manifests, 11 module facets, 3 hooks, 5 scripts/data, settings, map, 3 root build/format assets, `CLAUDE.md`, 2 product inputs).

```text
template/
├── .claude/
│   ├── agents/code-reviewer.md
│   ├── capabilities/
│   │   ├── architecture/        CONTRACT.md; clean-architecture/{MODULE.md, layout.md, check.json}
│   │   ├── backend-testing/     CONTRACT.md; nunit/{MODULE.md, commands.md, scaffold.md, check.json}
│   │   ├── frontend/            CONTRACT.md; angular/{MODULE.md, commands.md, scaffold.md, check.json}
│   │   └── persistence/         CONTRACT.md; ef-core/{MODULE.md, workflow.md, scaffold.md, co-change.json}
│   ├── hooks/{dependency-guard.cjs, post-edit-check.cjs, stop-co-change.cjs}
│   ├── rules/
│   │   ├── 0-core/{operating-policy, product-governance, decision-control, minimalism, security, coding,
│   │   │           performance, error-handling, http-api, outbound-calls, hosting, testing}.md
│   │   ├── 1-architecture/{roles, role-boundaries, frontend-structure, adopted-architecture, layering}.md
│   │   ├── 2-technology/{backend-technologies, data-access, test-framework, frontend-framework}.md
│   │   └── 3-project/{stack, capability-selection, package-management, persistence-stack,
│   │                  backend-testing-stack, frontend-stack}.md
│   ├── scripts/{check-instructions.cjs, check-architecture.cjs, check-packages.cjs, package-policy.json, lib/project.cjs}
│   ├── skills/
│   │   ├── workflows: develop, verify, code-review, build-fix, add-dependency, custom-settings,
│   │   │              project-structure (+references/solution-layout.md), delivery, architecture-decision,
│   │   │              git-workflow, security-scan (+references/scan-layers.md), template-maintenance (user-only)
│   │   └── knowledge: http-api, aspnet-error-handling, logging (+references/serilog.md),
│   │                  httpclient-factory (+references/resilience.md), configuration, dependency-injection,
│   │                  caching, swagger, api-versioning, health-check, docker, ci-cd, modern-csharp,
│   │                  authentication, ef-core*, dotnet-testing*, angular*   (* module-owned)
│   ├── INSTRUCTION-MAP.md
│   └── settings.json
├── .editorconfig
├── CLAUDE.md
├── CUSTOM_SETTINGS.md
├── Directory.Build.props
├── Directory.Packages.props
└── SPECIFICATION.md   (empty by design)
```

## Structural choices where the candidate allowed freedom

1. Always-loaded rules live in level directories, declare `paths` matching their scope, and are imported directly by `CLAUDE.md` (root-relative imports only; nested-import path resolution is not relied on). The `CLAUDE.md` decision-import list is kept identical to the selection record by the checker.
2. Role-expressible architecture invariants are neutral L1 (`role-boundaries.md`); only Clean-Architecture-specific mapping, dependency graph, orchestration mechanism, and patterns-not-adopted are frame facets.
3. Procedural/data facets (`layout`, `workflow`, `commands`, `scaffold`, `check`, `co-change`) live in the module directory; rule/knowledge facets live in normal rule/skill locations. Scaffold facets and `add-dependency` are Level 3 because they encode project layout/package conventions.
4. Two workflows beyond the shared set: `develop` (owns the Development Workflow obligations that must not sit in `CLAUDE.md`) and `delivery` (owns CI/deployment workflow obligations); both are routed from `CLAUDE.md`.
5. Embedded (non-slot) backend technologies share one L2 rule (`backend-technologies.md`) with per-technology sections.
6. Leaves declare `binds: architecture` only for code examples that use frame names; prose binds to roles.
7. Enforcement is data-driven by the selected modules (frame check spec, test-framework adapter, persistence co-change rules, frontend dependency commands, module leak terms), so replacing a module needs no script edits. Hooks use a `node -e` bootstrap without shell metacharacters or `$VAR` expansion and emit Claude Code JSON decisions with exit 0 (shell-independent).

## Intentionally permitted wording/placement deltas

- Architecture policies naming V2 layers or EF types (e.g. Application must not use `DbContext`; EF Core is an Infrastructure detail) are expressed in role vocabulary ("use-case units", "persistence-technology types", "persistence implementation"); the EF type list is the persistence module's binding. Semantics unchanged under the selected modules.
- Core/Architecture text omits concrete library names required by the leak/platform rules: "MediatR, Kommand" → "mediator libraries or mediator-based dispatch"; "multiple DbContexts" → "multiple persistence contexts"; "do not assume an Angular frontend removes CSRF risk" → "the frontend framework"; "Testcontainers is optional" (TST-007) → "an isolated container-hosted instance is optional" (Testcontainers is named in the backend-testing decision).
- MUST policies whose normalized text says "normally" are written with explicit conditions instead of "normally" (normative-vocabulary requirement), without changing strength.
- Overlapping inventory pairs (DEP-012/API-017, DEP-013/DEP-024, GOV-013/DEP-001, ARC-009/ARC-020) each keep one owner; the always-loaded side points to the path-scoped side where the clause is owned there.

## Policy-preservation concerns

None open. Semantic-fidelity review covered all 196 owners; seven strength/condition drifts found in the primary audit were repaired (see below).

## Unresolved ambiguity

- Claude Code's support for the agent `skills:` frontmatter field is not established; the reviewer agent also reads `code-review/SKILL.md` explicitly, so delegation does not depend on it.
- Always-loaded rules also match their own `paths`; possible re-injection on file reads is a token cost only.

## Broken references found / fixed

Found during audits: rule/facet references that would break when the optional frontend slot is cleared (map rows and concrete facet paths in contracts) — fixed by referring to module facets by role and listing them only in the map's capability view. Unresolved broken references: **0** (checker + references scan).

## Audit evidence (primary audit)

- **A. Owner/trigger/scope:** scripted mapping of all 194 inventory policies + 2 shared invariants to one owner each, trigger role derived from loading (import / path rule / workflow artifact), scope verified against `paths`; anchors present; exact-anchor duplicates swept.
- **B. Semantic fidelity:** side-by-side review of every normalized policy vs owner text, including strength and conditions.
- **C. V2 preservation:** section-level key-term coverage over all 41 V2 files (0.917); all 27 low sections manually reviewed (renamed owner files, `<Name>` placeholders, leak-avoidance rewording); lost technique restored.
- **D. Restatement:** cross-file 7-gram sweep and policy-text 4-gram sweep; remaining overlaps are routing pointers, check-by-reference items, the designated decision summary, or structural table text.
- **E. Structure/dependencies:** L1 structure checker (levels, headers, `paths`, imports, slots/modules/facets/levels, selection record, leak and platform-vocabulary rules); manual classification of every reference toward less stable levels (routing/check-by-reference only).
- **F. References:** checker resolution of paths, file names, facet roles, routing targets.
- **G. Deterministic tooling:** 74 sandbox tests (positive/negative checker cases, architecture/package checks, dependency guard, post-edit and stop hooks incl. no-loop, frontend-slot clearing, settings hook commands through cmd, PowerShell and Git Bash with and without `CLAUDE_PROJECT_DIR`); Git discovery capped with `GIT_CEILING_DIRECTORIES`.
- **H. Hygiene/budget:** no research metadata, policy IDs, model IDs, or non-English script in the template; budget measured above.

### Primary-audit repairs that materially changed the template

1. Strength/condition fixes: API-019 readiness condition, RUN-013, RUN-020, PST-007, TST-003; SEC-012 missing "never log tokens" clause.
2. Removed ~15 cross-file restatements (migration-editing clause, dependency cleanup, approval clause, spec authority in review, transport contracts, CPM, test placement, lockfile, token validation, Docker optionality, etc.).
3. Restored V2 technique (options-monitor usage, Serilog enrichers/diagnostic context/OTLP/conditional/Elastic examples and decision guide, HTTP-named category examples).
4. Moved scaffold facets and `add-dependency` to Level 3 (dependency direction).
5. Windows hooks: replaced exit-code-2 signalling (collapsed to 1 by Windows PowerShell `-Command`) with JSON decisions on exit 0; replaced `||` in the bootstrap with `??`; checker now rejects shell metacharacters in hook commands.
6. Optional-slot clearing: map lists module facets only in the capability view; contracts describe facet locations by role; module knowledge skills enforced via contract facets.
7. Checker: module level consistency; data-driven leak terms from `MODULE.md`; research-specific patterns removed from the runtime checker; ASCII-only language check.
8. Skill descriptions shortened (budget) without moving policy.

### Confirmation audit

Re-ran all gates (structure checker, mapping/trigger/scope, fidelity of changed policies, V2 coverage, restatement sweeps, dependency direction, 74 tooling tests, research/language scan). Intermediate confirmation runs found and fixed: two residual procedure restatements (generated-client steps; NUnit package requirement), research strings and hardcoded implementation names in the runtime checker, and a manifest rule repeated across four contracts. **Final confirmation run: 0 concrete template defects.**

## Workspace events (directly observed)

- Experimental isolation violations: **0** (only the run workspace was read; no network, parent/sibling, or research material access).
- Recoverable workspace-process incident: early sandbox Git test runs let Git consult the user's global Git configuration (standard Git behavior; no information used). Remediated: tests set `GIT_CONFIG_GLOBAL` to an empty in-workspace file and `GIT_CEILING_DIRECTORIES` to `output/.work`.
- Platform-managed persistence event: one oversized tool output was automatically saved by the tool runtime to a tool-results location outside the workspace; it was not opened, and the check was re-run with output written to `output/.work/`.
- Construction material lived only in `output/.work/` and was removed; `output/` contains only `template/` and this report.
