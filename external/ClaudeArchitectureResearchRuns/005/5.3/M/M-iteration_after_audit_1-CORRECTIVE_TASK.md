# M / Phase 5.3 — Corrective iteration_after_audit_1

## 1. Mission and immutable contract

This task is the **first post-independent-audit correction** to Candidate M. Its numbering is distinct from the earlier corrective iterations. The source of truth for implementation is the **current** `output/template/` (accepted iteration 4); the immutable original `baseline/template/` is **not** the starting point.

The task is **not** to create a new M candidate, modify architecture, or expand the audit scope. Close a demonstrated XML parsing discrepancy in the existing M manifest checker. The same legal XML attributes have different outcomes depending on the quote delimiter. Preserve every previously accepted behavior and report actual evidence without claiming unperformed tests.

Read, in order and with an explicit time boundary:

1. This task and the paired `M-iteration_after_audit_1-GOAL_PROMPT.txt`.
2. `CANDIDATE.md` and the identity/preservation sections of `REFINEMENT_TASK.md`.
3. `audit/DEFECT_DOSSIER.md` for the original M D1–D6 contract.
4. The final cumulative acceptance and implementation changes recorded in `output/REFINEMENT_REPORT.md` (read the relevant iteration-4 and earlier acceptance summaries; no transcript reconstruction).
5. The full current `output/template/.claude/scripts/check-manifests.mjs`.
6. The relevant callers (`.claude/hooks/dependency-guard.mjs`, `.claude/hooks/file-change.mjs`) and rule owners (`.claude/rules/architecture.md`, `.claude/rules/dependencies.md`, `.claude/skills/add-dependency/SKILL.md`).
7. `source/inventory.json` and `source/shared-research-invariants.json` for policy preservation and naming. Do not edit these source files.

Do not inspect other candidates, previous ChatGPT audit reports, parent/sibling workspaces, web sources, or unrelated historical code. No need to re-read the entire V2 archive to change one parser. Do not change files under `baseline/`, `source/`, `audit/`, or the workspace root.

## 2. Reproduced blocker — quote-sensitive XML inspection

The current checker contains, in `attributes(text)`, a match equivalent to:

```js
/\b([A-Za-z]+)\s*=\s*"([^"]*)"/g
```

It also finds project references with a distinct double-quote-only regex equivalent to:

```js
/<ProjectReference\b[^>]*?\bInclude\s*=\s*"([^"]+)"/gi
```

These are two surfaces of one root cause. In particular:

```xml
<ProjectReference Include="../Demo.Api/Demo.Api.csproj" />
<ProjectReference Include='../Demo.Api/Demo.Api.csproj' />
```

are equivalent XML. In a `Demo.Domain.csproj`, both must produce the **same forbidden Domain → Api** result.

Similarly, the following are equivalent, and both violate the current central-version placement rule:

```xml
<PackageReference Include="System.Text.Json" Version="9.0.0" />
<PackageReference Include='System.Text.Json' Version='9.0.0' />
```

And both of these are well-formed `Directory.Packages.props` entries with a nonempty pinned version, and neither should cause a **missing Include** or **missing Version** finding:

```xml
<PackageVersion Include="System.Text.Json" Version="9.0.0" />
<PackageVersion Include='System.Text.Json' Version='9.0.0' />
```

A local baseline probe against the supplied iteration-4 checker confirmed that an illegal single-quoted Domain→Api reference and an inline single-quoted package version were missed, while a single-quoted central PackageVersion generated bogus missing-attribute violations. The corrective implementation must fix **both false negatives and false positives**.

## 3. Required implementation behavior

