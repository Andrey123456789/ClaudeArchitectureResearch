"""PV2-03B source review on current v3 bytes: DEP-006 in K0 and M, read beside the four peers. Real MSBuild and NuGet fixtures ran in the PV2_03B suite."""
REVIEW = [
    dict(policy='DEP-006', candidate='K0', verdict='HOLDS',
         quotes=[('.claude/scripts/check-dependencies.cjs', '!centralFileAbove(files, project) && !centralImportProven(effectiveCpm(rootDir, project))'), ('docs/architecture/decision-register.md', 'any location MSBuild imports for each project is valid'),
                 ('.claude/rules/common/dependencies.md', 'the effective `ManagePackageVersionsCentrally` must be true for each project')],
         note='DEP-006 requires NuGet CPM with versions in Directory.Packages.props and names no location. K0 D-17 already said any location MSBuild imports for each project is valid; the checker now agrees: the static ancestor error yields to MSBuild proof of the import. A project with no central file still errors (static when the proof is missing, and through the evaluator).',
         counterexample='Directory.Build.props sets DirectoryPackagesPropsPath to config/Directory.Packages.props; MSBuild evaluates CPM on and imported, NuGet gives NU1008 for a pinned project version. Before PV2-03B K0 errored "no Directory.Packages.props in its directory or any parent"; now OK, as M1, L0, L1, K1.'),
    dict(policy='DEP-006', candidate='M', verdict='HOLDS',
         quotes=[('.claude/scripts/check-manifests.mjs', 'if (!centralImportProven(effectiveCpm(root, rel)))'), ('.claude/rules/dependencies.md', 'effective `ManagePackageVersionsCentrally` must be true for each project')],
         note='M NuGet rule names no location. The static "no Directory.Packages.props was found above this project" finding now stands only when MSBuild did not prove the import; the evaluator still reports every non-effective configuration.',
         counterexample='Same layout: before PV2-03B the M command errored and the M post-edit hook blocked the project edit; now OK in both, as the four peers.'),
]
