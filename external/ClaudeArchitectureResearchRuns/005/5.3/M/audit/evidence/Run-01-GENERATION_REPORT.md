# Generation Report — Candidate M (Minimal Modular)

## Final Acceptance

| Metric | Result |
|---|---|
| Final acceptance result | **NOT PASS** — every content, structure, trigger, and enforcement check passes, but this run recorded workspace-boundary violations, and TASK requires 0 for PASS. BLOCKED does not apply (no missing source, no contradiction). A strict PASS needs a clean re-run. |
| Trigger-role delta count | **0** (196/196 mapped: 32 always, 123 path, 41 workflow) |
| Unresolved broken-reference count | **0** |
| Known workspace-boundary violations | **2** (see Workspace Boundary) |
| Known Windows-hook compatibility defects | **0** |
| Always-loaded surface estimate | ~4.9k tokens (CLAUDE.md + imported stack + skill listing) |

## Implemented Candidate Model

M = V2 + the frozen V2 policy oracle + the shared construction constraints +
defect-driven refactoring. V2's mental model is kept: an always-loaded
`CLAUDE.md`, flat topical path rules, workflow skills, knowledge skills, one
reviewer agent. Two-part planning-time decision model: architecture defaults,
approval gate, and not-adopted patterns in `CLAUDE.md` (the designated
decision summary); approved and conditional technologies in
`docs/technology-stack.md`, `@`-imported by `CLAUDE.md`. Accepted project
decisions are recorded as ADRs in `docs/decisions/` (created on first use by
`architecture-decision`). There is no decision register, no Level/Kind
classification, and no capability slots. The scope taxonomy shows up only in
headers, `paths`, and the map.

## Runtime File Count and Tree

62 files under `output/template/` (48 instruction files, 8 hook/script files,
`settings.json`, 3 build/format files, 2 product inputs).

```text
template/
├── CLAUDE.md
├── SPECIFICATION.md                 (intentionally empty)
├── CUSTOM_SETTINGS.md
├── .editorconfig
├── Directory.Build.props
├── Directory.Packages.props
├── docs/technology-stack.md
└── .claude/
    ├── MAP.md
    ├── settings.json
    ├── agents/code-reviewer.md
    ├── hooks/{pre-tool,post-tool,stop,commands}.mjs
    ├── scripts/{check-instructions,check-manifests,check-architecture}.mjs, scripts/lib/repo.mjs
    ├── rules/{architecture,persistence,api,error-handling,performance,coding-style,
    │          testing,security,dependencies,angular,repository-layout}.md
    └── skills/
        ├── workflow: development-workflow, project-structure (+references/backend-layout.md,
        │   solution-layout.md), verify, code-review, build-fix, custom-settings, git-workflow,
        │   security-scan (+references/scan-layers.md), add-dependency, architecture-decision,
        │   template-maintenance (user-only)
        └── knowledge: ef-core, http-api, aspnet-error-handling, dotnet-testing,
            logging (+references/serilog.md), httpclient-factory (+references/resilience.md),
            configuration, dependency-injection, caching, swagger, api-versioning,
            health-check, docker, ci-cd, angular, modern-csharp, authentication
```

## V2 Lineage

| Change | Artifacts |
|---|---|
| Keep (restatements removed) | `CLAUDE.md`, `CUSTOM_SETTINGS.md`, `SPECIFICATION.md`, rules `architecture`, `coding-style`, `performance`, `security`, `testing`, `dependencies`, `error-handling`; skills `verify`, `code-review`, `build-fix`, `custom-settings`, `git-workflow`, `security-scan` (+ reference), `project-structure` (+ 2 references), all knowledge skills; agent `code-reviewer` |
| Split | `CLAUDE.md` Development Workflow → `development-workflow` (V2 put a multi-step procedure in CLAUDE.md); `rules/dependencies.md` procedure → `add-dependency`; `architecture.md` repository/UoW/EF boundary + `ef-core` seeding rules → `rules/persistence.md` |
| Move (more reliable trigger) | path-class rules that V2 kept only in model-invoked skills → path rules (HTTP, versioning, Swagger, health → new `rules/api.md`; Angular → new `rules/angular.md`; DI/options → `architecture.md`; caching → `performance.md`; logging, Serilog, outbound resilience → `error-handling.md`; auth, CSRF, token storage, fail-safe → `security.md`; physical-structure rule → new `rules/repository-layout.md`); `project-structure/references/technology-stack.md` → `docs/technology-stack.md` (binding candidate rule); `testing.md` probe rule and `coding-style.md` usings rule → `verify` (workflow class) |
| Merge | `serilog` → `logging/references/serilog.md`; `resilience` → `httpclient-factory/references/resilience.md` |
| Rename (shared names) | `error-handling` skill → `aspnet-error-handling`; `testing` skill → `dotnet-testing` |
| New | `architecture-decision`, `template-maintenance` (shared workflows), `MAP.md`, `settings.json`, hooks, scripts, `.editorconfig`, `Directory.*.props` (shared enforcement requirement) |

## Policy Owners (authoritative)

