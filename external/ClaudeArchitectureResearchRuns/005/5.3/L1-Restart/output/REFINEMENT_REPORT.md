# L1-Restart Refinement Report (Phase 5.3, Candidate L1)

## 1. Terminal status: **STRICTLY_BETTER**

All mandatory repairs D1–D15 are implemented and evidenced against the final template, D16/D17 were reviewed, the
frozen Section-3 P4/P6 matrix passes in both eligible levels, and one unchanged-oracle cumulative confirmation audit
ran clean (**302/302 checks, 0 failures**, groups G1–G7). L1 identity (0 Core → 1 Architecture → 2 Technology →
3 Project, four static slots, frame/leaf ownership, selected clean-architecture / ef-core(sqlserver) / nunit /
angular) is unchanged. The baseline fails the same harness broadly (Section 9). Known bounded limitations are listed
in Section 12; none is a known template defect or an accepted Level 0/1 technology assignment.

## 2. Provenance and working copy

- Workspace: fresh L1-Restart copy; `output/` was empty at start (0 files). Nothing was imported from L1 iterations 2–8
  or other candidates; no sibling/parent directories were read.
- Immutable inputs verified with `MANIFEST.sha256`: 144/144 OK at start and again at the end (the two Restart prompt
  files are not in the manifest and were not modified).
- `baseline/template/` (Run-02) copied byte-for-byte to `output/template/`; `diff -r` identical; 85 files.
- Tree-hash algorithm (run inside the tree): `find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum | sha256sum`.

| | Files | Bytes | Tree hash |
|---|---:|---:|---|
| Baseline Run-02 (start copy) | 85 | 298,925 | `852d78f8a8f8094d9507bdb8b827781b79cfc1696d94df65e91301b644c52422` |
| Final `output/template/` | 86 | 351,673 | `e11bcf8c00b884aabe8d4b6408f90f66c4ab2b67fab534fcc9dd66508702cc22` |

The final hash is the hash of the exact tree that the confirmation audit ran against (re-verified after the run).

## 3. File changes

Added (3): `.claude/rules/2-technology/backend-platform.md` (Level 2 bindings receiving the concrete API technique
removed from Levels 0/1), `.claude/hooks/pre-shell-command.mjs`, `.claude/hooks/post-change-checks.mjs`.
Removed (2): `.claude/hooks/pre-bash-dependency.mjs`, `.claude/hooks/post-edit-checks.mjs` (replaced by the two hooks
above; names now match their Bash+PowerShell / edit+shell scope).
Changed (34): `settings.json`; `hooks/stop-cochange.mjs`, `hooks/manifest-policy.json`; `scripts/check-instructions.mjs`,
`scripts/check-architecture.mjs`, `scripts/lib/project.mjs`; rules `0-core/{backend-code,frontend,http-api,security,testing}.md`,
`1-architecture/roles.md`, `1-architecture/frame/{adopted-style,boundaries}.md`,
`2-technology/backend-testing/test-framework.md`, `3-project/package-management.md`; capability metadata
`architecture/CONTRACT.md`, `architecture/clean-architecture/{MODULE.md,layout.md}`, `persistence/CONTRACT.md`,
`frontend/CONTRACT.md`, `frontend/angular/{MODULE.md,enforcement.json}`; skills `architecture-decision`, `build-fix`,
`code-review`, `dotnet-testing`, `project-structure`, `security-scan` (+ `references/scan-layers.md`, re-leveled to
Level 2), `template-maintenance`, `verify`; `INSTRUCTION_MAP.md`. `CLAUDE.md` is byte-identical to baseline.

## 4. D1–D17 disposition

