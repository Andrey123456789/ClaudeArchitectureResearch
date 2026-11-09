# K0 Refinement Report — Iteration 005 / 5.3

## Final status: **STRICTLY_BETTER**

Every strict-promotion gate item in `REFINEMENT_TASK.md` § 12 passes (gate table at the end). The result is still K0: seven Kinds, six Scopes, one primary Kind and Scope per artifact, mechanism by Kind, one always-loaded decision register with `Details in` / `Affects`, scope-first path-scoped standards, embedded technologies, and no Levels or capability machinery.

## Baseline provenance

- Immutable baseline: **5.2 / K0 / Run-02** (`baseline/template/`, 62 files, 324,363 bytes). The Run-01 template was not sought or used.
- `output/` was empty at start. `baseline/template/` was copied to `output/template/` and checked byte-identical (`diff -r`).
- Initial tree hash (sha256 of the sorted per-file `sha256sum` list): `18f51b02f45bb5cbc7284e5fc412aee810996bc8c16ff0676f65c9c3144c2209` (same as the baseline).
- Final tree hash, same method: **`51105bf425561a167dfda0bce08314c9f1fa84ef4a71be85bc9a26892ce08022`** (63 files).

## Evidence base

One bounded harness under `output/.work/`, created once and kept until this report was written:

- process-level hook runs in exec form, with the main checkout as the launcher;
- sandbox Git repositories whose paths contain spaces, a linked worktree and a worktree nested in a checkout;
- Git discovery capped from the first test (`GIT_CEILING_DIRECTORIES`), with an isolated empty global Git config;
- real Git Bash and Windows PowerShell 5.1 mutations;
- a small structural fixture set;
- a one-time baseline contrast run on a *copy* of the baseline.

**Final run: 298/298 checks pass.**

| Section | Checks |
|---|---:|
| Static: JS syntax, checker on the final template, settings shape | 6 |
| 6.1 Launch, root, worktree, nested cwd, spaces | 20 |
| 6.2 Input, failure modes, encodings | 24 |
| 6.3 Dependency and project-reference routing | 103 |
| 6.4 Git-safety routing | 81 |
| 6.5 Actual state after successful and failed shells | 23 |
| 6.6 Stop | 12 |
| 6.7 K0 structural fixtures | 23 |
| Baseline contrast | 6 |

The live Claude session was not moved into a sandbox. Host semantics come from `audit/EXTERNAL_MECHANICS_NOTES.md`:

- exec form and `${CLAUDE_PROJECT_DIR}` in `args`;
- hook input `cwd`;
- `PostToolUseFailure`;
- `onFailure: "block"`.

These semantics are relied on as documented. They were not re-proven against the running session.

## D1–D11 disposition

