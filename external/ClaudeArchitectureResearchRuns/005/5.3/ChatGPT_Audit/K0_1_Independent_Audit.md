# K0 / 5.3 — Independent audit of iteration 1

**Artifact:** `K0_1.zip`  
**Candidate:** K0 (Kind × Scope architecture, without K1 capability replacement)  
**Decision:** **IMPROVED BUT NOT READY TO FREEZE**; one confirmed common parser defect with three independent real behavioral consequences.

## 1. Scope and artifact integrity

- Selected immutable baseline: 5.2 K0 Run-02, 62 files and 324,363 bytes.
- Iteration-1 final template: 63 files and 366,543 bytes. One new reusable runtime helper, `.claude/scripts/repo.cjs`.
- Final reported tree hash **independently reproduced** as `51105bf425561a167dfda0bce08314c9f1fa84ef4a71be85bc9a26892ce08022`, using a sorted listing with `sha256sum -b` followed by `sha256sum`. Baseline tree hash matches `18f51b02f45bb5cbc7284e5fc412aee810996bc8c16ff0676f65c9c3144c2209`.
- Workspace `MANIFEST.sha256`: 121/121 entries verified; original input directories and task materials have not been mutated.
- `output/` contains only `template/` and `REFINEMENT_REPORT.md`. No residual `.work/` folder.
- All original STD rules and the authoritative DEC register are byte-identical to K0 Run-02. The K0 architecture's 7 Kinds, 6 Scopes and one 18-entry DEC register remain in place.
- Original always-loaded measurement from fresh checker output: approximately 19,738 characters (~4,935 tokens), matching Claude's report.

## 2. Verified independent positives

- Final `check-instructions.cjs --root <template>`: PASS, 60 artifacts, 0 errors.
- Final `check-dependencies.cjs --root <template>`: PASS, 1 manifest, 0 errors and notices.
- `node --check` for every `.cjs`: PASS.
- Command classification (npm/pnpm/yarn, dotnet packages and references, Git read-only and mutating operations, shell wrappers): 30/30 PASS.
- Process-level hook experiments in isolated repositories: 18/18 PASS: deny/ask/allow routing; invalid manifests after arbitrary successful and failed shell calls; same-path rewrites; removal; first shell observation of invalid committed manifest; deduplicated Stop reminders; `stop_hook_active`; fail-closed invalid PreToolUse.
- Real linked-worktree test: correct active-root resolution, invalid linked-worktree `.csproj` detected, main checkout remained clean.
- Eight isolated checker mutation tests: 8/8 PASS: missing critical `onFailure`, missing PostToolUseFailure, wrong STD Kind, unowned KNW norm, reversed STD→KNW, forbidden ENF→KNW, broken DEC Affects target, forbidden capability field.

The **298/298** score in `REFINEMENT_REPORT.md` is Claude's run. Its temporary harness was removed by design and is not in the submitted final output, so that exact suite was not independently rerun. The Windows PowerShell 5.1-specific portion is reported by Claude but not independently rerun in this Linux environment. The 196-policy owner/trigger/scope figures are reported by Claude and supported partly by unchanged normative artifacts, not by a fresh exhaustive 196-row manual audit here.

## 3. BLOCKER — valid single-quoted XML attributes bypass enforcement

Severity: **HIGH**. Primary owner: `.claude/scripts/check-dependencies.cjs` (shared attribute extraction and exported `projectReferences()`), consumed by `.claude/hooks/hook.cjs`.

### A. ProjectReference — D4/D5

Two temporary Git repositories were initialized with `backend/My.Domain/My.Domain.csproj` and `backend/My.Api/My.Api.csproj`; the hook first established its state snapshot. Domain → Api violates Clean Architecture and any new project-reference graph choice is Reserved.

| Mutated XML | PostToolUse | Direct dependency checker |
|---|---|---|
| `<ProjectReference Include="../My.Api/My.Api.csproj" />` | Explicit inward-dependency and Reserved graph-change findings | Error (nonzero exit) |
| `<ProjectReference Include='../My.Api/My.Api.csproj' />` | **Silent, empty output** | **0 errors, 0 notices** |

Both are valid XML with identical meaning. This is an end-to-end actual-state hook bypass, not just a difference in static text matching.

### B. PackageReference — package deny-list

| Mutated XML | Checker result |
|---|---|
| `<PackageReference Include="Microsoft.Extensions.Http.Polly" />` | Correct deprecated-package error |
| `<PackageReference Include='Microsoft.Extensions.Http.Polly' />` | **False PASS** |

The name extractor reads only double-quoted `Include` attributes, so the deprecated package is treated as unknown and passes.

### C. Directory.Packages.props — floating versions

| Mutated XML | Checker result |
|---|---|
| `<PackageVersion Include="NewDep" Version="*" />` | Correct floating-version error |
| `<PackageVersion Include='NewDep' Version='*' />` | **False PASS** |

In contrast, a single-quoted inline `PackageReference Version='*'` already triggers the general inline-version prohibition, but its name is not extracted correctly. The shared root cause is inconsistent XML attribute parsing, not missing Windows/Git/event logic.

## 4. Recommended bounded corrective action

Proceed to **K0 iteration 2**, preserving the entire completed iteration-1 output, with a narrowly scoped repair of XML attribute handling in `check-dependencies.cjs` and its exported `projectReferences()` function. Test both quote styles, mixed quotes, whitespace, attribute order, legitimate project references, invalid direction, Reserved graph changes after `PostToolUse` and `PostToolUseFailure`, deprecated NuGet package names, and floating central package versions.

Do not rewrite hooks, Kind architecture, DEC/STD rules, policy ownership, state machine or root/worktree resolver unless a newly reproduced directly related failure proves that unavoidable. Do not reconstruct Claude's removed 298-case harness or start unbounded fuzzing. Keep the 63-file topology and all other template files byte-identical if possible. Perform one finite test cycle and one confirmation audit, then stop.

**Prompts prepared:** `K0-5.3-corrective-GOAL_PROMPT_iteration2.txt` (3,274 characters; below 4,000-character limit) and `K0-5.3-corrective-pass_iteration2.md` in a two-file ZIP.

## 5. Status

- **K0_1:** an evidenced improvement over raw Run-02, but **not frozen**.
- **Next task:** K0 5.3 corrective iteration 2, strictly scoped to valid XML-attribute quote parity and its downstream validations.
- **K1:** independent candidate; its ongoing iteration need not be interrupted for this K0 finding.
