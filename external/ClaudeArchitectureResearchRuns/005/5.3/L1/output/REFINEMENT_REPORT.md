# Refinement Report — L1 (Iteration 005 / 5.3)

## Final status: **BLOCKED** (Corrective pass — iteration 8: P6 preservation unresolved, owner decision required); history: **STRICTLY_BETTER** accepted through iteration 6; iteration 7 reported **BLOCKED (confirmation protocol)**

Every mandatory defect D1–D15 is repaired with behavioral evidence, D16/D17 reviews are complete, the strict cumulative gate passes on every item, and one complete cumulative confirmation audit found **0 concrete template defects**.

Independent verification after iteration 1 found D1 and D2 still incomplete: Level 0/1 kept controller technique, and the checker let plain technology nouns pass. Iteration 2 (last section of this report) closed both while keeping every other iteration-1 result. Where the iteration-1 sections below claim D1/D2 complete, the iteration-2 section supersedes them. All other iteration-1 results stand: their runtime files are byte-identical.

Iteration 3 (final section) closed two remaining blind spots in deterministic checking: case-sensitive technology/implementation matching, and frame-owned Level 1 artifacts skipping the fail-closed API-shape check. It changed only the checker and the frame's maintainer metadata, and the iteration-2 instruction content is unchanged.

Iteration 4 (final section) closed the last two reproduced checker bypasses:
- routing-pointer masking of a clause that also carries a requirement;
- frame metadata legalizing arbitrary API-shaped identifiers.

It again changed only the checker and two maintainer-metadata sentences.

Iteration 5 (final section) closed the last reproduced routing bypass: normative wording placed in a label before an otherwise valid routing pointer. It changed only the checker.

Iteration 6 (final section) replaced line-oriented routing patches with one bounded abstraction: routing and neutrality are classified per logical Markdown statement, and the classification is proven invariant across a finite, documented set of formatting forms. It changed only the checker.

Iteration 7 (final section) fixed the remaining P4 false exemption. A routing marker can no longer legalize a technology selection, because masking now requires a positive reference proof instead of any short prefix. It changed only the checker. Its stop condition is reported as **BLOCKED (confirmation protocol)**; see the end of the iteration-7 section.

Iteration 8 (final section) closed the two remaining P4 false negatives in the routing exemption:
- adding a sibling no longer turns a selecting heading or parent item into an unchecked section title;
- a sibling obligation that explicitly refers to the indicated technique ("Must use this technique") now binds the pointer.

It started from the iteration-7 tree and changed only the checker. It reports **BLOCKED**: 9 previously accepted PASS fixtures now fail, so P6 preservation is unresolved. See the end of the iteration-8 section.

| Gate metric | Result |
| --- | --- |
| Normalized runtime requirements represented | 196 / 196 (194 inventory + GOV-017/GOV-018) |
| Authoritative-owner regressions | **0** (owner file per policy identical to baseline) |
| `trigger_class` deltas | **0** |
| Minimum-scope misses | **0** |
| Duplicate owner texts (anchor uniqueness) | 0 |
| Unresolved broken references | **0** |
| Regression matrix (harness) | **212 / 212** checks pass |
| Instruction checker on the template | PASS (67 artifacts, 0 violations, 0 warnings) |
| Runtime hygiene (language, research metadata, standalone, JS parse) | 0 findings |
| Cumulative confirmation audit | **0 concrete template defects** |

## Baseline provenance

- Immutable comparison point: **5.2 / L1 / Run-02** (`baseline/template/`), copied byte-identically to `output/template/` before any change (`diff -r`: identical).
- Initial tree hash (SHA-256 of the sorted per-file SHA-256 list): `852d78f8a8f8094d9507bdb8b827781b79cfc1696d94df65e91301b644c52422` (85 files).
- Final tree hash (same method): `7d52dd424fe003ca9217ed3376ccfb8ef7c322eb43a42cac73765ea6fa97191f` (86 files).
- Run-01 implementation files were not used; Run-01's report was read as comparative evidence only.

## L1 identity (unchanged)

Levels `0 Core → 1 Architecture → 2 Technology → 3 Project`, level-first rules, `Level:` headers; exactly four static slots — `architecture` (required frame, `clean-architecture`), `persistence` (required leaf, `ef-core`, provider `sqlserver`), `backend-testing` (required leaf, `nunit`), `frontend` (optional leaf, `angular`); contracts/manifests as maintainer metadata; the frame owns placement, leaves own technique; role vocabulary mediates frame/leaf interaction; `binds:` kept where executable frame integration needs it (persistence → frame); L-style stratified decisions; no `Kind:` taxonomy, no cross-level register, no flattening, no extra slots or dynamic discovery. The only structural addition is one frame facet, `architecture.enforcement` (Level 2 data), which moves package identifiers out of the Level 1 `architecture.check` data.

## D1–D15 disposition

| # | Defect | Repair | Evidence |
| --- | --- | --- | --- |
| D1 | Level 0/1 technology leakage | Neutral policy kept at its owner; concrete technique moved to Level 2: new **Platform bindings** table in `.claude/rules/2-technology/backend-libraries.md` (controllers mechanism + Minimal API rule, result/transport types, `ProblemDetails`/`ValidationProblemDetails`, `IExceptionHandler`, authentication handlers/Identity, Data Protection, `WebApplicationFactory<Program>`, `IHttpClientFactory`, `ILogger<T>`, `IConfiguration`/options). Rewritten owners: Core http-api (API-002, API-007, API-012), security (SEC-008, SEC-016), testing (TST-006), backend-code (RUN-005, RUN-013, RUN-022), frontend (FE-009); Architecture roles (API-001), frame boundaries (ARC-002, ARC-008, ARC-010, ARC-018), adopted-style, layout (Minimal API rule, composition code, test host). `scan-layers.md` (platform-specific search patterns, owns no policy) reclassified 0 → 2; `security-scan` and `build-fix` examples neutralized (`frontend.commands` gained a toolchain row). Package IDs moved from Level 1 `check.json` to `architecture.enforcement`. The fixed platform vocabulary itself is unchanged (.NET, C#, ASP.NET Core, NuGet, HTTP, Git) and now stated precisely in the map and `template-maintenance`. | Refined checker rejects all 8 baseline Level 0/1 terms when the baseline rule texts are restored (one-time demonstration); manual re-scan of every Level 0/1 artifact shows only platform names, `dotnet`/`git` CLIs, .NET project files, base-runtime types, role/frame vocabulary, skill names, template tooling |
| D2 | Neutrality checker was a partial deny-list | Layered, data-driven neutrality: (1) fail-closed allow-list for code identifiers and API-shaped prose in non-frame Level 0/1; (2) lexicon harvested from the template's own Level 2 binding sections, package tables, enforcement data, and module leak-tokens; (3) "ASP.NET Core <Feature>" rule; (4) generic non-slot technology list; (5) Level 0/1 JSON data may hold no package IDs | 9 leak fixtures fail (incl. `IHostedService`, named in no list, rejected by the fail-closed layer); platform/stable-role vocabulary fixture passes; baseline checker reports PASS on the unrepaired baseline (demonstrated once) |
| D3 | CWD-fragile launchers | Exec form everywhere: `"command": "node"`, `"args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.mjs"]` | Baseline shell form fails from a nested cwd (`MODULE_NOT_FOUND`, demonstrated once); exec form starts from root, nested backend/frontend, linked worktree, nested worktree cwd, paths with spaces |
| D4 | Launcher root vs active root conflated | `lib/project.mjs`: launcher root from script location; active root from hook `cwd` (or the edited file) via Git + instruction marker; policy data from the active root when present; per-worktree hook state in the worktree's own Git directory | Worktree-only invalid manifest reported with the worktree path while main stays quiet; main change does not affect the worktree; main working tree unmodified; state never in any working tree; Stop and architecture checks inspect the worktree |
| D5 | Critical PreToolUse could fail open | `onFailure: "block"` on the dependency guard; the script itself denies on empty/malformed/odd-encoded input, missing `tool_input.command`, missing configuration, and internal errors; post/Stop hooks stay non-blocking (checker enforces both) | Missing script, crashing script, and timeout → block (controlled exec-form runner with documented semantics); control without the flag fails open; 6 malformed-input cases deny |
| D6 | npm/pnpm/yarn global options and force flags bypassed routing | Quote-aware tokenizer; global options with values (`--prefix`, `-C`, `--workspace`, `-w`, `--dir`, `--filter`, `-F`, `--cwd`, …), `yarn workspace`, `npm pkg set`, `npm audit fix`, nested `bash -c`/`powershell -Command`/`cmd /c`, `npx`/`npm exec`; `--force`, `-f`, `--legacy-peer-deps`, `npm config set legacy-peer-deps` → ask; module CLI commands (`ng add/update`) read from `frontend.enforcement` | 77-row table (+1 check that module CLI commands come only from module data): all positives routed, all restore-only/unrelated negatives (`npm ci`, `npm install`, `dotnet restore`, `git add package.json`, quoted `echo`, …) quiet |
| D7 | `dotnet add/remove … reference` bypassed PreToolUse | Project-reference changes (incl. `dotnet reference add/remove`) denied once with a pointer to decision control / `project-structure` / `architecture-decision`; post-change architecture check validates the resulting graph | Reference cases routed (Bash and PowerShell); `dotnet reference list`, `dotnet sln add` quiet; architecture violations detected from actual state |
| D8 | Post-change shell validation relied on command text | `post-change-checks.mjs` (renamed from `post-edit-checks.mjs`) registered for `PostToolUse` Bash/PowerShell: per-worktree snapshot (HEAD + content hash of tracked/untracked, non-ignored manifests) compared with the previous one; only changed artifacts are validated | Unrecognized `node -e` and PowerShell `Set-Content` mutations detected; unchanged state after a report stays quiet |
| D9 | Failed shell calls with side effects | Same validation registered for `PostToolUseFailure` Bash/PowerShell; message marks the failed call; never blocks | Failed Bash and failed PowerShell partial mutations detected; failed call without relevant change quiet |
| D10 | HEAD transitions, rewrites, deletions, moves | Snapshot holds HEAD and hashes; first observation validates every manifest once; deletions reported only if the file is gone; moves = removed + added with equal hash; skipped dirs (`node_modules`, build output, dot-dirs, nested repos/worktrees) never listed | Fresh state + first HEAD transition to an invalid committed manifest (clean worktree) detected; later HEAD transition named; same-path rewrite, deletion, `git mv` reported; `node_modules` and newly ignored paths cause no false removals; HEAD change without manifest change quiet |
| D11 | Checker froze shell-form serialization | Checker validates `command`/`args` exec form, placeholder as data only, script existence, timeouts, required events/matchers, `onFailure: "block"` on the critical guard, no blocking post/Stop hooks, and the `PostToolUseFailure` registration | Fixtures: missing `onFailure`, missing `PostToolUseFailure`, shell-form command, blocking post hook all rejected; baseline checker rejects the correct exec-form settings (demonstrated once) |
| D12 | Root-relative manual commands | One form everywhere: `node "$(git rev-parse --show-toplevel)/.claude/scripts/<check>.mjs"`; scripts check the project containing the current directory | Bash and Windows PowerShell 5.1 from nested main and worktree directories check the right checkout |
| D13 | Windows encoding robustness | `decodeText`: UTF-8 (± BOM), BOM-tagged UTF-16LE/BE; deterministic errors for odd-length UTF-16, invalid UTF-8, BOM-less UTF-16; used for hook stdin and every manifest/project reader | UTF-8 BOM and UTF-16LE stdin routed; UTF-8 BOM/UTF-16LE/UTF-16BE project files and PowerShell 5.1 `Out-File` package.json validated; malformed files reported without crashing; architecture checker reads UTF-16 |
| D14 | Stop dedupe by path set | Material fingerprint = reminder set + HEAD + content hash of every triggering file, stored per worktree; `stop_hook_active` exits | remind → loop guard → unchanged silent → unrelated change silent → same-file change reminds → silent; identical change in worktree B still reminds |
| D15 | Capability invariants unproven | Checker: exactly four slot dirs and selection rows with the right requirement, contract titles (frame vs leaf), static composition, every module-dir file is a listed facet, contract facets provided at the contracted level, facet Level/Capability/Facet and JSON `$comment` consistency, leaf facets Level ≥ 2 and frame rule facets Level 1, frame `frame-terms:` ⇒ leaf `binds:` required, leak check incl. skill descriptions, module-directory paths, and hook/script code | 11 capability fixtures + removed-`binds:` fixture rejected; documented 6-step frontend removal → checker PASS, zero Angular references anywhere, routing still works |

## Reviews

**D16 — V2 fidelity (source-based).** All 41 files of `source/v2-baseline/` were read. The baseline preserved V2 semantics well; key-term recall is unchanged (658/703 terms, no section lower), i.e. neutralized terms moved into bindings rather than disappearing. Restored as useful technique: Serilog request-log diagnostic-context enrichment and process enrichers (`logging/references/serilog.md`), EF Core single-context concurrency (no fire-and-forget or parallel queries on one `DbContext`) (`ef-core`), the V2 testing decision guide (`dotnet-testing`), and V2's implementation-layer validation clause (`backend-libraries.md`). Intentionally not restored: lists that would restate rules already owned elsewhere (EF Core anti-patterns that repeat access/seeding rules, the reviewer's list of non-adopted pattern names — it would put technology names into Level 0), verbose duplicate examples.