| Item | Disposition | Evidence |
|---|---|---|
| D1 Core/Architecture neutrality | **Fixed.** Every Level 0/1 artifact audited. Neutral policy kept at its owner; concrete technique moved to `2-technology/backend-platform.md` (bindings that add no policy) or the owning facet: `IExceptionHandler`, `ProblemDetails`/`ValidationProblemDetails`, ASP.NET Core Identity/Data Protection, `dotnet user-secrets`, `WebApplicationFactory` (→ `backend-testing.framework`), `IActionResult`/`HttpResponseMessage`, ASP.NET Core Controllers / Minimal API in the frame, `.Result`/`.Wait()`/`CancellationToken`/`TimeProvider`/`HttpClient`/`IHttpClientFactory`/`ILogger<T>`/`IConfiguration`/`ValueTask`/`Task`, TypeScript/OpenAPI/curl/PowerShell/`[Authorize]`/`AllowAnyOrigin()` in Level 0 workflows. `scan-layers.md` (pure .NET/ASP.NET Core investigation technique) re-leveled 0→2. Platform boundary NOT enlarged (still .NET, C#, ASP.NET Core, NuGet, HTTP, Git). | G1 129/129; content audit (§6); owners unchanged (G7) |
| D2 Checker approximation | **Fixed.** Neutrality = deny-by-default API-shape detection + vocabulary derived from the template (Level-2 skill names, leaf leak tokens, enforcement package ids) + a lexicon + the bounded P4 grammar. Removing a lexicon entry does not make `IExceptionHandler`, `WebApplicationFactory<Program>`, `` `docker` `` or `NUnit` pass (A09). Frame terms / placement examples cannot legalize technology (A08, A08b). | G1 A01–A10, A08b, A09 |
| D3 Launcher cwd fragility | **Fixed.** Exec form `command: "node"`, `args: ["${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.mjs"]` for all five registrations. | G3 H01, G5 nested/worktree/space paths |
| D4 Launcher vs active root | **Fixed.** `resolveRoots(cwd)`: launcher root (script location) vs active root (template root ancestor of hook `cwd` within the Git top-level, else Git top-level); config from the active root when it carries the template. State, manifests, architecture and Stop use the active root; Edit hooks resolve from the edited file. | G5 W01–W06 (main tree and state byte-unchanged while worktree active) |
| D5 Fail-closed PreToolUse | **Fixed.** `onFailure: "block"` + script exit 2 on empty/malformed/incomplete input and internal failure. | G3 H03a–f blocked (missing script, crash, timeout, malformed, empty, no command); H03g harmless allowed |
| D6 npm/pnpm/yarn options | **Fixed.** Table-driven tokenizer/segmenter (quotes, `&&`/`;`/`|`, PowerShell `&`, `bash -c`, `cmd /c`, `powershell -Command`, `npx`), value-taking global options (`--prefix`, `-C`, `--workspace`/`-w`, `--dir`, `--filter`/`-F`, `--cwd` …), `=`-forms, force/legacy-peer flags anywhere incl. `npm config set`. | G4 71/71 |
| D7 dotnet reference bypass | **Fixed.** `dotnet add/remove … reference …` and `dotnet reference add/remove` → `ask` before execution (Reserved unless it implements the approved layout); architecture check validates the resulting graph afterwards. | G4 reference rows; G5 A08/A14 |
| D8 Post-change via command text | **Fixed.** `PostToolUse` Bash|PowerShell validates the actual per-worktree manifest snapshot independent of command text (Git index ids for clean files, content ids only for files Git reports changed). | G5 A04 (unrecognized `node -e` mutation), A06 |
| D9 Failed shell calls | **Fixed.** `PostToolUseFailure` Bash|PowerShell registered; same actual-state validation; quiet when nothing relevant changed. | G5 A07, A08 (findings), A09 (quiet) |
| D10 HEAD/rewrite/delete/move state | **Fixed.** Persistent per-worktree snapshot; first observation validates all manifests once; later events validate added/changed/removed/moved manifests incl. HEAD transitions; skipped dirs never enter state. | G5 A11–A18, W01 |
| D11 Checker freezes serialization | **Fixed.** Checker validates exec form, placeholder as argument data, script existence, required events/matchers, `onFailure` only on PreToolUse, `PostToolUseFailure` coverage. | G3 H02a–f |
| D12 Manual checker after `cd` | **Fixed.** One documented form everywhere: `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-…mjs"` (Bash and PowerShell); fallback documented outside Git. | G3 H05 (root, nested, worktree, worktree-nested × Bash/PowerShell; architecture check in worktree) |
| D13 Windows encodings | **Fixed.** Hook stdin and manifests: UTF-8, UTF-8 BOM, BOM-tagged UTF-16LE/BE; odd-length UTF-16, invalid UTF-8, BOM-less UTF-16 (NUL) → visible deterministic findings; single/double-quoted XML attributes equivalent; MSBuild `$(…)` values reported, not trusted. | G6 E01–E10 (incl. real PowerShell 5.1 `-Encoding Unicode`) |
| D14 Stop dedup | **Fixed.** Fingerprint = reminder kinds + content ids of triggering files, per worktree; `stop_hook_active` exits; clean state writes nothing. | G6 T01–T10 |
| D15 Four-slot integrity | **Fixed/strengthened.** Exactly four slot dirs and rows, recorded requirement (architecture = required frame), slot-contract titles, required facets from contracts, facet metadata, static composition, leak rule (now case-insensitive), `binds:` (frame binds nothing; leaf binds only the selected frame with a reason; required by contract `requires-binds` **and** independently by frame vocabulary in module content), frontend CLI routing moved into `frontend.enforcement`, documented removal incl. map rows. | G2 26/26 (S05–S08, S13–S16) |
| D16 V2 technique | **Reviewed.** 589 V2 sections compared with output and baseline: mean best-section term recall 0.586 vs baseline 0.587 (the 0.001 difference is relocation of API names into the binding rule, not loss). Low-recall sections inspected; restored V2's test-technique decision table in `dotnet-testing` (technique only). Other low-recall sections were compressions already present (e.g. deprecated Elasticsearch sink, expected-outcome technique). | §10 |
| D17 Always-loaded | **Reviewed, no compaction.** Same method on both trees (CLAUDE.md + imports + model-visible skill/agent listings): 20,623 → 20,596 chars ≈ 5,156 → 5,149 tokens (PROVENANCE's 20,341/5,085 used another method). No always-loaded routing prose was demonstrably redundant enough to remove without weakening routing. | G7 P-always-loaded |

## 5. P4/P6: supported grammar and fixture results

Implemented in `check-instructions.mjs` and frozen in advance (pre-edit contract):

- **Scope:** Markdown artifacts with header Level `0-core`/`1-architecture` (incl. frontmatter `description`, tables, code).
- **Only** a backticked reference to an existing Level-2 technique skill can be masked. Bare names, API identifiers,
  leaf leak tokens and package ids are never masked.
- **Pointer forms (per `;`/`·` clause):** `<reference label>: refs` (generic `Technique:`/`See technique:`/`References:`
  or self-describing `<topic> technique(s)|reference(s)`), `see refs`, `<area> → refs` / `->`, parenthesized aside
  `(technique: refs)` whose anchor has no modality word, `<reference label>: Technique: refs`, and a non-normative
  same-line lead before a route/self-describing pointer.
- **Six structural forms:** same line, heading, parent/nested item, list-item continuation, colon lead-in + following
  list, wrapped paragraph — parsed by a bounded block parser.
- **Governors:** any ancestor (all heading levels, parent items, lead-ins, same-sentence lead) with a word from a closed
  modality set (must, required, selected, chosen, default, preferred, use, approved, decided, …) blocks masking; a
  GENERIC-label pointer that forms a whole list item needs its nearest governor to be a reference label (so a generic
  rule list such as `Engineering Discipline` never legalizes `- Technique: \`docker\`.`); paragraphs are
  self-contained statements.
- **Referential obligations:** a sentence in the same block, an immediate sibling item or an ancestor containing
  `this|that|these|those|the above|below|following|preceding|previous|listed|referenced|said` + technique/tool/skill/
  reference… binds the pointer(s): no exemption, with one or several antecedents. Unrelated duties (`Must run unit
  tests.`) have no effect.

Results (both L0 `0-core/engineering.md` and L1 `frame/boundaries.md`, fresh copy per case): N01–N14 (19 rows) FAIL
with the neutrality diagnostic naming the injected `docker`/`swagger`; P01–P12 (19 rows) PASS with 0 violations and
0 warnings; metamorphic M01–M12 as specified (neutral siblings before/after never legalize a selection; binding sibling
above/below always fails; unrelated normative sibling keeps PASS; case variants `Docker`/`DOCKER` fail; Swagger
controls); A01–A07 API/vocabulary leaks fail; A10 platform/role paragraph passes; genuine in-place constructs
(`development-workflow` aside, `code-review` route map, `build-fix` footnote) pass. **G1: 129/129.**

Unsupported (documented, out of scope): remote pronouns and cross-section references; free paraphrase that assigns a
technology without any technology token (covered only by the content audit); a generic-label pointer paragraph under a
non-normative topic heading is accepted (matrix-silent); a maintainer could add a new, non-lexicon API name to the
frame's `frame-terms`/`placement-examples` (visible boundary change; technology names and known framework APIs are
rejected there).

## 6. Independent Level 0/1 content audit

All Level 0/1 artifacts were reread after the edits. Remaining concrete terms are inside the predefined platform
boundary or are not prescriptions: `dotnet build/test/format/package list`, `.slnx`, `global.json` (.NET toolchain),
LINQ (C#), `Program.cs`/`appsettings*.json` (ASP.NET Core host placement), ORM/identity (concepts), MD5/SHA1 (named as
acceptable non-security checksums), MCP (named as *not* required), Conventional Commits (optional commit-message
convention), and the grammar-verified pure pointers to `docker`, `ci-cd`, `swagger`, `http-api` and other technique
skills. The Level-1 JSON facet `check.json` keeps `Microsoft.AspNetCore.App` (platform shared framework, inner-role
prohibition) and MediatR/Kommand as approval-required (non-adoption enforcement data, not a selection).

## 7. Policy preservation (196 = 194 inventory + GOV-017/GOV-018)

Frozen owner map (owner file + distinctive anchor per policy), audited automatically and reviewed by hand:
mapped 196/196; owner missing 0; anchor missing 0; **trigger_class deltas 0**; **minimum-scope misses 0** (rule
`paths` checked against sample paths per scope); **strength/condition issues 0**; **duplicate primary anchors 0**;
**owner relocations 0** (D1 moved bindings, not owners; e.g. API-007 is still owned by `0-core/http-api.md`, now
neutral, with its mechanism in the Level-2 binding); broken references 0 (checker); hygiene: English only, no
research metadata. `SPECIFICATION.md` remains an empty input.

## 8. Structure, capability and hooks results (final template)

- **Level/stability (G2):** path/header mismatch, `Kind:`, reverse conformance dependency (rule → less stable rule or
  rule facet, only `Framework binding: \`<facet>\`` exempt) all fail; forward dependency passes.
- **Capabilities (G2):** fifth slot row and fifth slot directory fail; empty required selection fails; missing required
  facet (from contract) fails; facet metadata mismatch fails; implementation leaks (workflow and non-module Level 2)
  fail; `binds:` removed from manifest fails; removed from manifest **and** contract still fails (content evidence);
  frame binding a leaf fails; frontend cleared in a sandbox → checker PASS, architecture check runs, real pre/post hooks
  work, zero residual frontend-module tokens; final output keeps all four selections (persistence provider sqlserver);
  architecture checker catches outward refs, inner-role persistence packages, prod→test refs, single-quoted XML.
- **Hooks (G3):** exact exec-form registrations; checker rejects six broken configurations; PreToolUse fails closed in
  six failure modes; post/Stop crashes stay non-blocking; manual checkers work from 4 locations × 2 shells.
- **Routing (G4):** 70 table rows + deny-once/retry/ask semantics; restore-only and unrelated commands stay silent
  (`npm ci`, `dotnet restore`, `dotnet package list --vulnerable`, `git commit -m "npm install x"`, `echo …`).
- **Actual state (G5):** real Git repo + real linked worktree, directories with spaces, `GIT_CEILING_DIRECTORIES` from
  the first Git call: Bash/PowerShell success and failure, unrecognized command text, first and later HEAD transition,
  same-path rewrite, tracked delete, rename, skipped paths (`node_modules`, `bin`, nested repo) without false removals,
  unchanged calls quiet without state rewrite, nested cwd, Edit hook in worktree, Pre state per worktree.
- **Encoding/Stop (G6):** 22/22 as listed in §4.

Process level vs host semantics: hooks run as real processes with real inputs; the harness emulates documented host
behavior (exec form, `${CLAUDE_PROJECT_DIR}` substitution as data, exit-code/JSON interpretation, `onFailure`, timeout).
Live Claude Desktop hook activation was not tested (not required).

## 9. Baseline demonstration (run once against a copy of Run-02)

Same harness: G1 51/128 pass (the baseline checker accepted every negative fixture except the bare `Docker` (M08) and
`Serilog` (A07) sentences; the passes are the positive controls);
G2 17/26 (reverse dependency, fifth slot dir, binds removal, frame→leaf binds undetected); G3 6/26 (no exec form,
no fail-closed, no PostToolUseFailure, nested-cwd `MODULE_NOT_FOUND`); G4 42/70 (all reference forms, global options,
wrappers missed; `echo npm install x` falsely denied); G5 9/18 checked (no shell actual-state validation at all);
G6 8/22 (BOM/UTF-16, quotes, Stop dedup, nested-cwd Stop launch).

## 10. Complexity and V2

+1 instruction file (Level-2 binding owner required by D1); hooks renamed, not multiplied (3 hooks + 1 policy file as
before). Byte growth +52.7 KB is almost entirely deterministic enforcement: `check-instructions.mjs` 16.0→40.5 KB
(neutrality grammar, binds, contracts, conformance, hook validation), `lib/project.mjs` 5.8→10.7 KB (roots, decoding),
hooks 9.7→28.4 KB (routing parser, snapshots, Stop fingerprints). Instruction prose is essentially flat; always-loaded
−27 chars. The checker's size is the main maintainability cost; it is commented and bounded to the frozen grammar.

## 11. Audits

- **Primary substantive audit:** found and fixed real template defects: P09 route entries after a same-sentence lead
  not recognized; generic `X<Program>` mis-stripped as placeholder (API-shape miss); `IGenericRepository` base name not
  matched; shared hook code still hardcoding the Angular CLI (moved to `frontend.enforcement`); `.angular`/`Vitest`
  frontend tokens in shared code; three binding lines restating policy (reworded as pure mappings); scaffolding
  lacked a pointer to the entry-point folder binding (added to `project-structure`); V2 test-technique table restored.
- **Oracle corrections (all before the confirmation audit, recorded):** G6 E01–E03 reused one command (identical
  retry is allowed by design); G3 timeout case not executable for shell-form baseline hooks on Windows; G5 crash when
  baseline lacked a state file; G7 strength heuristic now accepts a modal cue shared verbatim with the inventory
  wording (SEC-014 "prefer", DEP-002 "rather than") and DEP-005 anchors its "Approval…" heading. No expected verdict
  was changed.
- **Confirmation audit:** oracles frozen by hash (`1658d6a3…`), template hash `e11bcf8c…`; G1 129, G2 26, G3 26,
  G4 71, G5 24, G6 22, G7 4 → **302/302 pass**. Oracle and template hashes re-verified unchanged afterwards.

## 12. Known limitations (no known template defect)

1. The neutrality check is a bounded guard, not an English proof; a bare product name absent from the lexicon and
   from all derived sources and with no API shape (e.g. a hypothetical new library name) is caught only by review.
2. Command routing covers the documented forms; not pre-gated: package-manager config via environment variables,
   PowerShell `Start-Process` argument arrays, project creation/`dotnet sln add`, and reference edits performed by
   arbitrary scripts — the post-state hook still validates resulting manifests and runs the architecture check.
3. MSBuild properties are not evaluated (reported as findings, never trusted).
4. The first shell event in a worktree validates all manifests once and can report pre-existing issues once; non-Git
   projects use a stat-based scan, and Stop reports that co-change checks are unavailable once per state.
5. A broken selection record makes the critical PreToolUse gate block shell commands (fail closed, with a message;
   file edits remain possible).
6. The root-aware manual command needs Git; a template nested below a monorepo root is not covered by that form.
7. Reproduction for any of the above: inject the case into a fresh copy and run the checker or hook as in G1–G6.

## 13. Workspace events

No isolation violations. Platform-managed: the desktop session auto-listed the copied template's skills (never
invoked); one oversized command output (inventory printout) was persisted by the tool runtime and read back (own
output of an allowed input); background command logs were written by the runtime. Recoverable process incidents: one
orphaned hook process (baseline shell-form timeout) was terminated; the first baseline run was cut short by my own
900 s wrapper and G5/G6 were rerun once. `output/.work/` (harness, ledgers, sandboxes) was deleted after this report.

