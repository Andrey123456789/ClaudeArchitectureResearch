# PV2-03-K0-CPM-ROOT: declaration

Written before the first edit of this change. Authority: kit 74 Part B PV2-03 and decision D-PV2-03 (approved; no further approval needed).

**Change.** K0 `.claude/scripts/check-dependencies.cjs` no longer errors because `Directory.Packages.props` is not at the repository root ("missing at the repository root (D-17)"). It now errors for each `.csproj` that has no `Directory.Packages.props` in its own directory or an ancestor inside the repository, which is where MSBuild looks for it (the nearest file wins). This is the static check M already makes ("no Directory.Packages.props was found above this project"). The MSBuild effective-state evaluation from v2 C01, byte-identical in all six, still proves per project and per context that the central file is imported and Central Package Management is effectively on.

**Authoritative text.** D-17 in `docs/architecture/decision-register.md` and the NuGet bullet in `.claude/rules/common/dependencies.md` say the root is the typical place, and that any location MSBuild imports for each project is valid. The solution-layout example tree keeps the root file as the typical layout.

**Not changed.** Versionless `PackageReference` entries, version and floating-version checks, the recorded DEP-003 exception and its NuGet switch, deny-lists, project-reference and test-reference checks, the hooks. No other candidate is touched.

**Claims and policies.** `DEP-006`. K0 records on the changed lines get dispositions; claims that stated the root requirement are reworded.

**Expected behavior.** Nested central file managing all projects: OK in all six. A project with no central file above it: error in all six (K0 and M statically, all six through MSBuild). Overridden or disabled CPM, a version in the project file, and an invalid `PackageVersion`: errors in all six. Root central file: OK as before. When the .NET SDK is missing the evaluation reports NOT_RUN as in C01.

**Regression adaptation.** v2 `final_audit_v2.py` asserted "K0 errors under D-17, the other five accept" for a central file below the root; v3's audit replaces that row with the same-task check that all six accept a valid nested layout. No v1 or v2 suite asserted the K0 root error.
