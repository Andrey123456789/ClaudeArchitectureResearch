# L0 5.3 — Corrective pass `iteration_after_audit_1`

## 1. Purpose and authoritative boundaries

This is **one bounded follow-up correction** to the accepted L0 controlled-refinement result (the existing `output/template/`, **71 files**). It is not a new generation from Run-02, a replacement architecture, a new evaluation phase, or a cleanup of unrelated weaknesses.

The independent re-audit found that two semantically identical XML spellings can lead to different diagnostics or different observed dependency graphs. Fix this **one root-cause class**. Preserve all previously accepted L0 behavior.

Read, in this order, before editing:

1. This task and `L0-iteration_after_audit_1-GOAL_PROMPT.txt`.
2. `CANDIDATE.md`, `audit/DEFECT_DOSSIER.md`, and the existing root `REFINEMENT_TASK.md` for L0 identity, D1–D12, and acceptance obligations.
3. Existing `output/REFINEMENT_REPORT.md`, as **historical evidence**, not as proof that the new regression cases pass.
4. **Complete** `output/template/.claude/hooks/manifest-checks.mjs`, especially `attributes`, `projectReferences`, `checkProjectFile`, `checkCentralPackages`, `checkManifestFile`, `declaredDependencies`, and `dependencyDelta`.
5. Only the relevant call paths in `output/template/.claude/hooks/claude-hook.mjs`, including shell actual-state snapshots, manifest scans, post-edit handling, `PostToolUse`, and `PostToolUseFailure`.
6. Relevant L0 rules on backend dependency direction and package management. Read source/inventory only as needed for preservation checks.

Never use older Claude iterations, previous ChatGPT audit artifacts, other candidate workspaces, chat history, outside scratch files, or external downloads as an implementation source. Make decisions from this L0 workspace's current source and the fixed contract below.

### Allowed persistent changes

- `output/template/.claude/hooks/manifest-checks.mjs` — minimal parser and affected call-site correction.
- `output/REFINEMENT_REPORT.md` — append a clearly separated `iteration_after_audit_1` section; preserve existing report history.

**Nothing else.** The other **70 template files** must remain byte-identical, including `claude-hook.mjs`, `.claude/settings.json`, the instruction checker, all level rules/skills, and `CLAUDE.md`. Never edit `baseline/`, `source/`, `audit/`, `CANDIDATE.md`, prior iteration tasks, or other root metadata. Keep L0's primary `0 Core -> 1 Architecture -> 2 Technology -> 3 Project` structure, technology-neutral Level 0/1 boundary, and embedded technology choices (no slots, Kind/Scope, capability contracts, or borrowed architecture).

All permanent code, comments, reports, test fixture names, and generated text must be **English-only**.

## 2. Reproduced defect and expected behavior

The existing module uses double-quote-specific extraction in `attributes()` and `projectReferences()`. This affects two independent responsibilities:

- **Enforcement:** `checkManifestFile()` / `scanManifests()` scan `ProjectReference`, `PackageReference`, and central `PackageVersion` declarations.
- **Change tracking:** `declaredDependencies()` feeds `dependencyDelta()` and the unchanged `claude-hook.mjs` actual-state path. An omitted dependency can make added/removed/changed files appear to have no material graph change, including after a failed shell command that partly modified a file.

Prove the defect *once* on an isolated copy of the **unmodified current** checker; do not touch authoritative files for the reproduction. Minimal paired cases:

```xml
<!-- Invalid dependency in a Domain project: reject BOTH versions. -->
<ProjectReference Include="../Demo.Api/Demo.Api.csproj" />
<ProjectReference Include='../Demo.Api/Demo.Api.csproj' />

<!-- Inline versions and denied package: reject BOTH. -->
<PackageReference Include="Microsoft.Extensions.Http.Polly" Version="9.0.0" />
<PackageReference Include='Microsoft.Extensions.Http.Polly' Version='9.0.0' />

<!-- Safe central declaration: accept BOTH (given central management is enabled). -->
<PackageVersion Include="Safe.Lib" Version="1.2.3" />
<PackageVersion Include='Safe.Lib' Version='1.2.3' />
```

The source shows that the single-quoted `ProjectReference` can be missed in both check and delta, the single-quoted `PackageReference` can evade inline-version and prohibited-package controls, and the single-quoted valid `PackageVersion` can get a false missing/empty-version diagnostic.

This is an attribute-handling defect, **not** permission to relax project-layer boundaries, package restrictions, or Central Package Management.

## 3. Implementation contract

