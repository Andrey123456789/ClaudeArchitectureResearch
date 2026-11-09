"""PV2-03B patches: the static ancestor check for a central package file yields to MSBuild's per-project proof of the import (K0, M). See DECLARATION.md."""
REASON = 'PV2-03 (approved), completed: a central file that MSBuild imports for the project from outside its ancestor folders (DirectoryPackagesPropsPath) is valid; the static ancestor check stands only when the MSBuild proof is missing.'
POLICIES = ['DEP-006']
EVIDENCE = '_investigation/cpm_residual_probe_before.json: with DirectoryPackagesPropsPath MSBuild evaluates CPM on and the file imported and NuGet enforces CPM (NU1008), yet K0 (repository check) and M (command and post-edit hook) error; M1, L0, L1 and K1 accept.'
PROVEN = r"""// True when MSBuild evaluated the project and found Central Package Management on with a central file imported in every context.
function centralImportProven(outcome) {
  return !outcome.notRun && !outcome.errors.some((e) => /^(effective ManagePackageVersionsCentrally is|Directory\.Packages\.props is not imported|could not be evaluated)/.test(e));
}
"""
PATCHES = [
    ('K0', '.claude/scripts/check-dependencies.cjs',
     r"""// D-17: a project needs a Directory.Packages.props in its own directory or an ancestor inside the repository,
// which is where MSBuild looks for it (the nearest file wins). The repository root is the typical place, not a
// requirement; the MSBuild evaluation proves per project that the file is imported and Central Package
// Management is effectively on.
function centralFileAbove(files, project) {""",
     r"""// D-17: MSBuild imports the Directory.Packages.props in a project's own directory or nearest ancestor, or the file
// DirectoryPackagesPropsPath names. The repository root is the typical place, not a requirement. The MSBuild evaluation
// proves per project that a central file is imported and Central Package Management is effectively on; the static
// ancestor check stands in only when that proof is missing (no SDK, a failed evaluation, or no import found).
function centralFileAbove(files, project) {"""),
    ('K0', '.claude/scripts/check-dependencies.cjs',
     r"""function checkRepository(rootDir) {
  const total = { errors: [], notices: [], notRun: [], files: [] };
  const reported = new Set();
  const files = findManifests(rootDir);
  for (const project of files.filter((f) => f.endsWith('.csproj'))) {
    if (!centralFileAbove(files, project)) {""",
     PROVEN + r"""
function checkRepository(rootDir) {
  const total = { errors: [], notices: [], notRun: [], files: [] };
  const reported = new Set();
  const files = findManifests(rootDir);
  for (const project of files.filter((f) => f.endsWith('.csproj'))) {
    if (!centralFileAbove(files, project) && !centralImportProven(effectiveCpm(rootDir, project))) {"""),
    ('M', '.claude/scripts/check-manifests.mjs',
     r"""function centralVersions(propsFile) {""",
     PROVEN + r"""
function centralVersions(propsFile) {"""),
    ('M', '.claude/scripts/check-manifests.mjs',
     r"""    const propsFile = findCentralProps(root, file);
    if (!propsFile) {
      result.violations.push({ file: rel, message: 'package references exist but no Directory.Packages.props was found above this project (.claude/rules/dependencies.md, NuGet)' });
    } else {""",
     r"""    const propsFile = findCentralProps(root, file);
    if (!propsFile) {
      // MSBuild may import a central file from elsewhere (DirectoryPackagesPropsPath); its proof for this project decides.
      // Without the proof (no SDK, a failed evaluation, or no import found) the static finding stands.
      if (!centralImportProven(effectiveCpm(root, rel))) {
        result.violations.push({ file: rel, message: 'package references exist but no Directory.Packages.props was found above this project (.claude/rules/dependencies.md, NuGet)' });
      }
    } else {"""),
]