**D17 — efficiency.** One demonstrably redundant always-loaded clause removed (`decisions.md` restated that changing a capability selection is Reserved; `CLAUDE.md` § Decision control owns it). No policy moved between trigger classes; no routing removed.

## Files and size

- Added (2): `.claude/capabilities/architecture/clean-architecture/enforcement.json`, `.claude/hooks/post-change-checks.mjs`.
- Removed (1): `.claude/hooks/post-edit-checks.mjs` (superseded by `post-change-checks.mjs`).
- Changed (39): `settings.json`; hooks `pre-bash-dependency.mjs`, `stop-cochange.mjs`; scripts `check-architecture.mjs`, `check-instructions.mjs`, `lib/project.mjs`; `manifest-policy.json`; frame `check.json`, `MODULE.md`, `CONTRACT.md`, `layout.md`; frontend `CONTRACT.md`, `MODULE.md`, `commands.md`, `enforcement.json`; Core rules (backend-code, frontend, http-api, security, testing); Architecture rules (roles, adopted-style, boundaries); `backend-libraries.md`; `decisions.md`, `package-management.md`; skills add-dependency, architecture-decision, build-fix, code-review, dotnet-testing, ef-core, project-structure, security-scan (+ `scan-layers.md`), template-maintenance, verify, `logging/references/serilog.md`; `INSTRUCTION_MAP.md`.

| Measure | Baseline | Refined |
| --- | ---: | ---: |
| Runtime files | 85 | 86 |
| Runtime bytes | 298,925 | 356,681 |
| Hook/script code bytes | 41,894 | 88,525 |
| Instruction Markdown bytes | 246,127 | 255,937 |
| Always-loaded chars (CLAUDE.md + imports + skill/agent listings) | 20,626 | 20,595 |
| Always-loaded tokens (chars/4) | ≈ 5,157 | ≈ 5,149 |