| ID | Repair | Evidence |
|---|---|---|
| **D1** active worktree | New `.claude/scripts/repo.cjs` separates the **launcher root** (only locates `hook.cjs`) from the **active root**. The active root is the Git work tree of the hook input `cwd`, or of the edited file. All checks use the active root: path relativization, Git state, manifest and graph validation, co-change, instruction validation, and per-worktree state in `<active root>/.claude/.hook-state/`. `process.cwd()` is only a fallback when `cwd` is absent. | The dossier reproduction now reports the inline-version error, whether the session cwd is the worktree or the main checkout. Root, nested backend, nested frontend, worktree root and nested worktree cwd all pass, with Bash and PowerShell tool names. Main and worktree snapshots stay separate, and the main checkout stays clean. Baseline contrast: silent. |
| **D2** fail-closed PreToolUse | `settings.json` uses exec form (`"command": "node"`, `args` with `${CLAUDE_PROJECT_DIR}/.claude/hooks/hook.cjs`) and `"onFailure": "block"`, set only on the PreToolUse policy hook. Unreadable or incomplete required input, or a crashing helper, produces an explicit `deny`. A missing script, a crash of `hook.cjs` itself or a timeout ends with a non-zero exit, which the host blocks. PostToolUse, PostToolUseFailure and Stop stay non-blocking. | Checks: <ul><li>empty, whitespace, malformed, array, missing-command and invalid-UTF-8 input → deny;</li><li>broken `repo.cjs` → deny;</li><li>missing script and syntax-broken hook → non-zero exit with no allow output;</li><li>hung stdin → the hook keeps waiting and never emits a premature allow;</li><li>malformed post/stop input → visible exit 1.</li></ul> Fixture: removing `onFailure` → FAIL. |
| **D3** dependency routing | Table-driven npm/pnpm/yarn classifier (subcommand → change / named-package / restore), with value-taking global options skipped (`--prefix`, `-w`, `--workspace`, `--dir`, `-C`, `--filter`, `--cwd`, …). Force and legacy-peer flags are detected in any position, and a restore with a bypass flag counts as a change. Also covered: ng/npx ng, NuGet CLI and PMC cmdlets, `.cmd`/`.exe`/full-path forms, nested `bash -c` / `powershell -Command` / `cmd /c`, quote-aware segment splitting. | 56 change forms detected (7 with the force flag noticed). 29 restore, read-only or unrelated forms allowed, including `npm install`, `npm ci`, `dotnet restore`, `dotnet list package`, and `git commit -m "npm install …"`. The reviewed marker allows the command. One classifier bug found by the harness (`yarn workspace <name> add`) was fixed. |
| **D4** project-reference graph | `dotnet add/remove [<project>] reference …` and `dotnet reference add/remove …` (spaces in paths, option placement) are denied as Reserved unless the command carries `# project-references: approved`. The dependency marker does not approve a reference change. New `project-structure` § Changing project references owns the procedure. After execution, actual graph changes — a changed reference set, a new project with references, a removal or move with dangling references — are flagged as Reserved; this is not a substitute for the pre-gate. | 7 reference forms detected, plus marker semantics. Shell matrix: a legal Api→Domain reference added by an unrecognized command is flagged; a production→test reference is caught after a failed PowerShell command. |
| **D5** actual-state post-validation | PostToolUse and PostToolUseFailure for `Bash\|PowerShell` run one per-worktree snapshot model. The first observation records a full baseline and validates every tracked manifest and the instruction files. Later observations hash only the paths Git reports: status now, status at the last observation, missing snapshot entries, and `diff old HEAD..new HEAD`, with a full list for a first commit or an unknown old HEAD. Same-content delete+add is reported as a move. `node_modules`, build output, dot-directories, nested repositories and nested worktrees are never in the surface. | 23 matrix checks (see the actual-state section below). |
| **D6** Git safety | Table-driven read-only vs repository-changing classifier after global options (`-C`, `-c`, `--git-dir`, `--no-pager`, …). Conditional forms are handled (branch, tag, stash, worktree, remote, config, notes, reflog, submodule, symbolic-ref, bisect, sparse-checkout, apply, checkout, hash-object), and unknown subcommands count as repository-changing. Mutations return `permissionDecision: "ask"` (user confirmation = the explicit-request path); read-only commands produce no output. The partial static `permissions.ask` list was removed. Map and `git-workflow` claims were narrowed to what is enforced; Git run indirectly by scripts is stated as not classified. | 34 read-only and 45 mutating forms, plus the `ask` decision text and deny precedence. Baseline contrast: the old ask-list omits add, rm, mv, switch, apply, am and update-ref. |
| **D7** encodings | Hook stdin and manifests are decoded by `decodeText`: UTF-8 with or without a BOM, BOM-tagged UTF-16LE and UTF-16BE. Deterministic findings, never a crash, for: <ul><li>odd-length UTF-16;</li><li>invalid UTF-8;</li><li>NUL bytes without a BOM;</li><li>invalid surrogates.</li></ul> | BOM-prefixed and UTF-16LE hook JSON are parsed on all events. The four encodings of an invalid `.csproj` give identical findings, and a UTF-16LE `package.json` is clean. Four malformed variants give a single deterministic error each. A real `Set-Content -Encoding Unicode` file is validated. Baseline contrast: BOM rejected. |
| **D8** checker vs serialization | The checker validates properties, not the old serialization (see the checks below). | Fixtures: missing `onFailure` → FAIL; missing PostToolUseFailure → FAIL; the old shell-string command → FAIL. Baseline contrast: the old checker rejects exec form. |
| **D9** root-aware manual tools | Every instructed invocation uses `node "$(git rev-parse --show-toplevel)/.claude/scripts/…"`, which works in Bash and PowerShell. The scripts default to the Git work tree of the current directory and accept `--root`. The checker rejects cwd-relative `node .claude/…` invocations. | Git Bash and Windows PowerShell 5.1 from nested worktree directories with spaces check the worktree. The instruction checker passes from nested directories in both shells. The `template-maintenance` sample runs in both shells. Fixture: a cwd-relative command → FAIL. |
| **D10** Stop material state | Reminder keys include a content hash of every relevant changed file. The fingerprint is stored per worktree. `stop_hook_active` returns immediately. | The five-state sequence passes: remind / silent / remind on a same-path rewrite / silent / no loop. Seed, migration, test-satisfied and custom-settings obligations behave as before. A worktree stop inspects the worktree. A non-Git root fails visibly. Baseline contrast: silent on the same-path change. |
| **D11** Kind direction | The checker formalizes CONFORMS_TO, routing pointers and the ENF rules (detailed below). | Fixtures (see the structural section below). Baseline contrast: the old checker accepts a reversed STD→KNW edge. |

