# Independent Audit — L1-Restart `iteration_after_audit_2`

**Source:** `L1-Restart_AA2.zip`, final `L1-Restart/output/template/`, compared byte-for-byte with the final template in `L1-Restart_AA1.zip`. The reference implementation of the L0 vocabulary was independently checked using the final `L0/output/template/` in `5.3(2).zip`. The previous ChatGPT audit reports were not used as test evidence.

## Verdict

**NOT YET READY TO FREEZE under the agreed strict P4 parity requirement.** The central contract change is implemented successfully, but two concrete technology names explicitly prohibited by L0 (`Jest` and `Scrutor`) are not recognized by the updated L1 checker. Both wrongly pass in Core and Architecture. This is a small, reproducible vocabulary parity gap, not a return to the previous natural-language pointer-classifier problem.

## Independent execution results

| Gate | Result | Notes |
|---|---:|---|
| Strict P4 negative and positive mutation matrix | 98/98 PASS | Tests in both Level-0 and Level-1 rule files, plus Level-2/3 controls. Includes `Technique: docker`, `See technique: swagger`, headings, lists, tables, code fences, link text, whitespace/case/format obfuscation, anaphora and elliptical fragments. |
| Architecture checker on real generated `.csproj` files | 11/11 PASS | Includes allowed `Application -> Domain`, forbidden `Domain -> Api`, single/double XML quotes, Web SDK, ASP.NET Core framework/packages and EF Core inside Domain. |
| Structural/contract + L0-vocabulary parity probes | 15/19 PASS | Seven structural mutation gates succeed and the additional technology probes for RxJS, Vitest, SQL Server and HybridCache pass in both levels; four parity failures are listed below. |
| Clean instruction checker | PASS | 68 artifacts, 0 violations, 0 warnings. |
| JavaScript syntax | PASS | All six `.mjs` files checked by Node.js. |
| Source manifest | PASS | `MANIFEST.sha256`: 144/144 entries verify. |
| Tree hash | MATCH | `546fd8dda79391be9f1294a14ab86add5ce4c8605b314b7f79ccb576af3a1b25` using binary-mode SHA-256 listing. |
| Template file identity | MATCH | 86 files before and after, exactly 9 changed, 77 byte-identical. |
| Output hygiene | PASS | Only `template/` and `REFINEMENT_REPORT.md`; no `.work/`. |
| Russian text in final template | NONE | No Cyrillic Unicode characters found. |

This suite is not an exhaustive correctness proof or a fresh independent owner/trigger/scope audit of every one of the 196 policies. Windows Claude Desktop live hooks were not rerun. Those limitations are not the cause of the negative verdict.

## Reproduced blocking failures: L0/L1 P4 dictionary mismatch

Inserting **either** of the following lines into the valid `0-core/engineering.md` or `1-architecture/frame/boundaries.md` file of an isolated L1 template produces exit code 0, with `0 violations, 0 warnings`:

```markdown
Must use Jest.
Must use Scrutor.
```

The same statements are rejected by the independently run L0 instruction checker. Its `TECHNOLOGY_TERMS` explicitly contains `/\bJest\b/i` and `/\bScrutor\b/i`, whereas the L1 checker `TECHNOLOGY_LEXICON`, selected-module tokens and currently selected package IDs do not recognize these names, and the API-shape regular expressions do not catch them either.

| Technology | L0 Level 0 | L1 Level 0 | L1 Level 1 | Expected L1 under harmonized P4 |
|---|---|---|---|---|
| Jest | FAIL | **PASS** | **PASS** | FAIL |
| Scrutor | FAIL | **PASS** | **PASS** | FAIL |

These are not unknown future product names; both were in the existing L0 prohibition set at the point of harmonization. They are outside the intentionally permitted fixed-platform vocabulary. Consequently the statement "L1 matches L0's technology-neutrality policy" is still false for these two cases.

**Minimal corrective action:** Add the two missing concrete-technology tokens to L1's static Level-0/1 vocabulary (or equivalent detection), create four regression tests (2 names x 2 levels), and run the existing clean-template, Level-2/3 and capability/structure gates. Do not reintroduce the pure-pointer exemption or any natural-language interpretation. Revalidate the intended neutral platform names separately.

## What was successfully corrected

- Concrete technology names now fail even in otherwise pure `Technique:` pointers at Levels 0/1, including inside Markdown headings, lists, code, link text and several supported formatting transformations.
- ASP.NET Core, NuGet, EF Core, Docker, Swagger, NUnit, Angular, Kubernetes, SQL Server, RxJS, Vitest and HybridCache were rejected on tested Level-0/1 fixtures. Generic Level-2 references without concrete technology names are permitted unless independently disallowed by the level-conformance rule.
- .NET, C#, TypeScript, Git, HTTP protocol wording and generic role references passed tested controls.
- Level-2 technique content and Level-3 technology selections remained valid under the existing ownership rules.
- PreToolUse must remain fail-closed; required binding cannot be silently removed from a selected module; removing it from the module and contract together still fails due to concrete frame-vocabulary evidence. Frame terms, placement examples and reverse conformance edges were properly rejected.
- The two edited normative architecture policies, ARC-002 and ARC-008, retain the same prohibition on persistence and web/transport implementation leakage; their explicit `ASP.NET Core` mentions were rewritten into implementation-role language. The other 77 files were byte-identical.
- This pass correctly documents the change as a deliberate **evolved acceptance criterion**, not as a bug that originally existed in all candidate runs.

## In-scope file paths inspected

- `L1-Restart/output/template/.claude/scripts/check-instructions.mjs`
- `L1-Restart/output/template/.claude/scripts/check-architecture.mjs`
- `L1-Restart/output/template/.claude/capabilities/{architecture,persistence,backend-testing,frontend}/`
- `L1-Restart/output/template/.claude/rules/{0-core,1-architecture,2-technology,3-project}/`
- `L1-Restart/output/template/.claude/skills/`
- `L1-Restart/output/template/.claude/settings.json`
- `L1-Restart/output/template/.claude/INSTRUCTION_MAP.md`
- `L1-Restart/output/template/CLAUDE.md`
- `L1-Restart/output/REFINEMENT_REPORT.md`
- `L1-Restart/source/inventory.json`
- `L1-Restart/MANIFEST.sha256`
- `L0/output/template/.claude/tools/check-instructions.mjs` (independent parity reference)

**Research recommendation:** Preserve the AA2 result, do not reset the candidate, and make a small `iteration_after_audit_3` update restricted to L1 technology-neutrality enforcement plus the existing research report. Once the two known parity cases pass without regressions, a final bounded confirmation is justified. The independently observed gaps do not warrant another broad rewrite.
