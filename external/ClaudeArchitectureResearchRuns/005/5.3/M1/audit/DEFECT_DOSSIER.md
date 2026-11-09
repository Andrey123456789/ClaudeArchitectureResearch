# M1 Run-02 defect dossier for 5.3

All items marked **CONFIRMED** must be resolved by the refinement. Items marked **QUALITY GATE** require an explicit review/result but do not force gratuitous rewriting.

## D1 — active worktree checks use the wrong root — CRITICAL — CONFIRMED

### Evidence

R2 `.claude/scripts/lib/common.js` defines a static `ROOT` from the script location. The hook scripts therefore inspect the main checkout even when Claude has entered another worktree.

An independent Git-worktree simulation was run:

- the hook script existed in the main checkout;
- an invalid `.csproj` was created only in the worktree;
- `CLAUDE_PROJECT_DIR` pointed at main, while hook JSON `cwd` pointed at the worktree;
- R2 PostToolUse returned status 0 with no output and missed the invalid manifest;
- placing the same invalid manifest in the main checkout caused the same hook to block it correctly.

Run-01 has the same conceptual defect because its root resolver checks `CLAUDE_PROJECT_DIR` before hook-input `cwd`.

### Required repair

Separate:

- **launcher root**: where hook scripts are located;
- **active repository/worktree root**: where repository policy/checks apply.

Parse hook JSON first. Derive active repository/worktree root from `input.cwd` (e.g. Git top-level from that cwd), without silently falling back to the original checkout when Claude is in a worktree. All path conversion, manifest walking, architecture checks, Git status, stop-hook state, and changed-file checks must operate on the active root.

Add deterministic tests using an actual in-workspace Git worktree and a nested cwd.

## D2 — hook launch configuration should use robust exec form — HIGH — CONFIRMED QUALITY/PORTABILITY DEFECT

R2 currently embeds a shell-form expression:

```text
node -e "require(require('path').resolve(process.env.CLAUDE_PROJECT_DIR || '.', ...))"
```

Current Claude Code supports and recommends exec form for path placeholders.

### Required repair

Use a cross-platform launcher equivalent to:

```json
"command": "node",
"args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.js"]
```

Preserve Windows compatibility. Add tests that settings commands are structurally valid and that hooks launch from project root, nested cwd, paths containing spaces, and active worktree scenarios.

## D3 — dependency command parser misses package-manager global options — HIGH — CONFIRMED

Independent tests against R2 `dependency-commands.js`:

```text
npm install x                    -> detected
npm --prefix frontend install x  -> NOT detected
npm --workspace app install x    -> NOT detected
pnpm add x                       -> detected
pnpm --dir frontend add x        -> NOT detected
yarn add x                       -> detected
yarn --cwd frontend add x        -> NOT detected
```

For the missed commands, `changesManifests()` also returns false.

### Required repair

Parse normal npm/pnpm/yarn global options (including options that consume a value) before identifying the subcommand. At minimum cover realistic `--prefix`, `--workspace`, `--dir`, `--filter`, and `--cwd` placements without generating broad false positives.

Use table-driven positive and negative tests. The same parser/classifier should drive PreToolUse routing and post-change manifest detection wherever practical, so the two phases cannot silently disagree.

## D4 — `dotnet add/remove ... reference` is not routed before mutation — HIGH — CONFIRMED

Independent tests:

```text
dotnet add Foo.Api.csproj reference Foo.Domain.csproj    -> analyzeCommand block=false; changesManifests=true
dotnet remove Foo.Api.csproj reference Foo.Domain.csproj -> analyzeCommand block=false; changesManifests=true
```

The graph mutation can happen before the architecture/project-reference decision boundary is enforced.

### Required repair

Classify `dotnet add/remove <project> reference <project>` before mutation and route it to the correct existing owner. Do **not** falsely treat a project reference as a NuGet package. Preserve M1/M policy ownership: this is a project-reference / architecture-boundary change and must use the appropriate decision/project-structure procedure and post-change architecture validation.

Add positive/negative tests for both add and remove, with and without explicit project operands.

## D5 — the generated instruction checker is coupled to the current launcher shape — HIGH — CONFIRMED BY DESIGN INSPECTION

The checker validates the existing shell-form command representation. A correct D2 migration to `command + args` must not cause the checker to reject or fail to validate the improved configuration.

