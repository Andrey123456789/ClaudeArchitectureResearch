# R04 HQ-03 / DEP-003: baseline and impact

**Target.** Floating and prerelease versions are forbidden by default. An explicit, bounded user request authorizes the canonical exception for the named package and version or range. Instruction text and checkers honor the same exception. No global disable. Compatibility and the selected exact install outcome are confirmed.

**Original.** DEP-003: "verify the current latest stable compatible version from the registry; avoid prerelease and floating versions unless explicitly requested." Checkers had no exception path for floating versions (`check-manifests` in M, M1, K1; `manifest-checks` in L0; `post-change-checks` in L1; `check-dependencies` in K0). K1's pre-command classifier also blocks a non-exact version. M1's skill had no exception for floating versions at all.

**Mechanism.** One small data file, `dependency-version-exceptions.json` at the repository root, created only when a user makes such a request; the templates do not ship it, so no candidate's file tree changes. It sits outside `.claude/` because the instruction checkers of M1, K0 and K1 fail on an unmapped file there; a test added at R05 caught that defect in the first version of this rule, and R04 was reopened and re-gated. Each candidate's own checker reads it in that candidate's own code style. It is not a new policy owner: `add-dependency` remains the owner.

**Why a record and not a comment marker.** It names package, version and manifest, shows in a diff, and cannot widen silently. An agent could still forge an entry: the checker cannot verify who asked. That limit is stated in the final report. The text duty stays with `add-dependency`.

**Related policies.** DEP-003 (owner), DEP-006 (CPM stays), DEP-001, DEP-014. Interaction with R06: a recorded version does not excuse a force flag (K1 test included here, extended at R06).

**Shared versus architecture-specific.** Equal obligation and equal record format. Only K1's pre-command classifier gates versions, so only it needed the pre-command branch; the others route and rely on post-change checks.

**Pre-change controls.** Suite before patch: 50 FAIL, 84 PASS, 2 NOT_RUN (`suite_pre.jsonl`); default-rejection tests passed on the original, acceptance and mutation tests failed, as expected.
