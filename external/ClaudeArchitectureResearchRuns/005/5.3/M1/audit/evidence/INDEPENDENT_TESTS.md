# Independent audit evidence

This file records checks performed outside the generated `GENERATION_REPORT.md` claims.

## Generated checkers

Run-01:

```text
Instruction structure: 0 error(s), 0 warning(s)
always-loaded ≈ 5640 tokens
Architecture: 0 errors
Dependencies: 0 errors
```

Run-02:

```text
check-instructions: 65 instruction files, always-loaded ~5568 tokens, 0 errors, 0 warnings
check-architecture: 0 errors
check-manifests: 0 errors
```

All generated `.js` / `.mjs` files passed `node --check`.

## File-tree comparison

```text
Run-01: 77 files, 397827 bytes, 65 md / 347952 md bytes, 14 rules, 28 skills
Run-02: 80 files, 368816 bytes, 67 md / 303524 md bytes, 14 rules, 29 skills
Common paths: 63
Union paths: 94
Jaccard: 0.6702127659574468
```

## Dependency command classifier probes (Run-02)

```text
npm install x                                  -> detected
npm --prefix frontend install x                -> missed
npm --workspace app install x                  -> missed
pnpm add x                                     -> detected
pnpm --dir frontend add x                      -> missed
yarn add x                                     -> detected
yarn --cwd frontend add x                      -> missed
dotnet add Foo.Api.csproj package X            -> detected
dotnet add Foo.Api.csproj reference Foo.Domain.csproj    -> not pre-routed; post-manifest classification true
dotnet remove Foo.Api.csproj reference Foo.Domain.csproj -> not pre-routed; post-manifest classification true
```

## Nested-cwd launch probe

Run-01 root-relative launcher (`node .claude/hooks/post-tool-use.mjs`) was invoked from an unrelated nested cwd and failed with Node `MODULE_NOT_FOUND` before hook logic could run.

Run-02's script itself can be bootstrapped by absolute/project-root location, but this does not solve active-worktree targeting.

## Actual Git-worktree probe

A temporary main checkout and real Git worktree were created from R2. An invalid `.csproj` containing a direct floating `PackageReference Version="*"` existed only in the worktree.

Hook input:

- `CLAUDE_PROJECT_DIR = <main checkout>`
- JSON `cwd = <worktree>`
- `Write` file path = invalid worktree `.csproj`

Result:

```text
R2 worktree hook: status 0, no stdout, no stderr — invalid manifest missed.
```

The same invalid file placed in the main checkout produced a blocking manifest finding. This isolates the defect to wrong-root/worktree handling rather than checker incapability.

The analogous Run-01 test also returned status 0/no finding when `CLAUDE_PROJECT_DIR` pointed at main and JSON `cwd` pointed at the worktree.

## Lexical diagnostics

These are diagnostics, not correctness metrics.

Policy normalized-text TF-IDF best-match means:

- Run-01 ≈ 0.491
- Run-02 ≈ 0.489

No material normative-policy advantage is visible from this diagnostic.

Exact literal V2 preservation:

- unique baseline headings retained exactly: R1 ~92.0%, R2 ~71.6%;
- unique baseline code blocks retained exactly: R1 ~79.3%, R2 ~42.5%.

This motivates Q1 in the defect dossier but does not justify copying R1 wholesale.
