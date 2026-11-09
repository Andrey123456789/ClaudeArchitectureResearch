# K1 Controlled Refinement — Iteration 005 / 5.3 — Report

## Verdict: **STRICTLY_BETTER**

All mandatory defects D1–D11 are repaired with final-file evidence, the D12 source-based fidelity review and D13 efficiency/capability review were performed, every cumulative gate in §8 of the task holds, and the single complete confirmation audit on the final template bytes found **0 concrete template defects**. No baseline PASS was traded away: the immutable baseline passes none of the 13 dossier-derived reproductions that the refined template now passes, and every baseline behavior/requirement re-checked (structure checker, manifest checks, 196-policy fidelity, V2 coverage, always-loaded budget, leak/slot rules, ranked K checker) is equal or stronger.

## 1. Provenance and integrity

| Item | Value |
|---|---|
| Baseline | immutable K1 / Run-02 at `baseline/template/` (85 files, 346,715 bytes) |
| Start | `output/` was empty; `baseline/template/` copied to `output/template/`; `diff -r` → identical before any edit |
| Tree hash definition | SHA-256 of the `LC_ALL=C`-sorted list of `sha256sum ./<path>` lines of every file |
| Initial tree hash (copy == baseline) | `9e524c3fbcca218d46810ac0aab8ebe8cf1ce95f1ec6f6b516b941ec36418bec` |
| Final tree hash (`output/template`) | `0b7b52ee100b58f136727cf6892441465e23175607de667203333de41d5965e5` (identical before and after the confirmation run) |
| Baseline after the run | `9e524c3f…8bec` (unchanged); `source/`, `audit/`, task files not written |

## 2. Exact file changes (template)

- **Added (2):** `.claude/scripts/classify-command.cjs` (pre-execution classifier), `.claude/scripts/actual-state.cjs` (post-execution actual-state inspection).
- **Changed (25):** `.claude/settings.json`; `.claude/hooks/dispatch.cjs`; `.claude/scripts/{lib,check-instructions,check-manifests,check-cochange}.cjs`; `.claude/scripts/facets/{architecture-style,persistence-technology,test-framework,frontend-framework}.cjs`; `.claude/capabilities/{architecture,persistence,backend-testing,frontend}/CONTRACT.md`; `.claude/MAP.md`; skills `add-dependency`, `architecture-decision`, `persistence-change`, `project-structure` (+ `references/test-setup.md`), `template-maintenance`, `verify`; `.editorconfig`, `Directory.Build.props`, `Directory.Packages.props` (header `Conforms:` line only).
- **Deleted:** none. **Untouched:** `CLAUDE.md`, the decision register, all 21 rules, all knowledge skills/references, all module manifests, the agent, `SPECIFICATION.md` (still empty), `CUSTOM_SETTINGS.md`.

## 3. Defect disposition (D1–D11) with evidence

Evidence comes from ONE harness under `output/.work/` (child processes running the real generated scripts and `settings.json` in isolated copies; real Git repositories and real linked worktrees with `GIT_CEILING_DIRECTORIES`, no system/global Git config; fixture paths contain spaces). Host behavior was **emulated** from the documented semantics in `audit/EXTERNAL_MECHANICS_NOTES.md` (exec form with `${CLAUDE_PROJECT_DIR}` substituted as a plain argument; exit 0/2; other failures blocking only with `onFailure: "block"`). **No live Claude Code hook activation was performed or claimed.** Every negative fixture asserts the expected diagnostic text and that no unrelated error occurs; positive fixtures assert zero errors and zero warnings.

