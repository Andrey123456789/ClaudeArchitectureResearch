# Generation Report — L0 (Stability-first, Embedded Capabilities)

## Implemented candidate model

- **Primary axis: stability.** Rules live in `.claude/rules/0-core/`, `1-architecture/`, `2-technology/`, `3-project/`. Every instruction artifact starts with a one-line header `> Level: <n> <Name> · Owns: … · Scope: … · Loads: …` (the map uses `Level: meta`).
- **Dependency direction.** Conformance references point only to the same or a more stable level. `CLAUDE.md` `@` imports are loading edges; skill-name pointers are routing. Both are enforced mechanically by `.claude/scripts/check-instructions.mjs`.
- **Technology neutrality.** Levels 0 and 1 name only .NET/C#/TypeScript platform vocabulary; concrete technologies appear at Levels 2–3. Mixed statements are split, for example L1 "no persistence-framework types in Application" ↔ L2 "`DbContext`, `DbSet<T>`… are persistence-framework types" ↔ L3 "EF Core + SQL Server selected". The map holds a split-statement table.
- **Stratified decisions.** Adopted and not-adopted architecture is in `1-architecture/overview.md`. Stack, conditional technologies and project defaults are in `3-project/decisions.md`. `CLAUDE.md` imports both; there is no merged register.
- **Embedded technologies.** There are no contracts, slots, manifests, `Kind:` taxonomy or Feature/Task levels. NUnit, EF Core, Angular and other technologies are named directly at Levels 2–3, in workflows and in assets.
- **Loading.** Level does not decide loading. The always-loaded surface is `CLAUDE.md` plus five imports: product governance, decision control, Git safety, the L1 overview and the L3 decisions. Everything else loads through `paths:`, through explicit "Read first" lists in workflows, on demand as skills, or through hooks.

## Runtime file count

72 files in `output/template/`:

- 59 instruction artifacts:
  - `CLAUDE.md`;
  - 24 rule modules (L0 9, L1 7, L2 5, L3 3);
  - 27 skills (10 workflows, 17 knowledge);
  - 5 skill-private references;
  - 1 agent;
  - 1 map.
- 11 enforcement assets: `settings.json`, 4 hook files, 3 scripts, `.editorconfig`, `Directory.Build.props`, `Directory.Packages.props`.
- 2 product-input placeholders: `SPECIFICATION.md` (empty by design), `CUSTOM_SETTINGS.md`.

## Final tree

```text
template/
├── .claude/
│   ├── agents/code-reviewer.md
│   ├── hooks/{lib,post-edit,pre-command,stop-co-change}.mjs
│   ├── rules/
│   │   ├── 0-core/{completion-contract,decision-control,dependency-hygiene,git-safety,logging-principles,
│   │   │          product-governance,runtime-principles,security-principles,testing-principles}.md
│   │   ├── 1-architecture/{backend-layers,code-organization,entry-points,frontend-structure,outcomes,
│   │   │                  overview,persistence-boundary}.md
│   │   ├── 2-technology/{angular,aspnet-core,containers-ci,csharp,ef-core}.md
│   │   └── 3-project/{conventions,data-lifecycle,decisions}.md
│   ├── scripts/{check-architecture,check-instructions,check-manifests}.mjs
│   ├── skills/
│   │   ├── workflows: add-dependency, architecture-decision, build-fix, code-review, custom-settings,
│   │   │              git-workflow, project-structure (+references/backend-layout.md, solution-layout.md),
│   │   │              security-scan (+references/scan-layers.md), template-maintenance, verify
│   │   └── knowledge: angular, api-versioning, aspnet-error-handling, authentication, caching, ci-cd,
│   │                  configuration, dependency-injection, docker, dotnet-testing, ef-core, health-check,
│   │                  http-api, httpclient-factory (+references/resilience.md), logging (+references/serilog.md),
│   │                  modern-csharp, swagger
│   ├── INSTRUCTION-MAP.md
│   └── settings.json
├── .editorconfig
├── CLAUDE.md
├── CUSTOM_SETTINGS.md
├── Directory.Build.props
├── Directory.Packages.props
└── SPECIFICATION.md
```

## Structural choices where `CANDIDATE.md` left freedom