1. Implement a small, deterministic XML-start-tag/attribute extraction strategy suitable for the **existing covered subset** of `.csproj` and `Directory.Packages.props`. Accept single-quoted, double-quoted, and mixed-quote attributes, multiline attribute lists, spaces around `=`, reordered attributes, and the present case-insensitive matching semantics. Avoid a naive regex that crosses from one XML tag into another when an attribute is absent.
2. Use the **same attribute interpretation** for `PackageReference`, `PackageVersion`, and `ProjectReference`. Eliminate the separate double-quote-only reference check or make it consume the shared parser. Keep original acceptance of self-closing tags and paired `PackageReference` with nested `<Version>`.
3. Do not reinterpret commented-out XML as active declarations. Preserve the existing `readXml()` comment-stripping behavior. For malformed input or unsupported dynamic MSBuild evaluation, do not invent a computed dependency or silently claim comprehensive XML/MSBuild validation; document the boundary. Keep this a small bounded patch, not a new interpreter.
4. Preserve source/target project-layer naming, legal vs illegal reference directions, production/test policy, central-version lookup and precedence, banned vs review-only NuGet rules, version pinning/floating/range/prerelease behavior, and the existing `notes` versus `violations` distinction. Preserve npm behavior unchanged.
5. No new runtime dependency or permanent test file. No hook registration, logic, or scope changes. Both file-edit hooks and shell PostToolUse/PostToolUseFailure already call the common checker: demonstrate propagation through them, but do not rewrite them without a separately proved blocker (which requires reporting BLOCKED rather than broadening this pass).
6. Keep every policy owner, trigger class, minimum scope, known exception, context budget and Candidate M flat-rule organization intact. In particular, do not introduce Level/Kind/capability taxonomy, move normative policy text, or change settings/hook engine behavior.

## 4. Frozen finite acceptance matrix

Use ONE in-workspace harness under `output/.work/`, invoking the actual output checker on isolated synthetic repositories. Before editing, prove the single-quote false negative and false positive on a byte-identical copy of the initial checker. After editing, run the following matrix; classify every result as **expected violation**, **expected note**, or **expected clean**. For a violation require the relevant checker message and a nonzero exit when using the CLI; a generic parse/setup error is not an acceptable PASS. For an expected-clean fixture require no violations and no unexpected notes. Inspect result objects directly when exercising the module API.

### A. Project references (positive and negative)

Run double-quoted, single-quoted, and mixed-quoted forms, with attributes in both orders and relevant whitespace/line breaks, across:

| Fixture | Expected |
|---|---|
| `Demo.Domain` → `Demo.Api` | VIOLATION (forbidden outward reference) |
| `Demo.Application` → `Demo.Infrastructure` | VIOLATION |
| `Demo.Api` → `Demo.Domain` | CLEAN (allowed inward reference) |
| `Demo.Application` → `Demo.Domain` | CLEAN |
| Production project → `Demo.Domain.Tests` | VIOLATION |
| Commented-out forbidden `<ProjectReference ...>` | CLEAN |

Test a representative sample with the `Include` attribute first, last, and on a separate line; do **not** generate a Cartesian product of every permutation. Keep test projects and filenames aligned with the existing `classifyProject()` conventions. A missing attribute must not be inferred from a different XML tag.

### B. NuGet / Central Package Management

Provide a well-formed central props file where needed (otherwise a missing-props diagnostic is a **test setup error**, not the intended result). Test equivalent double, single, and mixed quote forms for:

| Fixture | Expected |
|---|---|
| `<PackageReference Include=... Version=...>` in `.csproj` | VIOLATION (inline version) |
| `<PackageReference Include=...><Version>...</Version></PackageReference>` | VIOLATION (nested version) |
| Versionless PackageReference with matching pinned central version | CLEAN |
| Valid `<PackageVersion Include=... Version=... />` | CLEAN (no bogus missing attributes) |
| A missing PackageVersion `Version` attribute | VIOLATION (missing version) |
| A floating PackageVersion such as `Version='9.*'` | VIOLATION (floating/range) |
| Denied `Microsoft.Extensions.Http.Polly` in PackageReference or PackageVersion | VIOLATION (denied ID) |
| Review-gated `MediatR` (or existing REVIEW_NUGET ID) | NOTE, not a spurious violation |
| Central version with single quotes matched by a versionless PackageReference with double quotes | CLEAN (lookup equivalence) |
| A commented-out banned package or floating version | CLEAN |

Retain current behavior for `VersionOverride`, prereleases, `Update` (if supported), the absence of central props, and unrelated JSON/package.json. Do not claim a feature that the existing contract never implemented.

### C. Hook propagation and regression controls

