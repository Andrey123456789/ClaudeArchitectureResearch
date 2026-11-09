"""C01: effective CPM state in all six manifest checkers. One logical rule: DEP-006 is verified from the value MSBuild evaluates, with the routing, text owner and proof route that implement it."""
import os

from rcommon import out_path, wc_path

POLICIES = ['DEP-006', 'DEP-003']
REASON = 'User approval in kit 72: all six checkers verify the effective MSBuild ManagePackageVersionsCentrally state, not literal XML.'
EVIDENCE = 'Observed in _scratch probes and in the C01 suite: dotnet msbuild -getProperty/-getItem evaluates inheritance, conditions and imports without restore; offline restore gives NU1008, NU1010, NU1011, NU1015.'

# The evaluator is the same statements in all six, so parity can be read directly. Only the wrapper is native to each candidate.
EVALUATOR = r"""// Effective Central Package Management (DEP-006): MSBuild evaluates each project; the XML text is never taken as proof of the setting.
// Needs the .NET SDK (8.0.100 or later, for -getProperty) and no network: nothing is restored or built. A project is in violation,
// proven, or NOT_RUN when the proof is unavailable; NOT_RUN never counts as passed. Contexts: default, Configuration=Release and,
// for a multi-targeted project, each TargetFramework. Hooks share a time budget so a manifest edit stays responsive; the command has none.
const CPM_CHAIN_FILES = new Set(['Directory.Packages.props', 'Directory.Build.props', 'Directory.Build.targets']);
const CPM_QUERY = ['ManagePackageVersionsCentrally', 'CentralPackageVersionsFileImported', 'CentralPackageFloatingVersionsEnabled', 'TargetFrameworks'].map((name) => `-getProperty:${name}`).concat('-getItem:PackageReference', '-getItem:PackageVersion');
const CPM_TOOLING_GAP = /MSB1001|MSB4236|compatible \.NET SDK|No \.NET SDKs? (?:was|were) found/i;
const CPM_RUN_LIMIT_MS = 120000;
const cpmState = { budgetMs: 20000, started: 0, outcomes: new Map() };

function msbuildState(root, project, extra) {
  cpmState.started ||= Date.now();
  const left = cpmState.budgetMs ? cpmState.budgetMs - (Date.now() - cpmState.started) : CPM_RUN_LIMIT_MS;
  if (left <= 0) return { notRun: 'the hook time budget ran out; run the manifest check command' };
  const run = spawnSync('dotnet', ['msbuild', project, '-nologo', ...CPM_QUERY, ...extra], { cwd: root, encoding: 'utf8', timeout: Math.min(left, CPM_RUN_LIMIT_MS), maxBuffer: 1 << 24, windowsHide: true, env: { ...process.env, DOTNET_NOLOGO: '1', DOTNET_CLI_TELEMETRY_OPTOUT: '1' } });
  if (run.error) return { notRun: run.error.code === 'ENOENT' ? 'the .NET SDK (dotnet) is not available' : `dotnet msbuild did not finish (${run.error.code || run.error.message})` };
  const output = `${run.stdout || ''}\n${run.stderr || ''}`;
  if (run.status !== 0) {
    const line = output.split(/\r?\n/).find((l) => /error/i.test(l)) || output.trim().split(/\r?\n/)[0] || `exit code ${run.status}`;
    return CPM_TOOLING_GAP.test(output) ? { notRun: `the .NET SDK cannot evaluate it: ${line.trim().slice(0, 240)}` } : { failure: line.trim().slice(0, 300) };
  }
  try {
    return { state: JSON.parse(run.stdout) };
  } catch {
    return { notRun: 'dotnet msbuild printed no evaluation result' };
  }
}

// { errors, notices, notRun } for one project, evaluated once per process.
function effectiveCpm(root, project) {
  const key = `${root}\0${project}`;
  if (cpmState.outcomes.has(key)) return cpmState.outcomes.get(key);
  const errors = new Set();
  const notices = new Set();
  let notRun = null;
  const contexts = [['default', []], ['Configuration=Release', ['-p:Configuration=Release']]];
  for (let i = 0; i < contexts.length; i += 1) {
    const [label, extra] = contexts[i];
    const run = msbuildState(root, project, extra);
    if (run.notRun) {
      notRun = run.notRun;
      break;
    }
    if (run.failure) {
      errors.add(`could not be evaluated by MSBuild in context ${label}: ${run.failure}`);
      break;
    }
    const props = run.state.Properties || {};
    const items = run.state.Items || {};
    if (i === 0) {
      for (const tfm of (props.TargetFrameworks || '').split(';').map((t) => t.trim()).filter(Boolean)) contexts.push([`TargetFramework=${tfm}`, [`-p:TargetFramework=${tfm}`]]);
    }
    const value = (props.ManagePackageVersionsCentrally || '').trim().toLowerCase();
    if (value !== 'true') {
      errors.add(`effective ManagePackageVersionsCentrally is "${value || 'unset'}" in context ${label}; it must be true`);
      continue;
    }
    if ((props.CentralPackageVersionsFileImported || '').trim().toLowerCase() !== 'true') {
      errors.add(`Directory.Packages.props is not imported in context ${label}; the setting alone manages nothing`);
      continue;
    }
    const declared = new Map((items.PackageVersion || []).map((item) => [item.Identity.toLowerCase(), item.Version || '']));
    for (const ref of items.PackageReference || []) {
      if (String(ref.IsImplicitlyDefined).toLowerCase() === 'true') continue;
      if (ref.Version) errors.add(`effective PackageReference ${ref.Identity} has version ${ref.Version} in context ${label}; versions belong in Directory.Packages.props`);
      else if (!ref.VersionOverride && !declared.has(ref.Identity.toLowerCase())) errors.add(`effective PackageReference ${ref.Identity} has no PackageVersion in context ${label}`);
    }
    if ((props.CentralPackageFloatingVersionsEnabled || '').trim().toLowerCase() !== 'true') {
      for (const [id, version] of declared) {
        if (version.includes('*')) notices.add(`PackageVersion ${id} ${version} floats: restore rejects it (NU1011) unless CentralPackageFloatingVersionsEnabled is true`);
      }
    }
  }
  const outcome = { errors: [...errors], notices: [...notices], notRun };
  cpmState.outcomes.set(key, outcome);
  return outcome;
}

function cpmNotRunMessage(reason) {
  return `NOT_RUN effective Central Package Management was not proven: ${reason}. Report this check as NOT RUN, not as passed; confirm with dotnet msbuild <project> -getProperty:ManagePackageVersionsCentrally.`;
}
"""

