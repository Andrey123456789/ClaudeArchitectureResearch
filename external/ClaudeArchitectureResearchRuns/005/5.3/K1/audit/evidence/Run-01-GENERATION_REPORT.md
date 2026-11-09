# Generation Report

## Result

| Item | Value |
|---|---|
| Final acceptance result | **PASS** |
| Trigger-role delta count | 0 (196 of 196 policies mapped: 194 inventory + 2 shared invariants; always 32, path 123, workflow 41) |
| Minimum-scope failures | 0 |
| Unresolved broken references | 0 |
| Known Windows-hook compatibility defects | 0 |
| Directly observed experimental isolation violations | 0 |
| Recoverable workspace-process incidents | none observed |
| Platform-managed persistence events | 1 (see Workspace events) |
| Confirmation audit | 0 concrete template defects |

## Implemented model

Kinds × Scopes plus four replaceable capability slots, with static composition:

- **Kinds**: OP (`CLAUDE.md`), DEC (imported decision register, plus slot contracts and module manifests read on demand), STD (`.claude/rules/<scope>/`, every file with `paths:`), KNW (17 shared knowledge skills), WF (11 workflow skills, the thin `code-reviewer` agent, and one `workflow-facet.md` per module), ENF (settings, hooks, scripts, enforcement facets, `.editorconfig`, `Directory.*.props`), IN (`SPECIFICATION.md`, `CUSTOM_SETTINGS.md`).
- **Scopes**: common, backend, backend-tests, frontend, delivery, repo/meta.
- **Slots**: architecture → clean-architecture (required frame); persistence → ef-core, variant sqlserver (required leaf, `binds: architecture`); backend-testing → nunit (required leaf, `binds: architecture`); frontend → angular (optional leaf). Each slot has `CONTRACT.md`, a `MODULE.md` listing every facet, and facets distributed by Kind. Selection lives in the register's Capability selection section, and the structure checker enforces the leak rule.
- **Neutral policy + implementation facet** pairs: `architecture.md`/`architecture-style.md`, `persistence.md`/`persistence-technology.md`, `testing.md`/`test-framework.md`, `frontend.md`/`frontend-framework.md`.
- Every file starts with `Kind | Scope | Capability | Loading`. `.claude/MAP.md` provides the Kind × Scope view, the Capability view and a topic → owner index; it is not loaded at runtime.

## Runtime files: 84

```text
CLAUDE.md  SPECIFICATION.md (empty)  CUSTOM_SETTINGS.md  .editorconfig  Directory.Build.props  Directory.Packages.props
docs/architecture/decision-register.md
.claude/
  MAP.md  settings.json
  agents/code-reviewer.md
  capabilities/{architecture,persistence,backend-testing,frontend}/CONTRACT.md
  capabilities/architecture/clean-architecture/{MODULE.md,workflow-facet.md}
  capabilities/persistence/ef-core/{MODULE.md,workflow-facet.md}
  capabilities/backend-testing/nunit/{MODULE.md,workflow-facet.md}
  capabilities/frontend/angular/{MODULE.md,workflow-facet.md}
  rules/common/{security,dependencies,repository-structure}.md
  rules/backend/{architecture,architecture-style,persistence,persistence-technology,http-api,error-handling,security,performance,integrations,coding-style,operations}.md
  rules/backend-tests/{testing,test-framework}.md
  rules/frontend/{frontend,frontend-framework}.md
  skills/ (workflows) development-workflow project-structure verify code-review build-fix custom-settings git-workflow
          security-scan(+references/scan-layers.md) add-dependency architecture-decision template-maintenance
  skills/ (knowledge) ef-core http-api aspnet-error-handling dotnet-testing logging(+references/serilog.md)
          httpclient-factory(+references/resilience.md) configuration dependency-injection caching swagger api-versioning
          health-check docker ci-cd angular modern-csharp authentication
  hooks/{pre-tool-use,post-tool-use,stop}.mjs  hooks/lib/dependency-commands.mjs
  scripts/{check-instructions,check-architecture,check-manifests}.mjs  scripts/lib/common.mjs  scripts/enforcement.json
  scripts/facets/{architecture,persistence,frontend}/enforcement.json  scripts/facets/backend-testing/ArchitectureConformanceTests.cs
```