| Defect | Repair (final files) | Evidence (fixture IDs, all PASS on final bytes) | Baseline reproduction |
|---|---|---|---|
| **D1** worktree root | `dispatch.cjs` separates the launcher root (locates code) from the active root (`lib.activeRoot(input.cwd)`: Git top level; same-repository worktrees inside the checkout resolve to themselves via `--git-common-dir`; nested independent repos resolve to the enclosing project). All inspection, paths, and state use the active root. | HR-edit-wt-root, HR-edit-wt-nested, HR-shell-wt-change, HR-main-unaffected, HR-main-edit-clean, HR-state-per-worktree, HR-main-nested-frontend, HR-relative-file-path, HR-pre-wt, HR-approval-active-root, HR-whitespace, HR-inner-worktree, HR-nested-independent-repo | BR-D1-worktree: baseline exits 0 silently on the worktree-only violation |
| **D2** fail-open guard | PreToolUse hook has `"onFailure": "block"`; the dispatcher additionally exits 2 for any internal error, empty/malformed/non-object input, missing `tool_input.command`, or mismatched `hook_event_name`. Post/Stop stay advisory (exit 1, never 2 on failure). | IF-empty, IF-whitespace, IF-malformed, IF-array, IF-mismatch, IF-no-command, IF-thrown-error, IF-missing-target, IF-timeout, IF-broken-module, IF-unknown-event, IF-missing-target-advisory, IF-post-malformed, IF-stop-empty | BR-D2-onfailure |
| **D3** BOM input | Input decoded from bytes: UTF-8 with/without BOM, BOM-tagged UTF-16LE/BE, CRLF; manifests use the same decoder; NUL bytes without BOM fail visibly. | IF-json, IF-bom, IF-crlf, IF-utf16le, IF-bom-allow, IF-csproj-utf8bom, IF-csproj-utf16le, IF-csproj-utf16be, IF-csproj-nobom-utf16, IF-packagejson-bom | BR-D3-bom: baseline exit 1 `Unexpected token U+FEFF` |
| **D4** dependency classification | `classify-command.cjs`: quote/operator-aware lexer (`;` `|` `&` `&&` `||` newlines, parentheses/braces, redirections, comments, line continuations), prefix stripping (`VAR=`, `env`, `sudo`, …), wrappers (`bash -c`, `cmd /c`, `powershell -Command/-EncodedCommand`), `cd`/`Set-Location`/`Push-Location` tracking, per-manager tables (npm/pnpm/yarn verbs, global and value-consuming options), dotnet `add/remove [project] package`, `package add/remove/update`. Additions/updates need exact versions; removals, bulk updates, `npm audit fix`, `--force`/`--legacy-peer-deps` on dependency verbs are routed to `add-dependency`. | 53 blocked + 34 allowed command fixtures in `pre-route` (Bash and PowerShell tool inputs; list in §6) | BR-D4-uninstall, BR-D4-prefix, BR-D4-dotnet-remove |
| **D5** Reserved references | `dotnet add/remove [project] reference` and `dotnet reference add/remove … --project` are blocked as Reserved unless every edge `From -> To` is recorded in an accepted (dated) decision-register row or the `docs/decisions/` record it links. Post-execution, unrecorded reference-graph changes are reported again from actual files. `architecture-decision`, `project-structure`, `test-setup.md` document the recording. | PR-approved-register, PR-approved-record, PR-unapproved-other-edge, PR-partially-approved, PR-undated-row-not-approval, reference rows in `pre-route`, AS-edit-reserved, MA-approved-edge, MA-unapproved-removal | BR-D5-ref-add |
| **D6** shell post-validation | PostToolUse covers `Edit|Write|MultiEdit|Bash|PowerShell`; new PostToolUseFailure covers `Bash|PowerShell`. `actual-state.cjs` inspects actual files only: per-worktree snapshot in the worktree's Git dir (hash per relevant file, csproj edges, HEAD); first observation baselines against HEAD; reference findings = (current Δ base) ∩ (current Δ HEAD); change-attributed messages only for content differing from HEAD; bounded (≤ 5000 entries), atomic writes, corrupt state → deterministic re-baseline. | AS-* (34 fixtures: first/later observations, same-path and identical rewrites, untracked additions, deletions, rename, failure with partial mutation, unrelated success/failure, HEAD commit/checkout/back/plus-edit/reset, unborn → first commit, excluded dirs and nested repos, in-tree worktree, corrupt state, Edit+shell, non-Git), MA-* (CPM inline, missing/floating/range central versions, CPM disabled, deny-list, illegal direction, test references, leaf-through-frame, npm floating, approvals, Edit plus shell) | BR-D6-matcher |
| **D7** checker vs settings | `check-instructions.cjs` validates exec form (`command: "node"`, `args: ["${CLAUDE_PROJECT_DIR}/.claude/hooks/dispatch.cjs", <event>]`), target existence, dispatcher handler per event, args event == registered event, required matcher coverage per event, `onFailure: "block"` on PreToolUse only, timeouts, unexpected events, shell expansion. | SE-current, SE-obsolete-shell-form, SE-event-mismatch, SE-missing-target, SE-dispatcher-missing, SE-handler-missing, SE-matcher-gap, SE-failure-missing, SE-onfailure-removed, SE-stop-blocking, SE-relative-launcher, SE-env-expansion, SE-unexpected-event, SE-timeout-missing, SE-invalid-json | BR-D7-execform: baseline checker rejects the corrected exec form |
| **D8** nested-cwd commands | One convention in `verify` (Risk-scoped checks): `node "<root>/.claude/scripts/<checker>.cjs"`, `<root>` = `git rev-parse --show-toplevel`; checkers inspect the repository/worktree containing the current directory and print it; file arguments resolve against the current directory. All five workflows updated; no cwd-relative form remains. | CL-PowerShell-*, CL-GitBash-* (toplevel + 3 checkers each, from a nested worktree dir), CL-launcher-path-from-worktree, CL-main-clean, CL-file-arg-relative-cwd, CL-instructions-consistent, MA-cli-checkall | BR-D8-nested: `Cannot find module` |
| **D9** Stop identity | Per-reminder fingerprint = id + (path, bytes) of the triggering files; bounded (100) per worktree Git dir; `stop_hook_active` → silent; Git read-only; `-z` porcelain parsing. | ST-first, ST-unchanged, ST-active, ST-same-path-material, ST-repeat-silence, ST-same-bytes, ST-worktree-local, ST-worktree-repeat, ST-seed-migration, ST-migration-review, ST-tests-cleared, ST-bounded, ST-readonly-git, ST-nongit, IF-stop-active | BR-D9-samepath |
| **D10** binding enforcement | Slot identity fixed in the checker (architecture: required frame, binds nothing; persistence and backend-testing: required leaves that must bind architecture; frontend: optional independent leaf). Contracts now carry `- Binds:` and a `## Facet roles` table; contract and module `Binds:` must agree, name only the frame, and state a reason; module facets must equal the contract's role locations (KNW = register's knowledge facet); duplicate selection rows rejected. | CP-* (33): module removed/redirected/`—` for both leaves, contract-only removal, **both sides removed/redirected together (CP-persist-both-removed, CP-testing-both-removed, CP-both-redirected)**, nonexistent/wrong slot, frame→leaf, missing reason, extra slot, second implementation, second selection, missing slot, missing facet, moved facet role, knowledge mismatch, leaks, none-with-module, required none; positives CP-baseline, CP-positive-independent | BR-D10-binds: baseline 0 errors with `Binds: —` |
| **D11** ENF graph | Every ENF artifact declares `Conforms:` (line after the header). Targets must exist and be STD or DEC; capability direction enforced (non-slot ENF → neutral owners; facet → own module, neutral owners, or the bound frame); every STD/DEC owner path an ENF artifact cites must be declared (no evasion by omission). ENF edges join the cycle check; Markdown references to ENF are enforcement pointers; skill/agent names and `SKILL.md` paths are routing pointers. The ranked `WF → KNW → STD → DEC → OP` check is unchanged. | KS-* (34): ENF→STD / ENF→DEC / WF→STD accepted, WF→KNW kept as routing, DEC→STD, OP→STD, OP→DEC, cycle, ENF→KNW/WF/OP, missing declaration (facet and non-slot), invalid target, omission, frame→leaf, non-slot→facet, facet removed/replaced, Kind lie, owner lie, routing-not-conformance, ENF inventory completeness | dossier evidence (baseline RANK excludes ENF) |