### Required repair

Update checker/settings validation to understand the actual Claude Code hook schema used by the template, including exec-form `args`, script existence, expected event/matcher coverage, critical `onFailure` behavior, and cross-platform path placeholders.

## D6 — manual checker commands are cwd-sensitive — MEDIUM — CONFIRMED

Multiple workflows/MAP instructions use commands such as:

```text
node .claude/scripts/check-instructions.js
```

After Claude changes into a nested directory or worktree subdirectory, these commands can resolve incorrectly.

### Required repair

Make manual verification instructions explicitly operate from the active repository/worktree root, or provide an equivalently robust cross-platform invocation. Do not reintroduce dependence on the original checkout when an active worktree exists.

## D7 — Stop-hook dedup fingerprint does not represent actual changed state — MEDIUM — CONFIRMED

R2 fingerprints only:

```text
{ files, messages }
```

If file contents change again while the same set of files yields the same reminder text, the previous fingerprint can suppress a legitimate later reminder. `stop_hook_active` already prevents the immediate feedback loop.

### Required repair

Fingerprint the relevant actual repository/change state (for example a deterministic hash of status plus relevant diffs/content identity), not only file names/messages. Preserve no-loop behavior for unchanged state, but allow a materially changed state with the same file set to trigger again.

Keep state worktree-aware; do not cause one worktree's state to suppress another's.

## D8 — critical PreToolUse enforcement fails open on hook crash — HIGH — CONFIRMED AGAINST CURRENT CLAUDE CODE MECHANICS

R2's helper reports internal hook failures with exit 1. Current Claude Code documents most hook failures as non-blocking unless `onFailure: "block"` is configured.

### Required repair

For critical **PreToolUse** policy enforcement, configure fail-closed behavior using current supported mechanics (`onFailure: "block"`) and verify the checker recognizes it. Do not indiscriminately apply this to events where it is meaningless or harmful. Test a deliberately missing/crashing pre-hook and prove the protected tool call is blocked.

## Q1 — targeted V2-fidelity review — QUALITY GATE

R1 preserves much more V2 wording/examples literally than R2. This is not proof that R2 lost semantics, but it is enough to require a targeted review.

Compare every V2 baseline section/code example against R2. Restore **materially useful** technique, examples, edge cases, or instructions that R2 actually omitted. Do not restore duplicated policy or bulk text merely to improve lexical similarity.

Acceptance: no useful V2 technique is lost, while R2 remains at least as concise where paraphrase carries the same semantic content.

## Q2 — reduce avoidable persistence-to-frame coupling — QUALITY GATE

R2 persistence declares `binds` to `architecture/clean-architecture` because examples, migration commands, and co-change patterns use frame project/directory names. R1 demonstrated that stable role tokens can express more of this without a declared bind.

Try to replace avoidable frame-specific names with stable architecture-role vocabulary. Retain an explicit `binds` entry where concrete executable guidance genuinely requires frame-specific placement; do not remove it just to make a metric look better.

## Q3 — keep M1 minimal outside capability boundaries — QUALITY GATE

R2 has four always-loaded capability planning facets and ~5.57k estimated always-loaded tokens. This is acceptable because the TASK makes reliability higher priority than the ~5k target, but refinement must not add more capability/meta layers or increase always-loaded context without a concrete reliability need.

## Mandatory final regression gates

The refined result must prove:

- 194 inventory policies + 2 shared invariants still covered;
- trigger-role delta count = 0;
- minimum-scope gaps = 0;
- unresolved references = 0;
- exactly four M1 slots; no extra slots;
- no `Level:` / Stability-first hierarchy;
- no `Kind:` / Kinds × Scopes organization;
- static composition only;
- flat M-style topical rules remain primary outside capability metadata;
- selected implementation leak checks pass;
- optional frontend disable/enable mechanics remain deterministic and non-hunting;
- active worktree and nested-cwd tests pass;
- Windows-compatible launcher tests pass;
- package/project-reference command routing tests pass;
- PreToolUse fail-closed failure test passes;
- Stop hook does not loop on unchanged state and re-triggers after relevant content changes;
- no research-only metadata leaks into `output/template/`;
- `SPECIFICATION.md` stays product input, not instruction content;
- technical output remains English;
- no unjustified increase in always-loaded context, total files, or maintenance layers.
