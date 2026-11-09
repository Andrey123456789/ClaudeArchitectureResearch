# Generation Report — Candidate M (Minimal Modular)

## Result

| Item | Value |
| --- | --- |
| Final acceptance result | **PASS** |
| Trigger-role delta count | 0 (196/196 policies: 194 inventory + 2 shared invariants) |
| Minimum-scope gaps | 0 |
| Unresolved broken references | 0 |
| Known Windows-hook compatibility defects | 0 |
| Experimental isolation violations (directly observed) | 0 |
| Recoverable workspace-process incidents | 0 |
| Platform-managed persistence events surfaced | none surfaced during normal execution |
| Confirmation audit | 12/12 gates pass, **0 concrete template defects** |
| Runtime file count | 60 files in `output/template/` (48 Markdown instruction files, 1 settings file, 4 hook scripts, 2 checker scripts, 3 build/format configs, 2 product inputs) |
| Always-loaded estimate | ~4.8k tokens (`CLAUDE.md` + imported `docs/technology-stack.md` + skill/agent descriptions) |

## Implemented Model

M = V2 lineage + the frozen V2 policy oracle + shared construction constraints +
defect-driven refactoring. No stability levels, no `Kind:`/`Level:` taxonomy, no
capability contracts, no single decision register.

- **Always loaded:** `CLAUDE.md` (product-source governance, core defaults,
  challenge obligation, architecture defaults incl. layout and patterns not
  adopted, Decided/Delegated/Reserved decision control, Git boundaries, workflow
  routing) + `@docs/technology-stack.md` (approved stack, conditional
  technologies, solution/build defaults). ADR history: `docs/decisions/`
  (created with the first record).
- **Path-loaded:** flat `.claude/rules/` — `architecture`, `persistence`, `api`,
  `error-handling`, `performance`, `coding-style`, `security`, `testing`,
  `dependencies`, `angular`, `repository-structure`; every rule declares `paths`.
- **Workflows:** `development-workflow`, `verify`, `code-review`, `build-fix`,
  `custom-settings`, `git-workflow`, `security-scan`, `add-dependency`,
  `architecture-decision`, `project-structure`, `template-maintenance`
  (user-only, `disable-model-invocation: true`). Thin read-only `code-reviewer`
  agent runs `code-review`.
- **Knowledge (technique only, on demand):** the 17 shared names; Serilog depth
  is `logging/references/serilog.md`, resilience depth is
  `httpclient-factory/references/resilience.md`.
- **Enforcement:** `.editorconfig`, `Directory.Build.props`,
  `Directory.Packages.props`, `.claude/settings.json` hooks (Node, shell-neutral),
  `check-manifests.mjs`, `check-instructions.mjs`.
- **Human map:** `.claude/MAP.md` (not loaded): per-file owner, scope, loading,
  enforcement, extension guidance; topic → owner index.
- Every instruction file starts with `> Owns: … | Scope: … | Loads: …`.

## Final Tree

```text
template/
├── .claude/
│   ├── agents/code-reviewer.md
│   ├── hooks/ dependency-guard.mjs, file-change.mjs, hook-io.mjs, stop-co-change.mjs
│   ├── rules/ angular.md, api.md, architecture.md, coding-style.md, dependencies.md,
│   │          error-handling.md, performance.md, persistence.md,
│   │          repository-structure.md, security.md, testing.md
│   ├── scripts/ check-instructions.mjs, check-manifests.mjs
│   ├── skills/
│   │   ├── add-dependency/  architecture-decision/  build-fix/  code-review/
│   │   ├── custom-settings/  development-workflow/  git-workflow/  verify/
│   │   ├── project-structure/ (references/backend-layout.md, solution-layout.md)
│   │   ├── security-scan/ (references/scan-layers.md)
│   │   ├── template-maintenance/
│   │   ├── angular/  api-versioning/  aspnet-error-handling/  authentication/
│   │   ├── caching/  ci-cd/  configuration/  dependency-injection/  docker/
│   │   ├── dotnet-testing/  ef-core/  health-check/  http-api/  modern-csharp/  swagger/
│   │   ├── httpclient-factory/ (references/resilience.md)
│   │   └── logging/ (references/serilog.md)
│   ├── MAP.md
│   └── settings.json
├── docs/technology-stack.md
├── .editorconfig
├── CLAUDE.md
├── CUSTOM_SETTINGS.md
├── Directory.Build.props
├── Directory.Packages.props
└── SPECIFICATION.md   (empty by design)
```

