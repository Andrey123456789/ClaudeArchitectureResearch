"""R08 item 8.2: K0 checker reads the effective ManagePackageVersionsCentrally through the MSBuild file chain instead of one literal in one file."""
REASON = '8.2: honor the effective setting including valid inheritance, reject disabled or overridden values, keep central version enforcement; conditions and imports are reported as unproven, not assumed'
POLICIES = ['DEP-006']

C = 'K0'
F = '.claude/scripts/check-dependencies.cjs'
HELPERS = r"""// Effective ManagePackageVersionsCentrally in MSBuild evaluation order: nearest Directory.Build.props, nearest
// Directory.Packages.props, the project, nearest Directory.Build.targets; the last unconditional assignment wins.
// This is a static reading. Conditions, property references and imports are not evaluated, so they are reported as
// not proven: `dotnet msbuild <project> -getProperty:ManagePackageVersionsCentrally` gives the evaluated value.
function stripXmlComments(text) {
  return text.replace(/<!--[\s\S]*?-->/g, '');
}

function cpmAssignments(text) {
  const out = [];
  for (const group of xmlElements(text, 'PropertyGroup')) {
    if (group.malformed) continue;
    for (const item of xmlElements(group.content, 'ManagePackageVersionsCentrally')) {
      if (item.malformed) continue;
      out.push({ value: item.content.trim().toLowerCase(), conditional: group.attributes.has('Condition') || item.attributes.has('Condition') });
    }
  }
  return out;
}

function nearestUp(rootDir, startDir, name) {
  for (let dir = startDir; ; dir = path.posix.dirname(dir)) {
    const rel = path.posix.join(dir, name);
    if (fs.existsSync(path.join(rootDir, rel))) return rel;
    if (dir === '.' || dir === '') return null;
  }
}

function effectiveCpm(rootDir, startDir, projectRel) {
  const buildProps = nearestUp(rootDir, startDir, 'Directory.Build.props');
  const state = { value: undefined, source: null, unproven: false, mayDisable: false };
  let importPackages = true;
  const read = (rel) => {
    const decoded = readText(path.join(rootDir, rel));
    if (decoded.error) {
      state.unproven = true;
      return '';
    }
    return stripXmlComments(decoded.text);
  };
  const apply = (rel, text) => {
    if (/<Import\b/i.test(text)) state.unproven = true;
    for (const a of cpmAssignments(text)) {
      if (a.conditional || a.value.includes('$(')) {
        state.unproven = true;
        if (a.value === 'false') state.mayDisable = true;
      } else {
        state.value = a.value;
        state.source = rel;
      }
    }
  };
  if (buildProps) {
    const text = read(buildProps);
    if (/<ImportDirectoryPackagesProps>\s*false\s*<\/ImportDirectoryPackagesProps>/i.test(text)) importPackages = false;
    apply(buildProps, text);
  }
  const packages = importPackages ? nearestUp(rootDir, startDir, 'Directory.Packages.props') : null;
  if (packages) apply(packages, read(packages));
  if (projectRel) apply(projectRel, read(projectRel));
  const targets = nearestUp(rootDir, startDir, 'Directory.Build.targets');
  if (targets) apply(targets, read(targets));
  return state;
}

function reportCpm(rel, effective, result) {
  const where = effective.source ? ` (last set in ${effective.source})` : '';
  if (effective.value === 'false') {
    result.errors.push(`${rel}: ManagePackageVersionsCentrally is effectively false${where}; it must be true (D-17, rules/common/dependencies.md § NuGet).`);
  } else if (effective.mayDisable) {
    result.errors.push(`${rel}: ManagePackageVersionsCentrally may be effectively false under a condition; it must be true (D-17, rules/common/dependencies.md § NuGet).`);
  } else if (effective.unproven) {
    result.notices.push(`${rel}: ManagePackageVersionsCentrally is not proven true: a condition, property reference or import was not evaluated. Confirm with dotnet msbuild <project> -getProperty:ManagePackageVersionsCentrally.`);
  } else if (effective.value !== 'true') {
    result.errors.push(`${rel}: ManagePackageVersionsCentrally is effectively not set in the MSBuild chain of this file; it must be true (D-17, rules/common/dependencies.md § NuGet).`);
  }
}

"""
PATCHES = [
    (C, F, """function checkPackagesProps(rel, text, result, exceptions) {
  const cpm = text.match(/<ManagePackageVersionsCentrally>\\s*(\\w+)\\s*<\\/ManagePackageVersionsCentrally>/);
  if (!cpm || cpm[1].toLowerCase() !== 'true') {
    result.errors.push(`${rel}: ManagePackageVersionsCentrally must be true (D-17, rules/common/dependencies.md § NuGet).`);
  }
""", """function checkPackagesProps(rel, text, result, exceptions) {
"""),
    (C, F, """// DEP-003 exception: a floating or prerelease version is accepted only when
""", HELPERS + """// DEP-003 exception: a floating or prerelease version is accepted only when
"""),
    (C, F, """  return name.endsWith('.csproj') || name === 'Directory.Packages.props' || name === 'package.json';
""", """  return name.endsWith('.csproj') || name === 'Directory.Packages.props' || name === 'Directory.Build.props' || name === 'Directory.Build.targets' || name === 'package.json';
"""),
    (C, F, """  if (name.endsWith('.csproj')) checkCsproj(rootDir, rel, text, result);
  else if (name === 'Directory.Packages.props') checkPackagesProps(rel, text, result, loadVersionExceptions(rootDir, result));
""", """  const dir = path.posix.dirname(rel);
  if (name.endsWith('.csproj')) {
    reportCpm(rel, effectiveCpm(rootDir, dir, rel), result);
    checkCsproj(rootDir, rel, text, result);
  } else if (name === 'Directory.Packages.props') {
    reportCpm(rel, effectiveCpm(rootDir, dir, null), result);
    checkPackagesProps(rel, text, result, loadVersionExceptions(rootDir, result));
  } else if (name === 'Directory.Build.props' || name === 'Directory.Build.targets') {
    if (text.includes('ManagePackageVersionsCentrally')) reportCpm(rel, effectiveCpm(rootDir, dir, null), result);
  }
"""),
    (C, '.claude/rules/common/dependencies.md', """- Use NuGet Central Package Management (D-17): package versions belong in `Directory.Packages.props`.""",
     """- Use NuGet Central Package Management (D-17): the effective `ManagePackageVersionsCentrally` is true wherever the MSBuild chain sets it, no project or later file disables it, and package versions belong in `Directory.Packages.props`."""),
]