DEP_SENTENCE = 'What counts is the value MSBuild evaluates: the effective `ManagePackageVersionsCentrally` must be true for each project, whether it is set in `Directory.Packages.props` or inherited, and no project, condition, or later file may turn it off.'
FLOAT_SENTENCE = 'For a floating NuGet version, also set `CentralPackageFloatingVersionsEnabled` to true in `Directory.Packages.props`, because restore rejects the version otherwise (NU1011); that NuGet property does not widen the exception, and the manifest checks keep rejecting every other floating version.'
VERIFY_SENTENCE = 'A `NOT_RUN` line or exit code 3 from the manifest check means the MSBuild proof of effective Central Package Management did not run: report it as NOT RUN, never as passed.'


def between(c, rel, start, end):
    """Exact text from `start` up to, not including, `end`, in the file's own line endings normalized to LF."""
    snap = out_path('_rules', 'C01-CPM-EFFECTIVE', 'before', c, *rel.split('/'))
    with open(snap if os.path.exists(snap) else wc_path(c, rel), encoding='utf-8', newline='') as f:
        s = f.read().replace('\r\n', '\n')
    a = s.index(start)
    b = s.index(end, a)
    return s[a:b]


PATCHES = []


def add(c, rel, old, new):
    PATCHES.append((c, rel, old, new))


# ---------------------------------------------------------------- M
R = '.claude/scripts/check-manifests.mjs'
add('M', R, "// Exit codes: 0 = no violations, 1 = violations found, 2 = the checker could not run.\n", "// Exit codes: 0 = no violations, 1 = violations found, 2 = the checker could not run,\n// 3 = no violations found, but the proof of effective Central Package Management did\n// not run (report it as NOT RUN, never as passed).\n")
add('M', R, "import { readFileSync, readdirSync, existsSync } from 'node:fs';\n", "import { spawnSync } from 'node:child_process';\nimport { readFileSync, readdirSync, existsSync } from 'node:fs';\n")
add('M', R, "const result = { violations: [], notes: [], checked: [], versionExceptions: [] };", "const result = { violations: [], notes: [], notRun: [], checked: [], versionExceptions: [] };")
add('M', R, """    } else if (name === 'package.json') {
      checkPackageJson(root, file, result);
    } else {
      continue;
    }
    result.checked.push(rel);
  }
  return result;
}
""", """    } else if (name === 'package.json') {
      checkPackageJson(root, file, result);
    } else if (!CPM_CHAIN_FILES.has(name)) {
      continue;
    }
    result.checked.push(rel);
  }
  reportCpm(root, targets, result);
  return result;
}

// The projects whose effective state these targets can change: a project itself, or every project below a chain file.
function cpmProjects(root, targets) {
  const projects = new Set();
  const all = () => discover(root).filter((file) => basename(file).toLowerCase().endsWith('.csproj')).map((file) => toRel(root, file));
  for (const file of targets) {
    const rel = toRel(root, file);
    if (rel === null || !existsSync(file)) continue;
    const name = basename(file);
    if (name.toLowerCase().endsWith('.csproj')) projects.add(rel);
    else if (CPM_CHAIN_FILES.has(name)) {
      const dir = dirname(rel);
      for (const project of all()) if (dir === '.' || project.startsWith(`${dir}/`)) projects.add(project);
    }
  }
  return [...projects];
}

function reportCpm(root, targets, result) {
  for (const project of cpmProjects(root, targets)) {
    const outcome = effectiveCpm(root, project);
    for (const message of outcome.errors) result.violations.push({ file: project, message: `${message} (.claude/rules/dependencies.md, NuGet)` });
    for (const message of outcome.notices) result.notes.push({ file: project, message: `${message} (add-dependency)` });
    if (outcome.notRun) result.notRun.push({ file: project, message: cpmNotRunMessage(outcome.notRun) });
  }
}
""")
add('M', R, "  for (const n of result.notes) lines.push(`NOTE      ${n.file}: ${n.message}`);\n", "  for (const n of result.notes) lines.push(`NOTE      ${n.file}: ${n.message}`);\n  for (const n of result.notRun) lines.push(`NOT_RUN   ${n.file}: ${n.message}`);\n")
add('M', R, "        if (lower.endsWith('.csproj') || entry.name === 'Directory.Packages.props' || entry.name === 'package.json') {", "        if (lower.endsWith('.csproj') || CPM_CHAIN_FILES.has(entry.name) || entry.name === 'package.json') {")
add('M', R, """  const xml = readXml(file);
  if (!/<ManagePackageVersionsCentrally>\\s*true\\s*<\\/ManagePackageVersionsCentrally>/i.test(xml)) {
    result.violations.push({ file: rel, message: 'ManagePackageVersionsCentrally is not enabled (.claude/rules/dependencies.md, NuGet)' });
  }
  for (const { attrs } of elements(xml, 'PackageVersion')) {""", """  const xml = readXml(file);
  for (const { attrs } of elements(xml, 'PackageVersion')) {""")
add('M', R, """  const packageRefs = elements(xml, 'PackageReference');
  if (/<ManagePackageVersionsCentrally>\\s*false\\s*<\\/ManagePackageVersionsCentrally>/i.test(xml)) {
    result.violations.push({ file: rel, message: 'project opts out of Central Package Management (.claude/rules/dependencies.md, NuGet)' });
  }
  let central = null;""", """  const packageRefs = elements(xml, 'PackageReference');
  let central = null;""")