Additional defects found and fixed during the primary audit (beyond the dossier): (1) `lib.walk` descended into nested Git roots, so with an in-tree worktree (`.claude/worktrees/<name>`) the main checkout's checkers treated the worktree's files as its own (reproduced on the baseline: BR-new-intree-worktree; fixed: CL-intree-worktree-excluded, CL-intree-worktree-own, AS-intree-worktree-main/-own); (2) checkout/reset and unborn first observations initially produced deletion/product-input messages for changes fully explained by HEAD — fixed by HEAD-relative attribution (AS-head-checkout, AS-head-back, AS-unborn-first); (3) a research label I had introduced in checker comments was removed (HY-no-research-metadata).

## 4. D12 — 196-policy fidelity (source-based)

A ledger maps each of the 194 inventory policies and GOV-017/GOV-018 to exactly one owner file plus an exact owner-text anchor, built by reading every `normalized_policy` against the owner text; `fidelity.cjs` then verified it mechanically.

| Measure | Result |
|---|---|
| Policies reconciled | 196 / 196 (missing 0, extra 0, duplicates in ledger 0) |
| Owner anchors present | 196 / 196; 195 byte-identical to the baseline owner text, 1 punctuation-only change (WF-007: list colon → period in `verify`) |
| Trigger-role deltas | **0** (always → `CLAUDE.md`/register; path → STD rule; workflow → WF skill/agent) |
| Minimum-scope misses | **0** (rule `paths` cover the policy scope) |
| Normative strength/conditions | 0 weakened/strengthened; 5 screen hits (SEC-003, RUN-012, DEP-004, DEP-005, WF-002) manually confirmed as unchanged imperative/checklist/heading forms |
| Duplicate normative owners | 0 verbatim; restatement scan: 1 candidate (API-017 vs register) = the distinct owner of DEP-012 (inherent inventory overlap, unchanged) |
| Changed Markdown lines | 20 replaced lines, all adjudicated: D8 command form, appended D5 recording procedure (original text kept), D7 hook-maintenance guidance, MAP rows; no policy text weakened |
| V2 technique | no KNW skill/reference or STD rule changed or deleted; 633 V2 sections: mean best-match 0.6560 vs baseline 0.6553; one per-section decrease (project-structure "Adding a project later", 0.94 → 0.92, original steps retained); lowest sections sampled (list-to-prose, e.g. Docker anti-patterns and image variants still present) — no genuine loss, nothing needed restoring |