D8 checker properties:

- executable-only `command` plus an `args` vector;
- a `${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>` target that exists;
- an event argument handled by the script (parsed from its `EVENTS`);
- matchers covering the required tools: PreToolUse Bash/PowerShell; PostToolUse for edit tools and shells; PostToolUseFailure Bash/PowerShell; Stop;
- `onFailure: "block"` required on PreToolUse and rejected elsewhere;
- positive timeouts and no variable expansion.

D11 conformance relation (`CONFORMS_TO`):

- OP → nothing;
- DEC → OP;
- STD → DEC, OP;
- KNW → STD, DEC, OP;
- WF → KNW, STD, DEC, OP;
- ENF → STD, DEC;
- IN → OP, DEC;
- same-Kind edges are allowed but must stay acyclic.

D11 routing-pointer forms, which may point in any direction:

- references after `See also:`, `Workflow:`, `Technique:`, `Procedure:`, `Enforced by:` or `Loading:`;
- invocations (run, use, invoke, switch to, `→`, slash commands, `(agent …)`);
- sections whose heading names routing;
- imports;
- the register's Details in / Affects cells;
- a private reference naming its own skill;
- enforcement messages.

D11 handling of ENF and inputs:

- ENF declares its conformance in its header and in `Conforms to:` lines.
- References to product inputs are reads, not conformance.
- References to enforcement assets name files or tools, not owners.
- 16 unlabelled pointer lines in 11 files (KNW→WF, OP→WF, or same-Kind cross-references that formed cycles) were made explicit routing pointers.

## Actual-state shell matrix (D5)

All 23 checks pass:

- fresh state, then a first shell HEAD transition to an invalid committed manifest with a clean worktree → detected;
- later transitions → detected, or quiet on a valid revision;
- successful Bash mutation (`package.json` floating version) → detected;
- same-path rewrite with the same Git status → detected again;
- successful PowerShell UTF-16LE `.csproj` rewrite → detected;
- failed Bash (`exit 3`) and failed PowerShell (`exit 5`) commands with partial side effects → detected through `PostToolUseFailure` / `additionalContext`;
- failed command with no relevant change → quiet;
- unrecognized command text (Node script adding a deprecated package) → detected;
- unchanged unrelated commands in Bash and PowerShell → quiet, with no re-validation;
- tracked deletion → reported, and the dangling reference found;
- `mv` and `git mv` moves → reported as moves and validated at the new path;
- additions with references → validated and flagged;
- committing already-observed changes → quiet;
- skipped paths (`node_modules`, `bin`, a nested repository, a nested linked worktree) → neither observed nor falsely reported as removed;
- state loss → one re-baseline;
- product-input change → reminder;
- instruction-file corruption via `sed` → checked on the active root.

Non-Git copy of the system: a bounded walk validates the manifests, then stays quiet.

## K0 structural result (D8, D11)

`check-instructions` on the final template: **60 artifacts, 0 errors**.

Bounded fixture set: 23 checks, all as expected.

PASS cases:

- the legal WF→KNW, KNW→STD, STD→DEC and DEC→OP edges are recognized as conformance edges;
- legal ENF→STD and ENF→DEC declarations;
- explicit reverse-direction routing pointers.

FAIL cases:

- reversed STD→KNW, KNW→WF and DEC→STD edges;
- ENF→KNW and ENF→WF declarations;
- a KNW header on a rule, and an STD Kind on a skill;
- a broken `Affects` target, and a citation without `Affects` coverage;
- a decision restatement;
- a procedure in an STD;
- a bare norm in KNW;
- a `Level:` field, a `0-core/` directory and a capability-contract file;
- missing `onFailure`, missing PostToolUseFailure, and a shell-string hook;
- a broken reference and a missing section;
- a cwd-relative tool command;
- a second always-loaded import.