## V2 Lineage

| Change | Artifacts |
| --- | --- |
| Keep (restatements removed) | `rules/architecture`, `coding-style`, `dependencies`, `error-handling`, `performance`, `security`, `testing`; `skills/verify`, `code-review`, `build-fix`, `custom-settings`, `git-workflow`, `security-scan` (+ `scan-layers`), `project-structure` (+ `backend-layout`, `solution-layout`); knowledge skills `ef-core`, `http-api`, `angular`, `api-versioning`, `authentication`, `caching`, `ci-cd`, `configuration`, `dependency-injection`, `docker`, `health-check`, `httpclient-factory`, `logging`, `modern-csharp`, `swagger`; `CLAUDE.md`, `SPECIFICATION.md` |
| Fix in place | `CUSTOM_SETTINGS.md` reduced to the data table + pointer (product input no longer restates policy); `code-reviewer` reduced to a thin wrapper |
| Rename (shared naming) | `testing` → `dotnet-testing`; `error-handling` skill → `aspnet-error-handling` |
| Merge | `serilog` → `logging/references/serilog.md`; `resilience` → `httpclient-factory/references/resilience.md`; agent review criteria → `code-review` |
| Move | `project-structure/references/technology-stack.md` → `docs/technology-stack.md` (imported; was a skill-private file used by a rule); CLAUDE.md "Development Workflow" procedure → `development-workflow`; always-class items from rules/skills → `CLAUDE.md`/stack; path-class items from knowledge skills → rules; workflow-class items from rules/skills → workflows |
| Split | `rules/persistence.md` (seeding policy from `ef-core`), `rules/api.md` (normative core of `http-api`, `api-versioning`, `swagger`, `health-check`), `rules/angular.md` (normative core of `angular`), `skills/add-dependency` (procedure from `rules/dependencies.md`), `rules/repository-structure.md` (structure restraint from `project-structure`) |
| New (shared requirement) | `skills/architecture-decision`, `skills/template-maintenance`, `.claude/MAP.md`, `.claude/settings.json`, hooks, checkers, `.editorconfig`, `Directory.Build.props`, `Directory.Packages.props` |

## Structural Choices (where M allowed freedom)

- `development-workflow` is the single workflow owner for workflow-class
  implementation obligations (spec read, code inspection, durable source sync,
  seeder co-change, migration review, regression tests, performance-change
  procedure, generated output, API deprecation, CI/CD and production
  migrations, review/verify gates). CLAUDE.md only routes to it.
- Placement of path policies whose V2 owner was a knowledge skill: DI, typed
  options, Serilog registration, boundary contracts → `architecture.md`;
  outbound timeouts/retries/fallback/caller cancellation → `error-handling.md`;
  cache semantics → `performance.md`; structured logging calls →
  `coding-style.md`; payload logging, auth details, container runtime image →
  `security.md`; local Development connection string → `persistence.md`.
- `repository-structure.md` exists because ARC-027 is `common` scope; widening
  `architecture.md` to frontend/docs would load backend policy everywhere.
- `security.md` keeps V2's broad globs plus `.github/**`, `**/.*.yml`,
  `**/.*.yaml`, scripts (common scope must reach CI/delivery files).
- Hooks are backstops, not owners: PreToolUse blocks npm force flags; PostToolUse
  routes dependency commands/manifest edits to `add-dependency` and runs manifest
  checks; settings/spec edits get sync reminders; Stop gives seeder/migration/test
  reminders once per change set (`stop_hook_active` and a fingerprint prevent loops).
- `code-reviewer` declares `skills: [code-review]` but its body also delegates,
  so it does not depend on the preload field.

## Policy-Preservation Notes

- Inventory-level overlaps kept as separate owners at their frozen trigger roles,
  worded to their context: DEP-012↔API-017 (Swagger exposure), DEP-013↔TST-001/
  TST-006/TST-007, DEP-011↔DEP-020, PST-004↔WF-019, ARC-009↔ARC-020,
  GOV-013↔DEP-001, GOV-004/GOV-010↔Reserved item 10, DEP-002↔Reserved item 6,
  DEP-013↔DEP-024.
- GOV-005 is expressed through the Delegated class definition in Decision Control.
- Workflow-class MUST policies live in workflow skills that `CLAUDE.md` routes
  to and that hooks remind; no must-policy is owned by a knowledge skill or a
  private reference.