## 5. D13 — efficiency, complexity, capability value

| Measure | Baseline | Refined |
|---|---:|---:|
| Runtime files | 85 | 87 |
| Runtime bytes | 346,715 | 399,353 |
| Markdown files / rules / skill entry points | 72 / 21 / 30 | 72 / 21 / 30 |
| Always-loaded estimate (checker) | ~4,849 tokens | ~4,849 tokens (unchanged) |
| Hook events | 3 | 4 (adds PostToolUseFailure) via one dispatcher |
| Slots / registers / Kinds / Scopes | 4 / 1 / 7 / 6 | 4 / 1 / 7 / 6 |
| Hook latency sample (process spawn incl.) | — | PreToolUse 167 ms, PostToolUse(shell) 883 ms, Stop 716 ms |

All growth is ENF code (+52.6 KB) needed by D1–D11, plus 4 contract tables and one `Conforms:` line per ENF artifact. No meta-layer, no new Kind/Scope/slot/Level, no dynamic discovery, no second decision surface. Considered and rejected: a separate approval file for Reserved references (second decision surface), snapshotting in PreToolUse (would couple the fail-closed guard to state I/O), a self-attested bypass token for removals (removals instead run through `add-dependency` by manifest edit + restore), and a global optimization of Git calls (no defect). **Intentionally reverted neutral trade-offs:** none were introduced, so none were reverted.

## 6. K1 identity, capabilities, hooks — summary of evidence

- **K graph + ENF:** ranked chain retained and re-tested; ENF declarations complete for all 14 ENF artifacts (KS-enf-inventory, KS-enf-declared); mutation results per §3 (D11 row).
- **Modules/manifests/contracts/facets:** module facet tables equal contract facet roles; Kind/Scope/Capability of each facet match; leak rule unchanged and re-tested (CP-leak-*); exactly 4 slot directories with one implementation each (CP-four-static-slots).
- **Optional frontend clear (isolated copy only):** removing the module, its four facets, the MAP rows and setting the register row to `none` gives 0 errors / 0 warnings (CP-frontend-clear-check), neutral pointers become dormant role pointers (CP-frontend-clear-dormant), no `Angular`/`angular` token remains anywhere (CP-frontend-clear-no-leak), checkers and hooks still run (CP-frontend-clear-runtime); the authoritative template keeps angular selected (CP-authoritative-keeps-frontend). New tolerance, stated explicitly: only exact contract-declared facet-role paths of an optional slot selected `none` may be referenced without resolving.
- **Pre-route fixtures:** blocked — npm install/i/^range/@latest/uninstall/remove/rm, `--prefix`/`--workspace`/`-w` (before and after the verb), pnpm `--dir`/`-C`, yarn `--cwd`, `yarn workspace`, `yarn remove`, `npm update`, `npm update x`, `yarn upgrade`, `pnpm up x`, `npm audit fix`, `--force`/`--legacy-peer-deps` (incl. global-option and `ci` forms), dotnet `add/remove [project] package`, `package add/remove`, floating `--version 4.*`, both reference syntaxes (add/remove, multiple refs, `--project`, `cd` + implicit project), chains (`&&`, `;`, `||`, pipes, redirections, newlines), `bash -c`, `cmd /c`, `powershell -Command`/`-EncodedCommand`, env prefix, quoted full paths, `sudo`, PowerShell `&`, `Set-Location`, `Push-Location`, `*> $null`. Allowed — restores (`npm install`, `npm ci`, `yarn`, `pnpm install`), exact versions (incl. global-option forms and `dotnet package add X@v`), read-only (`npm ls/view/audit`, `dotnet list/package list/restore/build/test`, `--help`), `npm run … -- --force`, `npm cache clean --force`, local specs, `dotnet new`, and command text inside `git commit -m`, `echo`, `grep`, `Write-Output`, comments.
- **Pre vs post separation:** classification never reads files; post-execution uses only actual file state (AS-failure-partial detects a partial change after a failed command whose text names nothing).

## 7. Audits

