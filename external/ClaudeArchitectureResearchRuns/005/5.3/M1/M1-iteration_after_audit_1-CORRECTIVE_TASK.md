# M1 / Phase 5.3 — iteration_after_audit_1: XML attribute parity corrective pass

## 0. Status, objective, and scope

This is the **first corrective iteration after the fresh independent re-audit**, NOT the first M1 refinement overall. It continues the previously completed M1 5.3 iteration-2 output. Preserve the original iteration numbers in the research record; use the label `iteration_after_audit_1` only for this new corrective pass.

**Objective:** eliminate proven single-quoted XML attribute false negatives in the two existing M1 .NET checking scripts. Keep the same Minimal Modular + Replaceable Capabilities architecture; do not rebuild the template, redesign hooks, or expand architectural policy.

Authoritative inputs in this M1 workspace:

1. `CANDIDATE.md`, `REFINEMENT_TASK.md`, `audit/DEFECT_DOSSIER.md` for identity, frozen policy and original acceptance obligations.
2. `source/inventory.json` and `source/shared-research-invariants.json` for the 194 + 2 policy inventory.
3. The **CURRENT** `output/template/` and `output/REFINEMENT_REPORT.md`; especially these files:
   - `output/template/.claude/scripts/check-architecture.js`
   - `output/template/.claude/scripts/check-manifests.js`
   - `output/template/.claude/scripts/lib/common.js`
   - `output/template/.claude/hooks/post-tool-use.js`
   - `output/template/.claude/settings.json`
4. `baseline/template/` only to understand immutable M1 history if indispensable; never copy it over current output.

Do NOT inspect sibling candidates or use prior ChatGPT audit text as code. The cases in this task are independently reproducible acceptance examples. Source/candidate policy remains binding; where the original `REFINEMENT_TASK.md` asks to recreate output from baseline, that instruction applied only to the original pass and **does not apply now**. This task supersedes it on execution scope and staging.

### Immutable boundaries

- The current `output/template/` has **80 runtime files** and is the starting point. Record a sorted path/file SHA-256 inventory once before editing. Do not silently accept an unexpected inventory change; explain it and stop if the expected current M1 state is absent.
- `baseline/`, `source/`, `audit/`, `CANDIDATE.md`, `REFINEMENT_TASK.md`, `GOAL_PROMPT.txt`, `MANIFEST.sha256`, `PROVENANCE.json`, and previous iteration prompts are immutable.
- Only these output template files may change:
  1. `.claude/scripts/check-architecture.js`;
  2. `.claude/scripts/check-manifests.js`;
  3. `.claude/scripts/lib/common.js` **only if** a small shared, bounded XML-tag/attribute reader is materially preferable to duplicating it. Document the reason if touched.
- Also append a new labeled section to **the existing** `output/REFINEMENT_REPORT.md`; preserve all earlier sections and factual claims as historical records. Do not create a replacement report.
- All other template files, including hook entry points, capability contracts, rules, settings, and selection metadata, must remain byte-identical. No new permanent runtime artifact, package dependency, slot, or restructuring.
- Use `output/.work/` for temporary harnesses and Git fixtures and delete it only after completed checks and report writing.

## 1. Reproduced defect and implementation evidence

Direct inspection of the current scripts reveals separate double-quote-only parsing sites:

**`check-architecture.js`**

- `projectReferences()` uses a `<ProjectReference... Include="..."` regex. It misses the semantically identical `Include='...'` form.
- `classify()` identifies a test project by searching for the selected framework's `Include="package"`. The attribute quote style must not influence test-project identification.

**`check-manifests.js`**

- `packageReferences()` recognizes `Include` or `Update`, `Version`, and `VersionOverride` only in double quotes; a single-quoted tag can disappear from all NuGet checks.
- `checkPackagesProps()` requires double-quoted `Include` and `Version` in that order on `<PackageVersion>`. Single quotes or reversed order bypass floating/prerelease/deprecated/reserved package checks.

The following actual-source behavior was reproduced before this task was written, on an isolated copy of the attached final M1 template:

```xml
<!-- In backend/Demo.Domain/Demo.Domain.csproj: forbidden Domain -> Api -->
<ProjectReference Include='../Demo.Api/Demo.Api.csproj' />

<!-- In backend/Directory.Packages.props: floating + deprecated -->
<PackageVersion Version='*' Include='Microsoft.Extensions.Http.Polly' />
```

With a real `Demo.Api.csproj` present and central version management enabled, both `node .claude/scripts/check-architecture.js` and `node .claude/scripts/check-manifests.js` returned **0 errors, 0 warnings** on the current implementation. A same-meaning double-quoted reference is detected. This is a functional false negative, not merely a style mismatch.

Root-cause target: recognize supported XML **attributes**, not superficial quote formatting. Do not fix by adding special cases for these package/project names.

## 2. Required correction and boundaries