New property checks:

- malformed code fences (the check found and led to fixing a real defect in `logging/SKILL.md`);
- empty directories;
- exactly one Kind DEC artifact, which must be the only `@` import;
- `Details in` targets must appear in `Affects`;
- `Affects` targets must be STD/KNW/WF/ENF and unique;
- IN artifacts load as input;
- agents load as delegated agents.

No baseline check was weakened. The literal launcher-string check was replaced by stronger property checks. The STD-only "route to skills" check is subsumed by the general direction rule.

## Decision register / `Affects`

The register was unchanged: 18 entries, IDs, one-sentence decisions, Details in, Affects. Every citation is covered by `Affects`. Every `Details in` target is also listed in `Affects`. Every target exists and has an allowed Kind. The map's Decision → Affects view matches the register. New citations (`project-structure` → D-01; `solution-layout` → D-17) were already covered by `skills/project-structure`.

## Policy and invariant coverage (explicit 196-entry owner map, final vs baseline)

- **196 / 196** represented: 194 inventory policies plus GOV-017 and GOV-018.
- Owner regressions **0**, trigger-role deltas **0** (32 always / 123 path / 41 workflow, identical to the inventory), minimum-scope misses **0**, unresolved broken references **0**.
- Owner text is identical to the baseline except GOV-010. There, "synchronize it with `custom-settings`" became "synchronize it (workflow: `custom-settings`)", with the same semantics. The same routing-only change was made in the Decision Request line of `CLAUDE.md` § Decisions.
- Restatement sweep (shared 10-word sequences between artifacts): 14 pairs before and 14 after, no new sequences. All 14 are frontmatter/header boilerplate or check-by-reference pointers. One baseline restatement of D-17 in `solution-layout.md` was replaced by a citation.
- Hygiene: no research labels, policy IDs, workspace references or non-English text in `output/template/`. The only scanner hit is "Benchmark" in the RUN-012 owner text ("Benchmark or profile …"), which is a performance term.

## D12 — source-based V2 fidelity review

All of `source/v2-baseline/` was read.

Automated passes:

- section vocabulary coverage: 596 sections, mean 0.97;
- statement-level single-file coverage: 1,416 statements, 373 flagged below 0.75.

Every flagged statement was reviewed manually. Nearly all are preserved paraphrases at the K0 owner, V2 lineage notes ("detailed guidance belongs to the X skill", `technology-stack.md` pointers) that the register and Kind routing replace, or frontmatter descriptions kept concise for the always-loaded budget. No normative gap was found; all 196 owners are confirmed above.

Restored as practical technique, placed by Kind:

- `code-review` (WF): routing to the area → knowledge table, and approved `CUSTOM_SETTINGS.md` values as part of the intended behavior (from the V2 reviewer agent and code-review);
- `security-scan` (WF): a cross-skill technique pointer line (V2 "Cross-Skill Guidance");
- `build-fix` (WF): typical full-stack contract-failure triggers.

Intentionally omitted:

- verbose repetition;
- duplicate anti-pattern lists already expressed at the owner;
- V2 file-lineage notes;
- trigger keyword lists in descriptions.

## D13 — efficiency review

- Always-loaded surface: ≈ 19,724 → 19,738 characters, **≈ 4,931 → 4,935 tokens**. The +14 characters are the two explicit routing labels in `CLAUDE.md`, needed for D11.
- Runtime files: **62 → 63**. The added `.claude/scripts/repo.cjs` holds the single shared implementation of active-root resolution, Git calls, text decoding and hashing, used by the hook and both checkers; without it these would be implemented three times.
- Bytes: 324,363 → 366,543. Almost all of the growth is enforcement code:
  - `hook.cjs` 11.9 → 31.9 KB;
  - `check-instructions.cjs` 24.2 → 34.8 KB;
  - `check-dependencies.cjs` 11.8 → 13.7 KB;
  - `repo.cjs` 4.6 KB;
  - `MAP.md` 23.5 → 26.2 KB.
- Each increase implements a mandatory defect repair (D1–D11). No Markdown file, rule, skill, decision entry, layer or taxonomy cell was added, and the register stays a summary.

## Files