---

# Corrective pass — iteration 2

## Status: **STRICTLY_BETTER**

Both independently reproduced blockers are fixed, every preservation control in the fixed harness still passes, the
single final confirmation ran against the unchanged oracle (132/132), and no file outside the three permitted scripts
changed. Continued in place from the iteration-1 `output/template/`; nothing was taken from `baseline/template/`, L1
iterations 2–8 or other candidates.

## Hashes and files (`find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum -b | sha256sum`)

| | Files | Tree hash |
|---|---:|---|
| Start (iteration 1, verified once before editing) | 86 | `e11bcf8c00b884aabe8d4b6408f90f66c4ab2b67fab534fcc9dd66508702cc22` |
| Final (same before and after the confirmation run) | 86 | `cbabd288390b3d9b7eaf3d6264b460b21465ceeb1f5f46005c606d8f4ddd486b` |

Changed (only these; sha256 prefixes start → final):

- `.claude/scripts/check-instructions.mjs` (`6b76bc35` → `8fe5bb05`)
- `.claude/scripts/check-architecture.mjs` (`77f14c76` → `f755cf48`)
- `.claude/scripts/lib/project.mjs` (`81ec3e8b` → `2fdf409d`)

The other 83 files are byte-identical to iteration 1 (per-file hash comparison). No files were added or removed. Immutable inputs: `MANIFEST.sha256` 144/144 OK.

## Causes and repairs

- **Defect A (P4, heading content):** `neutralityCheck` skipped heading blocks
  (`if (block.type === 'heading') continue;`), so a heading that itself selects a technology was never checked.
  - **Repair:** headings now go through the same centralized check as paragraphs and list items. That covers technique-pointer grammar, technology vocabulary and API-shape identifiers.
  - **Governor role unchanged:** parsing is untouched, so each descendant still records the heading as its governing context.
  - **No new rules:** no new vocabulary, grammar or P6 reinterpretation was added.
- **Defect B (inner-role ASP.NET Core confinement):** `check-architecture.mjs` saw only explicit `<FrameworkReference>` elements.
  - **XML reader:** `parseCsproj` (`lib/project.mjs`) now also returns literal SDK names. It reads `<Project Sdk="A;B/ver">`, `<Sdk Name>` and `<Import Sdk>`, with single or double quotes; version suffixes are dropped and properties are not evaluated.
  - **Inner-role rule:** inner roles (domain-model, use-case-layer) now also reject:
    - an SDK that implicitly references a forbidden shared framework (fixed platform fact: `Microsoft.NET.Sdk.Web` → `Microsoft.AspNetCore.App`);
    - packages of a forbidden framework's family (`Microsoft.AspNetCore.App` → `Microsoft.AspNetCore.*`).
  - **Derived, not duplicated:** both checks come from the frame's existing `forbiddenFrameworkReferencesInInnerRoles`; the frame JSON and policy text are unchanged.
  - **Allowed roles unchanged:** the entry point (Api) and test roles are allowed as before.
  - **Reporting:** the post-change hook already calls `checkArchitecture`, so findings surface without hook changes.

## Fixed harness and results

One harness file in `output/.work/` held all expected verdicts. They were fixed before editing; oracle sha256 `d4faa6995be6ec6eb17ff97d90e7eb993e50234cbe57981a11db2663c622ee23`, verified unchanged before and after the confirmation. The oracle was not corrected at any point in this pass.

| Group | What | Pre-edit (demonstration) | Final confirmation |
|---|---|---|---|
| A-heading | 7 FAIL headings (`## Docker is required for deployment`, `## Selected deployment technology: Docker`, `## Must use Swagger`, `## Default logging provider: Serilog`, `## Use Docker for deployment` + neutral item, `## Docker`, `## Docker` + neutral item) and 3 PASS (`## Deployment technology`, `## HTTP API`, `## Technique: \`docker\``), each in `0-core/engineering.md` and `frame/boundaries.md` | 6/20 (all 14 FAIL headings falsely passed) | 20/20 |
| P4-matrix | Locked Section-3 matrix of `L1-Restart-REFINEMENT_TASK.md` (N01–N14, P01–P12 incl. variants), both levels | 76/76 | 76/76 |
| B-arch | Domain/Application with Web SDK (single/double quotes, `<Sdk>` element), `Microsoft.AspNetCore.Mvc.Core`, `Microsoft.AspNetCore.Authentication.JwtBearer` → FAIL. Explicit `FrameworkReference`, outward Domain→Api, EF Core in Domain/Application, production→test → FAIL. Clean graph, plain SDK with single quotes, Api with Web SDK + ASP.NET Core packages, integration tests → PASS | 8/17 (all 9 new FAIL cases falsely passed) | 17/17 |
| C-hooks | Real Git repo + linked worktree, launcher = main checkout: initial and unchanged events quiet; `PostToolUseFailure` Bash (Domain Web SDK, exit 3) and PowerShell (Application `Microsoft.AspNetCore.Mvc.Core`, exit 1) report the architecture finding; Api ASP.NET Core package quiet; PreToolUse unchanged (allow/ask) | 4/6 | 6/6 |
| D-struct | Clean template PASS with 0 violations/warnings and genuine pointers present; architecture check on template; four slots and selections; exact hook registrations; `binds:` removed from manifest, and from manifest + contract; fifth slot; reverse dependency; optional frontend cleared in a sandbox | 9/9 | 9/9 |
| E-integrity | All `.mjs` parse; 86 files; byte identity outside the permitted scripts; immutable manifest | 4/4 | 4/4 |

FAIL cases required the specific diagnostic, for example:
- `Level 0-core names concrete technology 'Swagger'`
- `domain-model must not use SDK 'Microsoft.NET.Sdk.Web', which implicitly references framework 'Microsoft.AspNetCore.App'`
- `domain-model must not reference package 'Microsoft.AspNetCore.Authentication.JwtBearer' of framework 'Microsoft.AspNetCore.App'`
- the hook output `Manifest state after failed Bash call: - architecture: backend/App.Domain/App.Domain.csproj: …`

## Evidence labels and policy identity

- **New in this pass:**
  - all results above, from real checkers and real hook processes;
  - hooks launched by the same controlled Node host emulation of documented exec-form semantics. No live Claude Desktop run was performed.
- **Policy identity (194 + GOV-017/GOV-018):**
  - every instruction, rule, skill, manifest, settings and hook file is byte-identical to iteration 1, so owner text, trigger and scope cannot have changed in this pass;
  - the 196-record owner/trigger/scope/strength audit itself is **previous evidence** (iteration-1 report above) and was not re-run independently here.
- **Previous evidence, not re-run:** Windows linked-worktree path/encoding/Stop experiments. The hook implementations are byte-identical, and the shared reader change only adds the `sdks` field.

## Limitations

- **Literal values only:** a project that reaches ASP.NET Core only through MSBuild properties, `Directory.Build.props/targets` imports or transitive packages is not detected.
- **Package-family rule:** this covers the forbidden framework family prefix (`Microsoft.AspNetCore.*`) and does not judge individual packages. A legitimately transport-free `Microsoft.AspNetCore.*` utility in an inner role would also be reported, so that case would need an approved exception.
- **Bounded guard:** the P4 heading check inherits the iteration-1 grammar limits (it is a bounded guard, not a natural-language proof).

`output/.work/` was deleted after this section was written; `output/` contains only `template/` and `REFINEMENT_REPORT.md`.

---

# Corrective pass — iteration_after_audit_1

## Status: **STRICTLY_BETTER**

The same-block pronominal selection bypass is closed at both eligible levels (Level 0 `0-core/engineering.md`, Level 1
`frame/boundaries.md`). Legitimate pointers and unrelated duties still pass. The representative previously frozen P4/P6
controls still hold. The other 85 files are byte-identical. The single final confirmation ran clean (148/148) against
the oracle frozen before the checker was edited. Work continued in place from the iteration-2 `output/template/`;
nothing was taken from `baseline/template/`, earlier L1 branches or other candidates.

## Hashes and files (`find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum -b | sha256sum`, inside `output/template/`)

| | Files | Tree hash |
|---|---:|---|
| Start (iteration 2, verified once before editing) | 86 | `cbabd288390b3d9b7eaf3d6264b460b21465ceeb1f5f46005c606d8f4ddd486b` |
| Final (same before and after the confirmation run) | 86 | `5ef3bc0a2ab1da1b715040ced1ab9f448691f79945712566e8d77e9a7050ed68` |

