# V3-Q10-PACKAGEVERSION-VERSION: declaration

Written before the first edit of this change. One logical change: every checker reads a `PackageVersion`'s version as MSBuild does, from the `Version` attribute or a `Version` child element. It reports one whose version is missing or empty. This resolves decision-queue item Q-10.

**Authority (no new policy).**
- Frozen-oracle policies, both MUST and accepted:
  - DEP-006: "versions belong in Directory.Packages.props".
  - DEP-003: choose the latest stable compatible version, with no floating version unless explicitly requested.
- Each candidate's own NuGet text already says package versions belong in `Directory.Packages.props`.
  - M1's add-dependency selects "the latest stable compatible version".
  - K0's add-dependency § 2 says "pin the verified stable version".
- Kit 74 PV2-03 requires negative fixtures for "malformed/invalid package metadata".
- Kit 74 Part C: "Other clear defects can be corrected only to implement previously approved policy semantics".
- The user's instruction of 2026-11-06: resolve within already-authorized semantics or keep in the queue.

The normative text of no candidate changes; only checker enforcement now follows the existing text.

**Evidence, recorded before the change** (`_investigation/cpm_residual_probe_before.json`, real MSBuild and NuGet offline restore):

| Fixture | MSBuild `Version` | NuGet | M | M1 | L0 | L1 | K0 | K1 |
|---|---|---|---|---|---|---|---|---|
| `<PackageVersion Include="A.B" />` (root or nested) | empty | NU1604 (no lower bound) | ERROR | **OK** | ERROR | ERROR | **OK** | ERROR |
| `Version=""` | empty | NU1604 | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR |
| `<Version>1.2.3</Version>` child | 1.2.3 | valid | **ERROR** | OK | OK | OK | OK | OK |
| `<Version></Version>` child | empty | NU1604 | ERROR | ERROR | ERROR | ERROR | **OK** | ERROR |

Three defects, one rule:
- M1 skips a `PackageVersion` with no version.
- K0 reads only the attribute, so it misses both a missing version and an empty child element.
- M reads only the attribute, so it rejects a valid pinned version written as a child element. MSBuild, NuGet and the other five accept it.

**Change.**
- M1 `.claude/scripts/check-manifests.js` `checkPackagesProps`: a `PackageVersion` with no version metadata is an ERROR. `versionOf` already reads the child element first.
- K0 `.claude/scripts/check-dependencies.cjs` `checkPackagesProps`:
  - a child `<Version>` wins over the attribute, as in M1;
  - a missing version is an error;
  - an empty child goes through the existing empty, floating or range error.
- M `.claude/scripts/check-manifests.mjs` `checkCentralProps`: a child `<Version>` wins over the attribute and goes through the existing `checkNuGetVersion`, which is unchanged.

**Not changed.**
- Floating, range and prerelease handling.
- The DEP-003 exception record and its NuGet switch.
- Deny lists, the shared MSBuild evaluator, hooks and rule text.
- L0, L1 and K1, which already behave this way.

**v3 suite update (documented, stricter).** `PV2_03_K0_CPM_ROOT.py` recorded the M1 and K0 acceptance as a documented, pre-existing difference (`NO_VERSION_EXPECTED`). This change removes that difference, so the row now requires ERROR in all six. The negative is this change's own mutations.

**Claims.** Records on the changed lines get dispositions. K0 records that list the version errors without "missing" are reworded to add it. Modality, labels and policy links are unchanged.

**Expected behavior.**
- Missing version, empty attribute, empty child, or self-closing child: ERROR in all six, at the root and nested.
- Valid child version: OK in all six.
- Floating child version: ERROR in all six.
- C01, R04, R08 and PV2-03 outcomes otherwise unchanged.