1. Implement one **bounded, consistent attribute-reading strategy** for the XML elements the module already recognizes. It must accept both `name="value"` and `name='value'`, including mixed quote styles across different attributes, spaces around `=`, line breaks, and reordered attributes. Preserve original attribute-name case semantics unless the current documented contract explicitly requires otherwise (XML attribute names are case-sensitive).
2. Apply that strategy to **all relevant existing paths**: package and central-package scanning, `projectReferences()`, and `declaredDependencies()`; do not leave a separate double-quote-only parser in any of them. Keep the existing `Include`/`Update` handling where supported.
3. A quoted `>` or other punctuation inside an attribute must not cause an unintended cross-element match or turn an unrelated element into a valid dependency. Keep XML comments inert: commented-out dependency text must not create a finding or a dependency delta. A small local lexer/helper is acceptable; do not introduce a dependency on an XML library, full DOM parser, full MSBuild evaluator, or broad new input grammar.
4. Preserve both self-closing elements and the already-supported paired forms, including existing nested `<Version>` treatment. Preserve `VersionOverride`, floating/prerelease/empty-version diagnostics, denied/review package classification, allowed project-layer references, and existing encoding behavior. Do not replace meaningful errors with a blanket rejection or suppress checks to achieve clean fixtures.
5. `declaredDependencies()` must use the same semantics as direct checks, so quote-only rewrites of a manifest are **dependency-neutral**, while real additions/removals/version changes are detectable. If a file's content is syntactically beyond the bounded checker, document the actual limit rather than guessing that it is safe.
6. Preserve existing file discovery, generated-directory skips, nested-repository handling, case handling for package IDs and reference comparisons, and per-worktree state isolation. Do not modify the PostToolUse pipeline or its D9–D12 logic.
7. Keep the implementation small and understandable. Avoid regular-expression patches for one named package or path, unbounded fuzzing, changing policies, or modifying supporting hooks to make a test pass.

## 4. Finite independent discriminating test matrix

Use **ONE** reusable harness in `output/.work/` calling the **real final** `manifest-checks.mjs` and the unchanged hook where specified. Isolate every fixture from other fixtures and any approved exceptions. Capture exit status, relevant diagnostics, and the checked file. Ensure the expected failure is the **correct reason**, not an unrelated invalid JSON, missing configuration, or test-setup error.

### 4.1 Project references — negative and positive

Check each relevant case with both single and double quotes, then a small subset with reordered attributes, multiline formatting, and mixed quote styles:

| Case | Required result |
|---|---|
| `Demo.Domain.csproj` references `Demo.Api.csproj` | FAIL, outward reference `Domain -> Api` |
| `Demo.Domain.csproj` references `Demo.Infrastructure.csproj` | FAIL, outward reference |
| Production project references `Demo.Tests.csproj` | FAIL, production-to-test reference |
| `Demo.Application.csproj` references `Demo.Domain.csproj` | PASS |
| `Demo.Infrastructure.csproj` references `Demo.Application.csproj` | PASS |
| `Demo.Api.csproj` references `Demo.Domain.csproj` | PASS |
| Non-dependency element with `Include='...'` | must not create a `ProjectReference` |
| A `ProjectReference` appearing only inside an XML comment | must not create a dependency or a diagnostic |

All expected PASS cases require **zero** relevant findings. All expected FAIL cases require the corresponding actual dependency-direction message.

### 4.2 Package declarations and Central Package Management

Test with both quote styles (plus representative mixed/reordered/multiline variants):

- A safe `<PackageReference Include='Safe.Lib' />` without `Version` remains allowed.
- A `.csproj` `<PackageReference Include='Safe.Lib' Version='1.2.3' />` fails for an **inline version**.
- `VersionOverride='1.2.3'` fails with the existing override diagnostic.
- A paired `<PackageReference Include='Safe.Lib'><Version>1.2.3</Version></PackageReference>` continues to fail for an inline version.
- `Microsoft.Extensions.Http.Polly` and `Serilog.Sinks.Elasticsearch` are detected through the existing DENY list.
- A review-only package such as `MediatR` is identified under the existing accepted-decision semantics; do not rewrite those semantics.
- `Directory.Packages.props` with `ManagePackageVersionsCentrally=true` and `<PackageVersion Include='Safe.Lib' Version='1.2.3' />` is **valid**, not reported as missing `Version`.
- A `PackageVersion` with `Version='*'` fails as floating; with an existing recognized prerelease suffix it produces the original prerelease diagnostic.
- `Update` attributes work where the original module already supports them.
- Comment-only declarations are inert; unrelated XML content does not produce a phantom package.

Do not start a new, unbounded audit of all MSBuild conventions. These are specific guards for the affected parser surface.

### 4.3 Declared dependencies and differences

Exercise the exported `declaredDependencies()` and `dependencyDelta()` directly, against representative `.csproj` and central props content:

- Two manifests differing **only by XML quoting** yield equivalent package maps and reference sets and **empty** delta.
- New project reference: `added` is reported; deleted reference: `removed` is reported, under either quote style.
- Added, removed, or version-changed package declaration is reported under either quote style.
- Real mixed-quote or multiline manifests do not appear to have empty dependency sets simply because the parser missed attributes.
- A comment-only declaration creates no new dependency.
- For an actual invalid, newly written manifest, `checkManifestFile()` flags the relevant violation even if the delta is computed separately.

