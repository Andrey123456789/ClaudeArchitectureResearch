# XC08 X0421-X0480 (SEC-018, TST, WF-001..WF-007). Analyst: Step 3.
_CHK = "Each candidate's verify/code-review/add-dependency skill names its own architecture or manifest checker for relevant changes (WF-007, FULL); the checker content is scored under ARC-*/DEP-* policies."

A(["X0421-X0448", "X0453-X0459", "X0462-X0466", "X0468", "X0469", "X0471", "X0473", "X0475", "X0477"])
X("X0449", "SAME_NORM_DIFFERENT_PACKAGING", "M1 names check-architecture.js. " + _CHK, task="none")
X("X0450", "SAME_NORM_DIFFERENT_PACKAGING", "Verify before a PR/push: L0, L1, K0, K1 here; M git-workflow :102 'Run verify before preparing a PR'; M and M1 'ensure verification before pushing' (X0451).", task="none")
X("X0451", "SAME_NORM_DIFFERENT_PACKAGING", "Same as X0450 (M, M1 push wording).", task="none")
X("X0452", "SAME_NORM_DIFFERENT_PACKAGING", "Container verification (build image, startup, port/configuration, non-root, probes): K0 delivery-pipeline here; docker skills of M1, K0, K1 (X0473) and L1 (X0395) carry the same list.", task="none")
X("X0460", "REDUNDANT_DERIVED_OR_NON_NORMATIVE", "Apply migrations locally and confirm the seeder: canonical PST-005 plus the runtime smoke (WF-006) in all six; same as X0309.", task="none of consequence")
X("X0461", "SAME_NORM_DIFFERENT_PACKAGING", "L1 names check-architecture.mjs. " + _CHK, task="none")
X("X0467", "SAME_NORM_DIFFERENT_PACKAGING", "K0 names check-dependencies.cjs. " + _CHK, task="none")
X("X0470", "SAME_NORM_DIFFERENT_PACKAGING", "Use the workspace's configured test runner (inspect package.json): L0 path rule; verify skills of M :60-63 and M1, L1, K0, K1 (X0465).", task="none")
X("X0472", "SAME_NORM_DIFFERENT_PACKAGING", "Launch-profile URLs agree with configured ports (no HTTPS launch URL on an HTTP-only port): M1, L1, K0, K1 here, L0 X0476, M swagger :47-48 (X0040).", task="none")
X("X0476", "SAME_NORM_DIFFERENT_PACKAGING", "L0 copy of X0472.", task="none")
X("X0474", "SAME_NORM_DIFFERENT_PACKAGING", "K0 scaffold verification runs its checker; same as X0231.", task="none")
X("X0478", "SAME_NORM_DIFFERENT_PACKAGING", "An optional formatter is not a mandatory CI gate without adoption: M, M1, L1 here, L0 and K1 X0479, K0 X0480.", task="none")
X("X0479", "SAME_NORM_DIFFERENT_PACKAGING", "Same as X0478 (L0, K1).", task="none")
X("X0480", "SAME_NORM_DIFFERENT_PACKAGING", "Same as X0478 (K0).", task="none")