- Exercise a changed `.csproj` via the actual `file-change.mjs` Edit/Write PostToolUse path. A newly forbidden single-quoted project reference must surface with the same owner as double-quoted form.
- Exercise changed `.csproj`/`Directory.Packages.props` state via the actual `dependency-guard.mjs` shell PostToolUse and PostToolUseFailure paths in a disposable Git repository; include one failure after a partial edit. Do not mistake a nonblocking failure-hook report for a PreToolUse blocking decision.
- Verify unchanged npm force/global-option blocking, PreToolUse fail-closed handling, active worktree resolution, manifest deletion detection and Stop deduplication via previously accepted focused checks or byte identity of untouched implementation files; do not rebuild every historical test harness.
- Run Node syntax checks for all existing `.mjs` files, `check-instructions`, and the clean-template manifest checker. Record any check which is not applicable to an empty template rather than claiming an integration PASS.

### D. Metamorphic equivalence properties

For each semantic case chosen from A/B, replacing `"value"` with `'value'`, reordering attributes, or breaking attributes over supported newlines must **not** reverse the violation/note/clean classification. A valid unrelated sibling element or an XML comment must not hide an actual violation or cause a false violation. Check at least one genuine negative and positive per transformation, rather than just counting many variants of one fixture.

Report per-group counts and total fixture count; do not invent a fixed total in advance or pad test numbers. Stop fixture generation when the specified finite matrix is complete.

## 5. Preservation and proof

Before modifying anything:

- Hash/inventory current `output/template/` (expected **61 files**); record the start hash for `check-manifests.mjs` and a sorted per-file inventory.
- Create the temporary harness and reproduce at least the key original failures against the **pristine** checker. Do not reset `output/template/`.

After the fix:

- Only `.claude/scripts/check-manifests.mjs` within `output/template/` is authorized to differ from the starting inventory; the other **60 files must be byte-identical**. Keep `output/REFINEMENT_REPORT.md` as the only additional persistent edit.
- Policy owner/trigger/scope checks for **194 source policies + GOV-017/GOV-018** must have zero regressions. Because normative owner files remain byte-identical, record that invariance as preserved evidence; do not claim an independent full semantic policy audit if none was performed.
- Check M identity (flat topical rules, no Levels/Kinds/capabilities), reference validity, syntax, stable installed hook registrations, and English-only hygiene.
- No `output/.work/`, new `output/` siblings or permanent test/harness files at completion.

## 6. Bounded execution and stopping protocol

1. Inspect the relevant files and record the initial inventory, once.
2. Reproduce the original quote-sensitive discrepancy on the current checker in isolated test repositories, once.
3. Implement the **smallest comprehensible shared XML attribute fix**, without editing hooks or rules.
4. Run the finite Section 4 suite; fix any directly demonstrated regression and rerun the affected fixtures.
5. Run **one cumulative confirmation** (suite plus preservation gates). If a concrete template defect appears, make one bounded correction and rerun the affected checks, followed by at most **one** reconfirmation. Stop after that, with either success or a precise blocker; no test-of-test or repeated evidence rounds.
6. Append `Post-audit corrective pass — iteration_after_audit_1` to the existing `output/REFINEMENT_REPORT.md`, without deleting prior iteration evidence. Record the exact changed file, root cause, baseline reproductions, tests by category, regression evidence, policy-preservation basis, checksum method, changed file hashes, limitations, and final disposition.
7. Remove the harness and `output/.work/` last; verify exactly `output/template/` and `output/REFINEMENT_REPORT.md` remain under `output/`; STOP.

Allowed final dispositions:

- `READY_TO_FREEZE` — all agreed post-audit tests and preservation gates pass, with truthful evidence.
- `BLOCKED` — a reproducible acceptance failure remains; list exact fixtures and limitations. Do not continue an unbounded search or silently weaken an oracle to obtain PASS.

An unexpected Stop hook challenge is **not** permission to restart verification loops. Record its exact outstanding requirement and stop; do not fabricate tool evidence. Do not do work for any other architecture or advance to phase 5.4.

## 7. Deliverables

The final workspace must contain the existing cumulative M template and historical report plus an appended post-audit correction section. Keep `iteration_after_audit_1` as a distinct counting label in the report; it does **not** erase the four earlier corrective passes. The owner will archive the entire M folder for independent verification after this pass.
