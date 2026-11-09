# Generation Report

## Result

| Item | Value |
|---|---|
| Final acceptance result | **PASS** |
| Trigger-role delta count | 0 (196 of 196 policies — 194 inventory + 2 shared invariants — mapped to one owner each) |
| Unresolved broken-reference count | 0 |
| Known Windows-hook compatibility defects | 0 |
| Directly observed experimental isolation violations | 0 |
| Confirmation-audit result | 0 concrete template defects |

## Implemented Candidate Model

Minimal Modular plus four static, replaceable capability slots:

- **architecture** (required frame) → `clean-architecture`;
- **persistence** (required leaf) → `ef-core`, provider variant `sqlserver`;
- **backend-testing** (required leaf) → `nunit`;
- **frontend** (optional leaf, enabled) → `angular`.

Outside the slots the system keeps the V2 mental model: `CLAUDE.md` plus
imported planning records, flat path-scoped topical rules, workflow skills,
knowledge skills with private references, a thin reviewer agent, and
deterministic enforcement. Each slot has a maintainer-only `CONTRACT.md`, a
`MODULE.md` manifest (human table plus a JSON block read by the checkers),
runtime facets carrying `Capability: <slot>/<implementation>` in their header,
and an entry in the always-loaded selection record `docs/capability-selection.md`.
Leaves bind to the frame only through the contract's stable roles (no `binds:`
coupling was needed).

## Runtime File Count and Final Tree

77 files (65 Markdown, 7 Node.js scripts, 3 JSON, 2 MSBuild props, plus
`.editorconfig` and `.claude/.gitignore`).

```text
template/
├── CLAUDE.md  SPECIFICATION.md (empty)  CUSTOM_SETTINGS.md
├── .editorconfig  Directory.Build.props  Directory.Packages.props
├── docs/
│   ├── technology-stack.md        capability-selection.md
│   ├── architecture.md            (frame planning facet)
│   └── frontend-stack.md          (frontend planning facet)
└── .claude/
    ├── MAP.md  settings.json  .gitignore
    ├── agents/code-reviewer.md
    ├── capabilities/{architecture,persistence,backend-testing,frontend}/CONTRACT.md
    │   └── clean-architecture | ef-core | nunit | angular /MODULE.md
    ├── hooks/post-tool-use.mjs  stop.mjs
    ├── scripts/check-instructions.mjs  check-architecture.mjs  check-dependencies.mjs
    │           dependency-policy.json  lib/template.mjs
    ├── rules/  api  architecture-style*  backend-runtime  coding-style  dependencies
    │           error-handling  frontend  frontend-framework*  performance
    │           persistence-technology*  repository-structure  security  test-framework*  testing
    └── skills/ workflows: development-workflow verify code-review build-fix custom-settings
                git-workflow security-scan (+scan-layers) project-structure (+solution-layout,
                backend-layout*) add-dependency architecture-decision template-maintenance
                knowledge: ef-core* http-api aspnet-error-handling dotnet-testing (+test-framework*)
                logging (+serilog) httpclient-factory (+resilience) configuration
                dependency-injection caching swagger api-versioning health-check docker ci-cd
                angular* modern-csharp authentication
```

`*` = capability facet.

## Structural Choices Where the Candidate Allowed Freedom

- **Always-loaded surface:** `CLAUDE.md` imports `docs/technology-stack.md` and
  `docs/capability-selection.md`; the selection record imports the always-loaded
  facets of the selected implementations (`docs/architecture.md`,
  `docs/frontend-stack.md`). Clearing a selection is therefore a one-file change
  for the import. The selection record also carries a facet-role table so
  workflows can name facets by role ("the frontend rule facet").
- **Frame facets:** patterns not adopted and the role mapping are an always-loaded
  frame record (`docs/architecture.md`); layer rules are the path rule
  `architecture-style.md`; layout technique is the `project-structure` private
  reference `backend-layout.md`; the architecture-check specification is the JSON
  block of the frame's `MODULE.md`.
- **Classification boundary:** the frame owns the layer model, placement,
  repositories/Unit of Work, registration, transport-contract and test-project
  placement. Topic rules that merely mention layers (HTTP, errors, caching,
  outbound HTTP, versioning, DI technique) stay in embedded rules and keep
  Domain/Application/Infrastructure names (no neutralization of non-slot content).
- **Leaves:** all persistence path policies (seeding included) live in the leaf
  facet `persistence-technology.md`, written with frame roles; the contract
  obliges any replacement to restate the seeding and migration semantics.
  Framework-neutral test policy stays in `testing.md`; NUnit owns
  `test-framework.md` (default framework plus vocabulary binding) and the
  `dotnet-testing` private reference with NUnit syntax and commands.
  Framework-neutral frontend policy stays in `frontend.md`; Angular owns
  `frontend-framework.md`, `docs/frontend-stack.md`, and the `angular` skill.
- **New embedded artifacts (shared-requirement driven):** `development-workflow`
  (the V2 Development Workflow moved out of `CLAUDE.md`, plus workflow-trigger
  co-change obligations that V2 kept in knowledge skills); `add-dependency`,
  `architecture-decision`, `template-maintenance` (shared workflow set); rules
  `api.md`, `backend-runtime.md`, `frontend.md`, `repository-structure.md` for
  path-trigger policies that V2 held only in knowledge skills; `.claude/MAP.md`.