add('M', R, "function isMain() {\n", EVALUATOR + "\nfunction isMain() {\n")
add('M', R, """  const result = checkManifests(root, process.argv.slice(2).map((file) => resolve(process.cwd(), file)));
  for (const line of formatResult(result)) process.stdout.write(`${line}\\n`);
  process.stdout.write(`check-manifests: ${result.checked.length} manifest(s) checked, ${result.violations.length} violation(s), ${result.notes.length} note(s)\\n`);
  process.exit(result.violations.length > 0 ? 1 : 0);""", """  cpmState.budgetMs = 0;
  const result = checkManifests(root, process.argv.slice(2).map((file) => resolve(process.cwd(), file)));
  for (const line of formatResult(result)) process.stdout.write(`${line}\\n`);
  process.stdout.write(`check-manifests: ${result.checked.length} manifest(s) checked, ${result.violations.length} violation(s), ${result.notes.length} note(s), ${result.notRun.length} not run\\n`);
  process.exit(result.violations.length > 0 ? 1 : result.notRun.length > 0 ? 3 : 0);""")
add('M', '.claude/hooks/file-change.mjs', "//   .csproj, Directory.Packages.props, package.json -> manifest check\n", "//   .csproj, Directory.Packages.props, Directory.Build.props, Directory.Build.targets,\n//   package.json -> manifest check\n")
add('M', '.claude/hooks/file-change.mjs', "const isManifest = name.toLowerCase().endsWith('.csproj') || name === 'Directory.Packages.props' || name === 'package.json';", "const isManifest = name.toLowerCase().endsWith('.csproj') || name === 'Directory.Packages.props' || name === 'Directory.Build.props' || name === 'Directory.Build.targets' || name === 'package.json';")
add('M', '.claude/hooks/hook-io.mjs', "// Manifests (.csproj, Directory.Packages.props, package.json) whose content\n", "// Manifests (.csproj, the MSBuild chain files, package.json) whose content\n")
add('M', '.claude/hooks/hook-io.mjs', "const MANIFEST_PATHSPECS = [':(glob,icase)**/*.csproj', ':(glob)**/Directory.Packages.props', ':(glob)**/package.json'];", "const MANIFEST_PATHSPECS = [':(glob,icase)**/*.csproj', ':(glob)**/Directory.Packages.props', ':(glob)**/Directory.Build.props', ':(glob)**/Directory.Build.targets', ':(glob)**/package.json'];")
add('M', '.claude/hooks/hook-io.mjs', "  return name.toLowerCase().endsWith('.csproj') || name === 'Directory.Packages.props' || name === 'package.json';", "  return name.toLowerCase().endsWith('.csproj') || name === 'Directory.Packages.props' || name === 'Directory.Build.props' || name === 'Directory.Build.targets' || name === 'package.json';")
add('M', '.claude/MAP.md', "manifest checks after editing `.csproj`, `Directory.Packages.props`, `package.json`", "manifest checks after editing `.csproj`, `Directory.Packages.props`, `Directory.Build.props`, `Directory.Build.targets`, `package.json`")
add('M', '.claude/rules/dependencies.md', """`Directory.Packages.props`, and project `PackageReference` entries are
versionless by default — do not duplicate centrally managed versions in
individual `.csproj` files. Keep""", """`Directory.Packages.props`, and project `PackageReference` entries are
versionless by default — do not duplicate centrally managed versions in
individual `.csproj` files. What counts is the value MSBuild evaluates: the
effective `ManagePackageVersionsCentrally` must be true for each project,
whether it is set in `Directory.Packages.props` or inherited, and no project,
condition, or later file may turn it off. Keep""")
add('M', '.claude/skills/add-dependency/SKILL.md', """rejecting every other floating or prerelease version; there is no global switch.
Confirm""", """rejecting every other floating or prerelease version; there is no global switch.
For a floating NuGet version, also set `CentralPackageFloatingVersionsEnabled` to
true in `Directory.Packages.props`, because restore rejects the version otherwise
(NU1011); that NuGet property does not widen the exception, and the manifest
checks keep rejecting every other floating version.
Confirm""")
add('M', '.claude/skills/verify/SKILL.md', """```bash
node .claude/scripts/check-manifests.mjs
```
""", """```bash
node .claude/scripts/check-manifests.mjs
```

A `NOT_RUN` line or exit code 3 from the manifest check means the MSBuild proof of
effective Central Package Management did not run: report it as NOT RUN, never as
passed.
""")

# ---------------------------------------------------------------- M1
R = '.claude/scripts/check-manifests.js'
add('M1', R, "//   node \"$(git rev-parse --show-toplevel)/.claude/scripts/check-manifests.js\" [file ...]   (default: all manifests)\n", "//   node \"$(git rev-parse --show-toplevel)/.claude/scripts/check-manifests.js\" [file ...]   (default: all manifests)\n// Exit codes: 0 = no errors, 1 = errors, 2 = cannot run, 3 = no errors, but the proof of effective\n// Central Package Management did not run (report it as NOT RUN, never as passed).\n")
add('M1', R, "const path = require('path');\nconst common = require('./lib/common.js');\n", "const { spawnSync } = require('child_process');\nconst path = require('path');\nconst common = require('./lib/common.js');\n")
add('M1', R, """  const xml = common.readXml(file);
  if (!/<ManagePackageVersionsCentrally>\\s*true\\s*<\\/ManagePackageVersionsCentrally>/i.test(xml)) {
    findings.push(finding('ERROR', file, `Central Package Management is not enabled (ManagePackageVersionsCentrally=true) (${OWNER_RULE}).`));
  }
  for (const item of common.xmlElements(xml, 'PackageVersion')) {""", """  const xml = common.readXml(file);
  for (const item of common.xmlElements(xml, 'PackageVersion')) {""")
