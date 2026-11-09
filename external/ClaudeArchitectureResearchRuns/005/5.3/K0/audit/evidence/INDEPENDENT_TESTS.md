# Independent Audit Evidence — K0

This file records checks performed independently of the generated `GENERATION_REPORT.md` files.

## Frozen-input equivalence

Run-01 and Run-02 have identical:

- `TASK.md`;
- `CANDIDATE.md`;
- `inventory.json`;
- `shared-research-invariants.json`;
- V2 source tree.

## Runtime size / topology

- Run-01: 66 files, 356,264 bytes, 56 Markdown files, 15 STD rules, 29 skills.
- Run-02: 62 files, 324,363 bytes, 55 Markdown files, 14 STD rules, 29 skills.
- common paths: 55;
- union paths: 73;
- whole-tree Jaccard: 0.753;
- rule-path Jaccard: 0.611;
- skill-name Jaccard: 1.000;
- only `SPECIFICATION.md` is byte-identical among common runtime paths.

Both contain no structural `Level:` hierarchy and no capability contract/module/slot files.

## Generated checkers and syntax

Independent execution:

- Run-01 `check-instructions`: 0 errors, 0 warnings; generated estimate ~5363 always-loaded tokens.
- Run-01 manifest checker: no findings.
- Run-02 `check-instructions`: 0 errors; generated estimate ~4931 always-loaded tokens.
- Run-02 dependency checker: 0 errors/notices on the template baseline.
- all `.mjs` / `.cjs` files in both templates pass `node --check`.

These PASS results are not treated as proof of correctness; the behavioral failures below bypass them.

## Lexical fidelity diagnostics

Diagnostics only, not acceptance metrics:

194 normalized inventory policies -> generated Markdown best TF-IDF match:

- Run-01 mean ~0.3898, 33 below 0.25;
- Run-02 mean ~0.3905, 29 below 0.25.

602 extracted V2 Markdown sections -> generated Markdown best TF-IDF match:

- Run-01 mean ~0.5174, 55 below 0.25;
- Run-02 mean ~0.4294, 123 below 0.25.

This supports selecting Run-02 for compactness while requiring a fresh V2 technique review.

## Run-01 nested-cwd launcher reproduction

Configured Run-01 hook command:

`node .claude/hooks/pre-command-guard.mjs`

From a nested directory, Node fails with `MODULE_NOT_FOUND` before the hook's own root resolver can execute.

This is a major reason not to choose Run-01 as the 5.3 baseline despite several stronger classifier details.

## Run-02 active-worktree reproduction

A real Git repository and linked worktree were created.

The worktree received an invalid `.csproj` containing an inline `PackageReference Version`.

PostToolUse was invoked with:

- `CLAUDE_PROJECT_DIR` = main checkout;
- input `cwd` = worktree;
- `tool_input.file_path` = invalid worktree `.csproj`.

Result:

- hook: exit 0, no output;
- direct worktree dependency checker: exit 1 with the expected inline-version error.

Thus Run-02 enforces the main checkout rather than the active worktree in this scenario.

## Run-02 dependency classifier reproduction

Detected:

- `npm install x`;
- `dotnet add Foo.Api.csproj package Serilog`;
- `npm update x`;
- `pnpm update x`;
- `yarn up x`.

Missed:

- `npm uninstall x`;
- `npm remove x`;
- `pnpm remove x`;
- `yarn remove x`;
- `dotnet remove Foo.csproj package X`;
- `dotnet package remove X`;
- `npm --prefix frontend install x --force`;
- `npm --workspace app install x --legacy-peer-deps`;
- `pnpm --dir frontend add x --force`;
- `yarn --cwd frontend add x --force`;
- `dotnet add Foo.Api.csproj reference Foo.Domain.csproj`;
- `dotnet remove Foo.Api.csproj reference Foo.Domain.csproj`.

Run-01 detects the tested package removal and global-option cases but also misses dotnet project-reference mutation.

## Run-02 BOM reproduction

BOM-prefixed hook JSON causes:

`hook input is not valid JSON: Unexpected token U+FEFF`

because `raw.trim()` is used only for the empty check while `JSON.parse(raw)` parses the untrimmed string.

## Run-02 Stop fingerprint reproduction

First change to a production file without test changes:

- Stop returns the expected blocking reminder.

The same path is then modified again with different content while the changed-path set remains the same:

- Stop returns no reminder.

The fingerprint therefore suppresses a materially new state when only content changes.

## Run-02 checker / modern hook serialization

A temporary copy of `settings.json` was changed to the current exec form:

- `command: "node"`;
- `args: ["${CLAUDE_PROJECT_DIR}/.claude/hooks/hook.cjs", <event>]`.

The generated instruction checker reports three errors saying the hooks do not use its expected shared launcher. The checker validates the baseline's string serialization, not the required runtime property.

## Git enforcement inspection

The Run-02 map claims Git `ask` permissions cover repository-changing Git commands, but the explicit settings list omits multiple representative state-changing forms such as `git add`, `git rm`, `git mv`, `git switch`, `git apply`, `git am`, and `git update-ref`.

Run-01 independently contains a substantially broader read-only-vs-mutating Git classifier, demonstrating that K0 can enforce the policy more completely without changing candidate identity.

## K0 checker dependency-direction inspection

Run-02's instruction checker collects non-routing conformance edges and checks them for cycles. It does not compare source/target Kinds against the binding K0 direction from `CANDIDATE.md`.

An acyclic but directionally invalid mutation therefore is not mechanically ruled out by this predicate. Refinement must add direction-aware mutation tests.