- **Added:** `.claude/scripts/repo.cjs`.
- **Removed:** none.
- **Changed, enforcement:** `.claude/settings.json`, `.claude/hooks/hook.cjs`, `.claude/scripts/check-dependencies.cjs`, `.claude/scripts/check-instructions.cjs`.
- **Changed, map:** `.claude/MAP.md` — conformance and routing conventions, Kind × Scope ENF cell, artifact rows, topic row, enforcement summary.
- **Changed, OP:** `CLAUDE.md` — two routing labels.
- **Changed, WF:**
  - `add-dependency`, `architecture-decision`, `verify`, `template-maintenance`, `project-structure` (+ `references/backend-layout.md`): root-aware commands, gate notes, § Changing project references;
  - `project-structure/references/solution-layout.md`: D-17 citation;
  - `git-workflow`: enforcement line;
  - `code-review`, `security-scan`, `build-fix`: D12;
  - `development-workflow`, `custom-settings`: routing and wording.
- **Changed, KNW:** `angular`, `api-versioning`, `ci-cd`, `docker`, `dotnet-testing`, `ef-core`, `swagger`, `httpclient-factory/references/resilience.md` (explicit routing labels); `logging` (broken code fence).

## Audits

- **Primary substantive audit** (all 20 items of § 10) found these concrete defects and repaired them:
  - the yarn-workspace classifier miss;
  - the D-17 restatement;
  - the D12 review cue;
  - "post-edit" wording made stale by shell-path reminders;
  - an over-broad "every Git command" claim (D6 claim accuracy).

  Before that, during the repairs themselves, the new checker exposed:
  - the broken fence in `logging/SKILL.md`;
  - 16 unlabelled reverse-direction or cycle-forming pointer lines;
  - the cwd-relative commands.
- **Cumulative confirmation audit** ran after the last template edit. It covered:
  - the full harness from fresh sandboxes (298/298);
  - the checker (0 errors) and JS syntax;
  - the 196-entry owner, trigger and scope audit;
  - the restatement sweep and hygiene;
  - the K0 identity checklist (§ 4);
  - a read of the final map and of the complete Markdown diff against the baseline.

  Result: **0 concrete template defects.**

## Workspace events (directly observed)

- Experimental isolation violations: **0**.
- Recoverable workspace-process incident: during the initial hash, a relative path wrote a hash list of the template one directory above the workspace (`../treehash.tmp`). It was deleted immediately and contained only hashes of allowed workspace files. No forbidden information was obtained.
- Platform-managed events:
  - the desktop app auto-registered the template's skills under `output/template/` as session skills; none was invoked;
  - one oversized output of my own listing of the template's rule files was stored by the tool runtime in its tool-results directory and read back once to see that output.

  Neither creates a dependency of the result on external data.

## Why the result is strictly better than the baseline

The baseline enforced the main checkout instead of the active worktree. Its critical pre-command hook could fail open. It missed removals, global-option forms and project-reference changes, and judged shell effects only by command text. It ignored failed shells and HEAD transitions, crashed on BOM input, let materially new work escape the Stop reminder, depended on cwd-relative manual commands, and had a checker that both froze an obsolete hook serialization and was blind to Kind direction.

The baseline-contrast checks reproduce each of these against the immutable baseline. The refined template repairs all of them with direct behavioral evidence. Every policy, trigger role, minimum scope, decision and K0 structural property is preserved; the only cost is enforcement code and +4 always-loaded tokens. This is a strict improvement, not a tie.

## Strict promotion gate

| Gate item | Result |
|---|---|
| D1–D11 repaired | PASS |
| D12 completed, real gaps repaired | PASS |
| D13 completed without unnecessary expansion | PASS |
| 194 + GOV-017/GOV-018 represented | PASS (196/196) |
| Owner regressions / trigger-role deltas / minimum-scope misses / broken references | 0 / 0 / 0 / 0 |
| K0 identity unchanged; exactly one authoritative DEC register; Kind determines mechanism | PASS |
| Kind conformance direction mechanically enforced | PASS (fixtures) |
| Git policy and deterministic Git enforcement agree on the documented surface | PASS |
| Active worktree, successful/failed shell, first/later HEAD, delete/move, encoding, Stop | PASS |
| No checker weakened to achieve PASS | PASS |
| Complexity growth justified by correctness | PASS |

---

## Corrective pass — iteration 2 (XML attribute quote parity)

### Status

**Defect repaired. Overall status remains `STRICTLY_BETTER`** relative to the immutable Run-02 baseline. The iteration-1 gate evidence above is unaffected because every other file is byte-identical, and this pass closes a gap in it. The cumulative confirmation audit found **0 concrete template defects (125/125)**.