add('M1', R, """function isManifest(rel) {
  return /\\.csproj$/i.test(rel) || /(^|\\/)Directory\\.Packages\\.props$/.test(rel) || /(^|\\/)package\\.json$/.test(rel);
}
""", EVALUATOR + """
function isManifest(rel) {
  return /\\.csproj$/i.test(rel) || CPM_CHAIN_FILES.has(path.posix.basename(rel)) || /(^|\\/)package\\.json$/.test(rel);
}

// The projects whose effective state these targets can change: a project itself, or every project below a chain file.
function cpmProjects(targets) {
  const projects = new Set();
  for (const rel of targets) {
    if (!common.exists(rel)) continue;
    if (/\\.csproj$/i.test(rel)) projects.add(rel);
    else if (CPM_CHAIN_FILES.has(path.posix.basename(rel))) {
      const dir = path.posix.dirname(rel);
      for (const project of common.walk('.').filter((f) => /\\.csproj$/i.test(f))) if (dir === '.' || project.startsWith(`${dir}/`)) projects.add(project);
    }
  }
  return [...projects];
}

function checkEffectiveCpm(targets, findings) {
  const root = common.absPath('.');
  for (const project of cpmProjects(targets)) {
    const outcome = effectiveCpm(root, project);
    for (const message of outcome.errors) findings.push(finding('ERROR', project, `${message} (${OWNER_RULE}, NuGet).`));
    for (const message of outcome.notices) findings.push(finding('WARN', project, `${message} (${OWNER_WORKFLOW}).`));
    if (outcome.notRun) findings.push(finding('WARN', project, cpmNotRunMessage(outcome.notRun)));
  }
}
""")
add('M1', R, """    else if (/package\\.json$/.test(rel)) checkPackageJson(rel, data, findings);
  }
  return findings;
}
""", """    else if (/package\\.json$/.test(rel)) checkPackageJson(rel, data, findings);
  }
  checkEffectiveCpm(targets, findings);
  return findings;
}
""")
add('M1', R, """    const findings = checkManifests(files);
    if (findings.length) console.log(common.formatFindings(findings));
    const errors = findings.filter((f) => f.level === 'ERROR').length;
    console.log(`check-manifests: ${errors} error(s), ${findings.length - errors} warning(s)`);
    process.exit(errors ? 1 : 0);""", """    cpmState.budgetMs = 0;
    const findings = checkManifests(files);
    if (findings.length) console.log(common.formatFindings(findings));
    const errors = findings.filter((f) => f.level === 'ERROR').length;
    const notRun = findings.filter((f) => f.message.startsWith('NOT_RUN')).length;
    console.log(`check-manifests: ${errors} error(s), ${findings.length - errors - notRun} warning(s), ${notRun} not run`);
    process.exit(errors ? 1 : notRun ? 3 : 0);""")
add('M1', '.claude/rules/dependencies.md', """by default, and a `VersionOverride` needs a concrete, documented reason. Do not
duplicate centrally managed versions in individual `.csproj` files.
""", """by default, and a `VersionOverride` needs a concrete, documented reason. Do not
duplicate centrally managed versions in individual `.csproj` files. What counts
is the value MSBuild evaluates: the effective `ManagePackageVersionsCentrally`
must be true for each project, whether it is set in `Directory.Packages.props`
or inherited, and no project, condition, or later file may turn it off.
""")
add('M1', '.claude/skills/add-dependency/SKILL.md', """rejecting every other floating or prerelease version; there is no global switch.
Confirm""", """rejecting every other floating or prerelease version; there is no global switch.
For a floating NuGet version, also set `CentralPackageFloatingVersionsEnabled` to
true in `Directory.Packages.props`, because restore rejects the version otherwise
(NU1011); that NuGet property does not widen the exception, and the manifest
checks keep rejecting every other floating version.
Confirm""")
add('M1', '.claude/skills/verify/SKILL.md', """For dependency changes, run
`node "$(git rev-parse --show-toplevel)/.claude/scripts/check-manifests.js"`
and the vulnerability commands of `add-dependency` § Verify. For""", """For dependency changes, run
`node "$(git rev-parse --show-toplevel)/.claude/scripts/check-manifests.js"`
and the vulnerability commands of `add-dependency` § Verify. A `NOT_RUN` line or
exit code 3 from the manifest check means the MSBuild proof of effective Central
Package Management did not run: report it as NOT RUN, never as passed. For""")

# ---------------------------------------------------------------- L0
R = '.claude/hooks/manifest-checks.mjs'
add('L0', R, "// workflow; they do not restate policy.\nimport { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';\nimport path from 'node:path';\n", "// workflow; they do not restate policy.\n// Whole-repository command: node \"$(git rev-parse --show-toplevel)/.claude/hooks/manifest-checks.mjs\"\n// Exit codes: 0 = no problems, 1 = problems, 3 = no problems, but the proof of effective Central Package\n// Management did not run (report it as NOT RUN, never as passed).\nimport { spawnSync } from 'node:child_process';\nimport { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';\nimport path from 'node:path';\nimport { fileURLToPath } from 'node:url';\n")
add('L0', R, "    || base === 'Directory.Build.props'\n", "    || base === 'Directory.Build.props'\n    || base === 'Directory.Build.targets'\n")
add('L0', R, """// <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally> outside comments (element name and
// value in any case, no attributes).
function centralManagementEnabled(tokens) {
  const isSwitch = name => name?.toLowerCase() === 'managepackageversionscentrally';
  return tokens.some((token, index) => isSwitch(token.start) && !token.selfClosing && !token.malformed
    && Object.keys(token.attrs).length === 0
    && tokens[index + 1]?.text?.trim().toLowerCase() === 'true'
    && isSwitch(tokens[index + 2]?.end));
}

""", EVALUATOR + "\n")
add('L0', R, """  const tokens = xmlTokens(content);
  if (!centralManagementEnabled(tokens)) {
    problems.push(`${location}: ManagePackageVersionsCentrally must be true → ${OWNER.packageManagement}`);
  }
  const items = msbuildItems(tokens, ['PackageVersion']);""", """  const tokens = xmlTokens(content);
  const items = msbuildItems(tokens, ['PackageVersion']);""")
