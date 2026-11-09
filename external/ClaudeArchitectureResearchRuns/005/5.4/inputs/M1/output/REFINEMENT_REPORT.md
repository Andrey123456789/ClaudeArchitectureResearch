# Refinement Report — M1 / Run-02

## Final Status

**STRICTLY_BETTER** (cumulative, after corrective iteration 2)

All eight confirmed defects (D1–D8) are fixed with deterministic behavioral evidence, one adjacent
worktree defect found during the audit is fixed, the three quality gates (Q1–Q3) were reviewed with
targeted changes, no binding regression was found, and the result is the same M1 architecture
(four static capability slots, flat M-style rules, frame/leaf rule, no Level/Kind taxonomy).
Corrective iteration 2 (Section 16) closed the two residual gaps found by a later audit: shell
commands are now judged by their actual effect on manifests and project files after successful
and failed Bash/PowerShell calls (`PostToolUseFailure`), including HEAD transitions, same-file
rewrites, deletions, and moves in repository roots, nested directories, and real worktrees; and
hook input is UTF-8-BOM tolerant while the critical PreToolUse hook stays fail-closed. Every
earlier result was re-verified unchanged, and the cumulative confirmation audit found zero
concrete template defects.

## 1. Baseline Identity and Hashes

| Item | Value |
|---|---|
| Baseline | `baseline/template/` = 5.2 / M1 / Run-02 (PROVENANCE `selected_baseline`) |
| `MANIFEST.sha256` | all 140 entries verified OK before and after refinement (baseline, source, audit, task files unchanged) |
| `CANDIDATE.md` | `f1b209f4984ecf93b35c4552026f0b5ed85fada9d54d337c5b47b2642332bff3` (= PROVENANCE `candidate_sha256`) |
| Baseline report | `67ea0ebe749ecccbb8ee72ac78394fb0fd941fa8f3a509a489711c38928913d7` (= PROVENANCE `baseline_report_sha256`) |
| Baseline tree hash¹ | `f3cbfd5d87e39307de67cf57198460230734c203cf45d154253a587d5f3e860d` |
| Output tree hash¹ (final, after iteration 2) | `60b39d95af92099e0af5fdc0ca53d6f899899fe715a86ed43e74b57389eed49b` |
| Iteration-1 output tree hash¹ | `84fd48d280e7a9881f60f4b685388636f016e7d956ea5cdfa967be4f6d44d138` |
| `source/inventory.json` | `bcf1a1532437f4a1d7bfafcb1f27ebcbb832ba684e35b8a42569cd9d2d9ad168` |
| `source/shared-research-invariants.json` | `51b442b118b55ea89e16f3ac8603309d66635a7d184e456af2091d584f7da6d7` |

¹ SHA-256 over the sorted lines `<sha256-of-file>  <relative path>` of every file in the template.
(The PROVENANCE `baseline_template_tree_sha256` uses an undocumented method; identity is
established through the per-file `MANIFEST.sha256` entries, which all verify.)

`output/template/` started as an exact copy (`diff -r` empty). Changed files (baseline → final output,
first 12 hex digits of SHA-256; iteration 2 changed ten of them again, see Section 16.3 for the
iteration-1 hashes); the other 61 files are byte-identical to the baseline:

| File | Baseline | Output | Reason |
|---|---|---|---|
| `.claude/settings.json` | `0c493e2de5b3` | `7ea3bfbc19f2` | D2, D8, I2 |
| `.claude/hooks/pre-tool-use.js` | `58db15b3de3a` | `0191df357e55` | D3, D4, D8, I2 |
| `.claude/hooks/post-tool-use.js` | `4429735d81cc` | `0de60c2d7a85` | D1, D3, I2 |
| `.claude/hooks/stop.js` | `2f2a5d2d5ad2` | `0709d980e8c9` | D1, D7, I2 |
| `.claude/scripts/lib/common.js` | `189c1f9fa53c` | `cfe2358e18d4` | D1, D6, I2 |
| `.claude/scripts/lib/dependency-commands.js` | `e0082ce89969` | `62efa646f2bd` | D3, D4 |
| `.claude/scripts/lib/hook-output.js` | `596f0b4c9702` | `f8a135e48ff5` | D8, I2 |
| `.claude/scripts/check-instructions.js` | `2b622b7d4942` | `98b741da768b` | D5, I2 |
| `.claude/scripts/check-manifests.js` | `934d3fd2ac60` | `4db4f14dbb4a` | D6, I2 |
| `.claude/scripts/check-architecture.js` | `a3e3ede311ad` | `49647ea148f7` | D6, I2 |
| `.claude/skills/project-structure/SKILL.md` | `a14c87493c3f` | `140a4c74cabd` | D4, D6 |
| `.claude/skills/development-workflow/SKILL.md` | `203291df566e` | `f5ea2951cb6e` | D4 routing |
| `.claude/skills/verify/SKILL.md` | `10359e58fc4e` | `b362c4d7ceb2` | D6 |
| `.claude/skills/add-dependency/SKILL.md` | `8ad9fba35c87` | `559ab9eb214e` | D6 |
| `.claude/skills/template-maintenance/SKILL.md` | `109df8ad02b9` | `91e9ba6989a0` | D6 |
| `.claude/skills/code-review/SKILL.md` | `22151d09d241` | `99d4a418e4be` | D6, Q1 |
| `.claude/skills/ef-core/SKILL.md` | `49efd50c885a` | `525cf3a7b08e` | Q2 |
| `.claude/capabilities/persistence/ef-core/MODULE.md` | `067af9813eb0` | `43815c211f24` | Q2 |
| `.claude/MAP.md` | `8b4bc930f430` | `78e82cfc82f7` | map of the above, I2 |

## 2. Old vs. New Metrics

| Metric | Baseline | Output | Delta |
|---|---:|---:|---:|
| Runtime files | 80 | 80 | 0 |
| Total bytes | 368,816 | 405,146 | +36,330 |
| Markdown files / bytes | 67 / 303,524 | 67 / 307,055 | 0 / +3,531 |
| JavaScript files / bytes | 9 / 61,012 | 9 / 93,601 | 0 / +32,589 |
| Flat rules / skills | 14 / 29 | 14 / 29 | 0 |
| Always-loaded files / bytes | 7 / 16,474 | 7 / 16,474 | 0 (byte-identical) |
| Always-loaded estimate (checker, incl. skill listings) | ~5,568 tokens | ~5,568 tokens | 0 |
| Capability slots / implementations | 4 / 4 | 4 / 4 | 0 |
| Checker result | 0 errors, 0 warnings | 0 errors, 0 warnings | — |

The byte increase is almost entirely enforcement code required by D1/D3/D4/D7/D8 (a real
Bash/PowerShell command parser, the two-root model, content-identity hashing, fail-closed
handling) and by iteration 2 (+8,215 JavaScript bytes for the actual-state manifest check,
the failure event, and BOM/UTF-16 tolerance; +290 Markdown bytes in two map rows). No file,
layer, slot, or always-loaded content was added. Iteration-1 figures: Section 16.8.

## 3. Confirmed Defects D1–D8