Correction to the iteration-1 claims above: the D4/D5 manifest and project-graph evidence held only for **double-quoted** XML attributes. A valid single-quoted attribute bypassed both the dependency checker and the post-change hook.

### Scope and starting state

- Continued in place from the iteration-1 `output/template/` (63 files, 366,543 bytes); `baseline/` was not used.
- The starting tree hash was verified once with the iteration-1 recipe and matches the recorded value.
- A byte-identical snapshot of the starting template was kept in `output/.work/iter1/` as the comparison point.
- The iteration-1 298-check harness was **not available**: it was deleted from `output/` after iteration 1. It was not reconstructed, and no claim of 298 freshly run checks is made.
- The live Windows matrix was not rerun, because `hook.cjs`, `repo.cjs`, `check-instructions.cjs` and `settings.json` are byte-identical.

### Reproduction before editing: 14/14

Run against the iteration-1 snapshot in isolated Git sandboxes.

| Case | Double-quoted control | Single-quoted, iteration 1 |
|---|---|---|
| A — Domain `<ProjectReference Include='../My.Api/My.Api.csproj' />`, checker | exit 1, `Domain must not reference Api (My.Api)` | exit 0, zero errors |
| A — hook: clean first PostToolUse observation, then a real Git Bash rewrite of the Domain project | direction error and Reserved graph reminder | **no PostToolUse output at all** |
| B — `<PackageReference Include='Microsoft.Extensions.Http.Polly' />` | deprecated-package error | no diagnostic |
| C — `<PackageVersion Include='NewDep' Version='*' />` | floating-version error | no diagnostic |

`projectReferences()` returned `[target]` for the double-quoted form and `[]` for the single-quoted form.

The same run confirmed three same-root defects in the same attribute readers. Each was covered by one finite case and fixed with the main defect:

- `<PackageVersion Version="*" Include="NewDep" />` produced no diagnostic, because the regex required `Include` before `Version`.
- A single-quoted `<PackageReference … Version='…' />` produced an error that named the package `?`.
- An unclosed quote (`Include='../My.Api/My.Api.csproj />`) was accepted silently with exit 0.

### Root cause

Four separate regexes in `check-dependencies.cjs` read attributes only in the form `name\s*=\s*"…"`:

- `projectReferences()`;
- the `PackageReference` Include reader;
- the `PackageVersion` Include and Version reader, which was also order-dependent;
- the textual `Version=` and `VersionOverride=` tests.

The hook builds its project-reference snapshots through the exported `projectReferences()`, so it inherited the blind spot. With single quotes, the reference set was `[]` both before and after the change, so no graph change was seen.

### Repair

The only changed file is `.claude/scripts/check-dependencies.cjs`: new lines 69–131 and 171–175 replace old lines 69–87 and 127–128.

- **One start-tag reader.** `xmlElements(text, name)` uses two sticky regexes: one for an attribute, `\s+name\s*=\s*("…"|'…')` with no `<` inside a value, and one for the tag end, `\s*/?>`. It returns each element's attributes and the content of a paired element. Attributes may come in any order, with whitespace around `=`, in either matching delimiter, and with mixed styles across attributes.
- **Malformed start tags are reported.** A start tag that cannot be read completely (unclosed or mismatched quote, unquoted value) is marked malformed. `readable()` then reports a deterministic error with the line number. The tag is never guessed at or skipped.
- **Every reader uses it.** `projectReferences()`, the `PackageReference` loop (Include, `Version` attribute or `<Version>` child, `VersionOverride`, package names) and the `PackageVersion` loop all go through the reader. No divergent quote-specific regex remains.
- **Unchanged:**
  - the K0 ENF header (lines 1–8) and the exports;
  - backslash normalization of reference paths;
  - every validation and every existing finding message (one new malformed-element error was added);
  - the hook, which calls the export.
- No dependency, parser or framework was added. The file grew from 13,659 to 15,928 bytes (+2,269).

Double-quoted behavior differs from iteration 1 only where the old reader was wrong:

- `PackageVersion` entries with `Version` before `Include` are now checked;
- a `>` inside a quoted value no longer truncates the start tag;
- a malformed start tag of these three elements is reported;
- a paired `PackageReference` without a closing tag has its attributes checked;
- the element name must be followed by whitespace, `/` or `>`.

### Confirmation audit: 125/125, 0 failures

The confirmation run used fresh sandboxes and a frozen harness.

**Harness**

