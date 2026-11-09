# M Run-02 — Independent defect dossier for 5.3

This dossier is binding input to refinement. `GENERATION_REPORT.md` is evidence, not authority: every item below was identified independently against the generated files and current Claude Code hook mechanics.

## Confirmed defects — must be fixed

### D1 — Hook launch commands are current-working-directory dependent

**Severity: High**

`.claude/settings.json` launches hooks with shell-form relative commands such as:

- `node .claude/hooks/dependency-guard.mjs`
- `node .claude/hooks/file-change.mjs`
- `node .claude/hooks/stop-co-change.mjs`

These fail when the current directory is a nested project directory because Node resolves `.claude/...` relative to the current working directory before the script can run.

**Required correction:** use the current Claude Code cross-platform exec-form hook configuration: executable `node` plus an `args` array whose script path is rooted through the platform placeholder `${CLAUDE_PROJECT_DIR}`. Do not replace this with POSIX shell-variable syntax.

### D2 — Hook logic confuses the stable launcher root with the active worktree/repository root

**Severity: High**

The shared helper prefers `process.env.CLAUDE_PROJECT_DIR` as `projectRoot`. In Claude Code, the project-directory placeholder is useful for locating project-installed hook scripts, but the hook input `cwd` can point at a different active working tree/subdirectory. Using the launcher root as the repository-state root can make checks inspect the main checkout rather than the active worktree, make repository-relative path conversion fail, and make Stop checks observe the wrong Git state.

**Required correction:** separate two concepts:

1. **launcher/template root** — only for locating the installed hook script;
2. **active repository/worktree root** — derive after reading hook stdin, starting from `input.cwd`, preferably with a validated `git -C <cwd> rev-parse --show-toplevel` or an equally deterministic cross-platform approach. Fail clearly when a required repository root cannot be established.

All manifest/path/Git-state checks must operate on the active repository/worktree root.

### D3 — Project-reference CLI changes bypass dependency enforcement

**Severity: High/Medium**

The dependency guard detects NuGet package operations but misses project-reference changes such as:

`dotnet add backend/Foo.Api/Foo.Api.csproj reference backend/Foo.Domain/Foo.Domain.csproj`

This can alter `.csproj` project references without routing/checking the architecture/project-reference constraints required by the shared task.

**Required correction:** detect supported `dotnet` project-reference add/remove command forms, route them to the correct M-owned architecture/dependency guidance, and validate manifests/project references after the change. Do not misclassify a project reference as a NuGet package operation.

### D4 — npm global options can bypass dependency/force detection

**Severity: High/Medium**

The current npm command parser assumes the first non-dash argument is the npm subcommand. Global options with values can therefore hide `install` and bypass forbidden force flags. Examples that must not bypass enforcement include:

- `npm --prefix frontend install x --force`
- `npm --workspace app install x --legacy-peer-deps`

**Required correction:** parse the npm command sufficiently to skip known global options and their values, then detect the real dependency subcommand and forbidden flags. Prefer a small deterministic/table-driven parser over a fragile full shell parser.

### D5 — The instruction checker rejects the correct exec-form hook repair

**Severity: High**

`check-instructions.mjs` currently assumes each hook is one shell command string beginning with `node <script>.mjs`, and broadly rejects `$`/`%`. That would reject the cross-platform exec-form configuration required to fix D1.

**Required correction:** update static validation to accept and preferably require the supported exec-form shape for project-installed Node hooks:

- executable/command: `node`;
- args array containing `${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.mjs`;
- referenced script must exist after resolving the placeholder to the template root for static checking.

Continue rejecting shell-dependent or ambiguous launcher forms.

### D6 — Manual checker commands are root-relative without an explicit root precondition

**Severity: Medium**

Several workflows/MAP instructions invoke commands like `node .claude/scripts/...`. They fail after `cd` into a nested directory unless the model returns to the repository root first.

**Required correction:** workflows must explicitly establish the active repository/worktree root before invoking root-relative project checkers (or use an equally robust cross-platform invocation strategy). Keep commands Windows-safe and avoid POSIX-only shell assumptions.

## Regression-sensitive areas — must remain correct

The refinement must preserve or improve all of the following:

- all normalized inventory policies plus both shared invariants have exactly one normative owner;
- zero trigger-role deltas;
- minimum scope preserved;
- flat M rule organization with explicit `paths`;
- no Stability/Level, Kinds/Scopes/Kind, or capability architecture leakage;
- no shared policy moved into a private skill reference;
- workflow/knowledge distinction remains clean;
- internal references resolve;
- Windows compatibility, including PowerShell 5.1 BOM-tolerant hook stdin;
- useful V2 detail restored in Run-02 remains present;
- research metadata does not enter runtime artifacts;
- always-loaded context stays near the ~5k target unless a small increase is required for reliability;
- no gratuitous files or layers.

## Optional improvements — adopt only if demonstrably net-positive

These are ideas visible in Run-01, not mandatory defects in Run-02:

1. a deterministic source-level architecture checker;
2. destructive-Git confirmation/guarding;
3. targeted automatic instruction-structure checking after instruction edits.

Do **not** add them merely because Run-01 had them. Add only if the resulting behavior is reliable, low-noise, maintainable, M-compatible, and improves the baseline under the promotion gate.

## Required regression tests for the repaired hooks/checkers

At minimum, prove all of these in an in-workspace sandbox:

1. hook launch succeeds from repository root;
2. hook launch succeeds from a nested current directory;
3. hook launch works in Windows-safe exec form;
4. PowerShell 5.1 BOM-prefixed stdin remains accepted;
5. active worktree/repository root is derived from hook `cwd`, not silently from the main-checkout launcher root;
6. `dotnet add ... reference ...` is detected;
7. corresponding project-reference removal is detected;
8. normal `npm install` dependency changes are detected;
9. `npm --prefix ... install ... --force` cannot bypass the force guard;
10. `npm --workspace ... install ... --legacy-peer-deps` cannot bypass the guard;
11. manifest/project-reference checks run against the active worktree;
12. instruction checker accepts the repaired exec-form settings and still rejects unsafe shell-form regressions.