| Owner | Trigger | Policies |
|---|---|---|
| `CLAUDE.md` | always | GOV-001, 003–006, 008–018, ARC-009, ARC-020 |
| `docs/technology-stack.md` | always | DEP-002, 008–016, 018, 022–024 |
| `rules/architecture.md` | path | ARC-001–008, 010–012, 021–026, 028, 029, RUN-022 |
| `rules/persistence.md` | path | ARC-013–019, PST-001–007, DEP-026 |
| `rules/api.md` | path | API-001, 003–006, 013–020 |
| `rules/error-handling.md` | path | API-002, 007–012, 021, RUN-013, 015–019, DEP-021 |
| `rules/performance.md` | path | RUN-001–008, 020, 021, 023 |
| `rules/coding-style.md` | path | RUN-009, 011, 024 |
| `rules/testing.md` | path | TST-001–008, 011, 012 |
| `rules/security.md` | path | SEC-001–018, RUN-014, DEP-019 |
| `rules/dependencies.md` | path | DEP-001, 006, 007 |
| `rules/angular.md` | path | FE-001–012 |
| `rules/repository-layout.md` | path | ARC-027 |
| `development-workflow` | workflow | GOV-002, 007, PST-008, 010, API-022, TST-009, RUN-012, WF-001–003, 017–019 |
| `verify` | workflow | TST-010, RUN-010, WF-004–009 |
| `add-dependency` | workflow | DEP-003–005, 017, 020, 025 |
| `build-fix` | workflow | WF-013–016 |
| `git-workflow` | workflow | GOV-019, 020, WF-022 |
| `custom-settings` | workflow | GOV-021, PST-009 |
| `code-review` | workflow | WF-011, 012 |
| `security-scan` | workflow | WF-020, 021 |
| `agents/code-reviewer.md` | workflow | WF-010 |

The shared invariants GOV-017 (decision control) and GOV-018 (challenge
obligation) are owned by `CLAUDE.md` (always).

## Structural Choices Where M Allowed Freedom

- **11 flat rules.** The illustrative nine plus `api.md` and `repository-layout.md`. `api.md` gives a
  path trigger to HTTP-contract rules that V2 kept only in skills.
  `repository-layout.md` exists because ARC-027 has `common` scope and must not
  widen the backend-only `architecture.md`. V2-like broad globs are kept.
  `angular.md` uses `frontend/**`.
- **`development-workflow`.** This is the workflow owner of V2's Development
  Workflow section. It also owns workflow-class obligations that V2 placed in
  rules or knowledge skills: seed co-change, migration review, regression tests,
  the performance-change procedure, API deprecation, CI/CD, and production
  migrations. `CLAUDE.md` keeps only a routing table.
- **Explicit rule reads.** Path-rule loading is not assumed to have happened.
  `development-workflow`, `project-structure`, `code-review`, and `verify` read
  the rule files for the affected areas explicitly; the area-to-rule list lives
  once, in `CLAUDE.md` (Workflows).
- **Headers.** Every instruction file carries one line with `Owns · Scope · Loads · Depends on
  [· Enforced by]`, placed after any frontmatter. `check-instructions.mjs` builds
  the dependency graph from these headers and verifies it is acyclic and that
  always-loaded or path-scoped policy depends only on reliably loaded files.
- **Enforcement.** Node.js ES modules use only built-in modules. Hooks:
  - **PreToolUse:** blocks npm peer-dependency bypass flags and asks before
    destructive Git commands.
  - **PostToolUse:** manifest check with dependency routing, product-input
    reminder, and instruction-structure check.
  - **Stop:** shows co-change reminders once. It honors `stop_hook_active` and
    deduplicates per session through the OS temp directory.
  - **Scripts:** `check-manifests` (Central Package Management, versions,
    deprecated and review-required packages, reference direction, npm hygiene),
    `check-architecture` (source-level boundary heuristics), and
    `check-instructions`.
- **ADR directory.** `docs/decisions/` is not pre-created, so the template has
  no empty tree. The ADR template lives in `architecture-decision`.

## Policy-Preservation Notes and Permitted Deltas

- **Inventory-inherent overlaps** are split so that each clause has one owner,
  and the other location points to it:
  - DEP-012/API-017: the stack names Swagger UI as the Development surface;
    `api.md` owns the exposure rule.
  - DEP-013 vs. TST-001/006/007: the stack owns the choices; `testing.md` owns
    their use.
  - DEP-010 vs. RUN-013/DEP-021, DEP-014/FE-001, DEP-015/FE-006, DEP-006/DEP-023,
    ARC-004/ARC-020, ARC-008/API-001, SEC-003/API-010.
  - ARC-020 and GOV-017 share one Decision Control section; the Reserved list
    merges V2's consequential-decision examples with the shared Reserved
    categories.
- **Vocabulary.** DEFAULT policies are labeled `Default:` and REQUIRES_APPROVAL
  policies say `requires approval`; this was checked mechanically.
  MUST policies whose normalized text used "normally" or "should" are written as
  must-level, matching their inventory strength (API-012, API-014, API-019,
  TST-003, DEP-006). "normally" was removed throughout.