- **Enforcement:** dependency-free Node.js scripts launched as
  `node .claude/hooks/<file>.mjs` (shell-neutral; the project root comes from
  `CLAUDE_PROJECT_DIR` or the hook input, resolved inside the script). The Stop
  hook blocks once per distinct change set and never when `stop_hook_active`.
  Hook state lives in `.claude/.cache/` (git-ignored).

## Policy-Preservation Notes and Permitted Wording/Placement Deltas

- Slot implementation names are replaced by facet roles outside the
  implementation's facets (enforced by the leak check), for example
  "persistence-technology types" in the frame rule instead of `DbContext`/`DbSet`
  (the leaf lists the concrete types), "persistence mapping/migration mechanism"
  in `custom-settings`, and "the frontend framework" in security text.
- DEP-009/DEP-013 name the selected technologies through the selection record
  (`ef-core`/`sqlserver`, `nunit`) instead of restating them in
  `docs/technology-stack.md`.
- Inventory pairs with overlapping semantics at different frozen trigger levels
  keep one owner each, with the lower-level owner referring to the planning
  record where the wording would otherwise repeat: DEP-012/API-017 (API-017 is
  phrased as the code-level mapping rule), ARC-020/ARC-009 (CLAUDE.md Reserved
  list per the shared decision contract; `docs/architecture.md` patterns not
  adopted), DEP-011/DEP-020, PST-004/TST-008, ARC-008/ARC-019/DEP-009.
- Vocabulary normalized to `must` / `Default:` / `prefer` per strength (for
  example SEC-006 "should" → "must"; DEFAULT policies phrased "prefer/normally"
  now start with "Default:").
- V2 defects fixed in place: unclosed code fence in the testing rule; path-class
  MUST policies held only in knowledge skills moved to rules; the V2
  `technology-stack.md` reference promoted to an always-loaded planning record.
- Always-loaded surface measured at ≈5.6k tokens (character estimate, including
  27 model-invocable skill descriptions); no frozen trigger role was changed to
  reduce it.

## Unresolved Ambiguity

None blocking. Interpretation recorded: workflow-trigger MUST policies are owned
by workflow skills that the always-loaded `CLAUDE.md` routes to; this is how they
avoid existing "only" in model-invoked material.

## Broken References

Found and fixed during construction and audit: bare script names and multi-line
section references not resolved by the checker (checker fixed), `testing` skill
name in `ci-cd`, section references in `verify`/`build-fix`, and dangling
optional-slot filename references (`frontend-framework.md` named in five embedded
files; replaced by role references and now rejected mechanically). Remaining: 0.

## Audit Summary

Primary audit (all required checks) on the generated files:

- owner/trigger/scope mapping of 196 policies: 0 trigger deltas, 0 scope gaps
  (rule globs tested against sample paths per scope), all workflow owners
  reachable from `CLAUDE.md`;
- semantic-fidelity review of every owner text against its normalized policy;
- V2 preservation over all 43 baseline files: 587/645 headings, 405/475 code
  blocks, 1098 exact + 332 fuzzy sentence matches; the remaining unmatched items
  were reviewed manually (moved, neutralized, or removed restatements);
- duplicate/restatement sweep, conformance-dependency graph (31 nodes, 40 edges,
  acyclic; no rule depends on product inputs), candidate structure and leakage
  checks, internal references, research-metadata/language hygiene (0 findings);
- 51 enforcement tests in an in-workspace sandbox (checker negative cases,
  optional-slot disable, architecture and dependency checks, both hooks, and the
  exact `settings.json` commands launched through cmd.exe, Windows PowerShell,
  and sh).

Primary-audit repairs that materially changed the template:

1. strength/vocabulary repairs in the owner text of 18 policies (SEC-006, SEC-009, SEC-014,
   API-007, API-012, API-014, API-019, ARC-013, ARC-016, ARC-017, TST-005,
   RUN-001, RUN-008, RUN-009, RUN-024, DEP-006, DEP-020, WF-016);
2. removal of restatements from knowledge skills and references (FE-005 in
   `angular`, API-015 in `api-versioning`, RUN-015 in `httpclient-factory`,
   DEP-013/DEP-023/test placement in `solution-layout`, E2E placement in
   `frontend-stack.md`) and API-017 rephrased to reference DEP-012;
3. optional frontend facets referenced by role only, plus a checker rule;
4. hooks tolerate the UTF-8 byte-order mark that Windows PowerShell 5.1 adds to
   piped input;
5. restored minor V2 technique losses (a `project-structure` instruction,
   BAD/GOOD examples in `configuration` and the Serilog reference, the
   not-adopted-pattern examples in `code-review`);
6. explicit owner read in `add-dependency`; documented frontend-disable steps
   (`template-maintenance`, frontend contract) including the map update.

Confirmation audit: every gate rerun after rebuilding from the construction
specs, with the repaired policies rechecked individually — 0 concrete template
defects.

## Workspace Events

- Experimental isolation violations: 0 (only the run directory was read; no
  network, no sibling or parent content).
- Recoverable workspace-process incidents: none observed. Construction and audit
  material stayed in `output/.work/`; Git tests used
  `GIT_CEILING_DIRECTORIES` and an in-workspace empty global Git config.
- Platform-managed persistence events: one directly observed — the tool runtime
  saved one oversized command output (a listing of V2 baseline files) to its
  session tool-results storage outside the workspace. That copy was not read;
  the files were re-read from the workspace instead.
