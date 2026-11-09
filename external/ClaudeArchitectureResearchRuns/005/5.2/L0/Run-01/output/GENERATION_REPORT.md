# Generation Report

## Implemented Candidate Model

L0 — stability-first organization with embedded technologies. Rules are
level-first under `.claude/rules/{0-core,1-architecture,2-technology,3-project}/`,
each module cohesive with its own `paths` trigger. Every instruction artifact
starts with `> Level: <n> <Name> | Owns | Scope | Loads | Depends on`.
Conformance dependencies point only to the same or a more stable level; routing
pointers (`→`) may point anywhere. Levels 0–1 name no concrete technology.
Decisions are stratified: the architecture summary (`1-architecture/overview.md`)
and the project summary (`3-project/decisions.md`) are both imported by
`CLAUDE.md`, and they stay separate. There are no `Kind:` fields, contracts, slots,
module manifests, or feature/task levels. Technologies (NUnit, EF Core, Angular,
Serilog, …) are named directly at Levels 2–3, in workflows, and in assets.

## Runtime File Count and Tree

78 files in `output/template/`:

```text
CLAUDE.md  SPECIFICATION.md (empty)  CUSTOM_SETTINGS.md
.editorconfig  .gitignore  Directory.Build.props  Directory.Packages.props
.claude/
├── INSTRUCTION_MAP.md          human map (not loaded)
├── settings.json               hooks
├── agents/code-reviewer.md
├── hooks/                      lib, dependency-guard, post-edit, stop-cochange (.cjs)
├── scripts/                    check-instructions.cjs, check-manifests.cjs, dependency-policy.json
├── rules/
│   ├── 0-core/                 security, logging, dependency-hygiene, structure, testing,
│   │                           error-exposure, health, performance, caching, integration (10)
│   ├── 1-architecture/         overview*, backend-layers, persistence-boundary, entry-points,
│   │                           outcomes, frontend-structure (6)
│   ├── 2-technology/           csharp, dotnet-runtime, aspnet-core, ef-core, backend-testing,
│   │                           logging, package-management, angular, containers (9)
│   └── 3-project/              decisions*, data-lifecycle (2)        (* imported, always-loaded)
└── skills/
    ├── workflows (11): develop, project-structure (+3 private refs), verify, code-review,
    │   build-fix, custom-settings, git-workflow, security-scan (+1 private ref),
    │   add-dependency, architecture-decision, template-maintenance (user-only)
    └── knowledge (17): ef-core, http-api, aspnet-error-handling, dotnet-testing,
        logging (+references/serilog.md), httpclient-factory (+references/resilience.md),
        configuration, dependency-injection, caching, swagger, api-versioning,
        health-check, docker, ci-cd, angular, modern-csharp, authentication
```

## Structural Choices (Where the Candidate Allowed Freedom)

- **Core always-loaded content lives directly in `CLAUDE.md`**, not in an
  extra imported Core file; Core path rules hold the technology-neutral
  principles. Only the two decision summaries are imported.
- **A `develop` workflow** owns the development procedure (spec reading, rule
  reads, change-type obligations, review → verify). The shared construction
  contract forbids putting that procedure in `CLAUDE.md`, and the shared
  workflow list has no other owner for it.
- **Level placement follows the four-question test.** Technology-neutral
  health, performance, caching, and outbound-integration principles are
  therefore Core path rules. HTTP status and versioning semantics sit at
  Level 1 (`entry-points.md`) because they presuppose the Api boundary.
  Development data lifecycle is Level 3.
- **Protocols and standards are treated as vocabulary, not concrete
  technologies:** HTTP, TLS, SQL, CORS, OIDC, OpenAPI, ProblemDetails. The
  checker's deny-list covers products and libraries.
- **No separate `layout.md`.** The always-needed layout is in `decisions.md`;
  illustrative layouts are private references of `project-structure`.
- **Workflow levels:** most workflows are Level 3 because they embed commands
  and layout. `custom-settings`, `architecture-decision`, and
  `template-maintenance` are Level 0; `custom-settings` uses "persistence
  mapping" to stay technology-neutral.