| # | Defect | Fix | Test evidence (output) | Baseline on same tests | Result |
|---|---|---|---|---|---|
| D1 | Repository checks used a static root from the script location, so a worktree was checked against the main checkout | `common.js` two-root model: **launcher root** (script location) only loads code; **active root** = Git top-level of hook-input `cwd` (parsed first) when it holds the instruction system, otherwise the nearest enclosing directory with `CLAUDE.md` and `.claude/` (bounded by that top-level, or anywhere above `cwd` when there is no repository yet); never the launcher root. All path containment, walking, manifest/architecture/instruction checks, Git calls, and Stop state use the active root. Paths are canonicalized (junctions/symlinks/short names). Nested repositories/worktrees (e.g. Claude Code's `.claude/worktrees/<name>`) are not walked as part of the outer checkout | 15 D1 tests in real Git worktrees under paths with spaces: invalid worktree manifest detected; valid equivalent passes; nested cwd maps to worktree root; invalid main does not leak into worktree, valid main does not hide invalid worktree; edits outside the active worktree and `..` escapes are not checked as inside; CLI path outside root rejected (exit 2); nested `.claude/worktrees` checkout neither pollutes nor is hidden; junction cwd and junction file path resolve; Stop reads the worktree change set — **15/15 pass** | 11 of these are wrong (misses the worktree manifest, substitutes main state, 119 false instruction errors from a nested worktree, junction paths missed) | Fixed |
| D2 | Complex shell-form `node -e "require(...)"` launcher | Exec form for all three hooks: `"command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.js"]` | Launch matrix (project root, nested cwd, worktree root, nested cwd in worktree; all under a path containing spaces; Windows, `shell: false`, placeholder substituted as a plain string; Windows backslash `file_path`) — **18/18 pass** | Baseline launches too, but through a shell form; it routes none of the global-option forms | Fixed |
| D3 | npm/pnpm/yarn global options before the subcommand bypassed routing; pre and post phases used different regexes | One tokenizer/classifier (`classifyCommand`) drives both `analyzeCommand` (PreToolUse) and `changesManifests` (PostToolUse): Bash/PowerShell lexing (quotes, comments, `;` `&&` `\|\|` `\|` `&`, subshells, redirections, heredocs/here-strings, shell-aware line continuation), wrapper removal (`sudo`, `env`, `FOO=1`, `&`, `if`…), nested `bash -c`/`pwsh -Command`/`cmd /c`, `npx`/`npm exec`/`corepack` re-dispatch, per-manager global options with value consumption (`--prefix`/`-C`, `--workspace`/`-w`, `--dir`, `--filter`/`-F`, `--cwd`, …), `yarn workspace`/`global`, executable paths such as `npm.cmd`. Markers count only in the trailing comment of the same line | 125-case table, positive and negative (Section 7) — **125/125 pass** | 71/125 (54 misses or false positives) | Fixed |
| D4 | `dotnet add/remove … reference` not routed before mutation | Classified as `reference` operations (never as NuGet packages) for `dotnet add/remove [<project>] reference …` and `dotnet reference add/remove …`; denied until `project-structure` § Changing Project References (new 4-step procedure pointing to the dependency-direction rule, the frame's reference layout, and `architecture-decision` for Reserved changes) is applied and the command is re-run with `# project-reference: checked`; `changesManifests` is true so the post-command architecture check validates the result | Add/remove with explicit project operands, shorthand without project, noun-first .NET 10 form, `cd … &&` form, marker isolation (package marker does not approve a reference and vice versa), post-command outward-reference detection in a sandbox — all pass | All reference cases allowed before mutation; `dotnet reference add/remove` not even post-checked | Fixed |
| D5 | Checker hardcoded the old shell-form launcher | `checkSettings` validates the actual schema: expected events only; each event runs its script; matcher covers the required tools; `type: "command"`, `command: "node"`, `args` exactly one `${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.js`; script exists; PreToolUse must declare `onFailure: "block"`; PostToolUse/Stop must not | 17 settings mutations (old shell form, missing/extra args, cwd-relative path, missing script, shell command string, missing fail-closed, `onFailure` on Stop/PostToolUse, matcher gaps, missing/unexpected event, wrong script, invalid JSON) — **17/17 detected/passed as expected** | Baseline checker rejects the exec form and accepts the old launcher (2/17) | Fixed |
| D6 | Manual checker commands (`node .claude/scripts/…`) failed after `cd` and ignored the active worktree | One self-contained form everywhere: `node "$(git rev-parse --show-toplevel)/.claude/scripts/<checker>.js"` (works in Bash and PowerShell, from any directory of the active repository or worktree); checkers resolve the active root from their working directory and resolve file arguments against it (`verify`, `add-dependency`, `project-structure`, `template-maintenance`, `code-review`, MAP, script usage lines) | Documented commands run from a nested directory inside a worktree in Bash and in Windows PowerShell check the worktree; instruction checker passes there — **3/3 pass** | `MODULE_NOT_FOUND` from nested cwd (0/3) | Fixed |
| D7 | Stop dedup fingerprint was only `{files, messages}` | Fingerprint = SHA-256 of the reminders plus the content identity (file hash, `missing`, or `directory`) of every changed file the reminders were derived from; stored in the worktree's own Git directory; `stop_hook_active` still short-circuits | Section 9 — **12/12 pass** | In an ordinary checkout it suppresses the reminder for the same file set with modified content; inside a worktree it never reminds | Fixed |
| D8 | Critical PreToolUse failure was non-blocking | Three layers: `settings.json` PreToolUse handler `onFailure: "block"`; caught internal errors return a `deny` decision with a clear reason; failure to load the output helper exits with blocking code 2. PostToolUse/Stop keep visible non-blocking failures | Missing script, crashing classifier, crashing output helper, syntax error in the hook, unparseable input → all **blocked**; post-tool failure stays non-blocking — **6/6 pass** | All five failure modes allowed the command (non-blocking error) | Fixed |

**Additional defect found in the primary audit (same class as D1):** in the baseline, a Git worktree
created inside the project (Claude Code places them at `.claude/worktrees/<name>`) was walked as part of
the main checkout: its manifests were reported as main-checkout errors and its instruction files produced
119 false instruction-checker errors. Fixed by not walking nested repositories/worktrees (`common.walk`);
covered by the D1 tests above.

**Observed vs. simulated (method limit).** No live Claude Code session was driven, and this report
does not claim one; the workspace is isolated and the hook-engine mechanics are supplied as binding
external evidence in `audit/EXTERNAL_MECHANICS_NOTES.md`. The tests are the "controlled tests" the task
asks for:

- *observed:* the real hook scripts and `settings.json` of each template, launched as real Windows
  processes exactly as the documented exec form prescribes (`node` with the `${CLAUDE_PROJECT_DIR}`
  argument substituted as a plain string, no shell, hook JSON on stdin, `CLAUDE_PROJECT_DIR` set);
  real Git repositories, worktrees, and a directory junction under paths with spaces; real Bash and
  Windows PowerShell for the manual checker commands; real exit codes, stdout, and stderr;
- *simulated:* only the final mapping from a hook's exit status/JSON to allow, deny, or block, which
  applies the documented rules (exit 0 + JSON decides; exit 2 blocks; any other failure is non-blocking
  unless the handler declares `onFailure: "block"`).

A live runtime observation was attempted but is not obtainable in this environment:

- no Claude Code CLI is installed on `PATH` (checked with `which`/`where.exe`), and locating or
  installing one outside the workspace would have violated the workspace boundary;
- the running desktop session was moved (with the user's folder approval) into a sandbox Git
  repository created from the output template, with a worktree at `.claude/worktrees/feature`. The app
  loaded the sandbox's instruction files as context, but did not activate the sandbox's hooks for the
  running session: the probe `dotnet add Foo.Api.csproj reference Foo.Domain.csproj` executed (and
  failed harmlessly, because the project did not exist) instead of being denied, and writing a
  `.csproj` with a versioned `PackageReference` produced no PostToolUse feedback. A session's hook
  configuration is fixed when the session starts, and a fresh session cannot be started from inside
  this one. Both probes were chosen to be harmless when not intercepted; the session was moved back to
  the workspace afterwards.

Node.js must be resolvable as `node` on `PATH` (as in the baseline).

## 4. Quality Gates Q1–Q3

**Q1 — V2 fidelity.** Every one of the 41 V2 files was compared side by side with its owners in the
output (rules, `CLAUDE.md`, decision records, every knowledge and workflow skill and reference). An
automated section/code-block scan identified low-overlap areas; each was reviewed manually. Result: the
baseline preserves the V2 technique and examples; differences are condensation, policy moved to its
single owner, or leak-rule neutralization of selected implementation names. One materially useful
omission was found and restored (Section 10). The lexical diagnostic is otherwise unchanged
(130/300 exact code blocks before and after; mean section overlap 0.305 → 0.304, the only movement being
three `ef-core` sections whose layer names became role vocabulary under Q2 — same code and technique).

Per-file review record (all 41 V2 files; the per-file lexical diagnostic — section overlap, exact and
covered code blocks — is identical between baseline and output for 40 files, and `ef-core` moves only
in section overlap, 0.29 → 0.28):

| V2 file | Output owners compared | Result |
|---|---|---|
| `CLAUDE.md` | `CLAUDE.md`, `development-workflow`, `docs/technology-stack.md`, `docs/capabilities/architecture.md` | preserved; Development Workflow lives in its workflow per the construction contract |
| `CUSTOM_SETTINGS.md` | `CUSTOM_SETTINGS.md` (product input), `CLAUDE.md` § Product Sources | preserved |
| `SPECIFICATION.md` | `SPECIFICATION.md` | identical (empty) |
| `.claude/agents/code-reviewer.md` | `code-reviewer` agent, `code-review` | preserved; area→skill routing restored |
| `.claude/rules/architecture.md` | `rules/architecture.md`, `rules/persistence-technology.md`, `CLAUDE.md` § Decision Control, `docs/capabilities/architecture.md` | preserved |
| `.claude/rules/coding-style.md` | `rules/coding-style.md`, `verify` § 9 (using cleanup) | preserved |
| `.claude/rules/dependencies.md` | `rules/dependencies.md`, `add-dependency`, `docs/technology-stack.md`, `docs/capabilities/`, `verify` § 8 | preserved |
| `.claude/rules/error-handling.md` | `rules/error-handling.md`, `rules/performance.md` | preserved |
| `.claude/rules/performance.md` | `rules/performance.md`, `development-workflow` | preserved |
| `.claude/rules/security.md` | `rules/security.md`, `ef-core` § Raw SQL | preserved |
| `.claude/rules/testing.md` | `rules/testing.md`, `rules/test-framework.md`, `verify` § 4 | preserved |
| `skills/angular` | `angular`, `rules/frontend.md`, `rules/frontend-framework.md` | preserved |
| `skills/api-versioning` | `api-versioning`, `rules/api.md`, `architecture-decision` § 6, `add-dependency` § 2 | preserved |
| `skills/authentication` | `authentication`, `rules/security.md` | preserved |
| `skills/build-fix` | `build-fix` | preserved |
| `skills/caching` | `caching`, `rules/performance.md`, `rules/architecture.md` | preserved |
| `skills/ci-cd` | `ci-cd`, `verify` § 8 | preserved |
| `skills/code-review` | `code-review` | preserved |
| `skills/configuration` | `configuration`, `rules/composition.md` | preserved |
| `skills/custom-settings` | `custom-settings`, `CLAUDE.md`, `persistence-change` § 5 | preserved |
| `skills/dependency-injection` | `dependency-injection`, `rules/composition.md`, `rules/architecture.md` | preserved |
| `skills/docker` | `docker`, `rules/security.md`, `verify` § 8 | preserved |
| `skills/ef-core` | `ef-core`, `rules/persistence-technology.md`, `persistence-change` | preserved (Q2 role vocabulary) |
| `skills/error-handling` | `aspnet-error-handling`, `rules/error-handling.md` | preserved |
| `skills/git-workflow` | `git-workflow` | preserved |
| `skills/health-check` | `health-check`, `rules/api.md` | preserved |
| `skills/http-api` | `http-api`, `rules/api.md` | preserved |
| `skills/httpclient-factory` | `httpclient-factory`, `rules/performance.md`, `rules/architecture.md` | preserved |
| `skills/logging` | `logging`, `rules/composition.md`, `rules/security.md` | preserved |
| `skills/modern-csharp` | `modern-csharp`, `rules/coding-style.md` | preserved |
| `skills/project-structure` | `project-structure` | preserved |
| `project-structure/references/backend-layout.md` | `references/backend-layout.md`, `ef-core` § Persistence Layout | preserved |
| `project-structure/references/solution-layout.md` | `references/solution-layout.md`, `docs/capabilities/architecture.md` | preserved |
| `project-structure/references/technology-stack.md` | `docs/technology-stack.md`, `docs/capabilities/*.md`, `ef-core` § Project Setup, `dotnet-testing` § Test Project Setup, `angular` § Scaffolding, `rules/persistence-technology.md` | preserved |
| `skills/resilience` | `httpclient-factory/references/resilience.md`, `add-dependency` § 2 | preserved |
| `skills/security-scan` | `security-scan` | preserved |
| `security-scan/references/scan-layers.md` | `references/scan-layers.md`, `angular` § Security Review Notes | preserved |
| `skills/serilog` | `logging/references/serilog.md`, `rules/composition.md` | preserved |
| `skills/swagger` | `swagger`, `rules/api.md`, `docs/technology-stack.md` | preserved |
| `skills/testing` | `dotnet-testing`, `rules/testing.md`, `verify` § 4, `development-workflow` | preserved |
| `skills/verify` | `verify` | preserved |

**Q2 — persistence coupling.** Frame-specific names in the four persistence facets were classified:

- normative persistence rule/workflow text that says "Domain invariants" / "Domain or persistence
  changes" is domain language of the policy owners (PST-007, PST-008) and stays;
- layer and project names in `ef-core` prose, review checks, decision guide, layout root, and package
  placement were avoidable and now use the frame's role vocabulary (adapter layer, use-case layer, core
  model) resolved by the always-loaded role map;
- executable guidance keeps concrete frame names because it cannot be expressed through roles without
  becoming less usable: the registration example (`AddInfrastructure`, the frame's composition method),
  the `Persistence/` placement inside the adapter-layer project (frame-owned placement), the V2
  migration command, and the co-change globs consumed by the Stop hook.

`binds` is kept (not forced to zero) and its reason now lists exactly those four couplings, so a frame
replacement knows precisely what to revisit. The checker still verifies that a facet uses frame names
only with a declared `binds` entry.

**Q3 — minimalism.** No new slot, file, layer, decision artifact, or always-loaded text; always-loaded
bytes are identical. New maintenance concepts are limited to what the repairs require: the
launcher/active-root model (D1), the `# project-reference: checked` marker (D4), the exec-form schema
with `onFailure` (D2/D5/D8). Rejected ideas that would have added concepts are listed in Section 12.

## 5. Policy, Trigger, Scope, and Semantic Audit

An explicit owner map for all 196 policies (194 inventory + GOV-017, GOV-018) records owner file and the
anchor text that must appear there. A script checked, for output and baseline alike:

| Check | Output | Baseline |
|---|---|---|
| Policies with an owner whose anchor text is present | 196/196 | 196/196 |
| Trigger-role deltas (always 32 / workflow 41 / path 123) | 0 | 0 |
| Minimum-scope gaps (rule `paths` matched against scope sample files) | 0 | 0 |
| Anchor texts restated in a second instruction file | 0 | 0 |

Semantic review: every changed instruction file was diffed against the baseline. The diffs consist of
checker command forms (D6), the new pointer-only procedure section in `project-structure` (D4; it
classifies through `CLAUDE.md` § Decision Control and keeps every non-prescribed reference-graph change
Reserved), one routing line in `development-workflow`, the restored review routing table (Q1), role
vocabulary in the `ef-core` knowledge skill (Q2), and map updates. No normative sentence of any policy
owner changed; strength and conditions are unchanged. `SPECIFICATION.md` is still the empty product input.

## 6. Capability Identity and Conformance

| Check | Result |
|---|---|
| Slots | exactly `architecture` (frame, required), `persistence` (leaf, required, provider `sqlserver`), `backend-testing` (leaf, required), `frontend` (leaf, optional) |
| Selected implementations | one per required slot, one for the optional slot; manifests present and matching their location |
| Composition | static selection record only; no discovery or runtime selection code |
| Facets / properties / enforcement data | complete per contract (checker + independent audit) |
| Implementation-name leaks outside module facets | 0 (checker and an independent scan over Markdown, JS, and JSON) |
| `binds` | persistence → frame, reason lists the remaining executable couplings; frame use is verified |
| Unselected implementations in runtime | none; optional-frontend removal procedure applied in a sandbox → checker 0 errors, 61 instruction files, ~5,219 tokens (identical to baseline) |
| Flat rules, no `Level:` / `Kind:` | yes |
| Internal references | checker 0 errors; independent resolver 454 references, 0 unresolved |
| Hygiene | no research labels, policy IDs, run identifiers, workspace paths, or non-English text in `output/template/` |

## 7. Dependency-Command Test Matrix

Columns: expected PreToolUse decision / expected `changesManifests`; actual output; actual baseline
(`✗` = baseline differs). `dep` = routed to `add-dependency`; `ref` = routed to `project-structure`
§ Changing Project References; `force` = peer-override approval required; `⏎` = newline.
Output 125/125; baseline 71/125.

<details>
<summary>All 125 cases</summary>

| Command | Expected | Output | Baseline |
|---|---|---|---|
| `npm install lodash` | dep / true | dep / true | dep / true |
| `npm i -D typescript` | dep / true | dep / true | dep / true |
| `npm add zod` | dep / true | dep / true | dep / true |
| `npm --prefix frontend install x` | dep / true | dep / true | allow / false ✗ |
| `npm --prefix=frontend install x` | dep / true | dep / true | allow / false ✗ |
| `npm -C frontend install x` | dep / true | dep / true | allow / false ✗ |
| `npm --workspace app install x` | dep / true | dep / true | allow / false ✗ |
| `npm -w app install x` | dep / true | dep / true | allow / false ✗ |
| `npm --workspace=app install x` | dep / true | dep / true | allow / false ✗ |
| `npm install x --prefix frontend` | dep / true | dep / true | dep / true |
| `npm --loglevel warn --prefix frontend uninstall x` | dep / true | dep / true | allow / false ✗ |
| `npm update` | dep / true | dep / true | dep / true |
| `npm --prefix frontend update @angular/core` | dep / true | dep / true | allow / false ✗ |
| `npm uninstall x` | dep / true | dep / true | dep / true |
| `npm rm x` | dep / true | dep / true | dep / true |
| `npm audit fix` | dep / true | dep / true | allow / false ✗ |
| `npm exec -- ng add @angular/material` | dep / true | dep / true | dep / true |
| `npx ng add @angular/material` | dep / true | dep / true | dep / true |
| `npx -p @angular/cli ng add @angular/material` | dep / true | dep / true | dep / true |
| `cd frontend && npm install x` | dep / true | dep / true | dep / true |
| `(cd frontend; npm install x)` | dep / true | dep / true | dep / true |
| `FOO=1 npm install x` | dep / true | dep / true | dep / true |
| `sudo npm install -g @angular/cli` | dep / true | dep / true | dep / true |
| `& "C:\Program Files\nodejs\npm.cmd" install x` | dep / true | dep / true | allow / false ✗ |
| `npm.cmd --prefix frontend install x` | dep / true | dep / true | allow / false ✗ |
| `bash -c "npm --prefix frontend install x"` | dep / true | dep / true | allow / false ✗ |
| `pwsh -Command "npm install x"` | dep / true | dep / true | dep / true |
| `npm install x 2>&1 \| tee log.txt` | dep / true | dep / true | dep / true |
| `npm install \ ⏎   --prefix frontend x` | dep / true | dep / true | dep / true |
| `npm install x # add-dependency: checked ⏎ npm install y` | dep / true | dep / true | allow / true ✗ |
| `pnpm add x` | dep / true | dep / true | dep / true |
| `pnpm --dir frontend add x` | dep / true | dep / true | allow / false ✗ |
| `pnpm -C frontend add x` | dep / true | dep / true | allow / false ✗ |
| `pnpm --filter app add x` | dep / true | dep / true | allow / false ✗ |
| `pnpm -F app add -D x` | dep / true | dep / true | allow / false ✗ |
| `pnpm --filter=app remove x` | dep / true | dep / true | allow / false ✗ |
| `pnpm -r update` | dep / true | dep / true | allow / false ✗ |
| `corepack pnpm add x` | dep / true | dep / true | dep / true |
| `yarn add x` | dep / true | dep / true | dep / true |
| `yarn --cwd frontend add x` | dep / true | dep / true | allow / false ✗ |
| `yarn --cwd frontend remove x` | dep / true | dep / true | allow / false ✗ |
| `yarn workspace app add x` | dep / true | dep / true | allow / false ✗ |
| `yarn global add x` | dep / true | dep / true | allow / false ✗ |
| `yarn upgrade x` | dep / true | dep / true | dep / true |
| `yarn up x` | dep / true | dep / true | dep / true |
| `yarn ng add @angular/material` | dep / true | dep / true | dep / true |
| `dotnet add package Serilog` | dep / true | dep / true | dep / true |
| `dotnet add backend/Shop.Api/Shop.Api.csproj package Serilog` | dep / true | dep / true | dep / true |
| `dotnet add Shop.Api.csproj package Serilog --version 4.0.0` | dep / true | dep / true | dep / true |
| `dotnet remove Shop.Api.csproj package Serilog` | dep / true | dep / true | dep / true |
| `dotnet package add Serilog --project Shop.Api.csproj` | dep / true | dep / true | dep / true |
| `dotnet package update` | dep / true | dep / true | dep / true |
| `Install-Package Serilog` | dep / true | dep / true | dep / false ✗ |
| `nuget install Serilog` | dep / true | dep / true | dep / false ✗ |
| `ng add @angular/material` | dep / true | dep / true | dep / true |
| `ng update @angular/core @angular/cli` | dep / true | dep / true | dep / true |
| `dotnet add Foo.Api.csproj reference Foo.Domain.csproj` | ref / true | ref / true | allow / true ✗ |
| `dotnet remove Foo.Api.csproj reference Foo.Domain.csproj` | ref / true | ref / true | allow / true ✗ |
| `dotnet add backend/Shop.Api/Shop.Api.csproj reference backend/Shop.Application/Shop.Application.csproj` | ref / true | ref / true | allow / true ✗ |
| `dotnet add reference ../Shop.Domain/Shop.Domain.csproj` | ref / true | ref / true | allow / true ✗ |
| `dotnet remove reference ../Shop.Domain/Shop.Domain.csproj` | ref / true | ref / true | allow / true ✗ |
| `dotnet reference add ../Shop.Domain/Shop.Domain.csproj --project Shop.Application.csproj` | ref / true | ref / true | allow / false ✗ |
| `dotnet reference remove ../Shop.Domain/Shop.Domain.csproj` | ref / true | ref / true | allow / false ✗ |
| `cd backend/Shop.Api && dotnet add reference ../Shop.Application/Shop.Application.csproj` | ref / true | ref / true | allow / true ✗ |
| `dotnet add Foo.Api.csproj reference Foo.Domain.csproj # project-reference: checked` | allow / true | allow / true | allow / true |
| `dotnet add reference ../X/X.csproj # add-dependency: checked` | ref / true | ref / true | allow / true ✗ |
| `dotnet add package Serilog # project-reference: checked` | dep / true | dep / true | dep / true |
| `npm install x --legacy-peer-deps` | force / true | force / true | force / true |
| `npm --prefix frontend install x --force` | force / true | force / true | force / false ✗ |
| `npm install --legacy-peer-deps` | force / true | force / true | force / true |
| `npm ci --legacy-peer-deps` | force / true | force / true | force / false ✗ |
| `npm install x --force # add-dependency: checked` | force / true | force / true | force / true |
| `npm install x --force # add-dependency: checked # peer-override: approved-by-user` | allow / true | allow / true | allow / true |
| `pnpm add x --force` | force / true | force / true | force / true |
| `yarn --cwd frontend add x --force` | force / true | force / true | force / false ✗ |
| `npm install x # add-dependency: checked` | allow / true | allow / true | allow / true |
| `npm --prefix frontend install x # add-dependency: checked` | allow / true | allow / true | allow / false ✗ |
| `cd frontend && npm install x # add-dependency: checked` | allow / true | allow / true | allow / true |
| `echo "# add-dependency: checked" && npm install x` | dep / true | dep / true | allow / true ✗ |
| `npm install` | allow / true | allow / true | allow / true |
| `npm ci` | allow / true | allow / true | allow / false ✗ |
| `npm --prefix frontend ci` | allow / true | allow / true | allow / false ✗ |
| `pnpm install` | allow / true | allow / true | allow / true |
| `pnpm --dir frontend install` | allow / true | allow / true | allow / false ✗ |
| `yarn` | allow / true | allow / true | allow / false ✗ |
| `yarn install --frozen-lockfile` | allow / true | allow / true | allow / true |
| `npm run build` | allow / false | allow / false | allow / false |
| `npm --prefix frontend run build` | allow / false | allow / false | allow / false |
| `npm test` | allow / false | allow / false | allow / false |
| `npm audit` | allow / false | allow / false | allow / false |
| `npm ls` | allow / false | allow / false | allow / false |
| `npm outdated` | allow / false | allow / false | allow / false |
| `npm view zod version` | allow / false | allow / false | allow / false |
| `npm cache clean --force` | allow / false | allow / false | force / false ✗ |
| `pnpm --filter app build` | allow / false | allow / false | allow / false |
| `yarn --cwd frontend build` | allow / false | allow / false | allow / false |
| `yarn test` | allow / false | allow / false | allow / false |
| `npx ng build` | allow / false | allow / false | allow / false |
| `ng build --configuration production` | allow / false | allow / false | allow / false |
| `ng update` | allow / false | allow / false | allow / true ✗ |
| `dotnet build` | allow / false | allow / false | allow / false |
| `dotnet test --filter "FullyQualifiedName~Orders"` | allow / false | allow / false | allow / false |
| `dotnet list package --vulnerable` | allow / false | allow / false | allow / false |
| `dotnet package list --vulnerable --include-transitive` | allow / false | allow / false | allow / true ✗ |
| `dotnet list Shop.Api.csproj reference` | allow / false | allow / false | allow / false |
| `dotnet reference list --project Shop.Api.csproj` | allow / false | allow / false | allow / false |
| `dotnet ef migrations add AddOrderIndex` | allow / false | allow / false | allow / false |
| `git commit -m "npm install x"` | allow / false | allow / false | dep / true ✗ |
| `echo npm install x` | allow / false | allow / false | dep / true ✗ |
| `grep -rn "dotnet add package" docs` | allow / false | allow / false | allow / true ✗ |
| `cat > setup.sh <<'EOF' ⏎ npm install x ⏎ EOF` | allow / false | allow / false | dep / true ✗ |
| `Write-Output "npm install x"` | allow / false | allow / false | dep / true ✗ |
| `Set-Location C:\Projects\App\ ⏎ npm install x` (PowerShell) | dep / true | dep / true | dep / true |
| `` npm install ` ⏎   --prefix frontend x `` (PowerShell) | dep / true | dep / true | dep / true |
| `npm install \ ⏎   --prefix frontend x` (Bash) | dep / true | dep / true | dep / true |
| `git commit -m "fix @" ⏎ npm install x` | dep / true | dep / true | dep / true |
| `$body = @" ⏎ npm install x ⏎ "@ ⏎ Set-Content notes.txt $body` (PowerShell) | allow / false | allow / false | dep / true ✗ |
| `bash -lc "npm --prefix frontend i x"` | dep / true | dep / true | allow / false ✗ |
| `powershell -NoProfile -Command "npm i x"` | dep / true | dep / true | dep / true |
| `cmd /C npm install x` | dep / true | dep / true | dep / true |
| `if ($LASTEXITCODE -eq 0) { npm --prefix frontend install x }` (PowerShell) | dep / true | dep / true | allow / false ✗ |
| `npm install x; if ($?) { npm run build }` (PowerShell) | dep / true | dep / true | dep / true |
| `dotnet new classlib -n Shop.Domain -o backend/Shop.Domain` | allow / true | allow / true | allow / true |
| `dotnet sln add backend/Shop.Domain/Shop.Domain.csproj` | allow / true | allow / true | allow / true |
| `ng new Shop.Web --directory frontend/Shop.Web` | allow / true | allow / true | allow / true |

</details>

Key behavior changes against the baseline: all global-option forms now route (npm `--prefix`/`-C`/
`--workspace`/`-w`, pnpm `--dir`/`-C`/`--filter`/`-F`, yarn `--cwd`, `yarn workspace`, `yarn global`);
`dotnet … reference` routes to the project-reference owner; an approval marker on one line no longer
approves a command on another line or inside a quoted string; ordinary non-mutating commands are no
longer denied (`npm cache clean --force`, `git commit -m "npm install x"`, `echo npm install x`, heredoc
and here-string bodies); restore-type installs, `Install-Package`, `nuget install`, and
`dotnet reference add/remove` now also trigger the post-command manifest/architecture re-check, so the
two phases agree.

## 8. Worktree, Nested-cwd, and Windows Matrix

All runs: Windows 11, Node 24, Git for Windows, sandbox paths containing spaces (`…\AI Learning\…\main repo`,
`wt one`), `GIT_CEILING_DIRECTORIES` capped at the sandbox, `CLAUDE_PROJECT_DIR` = main checkout,
hook input `cwd` as listed.

| Scenario | Output | Baseline (actual outcome) |
|---|---|---|
| Write invalid `.csproj` in worktree, cwd = worktree root | block + ERROR | allow (missed) |
| Same, cwd = nested directory of the worktree | block + ERROR | allow (missed) |
| Same, relative `file_path` | block + ERROR | reminder only (checked the main file) |
| Valid worktree manifest | no ERROR | no ERROR |
| Invalid main + valid worktree, post-command check from worktree | no ERROR | ERROR from main (substitution) |
| Valid main + invalid worktree, post-command check from worktree | ERROR | no ERROR (masked) |
| Edit of a main-checkout file while cwd = worktree | not checked as worktree content | checked |
| `../../outside/Evil.csproj` | ignored | ignored |
| CLI argument outside the active root | exit 2 | exit 2 |
| Nested worktree in `.claude/worktrees/feature`: main checks | clean | ERROR + 119 instruction errors |
| Nested worktree cwd | checks the nested worktree | checks it |
| Junction to the worktree as cwd and in `file_path` | block + ERROR | allow |
| Stop in worktree with a model change | reminds | allow (looks at main) |
| PreToolUse / PostToolUse / Stop launch from root, nested, worktree, nested-in-worktree (exec form, no shell) | launched, routed | launched (shell form), global-option form not routed |
| Windows backslash `file_path` | contained and checked | contained and checked |
| Documented manual checker from nested worktree dir, Bash | checks the worktree | `MODULE_NOT_FOUND` |
| Same, Windows PowerShell | checks the worktree | `MODULE_NOT_FOUND` |
| Template copy before `git init` | post/pre checks run; Stop fails visibly | same |

## 9. Stop-Hook State Tests

| Step (worktree `wt one`, then `wt two`) | Output | Baseline |
|---|---|---|
| Model file changed without seed/migrations → stop | reminder | allow (checks main) |
| `stop_hook_active: true` | allow (no loop) | allow |
| Later stop, unchanged state | allow (no repeat) | allow |
| Unrelated file changed | allow (no noise) | allow |
| Same file set, modified model content | reminder again | allow (suppressed) |
| Repeat with that modified state | allow | allow |
| `wt two` with equivalent file names and content | reminder (not suppressed) | allow |
| Main checkout without changes | allow | allow |
| State file location | each worktree's own Git directory | n/a (main only) |
| Ordinary checkout (no worktree): model change → stop | reminder | reminder |
| Ordinary checkout: later stop, unchanged | allow | allow |
| Ordinary checkout: same file set, modified content | **reminder again** | **allow (suppressed — the D7 defect)** |

## 10. V2 Material Restorations

| Restored | Where | Why |
|---|---|---|
| The V2 reviewer's "Project Guidance" routing from changed area to knowledge skill (persistence, tests, frontend, authentication, HTTP, error handling, outbound HTTP/resilience, caching, configuration/DI, containers/CI, security-sensitive changes) | `code-review` § Step 2 (canonical procedure; the `code-reviewer` agent preloads it and stays thin) | Operational review technique dropped by the baseline; capability skills are referenced by slot role, so no implementation name leaks |

No other V2 technique was missing; no duplicate normative text or research material was restored.

## 11. Intentional Baseline Behavior Retained

- Hook decisions as ASCII-only hook JSON with exit 0; PostToolUse and Stop failures visible and
  non-blocking; Stop loop prevention through `stop_hook_active`.
- Marker syntax `# add-dependency: checked` and `# peer-override: approved-by-user` (now line-bound).
- Global tool installs (`npm i -g …`) and `npm audit fix --force` still require the workflow / approval.
- Post-command checks after `dotnet new`, `dotnet sln`, and the frontend framework CLI's project creation.
- The frontend framework CLI stays recognized inside the embedded classifier (written without leak tokens)
  so the fail-closed pre-tool hook reads no repository state.
- All policy owner texts, trigger roles, scopes, the always-loaded surface, the capability model, the
  checker's structural predicates other than hook wiring, and the optional-frontend removal procedure.

## 12. Rejected Refinement Ideas

| Idea | Reason rejected |
|---|---|
| Role placeholders in the persistence co-change globs, resolved by the Stop hook | New resolution mechanism (Q3); `Persistence/…` sub-paths are frame placement anyway, so `binds` would remain |
| Role placeholders in the migration command | Makes an executable V2 example less directly usable (Q1 vs. Q2) |
| Moving frontend-CLI recognition into the frontend manifest | Would make the critical fail-closed pre-tool hook depend on repository state, so a broken selection file would block every shell command |
| `onFailure: "block"` on PostToolUse / Stop | No effect on Stop; would turn post-change reporting into blocking |
| Deriving the active root from the edited file instead of `cwd` | Contradicts the required model and reintroduces cross-checkout substitution |
| Adding "project references" to the `CLAUDE.md` routing table | Grows always-loaded context; the `project-structure` description already names project references and the hook routes deterministically |
| Pre-routing `dotnet new` / `dotnet sln add` | Not a confirmed defect; would add friction without evidence; post-checks retained |
| Rewording "Domain invariants" in persistence policy owners to role terms | Domain language of policy owner text; churn without substitutability gain |

## 13. Audit Cycles and Confirmation

This section records iteration 1 (template `84fd48d2…6d44d138`). The cumulative confirmation of
the final template after corrective iteration 2 is Section 16.12.

Primary audit repairs that changed the template after the first implementation: shell-aware line
continuation, unbalanced-quote here-string detection, and `bash -lc` / `pwsh -Command` prefixes in the
parser; the `project-structure` procedure step reworded to classify through Decision Control without
reinterpreting Reserved item 3; the reference-routing hook message reduced to a pointer; line wrapping.

**Confirmation audit: 0 concrete template defects.** It was performed as one clean, uninterrupted
run of a single script over the frozen template (output tree hash `84fd48d2…6d44d138`, verified at the
start of the run), after the evidence set (all test cases and audit scripts) was final, on freshly
created sandboxes:

| Gate | Output | Baseline (comparison) |
|---|---|---|
| `MANIFEST.sha256` (protected inputs) | 140/140 OK | — |
| Script syntax (`node --check`) | 0 failures | — |
| `check-instructions` / `check-architecture` / `check-manifests` | 0 / 0 / 0 errors, 0 warnings | — |
| Command matrix | 125/125 | 71/125 |
| Hook behavior (D1, D2, D6, D7, D8, regressions) | 69/69 | 48/69 (all 21 failures in D1/D6/D7/D8 rows) |
| Checker hook-schema cases | 17/17 | 2/17 |
| Policy audit (owner, trigger role, scope, restatement) | 196/196 | 196/196 |
| Independent structure audit | 0 issues (454 references) | 0 issues (449 references) |
| Optional-frontend removal | 0 errors | 0 errors |
| V2 lexical diagnostic (41 files) | 130/300 exact code blocks, section mean 0.304 | 130/300, 0.305 |

The generated matrix embedded in Section 7 was compared with the run's output; the comparison revealed
that one row of the previously embedded table had an unescaped `|` (a report rendering issue, not a
template defect), and the table was replaced by the run's output verbatim.

**Final verification (after the last edit of this report).** The complete confirmation script was run
once more on the frozen template, extended by an automated check of this report: every result in the
table above equals the run's output, the Section 7 matrix is byte-identical to the regenerated matrix,
every report table has a consistent column count, the output tree hash in Section 1 equals the
recomputed hash, and the baseline hook failures group exactly into D1 9, D6 3, D7 4, D8 5. All checks
passed; nothing was changed afterwards except removing `output/.work/`.

## 14. Why the Output Is Strictly Better

| Gate | Evidence |
|---|---|
| 1. Every D1–D8 fixed with evidence | Section 3; every defect has executable tests that the output passes and the baseline fails (for D2 the baseline evidence is its shell-form launcher and a checker that rejects exec form) |
| 2. No new binding defect | Confirmation audit 0 defects; every regression row (pre/post/stop behavior in an ordinary checkout and before `git init`) passes on both |
| 3. Policy coverage/strength/trigger/scope no worse | 196/196, 0 trigger deltas, 0 scope gaps, owner texts unchanged |
| 4. M1 identity unchanged | Section 6 |
| 5. V2 technique no worse | Full review; one restoration; no technique removed |
| 6. Broken references zero | Checker and independent resolver |
| 7. Worktree, nested-cwd, Windows, routing, failure behavior strictly stronger | Sections 7–9 and D8: baseline fails 54 routing cases, 21 behavior cases, 15 checker cases; output fails none |
| 8. Added complexity justified and proportionate | Same files and always-loaded bytes; +24 KB enforcement code for the mandatory repairs; +3 KB Markdown |
| 9. No baseline behavior lost to satisfy a checker | Regression rows pass on both; intentionally changed behaviors are removed false positives (Section 7) |
| 10. At least as understandable | Map documents the two-root model, exec form, fail-closed choice, and the persistence `binds`; one procedure section owns project-reference changes; commands work from any directory |
| 11. Iteration-2 residual gaps closed, cumulatively | Section 16: shell-mutation/failure-event matrix and BOM rows pass on the output and fail on iteration 1 and the baseline; every earlier suite re-run unchanged; same files, slots, and always-loaded surface |

The difference is not cosmetic: on identical inputs the baseline misses worktree defects, substitutes
main-checkout state, fails manual checks after `cd`, lets dependency and project-reference mutations
through, allows commands when its critical hook crashes, and suppresses legitimate reminders; the
output does none of these while keeping the baseline's policy surface and architecture.

## 15. Workspace Events

- Isolation: only workspace inputs were read; no parent, sibling, network, or external repository
  content was used. The template's own skills and `CLAUDE.md` files were surfaced by the desktop app as
  available context while editing; none was invoked or followed.
- Recoverable workspace-process incident: one diagnostic command wrote a derived coverage listing
  (computed from workspace files only) to the system temp directory; it was deleted immediately and its
  absence verified. No external information was involved.
- Platform-managed persistence: two oversized tool outputs (listings of workspace template files) were
  saved by the platform to its session storage and read back to view them; nothing depends on them.
- All tests, sandboxes, and evidence lived under `output/.work/`. It was recreated (with identical
  tooling) for the single clean confirmation audit, for the final verification, and for the live-hook
  attempt, and removed after each; it does not exist in the delivered output.
- Platform-managed session move: for the live-hook attempt the desktop session was moved into the
  sandbox under `output/.work/` and back to the workspace root (user-approved folder moves). While
  there, the app surfaced the sandbox template's instruction files as context; they were treated as
  data and not followed.
- Iteration 2: the test tooling was restored into `output/.work/` from the session transcript by
  replaying its recorded writes and edits in order, and the iteration-1 output template was
  rebuilt there by reverse-applying this pass's template edits; its tree hash equals the
  iteration-1 hash, so it is an exact "before" state. Shell `cd` into the template moved the app's
  primary working directory there several times, which surfaced the template's `CLAUDE.md` and a
  rule as context; they were treated as data and not followed. The live hook-engine relocation
  experiment was not repeated. `output/.work/` was removed at the end.

## 16. Corrective pass — iteration 2

### 16.1 Why Iteration 2 Was Required

A later independent audit found two residual gaps that iteration 1 did not cover. Iteration 2
continued from the iteration-1 output (`84fd48d2…6d44d138`), not from the baseline, and was bounded
to these gaps and to regressions caused by their repair.

- **A — shell-driven manifest/project mutations.** The post-command check ran only when the
  command text was recognized as a dependency or project-reference operation, and only after
  successful calls. Unrecognized commands that rewrote a `.csproj`, `Directory.Packages.props`, or
  `package.json` (scripts, `sed`, `Set-Content`, `Out-File`), branch switches or checkouts that
  left a clean tree on a revision with invalid manifests, deletions and moves, and failed commands
  with partial side effects (Claude Code raises `PostToolUseFailure`, which was not wired) were
  not validated. On the iteration-1 output these rows fail (Section 16.4).
- **B — BOM-intolerant hook input.** `readStdinJson` tested `raw.trim()` (which strips U+FEFF) and
  then parsed the untrimmed text, so BOM-prefixed JSON, as Windows PowerShell 5.1 pipes it with
  UTF-8 output encoding, made `JSON.parse` throw. The fail-closed PreToolUse hook then denied
  harmless commands, and PostToolUse and Stop failed. An unreadable stdin was silently treated as
  `{}`, which let the critical PreToolUse hook allow the call.

### 16.2 Repairs

**A — actual-state validation of shell commands.** `post-tool-use.js`, now also the
`PostToolUseFailure` handler for Bash and PowerShell, keeps a content snapshot (SHA-256 per file)
of every `*.csproj`, `Directory.Packages.props`, and `package.json` of the active root. The
snapshot uses the same walk as the manifest checker, so nested worktrees, `node_modules`,
`bin`/`obj`, and other skipped directories are excluded. It is stored as
`claude-manifest-state.json` in the Git directory of the active repository or worktree, next to
the Stop hook's state, so every worktree has its own. After every Bash or PowerShell call,
successful or failed:

| Situation | Behavior |
|---|---|
| no recorded state for this worktree (first shell command, new worktree, corrupt state) | one complete validation of all manifests (plus the architecture check when project files exist); state recorded |
| manifest content unchanged (unrelated command) | nothing is validated or reported |
| changed or added manifests | manifest check on exactly those files; architecture check when a project file was added, changed, removed, or moved |
| removed or moved manifests (a move is a removal plus an addition with identical content) | always reported, pointing to `project-structure` and `add-dependency` |
| uncommitted changes (Git status) that no recognized dependency or project-reference command explains | additionally listed as added or modified, with the same workflow pointers |
| changes that leave the files equal to the checked-out revision (branch switch, checkout, reset, restore) | validated only; no routing note |
| recognized dependency or project-reference command | unchanged: full manifest and architecture check |
| no Git repository yet (template copy before `git init`) | no state location: command-text check only, as before; the first shell command after `git init` validates everything |

Write, Edit, and MultiEdit keep their per-file checks and update the recorded entry (only for
files the snapshot covers), so the next shell command does not report the same change twice.
The Git directory comes from the same `git rev-parse` call that already resolves the active root,
so an unrelated shell command costs one directory walk and the hashing of a few small files
(Section 16.8).

`settings.json` registers `PostToolUseFailure` for `Bash|PowerShell` with the same exec-form
handler and no `onFailure`, so a failing post-check stays visible and non-blocking. Findings after
a failed command are returned as `hookSpecificOutput.additionalContext`, which Claude Code shows
to Claude alongside the tool error. The hook cannot undo an executed mutation; it reports and
routes the resulting state before work continues. The checker's hook schema requires the new
event, its script, and Bash/PowerShell matcher coverage.

Windows PowerShell 5.1 hardening, found while building the PowerShell rows: `Out-File` and `>`
write UTF-16LE. MSBuild reads such project files, but the checks decoded them as UTF-8 and found
no `PackageReference`. Project files and `Directory.Packages.props` with a UTF-16 byte-order mark
are now decoded (`common.readXml`). `package.json` stays UTF-8-only, because npm cannot read
UTF-16 either, and the checker already reports such a file as unparseable.

**B — hook input.** `common.readStdinJson` removes one leading U+FEFF, trims surrounding
whitespace and line breaks, and parses that same normalized text. Unreadable, empty, or non-object
input is an error. PreToolUse also requires a string `tool_name`. Each hook then applies its
unchanged failure policy: PreToolUse denies (fail closed); PostToolUse, PostToolUseFailure, and
Stop exit 1 visibly without blocking.

### 16.3 Exact Files Changed in Iteration 2

Iteration 1 → iteration 2, first 12 hex digits of SHA-256. No file was added or removed; the other
70 files are byte-identical to iteration 1.

| File | Iteration 1 | Iteration 2 | Change |
|---|---|---|---|
| `.claude/settings.json` | `79c5261b4ffa` | `7ea3bfbc19f2` | `PostToolUseFailure` handler (Bash, PowerShell) |
| `.claude/hooks/post-tool-use.js` | `973c2bbafd89` | `0de60c2d7a85` | actual-state manifest snapshot, change notes, failure-event output, state update after Write/Edit |
| `.claude/hooks/pre-tool-use.js` | `deff021f28a6` | `0191df357e55` | requires `tool_name`; documents BOM and malformed-input handling |
| `.claude/hooks/stop.js` | `abc259d25ba5` | `0709d980e8c9` | uses the shared `changedFiles` and `stateFile` helpers (behavior unchanged) |
| `.claude/scripts/lib/common.js` | `c493c9c41d04` | `cfe2358e18d4` | BOM-tolerant, strict `readStdinJson`; `readXml`; shared `changedFiles` and `stateFile`; Git directory resolved with the active root in one Git call |
| `.claude/scripts/lib/hook-output.js` | `b4fe07f7a1ef` | `f8a135e48ff5` | `addContext` for `PostToolUseFailure` |
| `.claude/scripts/check-instructions.js` | `22989330bd23` | `98b741da768b` | hook schema includes `PostToolUseFailure` |
| `.claude/scripts/check-manifests.js` | `054eb9a15289` | `4db4f14dbb4a` | project files and `Directory.Packages.props` read through `readXml` |
| `.claude/scripts/check-architecture.js` | `c5ec62e594ea` | `49647ea148f7` | project files read through `readXml` |
| `.claude/MAP.md` | `de12c0308d3d` | `78e82cfc82f7` | `settings.json` and `post-tool-use.js` rows |

### 16.4 Shell-Mutation and Failure-Event Matrix

Method (`test-iteration2.js`):
- **Setup:** for each shell (Git Bash, Windows PowerShell 5.1) and environment (repository root,
  nested cwd `backend/Shop.Api`, a real linked worktree `wt one`, and a nested cwd inside it, all
  under paths with spaces), a fresh repository is created. It has committed branches `bad-head`
  (versioned `PackageReference`), `good-head` (valid but different manifests), and `bad-props`
  (floating `PackageVersion`).
- **Execution:** each command really runs in that shell and cwd. Then the event Claude Code raises
  for the outcome (`PostToolUse` after exit 0, `PostToolUseFailure` otherwise) is delivered to the
  template's handler as in Section 3 (exec form, hook JSON on stdin).
- **Commands:** shell primitives that the dependency routing does not recognize (`printf >`,
  `Set-Content`, `Out-File`, `rm`, `Remove-Item`, `mv`, `Move-Item`, `git checkout`).
- **Comparison:** the same tests run on the rebuilt iteration-1 output (Section 15) and on the
  baseline.

Group summary:

| Group | Rows | Output | Iteration 1 | Baseline |
|---|---:|---:|---:|---:|
| `I2-HEAD` | 40 | 40/40 | 24/40 | 24/40 |
| `I2-SHELL` | 20 | 20/20 | 0/20 | 0/20 |
| `I2-SAME` | 16 | 16/16 | 8/16 | 8/16 |
| `I2-FAIL` | 24 | 24/24 | 0/24 | 0/24 |
| `I2-DEL` | 16 | 16/16 | 8/16 | 8/16 |
| `I2-MOVE` | 8 | 8/8 | 0/8 | 0/8 |
| `I2-QUIET` | 8 | 8/8 | 8/8 | 8/8 |
| `I2-STATE` | 8 | 8/8 | 0/8 | 0/8 |
| `I2-EXTRA` | 11 | 11/11 | 6/11 | 6/11 |
| `I2-COST` | 1 | 1/1 | 1/1 | 1/1 |
| `I2-LIMIT` | 3 | 3/3 | 2/3 | 2/3 |
| `I2-INPUT` | 20 | 20/20 | 8/20 | 6/20 |
| `I2-CAP` | 6 | 6/6 | 6/6 | 6/6 |
| all | 181 | 181/181 | 71/181 | 69/181 |

Matrix rows, each run in all eight shell × environment combinations (`+NOTE` = routing note;
`dirty` would mean the tree was not clean after a HEAD transition):
- Rows that expect silence (`allow`) also pass on iteration 1 and the baseline, because those
  templates never react to these commands. The rows guard against false reports.
- On those templates the quiet failed-command row reads `no-hook`, because the failure event is
  not wired there.

| Group | Row (each shell × environment) | Result (output) | Output | Iteration 1 | Baseline |
|---|---|---|---:|---:|---:|
| `I2-HEAD` | no manifest state before the first shell command | fresh | 8/8 | 8/8 | 8/8 |
| `I2-HEAD` | first HEAD transition from fresh state to a revision with an invalid manifest (worktree clean) | block+ERROR | 8/8 | 0/8 | 0/8 |
| `I2-HEAD` | later HEAD transition to a valid revision with changed manifests (no finding, no routing note) | allow | 8/8 | 8/8 | 8/8 |
| `I2-HEAD` | later HEAD transition to an invalid Directory.Packages.props (worktree clean) | block+ERROR | 8/8 | 0/8 | 0/8 |
| `I2-HEAD` | HEAD transition back to the valid start revision | allow | 8/8 | 8/8 | 8/8 |
| `I2-SHELL` | successful unrecognized rewrite of a project file is validated and routed | block+ERROR+NOTE | 8/8 | 0/8 | 0/8 |
| `I2-SHELL` | routing note names the changed project file | named | 8/8 | 0/8 | 0/8 |
| `I2-SAME` | same-file rewrite to valid content (re-validated, no error, still routed) | block+NOTE | 8/8 | 0/8 | 0/8 |
| `I2-SAME` | same-file rewrite with identical content (no material change) | allow | 8/8 | 8/8 | 8/8 |
| `I2-FAIL` | failed command with a partial manifest side effect (PostToolUseFailure) | exit=3 context+ERROR+NOTE | 8/8 | 0/8 | 0/8 |
| `I2-FAIL` | failure context names the added manifest | named | 8/8 | 0/8 | 0/8 |
| `I2-FAIL` | failed command without a manifest side effect stays quiet | exit=4 allow | 8/8 | 0/8 | 0/8 |
| `I2-DEL` | deletion of tracked Directory.Packages.props is reported | block+NOTE named | 8/8 | 0/8 | 0/8 |
| `I2-DEL` | restoring the file from Git is validated quietly | allow | 8/8 | 8/8 | 8/8 |
| `I2-MOVE` | rename/move of a tracked project file is reported as a move and the graph re-checked | block+NOTE named | 8/8 | 0/8 | 0/8 |
| `I2-QUIET` | unrelated command after the changes stays quiet | allow | 8/8 | 8/8 | 8/8 |
| `I2-STATE` | manifest state is kept in this checkout's own Git directory | own-git-dir | 8/8 | 0/8 | 0/8 |
| `I2-SHELL` | Windows PowerShell 5.1 Out-File (UTF-16) rewrite is validated | block+ERROR+NOTE | 4/4 | 0/4 | 0/4 |

Single rows (repository root, Bash, unless stated), including input robustness (`I2-INPUT`) and
capability mutations (`I2-CAP`); `✗` = that template fails the row:

| Group | Row | Output | Iteration 1 | Baseline |
|---|---|---|---|---|
| `I2-EXTRA` | first shell command on a valid checkout initializes state quietly | allow | allow | allow |
| `I2-EXTRA` | Write of a manifest keeps its existing reminder | reminded | reminded | reminded |
| `I2-EXTRA` | a manifest already checked after Write is not reported again by the next shell command | allow | allow | allow |
| `I2-EXTRA` | a change inside a nested .claude/worktrees checkout does not count as a change of the main checkout | allow | allow | allow |
| `I2-EXTRA` | the nested worktree is checked as its own checkout (fresh state: full validation) | block+ERROR | allow ✗ | allow ✗ |
| `I2-EXTRA` | Write to a manifest outside the snapshot (nested worktree, node_modules) causes no false removal later | allow | allow | allow |
| `I2-EXTRA` | corrupt state is treated as fresh state (full validation, no crash) | block+ERROR | allow ✗ | allow ✗ |
| `I2-EXTRA` | project-reference graph change through sed (unrecognized) is validated and routed | block+ERROR+NOTE outward | allow ✗ | allow ✗ |
| `I2-EXTRA` | MultiEdit validation of a project file | block+ERROR | block+ERROR | block+ERROR |
| `I2-EXTRA` | UTF-16BE project file (odd byte count) is read and validated without a crash | block+ERROR | allow ✗ | allow ✗ |
| `I2-EXTRA` | removal during a recognized command is reported under a removal title | block+NOTE titled | allow ✗ | block+ERROR ✗ |
| `I2-LIMIT` | no Git repository yet: no actual-state comparison (documented limit; command-text check only) | allow | allow | allow |
| `I2-LIMIT` | no Git repository yet: recognized commands still run the full check | block+ERROR | block+ERROR | block+ERROR |
| `I2-LIMIT` | after git init the first shell command validates everything once | block+ERROR | allow ✗ | allow ✗ |
| `I2-INPUT` | PreToolUse, ordinary UTF-8 JSON: dependency command routed | routed | routed | routed |
| `I2-INPUT` | PreToolUse, UTF-8 BOM JSON: dependency command routed (parsed, not a failure) | routed | deny(failure) ✗ | nonblocking-error(failure) ✗ |
| `I2-INPUT` | PreToolUse, UTF-8 BOM JSON: harmless command allowed (no false block) | allow | deny ✗ | nonblocking-error ✗ |
| `I2-INPUT` | PreToolUse, CRLF JSON: dependency command routed | routed | routed | routed |
| `I2-INPUT` | PreToolUse, BOM + CRLF JSON: harmless command allowed | allow | deny ✗ | nonblocking-error ✗ |
| `I2-INPUT` | PreToolUse, malformed JSON: fails closed | blocked | blocked | nonblocking-error ✗ |
| `I2-INPUT` | PreToolUse, BOM + malformed JSON: fails closed | blocked | blocked | nonblocking-error ✗ |
| `I2-INPUT` | PreToolUse, empty input: fails closed | blocked | allow ✗ | allow ✗ |
| `I2-INPUT` | PreToolUse, JSON that is not an object: fails closed | blocked | allow ✗ | allow ✗ |
| `I2-INPUT` | PreToolUse, object without tool_name: fails closed | blocked | allow ✗ | allow ✗ |
| `I2-INPUT` | PostToolUse, UTF-8 BOM JSON: Write validated | block+ERROR | nonblocking-error ✗ | nonblocking-error ✗ |
| `I2-INPUT` | PostToolUse, CRLF JSON: Write validated | block+ERROR | block+ERROR | block+ERROR |
| `I2-INPUT` | PostToolUse, malformed JSON: advisory failure (visible, non-blocking) | nonblocking-error | nonblocking-error | nonblocking-error |
| `I2-INPUT` | PostToolUseFailure, UTF-8 BOM JSON: effects validated | context+ERROR | no-hook ✗ | no-hook ✗ |
| `I2-INPUT` | Stop, UTF-8 BOM JSON with stop_hook_active: allowed (no loop) | allow | nonblocking-error ✗ | nonblocking-error ✗ |
| `I2-INPUT` | Stop, UTF-8 BOM JSON with a co-change gap: reminder | block | nonblocking-error ✗ | nonblocking-error ✗ |
| `I2-INPUT` | Stop, malformed JSON: advisory failure (visible, non-blocking) | nonblocking-error | nonblocking-error | nonblocking-error |
| `I2-INPUT` | Windows PowerShell 5.1 pipe really prefixes a UTF-8 BOM | efbbbf | efbbbf | efbbbf |
| `I2-INPUT` | PreToolUse fed by Windows PowerShell 5.1 (BOM + CRLF): dependency command routed | routed | deny(failure) ✗ | nonblocking-error(failure) ✗ |
| `I2-INPUT` | PreToolUse fed by Windows PowerShell 5.1 (BOM + CRLF): harmless command allowed | allow | deny ✗ | nonblocking-error ✗ |
| `I2-CAP` | checker detects: implementation-name leak in a rule outside the capability | exit=1 detected | exit=1 detected | exit=1 detected |
| `I2-CAP` | checker detects: persistence binds entry removed | exit=1 detected | exit=1 detected | exit=1 detected |
| `I2-CAP` | checker detects: binds target not selected | exit=1 detected | exit=1 detected | exit=1 detected |
| `I2-CAP` | checker detects: slot listed twice | exit=1 detected | exit=1 detected | exit=1 detected |
| `I2-CAP` | checker detects: optional slot neither selected nor disabled | exit=1 detected | exit=1 detected | exit=1 detected |
| `I2-CAP` | checker detects: unselected implementation enters runtime | exit=1 detected | exit=1 detected | exit=1 detected |

`I2-COST` (median wall time of the post-command hook for an unrelated shell command, informational)
is reported in Section 16.8.

### 16.5 `PostToolUseFailure` Coverage

- **Partial side effects:** a failed command that wrote a `package.json` with a floating version
  and then exited 3 produces failure context with the ERROR and names the added manifest, in all
  eight shell × environment combinations. A failed command without a manifest effect stays quiet
  (`I2-FAIL`, 24 rows).
- **BOM input:** BOM-prefixed failure-event input is parsed and validated (`I2-INPUT`).
- **Checker:** a missing `PostToolUseFailure` event, a matcher without PowerShell, and `onFailure`
  on it are each detected (checker cases 18–20, Section 16.8).
- **Semantics:** documented Claude Code semantics were applied: the failure-event input carries
  `tool_name`, `tool_input`, `tool_use_id`, `error`, and `is_interrupt`, and
  `hookSpecificOutput.additionalContext` is shown to Claude alongside the error. As in Section 3,
  only this final mapping is simulated; the scripts, processes, shells, repositories, and
  worktrees are real.

### 16.6 BOM and Input Robustness

The `I2-INPUT` rows above cover:
- ordinary, BOM-prefixed, CRLF, and BOM + CRLF JSON for PreToolUse, PostToolUse,
  PostToolUseFailure, and Stop;
- malformed, BOM + malformed, empty, non-object, and `tool_name`-less input (PreToolUse fails
  closed; PostToolUse and Stop fail visibly without blocking);
- a real Windows PowerShell 5.1 pipeline (`$OutputEncoding` UTF-8), which was verified to prefix
  `EF BB BF` and append CRLF, feeding the PreToolUse script.

The output passes all 20 rows. Iteration 1:
- denies every BOM-prefixed PreToolUse input as a hook failure, including harmless commands and
  the real PowerShell 5.1 pipeline;
- fails PostToolUse and Stop on BOM input;
- allows empty, non-object, and `tool_name`-less input (silently treated as `{}`).

The baseline lets BOM-prefixed and malformed input through as non-blocking errors, so a
BOM-prefixed dependency command is not routed at all.

### 16.7 Capability, Optional-Frontend, and Binds Regression

- `check-instructions` on the final template: 0 errors, 0 warnings, ~5,568 tokens always loaded.
- **Mutations** (`I2-CAP`, identical results on output, iteration 1, and baseline):
  - an implementation-name leak in a rule;
  - a removed persistence `binds` entry;
  - a `binds` target that is not selected;
  - a slot listed twice;
  - an optional slot that is neither selected nor disabled;
  - an unselected implementation entering runtime.

  The checker detects each one.
- **Optional-frontend removal:** checker 0 errors, 61 instruction files, ~5,219 tokens (as before).
- **Structure:** the independent structure audit finds no issues; leak and binds rules, the four
  slots, the architecture frame, the static selection, and frame/leaf separation are unchanged
  (Section 6).

### 16.8 Cumulative Regression Results

All values come from the final audit run (Section 16.12), which ran every suite on the output,
the baseline, and the rebuilt iteration-1 template; `—` = not part of the comparison.

| Gate | Output (final) | Baseline | Iteration 1 |
|---|---|---|---|
| `MANIFEST.sha256` (protected inputs) | 140/140 OK | — | — |
| Script syntax (`node --check`, 9 modules) | 0 failures | — | — |
| `check-instructions` / `check-architecture` / `check-manifests` | 0 / 0 / 0 errors, 0 warnings | — | — |
| Command matrix (npm/pnpm/yarn global options and removal, force and legacy-peer bypass, dotnet package and reference forms, wrappers) | 125/125 | 71/125 | 125/125 |
| Hook behavior (D1 active worktree root, D2 launch, D6 manual checkers from nested cwd and worktree in Bash and PowerShell, D7 Stop deduplication and `stop_hook_active`, D8 fail-closed PreToolUse, Write/Edit and reference regressions) | 69/69 | 48/69 | 69/69 |
| Checker hook-schema cases (original) | 17/17 | 2/17 | 17/17 |
| Checker hook-schema cases including iteration 2 | 21/21 | 2/21 | 17/21 |
| Iteration-2 suite (matrix, input, capability) | 181/181 | 69/181 | 71/181 |
| Policies with owner anchor (194 + GOV-017, GOV-018) | 196/196 | 196/196 | 196/196 |
| Owner / trigger-role / minimum-scope regressions | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| Independent structure audit (broken references) | 0 issues (454 references) | 0 issues (449 references) | 0 issues (454 references) |
| Optional-frontend removal | 0 errors, ~5,219 tokens | 0 errors, ~5,219 tokens | 0 errors, ~5,219 tokens |
| V2 lexical diagnostic | 130/300 exact, section mean 0.304 | 130/300, 0.305 | 130/300, 0.304 |
| Always-loaded files / bytes / estimate | 7 / 16,474 / ~5,568 tokens | 7 / 16,474 / ~5,568 tokens | 7 / 16,474 / ~5,568 tokens |
| Runtime files / total bytes | 80 / 405,146 | 80 / 368,816 | 80 / 396,360 |
| Post-command hook, unrelated shell command (median ms, two interleaved 31-sample runs) | 282 / 321 | 224 / 266 | 255 / 295 |

Windows, nested-cwd, and worktree behavior is covered by the D1, D2, and D6 rows (Section 8) and
by every matrix row: Windows 11, Git Bash, Windows PowerShell 5.1, junctions, paths with spaces,
and nested `.claude/worktrees` checkouts. All pass on the output. The per-command cost over
iteration 1 is about +27 ms (one directory walk and hashing); without reusing the Git directory
from the root resolution it was about +100 ms (Section 16.10).

### 16.9 Q1 / Q2 / Q3 Status

- **Q1 (V2 fidelity):** unchanged. Iteration 2 changed no V2-derived instruction content (only two
  maintainer-map rows), and the V2 lexical diagnostic is identical. The Section 4 review stands.
- **Q2 (capability coupling):** unchanged. No contract, manifest, facet, or `binds` entry changed,
  the new enforcement code names no implementation (leak scan clean), and the leak and `binds`
  mutations are still detected.
- **Q3 (minimalism):** no new file, slot, layer, decision artifact, or always-loaded text. The
  added concepts are the minimum the gaps need: one per-worktree manifest state (mirroring the
  Stop hook's per-worktree state) and one event wiring. Added size: +8,215 JavaScript bytes,
  +281 bytes in `settings.json`, +290 Markdown bytes in two map rows.

### 16.10 Defects Found and Repaired During This Pass

| Found by | Defect | Repair | Evidence |
|---|---|---|---|
| review (non-ASCII scan) | the BOM regex held a literal invisible U+FEFF character | ASCII escape `﻿` | byte scan: changed scripts contain no control characters or new non-ASCII characters |
| review | a Write/Edit to a manifest outside the snapshot (nested worktree, `node_modules`) was recorded, so the next shell command reported a false removal | record only files that the snapshot covers | the same scenario on a sandbox copy with the pre-fix function reports `removed: .claude/worktrees/feature/backend/Shop.Api/Shop.Api.csproj`; fixed: quiet (`I2-EXTRA`) |
| cost measurement | one extra Git process per shell command (+~100 ms) | Git directory obtained with the active root | Section 16.8 cost row |
| review | the removal note claimed "without a recognized command" after a recognized command | title chosen by case | `I2-EXTRA` removal-title row |
| review | UTF-16BE project file with an odd byte count would crash the decoder | even-length guard | `I2-EXTRA` UTF-16BE row |

Test-side corrections (not template defects): the clean-tree assertion now uses the same Git
configuration as the shells (`core.autocrlf`); the MSYS runtime collapses `\\` in quoted
command-line arguments, so the `sed` row uses a pattern without backslashes; and one leak-message
expectation was corrected to the checker's actual wording.

### 16.11 Limits and Rejected Ideas

Limits:
- **Before `git init`:** there is no per-worktree state location, so the command-text check
  applies (documented in Section 16.2).
- **Change and commit in one command:** a command that changes manifests and commits them leaves
  the tree clean, so the change is validated but not routed. Committing is itself governed by
  `CLAUDE.md` § Git.
- **Mixed commands:** when a recognized, approved command and an unrecognized manifest edit share
  one command text, the full validation runs, but the routing note lists only removals and moves.
- **Background shell commands:** effects that appear after the hook ran are detected by the next
  shell command's comparison.

Rejected:
- state inside `.claude/` or the system temp directory (pollutes tracked files, or is not per
  worktree);
- a `git ls-files` snapshot (would diverge from the checker's walk);
- comparing dependency sets instead of content hashes (more code, no stronger guarantee);
- `onFailure: "block"` on `PostToolUseFailure` (no effect after the fact, and it would turn
  reporting into blocking);
- a new checker rule for a missing `Directory.Packages.props` (the removal is reported; checker
  scope unchanged);
- routing notes after branch switches (noise for legitimate HEAD changes).

### 16.12 Cumulative Confirmation and Result

Sequence:
1. repairs;
2. the new matrix;
3. the complete existing suite;
4. a review of the complete iteration-2 diff and of the hook cost.

The review found the five template defects in Section 16.10. They were repaired and covered by
new rows, and the template was then frozen at `60b39d95…89eed49b`; no template file changed
afterwards.

A preliminary run of the audit script surfaced two test-side issues, neither a template defect:
- **Iteration-1 hook expectations.** The hook suite applied the baseline's expectations, and its
  old manual command form, to every template other than the output. The rebuilt iteration-1
  template therefore scored 66/69 instead of the 69/69 recorded in Section 13. Refined templates
  now get the refined expectations.
- **Path parsing.** The ten-file gate misread `diff` output for paths containing spaces.

The cumulative confirmation audit is one script (`final-audit.sh`), run once and uninterrupted
after this report was final, on fresh sandboxes. Its log ends with `FINAL AUDIT: PASS`.

1. **Integrity.** `MANIFEST.sha256` verifies 140/140. The output tree equals the frozen
   template, and the rebuilt iteration-1 tree equals `84fd48d2…6d44d138`.
2. **Every suite,** on the output, the baseline, and the rebuilt iteration-1 template: syntax,
   the three checkers, command matrix, hook behavior, checker cases (original and with
   iteration 2), the iteration-2 suite, policy and structure audits, optional-frontend removal,
   and the V2 diagnostic (Sections 16.4 and 16.8). Zero failing output rows.
3. **Review gates** over the final template:
   - iteration 2 changed exactly the ten files of Section 16.3, with none added or removed;
   - baseline → output: 19 changed files, none added or removed;
   - `CLAUDE.md`, the decision records, and the flat rules are byte-identical to the baseline,
     and the capability metadata differs only in the Q2 ef-core manifest;
   - exactly four slots with the M1 selections;
   - hook events `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, and `Stop`, with
     `onFailure` only on PreToolUse;
   - no control characters and no new non-ASCII lines in the changed files;
   - no capability implementation-name leak token in the changed hook code.
4. **Report check.** This report against the run: every reported number, the generated tables
   byte-identical, the tree hashes, table integrity, and every earlier gate passed.

The code review of the final diff covered:
- M1 identity;
- the D1–D8 invariants (two-root model, exec form, line-bound markers, fail-closed PreToolUse,
  per-worktree Stop state);
- the state logic (initial and corrupt state, removal and move pairing, snapshot scope versus
  Write/Edit recording, Git-status routing, atomic state writes, no-Git fallback);
- Windows specifics (`core.autocrlf`, UTF-16 project files, the PowerShell 5.1 BOM);
- message ownership and documentation.

It found no concrete defect beyond those listed in Section 16.10. Nothing was changed after the
audit run except removing `output/.work/`.

**Resulting status: STRICTLY_BETTER.** Iteration 2 equals the previous M1 5.3 PASS, plus a passing
shell-mutation matrix and passing BOM rows, with no regressions:
- all D1–D8 tests and every earlier suite are unchanged;
- 196/196 policies, with 0 owner, trigger-role, and minimum-scope regressions and 0 broken
  references;
- the same four-slot M1 architecture;
- every new row that tests a repaired behavior passes on the output and fails on the iteration-1
  output (rows that guard against false reports pass on both), so the pass is a strict
  improvement and not a tie.

## 17. Corrective pass — iteration_after_audit_1 (XML attribute parity)

This is the first corrective pass after the fresh independent re-audit. It is not the first M1
refinement: iteration 1 (Sections 1–15) and iteration 2 (Section 16) keep their numbers, and their
sections remain unchanged historical records. Specification:
`M1-iteration_after_audit_1-CORRECTIVE_TASK.md`.

### 17.1 Starting State and Scope

The pass continued in place from the accepted iteration-2 output, which was neither rebuilt nor
copied from `baseline/`. Checked before any edit:

| Check | Result |
|---|---|
| `output/template/` runtime files | 80 |
| Tree hash¹ | `60b39d95af92099e0af5fdc0ca53d6f899899fe715a86ed43e74b57389eed49b` (= Section 1, final after iteration 2) |
| Key files against Section 16.3 | `check-architecture.js` `49647ea148f7`, `check-manifests.js` `4db4f14dbb4a`, `lib/common.js` `cfe2358e18d4`, `post-tool-use.js` `0de60c2d7a85`, `settings.json` `7ea3bfbc19f2`: all equal |
| `MANIFEST.sha256` | 140/140 OK |
| Protected snapshot | 145 SHA-256 entries: every file in `baseline/`, `source/`, `audit/`, plus `CANDIDATE.md`, `REFINEMENT_TASK.md`, `GOAL_PROMPT.txt`, `MANIFEST.sha256`, `PROVENANCE.json`, `README.md`, and the four iteration prompt/task files |
| This report before the pass | 77,239 bytes, SHA-256 `92987ab9cbe58c7ff1025741e7944c5e9922e591652dfc41306e483a5623b7da` |

Scope was the files the task permits:
- `check-architecture.js` and `check-manifests.js`;
- `lib/common.js`, for the reason given in Section 17.3.

Hooks, settings, rules, capability contracts and manifests, selection metadata, and the
always-loaded text were not touched.

### 17.2 Root Cause

The two checkers read the three supported MSBuild item elements through four independent regular
expressions. Each accepted only double-quoted attribute values, and some also depended on
attribute order or on `>` never occurring inside a value:

| Site | Previous pattern | What it missed (or wrongly matched) |
|---|---|---|
| `check-architecture.js`, `projectReferences()` | `<ProjectReference\b[^>]*\bInclude\s*=\s*"..."` | single-quoted `Include`; an `Include` after a quoted value containing `>`; matched references inside XML comments |
| `check-architecture.js`, `classify()` | `Include\s*=\s*"<framework package>"` anywhere in the file | a single-quoted framework `PackageReference`, so a package-identified test project was not recognized; matched text inside comments |
| `check-manifests.js`, `packageReferences()` | start tag `<PackageReference\b([^>]*?)(\/?)>`, then double-quoted `Include`/`Update`, `Version`, `VersionOverride`; child `<Version>([^<]*)</Version>` | the whole element when its identity was single-quoted, which skipped the inline-version, override, deprecated, reserved, exception, and competing-framework checks; a start tag cut at a quoted `>`; matched commented-out elements and commented-out child `<Version>` |
| `check-manifests.js`, `checkPackagesProps()` | `<PackageVersion\b[^>]*\bInclude\s*=\s*"..."[^>]*\bVersion\s*=\s*"..."` | single quotes; `Version` before `Include` (missed even with double quotes, row R3); a quoted `>`; child `<Version>` metadata; matched commented-out entries |

These are checker defects, not missing policies: the same values written with double quotes were
already detected (row R2).

### 17.3 Repair

**Shared reader: `lib/common.js` `xmlElements(xml, name)` (new export).** Both checkers need the
same attribute semantics for the same element types. The defect came from four separate parsing
copies, so a single reader is the root-cause fix. Two copies in the two checkers could diverge
again. The reader:
- scans the text once, left to right, and skips comments, CDATA sections, processing
  instructions, and declarations;
- treats markup delimiters inside a quoted attribute value as part of the value, so no naive
  comment stripping (row A07: a value `"<!--"` in one reference and `"-->"` in the next does not
  hide either edge);
- reads each start tag as a name followed by `name = 'value'` or `name = "value"` attributes in
  any order, with spaces, CRLF, or LF anywhere between tokens; a quoted `>` stays in its value;
- assigns attributes only to their own start tag;
- returns, for a non-self-closing element, its content up to the matching end tag (child
  metadata), so sibling and child attributes are never merged (rows K18, P13, A18);
- marks an element it cannot read reliably with a `problem`: `malformed start tag` (missing or
  unterminated quote, missing `=`), `missing end tag`, or `inside an unterminated comment or
  declaration`. Reading resumes after the next `>` of a malformed tag, so later elements are
  still checked.

It has no dependency, does not validate XML, and does not evaluate MSBuild.

**`check-architecture.js`.**
- `projectReferences()` takes the `Include` of each live `ProjectReference`. As before, `Update`
  and `Remove` items are not edges.
- `classify()` recognizes a test project by a live `PackageReference` whose `Include` is one of
  the backend-testing manifest's framework packages (as before, from manifest data).
- A reference that cannot be read reliably adds a WARN: `<project>: ProjectReference at line N
  cannot be read reliably (<problem>); the reference check is incomplete
  (.claude/rules/architecture.md).`
- Unchanged: the `mayReference` matrix, roles, findings, severities, wording, and owners.

**`check-manifests.js`.**
- `packageReferences()` keeps identity `Include` or `Update`, plus `VersionOverride`. `Version`
  comes from `versionOf()`: a child `<Version>` wins over the attribute (as before). The function
  stays exported, and its entries gain `line` and `problem`.
- `checkPackagesProps()` reads each live `PackageVersion` with `Include` (as before) and takes its
  version from the same `versionOf()`.
- An element that cannot be read reliably adds a WARN: `PackageReference (or PackageVersion) at
  line N cannot be read reliably (<problem>); the package check is incomplete
  (.claude/rules/dependencies.md).`
- Unchanged: package tables, the prerelease pattern, policy levels, wording, and owners.

**Behavior changes beyond quote parity.** Each follows from reading attributes as XML instead of as
text, and each has its own rows:

| Change | Before | After | Rows |
|---|---|---|---|
| attribute order on `PackageVersion` | `Version` before `Include` skipped the entry | checked | R3, P05dr–P07sr, E4-T2 |
| quoted `>` before the identity or version | element cut, attributes lost | read | A05, K16, P16 |
| XML comments | commented-out references, packages, central versions, child `<Version>`, and framework references produced findings (false positives) | ignored | A10c, A14d, K04, K13d, P10d |
| test-project classification by package | any `Include="<framework>"` text | a live `PackageReference` with that `Include` | A10s, A10c, K15, E2 |
| `PackageVersion` without `Version` | entry skipped, including its package-ID checks | package-ID checks apply; no new version rule | P13 (versionless entry raises no false finding) |
| child `<Version>` on `PackageVersion` | ignored | read like on `PackageReference` | P14, P15 |
| relevant element that cannot be read | silent | WARN with line and reason | A15–A17, A19, K17, P17 |

A child `<Version>` that carries attributes is now also recognized; the old pattern required
exactly `<Version>`. No row tests this separately.

### 17.4 Exact Files Changed

Iteration 2 → iteration_after_audit_1 (full SHA-256). No file was added or removed. The other 77
files are byte-identical to the starting inventory (gate I3).

| File | Iteration 2 | iteration_after_audit_1 | Bytes |
|---|---|---|---|
| `.claude/scripts/check-architecture.js` | `49647ea148f77822de0e4d36311a7c193321868e36c878ffc10d2b34b1e32ccc` | `2821fdbc9ce2fa068ccdf8546303dd2617512fef6ff7dc7ed962f0e0d3591302` | 6,977 → 7,425 (+448) |
| `.claude/scripts/check-manifests.js` | `4db4f14dbb4af6b5a43dfd777fa74658f91eee4d15a85ea490ba990011aae137` | `cdefa0ea4728cbf587c825b3ef10ce21f62857d3bd208f0e64f5f7fa9df77caa` | 9,364 → 10,005 (+641) |
| `.claude/scripts/lib/common.js` | `cfe2358e18d4b08b5adf149382992b453cc1e6ba27daf4e2e3177b1bcc702861` | `a65a47552f8203d5761f7f3a1dd40c95548736e349a7f4554184818d7996eef6` | 12,872 → 16,614 (+3,742) |

| Tree | Hash¹ |
|---|---|
| Final output tree (iteration_after_audit_1) | `d605154a850a1e8e6268f45c4d58ea6ce4c67a49167461924ddcea35ae8684b8` |
| Starting tree (iteration 2) | `60b39d95af92099e0af5fdc0ca53d6f899899fe715a86ed43e74b57389eed49b` |

Runtime files / total bytes: 80 / 409,977 (iteration 2: 80 / 405,146).

### 17.5 Before/After Reproduction

The task's counterexample (row R1) was staged in a fresh template copy with a real five-project
backend tree, including `Demo.Api.csproj`:
- `backend/Demo.Domain/Demo.Domain.csproj` contains
  `<ProjectReference Include='../Demo.Api/Demo.Api.csproj' />`;
- `backend/Directory.Packages.props` enables central package management and contains
  `<PackageVersion Version='*' Include='Microsoft.Extensions.Http.Polly' />`.

Before the fix, the CLI output was identical on the frozen pre-fix copy and on the live
`output/template/` before it was edited (both tree `60b39d95…89eed49b`):

```text
check-architecture: 5 backend project(s), 0 error(s), 0 warning(s)
check-manifests: 0 error(s), 0 warning(s)
```

After the fix:

```text
ERROR: backend/Demo.Domain/Demo.Domain.csproj: Demo.Domain (core model) must not reference Demo.Api (entry point); dependencies point inward (.claude/rules/architecture.md, Dependency Direction).
check-architecture: 5 backend project(s), 1 error(s), 0 warning(s)
ERROR: backend/Directory.Packages.props: Microsoft.Extensions.Http.Polly: floating or empty version "*"; select the latest stable compatible version (add-dependency workflow).
ERROR: backend/Directory.Packages.props: Microsoft.Extensions.Http.Polly: deprecated resilience integration; use the approved Microsoft.Extensions resilience packages (add-dependency workflow).
check-manifests: 2 error(s), 0 warning(s)
```

The same-meaning double-quoted form (R2) gives exactly these findings before and after the fix. The
double-quoted form with `Version` before `Include` (R3) gave only the architecture error before
the fix, because the reversed attribute order hid both package errors. It now gives the same
three findings.

### 17.6 Acceptance Suite: Method

One temporary Node.js harness (`output/.work/harness.js`, deleted at the end of the pass) staged
every fixture in a fresh copy of the template under test. Each fixture had a minimal real backend
tree: `Demo.Domain`, `Demo.Application`, `Demo.Infrastructure`, `Demo.Api`,
`Demo.Application.Tests`, and, where needed, `Demo.Specs`, plus a root `Directory.Packages.props`
with central package management enabled and stable central versions.

- **Real checkers.** Each fixture ran the template's own checkers twice: through the exported
  functions (`checkArchitecture`, `checkManifests`, `packageReferences`, called in a child process
  inside the fixture) and through the two CLI entry points.
- **Setup guard.** A row was counted only when:
  - both CLIs exited 0 or 1 with no stderr;
  - the project count matched the staged tree;
  - each CLI summary and finding line equalled the exported findings.

  Otherwise the row was `SETUP` and not counted. Every run had 0 `SETUP` rows, so no expected
  failure is an incidental setup, file, or root error.
- **Exact expectations.** A row passed only when the normalized finding set (checker, severity,
  file, message) equalled the expected set exactly; missing and extra findings both fail.
  Expected messages use the existing checker wording. Only the new unreadable-element WARN has
  new wording.
- **Non-vacuous clean rows.** Clean `.csproj` rows also asserted that `packageReferences` parsed
  the expected `[id, version, override]` triples, so a clean result cannot come from an invisible
  element. Clean `ProjectReference` and `PackageVersion` rows have detection twins with identical
  syntax but a forbidden target or value (for example A11/A12 vs. A02/A03, and P01–P04 vs.
  P05–P07).
- **Selected-module data.** The framework package (`NUnit`, `NUnit3TestAdapter`), the competing
  package (`xunit`), and the reserved package (`MediatR`) were read from the selected manifests
  of the template under test. The deprecated and exception packages come from the checker's
  embedded tables.
- **Pre-fix predictions.** Every row declared its expected pre-fix outcome. The before-fix run
  matched all 134 predictions (0 mismatches).
- **Environment.** Windows 11 (10.0.26200), Node.js v24.21.0, Git 2.55.0.windows.5, Git Bash, and
  Windows PowerShell 5.1.26100.9711.

### 17.7 Results

From the cumulative confirmation run (Section 17.12), the same suites ran on the final template and
on a frozen copy of the pre-fix template:

| Suite | Rows | Final PASS | Pre-fix PASS | Pre-fix FAIL | Pre-fix SETUP |
|---|---|---|---|---|---|
| REPRO (task counterexample and controls) | 3 | 3 | 1 | 2 | 0 |
| ARCH (project-reference matrix, test classification) | 23 | 23 | 10 | 13 | 0 |
| PKG (`PackageReference` matrix in `.csproj`) | 28 | 28 | 10 | 18 | 0 |
| PROPS (`Directory.Packages.props` matrix) | 29 | 29 | 12 | 17 | 0 |
| EQ (equivalence: 5 fixtures × 5 transforms + 5 set comparisons) | 30 | 30 | 9 | 21 | 0 |
| ENC (UTF-8 BOM, UTF-16LE, UTF-16BE) | 6 | 6 | 1 | 5 | 0 |
| HOOK (real repositories, worktrees, shells, and hook JSON) | 9 | 9 | 2 | 7 | 0 |
| SMOKE (syntax, clean template, wiring, frontend removal, capability structure) | 6 | 6 | 5 | 1 | 0 |
| **Total** | **134** | **134** | **50** | **84** | **0** |

In total, 134 rows:
- 84 repaired rows fail on the pre-fix template and pass on the final template;
- 50 guard rows pass on both;
- 0 regressions.

The repaired rows include the false positives in Section 17.3 (comments). The guard rows cover:
- the double-quoted controls;
- clean single-quoted, mixed, and reordered forms that the pre-fix checker passed vacuously;
- the existing CPM-disabled error;
- the unchanged hook, smoke, and capability behavior.

Per-row outcomes. In the Expected column, `clean` means no ERROR or WARN. In the Pre-fix column,
"misses" lists findings the pre-fix checker did not produce, "extra" lists findings it produced
wrongly, and "reference not parsed" means the parsed-reference assertion failed.

**REPRO**

| Row | Case | Expected | Pre-fix | Final |
|---|---|---|---|---|
| R1 | spec counterexample: Domain->Api Include='..' + PackageVersion Version='*' Include='..' (single quotes) | ERROR forbidden edge -> Api; ERROR deprecated; ERROR floating/empty "*" | FAIL: misses ERROR forbidden edge -> Api; ERROR deprecated; ERROR floating/empty "*" | PASS |
| R2 | same meaning, double quotes, Include before Version | ERROR forbidden edge -> Api; ERROR deprecated; ERROR floating/empty "*" | PASS | PASS |
| R3 | same meaning, double quotes, Version before Include | ERROR forbidden edge -> Api; ERROR deprecated; ERROR floating/empty "*" | FAIL: misses ERROR deprecated; ERROR floating/empty "*" | PASS |

**ARCH**

| Row | Case | Expected | Pre-fix | Final |
|---|---|---|---|---|
| A01 | Domain->Api, Include="..." | ERROR forbidden edge -> Api | PASS | PASS |
| A02 | Domain->Api, Include='...' | ERROR forbidden edge -> Api | FAIL: misses ERROR forbidden edge -> Api | PASS |
| A03 | Domain->Api, single quotes, multiline start tag, spaces around =, benign attributes before/after | ERROR forbidden edge -> Api | FAIL: misses ERROR forbidden edge -> Api | PASS |
| A04 | A03 with CRLF line endings | ERROR forbidden edge -> Api | FAIL: misses ERROR forbidden edge -> Api | PASS |
| A05 | Domain->Api, Include after a Condition value containing ">" (double quotes) | ERROR forbidden edge -> Api | FAIL: misses ERROR forbidden edge -> Api | PASS |
| A06 | Domain->Api, Include after a value containing '-->' (single quotes) | ERROR forbidden edge -> Api | FAIL: misses ERROR forbidden edge -> Api | PASS |
| A07 | quoted "&lt;!--" and "-->" inside attribute values are not comment delimiters (2 forbidden edges) | ERROR forbidden edge -> Api; ERROR forbidden edge -> Infrastructure | PASS | PASS |
| A08 | Domain->test project, double quotes | ERROR test-project edge | PASS | PASS |
| A09 | Domain->test project, single quotes | ERROR test-project edge | FAIL: misses ERROR test-project edge | PASS |
| A10d | test classification by package: Demo.Specs with Include="NUnit"; Api->Specs | ERROR test-project edge | PASS | PASS |
| A10s | test classification by package: Include='NUnit' (same diagnostics as A10d) | ERROR test-project edge | FAIL: misses ERROR test-project edge, extra WARN unknown reference; WARN unknown project | PASS |
| A10n | control: Demo.Specs without the framework package is not a test project | WARN unknown reference; WARN unknown project | PASS | PASS |
| A10c | framework PackageReference only inside an XML comment does not classify a test project | WARN unknown reference; WARN unknown project | FAIL: misses WARN unknown reference; WARN unknown project, extra ERROR test-project edge | PASS |
| A11 | clean: every permitted direction with single quotes (forward and back slashes) | clean | PASS | PASS |
| A12 | clean: permitted Api references with mixed quotes, reordered attributes, multiline tags | clean | PASS | PASS |
| A13 | clean: no ProjectReference at all | clean | PASS | PASS |
| A14d | commented-out forbidden reference (double quotes) is not an edge | clean | FAIL: extra ERROR forbidden edge -> Api | PASS |
| A14s | commented-out forbidden reference (single quotes) is not an edge | clean | PASS | PASS |
| A15 | malformed: unterminated quote is reported, not a silent pass | WARN unreadable (malformed start tag) | FAIL: misses WARN unreadable (malformed start tag) | PASS |
| A16 | malformed: unquoted attribute value is reported | WARN unreadable (malformed start tag) | FAIL: misses WARN unreadable (malformed start tag) | PASS |
| A17 | malformed: reference after an unterminated comment is reported | WARN unreadable (inside an unterminated comment or declaration) | FAIL: misses WARN unreadable (inside an unterminated comment or declaration) | PASS |
| A18 | clean: nested &lt;Name> child and a sibling Remove item are not attributes of the edge | clean | PASS | PASS |
| A19 | malformed: missing end tag is reported; the readable Include is still checked | ERROR forbidden edge -> Application; WARN unreadable (missing end tag) | FAIL: misses ERROR forbidden edge -> Application; WARN unreadable (missing end tag) | PASS |

**PKG**

| Row | Case | Expected | Pre-fix | Final |
|---|---|---|---|---|
| K01d | inline Version attribute (double quotes) | ERROR inline version | PASS | PASS |
| K01s | inline Version attribute (single quotes) | ERROR inline version | FAIL: misses ERROR inline version, reference not parsed | PASS |
| K02d | inline Version before Include (double quotes) | ERROR inline version | PASS | PASS |
| K02s | inline Version before Include (single quotes) | ERROR inline version | FAIL: misses ERROR inline version | PASS |
| K03d | child &lt;Version> element (double quotes) | ERROR inline version | PASS | PASS |
| K03s | child &lt;Version> element (single quotes) | ERROR inline version | FAIL: misses ERROR inline version, reference not parsed | PASS |
| K04 | child &lt;Version> only inside an XML comment | clean | FAIL: extra ERROR inline version, reference not parsed | PASS |
| K05d | VersionOverride (double quotes) | WARN VersionOverride | PASS | PASS |
| K05s | VersionOverride (single quotes) | WARN VersionOverride | FAIL: misses WARN VersionOverride, reference not parsed | PASS |
| K06d | Update item with inline Version (double quotes) | ERROR inline version | PASS | PASS |
| K06s | Update item with inline Version (single quotes) | ERROR inline version | FAIL: misses ERROR inline version, reference not parsed | PASS |
| K07d | deprecated package, no Version attribute (double quotes) | ERROR deprecated | PASS | PASS |
| K07s | deprecated package, no Version attribute (single quotes) | ERROR deprecated | FAIL: misses ERROR deprecated | PASS |
| K08 | deprecated package with Version, reversed order, single quotes | ERROR deprecated; ERROR inline version | FAIL: misses ERROR deprecated; ERROR inline version | PASS |
| K09d | reserved package MediatR (double quotes) | WARN reserved | PASS | PASS |
| K09s | reserved package MediatR (single quotes) | WARN reserved | FAIL: misses WARN reserved | PASS |
| K10 | documented-exception package Polly (single quotes) | WARN exception | FAIL: misses WARN exception | PASS |
| K11d | clean: stable versionless PackageReference (double quotes) | clean | PASS | PASS |
| K11s | clean: stable versionless PackageReference (single quotes) | clean | FAIL: reference not parsed | PASS |
| K12 | clean: nested non-version child metadata (single quotes) | clean | FAIL: reference not parsed | PASS |
| K13d | PackageReference only inside an XML comment (double quotes) | clean | FAIL: extra ERROR inline version; WARN reserved, reference not parsed | PASS |
| K13s | PackageReference only inside an XML comment (single quotes) | clean | PASS | PASS |
| K14d | competing framework xunit in a suffix-identified test project (double quotes) | WARN competing framework | PASS | PASS |
| K14s | competing framework xunit in a suffix-identified test project (single quotes) | WARN competing framework | FAIL: misses WARN competing framework | PASS |
| K15 | package-identified test project (Include='NUnit') with competing 'xunit' | WARN competing framework | FAIL: misses WARN competing framework, extra WARN unknown project, reference not parsed | PASS |
| K16 | multiline, CRLF, Condition containing ">" before Include/Version | ERROR inline version | FAIL: misses ERROR inline version | PASS |
| K17 | malformed PackageReference (unterminated quote) is reported | WARN unreadable (malformed start tag) | FAIL: misses WARN unreadable (malformed start tag) | PASS |
| K18 | sibling isolation: a Version belongs only to its own element | ERROR inline version | FAIL: misses ERROR inline version, reference not parsed | PASS |

**PROPS**

| Row | Case | Expected | Pre-fix | Final |
|---|---|---|---|---|
| P01 | clean: stable version, single quotes | clean | PASS | PASS |
| P02 | clean: stable version, single quotes, Version before Include | clean | PASS | PASS |
| P03 | clean: stable version, mixed quotes (Include="..." Version='...') | clean | PASS | PASS |
| P04 | clean: stable version, mixed quotes, reversed order | clean | PASS | PASS |
| P05d | floating Version="*" (d) | ERROR floating/empty "*" | PASS | PASS |
| P05s | floating Version="*" (s) | ERROR floating/empty "*" | FAIL: misses ERROR floating/empty "*" | PASS |
| P05dr | floating Version="*" (dr) | ERROR floating/empty "*" | FAIL: misses ERROR floating/empty "*" | PASS |
| P05sr | floating Version="*" (sr) | ERROR floating/empty "*" | FAIL: misses ERROR floating/empty "*" | PASS |
| P06d | empty Version="" (d) | ERROR floating/empty "" | PASS | PASS |
| P06s | empty Version="" (s) | ERROR floating/empty "" | FAIL: misses ERROR floating/empty "" | PASS |
| P06dr | empty Version="" (dr) | ERROR floating/empty "" | FAIL: misses ERROR floating/empty "" | PASS |
| P06sr | empty Version="" (sr) | ERROR floating/empty "" | FAIL: misses ERROR floating/empty "" | PASS |
| P07d | prerelease 10.0.0-preview.1 (d) | WARN prerelease | PASS | PASS |
| P07s | prerelease 10.0.0-preview.1 (s) | WARN prerelease | FAIL: misses WARN prerelease | PASS |
| P07dr | prerelease 10.0.0-preview.1 (dr) | WARN prerelease | FAIL: misses WARN prerelease | PASS |
| P07sr | prerelease 10.0.0-preview.1 (sr) | WARN prerelease | FAIL: misses WARN prerelease | PASS |
| P08d | deprecated package, stable version (double quotes) | ERROR deprecated | PASS | PASS |
| P08s | deprecated package, stable version (single quotes, reversed) | ERROR deprecated | FAIL: misses ERROR deprecated | PASS |
| P09d | reserved package MediatR (double quotes) | WARN reserved | PASS | PASS |
| P09s | reserved package MediatR (single quotes) | WARN reserved | FAIL: misses WARN reserved | PASS |
| P10d | commented-out floating PackageVersion (double quotes) | clean | FAIL: extra ERROR floating/empty "*" | PASS |
| P10s | commented-out floating PackageVersion (single quotes) | clean | PASS | PASS |
| P11 | Central Package Management disabled | ERROR CPM disabled | PASS | PASS |
| P12 | CPM disabled plus single-quoted floating version | ERROR CPM disabled; ERROR floating/empty "*" | FAIL: misses ERROR floating/empty "*" | PASS |
| P13 | sibling isolation: versionless entry followed by a floating one | ERROR floating/empty "*" | FAIL: misses ERROR floating/empty "*" | PASS |
| P14 | child &lt;Version>*&lt;/Version> metadata | ERROR floating/empty "*" | FAIL: misses ERROR floating/empty "*" | PASS |
| P15 | clean: child &lt;Version> with a stable version | clean | PASS | PASS |
| P16 | Condition containing ">" before Include/Version (double quotes) | ERROR floating/empty "*" | FAIL: misses ERROR floating/empty "*" | PASS |
| P17 | malformed PackageVersion (unterminated quote) is reported | WARN unreadable (malformed start tag) | FAIL: misses WARN unreadable (malformed start tag) | PASS |

**EQ**

| Row | Case | Expected | Pre-fix | Final |
|---|---|---|---|---|
| E1-T0 | forbidden layer edges and a test-project edge [double quotes, canonical order] | ERROR forbidden edge -> Api; ERROR forbidden edge -> Infrastructure; ERROR test-project edge | PASS | PASS |
| E1-T1 | forbidden layer edges and a test-project edge [single quotes] | ERROR forbidden edge -> Api; ERROR forbidden edge -> Infrastructure; ERROR test-project edge | FAIL: misses ERROR forbidden edge -> Api; ERROR forbidden edge -> Infrastructure; ERROR test-project edge | PASS |
| E1-T2 | forbidden layer edges and a test-project edge [reversed attribute order] | ERROR forbidden edge -> Api; ERROR forbidden edge -> Infrastructure; ERROR test-project edge | PASS | PASS |
| E1-T3 | forbidden layer edges and a test-project edge [single quotes, multiline tags, CRLF] | ERROR forbidden edge -> Api; ERROR forbidden edge -> Infrastructure; ERROR test-project edge | FAIL: misses ERROR forbidden edge -> Api; ERROR forbidden edge -> Infrastructure; ERROR test-project edge | PASS |
| E1-T4 | forbidden layer edges and a test-project edge [mixed quotes, reversed, multiline] | ERROR forbidden edge -> Api; ERROR forbidden edge -> Infrastructure; ERROR test-project edge | FAIL: misses ERROR forbidden edge -> Api; ERROR forbidden edge -> Infrastructure; ERROR test-project edge | PASS |
| E1-EQ | forbidden layer edges and a test-project edge: identical normalized diagnostic sets across T0-T4 (3 finding(s) each) | identical sets | FAIL: normalized sets identical across transforms; every transform row passed | PASS |
| E2-T0 | test-project classification by framework package [double quotes, canonical order] | ERROR test-project edge | PASS | PASS |
| E2-T1 | test-project classification by framework package [single quotes] | ERROR test-project edge | FAIL: misses ERROR test-project edge, extra WARN unknown project, reference not parsed | PASS |
| E2-T2 | test-project classification by framework package [reversed attribute order] | ERROR test-project edge | PASS | PASS |
| E2-T3 | test-project classification by framework package [single quotes, multiline tags, CRLF] | ERROR test-project edge | FAIL: misses ERROR test-project edge, extra WARN unknown project, reference not parsed | PASS |
| E2-T4 | test-project classification by framework package [mixed quotes, reversed, multiline] | ERROR test-project edge | FAIL: misses ERROR test-project edge, extra WARN unknown project, reference not parsed | PASS |
| E2-EQ | test-project classification by framework package: identical normalized diagnostic sets across T0-T4 (1 finding(s) each) | identical sets | FAIL: normalized sets identical across transforms; every transform row passed | PASS |
| E3-T0 | PackageReference policies (inline, override, deprecated, reserved, Update, child Version, clean) [double quotes, canonical order] | ERROR deprecated; 3x ERROR inline version; WARN reserved; WARN VersionOverride | PASS | PASS |
| E3-T1 | PackageReference policies (inline, override, deprecated, reserved, Update, child Version, clean) [single quotes] | ERROR deprecated; 3x ERROR inline version; WARN reserved; WARN VersionOverride | FAIL: misses ERROR deprecated; 3x ERROR inline version; WARN reserved; WARN VersionOverride, reference not parsed | PASS |
| E3-T2 | PackageReference policies (inline, override, deprecated, reserved, Update, child Version, clean) [reversed attribute order] | ERROR deprecated; 3x ERROR inline version; WARN reserved; WARN VersionOverride | PASS | PASS |
| E3-T3 | PackageReference policies (inline, override, deprecated, reserved, Update, child Version, clean) [single quotes, multiline tags, CRLF] | ERROR deprecated; 3x ERROR inline version; WARN reserved; WARN VersionOverride | FAIL: misses ERROR deprecated; 3x ERROR inline version; WARN reserved; WARN VersionOverride, reference not parsed | PASS |
| E3-T4 | PackageReference policies (inline, override, deprecated, reserved, Update, child Version, clean) [mixed quotes, reversed, multiline] | ERROR deprecated; 3x ERROR inline version; WARN reserved; WARN VersionOverride | FAIL: misses ERROR deprecated; 3x ERROR inline version; WARN reserved; WARN VersionOverride, reference not parsed | PASS |
| E3-EQ | PackageReference policies (inline, override, deprecated, reserved, Update, child Version, clean): identical normalized diagnostic sets across T0-T4 (6 finding(s) each) | identical sets | FAIL: normalized sets identical across transforms; every transform row passed | PASS |
| E4-T0 | PackageVersion policies (floating, empty, prerelease, deprecated, reserved, stable) [double quotes, canonical order] | ERROR floating/empty ""; ERROR deprecated; ERROR floating/empty "*"; WARN prerelease; WARN reserved | PASS | PASS |
| E4-T1 | PackageVersion policies (floating, empty, prerelease, deprecated, reserved, stable) [single quotes] | ERROR floating/empty ""; ERROR deprecated; ERROR floating/empty "*"; WARN prerelease; WARN reserved | FAIL: misses ERROR floating/empty ""; ERROR deprecated; ERROR floating/empty "*"; WARN prerelease; WARN reserved | PASS |
| E4-T2 | PackageVersion policies (floating, empty, prerelease, deprecated, reserved, stable) [reversed attribute order] | ERROR floating/empty ""; ERROR deprecated; ERROR floating/empty "*"; WARN prerelease; WARN reserved | FAIL: misses ERROR floating/empty ""; ERROR deprecated; ERROR floating/empty "*"; WARN prerelease; WARN reserved | PASS |
| E4-T3 | PackageVersion policies (floating, empty, prerelease, deprecated, reserved, stable) [single quotes, multiline tags, CRLF] | ERROR floating/empty ""; ERROR deprecated; ERROR floating/empty "*"; WARN prerelease; WARN reserved | FAIL: misses ERROR floating/empty ""; ERROR deprecated; ERROR floating/empty "*"; WARN prerelease; WARN reserved | PASS |
| E4-T4 | PackageVersion policies (floating, empty, prerelease, deprecated, reserved, stable) [mixed quotes, reversed, multiline] | ERROR floating/empty ""; ERROR deprecated; ERROR floating/empty "*"; WARN prerelease; WARN reserved | FAIL: misses ERROR floating/empty ""; ERROR deprecated; ERROR floating/empty "*"; WARN prerelease; WARN reserved | PASS |
| E4-EQ | PackageVersion policies (floating, empty, prerelease, deprecated, reserved, stable): identical normalized diagnostic sets across T0-T4 (5 finding(s) each) | identical sets | FAIL: normalized sets identical across transforms; every transform row passed | PASS |
| E5-T0 | clean tree: every permitted edge, test packages, central versions [double quotes, canonical order] | clean | PASS | PASS |
| E5-T1 | clean tree: every permitted edge, test packages, central versions [single quotes] | clean | FAIL: reference not parsed | PASS |
| E5-T2 | clean tree: every permitted edge, test packages, central versions [reversed attribute order] | clean | PASS | PASS |
| E5-T3 | clean tree: every permitted edge, test packages, central versions [single quotes, multiline tags, CRLF] | clean | FAIL: reference not parsed | PASS |
| E5-T4 | clean tree: every permitted edge, test packages, central versions [mixed quotes, reversed, multiline] | clean | FAIL: reference not parsed | PASS |
| E5-EQ | clean tree: every permitted edge, test packages, central versions: identical normalized diagnostic sets across T0-T4 (0 finding(s) each) | identical sets | FAIL: every transform row passed | PASS |

**ENC**

| Row | Case | Expected | Pre-fix | Final |
|---|---|---|---|---|
| N1 | UTF-8 BOM project file, single-quoted Domain->Api | ERROR forbidden edge -> Api | FAIL: misses ERROR forbidden edge -> Api | PASS |
| N2 | UTF-16LE project files, single-quoted Domain->Api and inline Version | ERROR forbidden edge -> Api; ERROR inline version | FAIL: misses ERROR forbidden edge -> Api; ERROR inline version, reference not parsed | PASS |
| N3 | clean: UTF-16LE single-quoted permitted references and versionless package | clean | FAIL: reference not parsed | PASS |
| N4 | UTF-16BE project file (tolerated), single-quoted Domain->Api | ERROR forbidden edge -> Api | FAIL: misses ERROR forbidden edge -> Api | PASS |
| N5 | UTF-16LE Directory.Packages.props, single-quoted floating version | ERROR floating/empty "*" | FAIL: misses ERROR floating/empty "*" | PASS |
| N6 | control: UTF-16LE double-quoted Domain->Api | ERROR forbidden edge -> Api | PASS | PASS |

**HOOK**

| Row | Case | Expected | Pre-fix | Final |
|---|---|---|---|---|
| H1 | PostToolUse Write (nested cwd in worktree): single-quoted Domain->Api reaches the hook response | assertions | FAIL: decision block; reason has the architecture ERROR; manual checker from nested worktree cwd reports it (exit 1) | PASS |
| H2 | PostToolUse Edit: PackageVersion Version='*' Include='Microsoft.Extensions.Http.Polly' reaches the hook response | assertions | FAIL: manifest title for the file; floating-version ERROR; deprecated-package ERROR | PASS |
| H3 | PostToolUseFailure Bash (real Git Bash, exit 3): single-quoted Domain->Api written before failing | assertions | FAIL: context has the architecture ERROR | PASS |
| H4 | PostToolUseFailure PowerShell (real Windows PowerShell 5.1 Out-File = UTF-16LE, exit 3): single-quoted inline Version | assertions | FAIL: context has the inline-version ERROR | PASS |
| H5 | PostToolUse Write of a valid single-quoted project file in the worktree: no spurious violation; launcher violation not reported | assertions | FAIL: the launcher checkout really holds a detectable violation | PASS |
| H6 | PostToolUse PowerShell success (UTF-16LE): valid single-quoted central version + versionless reference, no spurious violation | assertions | FAIL: the UTF-16LE single-quoted reference is parsed (not vacuous) | PASS |
| H7 | PostToolUse Bash success: valid single-quoted Application->Domain, no spurious violation | assertions | PASS | PASS |
| H8 | Stop: uncommitted single-quoted floating version is a manifest error; repeat and stop_hook_active do not re-block | assertions | FAIL: first Stop blocks; reason has the manifest error | PASS |
| H9 | PreToolUse unchanged: harmless allowed, BOM input allowed, malformed input denied (fail closed), dependency and reference commands routed | assertions | PASS | PASS |

**SMOKE**

| Row | Case | Expected | Pre-fix | Final |
|---|---|---|---|---|
| S1 | node --check on every template JavaScript module (9) | assertions | PASS | PASS |
| S2 | clean template: check-instructions / check-manifests / check-architecture (smoke only; no backend) | assertions | PASS | PASS |
| S3 | hook wiring: four events, exec form, PreToolUse onFailure "block" only, PostToolUseFailure on Bash\|PowerShell | assertions | PASS | PASS |
| S4a | optional-frontend removal procedure: instruction checker 0 errors, 61 files, ~5219 tokens | assertions | PASS | PASS |
| S4b | frontend removed: both checkers still run (no frontend module) and report the single-quoted counterexample | assertions | FAIL: exact expected findings | PASS |
| S5 | M1 capability structure: four static slots, frame + required leaves + optional frontend, binds | assertions | PASS | PASS |

### 17.8 Equivalence Table

Each fixture is rendered five times. The transforms change only quote style, attribute order,
whitespace and line breaks inside start tags, and line endings:
- T0: double quotes, canonical order;
- T1: single quotes;
- T2: reversed attribute order;
- T3: single quotes, one attribute per line with spaces around `=`, CRLF;
- T4: alternating quotes (first attribute single-quoted), reversed order, multiline.

The assertion is equal normalized diagnostic sets (severity, reason, file, project or package
identity), not equal counts.

| Fixture | Findings per transform | Final: sets identical T0–T4 | Pre-fix |
|---|---|---|---|
| E1 forbidden layer edges (Domain → Api, Domain → Infrastructure) and a test-project edge | 3 ERROR | yes | T1, T3, T4 lose all three |
| E2 test-project classification by `Include` of the framework package; Api → Specs | 1 ERROR | yes | T1, T3, T4: ERROR replaced by an unknown-project WARN |
| E3 `PackageReference` policies: inline `Version`, `VersionOverride`, deprecated, reserved, `Update` + `Version`, child `<Version>`, clean | 4 ERROR, 2 WARN | yes | T1, T3, T4 lose all six |
| E4 `PackageVersion` policies: `*`, empty, prerelease, deprecated, reserved, stable | 3 ERROR, 2 WARN | yes | T1–T4 lose all five (T2: order only) |
| E5 clean tree: every permitted edge, test packages, central versions | none (references parsed) | yes | T1, T3, T4: clean only because nothing was parsed |

### 17.9 Hook Integration

The hooks and `settings.json` are byte-identical to iteration 2. Each hook row used a fresh, real
Git repository: the template under test plus the backend tree, committed, with a real worktree at
`.claude/worktrees/feat`.
- The hook script of the launcher checkout ran with `CLAUDE_PROJECT_DIR` set to the launcher and
  with the worktree (or a directory nested in it) as both process and input `cwd`.
- Each mutation was actually performed in the worktree:
  - Write/Edit rows wrote the file;
  - the Bash rows executed `C:\Program Files\Git\bin\bash.exe`;
  - the PowerShell rows executed Windows PowerShell 5.1 (`powershell.exe -EncodedCommand`).
- The hook input was the documented event JSON.

| Row | Event and mutation | Final hook response |
|---|---|---|
| H1 | `PostToolUse` Write, cwd `worktree/backend`: Domain → Api with `Include='...'` | `decision: block`, `Architecture check (.claude/rules/architecture.md):` with the forbidden-edge ERROR. The manual checker from the nested worktree cwd also exits 1 with it; the launcher checkout stays at 5 projects, 0 errors |
| H2 | `PostToolUse` Edit of `Directory.Packages.props`: `<PackageVersion Version='*' Include='Microsoft.Extensions.Http.Polly' />` | block with the floating ERROR and the deprecated ERROR, plus the add-dependency reminder |
| H3 | `PostToolUseFailure` Bash: `printf … > backend/Demo.Domain/Demo.Domain.csproj; exit 3` writes the single-quoted forbidden edge, exit code 3 | `additionalContext` with the forbidden-edge ERROR and `- modified: backend/Demo.Domain/Demo.Domain.csproj` |
| H4 | `PostToolUseFailure` PowerShell: `Get-Content … -replace … \| Out-File` writes a UTF-16LE `.csproj` with `<PackageReference Include='Newtonsoft.Json' Version='13.0.3' />`, then `exit 3` | `additionalContext` with the inline-version ERROR and the routing note |
| H5 | `PostToolUse` Write of a valid single-quoted, multiline, reordered `Demo.Api.csproj` in the worktree; the launcher checkout holds an uncommitted single-quoted Domain → Api violation | no output (no spurious violation). The launcher's own checker reports its violation, so the silence is worktree targeting, not blindness |
| H6 | `PostToolUse` PowerShell success: UTF-16LE `PackageVersion Include='Newtonsoft.Json' Version='13.0.3'` and versionless `PackageReference Include='Newtonsoft.Json'` | routing note only, no ERROR or WARN. The worktree checkers give 0 findings and parse `[Newtonsoft.Json, null, null]` |
| H7 | `PostToolUse` Bash success: valid single-quoted Application → Domain | routing note only, no ERROR or WARN |
| H8 | `Stop`: uncommitted single-quoted `Version='*'` in the worktree's `Directory.Packages.props` | first Stop blocks with `Manifest errors (.claude/rules/dependencies.md):` and the floating ERROR. The unchanged repeat and `stop_hook_active: true` both allow |
| H9 | `PreToolUse` | harmless command and BOM + CRLF input allowed; malformed input denied (fail closed); `dotnet add … package` and `dotnet add … reference` denied for routing; identical before and after |

Before the fix, H1 and H8 produced no response at all. H2 produced only the reminder. H3, H4, and
H6 produced only the routing note: the hooks fired and saw the change, but the checker reported
nothing. Verbatim final H3 context (abridged after the first three lines):

```text
Architecture check (.claude/rules/architecture.md):
ERROR: backend/Demo.Domain/Demo.Domain.csproj: Demo.Domain (core model) must not reference Demo.Api (entry point); dependencies point inward (.claude/rules/architecture.md, Dependency Direction).
Dependency manifests or project files changed without a recognized dependency or project-reference command:
- modified: backend/Demo.Domain/Demo.Domain.csproj
...
```

As in Section 16.5, only the last step is simulated: Claude Code's own tool runner was not invoked,
and the hook JSON was built to the documented schema. The scripts, processes, Windows shells,
repositories, and worktrees are real. This is a real Windows run: Windows 11, Git Bash, and
Windows PowerShell 5.1.

### 17.10 Preservation

| Gate | Result |
|---|---|
| S1 `node --check`, all 9 template JavaScript modules (including the three changed ones) | 0 failures |
| S2 clean template (smoke only, no backend) | `check-instructions: 65 instruction file(s), always-loaded ~5568 tokens, 0 error(s), 0 warning(s)`; `check-manifests: 0 error(s), 0 warning(s)`; `check-architecture: 0 backend project(s), 0 error(s), 0 warning(s)` |
| S3 hook wiring | exactly `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `Stop`; exec form; `onFailure: "block"` only on PreToolUse; PostToolUseFailure on `Bash\|PowerShell` |
| S4a optional-frontend removal (template-maintenance § Removing the Optional Frontend Slot) | 0 errors, 61 instruction files, ~5219 tokens, as in Section 16.7 |
| S4b checkers with the frontend slot removed | both run without the frontend module and report the R1 findings exactly |
| S5 capability structure | four slot contracts; selection rows architecture (frame, required, clean-architecture), persistence (leaf, required, ef-core), backend-testing (leaf, required, nunit), frontend (leaf, optional, angular); persistence binds `architecture/clean-architecture`; frame and other leaves bind nothing |
| ENC rows | UTF-8 BOM, UTF-16LE, and UTF-16BE project files and UTF-16LE `Directory.Packages.props` are decoded as before (`readXml` unchanged) and checked with single quotes; the double-quoted UTF-16LE control passes before and after |
| Nested cwd and worktree targeting | H1 (nested worktree cwd, hook and manual CLI), H3–H8 (worktree), H5 (launcher checkout not used) |
| Stop loop prevention | H8 (unchanged-state repeat and `stop_hook_active`) |
| I1 runtime files | 80, same paths; none added or removed |
| I2 changed files | exactly the three permitted files (Section 17.4) |
| I3 other template files | 77 byte-identical to the starting inventory |
| I4 pre-fix comparison copy | still `60b39d95…89eed49b` |
| I5 protected inputs | 145/145 unchanged |
| I6 `MANIFEST.sha256` | 140/140 OK |
| I7 policies | 194 inventory policies (unique IDs) + GOV-017, GOV-018; all 71 non-script template files byte-identical |
| I8 / I9 hygiene before cleanup | `output/` holds only `template/`, `REFINEMENT_REPORT.md`, and the temporary `.work/`; no `.git`, `bin`/`obj`, `node_modules`, or hook-state file inside `output/template/` |
| I10 changed scripts | no control or invisible characters and no new non-ASCII line (the one non-ASCII line, `'—'` in `selectedImplementation`, predates this pass) |
| I11 changed scripts | name no capability implementation or slot package; package data still comes from the manifests |

### 17.11 Policy and Capability Preservation Rationale

No policy-bearing artifact changed:
- `CLAUDE.md` and the decision records;
- the flat rules;
- skills, the agent, and the map;
- capability contracts and manifests, including `binds`;
- `settings.json` and the hooks.

All 71 non-script files are byte-identical to the accepted iteration-2 output, whose coverage
evidence is Sections 5 and 16.8 (196/196 owner anchors; 0 owner, trigger-role, and minimum-scope
regressions). This pass ran no fresh semantic audit of the 196 entries.

What did change is enforcement code that implements existing policies:
- dependency direction and test-project references (`.claude/rules/architecture.md`);
- central package management, floating and prerelease versions, and deprecated, reserved,
  exception, and competing-framework packages (`.claude/rules/dependencies.md`, add-dependency,
  test-framework).

Those policies now hold for single-quoted and reordered XML. Their levels, messages, and owners are
unchanged, and the only new message is the explicit unreadable-element WARN.

The architecture is the same:
- four static slots;
- one required architecture frame, required persistence and backend-testing leaves, and an
  optional frontend leaf, with frame/leaf separation;
- the static selection record;
- flat topical rules;
- the always-loaded surface (~5,568 tokens).

The reader names no implementation, and every package and project identity still comes from the
selected manifests (I11, S4b, S5).

### 17.12 Test-Side Calibrations and the Confirmation Correction

None of these changed a template file or an expected finding set.

1. **Before the fix: equivalence transform T4.** The first before-fix run showed E1-T4, E2-T4, and
   E5-T4 passing although they were predicted to fail. T4's alternating quotes started with a
   double quote, so the decisive `Include` was never single-quoted. The alternation now starts
   with a single quote, and P03 states the other mixed pairing (`Include="…" Version='…'`)
   explicitly. This makes the rows stronger, not weaker.
2. **Before the fix: frontend-removal procedure.** The harness's map edit also dropped the
   retained `capabilities/frontend/CONTRACT.md` pointer. The checker reported `map does not list
   .claude/capabilities/frontend/CONTRACT.md` on the unmodified template. After correcting the
   edit, the result equals Section 16.7.
3. **Before the confirmation: gate I10.** The first draft required the changed scripts to be
   ASCII-only. `lib/common.js` already contained `'—'`, so I10 now applies the established
   iteration-2 gate (no control characters and no new non-ASCII lines).
4. **Confirmation run 1: `CONFIRMATION: FAIL`, a gate error.**
   - All 134 final rows passed, all 11 identity gates passed, and the pre-fix run had 0
     `SETUP` rows and 0 prediction mismatches.
   - The overall gate also required zero prediction mismatches on the final run. Pre-fix
     predictions describe the pre-fix template, so on the fixed template the 84 rows predicted
     to fail must pass. The 84 "mismatches" were verified to be exactly the 84 repaired rows,
     each "predicted pre-fix fail, got PASS".
   - Correction: predictions are compared with the pre-fix run only.
   - One full reconfirmation then passed. Its final and pre-fix results, finding sets, and tree
     hashes are identical to run 1 and to the separate before-fix and after-fix records.

### 17.13 Known Limits

- **Bounded reader, not an XML or MSBuild implementation.**
  - It does not validate XML, decode entity or character references (`&#42;` stays literal), or
    expand properties, conditions, imports, item lists (`Include="A;B"`), or wildcards.
  - It does not trim item specifications.
  - Item and attribute names stay case-sensitive, and package-ID comparison stays exact, as
    before. NuGet IDs are case-insensitive, so `newtonsoft.json` is not matched against the
    tables.
- **Malformed input.** After a malformed start tag, reading resumes at the next `>`. An element
  hidden by an unterminated comment is reported only when its own element name appears after the
  comment start. A DOCTYPE internal subset containing `>` is not supported (none occurs in
  MSBuild files).
- **Unchanged regex-based property checks.** `ManagePackageVersionsCentrally` (CPM enabled) and
  `IsTestProject` are element-text checks, not attribute handling, and stay as they were. A
  commented-out `<ManagePackageVersionsCentrally>true</…>` would still satisfy the CPM check.
  This limitation predates the pass, which did not extend its scope to it.
- **Item identities read, as before.** `ProjectReference` and `PackageVersion` use `Include`
  only; `PackageReference` uses `Include` or `Update`; `GlobalPackageReference` is not checked.
- **Windows evidence.** H3, H4, H6, and H7 executed real Git Bash and Windows PowerShell 5.1
  processes on Windows 11. Claude Code's own tool runner was not exercised (Section 17.9).
- **Policy audit.** No fresh semantic audit of the 196 policies was run; preservation rests on
  byte identity (I7) and the earlier coverage evidence.

### 17.14 Q1 / Q2 / Q3 Status

- **Q1 (V2 fidelity):** unchanged. No instruction text changed.
- **Q2 (capability coupling):** unchanged:
  - no contract, manifest, facet, or `binds` entry changed;
  - the reader is implementation-neutral, and package data stays in the manifests;
  - checking still works with the optional frontend removed (S4b).
- **Q3 (minimalism):** no new file, slot, dependency, layer, or always-loaded text.
  - The added code is one shared reader (one new `common.js` export), one version-metadata
    helper, and one message helper.
  - Added size: +4,831 JavaScript bytes, of which `common.js` is +3,742.

### 17.15 Cumulative Confirmation and Result

Sequence:
1. Snapshot.
2. Reproduction on the untouched code: the frozen copy and the live output.
3. Full before-fix record: 134 rows, 50 PASS, 84 FAIL, 0 SETUP, 0 prediction mismatches.
4. The fix.
5. Full after-fix run: 134/134.
6. One cumulative confirmation: `node harness.js confirm` ran every suite on the final template
   and on the frozen pre-fix copy, plus the identity, policy, and hygiene gates.
7. One targeted gate correction (Section 17.12, item 4).
8. One full reconfirmation, which ended `CONFIRMATION: PASS`.

No template file changed after the fix was applied; the final tree is `d605154a…ae8684b8`
throughout. Nothing was changed after the reconfirmation except appending this section and
removing `output/.work/`.

**Resulting status: STRICTLY_BETTER.**
- Every reported single-quote bypass now produces the same relevant decision as its
  double-quoted equivalent:
  - R1 and the K, P, A, N, and E rows;
  - the equivalence sets E1–E5, identical across five transforms.
- Valid single-quoted, mixed, reordered, multiline, and UTF-16 XML is not rejected, and its
  references are parsed (A11–A13, A18, K11, K12, P01–P04, P15, N3, E5, H5–H7).
- Existing severities, layer rules, test-project classification, child `<Version>` precedence,
  and `VersionOverride` handling are preserved (the 50 guard rows include every double-quoted
  control).
- The unchanged hooks surface the corrected findings after Write, Edit, successful and failed
  Bash and PowerShell commands, and Stop, against the active worktree.
- Protected inputs, the 77 other template files, the four-slot M1 architecture, the 196
  policies, and the hook configuration are unchanged.

The 84 repaired rows fail on the iteration-2 output and pass now, so the improvement is
demonstrated and not a tie.

## after_codex_audit_1 — ARC-025 boundary correction

Task: `M1-after_codex_audit_1-CORRECTIVE_TASK.md`, a bounded single-policy correction. Work
continued from the current `output/template/`; nothing was recopied from `baseline/`,
regenerated, or replayed.

### Finding

- Two independent, same-input Codex freeze-readiness audits reported the same single confirmed
  M1 blocker: A-001 / `ARC-025`.
- Canonical policy (`source/inventory.json`, group `architecture`, `ARC-025`, `MUST`,
  `trigger_class: path`, `scope: backend`): "Infrastructure translates remote HTTP responses into
  Application-facing abstractions; do not leak HttpResponseMessage or remote transport concerns
  into Application."
- The M1 owner text (`.claude/rules/architecture.md` § Layer Placement) narrowed this twice:
  - it covered only "Application contracts", not Application itself;
  - it added an exception, "unless the Application explicitly models HTTP".
- The normalized policy has neither qualification, so the owner rule permitted what a `MUST`
  policy forbids. Historical V2 wording, local examples, and checker PASS results do not override
  the normalized policy.

### Change

One file, one literal block replacement in `output/template/.claude/rules/architecture.md`
(lines 135–137):

```diff
 - Infrastructure translates remote HTTP responses into Application-facing
   abstractions; do not leak `HttpResponseMessage` or remote transport concerns
-  into Application contracts unless the Application explicitly models HTTP.
+  into Application.
```

| Target | SHA-256 | Bytes |
|---|---|---|
| before | `47befd19b838669482734d5bc68ba365383c78b88f42e7953452237380b65e3e` | 6,712 |
| after | `c2040cf8f51e6ec0a00f8b23aabea3fc9fe891557636a1143029bd2992b4537c` | 6,656 |

LF line endings, no BOM, the trailing newline, the front matter, the owner header, and every
other byte are unchanged.

### Preflight Guard

All preconditions passed before any edit:
- 80 regular files in `output/template/`, with no non-regular entries;
- the target SHA-256 equals the stated original;
- the old block occurs exactly once, and the corrected block zero times.

A transient `output/.work/` held the snapshot:
- the sorted 80 paths and their SHA-256 values;
- the original target bytes;
- the report hash;
- the hashes of 147 protected files: the M1 root files (including all prompts and iteration
  records), `source/`, `baseline/`, and `audit/`.

### Validation

| Gate | Result |
|---|---|
| V1 canonical policy | PASS. The inventory text was re-read independently. The corrected bullet carries the full unconditional boundary: Infrastructure translates, and neither `HttpResponseMessage` nor any transport concern enters Application. `MUST` / `path` / `backend` are unchanged. `ARC-025` occurs once among the inventory's IDs. |
| V2 replacement identity | PASS. Expected bytes were built from the captured original by one literal replacement. The actual file is byte-identical to them (6,656 = 6,656 bytes) and hashes to `c2040cf8…2b4537c`. |
| V3 no collateral change | PASS. The 80/80 path set is identical. All 79/79 other template files hash-identical to the snapshot, re-checked after the checker run. All 147/147 protected files are identical. Hashes were compared, not modification times. |
| V4 static semantics | PASS. The unqualified prohibition is present once. "explicitly models HTTP" and "unless the Application" are absent from the rule. The ARC-025 bullet has no "Application contracts" wording. The front matter (`backend/**/*.cs`, `backend/**/*.csproj`), the owner header, and the `## Layer Placement` heading are unchanged. The `httpclient-factory` skill, which corroborates the policy ("Application does not need to know that the external service uses HTTP"), and all four capability slots are covered by V3. |
| V5 existing checkers | PASS as a smoke test; details below. |
| V6 hygiene | PASS. `output/.work/` was removed after the checks. `output/` contains only `template/` and `REFINEMENT_REPORT.md`. No fixture or runtime asset was added. |

V5 ran once from `output/template/`, with no checker edits:

| Command | Exit | Output |
|---|---|---|
| `node .claude/scripts/check-instructions.js` | 0 | 65 instruction file(s), always-loaded ~5568 tokens, 0 error(s), 0 warning(s) |
| `node .claude/scripts/check-architecture.js` | 0 | 0 backend project(s), 0 error(s), 0 warning(s) |
| `node .claude/scripts/check-manifests.js` | 0 | 0 error(s), 0 warning(s) |

No unrelated pre-existing issue was reported. The checkers do not test ARC-025's wording:
`check-architecture` finds no backend project to scan in the template. V1–V4 are the deciding
gates.

### Preserved M1 Identity

Unchanged:
- flat M-style topical rules;
- the four static capability slots, with their selection record, contracts, manifests, and
  `binds`:
  - architecture frame: `clean-architecture`;
  - persistence: `ef-core` / `sqlserver`;
  - backend-testing: `nunit`;
  - optional frontend: `angular`;
- frame/leaf ownership;
- every `trigger_class`, scope, and policy owner. ARC-025 stays owned by the path-loaded
  `architecture.md`;
- hooks, scripts, settings, and skill ownership.

No rule, document, file, or dependency was added.

### Scope Limit and Result

This pass fixes the one shared-policy blocker. It is not:
- a new audit of the inventoried policies. The task text says 196; `source/inventory.json`
  reports `policy_count: 194`, with 194 unique IDs. This pass did not investigate the difference;
- an exhaustive runtime proof;
- a phase-5.4 parity alignment. Analyzer configuration, Polly exceptions, test-host lifetime, and
  migration wording were left as they are;
- an unconditional freeze certification.

No live Claude host session was run. This section was appended after every gate passed. The prior
129,387 bytes (SHA-256 `4955c636…aebf93`) are its unmodified prefix.

**Result: `ARC-025_CORRECTED_WITH_DOCUMENTED_LIMITATIONS`.**