add('L0', R, """export function checkManifestFile(root, file) {
  const problems = [];""", """// The projects whose effective state this file can change: a project itself, or every project below a chain file.
function cpmProjects(root, location) {
  const base = path.posix.basename(location);
  if (base.endsWith('.csproj')) return [location];
  if (!CPM_CHAIN_FILES.has(base)) return [];
  const dir = path.posix.dirname(location);
  return findManifests(root).map(file => rel(root, file)).filter(project => project.endsWith('.csproj') && (dir === '.' || project.startsWith(`${dir}/`)));
}

function checkEffectiveCpm(root, location, problems, reported) {
  for (const project of cpmProjects(root, location)) {
    if (reported.has(project)) continue;
    reported.add(project);
    const outcome = effectiveCpm(root, project);
    for (const message of outcome.errors) problems.push(`${project}: ${message} → ${OWNER.packageManagement}`);
    for (const message of outcome.notices) problems.push(`${project}: ${message} → ${OWNER.addDependency}`);
    if (outcome.notRun) problems.push(`${project}: ${cpmNotRunMessage(outcome.notRun)}`);
  }
}

export function checkManifestFile(root, file, reported = new Set()) {
  const problems = [];""")
add('L0', R, """  else if (base === '.npmrc') checkNpmrc(content, location, problems);
  return problems;
}
""", """  else if (base === '.npmrc') checkNpmrc(content, location, problems);
  checkEffectiveCpm(root, location, problems, reported);
  return problems;
}
""")
add('L0', R, """export function scanManifests(root, files = findManifests(root)) {
  return files.flatMap(file => checkManifestFile(root, file));
}
""", """export function scanManifests(root, files = findManifests(root)) {
  const reported = new Set();
  return files.flatMap(file => checkManifestFile(root, file, reported));
}
""")
add('L0', R, """export function isFile(file) {
  try {
    return statSync(file).isFile();
  } catch {
    return false;
  }
}
""", """export function isFile(file) {
  try {
    return statSync(file).isFile();
  } catch {
    return false;
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  cpmState.budgetMs = 0;
  const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
  const problems = scanManifests(root);
  const notRun = problems.filter(problem => problem.includes(': NOT_RUN ')).length;
  const notices = problems.filter(problem => problem.includes('floats: restore rejects it')).length;
  for (const problem of problems) console.log(problem);
  console.log(`manifest-checks: ${problems.length - notRun - notices} problem(s), ${notices} notice(s), ${notRun} not run`);
  process.exit(problems.length - notRun - notices > 0 ? 1 : notRun > 0 ? 3 : 0);
}
""")
add('L0', '.claude/hooks/claude-hook.mjs', "  ':(glob)**/*.csproj', ':(glob)**/Directory.Packages.props', ':(glob)**/Directory.Build.props',\n", "  ':(glob)**/*.csproj', ':(glob)**/Directory.Packages.props', ':(glob)**/Directory.Build.props', ':(glob)**/Directory.Build.targets',\n")
add('L0', '.claude/hooks/claude-hook.mjs', "  for (const file of [...validate].sort()) lines.push(...checkManifestFile(root, path.join(root, file)));\n", "  const reported = new Set();\n  for (const file of [...validate].sort()) lines.push(...checkManifestFile(root, path.join(root, file), reported));\n")
add('L0', '.claude/rules/3-project/package-management.md', "- Do not duplicate centrally managed versions in individual `.csproj` files.\n", "- Do not duplicate centrally managed versions in individual `.csproj` files.\n- " + DEP_SENTENCE + "\n")
add('L0', '.claude/skills/add-dependency/SKILL.md', "keep rejecting every other floating or prerelease version; there is no global switch. Confirm", "keep rejecting every other floating or prerelease version; there is no global switch. " + FLOAT_SENTENCE + " Confirm")
add('L0', '.claude/skills/verify/SKILL.md', "- **Dependencies and security** — for dependency changes or security-sensitive work: `dotnet package list --vulnerable --include-transitive`, `npm audit`,", "- **Dependencies and security** — for dependency changes or security-sensitive work: `node \"$(git rev-parse --show-toplevel)/.claude/hooks/manifest-checks.mjs\"` (" + VERIFY_SENTENCE.rstrip('.') + "), `dotnet package list --vulnerable --include-transitive`, `npm audit`,")

# ---------------------------------------------------------------- L1
R = '.claude/hooks/post-change-checks.mjs'
add('L1', R, "// malformed input or internal failures exit 1 (non-blocking) and never block anything.\nimport { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';\n", "// malformed input or internal failures exit 1 (non-blocking) and never block anything.\n// Whole-repository command: node \"$(git rev-parse --show-toplevel)/.claude/hooks/post-change-checks.mjs\" --scan\n// Its exit codes: 0 = no findings, 1 = findings, 3 = no findings, but the proof of effective Central Package\n// Management did not run (report it as NOT RUN, never as passed).\nimport { spawnSync } from 'node:child_process';\nimport { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';\n")
add('L1', R, "const MANIFEST = /(^|\\/)([^/]+\\.csproj|Directory\\.Packages\\.props|package\\.json)$/i;\nconst PATHSPECS = [':(glob,icase)**/*.csproj', ':(glob,icase)**/Directory.Packages.props', ':(glob)**/package.json',", "const MANIFEST = /(^|\\/)([^/]+\\.csproj|Directory\\.Packages\\.props|Directory\\.Build\\.props|Directory\\.Build\\.targets|package\\.json)$/i;\nconst PATHSPECS = [':(glob,icase)**/*.csproj', ':(glob,icase)**/Directory.Packages.props', ':(glob,icase)**/Directory.Build.props', ':(glob,icase)**/Directory.Build.targets', ':(glob)**/package.json',")
add('L1', R, "const PCM = '.claude/rules/3-project/package-management.md';\n", "const PCM = '.claude/rules/3-project/package-management.md';\n\n" + EVALUATOR + """
const cpmReported = new Set();

// The projects whose effective state this manifest can change: a project itself, or every project below a chain file.
function cpmProjects(active, rel) {
  const name = path.posix.basename(rel);
  if (/\\.csproj$/i.test(name)) return [rel];
  if (!CPM_CHAIN_FILES.has(name)) return [];
  const dir = path.posix.dirname(rel);
  return listFiles(active, (f) => /\\.csproj$/i.test(f)).map((f) => toPosix(path.relative(active, f))).filter((project) => dir === '.' || project.startsWith(`${dir}/`));
}

function checkEffectiveCpm(active, rel, findings) {
  for (const project of cpmProjects(active, rel)) {
    if (cpmReported.has(project)) continue;
    cpmReported.add(project);
    const outcome = effectiveCpm(active, project);
    for (const message of outcome.errors) findings.push(`${project}: ${message} (owner: ${PCM}).`);
    for (const message of outcome.notices) findings.push(`${project}: ${message} (owner: add-dependency).`);
    if (outcome.notRun) findings.push(`${project}: ${cpmNotRunMessage(outcome.notRun)}`);
  }
}
""")
add('L1', R, """  const props = parsePackagesProps(text);
  if (!props.central) findings.push(`${rel}: ManagePackageVersionsCentrally must stay true (owner: ${PCM}).`);
  for (const { id, version } of props.versions) {""", """  const props = parsePackagesProps(text);
  for (const { id, version } of props.versions) {""")