- **Mechanical enforcement:**
  - `check-manifests.cjs`: central package management, floating/prerelease
    versions, package deny and approval lists, inward project references,
    narrow test references.
  - `check-instructions.cjs`: all L0 structural predicates, plus a
    `--rules-for <path>` lookup that workflows use for greenfield rule reads.
  - Hooks route to their owning workflows. Commands that bypass a hook carry
    explicit markers: `# add-dependency:checked` and
    `# project-structure:approved`.
- **Windows-safe hook commands:**
  `node -e "require(require('path').resolve(process.env.CLAUDE_PROJECT_DIR||'.','.claude','hooks','<x>.cjs'))"`.
  The project directory is resolved inside Node, so no shell expansion is
  needed. Tested from Git Bash, PowerShell 5.1, and cmd, including from a
  different working directory.

## Intentional Wording/Placement Deltas

1. **Split statements for neutrality.** Each rule keeps a neutral stable part,
   with its technology binding at Level 2 or 3:
   - Domain and Application independence, repository contracts, the shared
     persistence context, thin entry points, HTTP semantics in Api, and
     centralized failures → bindings in `ef-core.md` and `aspnet-core.md`.
   - Validation boundaries → FluentValidation selection in `decisions.md`.
   - No custom cryptography → Data Protection scope in `aspnet-core.md`.
   - CSRF: "do not assume the frontend framework removes the risk" (Angular
     generalized).
   - Frontend HTTP boundary and validation-as-UX → bindings in `angular.md`.
   - Provider fidelity → InMemory and Testcontainers bindings in
     `backend-testing.md` and `decisions.md`.
   - CQRS/mediator → MediatR and Kommand named in `decisions.md`.
   - "Multiple DbContexts" → "multiple persistence contexts", with the
     binding in `ef-core.md`.
2. **Swagger baseline vs. exposure.** The Swagger baseline in `decisions.md`
   keeps the selection ("default Development surface"). The overlapping
   "expose outside Development only when justified" clause has a single owner,
   `aspnet-core.md` (the environment-aware exposure policy), reached by a `→`
   pointer. That clause is therefore path-loaded, not always-loaded.
3. **Overlapping inventory pairs are kept as distinct owners without
   rewording each other:**
   - NUnit selection (`decisions.md`) vs. NUnit usage default
     (`backend-testing.md`);
   - logging selection vs. `ILogger` template vs. Serilog integration;
   - Angular library defaults vs. simple-state default;
   - conditional resilience vs. resilience package choice;
   - Development-only seeding vs. deliberate production migrations (the
     latter refers to the former).
4. **Generic vs. concrete Reserved decisions.** `CLAUDE.md` holds the generic
   Reserved categories and the five-question test. `overview.md` holds the
   concrete consequential-architecture catalog.
5. **Version-control safety at Core says "version-control" instead of "Git";**
   the Git-specific procedure is in `git-workflow` (Level 3).
6. **Skill renames to the shared names:** `testing` → `dotnet-testing`,
   `error-handling` → `aspnet-error-handling`. `serilog` and `resilience`
   became private references. V2 `technology-stack.md` is split into
   `decisions.md` (selection) and a `project-structure` private reference
   (scaffolding details).
7. **Code-reviewer independence** is owned by the agent file.
8. **One non-oracle V2 statement became guidance:** removing dependencies a
   change made unused ("prefer").

## Policy-Preservation Concerns

- Workflow-class must-policies are owned by model-invoked workflows, as
  `trigger_class: workflow` requires. They are reached through always-loaded
  routing (`CLAUDE.md` → `develop` → `verify`) and the Stop-hook reminders.
- The hook bypass markers are self-attested: they route behavior but do not
  prove the workflow ran.
- The agent `skills:` preload and `disable-model-invocation` are used with
  explicit fallbacks: the agent reads the skill file, and the skill text says
  "user-only". Path triggering on file creation is not relied upon; greenfield
  workflows read rules explicitly.