- One file, `output/.work/harness.cjs`.
- Frozen before the confirmation run (sha256 `a4614224376e3bbeb2693b73abacfd8eaeb1eb39e332ac0583343ed9c2a02274`) and verified unchanged after it.
- Each sandbox is a real Git repository with spaces in its path that holds a full copy of the template under test. The real checker and hook run from those copies.
- Git discovery was capped, and Git ran with an empty global configuration.
- Shell steps used real Git Bash and Windows PowerShell 5.1. Each step verified its own exit status and the resulting file content, so a sandbox error cannot pass as a template result.
- The first matrix run, before freezing, was also 125/125. No harness defect was found, and no criterion changed.

**Results by family**

"FAIL / PASS oracles" counts checks that expect a diagnostic or feedback versus checks that expect a clean or quiet result.

| Family | Pass/Total | FAIL / PASS oracles |
|---|---:|---:|
| checker: ProjectReference | 13/13 | 10 / 3 |
| checker: PackageReference | 17/17 | 11 / 6 |
| checker: PackageVersion | 18/18 | 13 / 5 |
| `projectReferences()` | 11/11 | — |
| hook: actual-state quote parity | 24/24 | 14 / 10 |
| hook: double-quoted output = iteration 1 | 9/9 | — |
| regression: preserved hook behavior | 20/20 | — |
| static and preservation | 13/13 | — |
| **Total** | **125/125** | |

**What fired, by family**

- **checker: ProjectReference**
  - The direction error fired with exit 1 in the double-quoted, single-quoted, mixed, reversed-order with whitespace and backslashes, and paired forms.
  - A missing target gave the existence error and a notice.
  - The legal Api→Domain reference gave exit 0 with 0 findings.
  - Three malformed forms each gave exactly one malformed error and no direction error.
  - The restored repository scan was clean.
- **checker: PackageReference**
  - Both deprecated Polly packages were flagged in the single-quoted, mixed, reversed-order and whitespace/newline forms.
  - The inline `Version` attribute and the `<Version>` child each gave an error naming `Serilog.AspNetCore`.
  - The `VersionOverride` and MediatR notices fired.
  - A non-deprecated package gave exit 0.
  - A malformed tag gave the malformed error without guessing a deprecated name.
- **checker: PackageVersion**
  - Floating `*`, range and empty versions each gave an error in the single-quoted, mixed, reversed-order and whitespace forms.
  - A pinned version gave exit 0 with 0 findings.
  - The prerelease notice and the deprecated-name error fired.
  - A mixed three-entry file gave exactly 1 error and 1 notice.
  - A malformed tag gave the malformed error.
- **`projectReferences()`**
  - Four double-/single-quoted pairs return identical targets.
  - Double-quoted results equal iteration 1.
  - Malformed input returns `[]`.
  - The exports are unchanged.
- **hook: double-quoted output = iteration 1**: steps s0–s8 below, run with double-quoted manifests, produce output identical to the iteration-1 hook and checker (root path normalized).

**Checker cross-checks**

- Every single-quoted, mixed or reordered fixture must give findings identical to its double-quoted twin (25 comparisons).
- Every valid double-quoted fixture must give findings identical to the iteration-1 checker (16 comparisons).
- 10 fixtures were also re-run in default repository-scan mode.

**Hook quote-parity sequence** (each quote style)

| Step | Action | Expected result |
|---|---|---|
| s0 | clean first observation (Bash) | quiet |
| s1 | unchanged state (PowerShell) | quiet |
| s2 | Bash adds a forbidden Domain→Api reference | `decision: block` with the direction error and the Reserved graph-change message |
| s3 | unchanged repeat | quiet |
| s4 | PowerShell removes the reference | graph change only |
| s5 | PowerShell adds a **legal** Api→Domain reference | Reserved graph change, no direction error |
| s6 | Bash fails (`exit 3`) after a partial change | `PostToolUseFailure` `additionalContext` with the direction error and the graph change |
| s7 | Bash fails with no relevant change | quiet |
| s8 | PowerShell fails (`exit 5`) after writing an Application→Api reference as UTF-16LE | `PostToolUseFailure` feedback |
| s9 | rewrite in the other quote style, same target | quiet: equivalent references, no false Reserved reminder |
| s10 | Bash renames the Api project | move reported, plus the dangling single-quoted references of Domain and Application |

The Edit-tool path was also tested in both styles: direction error and graph change.

**Preserved hook behavior** (regression family)

