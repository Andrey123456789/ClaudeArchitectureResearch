# M1 Run-03 decision

## Decision: do not run a third raw generation

M1's raw implementation variance is high enough to **record as a finding**, but not high enough to require Run-03 before 5.3.

Reasons:

1. The two runs differ materially in file topology (path Jaccard ~0.67) and implementation strategy.
2. Despite that, the **candidate identity converges independently**: same four slots, same frame/leaf model, same static selection concept, flat M-style rules, no Levels, no Kinds × Scopes, no extra capabilities.
3. The largest differences are implementation choices inside the permitted M1 design space, not competing definitions of M1.
4. A third run would mostly estimate how frequently those implementation styles occur. It is unlikely to resolve a conceptual ambiguity that blocks refinement.
5. Run-03 would break the 2-replicate symmetry used for the other candidates and delay the higher-value controlled refinement phase.

Therefore: preserve the high variance as a **generatability/robustness penalty** for M1, select the stronger R2 baseline, and normalize known defects in 5.3.

Run-03 would only be justified if the research question changes from "find a sound representative implementation" to "estimate the probability distribution of M1 generation outcomes." That is not required for the current stage.
