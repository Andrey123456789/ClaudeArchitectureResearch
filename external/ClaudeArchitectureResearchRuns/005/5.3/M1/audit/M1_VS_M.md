# M1 vs M — current interpretation before code-generation benchmark

This comparison separates **raw template generation cost/robustness** from the still-unanswered question of downstream coding performance.

## Observed raw-template cost

Earlier M pair (selected baseline M-R2):

- ~60 runtime files;
- ~340,417 bytes;
- ~4.8k always-loaded tokens;
- current-session usage ~63% in both runs;
- path Jaccard between M replicas ~0.961.

M1 selected R2 / pair:

- R2: 80 files, 368,816 bytes, ~5.568k always-loaded tokens;
- M1 current-session usage: R1 81%, R2 72%, mean **76.5%**;
- M1 path Jaccard between replicas ~0.670.

Relative to selected M-R2, selected M1-R2 therefore adds approximately:

- **+20 files / +33%** file count;
- **+28.4 KB / +8.3%** total bytes;
- **+~0.77k / +~16%** always-loaded tokens;
- **+13.5 percentage points / ~21% relative** average generation-session usage versus M's ~63%;
- substantially lower raw structural reproducibility.

## What that cost buys

M1 adds capabilities that M intentionally does not have:

- explicit stable replacement contracts;
- module manifests and static selection;
- implementation leak boundaries;
- architecture frame vs leaf-capability integration semantics;
- optional frontend removal as a declared slot operation;
- a place to reason mechanically about replacing EF Core, NUnit, Angular, or the architecture frame without template-wide hunting.

These are real capabilities, not decorative metadata.

## Current judgment

**M is clearly better on simplicity, generatability, and reproducibility.** M1 is not a free improvement over M.

**M1 can still be the better architecture if later maintenance/replacement tasks exploit its boundaries enough to repay the cost.** That question cannot be settled by this template-generation phase alone.

The key downstream test is therefore not ordinary feature coding only. The code-generation benchmark should include scenarios that stress the reason M1 exists: technology/provider replacement, optional frontend removal, frame/leaf substitution, and maintenance of cross-cutting capability contracts. If M1 does not win materially on those scenarios, M's simpler architecture should be favored.

M1 also provides a clean way to estimate how much complexity comes from the capability mechanism itself. Comparing M→M1, L0→L1, and K0→K1 will help separate capability cost from the cost of Stability-first or Kinds × Scopes organization.
