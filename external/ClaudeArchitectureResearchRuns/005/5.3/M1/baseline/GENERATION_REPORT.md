# Generation Report

## Result

| Item | Value |
|---|---|
| Final acceptance result | **PASS** |
| Trigger-role delta count | 0 (196 policies: 194 inventory + 2 shared invariants) |
| Minimum-scope failures | 0 |
| Unresolved broken references | 0 |
| Known Windows-hook compatibility defects | 0 |
| Experimental isolation violations (directly observed) | 0 |
| Recoverable workspace-process incidents | none observed |
| Platform-managed persistence events | 1 (see Workspace Events) |
| Confirmation-audit result | 0 concrete template defects |

## Implemented Model

Minimal Modular, V2-lineage instruction system with exactly four static
capability slots:

| Slot | Type | Selected | Facets |
|---|---|---|---|
| architecture | frame, required | clean-architecture | planning `docs/capabilities/architecture.md`, rule `rules/architecture.md`, placement `project-structure/references/backend-layout.md`, architecture-check spec |
| persistence | leaf, required | ef-core (provider `sqlserver`) | planning, rule `rules/persistence-technology.md`, workflow `persistence-change`, knowledge `ef-core`, namespace and co-change data |
| backend-testing | leaf, required | nunit | planning, rule `rules/test-framework.md`, knowledge `dotnet-testing`, adapter data |
| frontend | leaf, optional | angular | planning, rule `rules/frontend-framework.md` (with bindings), knowledge `angular`, package data |

Loading: always = `CLAUDE.md` + six direct imports (technology stack,
selection record, four planning facets); path = 14 flat rules; workflow = 12
workflow skills (`template-maintenance` user-only) + `code-reviewer` agent;
on demand = 17 knowledge skills; hook = 3 Node hooks; maintainer = 4
`CONTRACT.md` + 4 `MODULE.md` (JSON manifests). Always-loaded surface ≈ 5.6k
tokens including skill listings.

## Runtime File Count and Tree

80 files.

```text
template/
├── CLAUDE.md  SPECIFICATION.md (empty)  CUSTOM_SETTINGS.md
├── .editorconfig  Directory.Build.props  Directory.Packages.props
├── docs/
│   ├── technology-stack.md  capability-selection.md
│   └── capabilities/ architecture.md persistence.md backend-testing.md frontend.md
└── .claude/
    ├── MAP.md  settings.json
    ├── agents/code-reviewer.md
    ├── capabilities/<slot>/CONTRACT.md + <implementation>/MODULE.md (x4)
    ├── hooks/ pre-tool-use.js post-tool-use.js stop.js
    ├── scripts/ check-instructions.js check-manifests.js check-architecture.js
    │   └── lib/ common.js dependency-commands.js hook-output.js
    ├── rules/ api architecture coding-style composition dependencies error-handling
    │          frontend frontend-framework performance persistence-technology
    │          physical-structure security test-framework testing (.md)
    └── skills/
        ├── workflows: add-dependency architecture-decision build-fix code-review
        │   custom-settings development-workflow git-workflow persistence-change
        │   project-structure (+references/solution-layout.md, backend-layout.md)
        │   security-scan (+references/scan-layers.md) template-maintenance verify
        └── knowledge: angular api-versioning aspnet-error-handling authentication
            caching ci-cd configuration dependency-injection docker dotnet-testing
            ef-core health-check http-api httpclient-factory (+references/resilience.md)
            logging (+references/serilog.md) modern-csharp swagger
```

## Structural Choices

- V2 rules kept and fixed in place; V2's `architecture.md` became the frame
  rule facet (EF Core boundary moved to `persistence-technology.md`; decision
  gate and simplicity moved to `CLAUDE.md`).
- New rules only where path-class policy had no rule owner in V2: `api.md`,
  `composition.md`, `frontend.md`, `physical-structure.md`; capability rule
  facets use role-based names.
- Module planning facets live in `docs/capabilities/<slot>.md` and are imported
  directly from `CLAUDE.md` (no nested imports, so import-path resolution is not
  relied upon).
- `development-workflow` added: TASK 7.3 forbids the V2 Development Workflow in
  `CLAUDE.md`, and WF-001/WF-002/GOV-002 are workflow-class.
