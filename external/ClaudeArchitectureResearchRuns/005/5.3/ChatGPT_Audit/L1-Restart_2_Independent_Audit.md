# L1-Restart — independent audit of corrective iteration 2

**Candidate:** L1 / Phase 5.3  
**Artifact:** `L1-Restart_2.zip`  
**Decision:** **READY TO FREEZE under the agreed finite 5.3 acceptance contract.** No independently reproduced blocker remains. A third iteration is not justified by these findings.

## 1. Provenance and change control

- Examined the supplied `L1-Restart_2.zip` and independently compared its contents to `L1-Restart_1.zip`.
- Exactly **86 files** in `output/template/` before and after; changed only three permitted scripts:
  - `.claude/scripts/check-instructions.mjs`
  - `.claude/scripts/check-architecture.mjs`
  - `.claude/scripts/lib/project.mjs`
- The other **83/86 template files** are byte-for-byte identical to iteration 1, including instruction text, capability contracts, selected modules, settings, hooks and policy-bearing artifacts. `baseline/` (88 files), `source/` (43), and `audit/` (8) are also unchanged.
- Original input `MANIFEST.sha256` passes **144/144** entries.
- Final SHA-256 template-tree hash independently recomputed using `find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum -b | sha256sum`:
  `cbabd288390b3d9b7eaf3d6264b460b21465ceeb1f5f46005c606d8f4ddd486b` — matches Claude's report.
- `output/` contains only `template/` and `REFINEMENT_REPORT.md`; no residual `.work` files.
- All **six `.mjs`** files pass `node --check`. The clean instruction checker reports **68 artifacts, 0 violations, 0 warnings**.
- On the clean empty template, `check-architecture` reports **NOT APPLICABLE** (no `backend/`). This is not counted as a project architecture pass; independent actual `.csproj` tests follow.

## 2. Independent behavior tests

**125/125 instrumented checks successful:** 107 matrix/syntax/clean-check assertions and 18 integration/setup/mutation checks. Four integration checks establish temporary Git setup; they are not substantive correctness tests. All tests execute actual JS scripts, not the Claude self-report.

| Group | Independent result | Representative cases |
|---|---:|---|
| Strict P4/P6 L0/L1 | **72/72** | Forbidden Docker/Swagger/Serilog headings; selected/default headings with sibling; pointer under normative parent; `Must use this technique`; genuinely neutral pointer, including sibling and unrelated `Must run unit tests`; ambiguous generic parent; API-shaped leak |
| Architecture on actual `.csproj` | **28/28** | Domain/Application Web SDK single/double quotes, `<Sdk>` and `<Import>`; `Microsoft.AspNetCore.Mvc.Core`, `Authentication.JwtBearer`; explicit ASP.NET Core framework reference; EF Core, Domain→Api and production→test prohibited; API Web SDK/packages, ordinary inner-role SDK and valid inward references allowed |
| JS syntax | **6/6** | All generated `.mjs` files |
| Clean checker | **1/1** | Zero violations and warnings |
| Integration and mutations | **18/18** | Temporary Git setup; `PostToolUse` unchanged-state quiet; `PostToolUseFailure` after Bash and PowerShell with partial `.csproj` mutations; linked worktree; UTF-16LE hook input; `PreToolUse` reference-change approval and malformed-input block; fifth slot, disabled critical `onFailure`, simultaneous removal of `binds:` from both module and contract |

The `PostToolUseFailure` integration tests used Node subprocesses and real Git repositories/worktrees, with actual `.csproj` bytes changed on disk. They produced the intended architecture diagnostics, including `domain-model must not use SDK 'Microsoft.NET.Sdk.Web'` and `use-case-layer must not reference package 'Microsoft.AspNetCore.Mvc.Core'`.

Claude's own report claims **132/132** tests for corrective iteration 2 and **302/302** for iteration 1. Their deleted temporary harnesses were **not** replayed; these numbers are reported as executor evidence, not as part of the independent test count.

## 3. D1–D17 / policies / preservation

- The new changes close the **two independently reproduced iteration-1 blockers**: heading text now receives ordinary L0/L1 neutrality checking (P4); inner roles now reject the Web SDK's implicit ASP.NET Core reference and explicit ASP.NET Core package-family references (architecture confinement).
- D1/D2 and strict P4/P6 were independently sampled with positive, negative and contextual transformations across both levels. The remaining D3–D15 implementation artifacts are byte-identical to iteration 1 except for the three documented scripts. Selected regression checks of hooks, routing, worktree behavior, required `binds:` and four-slot cardinality pass. The original iteration-1 report contains broader Windows, Stop, encoding, capability and CLI evidence; not every prior scenario was independently replayed here.
- D16 (V2 content fidelity) and D17 (always-loaded/complexity review) were documented in the iteration-1 report and were **not affected** by iteration 2, since no instruction content or loading configuration changed.
- The source inventory contains **194 distinct V2 policy IDs** and the shared invariants identify **GOV-017 and GOV-018**, for 196 total. All policy-bearing files and the input sources are byte-identical to iteration 1. Therefore **no new owner/trigger/scope or policy-text regression was introduced by iteration 2**. A full independent semantic crosswalk of all 196 policies was not recreated; its accepted evidence comes from iteration 1 and Claude's documented audit.
- Overall status is therefore based on a **cumulative evidence chain**, not an assertion that all previous Windows/Desktop scenarios or all 196 semantic policy mappings were independently retested in this one audit.

## 4. Bounded limitations (not new freeze blockers)

1. `check-architecture` statically parses literal project XML. It does **not** evaluate arbitrary MSBuild properties, imports or transitive package graphs; this is expressly outside the accepted checker scope.
2. The `Microsoft.AspNetCore.*` inner-role package guard is family-based and may report an exceptional transport-free utility. Specific exemptions would require a separate approved change.
3. P4 is a bounded grammar/lexicon/static guard, not an unrestricted English semantics engine. Its agreed negative/positive format cases pass.
4. No actual Claude Desktop UI-hook activation or Windows PowerShell 5.1 execution occurred in this independent Linux/container audit. These have prior iteration-1 executor evidence; host-level acceptance remains a separate possible validation step.

## 5. Final decision

**Freeze `L1-Restart_2` as the L1 finalist for Phase 5.3.** Do not run iteration 3 on the basis of the previously known issues. This decision is conditional on the previously agreed scope and cumulative verification standard, not a guarantee of every possible Markdown expression or MSBuild configuration. Record the exact final tree hash above and preserve old `L1_8` as the separate unsuccessful historical branch.
