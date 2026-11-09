# Independent Audit Evidence — L1

This document records checks performed independently of the generated `GENERATION_REPORT.md`.

## Static/runtime checks

Both raw templates:

- JavaScript modules parse successfully with `node --check`;
- generated instruction checker reports PASS;
- generated architecture checker runs;
- expose exactly four capability implementations;
- retain the stability-first level hierarchy.

## Structural variance

- Run-01 runtime files: 96; bytes: 340,449.
- Run-02 runtime files: 85; bytes: 298,925.
- common runtime paths: 58.
- union runtime paths: 123.
- path Jaccard: ~0.472.
- skill-name Jaccard: 0.900.
- both select the same four capability implementations.

## Independent policy/V2 lexical diagnostics

These are diagnostics, not correctness metrics.

194 normalized inventory policies were compared against generated Markdown paragraphs with TF-IDF best-match similarity:

- Run-01 mean best match: ~0.434.
- Run-02 mean best match: ~0.394.

618 Markdown sections extracted from the frozen V2 baseline were compared against generated Markdown paragraphs:

- Run-01 mean best match: ~0.460; sections below 0.25: 103.
- Run-02 mean best match: ~0.401; sections below 0.25: 161.

This supports a mandatory V2-fidelity review for the more compressed Run-02 baseline; it does not establish missing semantics by itself.

## Candidate-conformance finding: technology neutrality

Both generated checkers report PASS while actual Level 0/1 content contains concrete technology implementation vocabulary.

Run-02 confirmed examples:

- Core HTTP: `IExceptionHandler`;
- Core security: ASP.NET Core authentication / Identity / Data Protection;
- Core testing: `WebApplicationFactory`;
- Architecture roles: `IActionResult` / ASP.NET Core;
- architecture frame: ASP.NET Core Controllers.

Run-01 contains the same class of defect.

This is a systematic raw-generation failure, not a one-run anomaly.

## Hook launcher test — Run-02

Exact configured command:

`node .claude/hooks/pre-bash-dependency.mjs`

When launched from a nested directory, Node fails before hook code runs with `MODULE_NOT_FOUND` under `<nested>/.claude/hooks/...`.

Therefore normal `cd` can disable the current hook entry point.

## Hook-input BOM — comparison

Run-02 hook input parsing succeeded with UTF-8 BOM-prefixed JSON.

Run-01's CJS hook input parser failed on the same input (`Unexpected token U+FEFF`).

This is one reason Run-02 is the better baseline.

## Dependency-command behavioral tests — Run-02

Detected:

- `npm install x`;
- `dotnet add Foo.Api.csproj package Serilog`.

Missed:

- `npm --prefix frontend install x --force`;
- `npm --workspace app install x --legacy-peer-deps`;
- `pnpm --dir frontend add x --force`;
- `yarn --cwd frontend add x --force`;
- `dotnet add Foo.Api.csproj reference Foo.Domain.csproj`;
- `dotnet remove Foo.Api.csproj reference Foo.Domain.csproj`.

## PostToolUse coverage

Run-02 settings use `PostToolUse matcher = Edit|Write|MultiEdit`.

Therefore Bash/PowerShell-driven changes to package/project manifests do not invoke the manifest post-check through this handler.

## Checker self-consistency

The Run-02 instruction checker accepts only hook commands shaped like `node <script>.mjs` and rejects `$`.

That serialization rule conflicts with the current robust exec-form pattern needed to repair nested-cwd launching.

The checker must be corrected together with the hook settings.