## Structural choices (where the candidate allowed freedom)

- Operating policy is written directly in `CLAUDE.md`, which imports the register; nothing else is always loaded. The estimated always-loaded surface is about 5.3k tokens, including skill descriptions.
- Module directories hold only `MODULE.md` and the WF facet (`workflow-facet.md`). Workflows reach that facet by role through the register, which lists each module path and knowledge facet. All other facets live in their Kind's location. ENF facets are role-named data under `.claude/scripts/facets/<slot>/`, read by neutral engines at fixed role paths.
- The architecture frame has no knowledge facet, because the shared knowledge set has no name for it. Its layout and type-role technique lives in its workflow facet.
- A `development-workflow` skill was added. §7.3 keeps the Development Workflow out of `CLAUDE.md`, and no shared workflow owned the inspect → implement → review → verify procedure.
- No `rules/delivery/` directory exists, because the inventory has no path-triggered delivery policy. `docs/decisions/` is created by `architecture-decision` with the first record instead of being shipped empty.
- Common-scope rules use `paths: **/*`. NuGet and npm conventions share one common dependency rule, as in V2.
- Enforcement includes:
  - a deny-once PreToolUse gate that routes dependency commands to `add-dependency`;
  - PostToolUse manifest and architecture checks, plus product-input reminders;
  - Stop co-change reminders, deduplicated per session and never repeated while `stop_hook_active` is set;
  - a neutral architecture engine, also run by the NUnit adapter from the backend-testing ENF facet;
  - a K1 structure checker covering headers, kinds and locations, `paths:`, slot composition, manifest completeness, the leak rule, references, frontmatter validity and hook commands.
- Hook commands are `node -e` bootstraps. They find `.claude/hooks/<hook>.mjs` from the current directory upward and use no `$`, `%` or backticks, so they work in cmd, PowerShell and bash and from subdirectories.

## Intentional wording and placement deltas

1. **Leak rule.** Non-module owners use role terms instead of implementation names. ARC-002, ARC-008, ARC-011 and ARC-014 say "persistence technology / persistence-technology types / persistence context", and the persistence STD facet lists the concrete EF Core and SQL Server types. SEC-011 says "a single-page frontend". FE-003 says "HTTP client calls". FE-010 says "structured form mechanism", bound to reactive forms in the frontend facet. TST-006 says "the persistence technology".
2. **Workflow-trigger policies need a workflow owner.**
   - `verify` owns WF-004–009, WF-017–019, TST-009, TST-010 and RUN-010.
   - `development-workflow` owns GOV-002, WF-001–003, PST-008 and RUN-012.
   - `architecture-decision` owns GOV-007 and API-022.
   - `add-dependency` owns DEP-003–005, DEP-017, DEP-020 and DEP-025.
   - The persistence workflow facet owns PST-009 and PST-010.
3. **DEP-013 placement.** The register states the test stack and points to the repository layout (DEP-024) and the architecture frame for test-project placement, because placement belongs to the frame.
4. **Overlaps inherited from the inventory are kept, one owner each, framed for their trigger role**: DEP-012/API-017, DEP-009/ARC-008/ARC-019, DEP-013/TST-001, DEP-010/API-010, DEP-011/DEP-020, DEP-001/GOV-013, ARC-009/ARC-020/ARC-004, DEP-015/FE-006, PST-004/WF-019, FE-001/FE-007.
5. **Non-oracle technique moved to the owning facet**:
   - EF Core transient-retry and command-logging tuning, plus raw-SQL API cues, went to the persistence facets.
   - Angular build-fix diagnostics, sanitizer-bypass cues and static hosting went to the frontend facets.
   - Constructor, record and `var` guidance went to `modern-csharp`.
   - Knowledge decision guides that restated standards became technique-only quick references or check-by-reference lists.
6. **Renames.** V2 `error-handling` → `aspnet-error-handling` and `testing` → `dotnet-testing`. `serilog` and `resilience` became private references of `logging` and `httpclient-factory`.

## Policy-preservation concerns