- Changed (only): `.claude/scripts/check-instructions.mjs`, sha256 `8fe5bb0584fedbae20764ab5708dc7012b701867a6cc0989d5ea334fbc0ad856` → `ef9b2dc0c1015ba7d8e7ca9dcf2ef6a3c37ecf95b5993b0f0571d57678195065` (40,759 → 43,253 bytes).
- The other 85 files match the per-file inventory captured before editing. No file was added or removed.
- Immutable inputs: `MANIFEST.sha256` 144/144 OK.

## Reproduced flaw (untouched checker, same frozen harness)

- `### Deployment technique` + `Technique: \`docker\`. This is the selected deployment technology.` → PASS (wrong) in both levels.
- `… That is the chosen deployment technology.` → PASS (wrong) in both levels.
- `Technique: \`docker\`.` and `Technique: \`docker\`. Must run unit tests.` → PASS (correct).
- `Technique: \`docker\`. Must use this technique.` → FAIL (correct).
- Whole pre-edit run: 102/148. All 46 misses are rows of this invariant: N01–N07, N09a/b, N11b and M01–M13, each at both levels. No positive or preservation row missed, and no case failed for a setup reason.

## Root cause

- **Recognition gap:** `REFERENTIAL` recognized a reference to a pointer only as a determiner followed by a listed head noun (`this technique`, `the above tool`), with at most two words between them.
- **Effect:** a demonstrative or personal pronoun used *without* a head noun (`This is the selected …`, `It is the default …`, `Use it for …`) was never connected to the pointer. The selecting sentence was treated as unrelated text, and the `docker` token stayed masked.
- **Accidental coverage:** `This is the technology` happened to match within the two-word gap; `This is the selected deployment technology` did not.

## Exact change (`check-instructions.mjs` only, +26 lines)

- **New constants** (next to `REFERENTIAL`):
  - `DEMONSTRATIVE`: the existing determiner set (`this|that|these|those|the above|the preceding|the previous|the following|below`).
  - `PRONOUN_SUBJECT`, `PRONOUN_OTHER`: where such a word counts as a bare pronoun (defined below).
- **`pronominalBinding(clause)`:**
  - Requires a word from the existing `MODALITY` set (`hasModality`). No new modality vocabulary was added.
  - Returns which pointers the clause binds: `all`, `back` or `forward`.
- **`techniquePointerViolations`:**
  - Collects these binders over the pointer's existing connected context, in reading order: earlier sibling items, the block's own `;`/`·` clauses, later sibling items. Ancestors with modality already poison the pointer, as before.
  - A covered pointer loses its mask and gets the regular diagnostic: `Level … names concrete technology 'docker' (bound by a pronominal selection or requirement in the same block or sibling items)`.
  - The clause split was factored into `clausesOf`; the regex is the same.
- **Unchanged:**
  - block parser and the six structural forms;
  - `pointerForm` and `referenceLabel` grammar;
  - `REFERENTIAL` and `MODALITY`;
  - governor/poison rule, generic-item governor rule and sibling handling;
  - resolved-skill requirement, technology vocabulary and API-shape detection;
  - all non-neutrality checks.

### Bounded predicate (frozen grammar, no general parser)

A clause carrying modality binds pointers through a **bare** pronominal reference, in one of two positions:

1. **Clause-initial subject** binds `all` pointers of the block and its sibling items:
   - Optional leading phrase of at most 4 words ending in `,`/`:`.
   - Optional connective: `and|but|so|thus|hence|therefore|then`.
   - Then a `DEMONSTRATIVE` word or `it`/`they`.
   - Followed by a finite `be`/modal/`have` form, `becomes|remains|stays`, or `'s`.
   - Rationale: a clause-initial subject has no antecedent inside its clause, so the bounded grammar cannot rule out any pointer.
2. **Elsewhere in the clause** binds pointers *before* it (`the following`/`below`: pointers *after* it):
   - `it`/`them`; or
   - a `DEMONSTRATIVE` word standing alone before punctuation, clause end or a preposition (`use this for …`).
   - Rationale: direction keeps an in-clause antecedent local. For example, `code-review`'s `… may not have them loaded …` precedes its route entries and does not bind them.

No antecedent is ever chosen. With several candidate pointers, all lose the exemption (N11b).

Scope is the same block and its sibling items:
- **Same block:** a paragraph (including wrapped lines), a list item (including continuation lines), a heading or a table row.
- **Sibling items:** items under the same parent.
- **Not in scope:** remote anaphora, cross-block or cross-section resolution, and new Markdown forms.

## Fixed harness and results

One table-driven harness lived in `output/.work/`. It ran the real checker for every case in a fresh copy of `output/template/`. Each fixture was injected into its own explicitly neutral section (`## Technique references` / `### Deployment technique`), except where the case brings its own governor:
- N10/R-N04/R-N05/R-N11 bring a normative heading.
- R-N14 is injected into the existing generic list: `Engineering Discipline` in L0, `Domain` in L1.

Verdict rules:
- **FAIL:** exit 1, and every violation is a neutrality diagnostic for the injected Level 0/1 file, and at least one names the case technology (`docker`/`swagger`, case-insensitive). Mutation rows require their specific diagnostic.
- **PASS:** 0 violations and 0 warnings.

Oracle freeze:
- Oracle (harness sha256 `b29d538950b07c954ca5b3884afcbdd3555fb74f9edb14e1a3bbfce42a221f69`) and pre-edit inventory (`cbb485ea…`) were frozen before the checker was edited, and verified before each run.
- Its tree computation reproduced `cbabd288…`.
- Correction before freezing: the S07/S08 allow-lists also accept the frame manifest's own Level-1 neutrality diagnostic, because that manifest is Level 1.
- No expected verdict was changed after freezing.

