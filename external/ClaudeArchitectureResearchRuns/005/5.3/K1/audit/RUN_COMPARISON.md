# K1 Run-01 vs Run-02

## Reproducibility / variance

The implementations have moderate file-level variance:

- Run-01 runtime paths: 84;
- Run-02 runtime paths: 85;
- common runtime paths: 62;
- union runtime paths: 107;
- whole-tree path Jaccard: **0.579**.

The variance is concentrated in decomposition rather than architecture identity:

- skill-name Jaccard: **28 / 30 = 0.933**;
- rule-path Jaccard: **13 / 26 = 0.500**;
- capability-file Jaccard: **8 / 12 = 0.667**.

Run-01 owns module workflow facets as `capabilities/.../workflow-facet.md` files. Run-02 distributes the same logical facets into mechanism-appropriate workflow/private-reference surfaces, including `persistence-change` and project-structure references.

## Raw acceptance

Both generation reports claim:

- PASS;
- zero trigger-role deltas;
- zero minimum-scope failures;
- 2/2 shared invariants represented;
- zero unresolved broken references;
- zero known Windows hook defects.

Independent audit agrees with the policy/structure coverage at a high level, but does **not** accept the hook-defect claim for Run-02.

## Independent lexical diagnostics

These are diagnostics only, not semantic correctness or promotion metrics.

Using TF-IDF best-match comparison between each of the 194 normalized policies and generated Markdown paragraphs:

- Run-01 mean best match: **~0.4146**; policies below 0.25: 19.
- Run-02 mean best match: **~0.4150**; policies below 0.25: 17.

Using 640 source V2 Markdown sections extracted from the frozen baseline:

- Run-01 mean best match: **~0.4630**; sections below 0.25: 110.
- Run-02 mean best match: **~0.4788**; sections below 0.25: 89.

The measurements do not prove completeness, but they provide no reason to prefer the larger Run-01 corpus for preservation.

## Structural-checker comparison

A decisive difference is the K dependency graph.

Diagnostic mutation:

- append a DEC conformance reference from `docs/architecture/decision-register.md` to the STD artifact `.claude/rules/backend/coding-style.md`.

Result:

- Run-01 checker: **PASS**;
- Run-02 checker: **FAIL**, correctly reporting that DEC must not depend on STD in `WF -> KNW -> STD -> DEC -> OP` direction.

Run-02 therefore provides the stronger starting implementation of the K axis.

However, Run-02's capability-binding checker is incomplete: replacing the persistence module manifest's real `Binds: architecture ...` declaration with `Binds: —` still produces a clean PASS. This is a confirmed K1-specific defect for 5.3.

## Enforcement comparison

Run-01 is stronger in several runtime details:

- its launcher searches upward from the current working directory and successfully targets a real Git worktree in the independent test;
- its PostToolUse matcher includes Bash and PowerShell;
- its stdin parser tolerates a UTF-8 BOM.

Run-02 is more compact, but:

- locates the dispatcher from `CLAUDE_PROJECT_DIR` and then derives the inspected root from the dispatcher's own location, which makes worktree edits point back at the main checkout;
- PostToolUse matches only Edit/Write/MultiEdit;
- parses the untrimmed raw string after testing `raw.trim()`, so a UTF-8 BOM breaks JSON parsing;
- has no fail-closed setting for the critical PreToolUse policy guard.

Both runs have incomplete command classification and same-path Stop deduplication weaknesses.

## Conclusion

Use Run-02, then repair its concrete enforcement and K1-conformance defects. The sibling runs differ enough to record non-trivial generatability variance, but not enough to indicate competing definitions of K1.