## Unresolved Ambiguity

None blocking. The interpretations above — the protocol vocabulary and the
level placement of neutral backend principles — are recorded as design choices.

## Broken References Found and Fixed

- `aspnet-core.md` → `decisions.md`: a reverse (L2 → L3) conformance reference;
  removed via delta 2.
- `containers.md` pointed to a non-existent `develop` section; corrected.
- "Rule Reads table" pointers had no matching heading in `develop`; heading
  renamed.
- `angular` skill → `decisions.md` lacked the routing arrow; fixed.
- Two checker/tooling defects fixed during audit:
  - the routing scan included the header line;
  - the `PackageReference` regex could span elements.

Unresolved broken references: **0**.

## Second Audit-and-Repair Cycle

A second cycle replaced keyword-level checks with item-level evidence.

- **Semantic side-by-side review.** All 196 policies (194 inventory + 2 shared)
  were printed next to their exact owning paragraph and read one by one against
  the normalized policy and its strength. Seven strength drifts were repaired:
  - GOV-003: the "do not invent" clause had become conditional;
  - SEC-003: validation lost its "when assumptions matter" condition;
  - API-013: "only when" was stronger than the inventory;
  - API-019: startup readiness lost its conditional framing;
  - DEP-006: "normally versionless" had become "versionless";
  - DEP-007: "unless there is a reason" was dropped;
  - WF-004: "remove accidental artifacts" had become "confirm none were added".
- **Restatement sweep.** Knowledge and workflow skills were reviewed for
  rewording of rule-owned policy. Restatements in these files became technique
  or check-by-reference:
  - knowledge skills: `http-api`, `dotnet-testing`, `aspnet-error-handling`,
    `angular`, `caching`, `authentication`, `logging`, `ef-core`, `ci-cd`,
    `docker`, `health-check`;
  - workflow skills: `custom-settings`, `build-fix`, `git-workflow`,
    `project-structure`.
- **V2 preservation map.** All 652 headings of the 41 V2 files (one file, the
  empty `SPECIFICATION.md`, has none) were mapped to template files.
  - 549 matched by full keyword match.
  - At first, 105 had no keyword match. Manual review found five real gaps,
    which were restored:
    - HTTPS redirection is not required when the hosting topology already
      enforces TLS;
    - PUT/DELETE are not automatically safe to retry;
    - the security-scan false-positive lists and cross-skill guidance;
    - allocation-sensitive technique detail;
    - the "empty `SPECIFICATION.md` is intentional" note.
  - Two of the 105 then matched. Each remaining heading (mostly generic: Core
    Principles, Anti-Patterns, Goal) was given an explicit destination file and
    a required phrase, verified by script: **103/103 present**.

## Convergence Cycle

A final from-scratch cycle re-ran every scripted check in one pass against the
final files and made **no changes to the template**. Result: 14 check groups,
**0 failing, 0 defects**.

- All 196 owners have verified text; trigger-role deltas 0; scope misses 0.
- 652/652 V2 headings placed (549 keyword-matched, 103 mapped and verified).
- No workspace/research references, no research metadata, no non-English text.
- `check-instructions` and `check-manifests` both exit 0.
- 35/35 hook and checker regression cases pass.
- Workspace top level is inputs plus `output/`; `source/` is unmodified; the
  template has 78 files.

The audit has converged: repeating it changes nothing.

**This cycle made no out-of-workspace probes.** Evidence:

- **Git:** the sandbox (`output/.work/sandbox`) ran with
  `GIT_CEILING_DIRECTORIES` set to its parent, `output/.work`. A control test
  placed a decoy repository inside the workspace directly above a capped
  sandbox.
  - Without the ceiling, `git rev-parse --show-toplevel` returned the decoy, so
    Git does search upward.
  - With the ceiling, it returned
    `fatal: not a git repository (or any of the parent directories)`, so the
    ceiling stops the upward search before the capped parent.