- **Primary audit:** full matrix + D12/D13 reviews + manual review of all runtime code. Template defects found and repaired: the three listed at the end of §3. Test-only corrections (wrong fixture path, too-broad regexes, incomplete allowed-diagnostic lists for relevant consequential errors, one mis-parsed root) were fixed in the harness and are not counted as runtime repairs.
- **Confirmation audit (one, on final bytes `0b7b52ee…`):** manual review of the complete diff against the baseline and re-read of every changed/added script, then all 13 groups rerun: **324 / 324 PASS** — baseline-repro 13, hook-root 15, input-failure 25, pre-route 92, actual-state 34, manifest-architecture 14, kind-scope 34, capabilities 33, stop 14, settings 15, cli 14, hygiene 9, fidelity 12. **0 concrete template defects.** (`baseline-repro` passes mean the dossier defects reproduce on the immutable baseline.)
- **Hygiene/references:** all 11 JavaScript files parse, settings JSON parses, structure checker 0/0 (includes internal reference resolution, imports, MAP completeness and existence), manifest checker clean, English-only, no research labels/IDs/workspace paths, `SPECIFICATION.md` empty, no sibling/external dependencies.

## 8. Known limitations

- No live host activation: `onFailure: "block"` for host-level failures (missing script, timeout), exec-form substitution, and the PostToolUseFailure event are exercised through documented-semantics emulation; the dispatcher's own fail-closed exit 2 covers in-process failures independently of the host.
- The classifier covers the documented forms above; other forms (e.g. `Start-Process`, package managers invoked by scripts, `dotnet tool install`) are not blocked before execution. Their resulting manifests are still validated after execution, but a removal performed that way is not reported (the resulting manifest is valid).
- A reference change committed inside the same shell command as the mutation is no longer pending and is not reported as Reserved; content rules still run on the changed file.
- The first observation in a worktree attributes every uncommitted relevant change (including pre-session edits) once.
- Initial scaffolding now records its project references as one accepted-decision row before running `dotnet … reference` commands (consequence of treating every reference-graph change as Reserved).
- Approval matching is textual (`From -> To`, project names); approval content remains the workflow's responsibility. Outside Git, the snapshot lives in the OS temp directory and the file listing walks the tree (skipping build directories and nested Git roots); the snapshot is capped at 5,000 relevant files (beyond that, every observation baselines against HEAD).
- Post-shell observation costs about 0.9 s per shell command in the sample (several Git process spawns on Windows).

## 9. Workspace events (directly observed)

- Experimental isolation violations: **0** (no sibling, parent, network, or external-repository access).
- Recoverable workspace-process incident: at the start two temporary hash-list files were written to `/tmp`; they were deleted immediately (content: hashes of the baseline copy only).
- Platform-managed events: the session working directory followed in-workspace `cd` commands, so Claude Desktop auto-loaded the template's `CLAUDE.md` (with its imported register) and discovered the template's skills (none were invoked); oversized command outputs were stored in the tool runtime's result storage and those specific outputs of in-workspace files were read back. No forbidden information was consumed and the result does not depend on these events.

## 10. Why the result is strictly better

The baseline fails D1–D11 concretely (13 reproduced failures); the refined template passes every one of them with discriminating fixtures, while keeping K1's exact Capability → Kind → Scope identity, the seven Kinds, six Scopes, one decision register, four static slots, frame/leaf ownership, neutral-policy/facet split, the leak rule, all 196 policies with their owners, trigger roles, minimum scopes and strengths, V2 technique, and the ~4.85k-token always-loaded surface. Hooks now inspect the worktree Claude is actually editing, fail closed where policy is critical, read Windows encodings, route every documented dependency and reference mutation before execution, validate actual state after successful and failed shell commands, remind on materially changed content without loops, and the structure checker enforces the corrected configuration, independent binding obligations, facet roles, and the complete K graph including ENF.

## Corrective pass — iteration 2

### Decision: **STRICTLY_BETTER** (iteration 2 over K1 Run-02 and K1_1)

Both independently demonstrated blockers are closed with discriminating fixtures on the final bytes: (A) XML attribute parsing is quote-equivalent; (B) only a validly dated accepted-decision row authorizes a Reserved reference change. Every fixture that K1_1 already passed still passes. The change is confined to the two expected ENF scripts (+1,581 bytes). The one cumulative confirmation on stable bytes found 0 concrete template defects. Sections 1–10 above remain the iteration-1 record. Their 324/324 count is historical evidence: that harness was deleted and was not reconstructed.

### I2.1 Provenance and file identity