add('L1', R, """  const name = path.posix.basename(rel).toLowerCase();
  if (name.endsWith('.csproj')) { checkCsproj(rel, text, rules, findings); return true; }
  if (name === 'directory.packages.props') checkPackagesProps(rel, text, rules, findings, loadVersionExceptions(active, findings));""", """  const name = path.posix.basename(rel).toLowerCase();
  checkEffectiveCpm(active, rel, findings);
  if (name.endsWith('.csproj')) { checkCsproj(rel, text, rules, findings); return true; }
  if (name === 'directory.packages.props') checkPackagesProps(rel, text, rules, findings, loadVersionExceptions(active, findings));""")
add('L1', R, """async function main() {
  let input;""", """function scanFlow() {
  cpmState.budgetMs = 0;
  const { active, config } = resolveRoots(process.cwd());
  const rules = packageRules(config);
  const findings = [];
  for (const abs of listFiles(active, (f) => MANIFEST.test(toPosix(f)))) validateManifest(active, toPosix(path.relative(active, abs)), rules, findings);
  const notRun = findings.filter((f) => f.includes(': NOT_RUN ')).length;
  const notices = findings.filter((f) => f.includes('floats: restore rejects it')).length;
  for (const finding of findings) process.stdout.write(`${finding}\\n`);
  process.stdout.write(`post-change-checks --scan: ${findings.length - notRun - notices} finding(s), ${notices} notice(s), ${notRun} not run\\n`);
  process.exit(findings.length - notRun - notices > 0 ? 1 : notRun > 0 ? 3 : 0);
}

async function main() {
  if (process.argv.includes('--scan')) scanFlow();
  let input;""")
add('L1', '.claude/scripts/lib/project.mjs', """  const clean = text.replace(/<!--[\\s\\S]*?-->/g, '');
  const central = /<ManagePackageVersionsCentrally>\\s*true\\s*<\\/ManagePackageVersionsCentrally>/i.test(clean);
  const versions = xmlElements(clean, 'PackageVersion')""", """  const clean = text.replace(/<!--[\\s\\S]*?-->/g, '');
  const versions = xmlElements(clean, 'PackageVersion')""")
add('L1', '.claude/scripts/lib/project.mjs', "  return { central, versions };\n", "  return { versions };\n")
add('L1', '.claude/rules/3-project/package-management.md', "and sit in the narrowest project that actually needs the package.\n", "and sit in the narrowest project that actually needs the package. " + DEP_SENTENCE + "\n")
add('L1', '.claude/skills/add-dependency/SKILL.md', "keep rejecting every other floating or prerelease version; there is no global switch. Confirm", "keep rejecting every other floating or prerelease version; there is no global switch. " + FLOAT_SENTENCE + " Confirm")
add('L1', '.claude/skills/verify/SKILL.md', "For dependency changes or security-sensitive work: `dotnet package list --vulnerable --include-transitive` (when the SDK supports it)", "For dependency changes or security-sensitive work: `node \"$(git rev-parse --show-toplevel)/.claude/hooks/post-change-checks.mjs\" --scan` (" + VERIFY_SENTENCE.rstrip('.') + "), `dotnet package list --vulnerable --include-transitive` (when the SDK supports it)")

# ---------------------------------------------------------------- K0
R = '.claude/scripts/check-dependencies.cjs'
add('K0', R, "//   --root <dir> overrides the checked repository root (default: the Git work tree of the current directory).\n", "//   --root <dir> overrides the checked repository root (default: the Git work tree of the current directory).\n// Exit codes: 0 = no errors, 1 = errors, 3 = no errors, but the proof of effective Central Package Management did not run\n// (report it as NOT RUN, never as passed).\n")
add('K0', R, "const fs = require('fs');\nconst path = require('path');\nconst { resolveRoot, readText } = require('./repo.cjs');\n", "const { spawnSync } = require('child_process');\nconst fs = require('fs');\nconst path = require('path');\nconst { resolveRoot, readText } = require('./repo.cjs');\n")
K0_OLD = between('K0', R, "// Effective ManagePackageVersionsCentrally in MSBuild evaluation order:", "// DEP-003 exception: a floating or prerelease version")
add('K0', R, K0_OLD, EVALUATOR + """
// The projects whose effective state this manifest can change: a project itself, or every project below a chain file.
function cpmProjects(rootDir, rel) {
  const name = rel.split('/').pop();
  if (name.endsWith('.csproj')) return [rel];
  if (!CPM_CHAIN_FILES.has(name)) return [];
  const dir = path.posix.dirname(rel);
  return findManifests(rootDir).filter((f) => f.endsWith('.csproj') && (dir === '.' || f.startsWith(`${dir}/`)));
}

function reportCpm(rootDir, rel, result, reported) {
  for (const project of cpmProjects(rootDir, rel)) {
    if (reported.has(project)) continue;
    reported.add(project);
    const outcome = effectiveCpm(rootDir, project);
    for (const message of outcome.errors) result.errors.push(`${project}: ${message} (D-17, rules/common/dependencies.md § NuGet).`);
    for (const message of outcome.notices) result.notices.push(`${project}: ${message} (add-dependency § 2).`);
    if (outcome.notRun) result.notRun.push(`${project}: ${cpmNotRunMessage(outcome.notRun)}`);
  }
}

""")
add('K0', R, """function checkFile(rootDir, rel) {
  const result = { errors: [], notices: [] };""", """function checkFile(rootDir, rel, reported = new Set()) {
  const result = { errors: [], notices: [], notRun: [] };""")
