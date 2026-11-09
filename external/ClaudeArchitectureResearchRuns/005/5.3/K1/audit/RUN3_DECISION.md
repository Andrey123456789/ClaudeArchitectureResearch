# Run-03 Decision — K1

## Decision: **NO Run-03**

A third raw generation is not justified.

## Why

The raw file trees are not near-identical (whole-tree Jaccard ~0.579), so K1 has meaningful implementation variance. But the variance is mostly decomposition and enforcement implementation, not architecture interpretation.

Both runs independently agree on all defining K1 dimensions:

- Capability -> Kind -> Scope classification;
- the same seven Kinds and the same Scope model;
- one decision register;
- scope-first standards;
- the same four slots and the same selected implementations;
- architecture as frame;
- static composition;
- contracts/manifests/facets;
- neutral-policy + implementation-facet split;
- role-based external workflow references;
- no Levels and no dynamic plugin system.

Skill topology is especially stable: 28 of the 30 union skill names are shared (~0.933 Jaccard).

A Run-03 would mainly sample another choice of rule/facet granularity. It is unlikely to resolve an ambiguity about what K1 is.

Record the observed variance as part of K1's raw-generatability result. Do not erase it by generating until two trees happen to look alike.