| Item | Value |
|---|---|
| Start (K1_1, verified once) | `output/template`: 87 files, 399,353 bytes, tree `0b7b52ee100b58f136727cf6892441465e23175607de667203333de41d5965e5` (matches the expected value) |
| Final | 87 files, 400,934 bytes, tree `52d74f3560085066f75e5ef5c8d112ba2a0680c6e34f44e068de005a3c9759e4` (identical before and after the confirmation run) |
| Tree hash definition | unchanged: SHA-256 of the `LC_ALL=C`-sorted `sha256sum -b ./<path>` list |
| Changed: `.claude/scripts/lib.cjs` | `5b834bb0adc40905fa65234debba7a7ccadadcdd2f05f727eb9c51b9b3c8d4b3` (6,761 B) → `f83639458289c5c58531127d3f69c8797949fe1a0f371dcd5eca79daf4e57e0e` (7,649 B) |
| Changed: `.claude/scripts/check-manifests.cjs` | `da90bd624ef736f3c53036b957f263a1ec19bcebbd5a98772ca8c0a968183baf` (11,100 B) → `1d704db02381c6ce9c0dd28717131f5d46f73dcb45c8ef2bdf9252381eb9a0be` (11,793 B) |
| Unchanged | the other 85 files are byte-identical to the starting per-file inventory; none were added or deleted. The header and `Conforms:` lines of both changed scripts are unchanged. |
| Immutable inputs | `baseline/template` tree `9e524c3f…8bec` unchanged; `baseline/`, `source/`, `audit/`, task and prompt files were not written |
| Pre-existing manifest discrepancy | `MANIFEST.sha256`: 142/144 entries verify. `GOAL_PROMPT.txt` and `REFINEMENT_TASK.md` differ because of the intentional K1 prompt refactor (both files are dated before this pass). Iteration 2 neither caused nor modified this. |

### I2.2 Root causes and repair

- **Blocker A — XML quote parity.** Inherited from Run-02 and unchanged in K1_1. `lib.xmlElements` read only `name="value"` attributes and ended a start tag at the first `>`. `parseProject` read the root SDK with a separate double-quote-only expression. It also turned a missing or unparsed `Include` into an edge to the containing project, producing a fabricated self-reference.
  - **Repair:** `xmlElements` is now one quote-aware start-tag reader. It does a sticky scan of `name = "…"` and `name = '…'` attributes in any order and spacing. A quoted `>` does not end the tag. It handles self-closing and paired forms and reads simple child elements as before.
  - **Malformed tags:** a malformed start tag throws. `checkFile` and the actual-state hook then report it as an unreadable manifest instead of silently skipping the element.
  - **`parseProject`:** reads the root `<Project>` `Sdk` through the same reader and creates reference edges only from an `Include`.
  - **Shared path:** all five inspection surfaces use the one reader: PackageReference (including `VersionOverride` and facet leaks), PackageVersion, ProjectReference, FrameworkReference and the root SDK. The CLI and PostToolUse/PostToolUseFailure share `parseProject`/`checkFile`, so no hook file changed.
- **Blocker B — undated approvals.** Introduced in K1_1 (Run-02 had no approval reader). `acceptedDecisionText` excluded only the values empty, `—`, `-` and `Date`, so any other text in the Date cell, such as `TBD` or `pending`, authorized the row.
  - **Repair:** a row, and the `docs/decisions/` records it links, counts only when its Date cell is exactly a real ISO `YYYY-MM-DD` calendar date: month 1–12, day within the month, Gregorian leap rule.
  - **Unchanged:** exact `From -> To` matching, the register as the single approval surface, and decision ownership.

### I2.3 Harness and reproduction on K1_1

- **Harness:** one file, `output/.work/harness.cjs`, with modes `baseline` (unmodified K1_1 copy) and `focused`/`confirm` (authoritative template). It runs 125 fixtures in 5 groups.
- **Isolation:** each fixture copies the template under test into a real Git repository, on a path containing spaces, with `GIT_CEILING_DIRECTORIES` = `output/` and no system or global Git config.
- **Execution:** each fixture runs the real `check-manifests.cjs`, `check-instructions.cjs` and `hooks/dispatch.cjs` as child processes, with stdin JSON and `cwd`.
- **Assertions:** negative fixtures assert the exit code and the **exact** diagnostic lines (category, project or package, owner). Positive fixtures assert exit 0 with zero errors and zero warnings; for hooks, stdout and stderr must be empty.
- **Safety:** hook command text was inert (`echo …`, `dotnet build # …`), and mutations were written only to fixture files.

**Baseline (K1_1): 60/125 as expected.** Every double-quoted control, preservation control and gate passed. The 65 mismatches are the reproduced defects:

