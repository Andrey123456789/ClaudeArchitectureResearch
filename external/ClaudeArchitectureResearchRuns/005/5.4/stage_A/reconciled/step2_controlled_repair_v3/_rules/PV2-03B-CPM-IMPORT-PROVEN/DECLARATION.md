# PV2-03B-CPM-IMPORT-PROVEN: declaration

Written before the first edit of this change. One logical change. It completes PV2-03, which is already approved.

**Authority.**
- Kit 74 Part B PV2-03: "Allow valid nested/otherwise legitimately effective central package configurations, validated using per-project effective MSBuild properties, matching the agreed CPM semantics of all six candidates."
- Decision D-PV2-03.
- Kit 74 Part C: "Other clear defects can be corrected only to implement previously approved policy semantics."
- The user's instruction of 2026-11-06: test a valid, explicitly imported central file that is not in an ancestor folder of the project, and correct a checker that rejects a genuinely valid effective CPM configuration as a separate gated change under PV2-03.

No new policy choice is made.

**Evidence, recorded before the change** (`_investigation/cpm_residual_probe_before.json`, real MSBuild 10.0.403 and NuGet offline restore).

A central file outside every ancestor folder of the project, named by `DirectoryPackagesPropsPath`:
- This is the SDK's own mechanism: `NuGet.props` imports `$(DirectoryPackagesPropsPath)` and only then sets `CentralPackageVersionsFileImported`. `NuGet.targets` enables CPM only when both `ManagePackageVersionsCentrally` and `CentralPackageVersionsFileImported` are true.
- MSBuild evaluates CPM on and the file imported.
- NuGet enforces CPM: a version in the project gives NU1008, and a versionless reference resolves through the central version (only NU1101, the package is absent from the empty feed).
- K0 rejects it in its repository check: `centralFileAbove()` says "no Directory.Packages.props in its directory or any parent up to the repository root".
- M rejects it in its command and in its post-edit hook, where it blocks the edit: `findCentralProps()` says "package references exist but no Directory.Packages.props was found above this project".
- M1, L0, L1 and K1 accept it.
- Fixtures P1 to P4: one project; two projects in different folders; a central file with another name; the path set in a nested `Directory.Build.props`.

The interim review's example, where the project file itself `<Import>`s `config/Directory.Packages.props`, is **not** effective CPM:
- The SDK does not mark the file imported (`CentralPackageVersionsFileImported` is empty).
- NuGet ignores CPM: a versionless reference gives NU1015, and a pinned version gives no NU1008.
- All six already reject it through the shared evaluator ("Directory.Packages.props is not imported"). This is correct and unchanged.
- The same holds for a plain `<Import>` from `Directory.Build.props` (N1).

**Change.**
- In K0 `.claude/scripts/check-dependencies.cjs` (`checkRepository`) and in M `.claude/scripts/check-manifests.mjs` (`checkProject`), the static "no central file in an ancestor folder" error now stands only when MSBuild did not prove the project's central import. That means one of these holds:
  - the evaluation is NOT_RUN (no SDK, time budget);
  - it failed;
  - it found `ManagePackageVersionsCentrally` not true;
  - it found the central file not imported.
- When MSBuild proves CPM on and a central file imported in every evaluated context, the static guess no longer overrides the proof.
- Both error messages are unchanged.

**Not changed.**
- The shared MSBuild evaluator (byte-identical in all six).
- Every other check: versions in projects, floating and range versions, the DEP-003 exception and its NuGet switch, deny lists, project references and hooks.
- The no-SDK behavior: K0 and M keep their static fallback, so a project with no ancestor central file still errors there without the SDK, as before. The other four report NOT_RUN.
- The text: K0 D-17 already says "any location MSBuild imports for each project is valid", and M's NuGet rule names no location.
- M1, L0, L1 and K1 are not touched.

**Claims.** Records on the changed lines get dispositions. K0 FG-K0-36395ffe06 and FG-K0-73dd5d1170, which state the static check as an unconditional error, are reworded to the conditional form. Labels, policy links and modality are unchanged: the per-project CPM obligation (DEP-006) is the same; only the false rejection goes.

**Expected behavior.**
- P1 to P4: OK in all six.
- N1 to N5 (a plain import, the review example, a path to a missing file, CPM off in the imported file, a version pinned in the project): ERROR in all six.
- The PV2-03, C01 and R08 fixtures are unchanged.

**Residual, reported, not changed.**
- Without the SDK, K0 and M error statically where the other four report NOT_RUN. Neither counts as passed.
- No candidate checks the name of a central file that MSBuild imports through `DirectoryPackagesPropsPath`. The rule texts say versions belong in `Directory.Packages.props`, so this is uniform across all six and goes to the decision queue.
