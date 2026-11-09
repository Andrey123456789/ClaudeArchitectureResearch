"""PV2-03 patches: K0 central-package placement follows MSBuild discovery instead of a repository-root mandate. See DECLARATION.md."""
REASON = 'PV2-03 (approved): remove the K0-only repository-root requirement for Directory.Packages.props; keep per-project effective CPM verification (DEP-006).'
POLICIES = ['DEP-006']
EVIDENCE = 'v2 same-task audit: a valid central file below the root errors only in K0 ("Directory.Packages.props is missing at the repository root (D-17)") while MSBuild evaluates CPM on in all six.'
CHK = '.claude/scripts/check-dependencies.cjs'
PATCHES = [
    ('K0', CHK,
     """function checkRepository(rootDir) {
  const total = { errors: [], notices: [], notRun: [], files: [] };
  const reported = new Set();
  const files = findManifests(rootDir);
  if (files.some((f) => f.endsWith('.csproj')) && !files.includes('Directory.Packages.props')) {
    total.errors.push('Directory.Packages.props is missing at the repository root (D-17).');
  }
""",
     """// D-17: a project needs a Directory.Packages.props in its own directory or an ancestor inside the repository,
// which is where MSBuild looks for it (the nearest file wins). The repository root is the typical place, not a
// requirement; the MSBuild evaluation proves per project that the file is imported and Central Package
// Management is effectively on.
function centralFileAbove(files, project) {
  for (let dir = path.posix.dirname(project); ; dir = path.posix.dirname(dir)) {
    const candidate = dir === '.' ? 'Directory.Packages.props' : `${dir}/Directory.Packages.props`;
    if (files.includes(candidate)) return candidate;
    if (dir === '.' || dir === '/' || dir === '') return null;
  }
}

function checkRepository(rootDir) {
  const total = { errors: [], notices: [], notRun: [], files: [] };
  const reported = new Set();
  const files = findManifests(rootDir);
  for (const project of files.filter((f) => f.endsWith('.csproj'))) {
    if (!centralFileAbove(files, project)) {
      total.errors.push(`${project}: no Directory.Packages.props in its directory or any parent up to the repository root, so Central Package Management cannot apply (D-17).`);
    }
  }
"""),
    ('K0', 'docs/architecture/decision-register.md',
     """| D-17 | Shared .NET build configuration: repository-level `Directory.Build.props` for genuinely shared build settings and `Directory.Packages.props` for Central Package Management; project-specific settings stay in their own projects. |""",
     """| D-17 | Shared .NET build configuration: repository-level `Directory.Build.props` for genuinely shared build settings and `Directory.Packages.props` for Central Package Management (typically at the repository root; any location MSBuild imports for each project is valid); project-specific settings stay in their own projects. |"""),
    ('K0', '.claude/rules/common/dependencies.md',
     """no project, condition or later file may turn it off, and package versions belong in `Directory.Packages.props`.""",
     """no project, condition or later file may turn it off, and package versions belong in `Directory.Packages.props` (typically at the repository root; a nested one that MSBuild imports for each project is equally valid)."""),
]