Complexity growth is confined to deterministic enforcement (actual-state snapshots, exec-form/fail-closed hooks, the stronger checker) required by D2–D15; the always-loaded surface did not grow. (The provenance file's 20,341-char estimate uses a slightly different counting method; both trees above use the same method.)

## Behavioral matrix summary (harness, controlled process-level execution)

Hooks were executed from the generated `settings.json` by an emulator of the documented host semantics (exec form, `${CLAUDE_PROJECT_DIR}` substituted as data, stdin input, per-hook timeout, `onFailure`), in Git sandboxes under `output/.work/` whose path contains spaces, with Git discovery capped at `output/` and no global/system Git configuration. The live Desktop session was not relocated.

- **Launch/root/worktree (29):** exec form from root, nested backend, nested frontend, linked worktree (`feature tree`), nested worktree cwd, worktree nested inside the main checkout; per-worktree deny-once state; reference routing via the PowerShell matcher; worktree vs main isolation for manifests, architecture, Stop; manual checks via Bash and PowerShell.
- **Input/encoding (25):** normal, UTF-8 BOM, UTF-16LE stdin; empty/whitespace/malformed/array/missing-command/odd-UTF-16 input denied; exact `command`/`args` shape; only PreToolUse blocks on failure; missing/crash/timeout blocked; manifest encodings as listed under D13.
- **Dependency/reference routing (78):** 77-row table under D6/D7 plus the module-data check.
- **Shell actual state (21):** under D8–D10, plus Edit/Write validation that refreshes the snapshot, product-source reminder, Windows path-casing reuse of the snapshot.
- **Stop (10):** under D14, plus satisfied co-changes silent and a non-blocking explanation outside Git.
- **Level/capability structure (32), bounded negative fixtures (13 = the 8 dossier fixtures + 2 hook-serialization fixtures + 3 one-time baseline demonstrations), frontend removal (4).**

## Level 0/1 neutrality and stability direction

Neutrality: checker PASS on the template; leak fixtures for a binding identifier, a framework type in prose, a named framework feature, persistence/frontend/testing implementations, an unlisted API, frame technique, and a package ID in Level 1 data all fail; platform vocabulary passes. Direction: rules and `CLAUDE.md` may reference less stable artifacts only through labeled routing pointers (imports are loading); reverse-dependency fixture fails, same-or-more-stable and labeled routing fixtures pass; rule path vs header level, `Kind:` rejection, and decision stratification (`Decided:` only in the frame style facet and Level 3 rules; no register) are enforced.

## Primary audit and confirmation audit

**Primary audit** (all 15 required areas) passed after repairing: (1) a Windows robustness defect — the shell snapshot compared its stored root case-sensitively, so a differently cased `cwd` resolved through the marker walk-up would repeat the initial validation on every call; (2) the frontend contract and map did not describe the new `dependencyCommands` data; (3) a harness coverage gap (worktree nested inside the main checkout). During construction the checker also caught the frame manifest description lacking its leak token and an Angular CLI cue (`ng add`) in the always-loaded `add-dependency` description; both were fixed.

**Cumulative confirmation audit** (complete rerun of all gates plus a manual review of every changed owner text against its normalized policy and new Level 2 binding): 212/212 matrix checks, checker PASS, 196/196 owners with 0 owner regressions, 0 trigger deltas, 0 scope misses, 0 duplicates, 0 broken references, hygiene 0 findings, V2 recall unchanged, always-loaded flat. **0 concrete template defects.**

## Workspace events (directly observed)

- Experimental isolation violations: 0 (no network, sibling, or excluded material; no Run-01 template).
- Recoverable workspace-process incidents (remediated): one shell redirect accidentally targeted an outside path (`/tmp/../dev/null`); it failed and wrote nothing. The shell's working directory twice drifted into `output/template/` after a `cd`; it was returned to the workspace root immediately and later commands used absolute paths.
- Platform-managed persistence events: three oversized command outputs were saved by the tool runtime outside the workspace; they were not opened and the content was re-read from workspace files. Claude Desktop auto-discovered the skills under `output/template/` and `source/v2-baseline/`; they were not invoked.

## Why this is strictly better than the baseline

The baseline passed its own checker while violating L1's core rule (concrete ASP.NET Core APIs and features in Core/Architecture), its hooks failed to start after a normal `cd`, conflated the launcher with the active worktree, could fail open, missed global-option and project-reference commands, ignored shell-driven and failed-call manifest mutations, and deduplicated Stop reminders by path only. The refined template removes every one of those failures with behavioral evidence, makes the checker prove L1's actual properties (neutrality, direction, four static slots, frame/leaf separation, `binds:`, exec-form fail-closed hooks), and does so with zero owner, trigger, scope, or reference regressions, unchanged V2 fidelity, and an unchanged always-loaded surface. No previously passing property regressed.

## Corrective pass — iteration 2

Iteration 2 continued in place from the iteration-1 `output/template/` (start tree hash `7d52dd42…`, 86 files). It did not recreate the template from the baseline. At the start, a file-hash inventory of that tree was recorded as the no-regression reference. The temporary harness under `output/.work/` was written new for this pass; nothing was recovered from iteration-1 material. It was deleted after this section was written.

### Independent residual findings

- **D1 (residual): Level 0/1 still carried controller technique.** The Level 1 frame named controllers and a `Controllers/` folder as the Api mechanism: the adopted-architecture role row, the Api section of the boundary rules, and the clean-architecture layout tree and prose. A Level 0 workflow cue read "New controller endpoint", and the maintainer map described "controller responsibilities".
- **D2 (residual): the checker had blind spots.** The neutrality checker matched only harvested binding tokens and API shapes. Plain technology nouns and phrases in Level 0/1 prose (Controllers, Identity, Data Protection, Kestrel, …) passed, so the checker reported PASS while D1 existed.

### Exact files changed (7)

| File | Change |
| --- | --- |
| `.claude/rules/1-architecture/frame/adopted-style.md` | Api role row is now "entry point and composition root (`Program.cs`)" → `backend/<Name>.Api` |
| `.claude/rules/1-architecture/frame/boundaries.md` | Api section restated in entry-point terms, keeping each rule (see below); it ends with a binding pointer to the platform bindings |
| `.claude/capabilities/architecture/clean-architecture/layout.md` | tree line `Controllers/` → `<entry points>/` (its folder and type conventions come from the platform bindings); prose points to the bindings |
| `.claude/skills/security-scan/SKILL.md` | cue "New controller endpoint" → "New API endpoint" |
| `.claude/rules/2-technology/backend-libraries.md` | new platform-binding row that receives the moved technique (see below) |
| `.claude/INSTRUCTION_MAP.md` | locator wording "entry-point responsibilities" |
| `.claude/scripts/check-instructions.mjs` | strengthened neutrality checker (design below) |

### How each Level 0/1 leak was neutralized without losing semantics

- **Api mechanism (adopted-style, boundaries, layout).** "Controllers" became "entry point / entry-point code". Every rule is kept at Level 1, unchanged in meaning:
  - Api is the default HTTP entry point (ARC-010).
  - Entry-point code stays thin: it binds and validates HTTP input, invokes Application services, and translates outcomes into HTTP responses.
  - Entry-point code contains no business logic, no persistence-context or concrete-repository access, and no manual construction of infrastructure services (ARC-011).
  - `Program.cs` is the composition root (ARC-012), and registration stays near the owning layer (ARC-023).
- **Controller technique moved to Level 2.** The technique lives in one binding row in `backend-libraries.md` § Platform bindings: ASP.NET Core controllers (`ControllerBase` with `[ApiController]`) in the Api project's `Controllers/` folder, with no Minimal API endpoint groups unless requested. The approved-stack decision "ASP.NET Core Controllers" stays at Level 3 in `decisions.md`. The controller-only default therefore keeps its force, now at the level that owns technique.
- **Security cue (Level 0 skill).** "New API endpoint" keeps the same review trigger (access control, input handling, HTTP security) without naming a mechanism. WF-020 and WF-021 are unchanged.
- **Kept on purpose:**
  - The fixed platform vocabulary is unchanged.
  - No controller term was added to frame-terms or to any allow-list.
  - The Level 2/3 mentions stay (binding rows, decisions, technique skills); that is where technique belongs.
- **Owners re-checked:** ARC-010 and ARC-011 (new phrases in `boundaries.md`), WF-020 and WF-021 (`security-scan`). Owner file, trigger, and scope are unchanged for all four.

### Checker design changes

1. **Binding-prose harvesting.** Besides binding tokens, packages, and leak tokens, the lexicon now harvests terms from the `## Platform bindings` / `## Bindings` cells: "ASP.NET Core <feature>" heads, and mid-sentence capitalized product runs, including acronym-led names. Stable methodology words, the fixed base vocabulary, and frame-terms are excluded.
2. **Whole-word matching for every term.** Matching is plural- and case-aware, and covers Level 0/1 Markdown and the Level 1 JSON facets. The frame is exempt only for its own frame-terms and tokens.
3. **Platform-follower rule.** "ASP.NET Core X" at Level 0/1 fails unless X is a generic follower (backend, application, project, code, version, …).
4. **Fail-closed capitalized-term layer.** At Level 0/1, any mid-sentence Title-case word or known technology acronym (EF, MVC, WPF, …) fails. The exceptions are stable methodology phrases and words (Unit of Work, Application Services, OWASP category names, level names, …) and, only in frame-owned artifacts, the frame's own words.
5. **Extended fixed technology-name list:** Controller/Controllers, Kestrel, Identity, Data Protection, Razor Pages, Web API, Hangfire, Quartz.NET, Orleans, Dapr.
6. **No legalizing.** The checker fails if its own allow-lists or any frame's frame-terms contain technology vocabulary, so a leak cannot be hidden by broadening vocabulary or frame-terms.

The existing API-shape, leak-token, `binds:`, slot, level, direction, and reference checks are unchanged.

### Positive/negative fixture results

The iteration-2 harness ended at **97/97**. It ran the strengthened checker against throwaway copies of the template.

- **Negative fixtures.** Each must FAIL, and did. Injected into Level 0/1:
  - Controllers/controller and ASP.NET Core Identity/Identity
  - Data Protection and Kestrel
  - WebApplicationFactory and DbContext
  - ControllerBase/`[ApiController]` and Minimal APIs
  - a restored `Controllers/` layout line
  - plural and case variants
  - attempts to legalize a term through frame-terms or the allow-lists
  - removal of the binding row or the binding pointer
- **Positive fixtures.** Each must PASS, and did:
  - the final template
  - stable-role and methodology wording (Application Services, Unit of Work, Decision Request fields, OWASP categories)
  - frame vocabulary inside frame-owned artifacts
  - the technique at Level 2/3
  - D12 regression cases
- **Syntax:** all scripts pass `node --check`.

**Development regression.** One development run reached 86/97. The causes were checker false positives on stable words and on a code comment that tripped the tooling leak rule. Both were fixed in the checker, after which the harness passed 97/97. That fix was the last template change: the tree hash has been `cebb0e61…` ever since, and it matches the confirmation below.

### D3–D17 preservation

- **7 of 86 files changed** compared with the start inventory, all listed above; the other 79 files are byte-identical.
- **D3–D14 runtime surface.** The 12 enforcement files are byte-identical to the iteration-1 accepted state:
  - the 3 hooks
  - `hooks/manifest-policy.json`
  - `settings.json`
  - `scripts/lib/project.mjs`
  - `scripts/check-architecture.mjs`
  - the 5 capability JSON facets

  As the task's efficient regression strategy allows, byte identity plus the iteration-1 evidence (212/212) carries D3–D14 forward. The shell/worktree matrix was not rebuilt.
- **D15 revalidated directly** by the strengthened checker: four static slots, frame/leaf levels, leak tokens, `binds:`, and the optional frontend. Result: PASS.
- **D16 V2 fidelity.** The full owner/trigger/scope audit below shows 0 deltas.
- **D17 efficiency.** The always-loaded surface shrank slightly. The only new logic is in the checker.

### Cumulative metrics

| Metric | Iteration-1 accepted | After iteration 2 |
| --- | --- | --- |
| Policies/invariants represented | 196/196 (194 + GOV-017/GOV-018) | 196/196 (194 + GOV-017/GOV-018) |
| Owner regressions | 0 | **0** |
| `trigger_class` deltas | 0 | **0** |
| Minimum-scope misses | 0 | **0** |
| Broken references | 0 | **0** |
| Runtime files | 86 | **86** |
| Template bytes | 356,681 | 365,140 |
| Always-loaded estimate | 20,595 chars (≈5,149 tokens) | **20,581 chars (≈5,145 tokens)** |
| Level 0/1 technology leaks | residual D1 (controller technique) | **0** |

The byte growth is in the checker (`check-instructions.mjs`). The instruction-text edits are small rewordings plus one binding row.

### Cumulative confirmation audit and final state

One cumulative confirmation audit ran after all repairs and before this section was written. It was a single script, deleted afterwards. An earlier draft of this section had been written before that audit; it was removed so that the audit precedes the report text. After the audit, only this report changed; the template was not edited. Results:

- **Tree identity:** 86 files, hash `cebb0e61…`, identical to the fixture-tested tree.
- **Syntax:** every `.mjs` passes `node --check`.
- **Strengthened instruction checker:** PASS (67 artifacts, 0 violations, 0 warnings). It covers:
  - D1 neutrality
  - level assignment and stability direction
  - the D15 slot, frame/leaf, leak, `binds:`, and optional-frontend checks
  - CLAUDE.md imports and internal path, skill, and agent references
- **Architecture checker:** exit 0.
- **Level 0/1 residual scan:** 0 hits. Terms scanned: Controller(s), Kestrel, Minimal API, ASP.NET Core Identity, Data Protection, DbContext, ApiController, WebApplicationFactory.
- **Full policy audit (194 inventory policies + GOV-017/GOV-018):** 196/196 owners found by phrase in their owner files, with 0 trigger deltas, 0 minimum-scope misses, and 0 duplicates.
- **Standalone/research/language hygiene:** 0 findings.
- **Always-loaded:** 20,581 chars (≈5,145 tokens).

**Result: CLEAN — 0 concrete template defects.**

Final tree hash: `cebb0e61796e50583c8db5c0ec1bfc3dec5d32ce3ede0dc025ade398306a6966` (86 files). It is the sha256 of the sorted per-file sha256 list, with `./path` names.

**Final status: STRICTLY_BETTER.** Iteration 2 keeps every iteration-1 pass and fully repairs residual D1 and D2, with no regressions.

## Corrective pass — iteration 3

Iteration 3 continued in place from the iteration-2 `output/template/`. Its start tree hash was `cebb0e61796e50583c8db5c0ec1bfc3dec5d32ce3ede0dc025ade398306a6966` (86 files), the iteration-2 final state; nothing was recopied from the baseline. A per-file hash inventory of that tree was recorded at the start and used as the byte-identity reference. One new harness under `output/.work/` held the fixture suite and the confirmation script. It was deleted after this section was written.

### Independent residual findings

- **A — technology enforcement was case-sensitive.**
  - `Use Kestrel for hosting.` failed while `Use kestrel for hosting.` passed.
  - Lowercase forms likewise bypassed the neutrality and implementation-leak checks: serilog, redis, dapper, nunit, angular, ef core, docker, hangfire, orleans, dapr.
  - A lowercase technology term could also be placed in `frame-terms` and so become legal.
- **B — frame-owned Level 1 artifacts skipped fail-closed API-shape detection.** The check ran only for non-frame artifacts (`if (!isFrame)`). `Use IHostedService here.` therefore failed in a Level 0 rule but passed in `.claude/rules/1-architecture/frame/boundaries.md`.

### Exact files changed (3)

| File | Change |
| --- | --- |
| `.claude/scripts/check-instructions.mjs` | case-robust term and identity matching, frame-inclusive fail-closed API-shape detection, structural routing-pointer recognition, new self-consistency checks |
| `.claude/capabilities/architecture/clean-architecture/MODULE.md` | new `- placement-examples:` line listing the 15 illustrative project-owned names the layout facet already uses, plus one replacement-notes sentence (maintainer metadata, never auto-loaded) |
| `.claude/capabilities/architecture/CONTRACT.md` | one sentence telling a replacement frame to declare `placement-examples:` (maintainer metadata, never auto-loaded) |

No instruction file that the agent loads changed. The iteration-2 D1 files are byte-identical: `adopted-style.md`, `boundaries.md`, `layout.md`, `backend-libraries.md`, `security-scan`, and `INSTRUCTION_MAP.md`.

### How case-robust matching was implemented

The case rule is decided once, where the term list is built. It does not use spelling variants.

- **Names match case-insensitively.** This covers every technology, product, package, and implementation name:
  - the fixed technology names
  - module leak tokens and each module's implementation name
  - names harvested from Level 2 binding prose
  - package identifiers from enforcement data
- **Case is significant in only two bounded situations**, where the spelling itself carries the meaning:
  - Single-word code identifiers harvested from binding code spans, such as `Include`. C# identifiers are case-sensitive, and the lowercase form is ordinary prose. Compound identifiers (`ControllerBase`, `WebApplicationFactory`) still match in any case.
  - `COMMON_WORD_NAMES` = {`Identity`}. Lowercase "identity" is ordinary vocabulary ("external identity" in the Reserved list). The capitalized product name still fails anywhere, including at the start of a sentence. "ASP.NET Core identity" fails in any case through the platform-follower rule, which now matches case-insensitively.
- **No legalizing.** The checker fails if:
  - an allow-list entry, a `frame-terms` entry, or a `placement-examples` entry is technology vocabulary in any case;
  - a `COMMON_WORD_NAMES` entry is the identity of any selected module, so selected implementations can never become case-sensitive.

### How frame-owned fail-closed API detection was restored

- The `if (!isFrame)` exemption is removed. Every Level 0/1 artifact, frame-owned ones included, runs API-shape detection on code spans and prose: interfaces, compound PascalCase types, attributes, generic types, method calls, and dotted identifiers.
- A frame artifact may additionally use only the identifiers its manifest declares explicitly:
  - `frame-terms`, which is unchanged, so `binds:` detection is unchanged;
  - the new `placement-examples` list. It names the illustrative project-owned folders, the registration file, and the example types that the layout facet already shows (`ExternalServices/`, `DependencyInjection`, `ITaskService`, `IEmailSender`, `TaskWorkflowRules`, …).
- Both lists are self-checked against technology vocabulary. No implementation API was added to frame vocabulary.
- `IHostedService`, `ControllerBase`, `DbContext`, and `WebApplicationFactory<Program>` now fail in `boundaries.md`, `layout.md`, and `adopted-style.md`.

### How routing pointers are distinguished from normative use

Pointer recognition is structural and does not depend on capitalization. A routing pointer is a `Technique:` label (any case) or a `→` route, followed directly by a list of skill-name code spans that resolve to an existing Level 2+ skill. Only those listed skill names are removed before the neutrality checks; everything else on the line is still checked. As a result:

- **PASS:** `Technique: \`docker\``, `Technique: \`swagger\``, and the template's existing "(technique: `ci-cd`, `docker`)" and "containers/CI → `docker` / `ci-cd`".
- **FAIL:**
  - `Use docker for deployment.` and `Use swagger here.`
  - `` Use `docker` for deployment. `` (code span, but no routing marker)
  - `Technique: use docker for deployment.` (label, but prose instead of a skill list)

### How implementation-name leakage became case-robust

- **A module's identity is its leak tokens plus its implementation name.** Matching is case-insensitive, with space and hyphen spellings treated as equal. So "EF Core", "ef core", and "ef-core" are one name, as are "Clean Architecture", "clean architecture", "clean-architecture", and "Clean-Architecture".
- **The same identity rule applies to hook and script code.**
- **One sanctioned cross-reference:** the capability id in a leaf manifest's own `binds:` declaration. Ownership, `binds:`, and slot rules are otherwise unchanged.
- **Effect:** lowercase `nunit`, `angular`, `ef core`, and `clean-architecture` now fail outside their owning module, both in a Level 2 non-owner rule and in Level 0.

### Fixture results (one bounded suite, final run 118/118)

| Group | Result | Content |
| --- | --- | --- |
| A case-robust technology | 32/32 FAIL as required | required 1–9 plus `Use swagger here.`, each in a Level 0 rule, a non-frame Level 1 rule, and a frame Level 1 rule; `` Use `docker` for deployment. ``; `Technique: use docker for deployment.` |
| B frame API-shape | 9/9 FAIL as required | required 10–13 in `boundaries.md` and `layout.md`; `IHostedService` in `adopted-style.md`. Each asserts the fail-closed API-shape violation itself |
| C no legalizing | 8/8 FAIL as required | lowercase kestrel/serilog/docker/ef core in `frame-terms`; kestrel in `frame-terms` plus frame use; redis in `placement-examples`; kestrel in the checker allow-list; Angular in `COMMON_WORD_NAMES` |
| D implementation identity | 10/10 FAIL as required | lowercase nunit/angular/ef core/clean-architecture in a Level 2 non-owner rule and in Level 0; `Clean-Architecture` and `clean architecture` |
| E iteration-2 neutrality | 22/22 FAIL as required | Controllers, Identity (sentence-initial), ASP.NET Core Identity, Data Protection, Kestrel, `WebApplicationFactory<Program>`, `DbContext`, `ControllerBase`, `[ApiController]`, Minimal APIs, each in Level 0 and the frame; restored `Controllers/` layout line; restored `entry point (controllers)` |
| F required PASS | 14/14 PASS | the clean iteration-2 template with its four-slot composition asserted; `Technique: \`docker\`` and `Technique: \`swagger\`` in Level 0, Level 1, and the frame; entry point/composition root/Domain/Application/Infrastructure/Api in frame artifacts; fixed-platform vocabulary in Level 0 and Level 1; stable methodology wording; ordinary "external identity"; the documented optional-frontend-disabled form |
| G stability direction | 5/5 | unlabeled Level 0 → Level 2 rule, Level 1 → Level 3 rule, and Level 0 → Level 2 facet FAIL; header/directory level mismatch FAILs; a labeled pointer PASSes |
| H capability | 8/8 FAIL as required | extra slot; unselected implementation present; leaf uses frame terms with `binds: none`; `binds:` to another frame; missing `binds:`; leaf facet at Level 1; a capitalized leak token in another module; incomplete frontend removal |
| I D11/D12 (checker file changed) | 4/4 | checker run from two subdirectories PASSes; a shell-string hook and a critical PreToolUse without `onFailure: block` FAIL |
| J syntax | 6/6 | `node --check` on every script |

During development the suite ran 118/118 on its first run. Two maintainer-text alignments followed: the contract sentence, and a checker comment and message. After them the suite was rerun at 118/118; those were the last template changes.

### D1 and D3–D17

- **D1:** content is unchanged in meaning; its six files are byte-identical to the iteration-2 accepted state. With the stronger checker, the Level 0/1 residual scan (case-insensitive) finds 0 hits.
- **D2:** the checker now also covers both residual gaps (A and B).
- **D3–D14:** the 12 enforcement files are byte-identical to the iteration-3 start inventory, so the iteration-1 behavioral evidence carries forward and the shell/worktree matrix was not rebuilt:
  - the 3 hooks
  - `hooks/manifest-policy.json`
  - `settings.json`
  - `scripts/lib/project.mjs`
  - `scripts/check-architecture.mjs`
  - the 5 capability JSON facets

  D11 and D12 were rerun directly (group I) because the checker file changed.
- **D15:** revalidated by groups C, F, and H: four static slots, frame/leaf levels, leak tokens, `binds:`, and optional-frontend removal.
- **D16:** owner/trigger/scope fidelity is unchanged (audit below).
- **D17:** the always-loaded surface is unchanged.

### Cumulative metrics

| Metric | Iteration-2 accepted | After iteration 3 |
| --- | --- | --- |
| Policies/invariants represented | 196/196 (194 + GOV-017/GOV-018) | **196/196** |
| Owner regressions | 0 | **0** |
| `trigger_class` deltas | 0 | **0** |
| Minimum-scope misses | 0 | **0** |
| Broken references | 0 | **0** |
| Runtime files | 86 | **86** |
| Template bytes | 365,140 | 369,568 |
| Always-loaded estimate | 20,581 chars (≈5,145 tokens) | **20,581 chars (≈5,145 tokens)** |

The added bytes are checker logic plus two maintainer-metadata lines; nothing loaded into agent context grew.

### Cumulative confirmation audit and final state

One cumulative confirmation audit ran over the final tree after all repairs and focused regressions, and before this section was written. After it, only this report changed. Results:

- **Identity:** 86 files. The only changes against the start inventory are the 3 files listed above; nothing was added or removed, and the 12 enforcement files are identical.
- **Syntax:** all scripts pass `node --check`.
- **Instruction checker:** PASS (67 artifacts, 0 violations, 0 warnings). This covers neutrality, levels and direction, slots, frame/leaf, leak tokens, `binds:`, imports, and internal path/skill/agent references (0 broken). The architecture checker exits 0.
- **Fixture suite:** 118/118.
- **Level 0/1 residual scan:** 0 hits.
- **Full policy audit:** 196/196 owners found, with 0 trigger deltas, 0 minimum-scope misses, and 0 duplicates.
- **Hygiene:** 0 standalone, research, or language findings.
- **Always-loaded:** 20,581 chars.

**Result: CLEAN — 0 concrete template defects.**

Final tree hash: `21c35a915b3a7547abd63d0e53e11e78666a83f5532488a5df7864c5ac1b5edf` (86 files; same method as before).

**Final status: STRICTLY_BETTER.** Iteration 3 closes both remaining checking blind spots while every iteration-1/2 result, metric, and content property stays unchanged.

## Corrective pass — iteration 4

Iteration 4 continued in place from the iteration-3 `output/template/`. Its start tree hash was `21c35a915b3a7547abd63d0e53e11e78666a83f5532488a5df7864c5ac1b5edf` (86 files), the iteration-3 final state; nothing was recopied from the baseline. A per-file hash inventory of that tree was recorded at the start as the byte-identity reference. One new harness under `output/.work/` held the fixture suite and the confirmation script. It was deleted after this section was written.

### Independently reproduced residual bypasses

- **A — a routing pointer could hide normative technology policy.** The iteration-3 recognizer masked the skill name as soon as a `Technique:` label or `→` was followed by skill code spans, without looking at the rest of the clause. These therefore passed:
  - `` Technique: `docker` must be used for deployment. ``
  - `` Technique: `docker` is required for deployment. ``
  - `` Container deployment → `docker` and it must be used. ``
- **B — frame allow-lists could legalize API-shaped identifiers.** `frame-terms` and `placement-examples` entries were rejected only if they appeared in the harvested technology lexicon. Adding `IHostedService` (absent from that lexicon) to either list legalized `Use IHostedService here.` in a frame-owned Level 1 artifact.

### Exact files changed (3)

| File | Change |
| --- | --- |
| `.claude/scripts/check-instructions.mjs` | whole-clause routing-pointer recognizer; frame vocabulary classes with positive validation; position-bound placement masking |
| `.claude/capabilities/architecture/CONTRACT.md` | the iteration-3 sentence on frame code identifiers restated as the two contract-defined classes (maintainer metadata, never auto-loaded) |
| `.claude/capabilities/architecture/clean-architecture/MODULE.md` | the replacement note now says placement examples are accepted only where the layout facet places them (maintainer metadata, never auto-loaded) |

No loaded instruction file changed. The iteration-3 frame vocabulary itself, the `frame-terms` and `placement-examples` lines, is byte-identical.

### A — routing-pointer recognition is now contextual

The recognizer first identifies the whole clause and proves it is a routing statement. Only then are the listed skill names masked. Accepted shapes:

- `[clause start] technique(s): <skill list> [skill(s)] [clause end]`
- `[clause start] <topic of one to three plain words> → <skill list> [clause end]`

Clause boundaries are fixed:

- **Clause start:** line start (after bullet or emphasis marks), `(`, `;`, `:`, or a sentence end.
- **Clause end:** `;`, `)`, a sentence end, or the line end.

The clause is a pointer only when all of the following hold:

1. Every listed name is a Level 2+ skill.
2. Nothing else stands between the list and the clause end, apart from an optional "skill(s)".
3. A label starts its clause.
4. An arrow's topic is one to three plain words.
5. A parenthesized pointer closes with `)`.
6. No normative wording appears in the topic, in a parenthesized pointer's lead-in, or in the rest of the line. The normative markers are a closed set: must, should, shall, require(d), mandatory, default, prefer(red), recommended, always, never, only, use(d), need(s), standard, approved, decided, replace(d).

Normative wording can therefore only disqualify a pointer; it never makes one, so the check fails closed. Any clause that fails a condition is checked unchanged, and the technology name stays visible to every neutrality layer. The template's existing pointers still qualify: "(technique: `ci-cd`, `docker`)" in `development-workflow` and "containers/CI → `docker` / `ci-cd`" in `code-review`.

### B — frame allow-lists cannot legalize implementation identifiers

Frame vocabulary is split into three classes. None of them is honored merely because the lexicon does not know an identifier, and the manifest is never its own evidence:

1. **Plain frame terms** (words and phrases such as Domain, Application, Infrastructure, Api, Application Services, entry point, composition root): prose vocabulary and `binds:` detection, as before.
2. **Frame code names** (API-shaped `frame-terms` entries): honored only when anchored by the frame's own facets. That means either `Add` plus a layer the style facet maps to a project (`AddApplication`, `AddInfrastructure`), or the code spelling of a multi-word phrase the frame facets state in plain prose: `IUnitOfWork` ↔ "Unit of Work", `IGenericRepository` ↔ "generic repository". An unanchored entry is a violation on the manifest and is not honored anywhere.
3. **Placement examples:** honored only at the positions where the layout facet places them, i.e.
   - inside its directory trees;
   - as folder paths (`ValueObjects/`);
   - as naming variants that extend a placed example with the facet's own words (`TaskWorkflowRules`).

   An entry that the facet does not place is a violation on the manifest. Listed names are masked only at those positions.

The manifest's own declaration lines are validated by these rules instead of being read as usage. Everywhere else, frame artifacts run the fail-closed API-shape check with only base vocabulary and anchored frame code names allowed. As a result, `IHostedService`, `ControllerBase`, `WebApplicationFactory`, `DbContext`, and the synthetic `IQuantumLedgerBroker` are rejected when inserted into either list, independent of the lexicon. The contract now states the two code-identifier classes explicitly.

### Fixture results (one bounded suite, final run 170/170)

| Group | Result | Content |
| --- | --- | --- |
| R1 routing pointer PASS | 10/10 | `` Technique: `docker`. `` and `` Technique: `swagger`. `` in Level 0, Level 1, and the frame; the clean template's existing pointers; `` Container or deployment change (technique: `docker`). ``; `` Containers → `docker`. ``; `` Technique: `docker`, `swagger` skills. `` |
| R2 routing-looking normative FAIL | 22/22 | `Use docker for deployment.`; `` Technique: `docker` `` + must be used / is required / should be used / is the default / is preferred / must not be replaced / `; it must be used`; `` Container deployment -> `docker` and it must be used. `` (ASCII and `→`); `swagger` must be used / is mandatory; normative lead-in `` Deployments must use containers (technique: `docker`). ``; normative topic `` Deployment must use → `docker`. ``; the four core cases also in non-frame Level 1 and the frame. Each asserts the Docker/Swagger neutrality violation |
| R3 allow-list legalizing FAIL | 22/22 | each of `IHostedService`, `ControllerBase`, `WebApplicationFactory`, `DbContext`, and the synthetic `IQuantumLedgerBroker`, inserted into `frame-terms` and into `placement-examples`, with `Use X here.` in `boundaries.md` and `` Use `X` here. `` in `layout.md`. Each asserts the structural metadata violation (unanchored / not placed), not a lexicon hit. Two more fixtures confirm the usage itself is also a violation in the artifact |
| R4 legitimate frame metadata PASS | 6/6 | "entry point" and "composition root" added to `frame-terms`; the clean frame terms and all 15 placement examples; entry point/composition root/Domain/Application/Infrastructure/Api in `boundaries.md` and `layout.md`; anchored frame code names (`IUnitOfWork`, `IGenericRepository<T>`, `AddApplication()`, `AddInfrastructure(configuration)`) in both |
| A3 case-robust technology (iteration 3) | 32/32 | required lowercase forms in Level 0, Level 1, and the frame; code-span and label-with-prose variants |
| B3 frame API-shape (iteration 3) | 9/9 | `IHostedService`, `ControllerBase`, `DbContext`, `WebApplicationFactory<Program>` in frame artifacts |
| C3 no legalizing (iteration 3) | 8/8 | lowercase technology in `frame-terms`/`placement-examples`; checker allow-list; `COMMON_WORD_NAMES` |
| D3 implementation identity (iteration 3) | 10/10 | lowercase nunit/angular/ef core/clean-architecture outside their modules, plus spelling variants |
| E2 iteration-2 neutrality | 22/22 | Controllers, Identity, ASP.NET Core Identity, Data Protection, Kestrel, `WebApplicationFactory<Program>`, `DbContext`, `ControllerBase`, `[ApiController]`, Minimal APIs in Level 0 and the frame; restored `Controllers/`; restored `entry point (controllers)` |
| F3 earlier PASS | 6/6 | four-slot composition; fixed-platform vocabulary in Level 0 and Level 1; stable methodology wording; ordinary "identity"; documented optional-frontend removal |
| G stability direction | 5/5 | unlabeled upward dependencies and level/directory mismatch FAIL; a labeled pointer PASSes |
| H capability | 8/8 | extra slot, unselected implementation, `binds:` missing/none/wrong frame, leaf facet at Level 1, cross-module leak token, incomplete frontend removal |
| I D11/D12 | 4/4 | checker from subdirectories PASSes; shell-string hook and non-blocking critical PreToolUse FAIL |
| J syntax | 6/6 | `node --check` on every script |

**Self-check (§8), answered mechanically:**
- **Can routing syntax plus normative wording still hide a technology token?** No; R2 is 22/22 FAIL.
- **Can an arbitrary API-shaped identifier become legal by adding it to `frame-terms` or `placement-examples`?** No; R3 is 22/22 FAIL, including the synthetic identifier.

The suite first ran 170/170. The contract and manifest sentence alignment followed, the suite was rerun at 170/170, and those were the last template changes.

### Iteration-3 semantics and D3–D17

- **Content and architecture:** L1 architecture and Level 0/1 content are unchanged; all loaded instruction files are byte-identical to the iteration-3 accepted state. Iteration-3 case-robust matching and implementation-identity checks are unchanged (groups A3, C3, D3).
- **D1/D2:** unchanged in meaning (E2, plus a 0-hit Level 0/1 residual scan).
- **D3–D14:** the 12 enforcement files are byte-identical to the iteration-4 start inventory, so the shell/worktree matrix was not rebuilt:
  - the 3 hooks
  - `hooks/manifest-policy.json`
  - `settings.json`
  - `scripts/lib/project.mjs`
  - `scripts/check-architecture.mjs`
  - the 5 capability JSON facets

  D11 and D12 were rerun because the checker file changed.
- **D15:** revalidated (F3, H, R4).
- **D16:** fidelity is unchanged (audit below).
- **D17:** the always-loaded surface is unchanged.

### Cumulative metrics

| Metric | Iteration-3 accepted | After iteration 4 |
| --- | --- | --- |
| Policies/invariants represented | 196/196 (194 + GOV-017/GOV-018) | **196/196** |
| Owner regressions | 0 | **0** |
| `trigger_class` deltas | 0 | **0** |
| Minimum-scope misses | 0 | **0** |
| Broken references | 0 | **0** |
| Runtime files | 86 | **86** |
| Template bytes | 369,568 | 376,521 |
| Always-loaded estimate | 20,581 chars (≈5,145 tokens) | **20,581 chars (≈5,145 tokens)** |

The added bytes are checker logic and two maintainer-metadata sentences; nothing loaded into agent context changed.

### Cumulative confirmation audit and final state

One cumulative confirmation audit ran over the final tree after all repairs and focused regressions, and before this section was written. After it, only this report changed. Results:

- **Identity:** 86 files. The only changes against the start inventory are the 3 files above; nothing was added or removed, and 12/12 enforcement files are identical.
- **Syntax:** all scripts pass.
- **Instruction checker:** PASS (67 artifacts, 0 violations, 0 warnings; 0 broken references). The architecture checker exits 0.
- **Fixture suite:** 170/170.
- **Level 0/1 residual scan:** 0 hits.
- **Policy audit:** 196/196 owners, with 0 trigger deltas, 0 minimum-scope misses, and 0 duplicates.
- **Hygiene:** 0 findings.
- **Always-loaded:** 20,581 chars.

**Result: CLEAN — 0 concrete template defects.**

Final tree hash: `38721f31fc0c65249c9b98691fa1f841b3a649c887ff87e8a4a3c072ce1d3aaa` (86 files; same method as before).

**Final status: STRICTLY_BETTER.** Iteration 4 closes the last two reproduced checker bypasses with structural rules, while every earlier result, metric, and content property stays unchanged.

## Corrective pass — iteration 5

Iteration 5 continued in place from the iteration-4 `output/template/`. Its start tree hash was `38721f31fc0c65249c9b98691fa1f841b3a649c887ff87e8a4a3c072ce1d3aaa` (86 files), the iteration-4 final state; nothing was recopied from the baseline. A per-file hash inventory of that tree was recorded at the start as the byte-identity reference. One new harness under `output/.work/` held the fixture suite and the confirmation script. It was deleted after this section was written.

### Reproduced bypass — normative lead-in before routing syntax

Iteration 4 rejected normative wording after a pointer (`` Technique: `docker` must be used ``). It still passed constructs whose normative meaning came before it:

- `` Required deployment technology: Technique: `docker`. ``
- `` Default deployment: Technique: `docker`. ``
- `` Required deployment: Containers -> `docker`. ``

The recognizer's clause start treated the preceding `:` (and `(`) as a new clause. So the governing label "Required deployment technology:" never entered the routing decision, and the skill name was masked.

### Exact files changed (1)

| File | Change |
| --- | --- |
| `.claude/scripts/check-instructions.mjs` | routing recognizer evaluates the governing lead-in together with the routing fragment; `->` accepted as the ASCII spelling of `→` |

No other file changed. The 85 other files, including all instruction content, contracts, manifests, hooks, settings, and capability data, are byte-identical to the iteration-4 start inventory.

### How the governing lead-in is now evaluated

The pointer grammar and the immediate-clause checks are unchanged:

- a label starts its clause, or an arrow has a one-to-three-word topic;
- only Level 2+ skill names are listed;
- nothing else stands before the clause end;
- a parenthesized pointer closes with `)`.

One structural notion is added: the **governing lead-in**. It is everything from the enclosing clause start (`;`, a sentence end, or the line start) up to the pointer. It deliberately spans `:` labels and the opening `(`, because those introduce, and so characterize, the pointer that follows.

Before anything is masked, both the lead-in and the rest of the line (the fragment's continuation) are tested against the existing closed `NORMATIVE` set: must, should, shall, require(d), mandatory, default, prefer(red), recommended, always, never, only, use(d), need(s), standard, approved, decided, replace(d). This replaces iteration 4's separate topic and parenthesis lead-in tests, which are subsumed by the new span. If either part carries normative force, nothing is masked and the technology name stays visible to every neutrality layer. The check fails closed, and no fixture strings are special-cased. Existing template pointers still qualify, because their lead-ins are neutral:

- "**CI/CD, container, or deployment change** (technique: `ci-cd`, `docker`)"
- "containers/CI → `docker` / `ci-cd`"

The iteration-5 PASS matrix requires `` Containers -> `docker`. `` to pass, so `->` is accepted as the ASCII spelling of the template's `→`. The same immediate-clause and lead-in rules apply to it, and the project-reference graph lines that use `->` are unaffected, because they list no skill code spans.

### Required routing fixtures

| Group | Result | Content |
| --- | --- | --- |
| P5 routing PASS | 14/14 | `` Technique: `docker`. ``, `` Technique: `swagger`. ``, and `` Containers -> `docker`. `` in Level 0, Level 1, and the frame; `` Containers → `docker`. ``; the clean template's existing pointers; neutral reference forms `` Container or deployment change (technique: `docker`). `` and `` Deployment: Technique: `docker`. ``; `` Technique: `docker`, `swagger` skills. `` |
| S5 normative suffix FAIL | 6/6 | `` Technique: `docker` `` + must be used / is required / should be used / is the default; `` Container deployment -> `docker` and it must be used. `` (ASCII and `→`) |
| N5 normative lead-in FAIL | 18/18 | Required deployment technology / Default deployment / Mandatory deployment mechanism / Preferred deployment technology + `` Technique: `docker`. ``; Required / Default / Mandatory deployment + `` Containers -> `docker`. ``, each in Level 0 and the frame; `` Required API documentation: Technique: `swagger`. ``; `` Preferred API documentation: API docs -> `swagger`. ``; parenthesized `` Required deployment (technique: `docker`). ``; emphasized label `` **Default:** Technique: `docker`. ``. Each asserts the Docker/Swagger neutrality violation |

Two forms listed only as examples in the task, `See technique: …` and `Implementation details: …`, are not routing syntax of this template. Per the task they were not added to the grammar, and they keep failing closed. The supported neutral forms above take their place.

### Regression results (same suite, final run 208/208)

| Group | Result |
| --- | --- |
| R1 iteration-4 routing PASS | 10/10 |
| R2 iteration-4 routing-looking normative FAIL | 22/22 |
| R3 iteration-4 allow-list legalizing FAIL (`IHostedService`, `ControllerBase`, `WebApplicationFactory`, `DbContext`, synthetic `IQuantumLedgerBroker` in `frame-terms`/`placement-examples`) | 22/22 |
| R4 iteration-4 legitimate frame metadata PASS | 6/6 |
| A3 iteration-3 case-robust technology | 32/32 |
| B3 iteration-3 frame API-shape | 9/9 |
| C3 iteration-3 no legalizing | 8/8 |
| D3 iteration-3 implementation identity | 10/10 |
| E2 iteration-2 neutrality | 22/22 |
| F3 earlier PASS (four-slot composition, fixed-platform vocabulary, stable wording, documented optional-frontend removal) | 6/6 |
| G stability direction | 5/5 |
| H capability leak / `binds:` / removal | 8/8 |
| I D11/D12 (checker file changed) | 4/4 |
| J syntax | 6/6 |

The suite ran 208/208 on its first run, and there was no later template change.

### Preservation of accepted behavior

- **Iteration-4 protections:** no-legalizing (R3, R4) is intact, and the frame vocabulary classes are untouched.
- **Iteration-3 enforcement:** case-robust matching (A3, C3, D3) and frame API fail-closed checking (B3) are intact.
- **D1:** content is byte-identical (E2; Level 0/1 residual scan 0 hits).
- **D3–D14:** the 12 enforcement/runtime files are byte-identical, so the shell/worktree matrix was not rebuilt:
  - the 3 hooks
  - `hooks/manifest-policy.json`
  - `settings.json`
  - `scripts/lib/project.mjs`
  - `scripts/check-architecture.mjs`
  - the 5 capability JSON facets

  D11 and D12 were rerun because the checker file changed.
- **D15:** revalidated (F3, H, R4).
- **D16:** fidelity is unchanged (audit below).
- **D17:** the always-loaded surface is unchanged.

### Cumulative metrics

| Metric | Iteration-4 accepted | After iteration 5 |
| --- | --- | --- |
| Policies/invariants represented | 196/196 (194 + GOV-017/GOV-018) | **196/196** |
| Owner regressions | 0 | **0** |
| `trigger_class` deltas | 0 | **0** |
| Minimum-scope misses | 0 | **0** |
| Broken references | 0 | **0** |
| Runtime files | 86 | **86** |
| Template bytes | 376,521 | 376,852 |
| Always-loaded estimate | 20,581 chars (≈5,145 tokens) | **20,581 chars (≈5,145 tokens)** |

### Cumulative confirmation audit and final state

One cumulative confirmation audit ran over the final tree after the repair and focused regressions, and before this section was written. After it, only this report changed. Results:

- **Identity:** 86 files. The only change against the start inventory is the checker; nothing was added or removed, and 12/12 enforcement files are identical.
- **Syntax:** all scripts pass.
- **Instruction checker:** PASS (67 artifacts, 0 violations, 0 warnings; 0 broken references). The architecture checker exits 0.
- **Fixture suite:** 208/208.
- **Level 0/1 residual scan:** 0 hits.
- **Policy audit:** 196/196 owners, with 0 trigger deltas, 0 minimum-scope misses, and 0 duplicates.
- **Hygiene:** 0 findings.
- **Always-loaded:** 20,581 chars.

**Result: CLEAN — 0 concrete template defects.**

Final tree hash: `da9e3771f749fa6ea189478f2235f4769627b73b7fee5fc692c709c4a9775a29` (86 files; same method as before).

**Final status: STRICTLY_BETTER.** Iteration 5 closes the normative-lead-in routing bypass structurally, while every earlier result, metric, and content property stays unchanged.

## Corrective pass — iteration 6

Iteration 6 continued in place from the iteration-5 `output/template/`. Its start tree hash was `da9e3771f749fa6ea189478f2235f4769627b73b7fee5fc692c709c4a9775a29` (86 files), the iteration-5 final state; nothing was recopied from the baseline. A per-file hash inventory of that tree was recorded at the start as the byte-identity reference. One new harness under `output/.work/` held the metamorphic suite, the regression families, and the confirmation script. It was deleted after this section was written.

### Why line-oriented patches were insufficient

Iterations 3–5 each fixed one counterexample, but the routing recognizer still reasoned about one physical line. The same semantic statement could therefore change classification just by being reformatted. For example, `` Required deployment technology: Technique: `docker`. `` failed on one line, but these passed:

- the lead-in on its own line followed by the pointer;
- the lead-in as a heading;
- the lead-in as a parent bullet;
- the pointer wrapped across lines.

The defect was the unit of analysis, not a missing pattern.

### The logical-Markdown abstraction

The checker now separates five steps:

1. **Lexical/technology detection:** unchanged; case-robust lexicon, identity, and API-shape layers.
2. **Logical-statement construction:** a bounded builder (`logicalStatements`), not a Markdown parser. It groups physical lines into statements and records governance edges.
3. **Pure-routing classification**, performed on `<governing chain>: <statement>`.
4. **Normative-force detection**, over the whole logical block: the governing chain, the governing lead-in, the rest of the statement, and the statement's governed content.
5. **Final neutrality decision:** only a pointer proven pure is masked, at its exact physical spans. Everything else is checked unchanged.

**Supported forms (exact and finite):**

1. a single line;
2. consecutive lines of one paragraph (soft-wrapped continuation);
3. a list item with its continuation lines (lazy or indented, including indented lines after a blank line);
4. a heading governing the next block, with or without a blank line between. This covers `#` headings and a block-starting line of emphasized text only, the pseudo-heading convention the template itself uses (`**Performance-motivated change**`);
5. a statement ending with `:` governing the next block (with or without a blank line), and a paragraph directly followed by a list governing that list;
6. a list item governing its nested items.

A "block" is the next paragraph, table, quote line, or list (all its top-level items). Governance chains compose: a heading over a lead-in over a list item.

**Boundary discipline:**
- Blank-line-separated paragraphs are never joined, and nothing is governed beyond these immediate relations.
- Fenced code is opaque and ends governance.
- Table rows and quote lines are single statements.
- `;` keeps separating independent clauses inside a statement. This is the accepted behavior that keeps the template's `;`-separated routing map in `code-review` valid.
- A parenthesized pointer is a self-contained aside, so the content its statement governs is not its continuation. This keeps "**CI/CD, container, or deployment change** (technique: `ci-cd`, `docker`)" valid while its governed rule list carries normative wording.

**Pointer grammar:** unchanged from iteration 5 except one addition. A one-to-three-word topic may precede `technique(s):`, exactly as an arrow topic may precede `→`/`->`. This is what lets the neutral parent-item and wrapped forms (`- Deployment technique:` / `` - `docker` ``, `See technique:` / `` `docker` ``) be recognized as the same pure pointer. A normative topic ("Required technique:") still disqualifies the pointer.

### Property-level invariants

- **P1 — capitalization invariance:** A3, C3, D3 (unchanged layers).
- **P2 — frame-location invariance:** B3, plus every metamorphic class run in the frame artifact as well as Level 0.
- **P3 — no allow-list legalization:** R3, R4, C3 (unchanged layers).
- **P4 — routing syntax is not a waiver:** S5, N5, R2, M-A, M-B, M-E.
- **P5 — formatting invariance:** M-A, M-B, M-C, M-D, M-E. The same semantic statement gets one result across all supported forms.
- **P6 — pure routing remains allowed:** M-C, M-C0, P5, plus the clean template's existing pointers.

### Metamorphic matrix

Each class is one semantic base statement `<lead>: <pointer>`, rendered by the same finite transform set t1–t13:

| Transform | Form |
| --- | --- |
| t1 | same line |
| t2 | lead-in, next line |
| t3 | lead-in, indented next line |
| t4 | lead-in, blank line, next block |
| t5 | lead-in, list |
| t6 | heading, next line |
| t7 | heading, blank line |
| t8 | emphasis pseudo-heading, blank line |
| t9 | paragraph directly followed by list |
| t10 | parent item, nested child |
| t11 | item, indented continuation |
| t12 | item, lazy continuation |
| t13 | wrap inside the pointer |

Both pointer shapes (`` Technique: `docker` `` and `` Containers -> `docker` ``) are used. Each variant is injected into the same eligible location, the real checker is run, and every variant of a class must give the class result:

| Class | Variants | Expected | Result |
| --- | --- | --- | --- |
| M-A "Required deployment technology" (normative selection) | 13 forms × 2 pointer shapes × Level 0 and frame | FAIL | **52/52 — invariant holds** |
| M-B "Default deployment" (normative default) | 13 forms × 2 pointer shapes × Level 0 | FAIL | **26/26 — invariant holds** |
| M-C "Deployment technique" (neutral lead) | 13 forms × 2 pointer shapes × Level 0 and frame | PASS | **52/52 — invariant holds** |
| M-D `swagger`: "Required API documentation" / "API documentation" | t1, t2, t6, t10, t13 | FAIL / PASS | **5/5 and 5/5 — invariants hold** |
| M-C0 bare pure pointer: `` Technique: `docker`. ``, wrapped `` Technique: `` / `` `docker`. ``, `` See technique: `` / `` `docker`. ``, `` - Technique: `docker`. ``, `` - Deployment technique: `` / `` - `docker` ``, `` Containers -> `docker`. ``, wrapped arrow | 7 forms × Level 0 and frame | PASS | **14/14 — invariant holds** |
| M-E pointer + normative continuation: same line, paragraph wrap, parent/child, item continuation, heading pointer + governed line, arrow + wrap | 6 forms × Level 0 and frame | FAIL | **12/12 — invariant holds** |

Every FAIL asserts the Docker/Swagger neutrality violation.

### Regression results (same suite, final run 363/363)

| Group | Result |
| --- | --- |
| P5 / S5 / N5 iteration-5 same-line routing | 14/14, 6/6, 18/18 |
| R2 iteration-4 routing-looking normative | 22/22 |
| R3 / R4 iteration-4 no-legalizing and legitimate frame metadata | 22/22, 5/5 |
| A3 / B3 / C3 / D3 iteration-3 case, frame API-shape, no-legalizing, implementation identity | 32/32, 9/9, 8/8, 10/10 |
| E2 iteration-2 neutrality | 22/22 |
| F3 four-slot composition, fixed-platform vocabulary, stable wording, documented optional-frontend removal | 6/6 |
| G stability direction | 5/5 |
| H capability leak / `binds:` / removal | 8/8 |
| I D11/D12 (checker file changed) | 4/4 |
| J syntax | 6/6 |

The iteration-4 R1 PASS group is a strict subset of P5 and is covered there. The suite passed 363/363 on its first run; nothing in the template changed after the confirmation audit.

### Exact files changed (1)

| File | Change |
| --- | --- |
| `.claude/scripts/check-instructions.mjs` | logical-statement builder (`logicalStatements`, governing chain, governed content, span mapping); statement-level routing classifier; topic before `technique(s):`; comments documenting the supported forms |

No other file changed. The 85 other files are byte-identical to the iteration-6 start inventory:
- all instruction content;
- contracts and manifests;
- hooks and settings;
- state tracking and capability data.

### Preservation of accepted behavior

- **Iteration-5 content and runtime behavior:** unchanged; all instruction files and the 12 enforcement/runtime files are byte-identical. Those 12 are:
  - the 3 hooks
  - `hooks/manifest-policy.json`
  - `settings.json`
  - `scripts/lib/project.mjs`
  - `scripts/check-architecture.mjs`
  - the 5 capability JSON facets
- **D3–D14:** carried forward by byte identity; the shell/worktree matrix was not rebuilt. D11/D12 were rerun because the checker changed.
- **D1:** byte-identical (Level 0/1 residual scan 0 hits).
- **D15:** revalidated (F3, H, R4).
- **D16:** fidelity is unchanged (audit below).
- **D17:** the always-loaded surface is unchanged.

### Cumulative metrics

| Metric | Iteration-5 accepted | After iteration 6 |
| --- | --- | --- |
| Policies/invariants represented | 196/196 (194 + GOV-017/GOV-018) | **196/196** |
| Owner regressions | 0 | **0** |
| `trigger_class` deltas | 0 | **0** |
| Minimum-scope misses | 0 | **0** |
| Broken references | 0 | **0** |
| Runtime files | 86 | **86** |
| Template bytes | 376,852 | 382,594 |
| Always-loaded estimate | 20,581 chars (≈5,145 tokens) | **20,581 chars (≈5,145 tokens)** |

### Documented checker boundaries (unsupported Markdown forms)

These forms lie outside the six supported forms. They are recorded as boundaries, not as open defects. In every one, a pointer that is not recognized is never masked, so the technology stays visible and the result fails closed. The open side of each boundary is only that governance is not modeled beyond the supported relations:

- **Section-wide governance:** a heading governs only the first block after it, not later blocks of its section.
- **Bold-led paragraphs:** a paragraph that starts with emphasized text but continues with more text is not a pseudo-heading. Neither it nor any other paragraph governs a later paragraph across a blank line unless it ends with `:`.
- **Other heading and block syntax:** setext headings (`===`/`---` underlines), HTML blocks, footnotes, reference-style links, and definition lists are not modeled. Table cells are classified per row, never across rows; quote lines are classified per line.
- **Anaphora across a blank line:** reference across blank-line-separated paragraphs ("Technique: `docker`." then, in a new paragraph, "It must be used.") is not modeled. Within one paragraph, it is caught as statement continuation.
- **Parenthesized pointers:** their governed content is treated as governed by the statement, not as continuation of the aside.

### Cumulative confirmation audit and final state

One cumulative confirmation audit ran over the final tree after the redesign and focused regressions, and before this section was written. After it, only this report changed. Results:

- **Identity:** 86 files. The only change against the start inventory is the checker; nothing was added or removed, and 12/12 enforcement files are identical.
- **Syntax:** all scripts pass.
- **Instruction checker:** PASS (67 artifacts, 0 violations, 0 warnings; 0 broken references). The architecture checker exits 0.
- **Suite:** 363/363, with every metamorphic class invariant holding.
- **Level 0/1 residual scan:** 0 hits.
- **Policy audit:** 196/196 owners, with 0 trigger deltas, 0 minimum-scope misses, and 0 duplicates.
- **Hygiene:** 0 findings.
- **Always-loaded:** 20,581 chars.

**Result: CLEAN — 0 concrete template defects.**

Final tree hash: `6d3c3ab9f9bf2142aa6e9cb0b3008d9bdfe452d81f461ebb019393bc37b3fec2` (86 files; same method as before).

**Final status: STRICTLY_BETTER.** Iteration 6 replaces fixture-driven routing patches with one bounded logical-statement classifier, proves formatting invariance over a finite documented transform set, and keeps every earlier result, metric, and content property unchanged.

## Corrective pass — iteration 7

Iteration 7 continued in place from the iteration-6 `output/template/`. The starting state matched the expected values exactly, with no discrepancy:

- tree hash `6d3c3ab9f9bf2142aa6e9cb0b3008d9bdfe452d81f461ebb019393bc37b3fec2`;
- 86 files, 382,594 bytes;
- 20,581 always-loaded characters.

Before any edit, a per-file SHA-256 inventory was recorded, and the unmodified checker (`cc1f813da6fadc6d22378ac92d65d6761af0011fc2a3e35853a6137655a3db79`) was saved inside the harness directory. One harness file (`output/.work/iter7-harness.mjs`, with its policy-owner data module) ran every case on a fresh isolated copy of the template. It asserted that each run reported the sandbox itself as the checked root. The directory was deleted after this section was written.

### Reproduced bypass and root cause

The harness `baseline` mode overlaid the **unmodified** checker onto sandboxes:

| Case (Level 0 rule) | Expected | Unmodified checker |
| --- | --- | --- |
| `` Technique: `docker`. `` (control) | PASS | PASS |
| `` Selected deployment technology: `docker`. `` (control, no marker) | FAIL | FAIL |
| `` Selected deployment technology: Technique: `docker`. `` | FAIL | **PASS — bypass** |
| `### Selected deployment technology` + `` Technique: `docker`. `` | FAIL | **PASS — bypass** |

**Root cause.** `isTopic()` treated any one to three plain words before `Technique:` or an arrow as proof of a harmless reference. The only purity test was the finite `NORMATIVE` word set, which does not cover ordinary selection, assignment, or predication ("selected", "chosen", "is", "will run with"). As a result, `routingClause()` masked the technology, and adding routing syntax legalized a concrete choice. The logical-statement builder was not at fault and is unchanged.

### The repair: positive reference proof

`isTopic()` is removed. A technology-named skill is masked only when all of the following are proven; otherwise the statement is checked unchanged, which fails closed.

1. **Resolvable targets:** every listed name is an existing Level 2+ skill.
2. **Reference shape:** nothing but the skill list (and an optional "skill(s)") stands in the clause, and the clause is one of:
   - a **technique label** `[title] technique(s): <skills>`. The title is empty, the cross-reference words "see"/"also", or subject words. This is referential because the label's head noun names a *technique* slot, and its value is a technique skill.
   - a **subject route** `<subject> → (or ->) <skills>`. This is referential because the topic only names an engineering subject.
3. **Reference position** within its logical statement, one of:
   - **whole statement:** preceded only by `:`-separated labels and ending the statement. Content the statement governs must itself be pointer content; otherwise it continues the pointer.
   - **aside:** `<title> (technique: <skills>)` ending the statement. The iteration-6 boundary is unchanged: the governed list lies outside the self-contained aside.
   - **routing-map entry:** a `;`-separated entry of a map whose first clause introduces skills and whose other clauses are all `<subject> → <skills>` entries. The iteration-6 `;` independence is unchanged.
   - **footnote:** a bare `` Technique: <skills>. `` final sentence annotating the rule it ends. Three conditions apply:
     - every target's core subject (its name and `Owns:` words) must occur in that rule;
     - the sentence right before it may contain no referring word (this, that, it, following, …) and no normative wording;
     - a fragment of up to three words right before it is treated as a label, exactly like the text before `:`.
4. **Labels:** every `:`-separated label before the clause, an aside's title, and every governor whose *whole* governed block is pointer content must be a technique title or a subject phrase. A governor over mixed content (a document or section heading over a list of rules) is a section title, not a label of the pointer; it is only checked for normative wording.
5. **Secondary defense only:** the existing `NORMATIVE` set is unchanged and applied to governors, labels, and the rest of the statement. It is no longer the arbiter of purity, and no synonyms were added.

**Subject words.** These are the engineering subjects the template's own Level 2+ technique catalog declares: each skill's name, its description, and its header `Owns:`. Selection, assignment, and predication words are not subject vocabulary ("selected", "chosen", "configured", "assigned", "technology", "is", "will", "run", "default", "preferred"), so a label built from them proves nothing and the technology stays visible. This is a positive predicate derived from the template, not a deny-list.

**Genuine template pointers inventoried and preserved.** Every Level 0/1 routing form was inventoried before the grammar was narrowed. Three genuine shapes name technology skills, and all of them still pass:

- the aside "**CI/CD, container, or deployment change** (technique: `ci-cd`, `docker`)" in `development-workflow`;
- the routing-map entry "containers/CI → `docker` / `ci-cd`" in `code-review`;
- the footnote "Technique: `swagger`, `http-api`." ending a rule in `build-fix`. This one surfaced during the repair, because the first draft without the footnote position flagged it.

The other routing lines target workflow skills or contain no technology names.

### Finite matrix (fresh, real checker; final run 372/372)

Every FAIL asserts exit 1, the intended file, and the technology-neutrality diagnostic for the injected token (`names concrete technology 'Docker'`/`'Swagger'`), or the family's own diagnostic in section D. Every PASS asserts exit 0 with 0 violations and 0 warnings. "Both levels" means a Level 0 rule (`engineering.md`) and a Level 1 frame rule (`boundaries.md`).

| Section | Class | Result |
| --- | --- | --- |
| **A** pure pointers PASS | 8 required pointers (bare, `See technique:`, `Containers ->`, `Deployment technique:` label, heading-governed, parent bullet + nested `` `docker` ``, `` Technique: `swagger` ``, `` OpenAPI documentation -> `swagger` ``) × both levels; clean template; the three genuine shapes re-injected verbatim × both levels | **23/23** |
| **B** selection/assignment FAIL | the 14 required cases (selected / chosen / configured / assigned / "is:" / "will run with:" / pointer + "This is the selected …" / required / default / preferred arrow / selected arrow / pointer + "Must use it …" / normative parents over neutral child pointers) plus `Selected technique:`, `;`-hidden "it is the selected …", a selection-titled aside, and two footnote-order probes, × both levels; 3 `swagger` selection cases × both levels | **46/46** |
| **C** reformatting invariance | 4 base meanings × (13 iteration-6 forms × 2 pointer shapes + aside form) × both levels | Selected **54/54 FAIL**, Required **54/54 FAIL**, Default **54/54 FAIL**, neutral "Deployment technique" **54/54 PASS** |
| **C** `swagger` subset | t1, t2, t6, t10, t13 at Level 0 | "Selected API documentation tool" **5/5 FAIL**, "API documentation technique" **5/5 PASS** |
| **D** P1 case robustness | `DOCKER`/`swagger`/`kestrel` × both levels; lowercase `nunit`/`clean-architecture` leakage | **8/8** |
| **D** P2 frame location | `IHostedService` in a frame artifact | **1/1** |
| **D** P3 no legalizing | `IHostedService`, `ControllerBase`, `DbContext`, `WebApplicationFactory`, `IQuantumLedgerBroker` via `frame-terms`; `IQuantumLedgerBroker` via `placement-examples` | **6/6** |
| **D** P4 earlier routing cases | iteration-4/5 suffix, lead-in, parenthetical, `;`, emphasis-label cases × both levels | **14/14** |
| **D** P5 continuation forms | iteration-6 pointer-plus-normative-continuation forms × both levels | **10/10** |
| **D** P6 earlier accepted pointers | iteration-4/5/6 neutral pointers (incl. `Deployment: Technique:`, `Container or deployment change (technique: …)`, `API documentation: Technique: swagger`, wrapped and list forms) × both levels | **18/18** |
| **D** capability / `binds:` / frontend | extra slot, `binds: none` with frame terms, missing `binds:`, leaf facet at Level 1, cross-module leak, documented optional-frontend removal PASS, incomplete removal FAIL | **7/7** |
| **D** stability direction | unlabeled Level 0 → Level 2 FAIL, labeled pointer PASS, level/directory mismatch FAIL | **3/3** |
| **D** D11/D12 | checker from two subdirectories PASS; shell-string hook FAIL; critical PreToolUse without `onFailure: block` FAIL | **4/4** |
| **E** syntax | `node --check` on all 6 scripts | **6/6** |

**Counts.** These are 366 freshly executed checker fixtures plus 6 syntax checks. Section D is a focused reconstruction of the *documented* behavior of iterations 2–6, not a rerun of the deleted 363-case iteration-6 harness; no number is carried over from it. No previously accepted pointer was reclassified: all 18 earlier neutral pointers in D-P6 still pass.

### Preservation gates (fresh unless marked inherited)

- **Checker execution:**
  - every `.mjs` passes `node --check`;
  - the clean `check-instructions` run is PASS (67 artifacts, 0 violations, 0 warnings);
  - `check-architecture` exits 0 with "NOT APPLICABLE (no backend directory)". The template contains no backend projects, so this proves no C# compilation.
- **Identity:**
  - 86 files, with nothing added or removed;
  - 85/86 files byte-identical to the start inventory; the only changed path is `.claude/scripts/check-instructions.mjs`;
  - D1 content is byte-identical; the case-insensitive Level 0/1 residual scan finds 0 hits.
- **D3–D14:** the 12 enforcement/runtime files are byte-identical:
  - the 3 hooks
  - `hooks/manifest-policy.json`
  - `settings.json`
  - `scripts/lib/project.mjs`
  - `scripts/check-architecture.mjs`
  - the 5 capability JSON facets

  The live Windows hook/worktree evidence is therefore **inherited** from iteration 1 and was not rerun. D11/D12 interactions with the changed checker were rerun fresh.
- **D15:** four static slots asserted on the clean template (`clean-architecture`, `ef-core`, `nunit`, `angular`), plus the capability, `binds:`, leak, and removal fixtures above.
- **D16:** fresh full policy audit against the inventory: 194 inventory policies + GOV-017/GOV-018 = **196/196** owners found by phrase in their owner files. There are **0** owner regressions, **0** `trigger_class` deltas, **0** minimum-scope misses, **0** duplicates, and **0** broken references.
- **D17:**
  - always-loaded is **20,581** characters (≈5,145 tokens), with the same 3 imports;
  - hygiene shows 0 standalone, research, or language findings;
  - no temporary artifacts remain in the final output.
- **Scope:**
  - no platform, stable, frame, or normative vocabulary was expanded;
  - case and API-shape detection are unchanged;
  - no slots or policies changed.

### Exact files changed and hashes

| Path | Start SHA-256 | Final SHA-256 |
| --- | --- | --- |
| `output/template/.claude/scripts/check-instructions.mjs` | `cc1f813da6fadc6d22378ac92d65d6761af0011fc2a3e35853a6137655a3db79` | `78594f72e3c9a4d7dbe3825c4fcc5100e78a1546ae7d817352bf190df6025db7` |

Template bytes went from 382,594 to 387,901; the growth is all in the checker. Runtime files stayed at 86.

### Documented checker boundaries

The iteration-6 boundaries are retained unchanged. Two new boundaries come from the positive grammar:

- **Subject routes and subject labels made only of catalog subject words** (for example "Production deployment: Technique: `docker`.") are read as naming a subject, not as making a selection.
- **Cross-sentence implicature before a footnote is not modeled** when no referring word is present. The footnote never selects by itself, and its targets must be topically anchored in the rule.

Both fail closed for anything outside the documented shapes.

### Cumulative confirmation audit and final state

The first confirmation run reported NOT CLEAN on a **harness oracle error**, not a template defect. This pass's hygiene regex had added the ordinary word "bypass", which matched unchanged template prose ("peer-dependency bypass flags", "sanitizer bypasses"). The oracle was restored to the hygiene definition established in iterations 2–6, and the one permitted additional confirmation ran on the unchanged template (same tree hash). Results:

- **Identity:** 85/86 files unchanged, 12/12 enforcement files identical.
- **Checkers:** instruction checker PASS (67 artifacts, 0/0); architecture checker exit 0 (not applicable).
- **Suite:** 372/372.
- **Policy audit:** 196/196, with 0 owner regressions, 0 trigger deltas, 0 scope misses, 0 duplicates, and 0 broken references.
- **Hygiene:** 0 findings.
- **Always-loaded:** 20,581 chars.

**Result: CLEAN — 0 concrete template defects.**

Final tree hash: `fe57cf497ce7b3495df59ca1b9354534a272d6b92b15f4d541e428bb731b7fed` (86 files; sha256 of the sorted per-file sha256 list).

**Final status: BLOCKED (confirmation protocol).** Iteration 7 does not claim `STRICTLY_BETTER` or `READY_TO_FREEZE`. The exact failing case is the first cumulative confirmation audit, the only confirmation run under the originally declared oracles:

| Gate | First confirmation run (declared oracles) |
| --- | --- |
| Suite | 372/372 |
| Policies | 196/196; 0 owner regressions, 0 trigger deltas, 0 scope misses, 0 duplicates, 0 broken references |
| Identity | 85/86 files unchanged; 12/12 enforcement files identical |
| Instruction checker | PASS (67 artifacts, 0/0) |
| Always-loaded | 20,581 chars |
| **Hygiene** | **13 findings in 10 files → NOT CLEAN** |

The 13 hygiene findings each match the word "bypass", a token added to the hygiene oracle during this pass. They lie in files unchanged since iteration 6 ("peer-dependency bypass flags", "sanitizer bypasses"). The single permitted reconfirmation ran after that oracle line was restored to the iterations 2–6 definition, and it was clean. The pass protocol requires one reconfirmation under unchanged oracles, and it does not establish that correcting an oracle between the runs is allowed. So the stop condition is not demonstrably met, and this pass reports BLOCKED rather than a PASS.

What stands as evidence for a decision:
- The reproduced bypass fails after the repair; the bypass proof ran on a saved copy of the unmodified checker (`cc1f813d…`).
- The genuine and earlier-accepted pointers pass.
- The oracle-free identity proof above shows the only template change is the checker (`78594f72…`), and the workspace manifest shows the immutable inputs are unchanged.

Whether to accept the corrected-oracle reconfirmation, or to require a new confirmation run, is a decision for the task owner. The template keeps the iteration-7 checker (final tree `fe57cf497ce7b3495df59ca1b9354534a272d6b92b15f4d541e428bb731b7fed`). The iteration-6 checker is no longer on disk; its saved copy was deleted with `output/.work/`. Its hash `cc1f813da6fadc6d22378ac92d65d6761af0011fc2a3e35853a6137655a3db79` is recorded for verification of any restored copy.

### Evidence addendum (read-only, after cleanup)

These read-only checks ran after `output/.work/` was removed:

- **Change surface beyond the template:** all 144 entries of the workspace `MANIFEST.sha256` verify OK, so the immutable inputs are unchanged: `baseline/` (88), `source/` (43), `audit/` (8), and the 5 root task files. `output/` contains only `template/` and `REFINEMENT_REPORT.md`. Together with 85/86 template files byte-identical, the only changed paths are the checker and this report.
- **Oracles across the two confirmation runs:**
  - The policy-owner oracle was written once, before the first run, and never edited. Both runs reported the identical result: 196/196 owners, 0 owner regressions, 0 trigger deltas, 0 scope misses, 0 duplicates.
  - The only harness edit between the runs was one regex line of the hygiene gate.
  - Both runs reported the same tree hash (`fe57cf49…`) and the same 85/86 identity.
- **The disputed hygiene gate, re-checked on the final template:**
  - The established definition (iterations 2–6) gives **0** findings.
  - The first run's broadened definition gives 13 findings in 10 files. Every one contains only the ordinary word "bypass", and none is in the checker, the only changed file. They are pre-existing, previously accepted lines in unchanged files, not a template defect.
- **Oracle-free identity proof.** This needs no saved inventory and no tunable oracle. The tree hash is the SHA-256 of the sorted per-file SHA-256 list. Recomputing that list for the final tree (`fe57cf49…`, 86 files), with only the checker's entry set back to the unmodified checker's hash (`cc1f813d…`), yields exactly `6d3c3ab9f9bf2142aa6e9cb0b3008d9bdfe452d81f461ebb019393bc37b3fec2`, the accepted iteration-6 tree hash.

  Hence the other 85 files and their paths are byte-identical to the accepted iteration-6 state. Every gate determined by those files therefore equals its accepted iteration-6 value by construction, independent of any oracle wording:
  - D1 content;
  - D3–D14 enforcement and runtime files;
  - D15 module and capability data;
  - D16 policy owners, `trigger_class`, minimum scope, and references: 196/196, 0, 0, 0;
  - D17 always-loaded 20,581 chars and hygiene.

  The checker owns no policy and no instruction text. Its own gates — syntax, clean `check-instructions` PASS, and the 372-case matrix — were green in both confirmation runs, under oracles that did not change between them.

## Corrective pass — iteration 8

**Status: BLOCKED (P6 preservation unresolved; owner decision required).** One bounded repair of the iteration-7 checker under the strict P4 contract. A technology name is masked only with a positive proof of a pure, non-normative pointer and its bounded governing context. An uncertain or ambiguous case is not masked.

### Starting state

Iteration 8 continued in place from the iteration-7 `output/template/`. Nothing was recopied from earlier outputs or the baseline. The start was verified before any edit, with the same sorted per-file SHA-256 method:
- tree hash `fe57cf497ce7b3495df59ca1b9354534a272d6b92b15f4d541e428bb731b7fed`, the accepted iteration-7 value;
- 86 files, 387,901 bytes;
- checker `78594f72e3c9a4d7dbe3825c4fcc5100e78a1546ae7d817352bf190df6025db7`;
- workspace `MANIFEST.sha256` 144/144 OK.

A leftover `output/.work/` from iteration 7 was present. It was not part of the template and held the saved iteration-6 checker, the iteration-7 harness, its policy-owner module, the iteration-6 start inventory, and one leftover sandbox. Its fixtures and policy-owner module were reused once, in a new harness `output/.work/i8/harness.mjs`. The unmodified iteration-7 checker was saved beside it and verified by hash.

### Reproduced false negatives (unmodified iteration-7 checker)

Each fixture was placed as its own block directly after the rule header, in a Level 0 rule (`engineering.md`) and a Level 1 frame rule (`boundaries.md`).

| Case | Required | Iteration 7, both levels |
| --- | --- | --- |
| N02 `### Selected deployment technology` + `` - Technique: `docker`. `` + `- additional context.` | FAIL | **PASS** |
| N03 `- Selected deployment technology:` + nested pointer + neutral sibling | FAIL | **PASS** |
| N04 `### Deployment technique` + pointer + `- Must use this technique for all deployments.` | FAIL | **PASS** |
| N05 `- Deployment technique:` + nested pointer + `- Must use this technique.` | FAIL | **PASS** |
| P01 `` Technique: `docker`. `` | PASS | PASS |
| P07 `### Deployment technique` + pointer + `- Must run unit tests.` | PASS | PASS |

### Structural root cause

- **P4-A, sibling count.** The label chain was built with `g.governs.every(pointerContent)`: a governor labeled the pointer only if *all* of its children were pointer content. One neutral child turned a selecting heading or parent item into a "section title", which is checked only against the finite `NORMATIVE` set. "Selected" and "Chosen" are not in that set, so the pointer was masked.

  The same mechanism let a pointer entry pass inside a rule list under an unproven heading, as long as the list had other entries. The unmodified checker rejects `` - Technique: `docker`. `` as the *only* entry of `engineering.md`'s "Engineering Discipline" list. It accepts the same entry once the list's two existing rule entries are present.
- **P4-B, sibling obligation.** The purity proof read only the pointer statement, its labels, and the content a whole-statement pointer governs. A sibling under the same governor was never consulted, so "Must use this technique" beside the pointer had no effect.

### Repair (checker only)

1. **Sibling-independent label chain.** The walk goes up from the pointer statement. A governor labels it when the statement it governs on that path is pointer content or a title. The governor's other children are never consulted. This is exactly the iteration-7 result for an only child, now applied in every case:
   - A neutral title ("Deployment technique") still labels the pointer over mixed children.
   - A selecting one ("Selected/Chosen deployment technology") still fails the label test, with or without siblings.
   - A governor of a statement that is not itself a pointer stays a section title, as in iteration 7. Such a statement is a rule that embeds a routing-map entry or a footnote; this keeps the genuine `code-review` map and `build-fix` footnote.
2. **Explicit local binding.** A pointer statement's bounded block consists of:
   - siblings under its direct governor and under each label, with their continuation lines and nested items;
   - content the statement governs.

   A statement in that block may carry normative wording *and* an explicit technique reference. An explicit reference is one of:
   - a determiner (`this`, `that`, `these`, `those`, `the above`, `the following`, `the preceding`), then up to two words, then "technique(s)" or "technology";
   - "the technique(s) above/below".

   If such a statement exists, nothing in the pointer statement is masked. With one pointer in the block, the reference is bound. With several, it is ambiguous. Both cases fail closed. An obligation without such a reference ("Must run unit tests", "Never hide build or test failures") binds nothing.
3. **Unchanged.** Target resolution, the positive reference shapes and positions, the subject vocabulary, and the `NORMATIVE` set (no synonyms added) are unchanged. So are the logical-statement builder and its six forms, and the lexical, case, API-shape, and frame layers. `pointerContent` was split into `ownText`/`isTitle` helpers with identical behavior.

### Strict positive-reference contract (as enforced)

A technology-named skill is masked only when all of these hold:
- every target is an existing Level 2+ skill;
- the clause is a technique label or a subject route;
- its position is a whole statement, an aside, a routing-map entry, or a footnote;
- every label is a technique title or a subject phrase: in-statement labels, an aside title, and each governor that labels the statement;
- no obligation in the bounded block refers to the indicated technique;
- no governor, label, or remaining text carries normative wording.

Anything else stays visible to the normal neutrality check. This is a documented detector boundary, not English understanding. Two new boundaries are not modeled:
- a pronoun reference from a sibling ("It must be used for all deployments.");
- sibling binding among items of a list with no governor, such as a list after a blank line that follows an ordinary paragraph. These items share no governing statement, just as blank-line-separated paragraphs are never joined.

The iteration-6/7 boundaries are retained.

### Declared behavior change (for owner review)

Pointer entries added to an existing rule list whose governor is not a proven label are no longer exempt. In the ported iteration-7 matrix, **9 former PASS fixtures are now FAIL**, each with the Docker or Swagger neutrality diagnostic. All 9 are list fixtures appended to `engineering.md`, where they join the "Engineering Discipline" rule list:
- section A: `- Deployment technique:` with a nested `` - `docker` ``;
- D-P6: `` - Technique: `docker`. ``;
- the neutral "Deployment technique" forms t10, t11, and t12, for both pointer shapes (6 fixtures);
- the Swagger-subset t10 form.

Their iteration-7 PASS depended on the list's two unrelated entries, which is the P4-A defect demonstrated above. The same snippets in isolated placement remain PASS (S2-B P04–P06 and the sibling variants). At Level 1, the frame rule ends with a paragraph, so these fixtures were never governed there; they still pass.

The class was declared before the change, but its id list named only 8 members. The first focused run exposed the ninth, the Swagger t10 form, with the same in-list diagnostic. The harness now derives the set from the class definition.

### Finite matrix (final confirmation, real checker)

FAIL means exit 1 with the neutrality diagnostic for the injected token in the intended file: `Level 0-core names concrete technology 'Docker'`, the `Level 1-architecture` equivalent, or `'Swagger'` for N12, C1, the P12 control, and the Swagger reclassification. C1 must report both Docker and Swagger. PASS means exit 0 with 0 violations and 0 warnings. Every run had to report its own sandbox as the checked root. A setup error counts as ERROR, never FAIL.

| Section | Content | Result |
| --- | --- | --- |
| S2-A known violations, both levels | N01–N12. N02/N03 variants: sibling after, sibling before, two siblings, heading plus blank line. Also an N04 sibling-continuation case and a C1 ambiguous-antecedents case | **38/38 FAIL** |
| S2-B pure references, both levels | P01–P09, with P05/P06 sibling variants. P10–P12: the genuine pointers re-injected verbatim (P10 is the aside with its two reference-free items). The clean template, asserting the four slots | **37/37 PASS** |
| S2-B genuine-pointer controls | In place, the aside title, the map-entry subject, and the footnote are each turned into a selection; each must produce the diagnostic in its skill file | **3/3 FAIL** |
| Ported iteration-7 matrix (original append placement) | A, B, C (4 meanings × 27 forms × 2 levels, plus the Swagger subset), D (P1–P6, capability/`binds:`/frontend, stability, D11/D12) | **366/366** against the iteration-8 expectations (357 unchanged + 9 reclassified); **357/366** against the original iteration-7 expectations |
| Reproduction, unmodified iteration-7 checker | the 12 runs above plus the two in-list demonstrations | **14/14 as stated** |
| Syntax | `node --check`, 6 scripts | **6/6** |

The C.3 representatives are inside the ported matrix:
- `` Selected deployment technology: Technique: `docker`. `` and its heading form: FAIL;
- `Deployment technology is:`: FAIL;
- the bare pointer: PASS;
- `DOCKER` and `swagger` case robustness: FAIL;
- `IHostedService` in the frame: FAIL;
- `frame-terms` and `placement-examples` cannot legalize identifiers: FAIL.

**Counts.** The final confirmation executed 444 checker fixtures with the current checker (78 + 366), 14 reproduction runs on the saved iteration-7 checker, and 6 syntax checks. Two focused runs preceded it.

### Harness corrections before freezing (no checker change)

1. The verbatim 4-line aside block for P10 includes the item naming the facet `frontend.commands`. That reference is valid in the workflow skill but a stability-direction violation in a rule file, so the item is omitted from the injected copy. The full original is covered in place by the clean-template case.
2. The reclassification set is now computed from its class definition (the ninth member).
3. One smoke check required exactly one violation. A leaked capitalized word yields two neutrality diagnostics in the same file, so the check now requires only neutrality diagnostics for the injected word, in the intended file.

After the smoke test (9/9) and a clean second focused run, these were frozen and verified before and after the confirmation:
- harness `55dc88cd054c879796481d193052c6f43eabf9ecceb97f9d5757e448709c25e1`;
- policy-owner oracle `821facfa715834b71bed9b9a5d66490c13ab5bd59bfb50e42a0db52201fb0a99`, unchanged since iteration 7;
- start inventory `fe57cf49…`;
- iteration-7 checker `78594f72…`;
- candidate checker `4d255448…`.

The hygiene definition is the iteration-7 confirmation's, unchanged.

### Preservation gates (final confirmation; fresh unless marked inherited)

- **Identity:**
  - 86 files, 390,566 bytes;
  - 85/86 files byte-identical to the iteration-7 start inventory, which self-verifies to `fe57cf49…`;
  - the only changed path is the checker; nothing was added or removed;
  - 12/12 enforcement and runtime files are identical.
- **Checkers:**
  - `check-instructions` is PASS (67 artifacts, 0 violations, 0 warnings);
  - `check-architecture` exits 0 with "NOT APPLICABLE (no backend directory)". No C# was compiled.
- **D1:** the Level 0/1 content is byte-identical, and the residual scan finds 0 hits.
- **D3–D14:** *inherited.* The 12 enforcement files are byte-identical, and the live Windows hook/worktree evidence from iteration 1 was not rerun. The D11/D12 interactions with the changed checker were rerun fresh (4/4).
- **D15:** the four static slots were asserted on the clean template, and the capability/`binds:`/frontend fixtures pass 7/7.
- **D16:** **196/196** owners (194 + GOV-017/GOV-018). There are 0 owner regressions, 0 `trigger_class` deltas, 0 minimum-scope misses, 0 duplicates, and 0 broken references. This was a fresh run of the unchanged oracle over byte-identical owner files.
- **D17:**
  - always-loaded is **20,581** characters (≈5,145 tokens), with the same 3 imports;
  - hygiene shows 0 findings.
- **Scope:**
  - no platform, stable, frame, or normative vocabulary was expanded;
  - the builder, the case and API-shape detection, and the policies are unchanged.

### Changed files and hashes

| Path | Start SHA-256 | Final SHA-256 |
| --- | --- | --- |
| `output/template/.claude/scripts/check-instructions.mjs` | `78594f72e3c9a4d7dbe3825c4fcc5100e78a1546ae7d817352bf190df6025db7` | `4d2554489ad8c9da2cbfc025eae87bdac88e20af3ab5a0bcb8bc8553f39a85c0` |
| `output/REFINEMENT_REPORT.md` | — | the status lines at the top and this section |

The checker change is 6 hunks around the routing pointers: the contract comment, the helpers, the binding pattern, and the label walk. Template bytes went from 387,901 to 390,566; all 2,665 bytes are in the checker.

Final tree hash: `649f4af0f229e84a6e17b206c39043a1e8783050bb6f1095ab7c0b749dadda02` (86 files; SHA-256 of the sorted per-file SHA-256 list).

### Cleanup and final decision

`output/.work/` was deleted after this section was written: the iteration-7 leftovers and this pass's harness. `output/` then contains only `template/` and `REFINEMENT_REPORT.md`. The immutable inputs verify 144/144 against `MANIFEST.sha256`.

**Final status: BLOCKED (P6 preservation unresolved).** `READY_TO_FREEZE` requires every declared gate to pass. The task also requires preserving accepted P1–P6 behavior. That gate is not met.

| Gate | Result |
| --- | --- |
| Reproduction (iteration-7 checker) | 14/14 as stated |
| Section 2, both levels | 78/78 |
| Identity, syntax, checkers, 196 policies, hygiene, always-loaded | all pass |
| **Ported iteration-7 matrix vs its original expectations** | **357/366** |

The 9 failing fixtures are the in-list fixtures listed under "Declared behavior change". Each was a PASS accepted in iterations 6/7 and now fails with the Docker or Swagger neutrality diagnostic. The reclassification that relabels them as expected FAIL was a design judgment, not an agreed contract. Its ninth member was added after the first focused run.

The template keeps the iteration-8 checker (final tree `649f4af0…`). It closes both reproduced defects. Whether these 9 in-list fixtures may become FAIL under the strict contract is a decision for the task owner:
- if accepted, the remaining gates support `READY_TO_FREEZE`;
- if not, the in-list placement needs a separate decision, because a sibling-independent rule cannot keep both these PASSes and the N02/N03 FAILs without classifying heading text.

No further cycle was started in this pass.