| Fixture (K1_1) | Expected | K1_1 observed |
|---|---|---|
| X02, X04, X08–X11, X13, X15, X24, X25: single-quoted EF inline version, VersionOverride, denied package, ASP.NET Core package, FrameworkReference, Web SDK, UTF-8/UTF-16LE BOM | the same FAIL/warning as the double-quoted form | exit 0, 0/0 (bypass) |
| X03 mixed quotes, reversed order; X05 paired tag with child `Version` | inline-version error and EF-leak error for `Microsoft.EntityFrameworkCore` | only one of the two; X05 reports package `""` |
| X06, X07 quoted `Condition` containing `>` (both quote styles) | element inspected | element silently dropped |
| X18, X21, X23 single-quoted Application → Domain; missing `Include`; Api positive | PASS 0/0 | `Application must not reference Application`, `Api must not reference Api` (fabricated) |
| X16 single-quoted root SDK after another attribute | `Application uses the Web SDK` | only a fabricated self-reference error |
| X20 single-quoted Domain → Api | `Domain must not reference Api ("My.Api")` | `Domain must not reference Domain ("My.Domain")` |
| X28–X32, X34–X36 PackageVersion with single or mixed quotes | exact versions PASS; floating, range, missing or denied FAIL naming `NewDep` or the package | `PackageVersion "" has a missing, floating, or range version …` (empty package identity; false FAIL for exact versions); X35 silently dropped |
| X26 unquoted attributes (invalid XML) | visible unreadable-manifest error | exit 0, 0/0 |
| H01–H03, H08: PostToolUse (Bash, primed and first observation), PostToolUseFailure (Bash, PowerShell) | the same violations as the CLI | exit 0, silent |
| H04 same-path rewrite of Application → Domain into single quotes | silent (graph unchanged) | `My.Application -> My.Application added; My.Application -> My.Domain removed` plus a fabricated direction error |
| H05, H09, H11 single-quoted new reference | correct edge (`My.Domain -> My.Api`, `My.Api -> My.Domain`) | fabricated self-edges |
| H06, H07, H13 single-quoted PackageVersion via Edit, Bash, PowerShell failure | `NewDep "1.*"` FAIL; exact version silent; denied package | `PackageVersion ""` error in all three |
| H10 `TBD` row through the PostToolUse graph check | Reserved `My.Api -> My.Domain added` | exit 0 (approved) |
| H14a, H14c real linked worktree (launcher in the main checkout; CLI from a nested worktree directory) | violation found in the worktree | not detected |
| V04, V05, V08, V10–V12, V14, V15, V17 (23 decision assertions) | BLOCK / not approved | `TBD`, `pending`, `2026-02-30`, `2027-02-29`, `21.10.2026`, `2026-10-21 (approved)`, `2026-1-05`, `2026-13-01`, `2026-00-10`, `2026-04-31` and `1900-02-29` all authorized, as did records linked under `TBD` or `pending` rows. With mixed rows, the `TBD` edge got through, both alone and inside a multi-reference command. |

On K1_1 these were already correct: absent register, placeholder row, `—`, empty Date, unrelated edge, valid dates and fail-closed input.

### I2.4 Final results — focused run and the one confirmation, identical: 125/125