add('K0', R, """  const dir = path.posix.dirname(rel);
  if (name.endsWith('.csproj')) {
    reportCpm(rel, effectiveCpm(rootDir, dir, rel), result);
    checkCsproj(rootDir, rel, text, result);
  } else if (name === 'Directory.Packages.props') {
    reportCpm(rel, effectiveCpm(rootDir, dir, null), result);
    checkPackagesProps(rel, text, result, loadVersionExceptions(rootDir, result));
  } else if (name === 'Directory.Build.props' || name === 'Directory.Build.targets') {
    if (text.includes('ManagePackageVersionsCentrally')) reportCpm(rel, effectiveCpm(rootDir, dir, null), result);
  }
  else if (name === 'package.json') checkPackageJson(rootDir, rel, text, result, loadVersionExceptions(rootDir, result));
  return result;
}""", """  if (name.endsWith('.csproj')) checkCsproj(rootDir, rel, text, result);
  else if (name === 'Directory.Packages.props') checkPackagesProps(rel, text, result, loadVersionExceptions(rootDir, result));
  else if (name === 'package.json') checkPackageJson(rootDir, rel, text, result, loadVersionExceptions(rootDir, result));
  reportCpm(rootDir, rel, result, reported);
  return result;
}""")
add('K0', R, """  const total = { errors: [], notices: [], files: [] };
  const files = findManifests(rootDir);""", """  const total = { errors: [], notices: [], notRun: [], files: [] };
  const reported = new Set();
  const files = findManifests(rootDir);""")
add('K0', R, """  for (const rel of files) {
    const r = checkFile(rootDir, rel);
    total.errors.push(...r.errors);
    total.notices.push(...r.notices);
    total.files.push(rel);
  }""", """  for (const rel of files) {
    const r = checkFile(rootDir, rel, reported);
    total.errors.push(...r.errors);
    total.notices.push(...r.notices);
    total.notRun.push(...r.notRun);
    total.files.push(rel);
  }""")
add('K0', R, """  const rootDir = resolved.root;
  let result;
  if (targets.length > 0) {
    result = { errors: [], notices: [], files: [] };
    for (const target of targets) {""", """  const rootDir = resolved.root;
  cpmState.budgetMs = 0;
  let result;
  if (targets.length > 0) {
    const reported = new Set();
    result = { errors: [], notices: [], notRun: [], files: [] };
    for (const target of targets) {""")
add('K0', R, """      const r = checkFile(rootDir, rel);
      result.errors.push(...r.errors);
      result.notices.push(...r.notices);
      result.files.push(rel);""", """      const r = checkFile(rootDir, rel, reported);
      result.errors.push(...r.errors);
      result.notices.push(...r.notices);
      result.notRun.push(...r.notRun);
      result.files.push(rel);""")
add('K0', R, """  for (const n of result.notices) console.log(`NOTICE ${n}`);
  console.log(`check-dependencies: ${rootDir}: ${result.files.length} manifest(s), ${result.errors.length} error(s), ${result.notices.length} notice(s).`);
  process.exit(result.errors.length > 0 ? 1 : 0);""", """  for (const n of result.notices) console.log(`NOTICE ${n}`);
  for (const n of result.notRun) console.log(`NOT_RUN ${n}`);
  console.log(`check-dependencies: ${rootDir}: ${result.files.length} manifest(s), ${result.errors.length} error(s), ${result.notices.length} notice(s), ${result.notRun.length} not run.`);
  process.exit(result.errors.length > 0 ? 1 : result.notRun.length > 0 ? 3 : 0);""")
add('K0', '.claude/hooks/hook.cjs', """      '*.csproj', '*Directory.Packages.props', '*package.json', 'CLAUDE.md',""", """      '*.csproj', '*Directory.Packages.props', '*Directory.Build.props', '*Directory.Build.targets', '*package.json', 'CLAUDE.md',""")
add('K0', '.claude/hooks/hook.cjs', """  const validated = new Set();
  const validate = (rel) => {
    if (validated.has(rel)) return;
    validated.add(rel);
    const result = t.dependencies.checkFile(root, rel);
    for (const e of result.errors) messages.push(`[manifest] ${e}`);
    for (const n of result.notices) messages.push(`[manifest notice] ${n}`);
  };""", """  const validated = new Set();
  const cpmReported = new Set();
  const validate = (rel) => {
    if (validated.has(rel)) return;
    validated.add(rel);
    const result = t.dependencies.checkFile(root, rel, cpmReported);
    for (const e of result.errors) messages.push(`[manifest] ${e}`);
    for (const n of result.notices) messages.push(`[manifest notice] ${n}`);
    for (const n of result.notRun) messages.push(`[manifest] ${n}`);
  };""")
add('K0', '.claude/rules/common/dependencies.md', "the effective `ManagePackageVersionsCentrally` is true wherever the MSBuild chain sets it, no project or later file disables it, and package versions", "what counts is the value MSBuild evaluates, so the effective `ManagePackageVersionsCentrally` must be true for each project wherever the MSBuild chain sets it, no project, condition or later file may turn it off, and package versions")
add('K0', '.claude/skills/add-dependency/SKILL.md', "keep rejecting every other floating or prerelease version; there is no global switch. Confirm", "keep rejecting every other floating or prerelease version; there is no global switch. " + FLOAT_SENTENCE + " Confirm")
add('K0', '.claude/skills/verify/SKILL.md', "`node \"$(git rev-parse --show-toplevel)/.claude/scripts/check-dependencies.cjs\"`, then review against `rules/backend/architecture.md`.", "`node \"$(git rev-parse --show-toplevel)/.claude/scripts/check-dependencies.cjs\"`, then review against `rules/backend/architecture.md`. " + VERIFY_SENTENCE)

