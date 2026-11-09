# Generation Report

## Result

| Item | Value |
|---|---|
| Final acceptance result | **PASS** |
| Trigger-role delta count | 0 (196 policies: 194 inventory + 2 shared invariants) |
| Unresolved broken-reference count | 0 |
| Known Windows-hook compatibility defects | 0 |
| Directly observed experimental isolation violations | 0 |
| Confirmation-audit result | 0 concrete template defects |

## Implemented candidate model

L0 — stability-first, embedded capabilities. Instructions are organized by stability, **0 Core → 1 Architecture → 2 Technology → 3 Project**; product/feature/task inputs sit outside the hierarchy. Rules are level-first (`.claude/rules/{0-core,1-architecture,2-technology,3-project}/`), each level holds several cohesive modules, and every instruction artifact starts with a one-line header `Level · Owns · Scope · Loads · Depends on`. Conformance dependencies (`Depends on`) point only to the same or a more stable level; routing pointers may point anywhere. Levels 0 and 1 name no concrete technology beyond .NET/C#/TypeScript. Decisions are stratified: the Level 1 architecture summary (`overview.md`) and the Level 3 project summary (`decisions.md`) are both imported by `CLAUDE.md`. There are no capability contracts, slots, manifests, `Kind:` fields, or Feature/Task levels. The instruction-structure checker enforces these predicates mechanically.

## Runtime files: 71

```text
template/
├── CLAUDE.md                         L0 always (imports overview.md + decisions.md)
├── SPECIFICATION.md                  product input (empty on purpose)
├── CUSTOM_SETTINGS.md                product input
├── .editorconfig  .gitignore  Directory.Build.props  Directory.Packages.props
└── .claude/
    ├── INSTRUCTION_MAP.md            human map, not auto-loaded
    ├── settings.json                 hooks
    ├── hooks/claude-hook.mjs  hooks/manifest-checks.mjs
    ├── tools/check-instructions.mjs
    ├── agents/code-reviewer.md
    ├── rules/
    │   ├── 0-core/          security-principles, logging-principles, testing-principles, dependency-hygiene, runtime-principles
    │   ├── 1-architecture/  overview (imported), backend-layers, persistence-boundary, entry-points, outcomes, frontend-structure, code-organization
    │   ├── 2-technology/    csharp, aspnet-core, ef-core, fluentvalidation, dotnet-testing, angular, logging, containers-ci
    │   └── 3-project/       decisions (imported), package-management, data-lifecycle, layout
    └── skills/
        ├── workflows (12):  development-workflow, project-structure (+2 refs), verify, code-review, build-fix,
        │                    custom-settings, git-workflow, security-scan (+1 ref), add-dependency,
        │                    architecture-decision, template-maintenance (user-only), delivery-pipeline
        └── knowledge (17):  ef-core, http-api, aspnet-error-handling, dotnet-testing, logging (+serilog ref),
                             httpclient-factory (+resilience ref), configuration, dependency-injection, caching,
                             swagger, api-versioning, health-check, docker, ci-cd, angular, modern-csharp, authentication
```

Always-loaded surface (CLAUDE.md + 2 imports + skill/agent descriptions): ≈ 5,000 tokens (chars/4 estimate printed by the checker).

## Meaningful structural choices

