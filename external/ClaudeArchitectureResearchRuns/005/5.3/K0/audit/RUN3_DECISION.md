# Run-03 Decision — K0

## Decision: **NO Run-03**

A third raw K0 generation is not justified.

## Reasoning

The two runs have meaningful but moderate file-level variance:

- whole-tree path Jaccard ~0.753;
- STD rule Jaccard ~0.611;
- skill-name Jaccard 1.000.

More importantly, both independently converge on the same defining architecture: seven Kinds, the same Scope model, one decision register, scope-first STD rules, mechanism aligned to Kind, embedded technologies, and no Levels/capability machinery.

The differences are mainly decomposition choices (`operations` vs `hosting`, `outbound-http` vs `integrations`, separate vs merged frontend security) and enforcement implementation details.

A third raw run would primarily sample another decomposition rather than resolve an architectural ambiguity. The observed variance should remain part of K0's generatability evidence rather than be hidden by adding a tie-breaker run.