- **Plain imperatives.** `CLAUDE.md` adds one line stating that plain
  imperatives carry must force. This is a vocabulary clarification, not a new
  policy.
- **Planning-time pointers.** DEP-017 (Asp.Versioning) and DEP-020 (resilience
  packages) are workflow-class. The stack therefore lists API versioning and
  resilience as conditional, with a pointer to `add-dependency`, and does not
  restate the package rules.
- **Deny-list mirror.** The deprecated and review-required package list in
  `check-manifests.mjs` mirrors the stack and `add-dependency`. Hook messages
  name the owner; they do not restate the policy.
- **Product inputs.** `SPECIFICATION.md` stays at 0 bytes, so the "authoritative
  when non-empty" semantics hold. `CUSTOM_SETTINGS.md` keeps a one-line
  product-input header and the table; its V2 policy restatements moved to
  `CLAUDE.md`.

## Unresolved Ambiguity

- **Hook commands** are project-relative (`node .claude/hooks/<file>.mjs`), as
  required (no `$CLAUDE_PROJECT_DIR`). If a host ever starts hooks outside the
  project directory, Node fails with a visible module-not-found error rather
  than skipping silently. The scripts themselves resolve the root from their own
  location and print "checks were NOT run" on failure.
- **Hook mechanics used:** exit code 2, `permissionDecision: "ask"`, Stop
  `decision: "block"`, and `stop_hook_active`.
- **Reviewer preload.** The `code-reviewer` agent preloads `code-review`
  through the `skills:` frontmatter, and its body also tells it to read the
  skill. The workflow therefore does not depend on the preload field.

## Broken References and Defects Found and Fixed

- **Checker defects:** the instruction checker flagged generic tokens as
  references, and its MAP-coverage pattern was malformed and matched
  everything. Both were fixed and are now covered by mutation tests.
- **Truncated skills:** a construction script truncated all 28 `SKILL.md`
  bodies while shortening descriptions. All were rebuilt and re-audited, and a
  backup step was added before later bulk edits.
- **Wording fixes:** one typo in `docker`; about 25 knowledge-skill or reference
  lines that restated a rule were converted to pointers; 4
  normative-strength wordings were corrected.
- **Final state:** 0 unresolved references.

## Workspace Boundary

Known violations of TASK Section 5 ("no temporary files outside the run
workspace"):

1. **Scratchpad dump.** Early in the run, before the `output/.work/` rule was
   applied, the generator wrote a 67 KB inventory dump to the agent's session
   scratchpad (outside the workspace). It was deleted within minutes and
   regenerated under `output/.work/`. The violation occurred; deleting the
   file does not undo it.
2. **Persisted command output.** One command printed more than about 31 KB (two
   V2 skill files). The agent host then persisted that output to its own session
   store (`.claude/projects/<session>/tool-results/`), outside the workspace.
   The generator did not write this file deliberately. It is host-managed
   session state, so it was neither modified nor deleted.

Apart from these, all construction material, test sandboxes, Git fixtures, and
hook temp state (redirected via `TMP`/`TEMP`/`TMPDIR`) stayed under
`output/.work/`, which has been removed. No parent or sibling directory,
network, or external repository was used. The template does not depend on
anything outside `output/template/`.

## Final Self-Check (TASK Section 10)

| # | Check | Result |
|---|---|---|
| 1 | `output/template/` is standalone | PASS (no references to sources, task files, or the workspace) |
| 2 | V2 policy semantics preserved | PASS (196/196 anchored in their owners) |
| 3 | Shared construction requirements and invariants | PASS |
| 4 | Binding `CANDIDATE.md` rules | PASS (flat rules, two-part decisions, lineage, no Level/Kind/slots) |
| 5 | One owner per policy, no accidental duplication | PASS (anchor-duplication audit 0; manual review) |
| 6 | Internal imports and references resolve | PASS (`check-instructions.mjs`) |
| 7 | Zero trigger-role deltas | PASS (0) |
| 8 | Minimum scope coverage | PASS (scope samples matched against rule `paths`) |
| 9 | Critical must-rules not only on-demand | PASS (knowledge skills and references own no policy) |
| 10 | Procedures owned by workflows, not `CLAUDE.md` | PASS |
| 11 | Product inputs remain inputs | PASS |
| 12 | Workflows, knowledge, enforcement, map present | PASS |
| 13 | Windows-compatible hooks | PASS (shell-neutral commands; 75/75 enforcement tests on Windows) |
| 14 | No files outside `output/`; no parent/sibling dependency | **FAIL**: 2 workspace-boundary violations (see Workspace Boundary). No parent/sibling dependency. |
| 15 | No application or benchmark generated | PASS |
| 16 | No research metadata in runtime | PASS (leak scan 0) |
| 17 | No dependency outside `output/template/` | PASS |
| 18 | Understandable, no gratuitous layers | PASS |
| 19 | Compact always-loaded surface, frozen triggers kept | PASS (~4.9k tokens) |
| 20 | English-only technical output | PASS (Cyrillic scan 0) |