Implement a compact, deterministic reader for the existing supported `<ProjectReference>`, `<PackageReference>`, and `<PackageVersion>` elements, with a single consistent understanding of XML attribute boundaries. A small shared helper is allowed; full MSBuild evaluation, new dependencies and broad XML subsystem rewrites are not.

**Required behavior:**

- Single-quoted and double-quoted attribute values must produce identical semantic results for identical values.
- Allow attribute order to vary (`Include` before or after `Version`); support optional spaces around `=`, ordinary CRLF/LF and line breaks inside start tags; keep correct boundaries for quoted `>` and spaces inside values where relevant.
- Preserve current handling of `Include` and `Update` for package references; keep `<Version>...</Version>` child content and `VersionOverride` handling. Do not weaken existing package policies.
- Only genuine live XML elements count. An element that occurs solely inside an XML comment must not create a dependency or package finding. Do not naively strip quoted comment delimiters inside attribute values.
- Attribute extraction must not inadvertently capture attributes of a sibling tag or a nested child. Do not treat attributes from one `<PackageVersion>` as belonging to another.
- For malformed/unsupported XML, avoid fabricating a successful parse: remain explicit about relevant uncertainty when the currently supported checker boundary cannot reliably identify a required attribute. Do not claim a full XML validity check or comprehensive MSBuild semantics.
- Retain existing policy levels (`ERROR`, `WARN`) and wording/owners wherever possible. Correct content must not be rejected merely because it uses single quotes or a different attribute order.

**Do not change** the architecture decision matrix (`mayReference`), package policy tables, selected capability manifests, hooks or surrounding repo logic. If a real blocker appears outside the permitted files, record and stop rather than silently expanding the rewrite.

## 3. Finite discriminating acceptance suite

Build **one** temporary, reusable Node.js harness under `output/.work/`. Each integration fixture must be staged in a fresh copy (or precisely restored clean state) of the current M1 template with a minimal real backend tree. Use the actual exported checker functions and CLI entry points, not a rewritten test-only parser. For hook cases use isolated real Git repositories/worktrees and real hook JSON.

First run at least two counterexamples on a copy of the **unmodified** checker code and show the expected false PASS (the `Domain -> Api` case and the floating central package version with single quotes). Preserve a trustworthy before-fix record; then run the same cases after the fix.

### 3.1 Project reference matrix — architecture checker

Use a real project tree with correct M1 suffixes such as `Demo.Domain`, `Demo.Application`, `Demo.Infrastructure`, `Demo.Api`.

**Expected ERROR:**

- `Demo.Domain` references `Demo.Api` via double-quoted `Include`.
- Same forbidden edge via single-quoted `Include`.
- The same edge with whitespace/newlines around/inside the start tag and a valid attribute reordering when other benign attributes are present.
- Reference to a test project remains forbidden irrespective of the quote style.

**Expected clean (no ERROR or WARN):**

- `Demo.Application -> Demo.Domain`, `Demo.Api -> Demo.Domain` and other explicitly permitted directions, with each quote style.
- No `ProjectReference` at all.
- A commented-out forbidden reference must not be treated as a real edge.

Test-framework detection parity: a project containing the selected framework package reference must be classified identically for `Include='NUnit'` and `Include="NUnit"` (use the actual configured selected-framework package ID). Check both the appropriate project-reference behavior and the resulting diagnostic level, rather than asserting only helper return values.

### 3.2 NuGet / package matrix — manifest checker

For real `.csproj` with both quote styles, and `Include` or `Update` as applicable:

- `<PackageReference Include='Newtonsoft.Json' Version='13.0.3' />` => **ERROR** (inline version forbidden by CPM); double-quoted equivalent => same.
- A child `<Version>13.0.3</Version>` => **ERROR**, including with single-quoted Include.
- `VersionOverride='13.0.3'` => existing **WARN** policy, both quote styles.
- `Include='Microsoft.Extensions.Http.Polly'` => **ERROR** for deprecated package, independent of Version attribute and quote style.
- `Include='MediatR'` => preserve existing reserved/decision **WARN** (use actual selected frame policy data), both quote styles.
- A correct stable package reference with no inline version and no prohibited ID => no errors/warnings.
- `<PackageReference ...>` only in an XML comment => no findings.

For real `Directory.Packages.props` with `ManagePackageVersionsCentrally=true`:

- Stable `<PackageVersion Include='Newtonsoft.Json' Version='13.0.3' />` => clean, including reversed attribute order and mixed quote styles.
- `Version='*'`, `Version=''` => existing **ERROR** for floating/empty version, with either quoting and either attribute order.
- `Version='10.0.0-preview.1'` => existing **WARN** for prerelease, with either quoting and either order.
- Deprecated/reserved IDs are still flagged according to existing package rules.
- A commented-out `PackageVersion` must not generate a spurious finding.
- Central package management disabled => existing error unchanged.