# ---------------------------------------------------------------- K1
R = '.claude/scripts/check-manifests.cjs'
add('K1', R, "// Conforms: .claude/rules/backend/dependencies.md, .claude/rules/frontend/dependencies.md, docs/architecture/decision-register.md\n", "// Conforms: .claude/rules/backend/dependencies.md, .claude/rules/frontend/dependencies.md, docs/architecture/decision-register.md\n// Exit codes: 0 = no errors, 1 = errors, 3 = no errors, but the proof of effective Central Package Management did not run\n// (report it as NOT RUN, never as passed).\n")
add('K1', R, "const fs = require('fs');\nconst path = require('path');\nconst lib = require('./lib.cjs');\n", "const { spawnSync } = require('child_process');\nconst fs = require('fs');\nconst path = require('path');\nconst lib = require('./lib.cjs');\n")
add('K1', R, """  const findings = exceptionFindings(ctx);
  if (!/<ManagePackageVersionsCentrally>\\s*true\\s*<\\/ManagePackageVersionsCentrally>/i.test(text)) {
    findings.push(lib.finding('error', rel, 'ManagePackageVersionsCentrally is not enabled', OWNER_NUGET));
  }
  const packages = lib.xmlElements(text, 'PackageVersion')""", """  const findings = exceptionFindings(ctx);
  const packages = lib.xmlElements(text, 'PackageVersion')""")
add('K1', R, """function isManifest(rel) {
  const base = path.posix.basename(rel);
  return rel.endsWith('.csproj') || base === 'Directory.Packages.props' || base === 'package.json';
}
""", EVALUATOR + """
function isManifest(rel) {
  const base = path.posix.basename(rel);
  return rel.endsWith('.csproj') || CPM_CHAIN_FILES.has(base) || base === 'package.json';
}

// The projects whose effective state this manifest can change: a project itself, or every project below a chain file.
function cpmProjects(root, rel) {
  if (rel.endsWith('.csproj')) return [rel];
  if (!CPM_CHAIN_FILES.has(path.posix.basename(rel))) return [];
  const dir = path.posix.dirname(rel);
  return lib.walk(root, '', r => r.endsWith('.csproj')).filter(project => dir === '.' || project.startsWith(`${dir}/`));
}

function effectiveCpmFindings(ctx, rel) {
  const findings = [];
  ctx.cpmReported ||= new Set();
  for (const project of cpmProjects(ctx.root, rel)) {
    if (ctx.cpmReported.has(project)) continue;
    ctx.cpmReported.add(project);
    const outcome = effectiveCpm(ctx.root, project);
    for (const message of outcome.errors) findings.push(lib.finding('error', project, message, OWNER_NUGET));
    for (const message of outcome.notices) findings.push(lib.finding('warn', project, message, OWNER_WORKFLOW));
    if (outcome.notRun) findings.push(lib.finding('warn', project, cpmNotRunMessage(outcome.notRun), OWNER_NUGET));
  }
  return findings;
}
""")
add('K1', R, """    if (rel.endsWith('.csproj')) return checkProjectFile(ctx, rel);
    if (base === 'Directory.Packages.props') return checkPackagesProps(ctx, rel);
    if (base === 'package.json') return checkPackageJson(ctx, rel);""", """    if (rel.endsWith('.csproj')) return [...checkProjectFile(ctx, rel), ...effectiveCpmFindings(ctx, rel)];
    if (base === 'Directory.Packages.props') return [...checkPackagesProps(ctx, rel), ...effectiveCpmFindings(ctx, rel)];
    if (CPM_CHAIN_FILES.has(base)) return effectiveCpmFindings(ctx, rel);
    if (base === 'package.json') return checkPackageJson(ctx, rel);""")
add('K1', R, """  const args = process.argv.slice(2);
  let findings;
  if (args.length === 0) {""", """  const args = process.argv.slice(2);
  cpmState.budgetMs = 0;
  let findings;
  if (args.length === 0) {""")
add('K1', R, """  const errors = findings.filter(f => f.severity === 'error').length;
  process.stdout.write(`check-manifests (${root}): ${errors} error(s), ${findings.length - errors} warning(s)\\n`);
  process.exitCode = errors ? 1 : 0;""", """  const errors = findings.filter(f => f.severity === 'error').length;
  const notRun = findings.filter(f => f.message.startsWith('NOT_RUN')).length;
  process.stdout.write(`check-manifests (${root}): ${errors} error(s), ${findings.length - errors - notRun} warning(s), ${notRun} not run\\n`);
  process.exitCode = errors ? 1 : notRun ? 3 : 0;""")
add('K1', '.claude/scripts/actual-state.cjs', "':(glob)**/*.csproj', ':(glob)**/Directory.Packages.props', ':(glob)**/package.json'];", "':(glob)**/*.csproj', ':(glob)**/Directory.Packages.props', ':(glob)**/Directory.Build.props', ':(glob)**/Directory.Build.targets', ':(glob)**/package.json'];")
add('K1', '.claude/rules/backend/dependencies.md', "(central versions are never duplicated in project files; a `VersionOverride` needs a recorded reason) and live in the narrowest project that actually requires the package.", "(central versions are never duplicated in project files; a `VersionOverride` needs a recorded reason) and live in the narrowest project that actually requires the package. " + DEP_SENTENCE)
add('K1', '.claude/skills/add-dependency/SKILL.md', "keep rejecting every other floating or prerelease version; there is no global switch. Confirm", "keep rejecting every other floating or prerelease version; there is no global switch. " + FLOAT_SENTENCE + " Confirm")
add('K1', '.claude/skills/verify/SKILL.md', "then run `node \"<root>/.claude/scripts/check-manifests.cjs\"`.", "then run `node \"<root>/.claude/scripts/check-manifests.cjs\"`. " + VERIFY_SENTENCE)
