# M Run-01 vs Run-02 — Independent comparison

## Decision

**Select Run-02 as the M baseline for 5.3. Do not run M Run-03.**

The two runs differ substantially in wording and implementation details, but not enough in architecture to justify an ad-hoc third replicate. Their structural convergence is strong and the important variance is implementation quality, which is exactly what phase 5.3 is intended to normalize.

## Structural convergence

| Metric | Run-01 | Run-02 / pair result |
|---|---:|---:|
| Runtime files | 62 | 60 |
| Runtime bytes | 346,325 | 340,417 |
| Markdown files | 50 | 50 |
| All-file path Jaccard |  | 0.821 |
| Markdown path Jaccard |  | 0.961 |
| Skill-tree path Jaccard |  | 1.000 |

Both runs converge on the same M identity:

- flat topical `.claude/rules/`;
- the same skill topology;
- no Stability levels;
- no Kinds × Scopes taxonomy;
- no capability contracts/manifests/selection layer;
- the same M decision/loading model;
- comparable always-loaded footprint around the ~5k target.

The only rule-name topology divergence is the repository rule (`repository-layout.md` vs `repository-structure.md`). Most other path differences are enforcement implementation choices rather than competing M architectures.

## Why Run-02 wins

Run-02 is the stronger baseline because its current-protocol audit found and repaired defects that remain visible in Run-01, including:

1. broader and more correct security-rule path coverage;
2. Windows PowerShell 5.1 UTF-8 BOM handling for hook stdin;
3. several policy-strength/fidelity corrections;
4. restored V2 details;
5. cleaner duplicate-to-owner pointers;
6. a more comprehensive bounded primary/confirmation audit under protocol 5.2.2.

An independent semantic-coverage diagnostic also favored Run-02 slightly (diagnostic only, not a proof): mean best policy-to-runtime similarity was about 0.750 vs 0.737 for Run-01, and the worst match improved from about 0.297 to 0.382.

## Useful Run-01 ideas not sufficient to reverse the choice

Run-01 contains potentially useful mechanisms that Run-02 does not, notably a source-level `check-architecture.mjs`, destructive-Git confirmation, and automatic instruction-structure checking after instruction edits. They are **not** copied automatically. During refinement they may be adopted only if they address a concrete reliability gap, remain M-compatible, have low false-positive/maintenance cost, and make the result demonstrably better.

## Run-03 decision

No Run-03 is recommended for M.

Reason: a third raw generation would primarily sample wording/enforcement implementation variance while unbalancing the experiment. The two existing replicas already agree strongly on M's architecture and topology. Their quality differences are concrete defects that can be normalized in 5.3. A Run-03 would be justified only if the two replicas represented materially different M design points; they do not.
