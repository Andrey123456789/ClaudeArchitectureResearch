# L0 Controlled Refinement Report

## Final status

**STRICTLY_BETTER**

All twelve mandatory defects (D1–D12) are fixed and backed by behavioral evidence against the final files. The documented regression matrix passes in full: 143 of 143 checks. A one-time demonstration also reproduced 9 of the baseline defects on `baseline/template/`. L0 identity, all 196 policy owners, trigger roles, scopes, Level 0/1 neutrality and the dependency direction are unchanged. The complete confirmation audit was run twice:

- **Pass 1** found 3 concrete template defects, all repaired (see "Confirmation audit").
- **Pass 2** found 0 defects.

| Item | Value |
|---|---|
| Baseline tree SHA-256 (L0 Run-02, `baseline/template/`) | `f65d218ced590536f94a2f2c28deb5cef2e959c998fc8c743cbbf6f0c2b4c74a` |
| Final tree SHA-256 (`output/template/`) | `f10953e36655ca6324ca7a546f1ba1b55bdbd8308b5d98e3bc88582e6b783654` |
| Tree-hash method | SHA-256 of the `sha256sum`-style listing (`<file sha256>␠␠<relative path>\n`, paths sorted by byte order) |
| Initial copy identity | byte-identical to the baseline; all 71 per-file hashes match `MANIFEST.sha256` |
| Trigger-role deltas / minimum-scope misses | 0 / 0 |
| Unresolved references | 0 |
| Regression matrix | 143 / 143 PASS |
| Confirmation audit | pass 1: 3 defects repaired · pass 2: **0 concrete template defects** |

`PROVENANCE.json` gives the baseline tree as `bf7f0012…`, but it does not document how that hash was computed, and the obvious listing variants did not reproduce it. Baseline identity was therefore established per file, against `MANIFEST.sha256` (71 of 71 match). Both tree hashes above use the same stated method.

## Files changed (6 of 71)

| File | Bytes before → after | Change |
|---|---:|---|
| `.claude/settings.json` | 814 → 1,250 | Exec form for every hook: `"command": "node"`, `"args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/claude-hook.mjs", "<event>"]`. PreToolUse `Bash\|PowerShell` gets `"onFailure": "block"`. New `PostToolUseFailure` `Bash\|PowerShell` → `post-bash`. Post-event and Stop hooks are not made blocking. |
| `.claude/hooks/claude-hook.mjs` | 13,401 → 31,857 | **Roots:** separate launcher and active roots. The active root comes from the hook input `cwd` or the edited file, through Git. **Pre-execution routing:** quote-aware command parser, fail-closed `pre-bash`, blocks project-reference mutations. **Post-shell:** actual-state validation through a per-worktree snapshot, after both successful and failed shell calls. **Stop:** fingerprint now includes the content of the relevant files. |
| `.claude/hooks/manifest-checks.mjs` | 10,957 → 14,273 | Decodes UTF-8, UTF-8 with BOM, and BOM-tagged UTF-16LE/BE; malformed UTF-16 is reported as a finding. Extracts project references and computes dependency/reference deltas. The fallback walk skips nested repositories and worktrees. |
| `.claude/tools/check-instructions.mjs` | 18,297 → 21,965 | Validates the new hook contract instead of the old shell-form string: exec form, launcher placeholder, event argument present in the script's handler map, imported modules, timeout, `onFailure: "block"` on PreToolUse only, and all five required registrations (including PostToolUseFailure). Skips nested worktrees under `.claude/`. Accepts an optional root argument. |
| `.claude/INSTRUCTION_MAP.md` | 18,418 → 20,265 | The Enforcement section and three Level 3 rows now describe the tested behavior. The checker command is root-stable. Documents the launcher/active root model and the non-Git fallback. |
| `.claude/skills/project-structure/SKILL.md` | 6,731 → 7,036 | Step 4 adds the mapped references as `<ProjectReference>` items, because the hook now blocks the `dotnet … reference` CLI. The rest is pointer-only text. |

No file was added or removed. No rule, decision summary, `CLAUDE.md`, knowledge skill or other policy-owning file changed.

## D1–D12 disposition

Evidence IDs refer to the regression matrix, summarized in the next section.

