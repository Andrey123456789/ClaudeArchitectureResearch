# M1 baseline selection for iteration 5.3

## Decision

**Select M1 / Run-02 as the refinement baseline.**

Run-01 remains a valid M1 realization and useful evidence, but Run-02 is the stronger starting implementation overall.

## Independent comparison summary

| Property | Run-01 | Run-02 | Audit view |
|---|---:|---:|---|
| Runtime files | 77 | 80 | R1 is smaller by file count |
| Runtime bytes | 397,827 | 368,816 | R2 is ~7.3% smaller by bytes |
| Markdown files | 65 | 67 | close |
| Markdown bytes | 347,952 | 303,524 | R2 is materially more concise |
| Flat rule files | 14 | 14 | same M1 shape |
| Skills | 28 | 29 | R2 adds `persistence-change` |
| Generated checker result | PASS | PASS | neither self-report is accepted blindly |
| Always-loaded estimate | ~5,640 tokens | ~5,568 tokens | R2 slightly lower; both near the experimental target |
| PreToolUse dependency routing | absent | present | strong R2 advantage |
| PostToolUse / Stop enforcement | present | present | both |
| Four capability slots | yes | yes | both preserve M1 identity |
| Stability levels / `Level:` | absent | absent | both preserve M1 identity |
| Kinds × Scopes / `Kind:` | absent | absent | both preserve M1 identity |

The generated file-path Jaccard similarity is only **63 / 94 = 0.6702**, much lower than the earlier M pair. Only one common-path file is byte-identical. This is important generatability variance, but the architectural design point is still stable: both runs independently converge on the same four static capability slots, flat M-style topical rules, no level hierarchy, no Kind taxonomy, and the same general owner/loading model.

## Why Run-02 wins

1. It has **PreToolUse** dependency routing; Run-01 can only react after a command has already run.
2. Its enforcement is more systematically decomposed (`common.js`, dependency command classifier, manifest checker, hook-output helper).
3. It is materially more concise in total bytes despite three additional files.
4. It adds an explicit `persistence-change` workflow, which gives co-change enforcement a clear procedure owner.
5. It has no root-relative launcher failure when `CLAUDE_PROJECT_DIR` is available; Run-01 uses `node .claude/hooks/...` and fails outright from nested cwd.
6. Its generated report/file inventory is more internally coherent and its capability planning surfaces are systematic.

## Run-01 qualities worth preserving conceptually

Do **not** mechanically merge Run-01 files. However, refinement should retain or recover these qualities when they can be proven better without regression:

- R1 preserved considerably more V2 wording/examples literally. R2 must therefore perform a targeted V2-fidelity review and restore any *materially useful* technique/details it compressed away; do not restore text merely for literal similarity.
- R1's persistence manifest expressed frame integration with stable `<role:...>` vocabulary and declared no `binds:` coupling. R2's explicit `binds` is permitted by M1, but refinement should reduce avoidable frame coupling where stable role vocabulary can express the same semantics without harming executable guidance.
- R1 used fewer always-loaded capability planning facets. Do not add further planning/meta layers to R2 without a binding reliability need.

## Promotion stance

Run-02 is a baseline, not a winner by fiat. The 5.3 result must fix every confirmed defect in `DEFECT_DOSSIER.md` and then prove no regression against the baseline and frozen source corpus.