- `add-dependency` absorbs V2's dependency procedure; `serilog` and
  `resilience` became private references of `logging` and `httpclient-factory`;
  V2 `testing` and `error-handling` skills became `dotnet-testing` and
  `aspnet-error-handling`.
- Leaf modules bind to frame roles; `ef-core` declares `binds` to the frame for
  examples, migration command, and co-change patterns.
- Hooks are launched with `node -e "require(...process.env.CLAUDE_PROJECT_DIR...)"`
  and return Claude Code hook JSON with exit 0; failures exit 1 visibly.

## Permitted Wording/Placement Deltas

- Implementation names were removed from embedded content: rules and workflows
  refer to "persistence technology", "persistence session", "the frontend
  framework rule/knowledge skill"; the persistence rule defines which EF Core
  types these are (ARC-002, ARC-008, ARC-011, ARC-014, ARC-017, TST-006, SEC-004,
  SEC-011, FE-003 keep their semantics through this binding).
- FE-010 is owned by `frontend.md`; its "Reactive Forms" part is expressed via
  the explicit-form-model binding in `frontend-framework.md`.
- DEP-013 placement and DEP-024 are expressed once (frame planning facet);
  DEP-013 points to it.
- ARC-020 is merged into the Reserved list of the decision-control section.
- WF-017–WF-019 are owned by `verify` § Delivery Changes; API-022 and GOV-007
  by `architecture-decision`; RUN-012 and TST-009 by `development-workflow`.
- Inventory-forced overlaps with different trigger classes are kept with
  distinct emphasis: DEP-012/API-017, DEP-013/TST-001/TST-007, DEP-010/API-010/
  RUN-013/DEP-021, DEP-014/FE-001, DEP-015/FE-006, ARC-020/ARC-004/ARC-009,
  WF-019/PST-004.
- Knowledge-skill "Anti-Patterns" became check-by-reference "Review Checks".

## Policy-Preservation Concerns and Ambiguity

- No unresolved policy contradictions; no BLOCKED condition.
- The shell Claude Code uses for hook commands on Windows is not established;
  the launcher and JSON results were verified under Git Bash, PowerShell, and
  cmd.exe.
- The agent preloads `code-review` via `skills:` and also reads it explicitly
  as a fallback.
- Always-loaded size (≈ 5.6k tokens) is slightly above the ≈ 5k target; no
  frozen trigger role was moved to reduce it.

## Audit Summary

Primary audit: owner/trigger/scope map for all 196 policies; manual
semantic-fidelity review of each owner text; V2 preservation (652 headings: 471
automatic, 181 manually classified as renamed/merged; 300 code blocks: 285
automatic, 15 manually confirmed as converted); duplicate sweep; structure,
dependency, hygiene, and budget checks; 22 checker tests; 42 hook tests across
three shells, including a ceiling-capped git sandbox.

Primary-audit repairs that changed the template:

1. WF-007 lacked an explicit risk-scoping statement (`verify`).
2. A skill-private reference (`backend-layout.md`) was depended on by a rule,
   a planning facet, and a knowledge skill (3 broken dependency directions).
3. Restatements converted to pointers in `backend-layout.md`, `logging`,
   `scan-layers.md`, `solution-layout.md`, `project-structure`, `ef-core`,
   `aspnet-error-handling`; V2 persistence layout tree restored in `ef-core`.
4. Checker treated all `docs/**` as instruction files and leak-scanned root
   project configuration.
5. Hook decisions used exit code 2, which a PowerShell `-Command` host turns
   into 1; replaced by hook JSON.
6. Clearing the optional frontend slot left dangling references; the checker
   now treats a disabled slot's contract facet locations as inactive.
7. The map lacked scope/enforcement/extension fields for several artifact
   kinds.

Broken references found/fixed: 3 private-reference dependencies and 1 map
reference fixed; checker false positives (section-reference parsing) fixed in
the checker; final unresolved count 0.

Confirmation audit: all gates rerun on the repaired files with the same
tooling; 0 concrete template defects.

## Workspace Events

- Isolation: only workspace inputs were read; no parent, sibling, network, or
  external material was used.
- Recoverable incidents: none observed; all audit material stayed in
  `output/.work/` and was removed.
- Platform-managed persistence: one oversized tool result was automatically
  saved by the platform to its session tool-results storage outside the
  workspace; it was not opened, and nothing depends on it. The desktop app also
  listed the generated template skills as available skills; none were invoked.