1. **Level 0 modules.**
   - `CLAUDE.md` owns precedence, vocabulary, operating principles and the work loop.
   - Imported modules: `product-governance`, `decision-control`, `git-safety`.
   - Path-scoped principle modules: `completion-contract` (workflow obligations), `testing-principles`, `security-principles`, `logging-principles`, `runtime-principles` (performance, caching semantics, external calls) and `dependency-hygiene`.
   - `runtime-principles` and `completion-contract` exist because the level test ("otherwise → Core") puts technology-neutral performance, caching, retry and verification statements at Level 0.
2. **C#/.NET conventions sit at Level 2.** CANDIDATE §2 lists "C#/.NET conventions" under Technology. Async, cancellation, `TimeProvider`, `HttpClient` lifetime, typed options and usings therefore live in `2-technology/csharp.md`, even though .NET is fixed-platform vocabulary.
3. **DI composition sits at Level 1.** Constructor injection, lifetimes and registration placement presuppose the adopted composition-root model, so they live in `backend-layers.md` (Composition).
4. **Health checks sit at Level 1** (`entry-points.md`, Operational endpoints). They presuppose the Api host role.
5. **Development data lifecycle sits at Level 3** (`data-lifecycle.md`), as CANDIDATE §2 lists it. It also owns settings-driven schema changes, the local Development connection string and the production-migration rule, because each depends on project-specific seeding and layout.
6. **No separate `nunit.md` or `fluentvalidation.md` rule.** No NUnit- or FluentValidation-specific normative policy exists beyond the selection (Level 3) and the integration-test rule (`aspnet-core.md`). NUnit and FluentValidation technique lives in the `dotnet-testing` and `aspnet-error-handling` skills.
7. **Workflow levels.**
   - `git-workflow` is Level 0.
   - All other workflows are Level 3, including `architecture-decision` and `template-maintenance`. Both record into or edit concrete Level 1–3 files, so placing them at Level 0 would create reverse references.
   - `custom-settings` is Level 3 because it touches EF Core mapping and Angular surfaces.
8. **Workflow-triggered must-policies have rule owners.** Workflows read those owners explicitly ("Read first"). Greenfield `project-structure` reads every Level 1 module and the relevant Level 2–3 modules before creating files.
9. **Enforcement.**
   - All hooks and checkers are Node.js ES modules, which are cross-platform and dependency-free.
   - The pre-command hook blocks dependency commands until the `add-dependency` marker comment `# add-dependency` is present, and always blocks `npm --force` / `--legacy-peer-deps`.
   - The post-edit hook runs manifest checks (central versions, floating/prerelease versions, listed packages, dev tooling placement, project references), reminds on product-input edits, and runs the structure checker after instruction edits.
   - The Stop hook issues seeder, migration, settings and test co-change reminders. It is guarded by `stop_hook_active` and de-duplicated per changed-file set.
   - `settings.json` sets `ask` permissions for repository-changing Git commands.
10. **The map** is `.claude/INSTRUCTION-MAP.md`, organized level-first. It contains per-module tables with file, owner, scope, loading, enforcement and where to extend, plus a split-statement table, a topic index and an enforcement table.

## Policy-preservation concerns

None blocking. Every policy in `source/inventory.json` (194) and `source/shared-research-invariants.json` (2) maps to exactly one owner, verified by a phrase check against the owner file:

| Owner | Policies |
|---|---|
| `CLAUDE.md` | GOV-012, GOV-013, GOV-014, GOV-018, WF-001, WF-002, WF-003 |
| `0-core/completion-contract.md` | WF-004 … WF-017 |
| `0-core/decision-control.md` | ARC-020, DEP-002, GOV-005, GOV-017 |
| `0-core/dependency-hygiene.md` | DEP-001, DEP-003, DEP-004, DEP-005 |
| `0-core/git-safety.md` | GOV-015, GOV-016, GOV-019, GOV-020, WF-022 |
| `0-core/logging-principles.md` | API-012, RUN-014, SEC-010 |
| `0-core/product-governance.md` | GOV-001 … GOV-004, GOV-006 … GOV-011, GOV-021 |
| `0-core/runtime-principles.md` | RUN-001, RUN-006, RUN-007, RUN-008, RUN-012, RUN-015 … RUN-021, RUN-023 |
| `0-core/security-principles.md` | API-008, SEC-001 … SEC-009, SEC-011 … SEC-018, WF-020, WF-021 |
| `0-core/testing-principles.md` | TST-002 … TST-005, TST-007 … TST-012 |
| `1-architecture/backend-layers.md` | ARC-001 … ARC-008, ARC-012, ARC-021 … ARC-025, ARC-028 |
| `1-architecture/code-organization.md` | ARC-027 |
| `1-architecture/entry-points.md` | API-001, API-003 … API-006, API-013 … API-016, API-018 … API-020, API-022, ARC-010, ARC-011, ARC-026, ARC-029 |
| `1-architecture/frontend-structure.md` | FE-002, FE-003, FE-005, FE-006, FE-007, FE-009, FE-010 |
| `1-architecture/outcomes.md` | API-007, API-009, API-010, API-011, API-021 |
| `1-architecture/overview.md` | ARC-009 |
| `1-architecture/persistence-boundary.md` | ARC-013 … ARC-019 |
| `2-technology/angular.md` | DEP-025, FE-001, FE-004, FE-008, FE-011, FE-012 |
| `2-technology/aspnet-core.md` | API-002, API-017, DEP-021, TST-006 |
| `2-technology/containers-ci.md` | DEP-019, WF-018 |
| `2-technology/csharp.md` | RUN-002 … RUN-005, RUN-009, RUN-010, RUN-011, RUN-013, RUN-022, RUN-024 |
| `2-technology/ef-core.md` | PST-010 |
| `3-project/conventions.md` | DEP-006, DEP-007, TST-001 |
| `3-project/data-lifecycle.md` | DEP-026, PST-001 … PST-009, WF-019 |
| `3-project/decisions.md` | DEP-008 … DEP-018, DEP-020, DEP-022 … DEP-024 |

Trigger classes are preserved:

- Every `always` policy is in the always-loaded surface.
- No `path` policy is imported.
- Every `workflow` policy is either read explicitly by its workflow or always loaded (see the placement deltas below).
- Minimum scopes are covered: `backend/**`, `backend/**/*Tests/**`, `frontend/**`, common globs, delivery-file globs and repo/meta files.

## Intentional wording and placement deltas

- **Split statements** (semantics unchanged; neutral part at Level 0/1, binding at Level 2/3):

  | Policy | Neutral part | Binding |
  |---|---|---|
  | ARC-002/ARC-008/ARC-014/ARC-017/ARC-019 | persistence-framework wording | EF bindings in `ef-core.md`; selection in `decisions.md` |
  | API-001 | transport types | `IActionResult` and other types in `aspnet-core.md` |
  | ARC-010 | thin entry points | Controllers selected in `decisions.md` |
  | API-007 | central handler | `IExceptionHandler` binding in `aspnet-core.md` |
  | API-010 | owning boundary | FluentValidation in `decisions.md` |
  | SEC-008, SEC-016 | `security-principles.md` | Data Protection and Identity bindings in `aspnet-core.md` |
  | FE-001 | feature organization stated in `frontend-structure.md` | standalone APIs in `angular.md` |
  | FE-010 | UX role in `frontend-structure.md` | reactive forms in `angular.md` |
  | ARC-009 | `overview.md` | MediatR/Kommand named in `decisions.md` |

- **Workflow-class policies owned by always-loaded modules:**
  - GOV-002, GOV-007, GOV-021 (product governance);
  - GOV-019, GOV-020, WF-022 (Git safety);
  - WF-001 … WF-003 (`CLAUDE.md` work loop);
  - DEP-017, DEP-020 (conditional technologies in the L3 decisions, which §6.9 requires at planning time).

  Their workflows reference them at the triggering step. This is a superset of the workflow trigger.
- **Inventory overlaps kept as separate owners** (no rewording into one): DEP-013 ↔ TST-001 (NUnit), DEP-012 ↔ API-017 (Swagger exposure — the decisions entry points to `aspnet-core.md`), ARC-020/GOV-017 Reserved list ↔ ARC-009 and ARC-004, PST-004 ↔ TST-008, GOV-013 ↔ DEP-001.
- **ARC-020's examples were merged into the shared Reserved list** in `decision-control.md`, using technology-neutral wording ("multiple persistence contexts" instead of "multiple DbContexts").
- **"Normally" in inventory wording became explicit vocabulary:**
  - API-004, API-007, API-009 and DEP-006 → **default**;
  - API-014 → **must** with "or another explicitly approved compatibility strategy";
  - API-019 → **must** for liveness restart-loop avoidance.