- PreToolUse:
  - a reference command with spaces in a path → deny;
  - `npm --prefix … --force` → deny;
  - `git -C … status` → silent;
  - `git -C . add -A` → ask;
  - empty input → deny;
  - BOM-prefixed input → parsed.
- A fresh state followed by a first shell HEAD transition to a committed single-quoted Domain→Api manifest → detected. Later HEAD transitions in both directions → detected.
- A `package.json` with a floating version → detected; `node_modules` → quiet.
- A tracked deletion → reported, with the dangling reference.
- A linked worktree (nested cwd, launcher in another checkout) is checked in place, and the main checkout stays quiet.
- The Stop five-state sequence passes.

**Static and preservation checks**

- `node --check` passes on all 4 `.cjs` files.
- PreToolUse keeps `onFailure: "block"`, and the Bash|PowerShell `PostToolUseFailure` registration is present.
- The register has exactly D-01…D-18.
- `check-instructions` on `output/template`: 60 artifacts, 0 errors, always-loaded surface ≈ 19,738 characters (≈ 4,935 tokens).
- The default `check-dependencies` scan on `output/template`: 0 errors, 0 notices.
- 63 files with the same paths as iteration 1.
- Only `check-dependencies.cjs` differs from iteration 1, and its ENF header is unchanged.

### Preservation and K0 identity

- **Changed runtime files: 1** — `.claude/scripts/check-dependencies.cjs`. No file was added or removed.
- The other 62 files are byte-identical to iteration 1, including every rule, skill and agent, `MAP.md`, `CLAUDE.md`, the register, `settings.json`, `hook.cjs`, `repo.cjs` and `check-instructions.cjs`.
- Unchanged by this pass:
  - policy text;
  - the Kind × Scope design: 7 Kinds, 6 Scopes;
  - loading;
  - the conformance relation;
  - the 18-entry DEC register;
  - all 196 policies (194 + GOV-017/GOV-018) with their owner, trigger and minimum-scope assignments;
  - the always-loaded surface (19,738 characters);
  - the 63-file topology.
- `source/inventory.json` assigns no policy to `check-dependencies.cjs`.
- Not re-run, because their tooling was deleted and every file they examine is byte-identical:
  - the 196-policy owner map;
  - the D11 Kind-direction fixtures.

  `check-instructions` passes on the final template.
- Immutable inputs: all 121 entries of the root `MANIFEST.sha256` verify, so `baseline/`, `source/`, `audit/` and the root files are untouched.

### Hashes

Same recipe as iteration 1: `find . -type f -print0 | sort -z | xargs -0 sha256sum -b | sha256sum`, run inside `output/template`.

| | Tree hash | Files | Bytes |
|---|---|---:|---:|
| Initial (iteration 1, verified once) | `51105bf425561a167dfda0bce08314c9f1fa84ef4a71be85bc9a26892ce08022` | 63 | 366,543 |
| **Final** | **`9cafc557ccdeca48499946fec6c3b6876de36a69b4c48d3a4fe86d78c7db5a03`** | 63 | 368,812 |

`check-dependencies.cjs` (`sha256sum -b`):

- before: `1ef1843241a0d362caaaccb663da9189493c9c854ec4336d22c785e329cfd01a`;
- after: `2a14aa061c2daf224843190038869f58610824a953b362dd8b2ab1aa37be7942`.

### Remaining limitations

None of these is a quote-parity issue; all are unchanged from iteration 1 unless noted.

- XML comments are scanned like element text, as before, so a commented-out element is checked as if active. New in this pass: comment prose that resembles an incomplete start tag of `ProjectReference`, `PackageReference` or `PackageVersion` is now reported as malformed rather than ignored.
- Attribute values are not entity-decoded.
- Attribute and element names are case-sensitive.
- A `PackageVersion` without a `Version` attribute, or with a `<Version>` child, is not version-checked.
- There is no MSBuild evaluation: Conditions, imports and `Update` items are not evaluated.
- Live Claude Code hook execution was not observed again. Host semantics are relied on as in iteration 1.

### Workspace events

- One probe briefly wrote a fixture `.csproj` to the shell temp directory (`/tmp`) instead of `output/.work/`. It was deleted immediately and contained only test XML.
- After this report was written, `output/.work/` (harness, logs, snapshot, sandboxes) was deleted. The final check confirms that `output/` contains exactly `template/` and `REFINEMENT_REPORT.md`.