## Intentional Wording/Placement Deltas

- Trigger-role-driven moves (all to match frozen `trigger_class`): GOV-002,
  GOV-007, WF-001..003 (CLAUDE.md → workflow); DEP-003..005, DEP-025, RUN-010,
  RUN-012, TST-010 (rules → workflows); PST-008/010, TST-009, WF-016..019,
  API-022, DEP-017, DEP-020 (knowledge skills → workflows); ARC-009, ARC-020,
  DEP-002, DEP-008..016, DEP-018, DEP-022..024 (rules/skills/references →
  always-loaded); ARC-021..029, PST-001..007, API-001..006/013..020,
  TST-005..008/011, SEC-011..018, RUN-013..023, DEP-019/021/026, FE-001..012
  (knowledge skills/references → path rules).
- "normally" rendered as "by default" per the normative vocabulary.
- Small V2 clarifications kept next to their owners (e.g., 204 has no body,
  in-app HTTPS redirection not required behind a TLS boundary).

## Unresolved Ambiguity

- Rule-glob dot-file semantics are not guaranteed; dot-directory paths are
  listed explicitly instead of relying on `**`.
- The always-loaded pair `CLAUDE.md` ↔ `docs/technology-stack.md` cross-reference
  (Decided sources / Reserved pointer); they load as one unit, and all other
  conformance edges point rule → always-loaded or workflow → rule (rule →
  workflow references are routing pointers only).
- No genuine contradiction among the inputs; no BLOCKED condition.

## Broken References

- V2 defects fixed: a rule depended on a skill-private reference
  (`technology-stack.md`); routing to `testing`, `error-handling`, `serilog`,
  `resilience` updated to the shared names/merged references.
- Generation-time checker findings (wrapped `§` references) were checker
  limitations, fixed in `check-instructions.mjs`. Final: 0 unresolved
  (file, `§` section, skill/agent, import, and private-reference checks).

## Audits

**Primary substantive audit** covered: owner + trigger + minimum-scope mapping
(scripted, all 196); side-by-side semantic-fidelity review of every owner block
against its normalized policy; V2 preservation (2,831 baseline sentences
scripted — 80% literal/paraphrase matched; all 556 remainders reviewed
manually); pairwise and policy-centric restatement sweeps; M structure and
dependency direction; reference resolution; hook/checker tests (47 cases, exact
`settings.json` commands launched via cmd.exe, PowerShell, and Git Bash; Git
tests capped with `GIT_CEILING_DIRECTORIES`); metadata/language/budget checks.

Primary-audit repairs that materially changed the template:

1. `security.md` paths: added `.github/**`, `**/.*.yml`, `**/.*.yaml`.
2. Fidelity: GOV-005 qualifier broadened to match V2; GOV-007 extra timing
   condition removed; GOV-008 made explicitly normative; ARC-027 examples made
   conditional; API-014/API-019/DEP-019/DEP-021 regained the "by default" qualifier.
3. V2 restorations: test-level "do not require" pair, "test code simpler than
   production", Angular Material for existing projects, endpoint-securing options,
   mapping-library concerns out of Domain.
4. Restatements converted to pointers in `angular`, `backend-layout`,
   `solution-layout`, `project-structure`, `api-versioning`, `dotnet-testing`;
   `http-api`/`aspnet-error-handling` decision tables attributed to rule owners.
5. Explicit owner reads added to `add-dependency`, `build-fix`, `custom-settings`.
6. `hook-io.mjs` strips a UTF-8 BOM (Windows PowerShell piping);
   `check-instructions.mjs` reports nested/non-Markdown entries instead of crashing.
7. `MAP.md` states loading/enforcement for knowledge skills.

**Confirmation audit:** reran every gate with the same tooling and rechecked all
repaired items. Its first passes found three residual fidelity defects (GOV-007
"approved during the work" condition, PST-001 missing "by default", RUN-010
obligation phrased as a checklist fragment); these were fixed and the complete
confirmation audit rerun: 12/12 gates, 0 concrete template defects.

## Workspace Events

- All construction and audit material stayed under `output/.work/` and was
  removed; the session scratchpad outside the workspace was not used.
- System executables (`node`, `git`, `cmd.exe`, PowerShell, Git Bash) were
  invoked as tools; no files outside the workspace were read or written, no
  network access, no sibling-run or research material accessed.
- Platform session storage was not inspected (evidence ceiling).