- **Node:** every `require` in the shipped hooks and scripts is a built-in
  (`fs`, `path`, `crypto`, `child_process`) or an explicit relative or
  root-anchored path, so Node never searched ancestor `node_modules`
  directories.
- **Scope of every command:** all commands and file operations in the cycle
  targeted paths under `output/` (the script's own path guard throws on any
  escape).

## Final Self-Check (Section 10 Evidence)

| # | Check | Evidence | Result |
|---|---|---|---|
| 1 | Standalone | No template line references `source/`, workspace files, or paths outside the template; the only `../` hits are a path-traversal example and a `src/.../File.cs` placeholder | PASS |
| 2 | V2 policy semantics preserved | 196-item side-by-side review after the repairs above; all 652 V2 headings have a verified destination | PASS |
| 3 | Shared requirements | Decision control, challenge obligation, separation of concerns, scope taxonomy, workflow/knowledge set, enforcement, map, vocabulary, and execution parity are all present; checker verifies the required sets | PASS |
| 4 | Candidate binding rules | Checker enforces: level-first directories, `Level:` headers, Levels 0–1 technology neutrality, dependency direction plus acyclicity, routing-pointer discipline, stratified imports, and no `Kind:`/contract/slot fields | PASS |
| 5 | One owner, no accidental duplication | Every policy has one owner file; restatement sweep done; overlapping inventory pairs documented as deltas | PASS |
| 6 | References resolve | Checker resolves rule paths, `.claude/` paths, private references, and skill/agent names; manual section-name check; **unresolved broken references: 0** | PASS |
| 7 | Trigger roles | always → `CLAUDE.md` or its imports; path → rule file; workflow → workflow skill or agent. **Trigger-role delta count: 0** | PASS |
| 8 | Minimum scopes | Each owning rule's `paths` matched against sample files for its scope; 0 misses | PASS |
| 9 | Critical must-rules not only on demand | No policy is owned by a knowledge skill or private reference; workflow-class policies are reached through always-loaded routing | PASS |
| 10 | Procedures in workflows | `CLAUDE.md` holds policy and routing pointers only; the development procedure is in `develop` | PASS |
| 11 | Product inputs stay inputs | `SPECIFICATION.md` empty; `CUSTOM_SETTINGS.md` is a table with a pointer header; neither carries rules | PASS |
| 12 | Required artifacts present | 11 workflows, 17 knowledge skills, agent, hooks, checkers, assets, map (checker-verified) | PASS |
| 13 | Windows hooks | Launcher resolves the project directory in Node and was tested from Git Bash, PowerShell 5.1, and cmd, including another working directory. The final regression suite (35 cases: 11 guard, 8 post-edit, 5 stop, 11 checker) all pass. **Known Windows-hook compatibility defects: 0** | PASS |
| 14 | Isolation and incidents | Ledger verified against the platform session log: 0 isolation violations; 5 recoverable process incidents, all remediated; 2 platform events, each confirmed by one platform entry, with no dependency | PASS |
| 15 | No application/benchmark | Sample projects existed only in `output/.work/` sandboxes, since deleted | PASS |
| 16 | No research metadata | 0 hits for policy IDs, research labels, or research file names in `output/template/` | PASS |
| 17 | No outside dependencies | Same as item 1; hooks and scripts use only Node built-ins and the template's own files | PASS |
| 18 | Understandable, no gratuitous files | 78 files; each module has one owner and trigger; map organized by level, then module | PASS |
| 19 | Compact always-loaded surface | ≈ 4.4k tokens including skill listings (chars/4); no trigger role changed to save tokens | PASS |
| 20 | English only | 0 non-ASCII letters outside typographic symbols in `output/template/` | PASS |

## Workspace Events (Verified Against the Platform Session Log)

**Method.** The ledger was first built by walking every tool call in this
session's conversation record. It was then independently verified against the
platform's own session transcript, read with these limits:

- only this session's file, opened by its exact ID, with no directory listing;
- read-only, inside an audit script under `output/.work/`;
- printed only aggregates and path references, never message content.

