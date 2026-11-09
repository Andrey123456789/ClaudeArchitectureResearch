# Independent Audit Evidence — K1

This evidence was produced independently of the generated `GENERATION_REPORT.md` files.

## Frozen-input equality

Both raw runs have identical:

- `CANDIDATE.md` SHA-256: `4c898fc26a300c04ba5948e755447146e7883b5f126b52624c173b0a53bc7a9c`;
- `TASK.md` SHA-256: `579b723fde56866f0f8dcc30a619ad6abae8579622c0af102054604baef81a5c`;
- source-tree hash (path + content): `abf6f1a02a5b95128badc4d0eabe928dda5fe34f501ac7cb3adb33244c2a060a`.

## Runtime corpus

Run-01:

- 84 files;
- 373,146 bytes;
- 67 Markdown files;
- 18 rule files;
- 28 SKILL.md entry points;
- generated always-loaded estimate ~5,315 tokens.

Run-02:

- 85 files;
- 346,715 bytes;
- 72 Markdown files;
- 21 rule files;
- 30 SKILL.md entry points;
- generated always-loaded estimate ~4,849 tokens.

## Syntax / generated-checker baseline

- all 8 Run-01 JS/MJS files parse with `node --check`;
- all 9 Run-02 JS/CJS files parse with `node --check`;
- all JSON files parse;
- both generated instruction checkers report PASS on their raw template;
- Run-01 architecture and manifest checks report PASS on the empty scaffold;
- Run-02 manifest check reports PASS on the empty scaffold.

## Path/topology variance

- common runtime paths: 62;
- union runtime paths: 107;
- whole-tree path Jaccard: ~0.57944;
- skill-name Jaccard: 28/30 = ~0.93333;
- rule-path Jaccard: 13/26 = 0.50000;
- capability-file Jaccard: 8/12 = ~0.66667.

## Lexical diagnostics

TF-IDF best-match diagnostics (not correctness metrics):

Normalized 194-policy oracle:

- Run-01 mean ~0.41461, 19 below 0.25;
- Run-02 mean ~0.41501, 17 below 0.25.

640 V2 Markdown sections:

- Run-01 mean ~0.46299, 110 below 0.25;
- Run-02 mean ~0.47878, 89 below 0.25.

## K dependency mutation

Mutation: add a DEC conformance reference from the decision register to `.claude/rules/backend/coding-style.md` (STD).

- Run-01 `check-instructions.mjs`: PASS.
- Run-02 `check-instructions.cjs`: FAIL with `DEC must not depend on STD ...`.

This materially favors Run-02 as the K1 refinement baseline.

## K1 Binds mutation

Mutation in Run-02:

- change persistence/ef-core `- Binds: architecture ...` to `- Binds: —`.

Result:

- Run-02 `check-instructions.cjs`: PASS (0 errors, 0 warnings).

This confirms missing mechanical enforcement of current leaf->frame binding obligations.

## Command-classifier tests — Run-02

Detected:

- `npm install x` (unversioned package);
- `dotnet add Foo.Api.csproj package Serilog` (unversioned package);
- force/legacy-peer flags even in several global-option forms.

Missed:

- `npm uninstall x`;
- `npm remove x`;
- `npm --prefix frontend install x`;
- `npm --workspace app install x`;
- `pnpm --dir frontend add x`;
- `yarn --cwd frontend add x`;
- `dotnet remove Foo.Api.csproj package Serilog`;
- `dotnet add Foo.Api.csproj reference Foo.Domain.csproj`;
- `dotnet remove Foo.Api.csproj reference Foo.Domain.csproj`.

## BOM test

Exact configured PreToolUse commands were fed identical UTF-8 JSON with a UTF-8 BOM prefix.

- Run-01: exit 0 for an unrelated command.
- Run-02: exit 1, `Unexpected token U+FEFF`.

## Real worktree test — Run-02

A real Git worktree contained a `.csproj` with an inline PackageReference Version forbidden under Central Package Management.

Direct worktree checker:

- exit 1;
- correctly reports the inline version error.

Exact Run-02 PostToolUse hook with:

- `CLAUDE_PROJECT_DIR = main checkout`;
- input `cwd = worktree`;
- edited `file_path = worktree/...csproj`;

result:

- exit 0;
- no stdout;
- no stderr.

The violation was missed.

## Real worktree comparison — Run-01

The equivalent Run-01 PostToolUse test launched from the worktree found the worktree's `.claude` tree and returned the expected manifest/architecture violation feedback.

This proves active-worktree correctness is feasible within the K1 design.

## Stop fingerprint test — Run-02

1. Modify one backend production `.cs` file without tests: `check-cochange(..., "hook")` returns the tests reminder.
2. Change the **same file path** again to materially different content, still without tests.
3. Second hook-mode call returns no reminder.

The current fingerprint uses path set + reminder IDs, not material working-tree content/change identity.

## Settings coverage inspection — Run-02

- PreToolUse: `Bash|PowerShell`.
- PostToolUse: `Edit|Write|MultiEdit` only.
- Stop: configured.
- critical PreToolUse handler has no `onFailure: "block"`.

Therefore shell-driven manifest/reference changes need explicit deterministic post-change coverage and the critical guard needs fail-closed behavior.
