# K1 / 5.3 — Independent Audit, Corrective Iteration 2

**Input:** `K1_2.zip` compared with `K1_1.zip`.  
**Disposition:** **READY TO FREEZE** for the bounded 5.3 corrective-acceptance contract; no iteration 3 recommended.

## Provenance and file identity

- Final `output/template`: **87 files**, **400,934 bytes**.
- Tree SHA-256 (SHA-256 of path-sorted per-file `sha256sum -b` listing): `52d74f3560085066f75e5ef5c8d112ba2a0680c6e34f44e068de005a3c9759e4`, independently reproduced, matching the report.
- Only two changed template files relative to K1_1: `.claude/scripts/lib.cjs`, `.claude/scripts/check-manifests.cjs`. The other **85/87** template files are byte-identical. `baseline/`, `source/`, `audit/` are byte-identical.
- `output/` contains **only** `template/` and `REFINEMENT_REPORT.md`; no `output/.work/`.
- Original `MANIFEST.sha256`: **142/144** hashes still match; two pre-existing mismatches are `GOAL_PROMPT.txt` and `REFINEMENT_TASK.md` because of the previously agreed prompt refactor. These are not introduced by iteration 2, and the immutable source trees are intact.

## Independent behavioral testing

**71/71 independently executed checks passed.** These are focused tests against the actual Node.js checkers and event dispatchers, not just a reading of the implementer's report.

1. **56 focused tests:** direct checks of both quote styles in `PackageReference`, `PackageVersion`, `ProjectReference`, `FrameworkReference`, and `Project Sdk`; expected positive/negative Clean Architecture directions; forbidden EF / ASP.NET packages and Web SDK in Domain; exact/floating central package versions; paired elements with child `Version`; reversed mixed quote styles; quoted `>`; comment exclusion; malformed attribute fail-closed. Live `PreToolUse` executions reject `TBD`, `pending`, impossible ISO calendar dates and malformed formats, and accept valid ISO dates (including a valid leap day). Baseline absent-approval rejection works. Also included syntactic checks of eleven `.cjs` files, clean instruction/manifest checker runs and the exact two-file identity check.
2. **15 preservation/integration tests:** negative structure mutations for removed persistence binding on both contract and implementation sides, illegal ENF → WF, missing ENF declaration, invalid Kind, invalid slot binding, fifth capability slot; actual `PostToolUse` detects a single-quoted EF inline-version violation, `PostToolUseFailure` (PowerShell event payload) detects ASP.NET shared framework leak, and the actual-state hook rejects new Domain → Api references; clean initial post observation; file count, tree SHA, output hygiene, unchanged original manifest discrepancies, and seven-Kind/six-Scope identity.

The actual hooks were invoked as Node child processes with realistic JSON event payloads and a disposable Git repository; Windows/Claude Desktop live-host execution was not performed.

## Evidence inherited from unchanged files

- No modifications to K1's policy texts, rules, capability contracts/manifests, decision register, settings, hook dispatcher, command classifier, or ENF facet implementations. Corresponding previously accepted D1–D13 evidence remains applicable to *those unchanged files*. The two modified parsers were tested directly.
- K1's reported previous 196-policy audit (194 inventory + GOV-017/GOV-018) remains relevant because normative owners and policies are byte-identical. This is **not** a newly repeated full 196-owner/anchor audit.
- Iteration-2 `REFINEMENT_REPORT.md` documents **125/125** focused fixtures; the original **324/324** iteration-1 suite is historical and its deleted harness was **not** recreated or independently rerun in full.
- Always-loaded surface stays at approximately **4,849 tokens** because always-loaded files are unchanged. Seven Kinds, six Scopes, four static slots and ENF dependency checks are additionally supported by the clean instruction checker and negative mutations.

## Residual boundaries (not acceptance blockers)

- The minimalist XML reader does not implement complete MSBuild evaluation (e.g., property expansion, XML entities, conditional item evaluation). This is an explicit, inherited scope boundary, not a regression introduced by iteration 2.
- The `Date` column must contain a real exact `YYYY-MM-DD` date. This is conservative but means a non-ISO format is not accepted; the human-facing architecture-decision workflow does not independently repeat this exact format requirement.
- No live Windows PowerShell 5.1 or Claude Desktop host-activation test was performed. A PowerShell **hook event** was tested in the Node child process.
- As with any finite validator, these tests do not prove that every imaginable XML/MSBuild or free-form policy representation is recognized. No unbounded-language completeness claim is made.

## Conclusion

**Freeze K1_2 as K1's 5.3 candidate.** The two independent K1_1 blockers are fixed, the K1 identity and unchanged artifacts are preserved, 71/71 new independent tests pass, and no concrete violation of the agreed bounded 5.3 acceptance contract was discovered. Do not start K1_3 solely to rerun generic audits or expand the parser beyond the documented contract. Proceed to L1_8, the one remaining unfrozen candidate.