| Group | Rows (cases × L0/L1) | Pre-edit | Final confirmation |
|---|---:|---:|---:|
| **N** — N01–N05 (`This is the selected` / `That is the chosen` / `It is the default` / `This must be used` / Swagger `This is the preferred`), N06 line wrap, N07 heading + paragraph, N08 `Must use this technique` sibling, N09a/b selection with neutral siblings before/after, N10a–c (`Selected …: Technique:`, `### Selected deployment technology`, `## Must use Swagger`), N11a/b two techniques + `This technology is selected` / `This is the selected …` | 30 | 10 | **30** |
| **M** — FAIL metamorphic: list item, separate sibling item, intervening neutral sentence, all-caps, `;` clause, Swagger sibling `It is the preferred …`, `Use it for deployment`, `Must use this for deployment`, selection *before* the pointer, `The following is …`, list continuation, nested siblings, `thus, it is the Default …` | 26 | 0 | **26** |
| **P** — P01–P05, P06a/b neutral siblings either order, P07a/b nested list with continuation and colon lead-in, P08a–c genuine `development-workflow` aside, `code-review` route map and `build-fix` footnote (verbatim, both levels; the aside's `frontend.commands` item omitted because it is a reverse conformance dependency inside a rule), P09a/b `;` clauses and parenthesized aside | 28 | 28 | **28** |
| **PM** — PASS metamorphic: `Must run unit tests` as sibling/`;` clause/preceding sentence, wrapped description, `It is described in the skill.`, `MUST RUN UNIT TESTS.`, duty before pointer + neutral sibling, `It covers …` | 16 | 16 | **16** |
| **R** — original N01, N02, N04–N06, N08–N14, P03, P06 representatives; heading `## Docker is required for deployment`; `Technique: \`Docker\``; `iexceptionhandler` | 34 | 34 | **34** |
| **S** — `.mjs` syntax (6); P10 clean template (68 artifacts, 0/0); genuine pointers present in place; architecture check; four slots/selections; exact hook registrations incl. `onFailure: "block"`; `binds:` removed from manifest, and from manifest + contract; frame-terms + placement-examples cannot legalize technology; byte identity; manifest; charset; output hygiene | 14 | 14 | **14** |
| **Total** | **148** | **102** | **148** |

- The development run after the edit (`dev-1`) was already 148/148. No code or oracle correction followed.
- The final confirmation re-ran the identical harness on the identical checker.
- The architecture check reports `NOT APPLICABLE (no backend directory)` on the empty template. This is not a functional .NET pass.

## Evidence labels

- **Independent in this pass:** every row above (real checker, fresh copies, both levels), plus the controlled mutations of `binds:`, frame terms and placement examples.
- **Inherited, not re-run:**
  - **Policy audit:** the 196-policy owner/trigger/scope/strength audit (iteration 1). All normative and owner files are byte-identical in this pass, so policy text cannot have changed. This pass does not claim a fresh semantic re-audit of the 196 policies.
  - **Behavior suites:** hook behavior (routing, actual state, worktrees, encodings, Stop) and functional architecture/integration checks (iterations 1–2). Hooks, settings and `lib/project.mjs` are byte-identical.
- **Level 0/1 content:** unchanged. Iteration 1's content audit still applies, and the clean template passes under the stricter rule (no genuine pointer newly rejected).
- **Unchanged by byte identity:**
  - D1–D17 dispositions, L1 identity, the four static slots and their selections, and `binds:`.
  - Always-loaded footprint and English-only runtime artifacts. The checker's new code adds no new non-ASCII characters and is English-only.
- **Live Claude Desktop:** no live session was tested.

## Known boundaries (observed, informational rows B01–B05; not acceptance rows)

- **B01 — PASS, elliptical fragment:** `Technique: \`docker\`. Selected for deployment.` has a zero anaphor and no pronoun, so it is outside the bounded grammar.
- **B02 — PASS, cross-block:** the selection in a *separate paragraph* after the pointer. Paragraphs remain self-contained statements (unchanged rule).
- **B03 — PASS, child item:** a child item under a pointer lead-in (`**Deployment change** (technique: \`docker\`)` + `- This is the selected deployment technology.`). Governed child content is not part of the pointer's connected context; `REFERENTIAL` has the same pre-existing boundary.
- **B04 — PASS, unlisted head noun:** a demonstrative with a head noun outside `REFERENTIAL`'s noun list (`This image is required for deployment.`). The noun list was deliberately not expanded.
- **B05 — FAIL by design, fail closed:** an extraposed `It is mandatory to run unit tests.` connected to a pointer. An expletive `it` is not distinguished from a referential one. Write independent duties imperatively (`Must run unit tests.`, P04) or in a separate block.
- **Design consequence, not separately tested:** a modal clause with `it`/`them` after a pointer in the same block (e.g. `Must run unit tests against it.`) also loses the exemption.
- **Nature of the check:** a bounded deterministic guard, not a proof about all English. Content review remains necessary for paraphrases outside these forms.

`output/.work/` (harness, ledgers, sandboxes) was deleted after this section was written; `output/` contains only
`template/` and `REFINEMENT_REPORT.md`.

---

# Corrective pass — iteration_after_audit_2 (deliberate P4 contract change)

## Status: **READY_TO_FREEZE (contract harmonization complete)**

This pass implements a **user-approved, intentional change of the P4 acceptance contract**, harmonizing L1-Restart's
Level 0/1 technology-neutrality policy with Candidate L0. It is **not** a newly discovered L1 defect and not an
architecture feature. The pure-pointer exemption of the earlier Restart contract is withdrawn: Levels 0 Core and
1 Architecture now name no concrete implementation technology in any form, including `Technique: <skill>`,
`See technique: <skill>`, `area → <skill>`, headings, lists, tables, code spans/fences and links. The frozen harness
passed 147/147 in the single final confirmation; the clean template passes with 68 artifacts, 0 violations and
0 warnings. Work continued in place from the `iteration_after_audit_1` template; nothing was taken from
`baseline/template/`, earlier L1 branches or other candidates.

**Methodology disclosure (must accompany any candidate comparison):** this is an *evolved acceptance criterion*.
The sections above were produced, and their results are valid, under the earlier P4 semantics (pure named pointers
to Level-2 technique skills allowed; ASP.NET Core and NuGet treated as fixed platform). They are kept unchanged as
research history. No claim is made that the original runs used the harmonized P4 semantics; future comparisons must
apply the harmonized contract below to every candidate.

## Old vs. new P4 contract

| Aspect | Previous Restart contract (§5, iteration 2, iteration_after_audit_1) | Harmonized contract (this pass) |
|---|---|---|
| Pure pointer to a concrete Level-2 skill (`Technique: \`docker\``, `See technique: \`swagger\``, `Containers -> \`docker\``, `(technique: … \`docker\`)`) | PASS when the bounded grammar proved it pure and non-normative | **FAIL** in every form; no wrapper, governor or context masks the token |
| Neutral role/capability/facet/topic reference (`backend-testing.framework`, `architecture.check`, `http-api`, `ci-cd`, "the Level-2 container technique") | PASS (as pointer) | PASS in any form |
| Fixed platform at Levels 0/1 | .NET, C#, ASP.NET Core, NuGet, HTTP, Git | .NET, C#, TypeScript, Git; HTTP as protocol vocabulary. **ASP.NET (Core) and NuGet are not exempt** |
| Level-2 skill name | every Level-2 skill name was "technique"; only pure pointers masked | a skill name is technology only when it names one (`docker`, `swagger`, `ef-core`, `aspnet-error-handling`, `httpclient-factory`, `angular`); abstract topic names stay neutral |
| Level 2 / Level 3 | concrete technique, bindings, selections allowed | unchanged (Docker/Swagger/EF Core skills and project selections untouched) |
| API shapes, module leak tokens, package ids, frame no-legalizing, `binds:` | enforced | enforced unchanged; matching made formatting-invariant (below) |

## Hashes and files (`find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum -b | sha256sum`, inside `output/template/`)

| | Files | Tree hash |
|---|---:|---|
| Start (`iteration_after_audit_1`, verified before any edit; matched the expected digest) | 86 | `5ef3bc0a2ab1da1b715040ced1ab9f448691f79945712566e8d77e9a7050ed68` |
| Final (identical before and after the confirmation run) | 86 | `546fd8dda79391be9f1294a14ab86add5ce4c8605b314b7f79ccb576af3a1b25` |

Changed (exactly these 9; sha256 prefix start → final, bytes):

| File | sha256 | Bytes |
|---|---|---|
| `.claude/scripts/check-instructions.mjs` | `ef9b2dc0` → `d315eaba` (full: `d315eaba57aad4a4423b780a932572f103f7acb16d77b1b608e889c521660afc`) | 43,253 → 35,770 (689 → 575 lines) |
| `.claude/INSTRUCTION_MAP.md` | `8da42d0b` → `5d8fecf6` | 22,764 → 23,122 |
| `CLAUDE.md` | `e4cf41c0` → `6af28e0f` | 6,527 → 6,522 |
| `.claude/rules/1-architecture/frame/boundaries.md` | `713302dc` → `3f17329f` | 4,483 → 4,525 |
| `.claude/skills/build-fix/SKILL.md` | `120ef208` → `ce0524b6` | 7,620 → 7,651 |
| `.claude/skills/code-review/SKILL.md` | `da4901ca` → `5cc45407` | 6,676 → 6,727 |
| `.claude/skills/development-workflow/SKILL.md` | `4eee75f7` → `b383de16` | 3,554 → 3,580 |
| `.claude/skills/security-scan/SKILL.md` | `c6d2bf87` → `ac92de2a` | 6,982 → 6,995 |
| `.claude/skills/template-maintenance/SKILL.md` | `f3d6efed` → `39a1d4cf` | 2,732 → 2,914 |

The other 77 files are byte-identical to the start (per-file comparison against a start snapshot). No file was added
or removed. Immutable inputs: `MANIFEST.sha256` 144/144 OK at start and in the final run.

## Exact changes

### `check-instructions.mjs` (neutrality section only)

All diff hunks lie in the neutrality code: the lexicon constants, the removed pointer grammar, `neutralityCheck`
and its vocabulary wiring in `main`. Headers, levels, paths, conformance, slots, contracts, manifests, `binds:`,
leakage, facet/skill/path references, map coverage and hook-registration validation are untouched.

- **Removed (exemption machinery, 124 lines):** `maskCode`, `sentencesOf`, `MODALITY`/`hasModality`, `plain`,
  `referenceLabel`, `pointerForm`, `REFERENTIAL`, `DEMONSTRATIVE`/`PRONOUN_*`, `pronominalBinding`, `clausesOf`,
  `isReferenceGovernor`, `techniquePointerViolations`. `parseBlocks` is unchanged (still used by conformance and
  neutrality).
- **Vocabulary aligned with the L0 boundary:** added `ASP.NET`, `ASP.NET Core`, `NuGet`, `EF Core`,
  `Entity Framework`, `Entity Framework Core`; `NUnit` and `Angular` added so they stay recognized even when the
  corresponding module is not selected. `TypeScript` removed (L0 fixed platform). Derived sources unchanged:
  leaf-module leak tokens and enforcement package ids. API-shape exemption `PLATFORM_IDENTIFIERS` changed from
  `{NuGet}` to `{TypeScript}` (the only PascalCase fixed-platform name; NuGet loses its exemption).
- **Formatting-invariant matching (`technologyMatcher`, `normalizeForms`):** text is NFKC-folded; HTML comments/tags,
  soft hyphens/zero-width characters, emphasis/strike markers, backslash escapes and code-span backticks are
  removed; a term matches case-insensitively with any run of space/`.`/`-`/`_` (or none) between its alphanumeric
  chunks (`ASP.NET` ~ the `aspnet` in `aspnet-error-handling`; `ASP.NET Core` ~ `AspNetCore`; `Docker` ~ `docker-compose`), and a term
  without inner capitals also matches as a PascalCase/camelCase component (`Swagger` in `AddSwaggerGen`). Terms with
  inner capitals (`HttpClient`) match only whole, so generic wording such as "HTTP client" stays neutral.
- **`neutralityCheck`:** every block (heading, paragraph incl. wrapped lines, list item incl. continuation, table row,
  code fence) and the frontmatter `description` is checked for vocabulary on the normalized text and for API shapes
  on the code-unwrapped text; the whole frontmatter is additionally checked for vocabulary (tool names there are
  harness metadata, so no API-shape check). The frame-term API-shape allowance for frame-owned files is unchanged.
- **Frame no-legalizing:** `isTechnology` (frame-terms/placement-examples) now uses the same matcher, so an entry such
  as `SwaggerGen` is rejected as technology (previously only exact lexicon words were).

### Level 0/1 text normalization (pinpointed by the new check on the clean template, 14 diagnostics in 7 files)

| File (Level) | Before | After |
|---|---|---|
| `frame/boundaries.md` (1), ARC-002 | Keep Domain free of persistence-implementation, ASP.NET Core, HTTP, and external-service implementation concerns. | … persistence-implementation, **web-framework/transport-implementation**, HTTP, and external-service implementation concerns. |
| `frame/boundaries.md` (1), ARC-008 | … or ASP.NET Core transport types. | … or **web-framework/transport implementation types**. |
| `CLAUDE.md` (0) | template for an ASP.NET Core backend | template for a **.NET web backend** |
| `development-workflow` (0) | (technique: `ci-cd`, `docker`) | (technique: `ci-cd` and the Level-2 container technique) |
| `code-review` (0) | error handling → `aspnet-error-handling`; outbound HTTP → `httpclient-factory`; containers/CI → `docker` / `ci-cd` | error handling → the Level-2 error-handling technique; outbound HTTP → the Level-2 outbound-HTTP technique; containers/CI → the Level-2 container technique / `ci-cd` |
| `build-fix` (0) | Technique: `swagger`, `http-api`. | Technique: `http-api` and the Level-2 API-description technique. |
| `security-scan` (0) | `authentication`, `configuration`, `logging`, `aspnet-error-handling`, `http-api`, `httpclient-factory` skills | `authentication`, `configuration`, `logging`, `http-api` skills and the Level-2 error-handling and outbound-HTTP techniques |
| `template-maintenance` (0) | … beyond the platform vocabulary (.NET, C#, ASP.NET Core, NuGet, HTTP, Git). | … no concrete technology — not even in a pointer to a Level-2 skill — beyond the fixed platform vocabulary (.NET, C#, TypeScript, Git; HTTP as protocol vocabulary); they refer to Level 2 only by role, capability, facet, or a technique skill whose name identifies no technology. |

`INSTRUCTION_MAP.md` (Level 3 metadata, not a policy owner): the level rule now states the harmonized boundary
(no pointer exemption; fixed platform .NET, C#, TypeScript, Git, HTTP as protocol; ASP.NET Core and NuGet not exempt;
neutral reference forms), and the checker row reads "no pointer exemption; case-, separator- and Markdown-insensitive
vocabulary plus API shapes". All routing rows and file listings are unchanged.

Routing trade-off (accepted by the contract): four Level-0 workflows now reach the error-handling, outbound-HTTP,
container and API-description skills through neutral descriptions instead of their names; those skills stay
model-visible through their listing descriptions. No Level-2/3 rule or skill was changed.

## Prior fixtures whose expected verdict changed (deliberate oracle changes, not regressions)

| Prior fixture (source) | Previous expectation | New expectation | Why |
|---|---|---|---|
| §3.3 P01 `Technique: \`docker\`.`; P02 `See technique: \`docker\`.`; P03 `Containers -> \`docker\`.` | PASS | FAIL | pure pointer exemption withdrawn |
| §3.3 P04 `### Deployment technique` + pointer; P05 (+ neutral siblings); P06 `- Deployment technique:` + nested pointer; P07 pointer + `Must run unit tests.` | PASS | FAIL | the `docker` token itself is disallowed regardless of governor/siblings |
| §3.3 P08 genuine `development-workflow` aside `(technique: \`ci-cd\`, \`docker\`)` | PASS | FAIL (`docker`); template text migrated | same |
| §3.3 P09 genuine `code-review` route map (`docker`, `aspnet-error-handling`, `httpclient-factory` entries) | PASS | FAIL for those entries; template text migrated (neutral entries such as `http-api`, `ci-cd` still pass) | implementation-bearing skill names |
| §3.3 P10 genuine `build-fix` footnote `Technique: \`swagger\`, \`http-api\`.` | PASS | FAIL (`swagger`); template text migrated | same |
| §3.3 P11 formatting variants of a pure `docker` pointer; P12 `swagger` pure pointer + `;` clauses | PASS | FAIL | P6 formatting invariance now preserves FAIL for concrete tokens and PASS only for neutral references |
| §5 metamorphic "neutral reformatting must not turn a pure pointer into FAIL" | PASS rows | FAIL for concrete pointers; still PASS for neutral references (PF1–PF4) | same |
| iteration 2 A-heading `## Technique: \`docker\`` | PASS | FAIL | headings get no exemption |
| iteration_after_audit_1 groups P (28 rows) and PM (16 rows), R-P03/R-P06 | PASS | FAIL | every row contains a `docker`/`swagger` pointer |
| iteration_after_audit_1 informational B01–B04 (observed PASS) | PASS (observed, not acceptance) | FAIL | the pointer token alone fails; the grammar boundary is moot |
| Any earlier row relying on ASP.NET Core or NuGet as Level 0/1 platform vocabulary | PASS | FAIL | L0 boundary: ASP.NET and NuGet are not exempt (the exact text of earlier platform rows such as iteration-1 A10 is not retained; stated conditionally) |
| `TypeScript` at Level 0/1 (iteration-1 D1 treated it as technology) | FAIL | PASS (P07a) | L0 fixed platform includes TypeScript |
| N01–N14 of §3.3, iteration_after_audit_1 N/M/R-N rows, B05 | FAIL | FAIL (now unconditional) | unchanged |

In this pass's harness, 19 cases × 2 levels = **38 rows** carry a previous-contract PASS expectation that is now FAIL
(N01, N02, N03a, N03b, N04, N06, N08b, N09a, N10a–e, N11b, F06, F07, F16, F17, F18), and P07a × 2 = **2 rows**
changed FAIL → PASS. (The harness's own `old` annotation also marked N09b/N09c as previously PASS; the pre-edit run
shows they already failed under the old grammar because `- Deployment:` is not a reference label, so its printed
"42" overstates by 4. This is an annotation error only; no expected verdict depends on it.)

## Fixed harness and results

One table-driven harness in `output/.work/` ran the real checker for every row in a fresh copy of `output/template/`.
Fixtures were appended to Level 0 `0-core/engineering.md` and Level 1 `frame/boundaries.md` under an explicitly neutral
`## Technique references` heading (or with their own heading), with metadata and original content retained.

- **FAIL rule:** exit 1, a `Level … names concrete technology '<token>'` diagnostic on the injected file whose token
  matches the target (`docker`, `swagger`, `asp…net`, `nuget`, `ef…core`, …), and no other violation except
  same-token co-diagnostics (module leak; unknown skill name such as `docker-compose`).
- **PASS rule:** exit 0, 0 violations, 0 warnings.
- **Oracle freeze:** first frozen at sha256 `71315804…`; the first pre-edit run (95/147) showed that F12's
  `Technique: \`docker-compose\`` also legitimately triggers the unknown-skill diagnostic for the same token, so —
  still before any template edit — the FAIL rule was corrected to accept that same-token co-diagnostic (expected verdict
  unchanged) and re-frozen at sha256 `7c6e4037fb9712786938b461139a24376b5fef6a6f53723cdfe154e445dd5a86`, verified before
  every later run. No expected verdict was changed at any time.

| Group | Rows | Pre-edit (unmodified checker, frozen oracle) | Final confirmation |
|---|---:|---:|---:|
| **N** — N01–N11k: `Technique:`/`See technique:`/`->`/`→` pointers, pointer + selection sentence, heading + list pointer, `## Must use Swagger`, `Selected technology: \`swagger\``, list/nested-list forms with neutral siblings inserted/removed, `ASP.NET Core`, `asp.net core`, `NuGet`, `` `nuget` ``, `` `aspnet-error-handling` ``, EF Core / `` `ef-core` `` / `efcore` / Entity Framework Core, NUnit, `## Angular`, `IActionResult`, `JsonSerializerOptions` (not in lexicon: API shape), Vitest (module token), `Microsoft.EntityFrameworkCore` (package id), `` `httpclient-factory` `` | 62 | 32 | **62** |
| **F** — case/format invariance (Docker and Swagger): `` `Docker` ``, `` `DOCKER` ``, `**Docker**`, `` `SWAGGER` ``, `*Swagger*`, `### Technique: \`docker\``, `#### See \`swagger\``, wrapped line, table row, code fence, Markdown link, `` `docker-compose` ``, `**Dock**er`, `Dock<!-- x -->er`, zero-width split, original P08 aside, P09/P12 route + `;` clause, P10 footnote | 36 | 18 | **36** |
| **P** — P01 `Use the deployment technique chosen at Level 3.`, P02 `See the Level-2 deployment guidance.`, P03 capability-selected implementation, P04 `Framework binding: \`backend-testing.framework\`.`, P04b `Mechanical check: \`architecture.check\`.` (L1 only: Level 0 → Level 1 facet is a reverse dependency), P05a–c `http-api` reference/route and `` `ci-cd` ``, P06 `Must run unit tests.`, P07a TypeScript, P07b .NET/C#/Git/`` `git status` ``, PF1–PF4 neutral heading/list/nested/table/wrapped forms; P08a–e concrete `docker`/`swagger`/`ef-core`/ASP.NET Core/NuGet content in Level-2 skills/rules and Level-3 decisions/package-management | 34 | 32 | **34** |
| **S** — `.mjs` syntax (6 files); P09 clean template 68 artifacts 0/0; architecture check; four slots and selections; byte identity outside the 9 permitted files; exact hook events and PreToolUse `onFailure: "block"`; `binds:` → `none` (contract requires-binds) and with `requires-binds` removed (content evidence); frame-terms `Docker` + placement-examples `SwaggerGen` rejected and a frame-owned `docker` pointer still fails; reverse dependency; fifth slot directory; optional frontend cleared → PASS (63 artifacts); manifest 144/144; no new non-ASCII characters; ARC-002/ARC-008 line-level semantic diff | 15 | 13 | **15** |
| **Total** | **147** | **95** | **147** |

- **Pre-edit misses (27 cases)** are exactly the intended change: the 19 previous-contract PASS cases above; formatting
  evasions that the old matcher did not see (`efcore`, `docker-compose`, `**Dock**er`, HTML-comment split, zero-width
  split); TypeScript (P07a, old FAIL); `SwaggerGen` accepted as a placement example (S08a); and the boundaries edit
  (S14).
- **Development run `dev-1`: 146/147.** S13 caught a real defect of my edit: the tool call had decoded the `­…﻿`
  escapes of the new character class into literal invisible characters in the checker. Rewritten as ASCII escapes;
  research wording ("Candidate L0") was also removed from two checker comments. These were the only corrections.
- **Final confirmation: 147/147** on the identical frozen harness; tree hash `546fd8dd…` identical before and after.
- The architecture check reports `NOT APPLICABLE (no backend directory)` on the empty template (not a functional .NET
  pass).

Representative final diagnostics:
- `.claude/rules/0-core/engineering.md: Level 0-core names concrete technology 'docker' (technology vocabulary); …` (N01)
- `.claude/rules/1-architecture/frame/boundaries.md: Level 1-architecture names concrete technology 'ASP.NET' …` (N10a)
- `.claude/rules/0-core/engineering.md: Level 0-core names concrete technology 'aspnet' …` (N10c, `` `aspnet-error-handling` ``)
- `…/clean-architecture/MODULE.md: placement-examples entry 'SwaggerGen' is technology vocabulary; …` (S08a)

## Comparison with Candidate L0's contract

The comparison is against the agreed L0 *policy* as stated in the task (Levels 0/1 name no concrete technology
outside the fixed platform; its checker bans Docker, Swagger, ASP.NET, NuGet and EF Core there). L0's code was not
available inside the L1 workspace and was not read or copied. All five L0-banned names now fail at Levels 0/1 in every
tested form (N01–N11, F01–F18), and .NET, C#, TypeScript and Git pass (P07). L1 keeps its stronger, additional
guards: the wider lexicon, template-derived module tokens and package ids, deny-by-default API shapes, case/separator/
Markdown-invariant matching, frame-term no-legalizing, and the unchanged leakage, `binds:` and conformance checks.
No platform exception was added; the API-shape exemption moved from NuGet to TypeScript only.

## Policy preservation (196 = 194 inventory + GOV-017/GOV-018)

- **Byte-identical owners:** 77 template files, including every Level 2/3 rule and skill, all hooks, settings,
  `lib/project.mjs` and `check-architecture.mjs`; their policies cannot have changed.
- **Edited inventory-owner text (semantic comparison):** ARC-002 and ARC-008 in `frame/boundaries.md`. Owner
  (frame facet `architecture.boundaries`), trigger (`paths: backend/**/*`, unchanged), scope (backend), strength
  (MUST / MUST_NOT) and condition (none) are unchanged. Only the concrete name of the decided web framework is replaced
  by its role, "web-framework/transport implementation"; the prohibition on inward framework/transport leakage is
  intact. The concrete binding stays at its owners: the decided stack in Level-3 `decisions.md` and the API bindings in
  Level-2 `backend-platform.md`; mechanical enforcement (`architecture.check` forbids `Microsoft.AspNetCore.App` and
  its package family in inner roles) is byte-identical.
- **Other edited lines** are routing or descriptive text, not inventory policy anchors: the `CLAUDE.md` template
  description; the `development-workflow` technique aside (the CI/CD obligations under it, incl. WF-019, are
  unchanged); the `code-review` knowledge-routing sentence (WF-011/WF-012 unchanged); the `build-fix` technique footnote
  (WF-016 unchanged); the `security-scan` deeper-technique pointer (WF-020/WF-021 unchanged); the `template-maintenance`
  level-placement sentence, updated to the new contract.
- **Not performed:** a fresh full 196-record owner/trigger/scope/strength audit. The iteration-1 audit remains the
  evidence for unchanged files; this pass adds the line-level semantic comparison above.

## D1–D17 and structure

- D1/D2 are the subject of this pass (content normalized; checker aligned). D3–D14 mechanics (PreToolUse
  `onFailure: "block"`, PostToolUseFailure, actual-state tracking, worktrees, encodings, Stop dedup) are in
  byte-identical files; their behavior suites are **inherited, not re-run**. D15: four slots, selections, contracts,
  `binds:` mutations, fifth-slot rejection and optional-frontend clearing re-verified (S04, S07a/b, S10, S11).
  D16: no Level-2 technique changed. D17: always-loaded surface −5 characters (`CLAUDE.md` line 5); skill and agent
  descriptions unchanged.
- English only; no new non-ASCII characters in any changed file (S13); `output/` hygiene below.

## Threat model and limits of the deterministic check

- It recognizes **known** technology: the lexicon, template-derived module tokens and package ids, and API-shaped
  identifiers. A bare product name in none of these (a hypothetical new library), a paraphrase without a token ("the
  container engine of the chosen vendor") or a Level-2 skill whose name is not technology vocabulary is not detected;
  such skill names are treated as neutral topics (e.g. `ci-cd`, `logging`). Content review stays necessary.
- Homoglyphs from other scripts are not folded (NFKC does not map Cyrillic look-alikes); a term split by characters
  that are not removed or tolerated (e.g. `Dock.er` inside a single-chunk term) is not matched. The API-shape check
  does not strip emphasis markers (the vocabulary check does).
- Fail-closed costs: generic English words that are vocabulary (`controller`, the package id `bootstrap`) fail at
  Levels 0/1 even when used generically; write role wording instead.
- No semantic understanding of natural language is claimed; within recognized vocabulary there is no exemption by
  phrasing, wrapper, governor or Markdown form.

## Evidence labels

- **New in this pass:** every harness row above (real checker, fresh copies, both levels), the dry scan that
  pinpointed the 7 Level 0/1 files, the per-file byte comparison, the manifest check, and the line-level semantic
  comparison of ARC-002/ARC-008.
- **Inherited, not re-run:** hook behavior suites (routing, actual state, worktrees, encodings, Stop), functional
  architecture checks on real projects, the 196-policy audit, V2 technique review. No live Claude Desktop session was
  tested.

`output/.work/` (harness, start snapshot, sandboxes, results) was deleted after this section was written; `output/`
contains only `template/` and `REFINEMENT_REPORT.md`.

---

# Corrective pass — iteration_after_audit_3 (lexical parity: Jest, Scrutor)

## Status: **READY_TO_FREEZE (pending independent verification)**

A minimal lexical parity correction of the harmonized P4 contract; no architectural, policy or contract change. The
independent audit found that `Must use Jest.` and `Must use Scrutor.` passed at Level 0 and Level 1, while Candidate L0
rejects both. Both misses were reproduced on the untouched checker; adding the two names to the existing
`TECHNOLOGY_LEXICON` closes them. The frozen 76-row harness passed 76/76 after the edit and in the single final
confirmation; the clean template passes with 68 artifacts, 0 violations and 0 warnings. Work continued in place from the
`iteration_after_audit_2` template; nothing was taken from `baseline/template/`, earlier L1 iterations or other candidates.

## Starting state (verified once, before any edit)

- `output/template/`: 86 files. Checker sha256 `d315eaba57aad4a4423b780a932572f103f7acb16d77b1b608e889c521660afc`,
  equal to the value recorded in the task.
- Tree hash with the documented method (below): `546fd8dda79391be9f1294a14ab86add5ce4c8605b314b7f79ccb576af3a1b25`,
  equal to the final hash of `iteration_after_audit_2`. Root `MANIFEST.sha256`: 144/144 OK.
- Occurrences in the template: `Jest` none; `Scrutor` only in the Level-2 `dependency-injection` skill (description and
  decorator bullet), where concrete technology is allowed.

## Observed initial misses and root cause

On the untouched checker the frozen harness gave **30/76**; the 46 misses are exactly the Jest/Scrutor rows (groups A
and F below): 42 returned `PASS (68 artifacts, 0 violation(s), 0 warning(s))`, and the 4 pure-pointer rows
(`` Technique: `jest`. ``, `` Technique: `scrutor`. ``, both levels) exited 1 **only** with the pre-existing
`references unknown skill or agent 'jest'`/`'scrutor'` diagnostic and no neutrality diagnostic, so they do not count
as rejections. Every regression, positive and smoke row already met its expectation.

Root cause: recognized technology at Levels 0/1 is the lexicon, plus template-derived leaf-module leak tokens and
enforcement package ids, plus API-shaped identifiers. `Jest` and `Scrutor` are in none of these sources: they are absent
from the lexicon, are not leak tokens or package ids of the selected modules, and as single-capital words without inner
capitals, generics, brackets or call syntax they match no API shape. The Markdown block parser is not involved: the
same shapes containing `Docker`, `Swagger`, `NUnit`, `EF Core`, `ASP.NET Core` and `NuGet` were rejected in the same
pre-edit run (group R).

## Exact change (one file, two tokens)

`.claude/scripts/check-instructions.mjs`: `'Scrutor'` inserted after `'Kommand'` on lexicon line 30 and `'Jest'`
inserted after `'Playwright'` on lexicon line 31. 575 → 575 lines; 35,770 → 35,789 bytes (+19 = `, 'Scrutor'` +
`, 'Jest'`); sha256 `d315eaba…` → `8171ce3941aba33d75a0b609d9d0c8a3f8761ad574b8a709209be6c219c55663`. Removing exactly
those two inserted tokens reproduces `d315eaba…` byte for byte, so nothing else in the file changed: the matcher,
`normalizeForms`, `API_SHAPES`, `PLATFORM_IDENTIFIERS` (`TypeScript` only), derived module tokens/package ids, the
frame no-legalizing rule and every other check are untouched. No pointer or context exemption was reintroduced, no
platform exception was widened, and no other vocabulary was added or merged from L0.

Both terms inherit the existing matching: case-insensitive, whole alphanumeric chunks (so `jestful` and `scrutinize`
do not match), Markdown/HTML/zero-width insensitive, and — as hump-free terms like `Docker` — also matched as a
PascalCase/camelCase component (`JestConfig` would be flagged).

## Hashes and files (`find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum -b | sha256sum`, inside `output/template/`)

| | Files | Tree hash |
|---|---:|---|
| Start (`iteration_after_audit_2`, verified before any edit) | 86 | `546fd8dda79391be9f1294a14ab86add5ce4c8605b314b7f79ccb576af3a1b25` |
| Final (after the final confirmation run) | 86 | `41084c6bab8399a7148d39b8c1d293dd52045b0c17083c9b8bd9aca7a1beb436` |

- Changed: only `.claude/scripts/check-instructions.mjs` (above). The other **85 files are byte-identical** (per-file
  sha256 comparison against a start snapshot: exactly one differing line, for the checker); no file added or removed.
- Persistent changes outside the template: only this appended section of `output/REFINEMENT_REPORT.md`.
- Immutable inputs: `MANIFEST.sha256` 144/144 OK in the final confirmation (it covers `CANDIDATE.md`, `GOAL_PROMPT.txt`,
  `PROVENANCE.json`, `README.md`, `REFINEMENT_TASK.md`, 8 `audit/`, 88 `baseline/`, 43 `source/` files). The later root
  task/prompt files are not in the manifest; this pass read them and did not write them.

## Fixed harness and results

One table-driven harness in `output/.work/` ran the **real checker** of a fresh full copy of `output/template/` for every
row (the authoritative template was never mutated). Injection targets: Level 0 `.claude/rules/0-core/engineering.md` and
the frame-owned Level 1 `.claude/rules/1-architecture/frame/boundaries.md`. Body fixtures were appended after the
original content; the frontmatter fixture inserts a `description:` string before `paths:`, leaving the required keys,
the header and the paths unchanged.

- **FAIL rule:** exit 1; a `Level <level> names concrete technology '<token>'` diagnostic on the injected file at the
  injected level whose token (normalized) contains the target; every other violation must be on the same file and name
  the same token (co-diagnostic); 0 warnings. A setup, unknown-skill, reference or Markdown error alone never counts.
- **PASS rule:** exit 0, `PASS (… artifacts, 0 violation(s), 0 warning(s))`; the clean row additionally requires 68 artifacts.
- **Smoke rule (S1, S2):** exit 1 and every violation is of the expected kind.
- **Oracle freeze:** first frozen at sha256 `b290846c…`. The first pre-edit run showed that S2 (`binds: none` on the
  ef-core manifest) legitimately produces two binds diagnostics on that manifest (the contract requirement and the
  frame-vocabulary evidence), while the oracle accepted only the first. Before any checker edit, S2's rule was corrected
  to "every violation is a `binds: none, but` diagnostic on `ef-core/MODULE.md`, including the contract one" (expected
  verdict unchanged: FAIL) and re-frozen at `efc12e1f725461b7d93fea38993d0f3c03065d6adfa46b82b34d87b475af5fdd`, verified
  before every later run. No expected verdict was changed at any time.

| Group | Rows | Pre-edit (untouched checker) | Post-edit | Final confirmation |
|---|---:|---:|---:|---:|
| **A** — required negatives, 10 cases × {Jest, Scrutor} × {L0, L1}: direct prescription, pure pointer, heading, bullet, nested list, table cell, frontmatter `description`, uppercase, lowercase, wrapped paragraph + code span | 40 | 0 | 40 | **40** |
| **F** — format controls × {L0, L1}: `**Jest**`, `` `Scrutor` ``, `### Technique: Jest` | 6 | 0 | 6 | **6** |
| **R** — non-regression negatives × {L0, L1}: `Must use` Docker / Swagger / NUnit / EF Core / ASP.NET Core / NuGet | 12 | 12 | 12 | **12** |
| **P** — positives: × {L0, L1} `Use the selected Level-2 test technique.`, `Follow the appropriate dependency-injection guidance.`, `Must run unit tests.`, `Use .NET, C#, TypeScript, Git, and HTTP.`, `Do not scrutinize jestful names.`; Level 2 `Technique: Scrutor …` (`dependency-injection` skill) and `Technique: Jest …` (`2-technology/frontend/framework.md`); Level 3 Scrutor decision (`decisions.md`) and Jest mention (`frontend-stack.md`); unmodified template | 15 | 15 | 15 | **15** |
| **S** — fifth capability slot directory rejected; `binds: none` on ef-core rejected (contract `requires-binds`); `check-architecture.mjs` reports NOT APPLICABLE | 3 | 3 | 3 | **3** |
| **Total** | **76** | **30** | **76** | **76** |

Diagnostics in the final confirmation (all FAIL rows exit 1; token as reported by the checker, identical on L0 and L1):

| Case | Jest | Scrutor | Co-diagnostic (same token) |
|---|---|---|---|
| A1 `Must use X.` | `'Jest'` | `'Scrutor'` | — |
| A2 `` Technique: `x`. `` | `'jest'` | `'scrutor'` | `references unknown skill or agent 'jest'` / `'scrutor'` (pre-existing reference check; not broadened) |
| A3 `## Selected technology: X` | `'Jest'` | `'Scrutor'` | — |
| A4 `- Use X.` | `'Jest'` | `'Scrutor'` | — |
| A5 nested `  - X` under `- Selected … technique:` | `'Jest'` | `'Scrutor'` | — |
| A6 `\| Tool \| X \|` | `'Jest'` | `'Scrutor'` | — |
| A7 frontmatter `description:` | `'Jest'` | `'Scrutor'` | — |
| A8 `JEST` / `SCRUTOR` | `'JEST'` | `'SCRUTOR'` | — |
| A8 `jest` / `scrutor` | `'jest'` | `'scrutor'` | — |
| A9 `Select` + newline + `` `X`. `` | `'Jest'` | `'Scrutor'` | — |
| F1 / F2 / F3 | `'Jest'` (F1, F3) | `'Scrutor'` (F2) | — |

Group R reported `'Docker'`, `'Swagger'`, `'NUnit'` (+ module-leak co-diagnostic), `'EF Core'` (+ module-leak
co-diagnostic), `'ASP.NET'` (+ a second neutrality diagnostic `'ASP.NET Core'`) and `'NuGet'` on both levels.
Representative lines:
- `.claude/rules/0-core/engineering.md: Level 0-core names concrete technology 'Jest' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet` (A1, L0)
- `.claude/rules/1-architecture/frame/boundaries.md: Level 1-architecture names concrete technology 'scrutor' (technology vocabulary); …` (A2, L1)

## Preservation gates (final confirmation)

- `node --check` OK for all six template modules (`check-instructions.mjs`, `check-architecture.mjs`, `lib/project.mjs`,
  `post-change-checks.mjs`, `pre-shell-command.mjs`, `stop-cochange.mjs`).
- Clean template: `Instruction check: PASS (68 artifacts, 0 violation(s), 0 warning(s))`, exit 0.
  `Architecture check: NOT APPLICABLE (no backend directory)`, exit 0 — not a functional .NET build or integration pass.
- Capabilities: exactly four slot directories; selection `architecture | required frame | clean-architecture`,
  `persistence | required | ef-core`, `backend-testing | required | nunit`, `frontend | optional | angular`; `binds:`
  lines unchanged (`none` for the frame, nunit and angular; ef-core → `architecture/clean-architecture — <reason>`);
  S1 and S2 confirm rejection of a fifth slot and of a missing required binding.
- English only; the checker diff adds no non-ASCII character (proved by the two-token reversal above).

## Policy preservation (196 = 194 inventory + GOV-017/GOV-018)

Inference, not a new audit: every policy owner is byte-identical (all rules, skills, capability files, contracts, the
agent, hooks, settings, `CLAUDE.md`, `INSTRUCTION_MAP.md`), so no owner, strength, trigger, minimum scope or routing
changed. The checker change only extends P4 detection vocabulary; the clean template is unaffected (68/0/0). A fresh
full 196-record semantic audit was **not** performed; earlier accepted evidence applies to the unchanged files.

## D1–D17

D1/D2 (P4 neutrality) are the subject: two more names are recognized, nothing else. D3–D14 hook mechanics live in
byte-identical files; their behavior suites are inherited, not re-run. D15 rechecked by S1/S2 and the clean run. D16: no
Level-2 technique changed. D17: always-loaded surface and skill/agent descriptions unchanged.

## Comparison with Candidate L0

Jest and Scrutor now fail at Levels 0/1 in every tested form, matching the L0 behavior reported by the audit. L0's code
was not read or copied, and no other L0 vocabulary was merged; whether any other lexicon differences remain is outside
this pass and was not verified.

## Known limitations

- Recognition stays vocabulary-based (lexicon, derived tokens, API shapes): a product name in none of these is not
  detected; content review remains necessary (threat model of `iteration_after_audit_2` unchanged).
- Fail-closed cost: the English word "jest" (e.g. "in jest") now fails at Levels 0/1, like `controller`; no such use
  exists in the template.
- The unknown-skill co-diagnostic on `` Technique: `jest` `` is a pre-existing reference check and was left as is.
- Not run: hook behavior suites, a live Claude Desktop/Windows integration session, a functional .NET build, the earlier
  147-case suite (not rebuilt), open-ended fuzzing, or a full 196-policy audit.

## Evidence labels

- **New in this pass:** start/final hashes and inventory, both pre-edit runs and the post-edit and final runs of the
  76-row harness, the two-token reversal proof, syntax checks, the clean checker and architecture runs, the capability
  smoke rows, the per-file byte comparison and the manifest check.
- **Inherited, not re-run:** hook behavior suites, functional architecture checks on real projects, the 196-policy audit,
  the V2 technique review, and all evidence of earlier sections.

`output/.work/` (harness, snapshots, results) was deleted after this section was written; `output/` contains only
`template/` and `REFINEMENT_REPORT.md`.