- **Core content in CLAUDE.md, neutral principles as Core path rules.** Planning-time Core policy (precedence, product governance, decision control, challenge, simplicity/scope, Git safety, work routing) is in `CLAUDE.md`; file-scoped neutral principles are five `0-core/` path rules.
- **Level test applied literally, with one documented interpretation.** Fixed-platform vocabulary may appear in Levels 0/1, but language/runtime conventions (C# style, async/cancellation APIs, `TimeProvider`, `HttpClient` lifetime, options) sit at Level 2 (`csharp.md`) because CANDIDATE §2 lists "C#/.NET conventions" under Technology. Git is named in Core because CANDIDATE lists Git safety as Core. Protocols and standards (HTTP, TLS, OIDC, CSRF, SQL) count as vocabulary, not technologies. HTTP status semantics are Level 1 (`entry-points.md`) because they presuppose the Api boundary.
- **Two workflows beyond the shared set.** `development-workflow` owns the V2 "Development Workflow" policies (spec read, inspect code, review then verify, seed/migration co-changes, regression tests, performance changes, durable product sources), so the full procedure stays out of `CLAUDE.md`. `delivery-pipeline` owns the CI/CD and production-migration workflow policies; the `ci-cd` and `docker` names stay knowledge-only.
- **Decision recording.** `architecture-decision` records approved decisions in the "Accepted …" section of the matching summary (Level 1 or Level 3). The manifest hook reads those sections, so an approved exception (for example a mediator library) stops being flagged.
- **Hooks.** Every command is `node .claude/hooks/claude-hook.mjs <event>`, with no shell variables; the script finds the project root from its own location. `pre-bash` blocks npm-family `--force`/`-f`/`--legacy-peer-deps`. `post-bash` and `post-edit` route dependency changes to `add-dependency` and check central versions, `VersionOverride`, floating and prerelease versions, deny/review lists, npm tooling category, `.npmrc` bypass, and outward project references. `post-edit` also reminds about product inputs and runs the structure checker after instruction edits. `stop` gives seed/migration/test/custom-settings reminders once per change set; its state lives in the Git directory, and it skips when `stop_hook_active` is set. When a check cannot run, the hook exits 1 with a visible message. The hook command assumes Claude Code's working directory is the project root.
- **The code-reviewer agent delegates by an explicit read** of `code-review/SKILL.md`. No unverified preload mechanism is used.
- **Headers follow the YAML frontmatter.** Rules and skills need frontmatter first, so the header line is the first body line.

## Policy-preservation concerns

None outstanding. The inventory itself contains overlapping policies. Each keeps its own owner with distinct framing, and they point to each other where the clauses coincide: GOV-013/DEP-001, ARC-009/ARC-020, DEP-012/API-017, PST-004/TST-008/WF-019, DEP-010/RUN-013/DEP-021, DEP-014/FE-001, DEP-008/ARC-010.

## Intentional wording/placement deltas

- **Split statements (CANDIDATE §3).** The neutral rule sits in Level 0/1 and the technology binding in Level 2/3. This covers ARC-002, ARC-008, ARC-010, ARC-014, ARC-017, ARC-019; API-001, API-002, API-007, API-010; SEC-008, SEC-016; FE-001, FE-010; ARC-009 (MediatR/Kommand named in `decisions.md`); and TST-007 (Testcontainers optional via DEP-013; EF InMemory in `dotnet-testing.md`). All splits are tabulated in the map.
- **Clauses preserved by owner pointer:**
  - DEP-009: "provider concerns stay out of Application/Domain" → `persistence-boundary.md`.
  - DEP-012: "exposure beyond Development" → `aspnet-core.md` (API-017).
  - DEP-006: "narrowly scoped" → `dependency-hygiene.md`.
- **Neutral wording in Levels 0/1:**
  - "persistence framework / context / set types" replaces DbContext/DbSet/EF.
  - "web-framework transport types" replaces ASP.NET Core types.
  - "HTTP entry points" replaces Controllers.
  - "problem-details contract" replaces ProblemDetails.
  - "single-page frontend" replaces Angular (SEC-011).
  - "platform's established authentication facilities" replaces ASP.NET Core Identity (SEC-016).
  - "normal single save/commit" replaces `SaveChangesAsync` (ARC-018).
- **Strength wording:** API-014's "normally requires" became "requires a new version or another explicitly approved compatibility strategy". It stays a MUST, and the approved-alternative path is kept.
- **Enforcement is stricter than the text in one place:** the hook blocks npm force/legacy-peer flags outright, because a hook cannot judge "merely to bypass". The user can still run such a command manually.
- **V2 restatements removed, examples renamed:** `CUSTOM_SETTINGS.md` now points to its owners instead of repeating them. V2's `ProjectName` placeholders became `<Name>`, matching `backend/<Name>.<Layer>/`.

## Unresolved ambiguity

None that blocks the template. No inputs contradicted each other irreconcilably.

## Broken references found/fixed

- The checker initially reported one false positive (`.claude/settings.local.json`, a `.gitignore` entry); the checker was fixed.
- One section pointer (`development-workflow → Approved product decisions`, in a skill and in a hook message) pointed at a bullet rather than a heading. It now points to the Implement section.
- Eight technology-named pointers in Level 0/1 rules (for example `2-technology/angular.md`, the `ef-core` skill) broke neutrality. They were replaced with neutral pointers to `.claude/rules/2-technology/`.
- Final state: all file, import, skill, and section references resolve (36 section pointers checked).

## Primary-audit repairs that materially changed the template

1. **Neutrality.** Technology-named pointers were removed from 8 Level 0/1 rules, and the checker's term list was extended with `ef-core` and `aspnet`.
2. **Budget.** Skill descriptions were shortened to trigger-first cues, reducing the always-loaded surface from about 5.9k to about 5.0k tokens.
3. **Semantic fidelity.**
   - TST-003 regained V2's "depend *unnecessarily* on…" qualifier; the strengthening was removed.
   - PST-003's seeder path became an example instead of mandatory.
4. **V2 preservation.**
   - Serilog OTLP, Expressions, Elasticsearch-sink, and AuditTo examples were restored.
   - The allocation-sensitive hot-path technique and C# naming/file-layout details were added to `modern-csharp`.
5. **Duplicate/restatement sweep.** About 40 restatements were replaced with owner pointers or technique wording. They were found in knowledge-skill anti-pattern and decision-guide items, the authentication 401/403 block, the `http-api` empty-collection line, health-check startup readiness, secrets lines in `delivery-pipeline` and `docker`, container verification, FluentValidation rule kinds, the headless rule repeated in two workflows, the regression-test definition, seed-change examples, `project-structure`/`solution-layout` copies of `layout.md` and `decisions.md` content, `custom-settings` conflict handling, the `scan-layers` cancellation line, and the Serilog configuration line.
6. **Windows enforcement defect.** A BOM-prefixed hook payload (as PowerShell pipelines produce) failed JSON parsing. The hook and the checker now strip a leading BOM, using code written without `\u` escapes.

## Audit summary

- **Primary audit** — checks run against the generated files:
  - owner, trigger role, and scope mapping for all 196 policies (0 deltas, 0 scope misses);
  - side-by-side semantic-fidelity review of all 196 owner texts (2 repaired);
  - automated V2 coverage: 608 sections, 297 code blocks, 652 headings, with manual review of every unmatched item (3 technique restorations);
  - shingle and distinctive-term duplicate sweeps;
  - structure checker;
  - section-pointer resolution;
  - 60 sandboxed hook/checker tests. These include the exact `settings.json` commands launched through cmd.exe, Windows PowerShell, and bash with stdin payloads, and Git-free and BOM cases. Git discovery was capped with `GIT_CEILING_DIRECTORIES`.
  - hygiene: no research IDs, labels, workspace paths, or model IDs; no Cyrillic; no BOM or control characters.
- **Confirmation audit** — every gate above was rerun after the repairs, and each repaired item was rechecked; all passed. The one new unmatched V2 heading (`http-api` "403 Forbidden") was reviewed: its content is preserved in `entry-points.md` and the `http-api` skill. Result: **0 concrete template defects**.

## Workspace events (directly observed)

- **Experimental isolation violations: 0.** No network access, no parent or sibling directory content, no external repositories.
- **Recoverable workspace-process incident (remediated).** One audit command began with `cd /tmp` before grepping workspace files by absolute path. Nothing was read or written outside the workspace; the tool reset the working directory to the run root, and later commands used workspace paths only.
- **Platform-managed persistence events.**
  - The tool runtime automatically saved two oversized command outputs to the user's Claude profile `tool-results` folder. They were not opened, and the evidence was regenerated under `output/.work/`.
  - After the template's skills were written, the desktop runtime listed `output/template/.claude/skills` as available session skills. None were invoked, and nothing depends on that listing.
  - The environment offered a scratchpad directory outside the workspace; it was not used.
- `output/.work/` was removed at completion. `output/` contains only `template/` and this report.
