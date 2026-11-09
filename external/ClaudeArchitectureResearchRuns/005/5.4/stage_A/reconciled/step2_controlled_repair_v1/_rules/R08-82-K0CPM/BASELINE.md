# R08 item 8.2 K0 CPM: baseline and impact

**Target.** K0's checker honors the effective `ManagePackageVersionsCentrally`, including a valid inherited setting. It rejects a disabled or overridden effective value. Central version enforcement stays.

**Original quote.** K0 `check-dependencies.cjs`: `const cpm = text.match(/<ManagePackageVersionsCentrally>...` on `Directory.Packages.props` alone, with "must be true" otherwise. Counterexamples: true in `Directory.Build.props` was wrongly rejected; true in `Directory.Packages.props` plus false in a project was wrongly accepted; a commented-out line counted.

**Mechanism.** A static walk of the MSBuild file chain, verified against the real evaluation order on this machine's SDK. Conditions, property references and imports are not evaluated: they give "not proven", except a conditional false, which is an error because it can disable the feature. The hook needs no .NET SDK, so it stays static.

**Effective-state limit.** Static reading only at hook time. The suite compares each fixture with the real `dotnet msbuild -getProperty` (.NET SDK 10.0.403, no restore, no network, `DOTNET_CLI_HOME` inside the fence). That proves the fixtures, not all real projects: command-line properties and custom imports stay unproven.

**Parity lead, not edited.** M, M1, L0, L1 and K1 keep a similar literal check on `Directory.Packages.props`. The register approves the change for K0 only. Recorded in `UNRESOLVED_DECISIONS.jsonl`.

**Related.** DEP-006; R04 exception path in the same file (regression re-run). `isManifest` now tracks `Directory.Build.props` and `Directory.Build.targets`, so the hook re-checks when they change.