### 4.4 Actual Git hook propagation

In small **isolated local Git repositories**, test the unchanged generated hook entry point and configured events, with the updated module underneath. At minimum:

1. After a successful Bash manifest edit, the relevant single-quoted invalid project reference is surfaced through `PostToolUse` actual-state validation.
2. After a failed Bash command with a **real partial file write**, the same invalid reference is surfaced through `PostToolUseFailure`. Do not count a command that failed without changing any file.
3. For PowerShell, verify propagation using the current event wiring and existing supported input/encoding contract; a real Windows PowerShell 5.1 process is not required on a non-Windows runner, and must not be claimed if not executed.
4. Valid single-quoted references and safe central package declarations do not produce false dependency violations.
5. A quote-only rewrite should not be treated as a new project-reference edge; a real new edge must be observed.
6. A failed command that changed no relevant manifest should remain quiet. An unrelated shell invocation must not produce repeated false positives.
7. Recheck at least one linked worktree and nested `cwd` scenario if runnable. Do not rerun the entire prior D1–D12 Windows/Stop campaign; those implementation files remain byte-identical and existing evidence can be clearly marked **inherited**.

Post events report violations; they do **not** become new blocking pre-execution hooks. Preserve PreToolUse's existing fail-closed semantics.

## 5. Preservation gates

- Verify the current **71-file** template before editing, and record one initial per-file hash inventory. At conclusion, exactly **70 files** (all except `manifest-checks.mjs`) are byte-identical to that starting inventory. There must be no new permanent template files.
- JS syntax: run `node --check` on the modified module and existing affected runner. Run the existing `.claude/tools/check-instructions.mjs` on the final template, using its supported invocation. Any `NOT APPLICABLE` check must be labeled as such, never called positive evidence of actual .NET runtime behavior.
- Reconfirm the policy and structure gates applicable to unchanged content: 194 inventory policies plus GOV-017/GOV-018, no changed owner/trigger/minimum-scope semantics, no broken internal references, no level inversion, technology-neutral Levels 0/1, the L0 four-level identity and no capability slots or Kind/Scope taxonomy.
- Preserve the unchanged `.claude/settings.json` and hook implementations: exec-form hook launch, critical `PreToolUse` `onFailure: "block"`, `PostToolUseFailure` registration, active root versus launcher root, `.git`/worktree handling, tracked HEAD/deletion/move observations, correct UTF-8/BOM/UTF-16 handling, and content-aware Stop deduplication. Test the parser-facing integration cases above; inherited tests of unchanged hook logic should be labeled as historical evidence rather than falsely claimed freshly executed.
- Keep the original V2 preservation/context/complexity balance: don't rewrite any `.md` instruction or skill, change always-loaded context, split files, or create novel helper scripts. If an initial integrity check fails, document the exact discrepancy and stop instead of resetting to baseline.
- Confirm input folders and original root metadata remain unchanged. Keep `output/` limited to `template/`, `REFINEMENT_REPORT.md`, and temporary `.work/` until cleanup.

## 6. Execution discipline and hard stop

1. Freeze the starting inventory. Establish the small test harness **once** and reproduce the original single-quote defect in a disposable copy. Do not repeatedly compare against Run-02 or a neighboring candidate.
2. Implement the smallest coherent fix in the authorized JS module. Prefer a shared internal XML-attribute recognizer used by all affected sites.
3. Run the finite tests in Section 4. If a fixture is wrong, correct it and rerun only relevant cases, with a plain explanation; do not weaken the oracle or count a failing setup as success.
4. Run **ONE** cumulative confirmation audit against final files (Section 5). If that audit finds an actual template defect, perform at most one direct corrective edit and one reconfirmation. If anything still fails or requires unsupported work, report `BLOCKED` honestly and **STOP**.
5. Append an `iteration_after_audit_1` subsection to the EXISTING `output/REFINEMENT_REPORT.md`: initial reproduced failure, actual root cause, exact changed file, old/new hashes, exact direct and hook checks run with counts, expected diagnostics, preservation results and evidence provenance, remaining bounded limitations, final state (`STRICTLY_BETTER` / `BLOCKED`). **Do not overwrite** earlier L0 results.
6. Keep `output/.work/` until the report and final validation are complete, then remove it **LAST**. Verify `output/` contains exactly `template/` and `REFINEMENT_REPORT.md`.
7. **STOP immediately** when accepted; do not perform further experiments, repeat audits, revise the report due only to a speculative stop-hook objection, reconstruct the harness, or argue with completion hooks. If a stop hook prevents normal termination, provide the final status and evidence and await the user's decision instead of looping.

A large PASS count does not imply comprehensive soundness. Do not claim behavior you did not test. This pass is successful only when it fixes both the false negatives and false positives introduced by quote-sensitive XML parsing, preserves old L0 obligations, and stops within the bounded protocol.