Add a small **equivalence table** that takes representative fixtures and transforms only quote style, whitespace/newlines, and attribute order, then asserts **equal normalized diagnostic sets** (severity + relevant reason + project/package identity). Equal counts alone are insufficient.

### 3.3 Real hook integration / actual-state cases

The existing hooks call these checkers. Preserve them untouched. On isolated real Git repos/worktrees, inject one forbidden XML mutation via Write/Edit and one via a Bash/PowerShell command which changes `.csproj`/`Directory.Packages.props` before returning failure; provide real `PostToolUse` and `PostToolUseFailure` JSON. Verify meaningful context/diagnostics reach the hook response for the active worktree, including the original single-quote counterexample. Test one valid modification that produces no spurious violation. Existing fail-closed `PreToolUse` remains unchanged; do not redirect a worktree action to the launcher checkout.

For Bash vs PowerShell, follow the existing platform semantics. Do not claim a live Windows PowerShell 5.1 integration test unless actually executed on Windows; Node hook JSON simulation on another OS is evidence for the hook logic but not for Windows-native process behavior.

### 3.4 Preservation smoke checks

- `node --check` for every changed JavaScript source file.
- `check-instructions`, `check-manifests`, `check-architecture` on clean current template, without treating a checker's 'no backend' status as a substantive dependency test.
- Hook event coverage, mandatory PreToolUse `onFailure: "block"`, `PostToolUseFailure`, nested-cwd/worktree targeting, and Stop loop prevention remain unchanged.
- Preserve supported XML BOM/UTF-16LE behavior (and existing UTF-16BE tolerance) with at least one targeted valid/invalid project fixture where applicable.
- Confirm M1 architecture: exactly four static slots, one required architecture frame, required persistence and backend-testing leaves, optional frontend leaf, static selection, correct `binds`, and frame/leaf separation. Optional-frontend removal should still pass using the existing checker path if an established finite smoke procedure is available.
- Reconcile 194 policy entries + GOV-017/GOV-018. Since no policy-bearing artifact is authorized to change, show their **byte identity** and reference the prior accepted coverage evidence; run focused policy/instruction/reference checks without claiming a fresh full semantic audit of 196 entries unless actually done.
- No change to always-loaded text or the M1 flat topical rule layout; no new file/capability slot.

## 4. Convergence and evidence protocol

1. Snapshot the initial path/hash inventory and current report state; establish 80-file identity.
2. Reproduce both false negatives on *unmodified* checkers with the real test runner.
3. Implement the smallest maintainable XML parsing correction in the two checkers, using `lib/common.js` only when truly justified. Review for duplicate parsing paths and accidental cross-element capture.
4. Run the **finite** suite in Section 3 and preserve per-fixture outcomes. Expected failures must show relevant checker findings, not incidental missing files, auth failures or invalid test roots.
5. Run **one cumulative confirmation** that includes syntax, baseline behavior on clean output, all required positive/negative equivalence cases, hook smoke tests, file/hash identity, capability/policy preservation and output hygiene.
6. If this confirmation uncovers a concrete test or template defect, correct only that specific cause and re-run the affected cases plus one full reconfirmation. Do not repeatedly modify test oracles to manufacture green results; distinguish a proven test-side false positive from a real template regression.
7. Append an `iteration_after_audit_1` section to `output/REFINEMENT_REPORT.md` recording root cause, exact changed files, before/after reproductions, table of test outcomes, 80-file invariant, protected-file hashes, scope/limitations, final template hash and `STRICTLY_BETTER` or `BLOCKED` with exact evidence. No vague claims of complete Windows testing or blanket policy verification.
8. Remove `output/.work/` only after the report and final checks; verify output contains **only** `template/` and `REFINEMENT_REPORT.md`; STOP.

If a required contractual property cannot be established with a bounded fix, report `BLOCKED` with reproducible failures and stop. The objective is one evidence-backed corrective pass, **not** endless new test generation, independent proof-of-proof cycles, or unrelated cleanup.

## 5. Acceptance contract and explicit exclusions

Promote only if all of the following hold:

- Every reported single-quote bypass produces the **same relevant policy/architecture decision** as its double-quote equivalent.
- Valid single-quoted and reordered XML no longer causes false errors or misclassification.
- Existing package-policy severities, project-layer rules, test-project classification and child Version behavior are preserved.
- Existing hooks still surface the corrected checker results in both success and failure events, and target the active worktree.
- Protected files are unchanged, M1 capabilities/policies/hook configuration remain intact, and the final output tree is clean.
- Only permitted files changed and the result is a demonstrated strict functional improvement.

**Out of scope:** arbitrary nonstandard XML, general-purpose MSBuild evaluation, full condition/property expansion, new libraries, new policy definitions, wholesale command-parser changes, alterations to dependency directions, broader shell parser redesign, source/candidate/baseline modifications, or any other architecture's code. Record genuine limitations transparently rather than redefining the acceptance target.