| Group | Fixtures | Content | Result |
|---|---:|---|---|
| xml — direct `check-manifests.cjs` | 37 | X01–X37. **Quoting forms:** double, single and mixed quotes, reversed attribute order, spaces around `=`, multi-line tags, paired tags with child `Version`, a `>` inside a quoted `Condition` (both quote styles), XML comments. **Edges:** a missing `Include` creates no edge. **Encodings:** UTF-8 BOM, UTF-16LE BOM. **Malformed:** unquoted attributes produce a visible `manifest could not be read (malformed <PackageReference> start tag …)`. **PackageVersion:** exact, floating, range, missing, prerelease, denied, test-framework facet. **Root SDK:** both quote styles. | 37/37 |
| hook — real dispatcher | 16 | **Events:** PostToolUse Bash (primed and first observation), PostToolUse Edit, and PostToolUseFailure Bash and PowerShell after a partial mutation (preface asserted). **Reference graph:** a same-path quote rewrite with an unchanged graph is silent; a new single-quoted Domain → Api gives the direction error plus Reserved `My.Domain -> My.Api added`; an approved single-quoted edge is silent; `TBD` and `pending` rows do not approve (`My.Api -> My.Domain added`). An unrelated failure is silent. **Worktree:** with the launcher in the main checkout of a real linked worktree, the violation is found with a worktree-relative path, the main checkout stays silent, and the CLI run from a nested worktree directory inspects the worktree. | 16/16 |
| decision — PreToolUse + helper | 49 | V01–V17 register variants, run through `PreToolUse` (`dotnet add/remove … reference`, `dotnet reference add … --project`, PowerShell tool, multi-reference command) and through direct `acceptedDecisionText`/`isApprovedEdge` calls. **Variants:** absent register, placeholder, valid `2026-10-21`, `TBD`, `pending`, `—`, empty, `2026-02-30`, leap day `2028-02-29`, `2027-02-29`, `21.10.2026`, trailing text, unrelated edge, mixed rows. **Linked records** under valid, `TBD` and `pending` rows: only the valid row's record text is included. **Also:** `→` normalization, and a date matrix (`2000-02-29` valid; `1900-02-29`, months `00`/`13`, `2026-04-31` invalid). **V18:** malformed, empty or missing-command input still blocks fail-closed and reports the input error, not a Reserved denial. | 49/49 |
| preserve — unchanged behavior | 17 | **Manifests:** check-manifests 0/0 on a clean repo; the double-quoted inline-version rejection still fires. **Structure:** check-instructions 0/0 with the always-loaded surface at 4,849 tokens. Unknown Scope, wrong Kind, a fifth slot, persistence `Binds:` removed on both sides, and an illegal ENF → KNW edge are each rejected with their specific diagnostic. **Optional frontend:** cleared in an isolated copy, instructions 0/0, manifests 0/0, no Angular token left. **Stop:** reminds, stays silent on repeat, reminds again after a same-path rewrite, silent under `stop_hook_active`. **Classifier routing:** npm install/ci, exact `dotnet package add`, `dotnet package remove`, `--prefix`, command text inside `git commit -m`, `cd` plus an implicit project reference. | 17/17 |
| gate | 6 | `node --check` on all 11 `.cjs` files; settings.json parses; file identity (exactly the 2 files changed, 85 identical); in-place check-instructions 0/0 with the always-loaded surface at about 4,849 tokens (unchanged); in-place check-manifests 0/0; hygiene of the two scripts (headers and `Conforms:` unchanged, no research or workspace labels, no new non-ASCII) | 6/6 |

### I2.5 Cumulative boundary

- **D1–D13 and the 194+2 policies.** No rule, skill, contract, module manifest, register, settings, hook, classifier or facet file changed. The 85 byte-identical files carry the iteration-1 evidence for those surfaces, including policy owners, triggers, minimum scopes and V2 technique. The two changed files are ENF helpers whose headers and `Conforms:` declarations are unchanged. The changed parser and approval behavior were freshly tested above, not inferred from unchanged files.
- **K1 identity.** Re-confirmed on the final bytes by the structure checker and the representative negatives in `preserve`: 7 Kinds, 6 Scopes, one register, 4 static slots with required-leaf `Binds: architecture`, and the ENF graph.
- **Cost.** The always-loaded surface is unchanged at about 4,849 tokens; the runtime grew by 1,581 bytes. There is no new file, Kind, Scope, slot, setting, hook or approval surface.

### I2.6 Audits and anomalies

- **Baseline reproduction:** one run on K1_1, 60/125 (the 65 mismatches above).
- **Focused run** after the two edits: 125/125.
- **Confirmation:** **one** cumulative run with the frozen harness, whose SHA-256 `a3a6aa84…` is unchanged since the baseline run, on the final bytes. Result 125/125, tree hash identical before and after, **0 concrete template defects**. There was no runtime re-fix and no second confirmation.
- **Harness correction:** test-only, made once, before any result was recorded. Case labels containing `>` had been used as Windows directory names; the harness switched to the short case ID. No expected value was changed.
- **Workspace:** no sibling, parent or network access. Git discovery was bounded by `GIT_CEILING_DIRECTORIES`. All fixtures lived under `output/.work/`, which is removed after this report is written, leaving `output/` = `template/` + this report.

### I2.7 Known limitations and caveats (iteration 2)

- **Date format.** Only an exact ISO `YYYY-MM-DD` Date authorizes, as this pass specifies. The `architecture-decision` workflow says "date" without naming the format, and the hook's block message points to that workflow without mentioning it. Both are outside the two-file scope. A non-ISO date therefore fails closed: the reference command is blocked and reported as unapproved, not accepted.
- **Unchanged MSBuild item semantics.** These are not quote-related. I observed them by reading the code; they were not tested and not changed:
  - semicolon-separated `Include` lists are not split into items;
  - attribute values are not trimmed;
  - XML character entities in values are not decoded;
  - `$(…)` properties are not expanded;
  - SDKs declared through `<Sdk Name=…>` or `<Import Sdk=…>`, and child `<Version>` elements that carry attributes, are not inspected.
- **Malformed start tags.** A malformed start tag (invalid XML, such as unquoted attribute values) is now reported as an unreadable manifest instead of being skipped. On the hook path the same file is reported twice (manifest check and reference-graph read), as other unreadable project files already were.
- **No live host activation.** As in iteration 1, hooks were executed as controlled child processes with documented input semantics.
