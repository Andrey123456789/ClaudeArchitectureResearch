# K1 / 5.3 — Independent audit of corrective iteration 1

**Input:** `K1_1.zip`  
**Disposition:** **Improved, NOT READY TO FREEZE. Iteration 2 required.**

## 1. Provenance, topology and static checks

- Immutable baseline: K1 Run-02, 85 template files and 346,715 bytes. The submitted iteration-1 output has 87 files and 399,353 bytes, including two new runtime helpers (`classify-command.cjs` and `actual-state.cjs`). Compared with Run-02: two added and 25 changed files; none deleted.
- Independently reproduced SHA-256-of-sorted-`sha256sum -b`-listing: baseline `9e524c3fbcca218d46810ac0aab8ebe8cf1ce95f1ec6f6b516b941ec36418bec`; output `0b7b52ee100b58f136727cf6892441465e23175607de667203333de41d5965e5` (both match the submitted report).
- All eleven runtime `.cjs` files passed `node --check`.
- `check-instructions.cjs` on the submitted clean template: 0 errors, 0 warnings, ~4,849 always-loaded tokens. `check-manifests.cjs`: 0 errors, 0 warnings. `check-cochange.cjs`: NOT APPLICABLE without a Git working tree (no false claim of conformance).
- Clean output shape: `output/template` plus `output/REFINEMENT_REPORT.md`, without `output/.work`.
- The source `inventory.json` declares 194 policies and `shared-research-invariants.json` contains GOV-017 and GOV-018. The independent test in this report is **not** a new exhaustive source-to-owner audit for each of the 196 policies. `324/324` in the submitted report belongs to Claude's deleted temporary harness and was **not independently rerun as 324 cases**.
- Checked the original `MANIFEST.sha256`: 142 of its 144 hash entries match; the two mismatches are `GOAL_PROMPT.txt` and `REFINEMENT_TASK.md`. Both submitted files exactly match the user's independently provided K1 refactored prompts and evidently postdate the original workspace manifest. This is an input-provenance caveat, not evidence of an iteration-1 template defect. The original research input file hashes otherwise match.

## 2. Critical independent reproductions — BLOCKER A: XML quote parity

The shared `.claude/scripts/lib.cjs` `xmlElements()` attribute reader is double-quote-only; `.claude/scripts/check-manifests.cjs` also independently reads the root Project `Sdk` with a double-quote-only regex. Both single and double attribute quotes are valid XML.

All experiments below executed the **real submitted scripts**, generally in separate disposable repository copies. The first table includes direct checker calls and actual PostToolUse calls after edits to a real Git repository.

| Case | Double-quoted attributes | Single-quoted attributes |
|---|---|---|
| Domain `PackageReference Microsoft.EntityFrameworkCore Version=9.0.0` | Correct error (central-package + EF Core leak); post-hook reports it | **Incorrect PASS**, including PostToolUse |
| Domain `FrameworkReference Microsoft.AspNetCore.App` | Correct framework-leak error | **Incorrect PASS**, including PostToolUse |
| Domain root `Sdk=Microsoft.NET.Sdk.Web` | Correct Web-SDK error | **Incorrect PASS** |
| Valid Application → Domain `ProjectReference` | Correct PASS | **Incorrect FAIL**: invents Application → Application self-reference |
| Invalid Domain → Api `ProjectReference` | Correct Domain → Api diagnostic | Wrong diagnostic: invents Domain → Domain; not an acceptable negative test |
| Central `PackageVersion NewDep Version=1.2.3` | Correct PASS | **Incorrect FAIL**: claims `PackageVersion ""` has an empty version |
| Central `PackageVersion NewDep Version=*` | Correct error identifying NewDep/version | Error with **wrong identity and cause**, `PackageVersion ""`/empty version |
| Partial failed-shell mutation of Domain `PackageReference` | `PostToolUseFailure` reports violations | **Silent**, exit 0 |

The `.csproj` failures include both missed violations and fabricated violations for otherwise valid content. They violate the manifest/architecture enforcement requirements and the criterion that negative fixtures must fail for the correct reason.

## 3. Independent reproduction — BLOCKER B: undated project-reference approvals

The `acceptedDecisionText(root)` function accepts any nonempty Date cell except `—`, `-`, or the table header label. This is too loose for the authorization of Reserved project-reference mutations.

The genuine PreToolUse dispatcher was exercised on:

`dotnet add Foo.Api.csproj reference Foo.Domain.csproj`

| Accepted-decision Date cell | Expected outcome | Observed |
|---|---|---|
| No approval row | BLOCK | BLOCK |
| Valid `2026-10-21`, matching edge | ALLOW | ALLOW |
| `TBD`, matching edge | **BLOCK** | **ALLOW** |
| `pending`, matching edge | **BLOCK** | **ALLOW** |
| `—`, matching edge | BLOCK | BLOCK |

Any text in an undated row can therefore authorize an otherwise Reserved change. This is a substantive safety-of-policy failure, not a stylistic issue.

## 4. Additional independent regression checks

- `check-instructions.cjs` on unmodified template: clean.
- Removing both contract and module `Binds: architecture` for persistence: correctly returns two required-binding errors.
- Removing ENF `Conforms:` declaration: correctly returns an error.
- Changing an ENF `Conforms:` target to a WF skill: correctly rejects the wrong direction (and the undeclared policy owner).
- Adding a fifth capability directory: correctly rejects it (no new static slot).
- Linked worktrees, the complete 324-case historical suite, Windows PowerShell 5.1 runtime, actual host activation, optional-frontend clearing, and all 196 source policy anchors were **not rerun independently** here. Their prior passed evidence remains reported evidence; no new broad claim is made.

## 5. Recommended correction — tightly bounded iteration 2

There are **two independent root causes**, with the XML defect explaining most reproduction failures. Do **not** regenerate the K1 template or refactor its hooks, Kind model, or capability selection.

1. Fix XML attribute recognition centrally in `.claude/scripts/lib.cjs` and reuse it for `Project Sdk` in `.claude/scripts/check-manifests.cjs`. Cover single/double/mixed quotes, attributes in either order, whitespace, quoted `>` and paired/self-closing element forms. Keep accurate diagnostics and ensure allowed Application→Domain and valid central exact versions produce no false errors. Check real PostToolUse and PostToolUseFailure.
2. Require an actual ISO calendar Date for rows in the canonical accepted-decision table before any row or its linked decision text can provide Reserved authorization. Preserve valid dated rows and approved edge checks; reject placeholders and invalid dates.
3. Freeze all unaffected template files by hash comparison; run one focused finite test suite and one cumulative confirmation, then report and stop. The historical 324-case harness was deleted and must not be reconstructed as an artificial gate.

**Next prompts prepared:** `K1-5.3-corrective-GOAL_PROMPT_iteration2.txt` (under 4,000 characters) and `K1-5.3-corrective-pass_iteration2.md` in `K1-5.3-corrective-iteration2-two-files.zip`.

## 6. State of unfinished 5.3 candidates (current conversation)

- **L1:** iteration 7 independently audited; residual P4 adjacent-Markdown-governor issues; iteration-8 Goal and Task already delivered, no L1_8 result received. Not frozen.
- **K0:** iteration 1 independently audited; XML single-quote parser issues; iteration-2 Goal and Task already delivered, no K0_2 result received. Not frozen.
- **K1:** iteration 1 independently audited here; quote parity and undated-approval bypass; iteration-2 Goal and Task delivered with this report. Not frozen.

The previously accepted candidates M, M1 and L0 are not reopened by this audit.