`TASK.md` section 5 classifies platform-stored session data as a persistence
event that does not prevent PASS unless the run reads forbidden information from
it. This file contains only this run's own activity. The read itself is
recorded below as incident 5.

**Results from the platform log:**

- **Tool calls:** 227 recorded at the first verification (Bash 69, Read 40, Write 92, Edit 24,
  PowerShell 1, ToolSearch 1).
- **File targets:** 156 Read/Write/Edit file targets, of which exactly **1** is
  outside the workspace: the mistyped first `Read` (incident 1).
- **Path-like strings in tool inputs:** every out-of-workspace string is one of
  these:
  - a ledger row below;
  - report or ledger text that only mentions a path;
  - a regex false positive: `cmd /c` and `/d` switches, `Env:\`, an
    `https://example.test` URL, or `s:\n`.

  There is no reference to any parent, sibling-run, network, or other external
  location, and no reference to the auto-saved tool-results file (confirming it
  was never read back).
- **Platform-produced entries:** exactly **1** "Output too large … saved to
  …tool-results…" event, and exactly **1** `nested_memory` attachment, whose path
  is `…\Run-01\source\v2-baseline\CLAUDE.md` (inside the workspace). No other
  memory auto-load is recorded.

| Activity | Evidence | Location | Classification |
|---|---|---|---|
| Read `TASK.md`, `CANDIDATE.md`, `source/**` | 155 in-workspace file targets | workspace | allowed |
| All writes: Write/Edit, redirects, `cp`, `sed -i`, `git init` in sandboxes | Every file target under `output/` | `output/` | allowed; `output/.work/` deleted after each cycle |
| First `Read` used a mistyped path (a `C:\Projects\AI\Learning\…\TASK.md` variant) | The single outside file target; result "File does not exist" | outside, not existing | recoverable process incident 1: no content obtained; retried at the workspace path |
| Wrong-cwd negative hook test: Node tried `C:\.claude\hooks\post-edit.cjs` | Command input plus "Cannot find module" | outside, not existing | recoverable process incident 2: intended failure test; no content obtained |
| `git status` in a not-yet-initialized sandbox, 6 times across 3 test runs; Git checks ancestors for `.git` | "not a Git repository" output | ancestor directories (existence only) | recoverable process incident 3: nothing found, nothing read. The final cycle capped discovery with `GIT_CEILING_DIRECTORIES`, proven by a decoy-repository control test |
| `test -e /tmp/null_err_unused` | "absent (never written)" | outside (existence only) | recoverable process incident 4: no content obtained |
| Ledger verification reads of this session's own platform transcript (one file, read-only, during verification cycles) | Commands in this cycle | platform session file | recoverable process incident 5: deliberate, scoped, this run's own data only; no forbidden information; the output does not depend on it |
| Launcher tests with cwd `C:\` (`cd /c`, `Push-Location C:\`) | Command inputs | working directory only | allowed: no outside file read |
| Oversized command output auto-saved by the tool runtime | 1 platform entry; never read back | platform | platform-managed persistence event |
| V2 baseline `CLAUDE.md` auto-loaded as project memory | 1 `nested_memory` attachment | platform; content inside the workspace | platform-managed persistence event |

- **Experimental isolation violations: 0.** Verified against the platform log:
  no parent, sibling-run, other-run, network, external-repository, or excluded
  research content was read or used. `source/` is unmodified.
- **Recoverable workspace-process incidents: 5, all remediated.** None wrote outside the workspace. Incidents 1–4 obtained no
  content. Incident 5 read only this run's own session record, solely to verify
  this ledger.
- **Platform-managed persistence events: 2.** Each is confirmed by exactly one
  platform-produced log entry. Neither supplied external information or created
  a dependency of the result.
- **History.** Earlier drafts recorded 0 incidents, undercounted the Git probes,
  attributed a second memory auto-load, and listed an inferred
  transcript-storage event. The platform log confirms the corrected figures
  above.

**Final acceptance result: PASS**