| ID | Defect | Disposition | Behavioral evidence |
|---|---|---|---|
| D1 | Launcher breaks after a nested `cd` | **Fixed.** Exec form with an absolute launcher path through `${CLAUDE_PROJECT_DIR}`; no shell and no cwd-relative path. | Passing: L-root, L-nested, L-nested-guard, L-worktree, L-worktree-nested, L-spaces, E-shape, E-noshell. Baseline B-D1: from a nested cwd the old launcher failed with `MODULE_NOT_FOUND` and failed open. |
| D2 | Launcher root and active worktree root not separated | **Fixed.** Launcher root = script location, used only for tooling. Active root = Git top level of the input `cwd` (or of the edited file's directory). State lives in the worktree-specific Git directory. | L-product-input, L-scan-active, L-scan-active-change, L-no-main-state, L-wt-state, L-main-untouched, L-stop-active, L-stop-worktree, L-stop-state, L-nested-wt-skip, L-nested-wt-edit |
| D3 | Critical PreToolUse can fail open | **Fixed.** `onFailure: "block"` on PreToolUse. `pre-bash` also exits 2 itself when it cannot decide: empty, malformed or non-object input, missing `tool_input.command`, or an internal error. Post and Stop failures exit 1, which is visible and never blocking. | E-missing, E-crash, E-timeout, E-empty-pre, E-malformed-pre, E-nocommand-pre, E-empty-post, E-malformed-stop, E-onfailure. Baseline B-D3: no `onFailure`. |
| D4 | Project-reference mutation not routed | **Fixed.** `dotnet add/remove [proj] reference`, `dotnet reference add/remove`, `dotnet.exe`, and forms nested in `cmd /c` / `-Command` / `-c` or chained segments are blocked before execution, with routing to `project-structure` / `architecture-decision`. Reference changes made any other way are reported after the fact (post-shell and post-edit). | 8 reference cases in C+, S-ps-failure, S-edit-reference. Baseline B-D4: the reference command went through. |
| D5 | npm-family global options hide mutations and force flags | **Fixed.** Per-manager tables of value-taking options (`--prefix`/`-C`/`-w` for npm, `--dir`/`-C`/`--filter`/`-F` for pnpm, `--cwd` for yarn), `yarn workspace`, `.cmd`/`.exe`/`.ps1`, quoted Windows paths, `npm_config_*` environment overrides, and flags before or after the subcommand. Restore-only commands stay distinct. | 20 force/legacy-peer cases in C+, 24 allowed cases in C-, 9 P+ routed, 7 P- quiet. Baseline B-D5: `pnpm --dir … add x --force` went through. |
| D6 | Checker rejects the safer configuration | **Fixed.** The checker validates the exec-form contract and event registrations described under "Files changed". | N-positive, N-onfailure, N-failure-event, N-shell-form (the old shell form is now rejected). Baseline B-D6: the old checker rejected exec form. |
| D7 | Manual checker command is cwd-relative; the map overclaims | **Fixed.** Root-stable command `node "$(git rev-parse --show-toplevel)/.claude/tools/check-instructions.mjs"`, valid in Bash and PowerShell. The map's shell-neutrality claim was replaced with the tested exec-form description. | L-checker-cmd-bash (nested cwd), L-checker-cmd-ps (nested worktree cwd), L-checker-nested |
| D8 | Stop fingerprint ignores content | **Fixed.** The fingerprint adds a bounded digest (up to 500 files) of the current content of the files that drive the reminders. The status-set semantics and `stop_hook_active` are kept. | T-initial, T-active, T-unchanged, T-material, T-repeat, T-irrelevant. Baseline B-D8: silent after a material edit. |
| D9 | Successful shell mutations validated from command text only | **Fixed.** `post-bash` compares a per-worktree manifest snapshot: tracked and untracked files that are not ignored, plus HEAD. It validates only what was added or changed and routes package and reference deltas. Command text only adds context. | S-bash-success, S-ps-success (UTF-16 `Out-File`), S-same-path, S-restore-detected, S-unrelated-quiet. Baseline B-D9: an actual mutation was ignored. |
| D10 | No post-failure path | **Fixed.** `PostToolUseFailure` `Bash\|PowerShell` is registered and handled by the same actual-state check ("after the failed shell call"). It is quiet when nothing relevant changed, and never blocks. | S-bash-failure, S-ps-failure, S-failure-quiet, S-failure-quiet-ps, P-failed-nochange. Baseline B-D10: no registration. |
| D11 | No persistent state for HEAD transitions, deletions, moves | **Fixed.** A fresh state validates every manifest once, using HEAD as the previous observation. Later observations diff the stored snapshot and HEAD. Deletions and moves are reported, with moves paired by normalized content. Ignored, build-output and nested repository/worktree paths are never observed, so they never appear "removed". A malformed snapshot counts as fresh. | S-fresh-clean, S-fresh-head, S-later-head, S-delete, S-move, S-skip-added, S-skip-removed, S-corrupt-state, S-edit-then-shell |
| D12 | Windows encodings | **Fixed.** The UTF-8 BOM in hook stdin is still handled, and stdin now uses the same decoder. Manifest and decision-summary readers handle UTF-8, UTF-8 with BOM and UTF-16LE/BE with BOM. Odd-length UTF-16 becomes a deterministic finding, not a crash. | E-bom, E-utf8bom-manifest, E-utf16le, E-utf16be, E-odd-utf16, E-edit-utf8, E-edit-utf16, S-ps-success. Baseline B-D12: a BOM `package.json` was falsely reported as invalid JSON. |

## Behavioral regression matrix

**How it ran.** The harness ran once under `output/.work/` (now removed) against the final files:

- sandbox repositories under a path containing spaces;
- Git discovery capped with `GIT_CEILING_DIRECTORIES`;
- `core.autocrlf=true`, Git 2.55 for Windows, Node 24, Windows PowerShell 5.1.

Hooks were executed exactly as the generated settings declare. Exec form was emulated per the documented host semantics: `command` + `args`, the placeholder substituted as a plain string, no shell. Block and fail-closed outcomes followed exit code 2 and `onFailure`.

| Area | Checks | Result | Coverage |
|---|---:|---|---|
| 6.1 Launch / root / worktree | 24 | PASS | Root, nested cwd, linked sibling worktree, nested cwd in the worktree, worktree nested under `.claude/worktrees/`, paths with spaces, product-input routing, manifest scan and Stop on active content, main checkout untouched, root-stable checker command in Bash and PowerShell. Also four non-Git checks (G-*): the fallback full scan after a dependency command, a quiet unrelated command, a visible Stop "unavailable", and a product-input reminder. |
| 6.2 Hook input / Windows encoding | 18 | PASS | Exact settings shape, `onFailure` only on PreToolUse, no shell syntax, BOM stdin, empty/malformed/non-object input, missing/crashing/timed-out guard blocking, UTF-8, UTF-8 BOM, UTF-16LE/BE and odd-length manifests (post-shell and post-edit) |
| 6.3 Dependency command matrix | 69 | PASS | 28 commands blocked before execution and 24 allowed. After the call, 9 dependency commands routed and 7 restore-only commands quiet; one failed no-change call quiet. Covers npm, pnpm, yarn, `ng add`, dotnet package and reference forms, global options and their values, force/legacy-peer flags in any position, restore-only commands, and nested shells. |
| 6.4 Shell actual state | 19 | PASS | Successful and failed Bash and PowerShell mutations, unknown-command mutation, fresh and later HEAD transitions, same-path rewrite, deletion, move, unchanged state quiet, skipped areas, edit-then-shell deduplication, reference edit, malformed snapshot |
| 6.5 Stop | 6 | PASS | Initial reminder, `stop_hook_active`, unchanged state silent, material change re-reminds, repeat silent, status-set change re-reminds |
| 6.6 Checker fixtures | 7 | PASS | Unmodified template passes. These fixtures fail it: missing `onFailure`, missing `PostToolUseFailure`, Level 1 technology (`EF Core`), reverse Level 1 → Level 3 dependency, broken reference, old shell form. |
| One-time baseline demonstration | 9 | defects reproduced | B-D1, B-D3, B-D4, B-D5, B-D6, B-D8, B-D9, B-D10, B-D12 |

### Shell events: success and failure

Both events run the same actual-state comparison:

- `PostToolUse` for `Bash|PowerShell`;
- `PostToolUseFailure` for `Bash|PowerShell`.

Tested results:

- **Mutation detected:** Bash success, PowerShell success, Bash failure (partial write, then `exit 3`), and PowerShell failure (`Set-Content`, then `throw`).
- **No relevant change:** failed calls in either shell stay quiet.
- **Never blocking:** neither post event blocks. If a check cannot run, the exit code is 1, which is visible.

### Worktree, nested cwd, Windows, BOM and UTF-16

All covered and passing, as listed in rows 6.1 and 6.2 and under D2 and D12. Two Windows-specific points:

- A real Windows PowerShell 5.1 `Out-File` produced UTF-16LE with BOM. The hook decoded it and reported the violation (S-ps-success).
- `& "C:\Program Files\nodejs\npm.cmd" --prefix … --force` is blocked.

### Stop state

All six Stop checks pass:

- **D8 fixed:** a material edit to an already-modified file re-reminds.
- **Loops still prevented:** an unchanged repeat is silent, and `stop_hook_active` keeps stopping the hook.

## Structural and policy audit

**Owner, trigger and scope mapping.** An explicit mapping was built for all 194 inventory policies plus GOV-017 and GOV-018:

- every policy has exactly one owner, and every anchor was found in it;
- trigger roles: always 32, workflow 41, path 123;
- trigger-role deltas: **0**; minimum-scope misses: **0** (path globs checked against representative paths per scope);
- duplicate-anchor restatements: **0**.

**Strength and conditions.** All 196 owner files are byte-identical to the baseline, so normative strength and conditions are unchanged. The only changed instruction artifacts own no policy:

- `project-structure` step 4 now uses pointer wording only;
- `INSTRUCTION_MAP.md` is the human map, not an instruction layer.

**L0 identity.** Unchanged:

- four level directories with matching headers;
- no `Kind:` field, contracts, slots, manifests, or Feature/Task levels;
- the two decision summaries are still imported separately from `CLAUDE.md`;
- `SPECIFICATION.md` is empty (0 bytes).

**Dependency direction.** The checker reports no reverse conformance dependency and no cycle. The negative fixture N-reverse is caught.

**Level 0/1 neutrality.**

- Checker: PASS on the template; the N-level-tech fixture (EF Core in Level 1) fails as required.
- Independent scan: 16 Level 0/1 artifacts against a 66-term deny list. The only hits were `LINQ` and `IQueryable<T>`, which are .NET/C# fixed-platform vocabulary and unchanged from the baseline. No concrete technology was found.

**References.** These all resolve:

- every file, import, skill, private reference, and section pointer the checker examines;
- all 19 `.claude/…` paths referenced by the hook and checker scripts;
- every section pointer used in hook messages: Install, Select the version, Conditional package bindings, Project references, Implement, Co-changes, Not added by default, npm, verify step 4.

**Hygiene.**

- No research labels, run identifiers, workspace paths, model IDs or Cyrillic text.
- No BOM or control characters.
- No dependency on files outside `output/template/`.

**Documentation matches behavior.** The map's Enforcement section, the `project-structure` step, the hook and checker header comments, and the hook messages were checked against the tested behavior.

## Always-loaded surface, file count and bytes

| Metric | Before | After |
|---|---:|---:|
| Always-loaded estimate (checker, chars/4: `CLAUDE.md` + 2 imports + skill/agent listings) | ≈ 5,002 tokens | ≈ 5,002 tokens |
| Runtime files | 71 | 71 |
| Runtime bytes | 305,547 | 333,575 (+28,028) |
| Markdown bytes | 257,463 | 259,615 (+2,152) |

**Where the bytes went.** All of the increase is in the deterministic enforcement layer: hooks +21,772 bytes, checker +3,668 bytes, settings +436 bytes. The rest is the human map and one workflow step.

**Justification.**

- The increase buys the D1–D12 reliability fixes.
- No new file, layer or helper was added.
- Nothing in the always-loaded surface changed.

**Efficiency review (8.1).** Done once. The remaining candidates were judged cosmetic or a risk to trigger reliability and decision content, so none was applied:

- the intro/maintainer pointer lines in `CLAUDE.md`;
- the owner-routing table in `overview.md`;
- further cuts to skill descriptions.

## V2-fidelity review (8.2)

**How it was checked.** A systematic automated pass used the frozen `source/v2-baseline/` tree, not Run-01. It covered 645 headings, 2,758 prose and bullet statements, and 300 code blocks, each matched against the template by content-word containment. The low-match residue (758 statements, 66 code blocks) was reviewed manually. It consisted of:

- sentence fragments from the splitter;
- cross-references to V2 skills that L0 renamed or merged (`testing` → `dotnet-testing`, `error-handling` → `aspnet-error-handling`, `serilog`/`resilience` → private references, `technology-stack.md` → `decisions.md`);
- `ProjectName` → `<Name>` example renames;
- content present in compressed form.

**Spot-checks.** More than 20 items were checked individually and found preserved, for example:

- the narrowest-project dependency scope;
- the dead-reference removal rule;
- HTTPS redirection versus hosting topology;
- `AsNoTracking` on projections;
- deterministic paging order;
- the documented direct-Polly exception;
- 406/415/422/428 semantics;
- the "do not forbid mocking project-owned abstractions" guidance.

**Result.** No material technique or example needed for correct use was missing, so nothing was restored. Every policy-owning and knowledge file is byte-identical to the audited baseline. The one V2-derived step that changed (`project-structure` step 4) keeps V2's "only the references the layout describes; never outward" semantics. V2 preservation is not worse.

## Confirmation audit

**Pass 1** covered the full matrix, checker, policy audit, hygiene, reference checks and a code read-through. It found and repaired three concrete template defects:

1. A malformed snapshot whose `manifests` was `null` passed the freshness test and caused a visible hook error instead of a fresh validation. Fixed with `usableState()`; regression test S-corrupt-state added.
2. The Stop message claimed it repeated "only when the relevant changes differ", but the status set also counts, as in the baseline. The wording was aligned with the behavior and the map.
3. The checker's handler check passed whenever the event name appeared anywhere in the hook script. It now checks the event against the keys of the `handlers` map.

An earlier matrix run had also found one implementation defect: `git ls-tree` rejected `:(glob)` pathspec magic in the fresh-state baseline. It was replaced with `git diff --name-status --no-renames` plus the untracked list before the confirmation audit.

**Pass 2** (complete rerun after the repairs) had these results:

- matrix 143/143;
- checker PASS;
- policy audit 0 problems;
- hygiene clean;
- docs consistent with behavior.

It found **0 concrete template defects**.

## Attempted or considered changes not adopted

These were considered and judged not demonstrably better; none was kept in the template:

- **Pre-blocking ordinary package installs** (deny first, allow on an identical retry). The friction trade-off was not clearly a net gain. Ordinary installs stay allowed before execution and are routed afterwards; force/legacy-peer flags are blocked as before.
- **`permissionDecision: "ask"` for reference mutations.** The external mechanics notes establish only deny semantics. A deterministic deny with routing was used instead.
- **Tracking `SPECIFICATION.md` and `CUSTOM_SETTINGS.md` in the shell snapshot.** Out of the dossier's scope. Edit-time and Stop reminders already exist.
- **Always-loaded trimming candidates.** Cosmetic; see the efficiency review.

## Remaining known limitations

- **No live hook-engine test.** Activation was proven by process-level execution of the generated settings and scripts plus the documented host semantics. Moving the running session into the template was out of scope by design.
- **Outside a Git work tree there is no snapshot.** `post-bash` falls back to a full scan after recognized dependency commands, and Stop reports visibly that it is unavailable. This is documented in the map.
- **Command classification is bounded.** Exotic wrappers can evade pre-classification: `sudo` with option values, versioned `npx` package specs, or text after a shell `#` comment. Actual-state validation after the call still catches the resulting manifest changes.
- **The reference CLI is blocked, but direct edits are not.** Approved reference changes are applied by editing the project file. Post-edit and post-shell report every reference-graph change; editing is reported, not pre-blocked.
- **Move pairing uses normalized content.** A move combined with an edit is reported as a removal plus an addition, which is still visible.
- **The Stop content digest is bounded** to 500 relevant files.

## Workspace events (directly observed)

- **Experimental isolation violations: 0.** No sibling, parent or network content was read. `audit/evidence/Run-01-GENERATION_REPORT.md` was not opened.
- **Recoverable incidents (remediated):**
  - Early in the run, three input-derived bundles were written to the session scratchpad outside the workspace; they were deleted at once and all later material went to `output/.work/`.
  - One command redirected a checksum listing to `/tmp/none`; it was deleted at once.
- **Platform-managed events:**
  - The tool runtime stored two oversized outputs in its tool-results folder; both were baseline/source content.
  - The desktop runtime loaded `output/template` instruction files as context and listed its skills. None was invoked, and nothing depends on it.
- **Cleanup:** `output/.work/` was removed after the final confirmation and this report. `output/` contains only `template/` and this report.

---

# iteration_after_audit_1 — corrective pass (quote-sensitive MSBuild XML parsing)

Everything above this line is the earlier L0 refinement record. It is kept unchanged as historical evidence. This section records one bounded corrective pass, run from the current `output/template/` (71 files) as specified by `L0-iteration_after_audit_1-CORRECTIVE_TASK.md`.

## Final status

**STRICTLY_BETTER**

The quote-sensitive parsing defect is fixed at its root in `.claude/hooks/manifest-checks.mjs`. That one file is the only template change; the other 70 files are byte-identical to the starting inventory.

| Check | Result |
|---|---|
| Final discriminating matrix | **100 / 100 PASS**, run against the real final module and the unchanged hook |
| Reproduction on the unmodified module | 62 of the same 100 cases failed (61 defect, 1 harness error, explained below) |
| Confirmation audit | ran once; **0 concrete template defects**, so the allowed correction was not used |

## File identity and hashes

| Item | Value |
|---|---|
| Starting tree SHA-256 (71 files) | `f10953e36655ca6324ca7a546f1ba1b55bdbd8308b5d98e3bc88582e6b783654`. Same method as above; identical to the earlier final tree, so the starting state was intact. |
| Final tree SHA-256 (71 files) | `a1ced4289e9a17f4980d22841cf5a4446fdebd51afc9f6fffcb1db2fe3aa64e8` |
| Changed file | `.claude/hooks/manifest-checks.mjs` only |
| `manifest-checks.mjs` before | `604c52e6b6c09638c1cbe2a19f47f0a97fedb5b061081e73fe91467d654a1147` · 14,273 bytes |
| `manifest-checks.mjs` after | `b7a5ee762cd856ac04e3c7fecdf69a7a15e243a3f40e6008c63db491ff960ade` · 20,127 bytes · 455 lines |
| Other 70 files | byte-identical to the starting per-file inventory; no file added or removed |
| Runtime bytes | 333,575 → 339,429 (+5,854, all in the changed module) |
| Always-loaded estimate (checker) | ≈ 5,002 tokens, unchanged |
| Inputs and root metadata | `baseline/`, `source/`, `audit/` (125 files) and the 8 root metadata files are unchanged; hashes taken before and after match |

## Reproduced failure and root cause

**Where the defect was.** The unmodified module read MSBuild XML with separate regular expressions, each tied to one spelling:

- `attributes()` accepted only `name="value"`;
- `projectReferences()` matched only `Include="…"`;
- the `PackageReference` and `PackageVersion` element patterns used `[^>]*?`, so a quoted `>` ended the tag early;
- no path treated XML comments as inert.

**What it affected.** These patterns fed both responsibilities named in the task:

- **Enforcement:** `checkManifestFile()` and `scanManifests()`.
- **Actual-state tracking:** `declaredDependencies()` and `dependencyDelta()`, which `claude-hook.mjs` uses after successful and failed shell calls and after edits.

**Reproduction.** The harness ran once against an isolated, byte-identical copy of the unmodified template. Representative failures:

| Case | Unmodified module | Required |
|---|---|---|
| `Demo.Domain.csproj` with `<ProjectReference Include='../Demo.Api/Demo.Api.csproj' />` | no finding, no reference | outward reference Domain → Api |
| `<PackageReference Include='Microsoft.Extensions.Http.Polly' Version='9.0.0' />` | no finding | inline version and deny-list findings |
| `<PackageVersion Include='Safe.Lib' Version='1.2.3' />` with central management on | false `[(unknown)]: empty version` | valid |
| Delta for a single-quoted reference added next to a double-quoted one (D→S) | `removed ../Demo.Domain/…`; the new edge is missing | `added ../Demo.Infrastructure/…` only |
| `PostToolUse`: successful Bash writes the single-quoted Domain → Api reference | exit 0, silent | exit 2 with violation and graph change |
| `PostToolUseFailure`: Bash with a real partial write, then `exit 3` | exit 0, silent | exit 2 with violation |
| Real PowerShell 5.1: `Out-File` (UTF-16LE) success, and `Set-Content` + `throw` failure | exit 0, silent | exit 2 |
| Fresh state on a valid repository with single-quoted entries | false "empty version" finding | quiet |
| Quote-only rewrite of a `.csproj` or `Directory.Packages.props` (shell call or edit) | reported as added/removed packages and references | quiet |
| Commented-out `<ProjectReference …Demo.Api…>` in Domain (double quotes) | outward-reference finding plus a dependency entry | inert |
| `Label="a > b"` before a paired `PackageReference` | inline-version finding attributed to the wrong package; the real one unseen | finding on the correct package only |

Reproduction totals: 38 PASS, 62 FAIL of 100.

| Group | Failed |
|---|---:|
| 4.1 project references | 12 |
| 4.2 packages and central management | 25 |
| 4.3 declared dependencies and deltas | 10 |
| 4.4 hook propagation | 15 |

One of the 62 failures, W2, was a **harness error**: the fixture hard-coded the worktree's administrative directory as `A wt`, but Git stores it as `A-wt`. The fixture was corrected to ask Git for the path (`git rev-parse --git-path`), and the oracle was not changed. The other 61 failures are attributable to the defect.

## Fix

**One shared reader.** The module now has one bounded, quote-aware reader for MSBuild XML: a small local lexer with no XML library and no MSBuild evaluation. `xmlTokens()` reads the markup; `msbuildItems()`, `metadata()` and `itemId()` read items from it. All three affected paths use it:

- `checkProjectFile()`: `PackageReference` and `ProjectReference`;
- `checkCentralPackages()`: `PackageVersion` and the `ManagePackageVersionsCentrally` switch;
- `declaredDependencies()`, including `projectReferences()`.

No double-quote-only parser and no `matchAll` element pattern is left.

**What the reader accepts:**

- `"…"` and `'…'` values, also mixed within one element;
- whitespace and line breaks around `=` and between attributes;
- attributes in any order;
- `>` inside a quoted value;
- the predefined entities and numeric character references (`&apos;`, `&#121;`, …);
- self-closing and paired elements.

**What it treats as inert:** comments, processing instructions and declarations. CDATA is read as text.

**Malformed tags.** A recognized element whose start tag cannot be read gets a new deterministic finding with its line number (`… is not well-formed XML …`). This covers an unquoted value, missing whitespace between attributes, an unterminated quote, and a duplicate attribute. Such a tag opens no element, so it cannot swallow the declarations that follow it.

**Item metadata** is read uniformly from an attribute or a direct child element. The old module did this only for `<Version>` inside `PackageReference`, and only in the check. Consequences:

- a nested `<VersionOverride>` now gets the existing override diagnostic;
- a `PackageVersion` with a nested `<Version>` is read instead of being reported as empty;
- `declaredDependencies()` records nested versions, using the same semantics as the checks.

**`Include`/`Update` values** are trimmed, so line-wrapped values are read the same as unwrapped ones.

**Preserved unchanged:**

- the text of every existing diagnostic;
- the deny and review lists and the accepted-decision semantics;
- `Include ?? Update` for packages and `Include` only for project references;
- case-sensitive attribute and element names (the central-management switch stays case-insensitive, as before);
- package-ID case handling and case-insensitive reference comparison in `dependencyDelta()`;
- backslash normalization;
- file discovery, skipped directories, nested-repository handling, and UTF-8/BOM/UTF-16 decoding;
- the module's 12 exports, which are identical.

Neither `claude-hook.mjs` nor any other file changed. The PostToolUse pipeline and its D9–D12 logic are untouched.

**One wording correction before the audit.** The first implementation (`55c46f4a…`) passed 100/100. The not-well-formed message was then reworded, because its old text named the wrong cause for a duplicate attribute. The matrix was rerun on the final hash `b7a5ee76…` with 100/100. Both runs happened before the confirmation audit.

## Discriminating test matrix (final files)

**How it ran.** One harness in `output/.work/` (now removed), run against the real final module. Platform: Node 24.21.0, Git 2.55.0.windows.5, Git Bash 5.3 and Windows PowerShell 5.1 on Windows 11.

**Direct cases:**

- each case is isolated in its own fixture root, with no approved exceptions unless the case adds one;
- each records the exact findings list;
- a case passes only if every expected diagnostic appears **and** no other diagnostic appears, so a negative case cannot pass for an incidental reason;
- for pass cases, `declaredDependencies()` was compared exactly where relevant.

**Hook cases:**

- isolated Git repositories under a path containing spaces, with `GIT_CEILING_DIRECTORIES` set;
- each repository is a full copy of the final template, with the copied hook, module and settings verified byte-identical;
- the hook was launched in exec form from the copied `settings.json` (`node` plus args, `${CLAUDE_PROJECT_DIR}` substituted, no shell);
- the actual Bash or PowerShell command ran first, and its real side effect (content and BOM) was asserted before the post event.

| Group | Cases | Result | Coverage |
|---|---:|---|---|
| 4.1 Project references | 24 | 24 PASS | Each in both quote styles: Domain → Api FAIL; Domain → Infrastructure FAIL; production → test FAIL; Application → Domain, Infrastructure → Application and Api → Domain PASS with zero findings; a non-dependency element with `Include` creates no reference; a commented-out reference is inert. Variants: reordered, multiline, mixed quotes, paired element, character reference, a quoted `ProjectReference` text inside another attribute, and an unterminated quote that must not swallow the next reference. |
| 4.2 Packages and central management | 44 | 44 PASS | Each in both quote styles: versionless safe package allowed; inline `Version`, `VersionOverride` and nested `<Version>` rejected; Polly and Elasticsearch-sink deny entries; MediatR review finding, cleared by an accepted decision; valid central `PackageVersion`; floating `*`; prerelease; missing version; `Update` on both item types; commented-out declarations inert; a non-package element creates no phantom package; a quoted `>` stays inside its element. Variants: mixed, reordered and multiline; commented-out central switch rejected; unquoted attributes and duplicate attribute reported; nested `VersionOverride`; nested central `Version`; character-reference spelling of a denied ID. |
| 4.3 Declared dependencies and deltas | 11 | 11 PASS | Quote-only rewrites (D→S, S→D, multiline) of a `.csproj` and of central props give equal non-empty maps and an empty delta. Added and removed references, and added/changed/removed packages (central and `.csproj`), give **identical** deltas for D, S and cross-quote pairs. A mixed multiline manifest is not read as empty. A comment-only addition is neutral. A new invalid manifest is flagged by `checkManifestFile()` and reported by the delta. |
| 4.4 Hook propagation | 21 | 21 PASS | See the next table. |
| **Total** | **100** | **100 PASS · 0 FAIL** | |

**Hook propagation cases (4.4):**

| Area | Cases | What was observed |
|---|---|---|
| Successful Bash (`PostToolUse`) | A0–A6 | Fresh state with valid single-quoted references and central entries is quiet. An unrelated call from a nested cwd is quiet. A quote-only rewrite of a `.csproj` and central props is quiet. A single-quoted Domain → Api write from a nested cwd reports the violation and graph change. The next unrelated call is quiet (no repeated findings). A real new allowed edge, Api → Domain, is reported as a graph change without a violation. Single-quoted central edits report `changed Safe.Lib, added Microsoft.Extensions.Http.Polly, removed Other.Lib` plus the deny finding. |
| Linked worktree | W1–W3 | Nested cwd inside the worktree, launcher in the main checkout. The worktree is the active root and its single-quoted Domain → Infrastructure violation is reported. The main checkout's manifest and state file are unchanged; the worktree keeps separate state. An unrelated call in the worktree is quiet. |
| Failed Bash (`PostToolUseFailure`) | B0–B4 | Real partial write of a single-quoted Domain → Api reference, then `exit 3`: reported "after the failed shell call". A failed call without changes is quiet. A failed call with an unrelated partial write is quiet. A partial write of a denied inline package plus a test reference, then `exit 5`: every relevant finding is reported. |
| Real Windows PowerShell 5.1 | P0–P3 | Fresh state is quiet. Successful `Out-File` (UTF-16LE BOM verified) is reported through `PostToolUse`. Failed `Set-Content -Encoding UTF8` (BOM verified) followed by `throw` is reported through `PostToolUseFailure`. A failed call without changes is quiet. |
| Post-edit | E1–E2 | A single-quoted Domain → Api edit is reported with the violation and graph change. A quote-only edit is quiet. |

Unrun cases: none of the planned matrix was skipped.

## Confirmation audit (one pass, final files)

| Gate | Result |
|---|---|
| Template identity | 71 files; 70 byte-identical to the starting inventory; only `manifest-checks.mjs` differs; no new files |
| `node --check` | PASS for `manifest-checks.mjs`, `claude-hook.mjs` and `check-instructions.mjs` |
| Instruction checker | `check-instructions.mjs`, supported invocation from a nested directory: `Instruction structure: PASS`, exit 0, ≈ 5,002 tokens. This is a structural check, not evidence of .NET runtime behavior. |
| Clean-template manifest scan | `scanManifests` on the template's own `Directory.Build.props` and `Directory.Packages.props`: 0 problems |
| Policies | 194 inventory policies (unique, matching the declared count) plus GOV-017 and GOV-018. Every policy-owning file is byte-identical, so owners, trigger roles, minimum scopes and strength are unchanged. The changed module is a Level 3 enforcement asset and owns no policy. |
| L0 identity | Unchanged by construction: no rule, skill, `CLAUDE.md`, decision summary, map, settings or checker file changed. The four levels, dependency direction, Level 0/1 technology neutrality, separate decision imports, and the absence of slots, contracts or `Kind:` are confirmed by the checker. |
| Hook contract | `settings.json` and `claude-hook.mjs` are byte-identical, so these are preserved: exec form; `PreToolUse` `Bash\|PowerShell` with `onFailure: "block"`; `PostToolUse` and `PostToolUseFailure` for `Bash\|PowerShell`; post-edit; Stop. The hook import of `./manifest-checks.mjs` is unchanged and the 12 exports are identical. |
| Hygiene of the changed module | English only. The non-ASCII characters are exactly the earlier set (`·` ×1, `→` ×25, `—` ×4); no Cyrillic; LF line endings; no BOM; the Level header line is retained. |
| Diff review | All three call paths use the shared reader. No quote-specific or `matchAll` element parsing remains. Every existing diagnostic's text is unchanged. |

**Audit tooling note.** One audit one-liner failed because of shell quoting in the command itself. It was rerun as a small script; this did not affect the template.

## Evidence provenance

**Freshly executed in this pass:**

- the reproduction run on the pre-edit copy;
- the final 100-case matrix;
- the confirmation audit.

**Exercised incidentally by the 4.4 cases** (shared hook code with unchanged files):

- fresh-state validation;
- nested cwd;
- linked-worktree root and state isolation;
- UTF-16LE and UTF-8-BOM manifests;
- success and failure events;
- quiet no-change behavior;
- post-edit.

**Inherited, not rerun.** These depend only on byte-identical files, so the evidence in the earlier section of this report stands:

- launcher and exec-form launch from any cwd;
- missing, crashing or timed-out fail-closed `PreToolUse` and malformed-input handling (D1, D3);
- `pre-bash` command classification (D4, D5);
- checker negative fixtures (D6, D7);
- Stop content fingerprint and `stop_hook_active` (D8);
- HEAD transitions, tracked deletion and move, skipped paths, malformed snapshot (D11);
- the non-Git fallback scan.

## Remaining bounded limitations

- **Not an MSBuild evaluator** (as before). Not expanded:
  - properties (`$(…)`), so values built from them are not resolved;
  - conditions (items under a false condition still count);
  - wildcards and imports;
  - `;`-separated lists in one `Include`.

  A list such as `Include="../X.Api/X.Api.csproj;../X.Domain/X.Domain.csproj"` is read as one path. In an Application project the Api entry can therefore go unreported by the static check; the post-call graph-change line still lists the combined value as an added reference. This limitation existed before, belongs to MSBuild item semantics rather than XML spelling, and was not in scope.
- **Element and attribute names are case-sensitive** (as before). MSBuild treats item types case-insensitively, so a lower-case `<projectreference …>` is not recognized.
- **A `<!DOCTYPE>` whose internal subset contains `>` would end early.** MSBuild files do not use one.
- **Malformed declarations.** `checkManifestFile()` reports them. `declaredDependencies()` uses the attributes it could read, so a malformed tag can make a delta incomplete. The file is still validated whenever its content changes, so the finding surfaces.
- **Versions are trimmed in `declaredDependencies()`.** A whitespace-only version change is not reported as `changed`.
- **One-time noise after upgrading.** In a worktree whose snapshot was stored by the earlier module, the first changed manifest is compared against the old parser's map and can show extra `added` lines for single-quoted entries. This is visible noise, never a missed violation. Snapshots are runtime state, not template content.
- **The new diagnostic is not documented in `INSTRUCTION_MAP.md`.** Editing the map was not authorized. Its row stays accurate, and the new finding names its own cause.
- **No live hook-engine test** (as before). Activation was proven by process-level exec-form execution of the generated settings and scripts.

## Workspace events

- **Persistent writes:** `output/template/.claude/hooks/manifest-checks.mjs` and this appended section.
- **Temporary material:** a pre-edit copy, the harness, fixtures, sandbox repositories and hash lists, all under `output/.work/`.
- **Isolation:** no sibling workspace, older iteration, earlier audit output, network or external source was read or used.
- **Platform-managed context:** the desktop runtime loaded `output/template` instruction files as context and listed its skills. None was invoked, and nothing depends on it.
- **Cleanup:** `output/.work/` is removed last, after this section. `output/` then contains only `template/` and this report.