- Workflow-trigger must-policies live in workflow skills, as the frozen trigger class requires. Their invocation is made reliable by the always-loaded routing in `CLAUDE.md` and by the dependency hooks.
- Hook output uses the Claude Code hook fields `decision`/`reason`, `hookSpecificOutput.additionalContext` and `systemMessage`.
- The NUnit adapter (`ArchitectureConformanceTests.cs`) was reviewed statically but not compiled, because compiling it requires a NuGet restore and the run uses no network.

## Unresolved ambiguity

None that blocks acceptance. `SPECIFICATION.md` stays empty, with no header, so its "non-empty" semantics hold. `settings.json` cannot carry a header line (JSON); `MAP.md` documents it.

## Broken references found and fixed

The first checker run reported 33 reference or pointer issues.

- Most came from checker parsing: table pipes, numbered headings, role file names like `workflow-facet.md`, and the map listing private references. The checker was corrected.
- Real template fixes: three short `references/…` paths in `MAP.md`, one `.claude/rules/delivery/` reference, and two pointer phrasings.

Final unresolved: 0.

## Primary-audit repairs that materially changed the template

- **Fidelity**: ARC-003 wording restored (validation and transition rules "do not by themselves justify a Rich Domain Model"). TST-003 strengthening removed. DEP-018 brought closer to V2.
- **Restatements removed**: clauses in the ARC-022 and RUN-022 owners; DEP-006 in `add-dependency`; DEP-014 in the frontend facet; GOV-001 in `code-review`; PST-001 in `ef-core`; TST-009 detail in `verify`; DEP-019 in `docker`; RUN-020 in `caching`; FE-003 in `angular`; ARC-010 in the `http-api` skill; the 201 definition in the `http-api` rule; declared-property restatements in all four `MODULE.md` files. Enforcement messages now point to owners instead of restating rules.
- **V2 preservation restored**: allocation-sensitive technique, the security → dependency-policy pointer, the typed-options example, the speculative-scaffolding examples, Serilog enricher/diagnostic-context/OTLP/Elasticsearch examples, and logging notes.
- **Structure**:
  - Removed the frame → leaf conformance cycle by making the `architecture-style.md` role definition self-contained.
  - Moved NUnit test-project and adapter placement to the frame.
  - Removed the `.angular` implementation-name leak from a neutral script.
  - Completed the §7.14 fields in `MAP.md`.
  - Replaced hook commands with the upward-search bootstrap.
  - Fixed invalid YAML in the `git-workflow` description and added a frontmatter check.
  - Removed a redundant `using` from the adapter.
  - Removed ambiguous "normally" from a standard.

## Audit evidence (in-workspace, removed after completion)

- Owner, trigger and scope map for all 196 policies, with anchors verified in the owner text.
- Side-by-side semantic-fidelity review of every owner.
- Automated V2 coverage over 687 sections in 41 files; the 45 residual flags were reviewed manually and are all intentional (V2 path pointers replaced by the register and facets, neutralized names, `<Name>` placeholders).
- 5-gram and 4-gram restatement sweeps.
- Hygiene scan: no research labels, policy IDs, workspace or research-file references, model IDs or non-English text.
- 64 of 64 deterministic tests in a sandbox copy:
  - checker negative cases;
  - architecture and manifest violations;
  - PreToolUse, PostToolUse and Stop behavior, including no loop and read-only Git;
  - the exact `settings.json` commands through cmd.exe, PowerShell and bash, from the root and from nested subdirectories;
  - a bounded not-found case and clear failure on invalid enforcement data.

## Workspace events

- **Isolation violations: 0.** Only `TASK.md`, `CANDIDATE.md`, `source/` and the run's own `output/` were read.
- **Platform-managed persistence: 1.** The tool runtime automatically saved one oversized command output (an inventory listing) to its session tool-results store outside the workspace. It was not opened; the data was re-read from `source/` in smaller parts.
- **Recoverable incidents: none observed.** Tests ran in `output/.work/sandbox`, with `TEMP`/`TMP`, Git global config and `GIT_CEILING_DIRECTORIES` confined to the sandbox. The hook not-found test was bounded at the sandbox so that no parent directory was probed. `output/.work/` was removed at completion.
