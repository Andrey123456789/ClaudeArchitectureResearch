"""PV2-03 source review on current v3 bytes: DEP-006 in K0, read beside the five peers. Real MSBuild fixtures ran in the PV2_03 suite."""
REVIEW = [
    dict(policy='DEP-006', candidate='K0', verdict='HOLDS',
         quotes=[('.claude/scripts/check-dependencies.cjs', 'no Directory.Packages.props in its directory or any parent up to the repository root'), ('docs/architecture/decision-register.md', 'any location MSBuild imports for each project is valid'),
                 ('.claude/rules/common/dependencies.md', 'the effective `ManagePackageVersionsCentrally` must be true for each project')],
         note='DEP-006 requires NuGet CPM with versions in Directory.Packages.props; it names no location. K0 no longer errors on a valid nested central file; a project outside every central file still errors (static) and the MSBuild evaluation still proves per project and context that CPM is effective. Same outcome as the other five on every PV2_03 fixture.',
         counterexample='backend/Directory.Packages.props managing backend/App.Api and backend/App.Domain, no root file: before PV2-03 K0 errored "missing at the repository root (D-17)" while MSBuild evaluated CPM on; now OK, as in M, M1, L0, L1 and K1.'),
]