- **Headers follow frontmatter.** Rules, skills and the agent need YAML frontmatter on line 1, so the classification header is the first body line.
- **The `CUSTOM_SETTINGS.md` placeholder** now holds only a pointer and the table. V2's restated rules moved to their owner.
- **Delivery paths are file-type globs.** DEP-019 and WF-018 (scopes backend/frontend) are scoped to Docker and CI file globs anywhere in the repository, which covers every place the policy applies.
- **V2 guidance outside the oracle** stays in workflows and skills as procedure or technique ("prefer", "typical", review cues) without new must-level policy. Examples: removing dead packages, not upgrading on scanner findings, treating `main` as non-rewritable, and iteration limits.
- **Knowledge-skill renames** follow the shared naming: `testing` → `dotnet-testing`, `error-handling` → `aspnet-error-handling`. `serilog` and `resilience` became private references of `logging` and `httpclient-factory`.

## Unresolved ambiguity

- **Duplicate loading of imported rules.** An imported rule's `paths:` might also trigger a second copy when a matching file is read. This behavior is unverified. Paths on imported modules are kept narrow (`SPECIFICATION.md`, `docs/decisions/**`, root build files) to bound the cost.
- **Always-loaded budget.** It is about 5.8k tokens by a chars/4 estimate: about 4.5k for the six always-loaded files plus about 1.35k for 26 skill descriptions. That is slightly above the ~5k target. Further cuts would remove planning-time policy, which §6.18 ranks below reliability. Actual usage remains an outcome to measure.
- **Node.js dependency.** Hooks need Node.js on the PATH. Without it, hook commands fail with a non-blocking error; the map documents this. The `PowerShell` hook matcher and the `skills:` preload field on the agent may be ignored by clients that do not support them. The agent body also reads the workflow file explicitly.

## Broken references found and fixed

- `check-instructions.mjs` reported a `Kind:` token in the map's description of the checker. The wording was changed.
- Negative tests on a scratch copy confirmed detection of:
  - neutrality violations;
  - reverse references;
  - missing `paths`;
  - `Kind:`;
  - foreign private references;
  - wrong header level;
  - broken paths;
  - competing skills.
- The architecture checker missed `AppDbContext` in controllers because of a word-boundary bug. The regex was fixed and re-tested.
- No broken references remain. All `@` imports, `.claude/...` paths and bare rule names resolve.

## Final self-check

| # | Check | Result |
|---|---|---|
| 1 | Template is standalone (no reference to `source/`, task or candidate files, or this workspace) | PASS |
| 2 | All applicable inventory semantics preserved (196/196 mapped, phrase-verified) | PASS |
| 3 | §6 and shared invariants preserved (decision control, challenge, workflows, knowledge set, enforcement, map, vocabulary, parity) | PASS |
| 4 | `CANDIDATE.md` binding rules: level folders, `Level:` headers, neutrality, dependency direction, stratified decisions, no K/L1 leakage, multiple modules per level | PASS (checker-enforced) |
| 5 | One owner per policy; pointer-only cross-references (duplicate-phrase scan reviewed and two re-wordings removed) | PASS |
| 6 | Every internal import/reference resolves | PASS |
| 7 | `trigger_class` and minimum scopes preserved | PASS (deltas above) |
| 8 | No must-rule only in model-invoked or private material | PASS |
| 9 | Product inputs remain inputs | PASS |
| 10 | Workflows, knowledge skills, enforcement and human map present | PASS |
| 11 | No application or benchmark implementation generated | PASS |
| 12 | No research metadata in runtime files (ID/label scan clean) | PASS |
| 13 | No dependency on files outside `output/template/` | PASS |
| 14 | Understandable structure without gratuitous files | PASS |
| 15 | All technical output in English (no Cyrillic found) | PASS |

Commands run on the final template:

- `node .claude/scripts/check-instructions.mjs` → PASS (59 artifacts, 0 failures).
- `check-architecture.mjs` → NOT APPLICABLE (no backend yet).
- `check-manifests.mjs` → PASS.
- Hooks were exercised with simulated inputs. All matched expected exit codes, including Stop-hook de-duplication and the `stop_hook_active` guard.
