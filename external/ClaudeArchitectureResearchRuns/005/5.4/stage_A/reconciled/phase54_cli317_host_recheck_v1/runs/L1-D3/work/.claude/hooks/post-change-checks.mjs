#!/usr/bin/env node
// PostToolUse (Edit|Write|MultiEdit and Bash|PowerShell) and PostToolUseFailure (Bash|PowerShell):
// validates the ACTUAL resulting state of package/project manifests in the active project or worktree.
// - Edit/Write: validates the edited file (resolved from its own location).
// - Shell calls (succeeded or failed): compares a per-worktree snapshot of manifest content (Git index ids for
//   clean files, content ids only for files Git reports as changed) with the previous snapshot, independent of
//   the command text. The first observation in a worktree validates every manifest once; later calls validate
//   only added, modified, removed, or moved manifests (including changes brought in by HEAD transitions).
// Checks: Central Package Management, floating/prerelease versions, denied and approval-required packages,
// project-reference direction (architecture check), product-source synchronization reminder.
// Findings go to stderr with exit code 2 (shown to Claude; the tool call already ran). Advisory only:
// malformed input or internal failures exit 1 (non-blocking) and never block anything.
// Whole-repository command: node "$(git rev-parse --show-toplevel)/.claude/hooks/post-change-checks.mjs" --scan
// Its exit codes: 0 = no findings, 1 = findings, 3 = no findings, but the proof of effective Central Package
// Management did not run (report it as NOT RUN, never as passed).
import { spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  EncodingError, SKIP_DIRS, blobId, git, hookStateDir, listFiles, loadJsonFacet, matchesAny, packageMatches, parseCsproj,
  parsePackagesProps, parseSelection, readStdinJson, readText, resolveRoots, toPosix, toRepoRelative,
} from '../scripts/lib/project.mjs';
import { checkArchitecture } from '../scripts/check-architecture.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const EDIT_TOOLS = new Set(['Edit', 'Write', 'MultiEdit', 'NotebookEdit']);
const MANIFEST = /(^|\/)([^/]+\.csproj|Directory\.Packages\.props|Directory\.Build\.props|Directory\.Build\.targets|package\.json)$/i;
const PATHSPECS = [':(glob,icase)**/*.csproj', ':(glob,icase)**/Directory.Packages.props', ':(glob,icase)**/Directory.Build.props', ':(glob,icase)**/Directory.Build.targets', ':(glob)**/package.json',
  ...[...SKIP_DIRS].filter((d) => d !== '.git').map((d) => `:(exclude,glob)**/${d}/**`)];
const PCM = '.claude/rules/3-project/package-management.md';

// Effective Central Package Management (DEP-006): MSBuild evaluates each project; the XML text is never taken as proof of the setting.
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

const cpmReported = new Set();

// The projects whose effective state this manifest can change: a project itself, or every project below a chain file.
function cpmProjects(active, rel) {
  const name = path.posix.basename(rel);
  if (/\.csproj$/i.test(name)) return [rel];
  if (!CPM_CHAIN_FILES.has(name)) return [];
  const dir = path.posix.dirname(rel);
  return listFiles(active, (f) => /\.csproj$/i.test(f)).map((f) => toPosix(path.relative(active, f))).filter((project) => dir === '.' || project.startsWith(`${dir}/`));
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

function isPrerelease(version) {
  return /^\d+(\.\d+){0,3}-[0-9A-Za-z]/.test(String(version || '').trim().replace(/^[\^~=<>v\s[(]+/, ''));
}

function packageRules(config) {
  const selection = parseSelection(config);
  const policy = JSON.parse(readText(path.join(here, 'manifest-policy.json')));
  const frame = loadJsonFacet(config, selection, 'architecture', 'check');
  const testing = loadJsonFacet(config, selection, 'backend-testing', 'enforcement');
  const frontend = loadJsonFacet(config, selection, 'frontend', 'enforcement');
  return {
    policy,
    nugetDenied: policy.nuget.denied,
    nugetApproval: [
      ...policy.nuget.approvalRequired,
      ...((frame && frame.approvalRequiredPackages) || []),
      ...((testing && testing.approvalRequiredPackages) || []),
    ],
    frontend,
  };
}

function checkNugetIds(ids, rules, rel, findings) {
  for (const id of ids) {
    if (/\$\(/.test(id || '')) { findings.push(`${rel}: package id '${id}' uses an MSBuild property; the hook does not evaluate MSBuild, so confirm the resolved package is allowed (owner: add-dependency).`); continue; }
    for (const r of packageMatches(id, rules.nugetDenied)) findings.push(`${rel}: '${id}' must not be added — ${r.reason} (owner: ${r.owner}).`);
    for (const r of packageMatches(id, rules.nugetApproval)) findings.push(`${rel}: '${id}' requires approval — ${r.reason} (owner: ${r.owner}). Remove it unless the user approved it.`);
  }
}

function checkCsproj(rel, text, rules, findings) {
  const info = parseCsproj(text);
  for (const pkg of info.packages) {
    if (pkg.version) findings.push(`${rel}: PackageReference '${pkg.id}' declares a version; versions belong only in Directory.Packages.props (owner: ${PCM}).`);
    else if (pkg.versionOverride) findings.push(`${rel}: PackageReference '${pkg.id}' uses VersionOverride; keep it only for a concrete reason and report that reason (owner: ${PCM}).`);
  }
  checkNugetIds(info.packages.map((p) => p.id), rules, rel, findings);
}

// DEP-003 exception: a floating or prerelease version is accepted only when
// dependency-version-exceptions.json records the user's explicit request for
// exactly this ecosystem, package, version, and manifest. There is no global switch.
function validVersionException(e) {
  if (typeof e !== 'object' || e === null) return false;
  if (e.ecosystem !== 'npm' && e.ecosystem !== 'nuget') return false;
  if (typeof e.package !== 'string' || !e.package.trim() || /[*?]/.test(e.package)) return false;
  if (typeof e.version !== 'string' || !e.version.trim()) return false;
  if (typeof e.manifest !== 'string' || !e.manifest.trim()) return false;
  if (e.requested_by !== 'user') return false;
  return typeof e.request === 'string' && e.request.trim() !== '';
}

function loadVersionExceptions(active, findings) {
  const file = path.join(active, 'dependency-version-exceptions.json');
  if (!existsSync(file)) return [];
  const label = 'dependency-version-exceptions.json';
  try {
    const entries = JSON.parse(readFileSync(file, 'utf8')).exceptions;
    if (!Array.isArray(entries)) throw new Error('"exceptions" is not a list');
    const valid = entries.filter(validVersionException);
    if (valid.length !== entries.length) findings.push(`${label}: exception entry ignored: it needs ecosystem, an exact package, version, manifest, requested_by "user", and the request text (owner: add-dependency).`);
    return valid;
  } catch (error) {
    findings.push(`${label}: unreadable exception record (${error.message}); no exception applies (owner: add-dependency).`);
    return [];
  }
}

function approvedVersionException(exceptions, ecosystem, id, version, rel) {
  const wanted = ecosystem === 'nuget' ? id.toLowerCase() : id;
  return exceptions.some((e) => e.ecosystem === ecosystem && (ecosystem === 'nuget' ? e.package.toLowerCase() : e.package) === wanted
    && e.version.trim() === String(version).trim() && e.manifest.replace(/\\/g, '/') === String(rel).replace(/\\/g, '/'));
}

function checkPackagesProps(rel, text, rules, findings, exceptions) {
  const props = parsePackagesProps(text);
  for (const { id, version } of props.versions) {
    if (!id) continue;
    if (approvedVersionException(exceptions, 'nuget', id, version, rel)) continue;
    if (/\$\(/.test(version)) findings.push(`${rel}: '${id}' version '${version}' uses an MSBuild property; the hook does not evaluate MSBuild, so confirm it resolves to a pinned stable version (owner: add-dependency).`);
    else if (version.includes('*') || version.trim() === '') findings.push(`${rel}: '${id}' uses a floating or empty version '${version}'; pin the latest stable compatible version (owner: add-dependency).`);
    else if (isPrerelease(version)) findings.push(`${rel}: '${id}' ${version} is a prerelease; allowed only when explicitly requested (owner: add-dependency).`);
  }
  checkNugetIds(props.versions.map((v) => v.id), rules, rel, findings);
}

function checkPackageJson(rel, text, rules, findings, exceptions) {
  let manifest;
  try { manifest = JSON.parse(text); } catch { findings.push(`${rel}: package.json is not valid JSON.`); return; }
  const frontendRules = rules.frontend && matchesAny(rel, rules.frontend.manifestGlobs) ? rules.frontend.approvalRequiredPackages : [];
  for (const section of ['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies']) {
    for (const [name, version] of Object.entries(manifest[section] || {})) {
      const v = String(version).trim();
      if (approvedVersionException(exceptions, 'npm', name, v, rel)) continue;
      if (rules.policy.npm.floatingVersions.includes(v)) findings.push(`${rel}: ${section}.${name} uses floating version '${v}' (owner: add-dependency).`);
      else if (isPrerelease(v)) findings.push(`${rel}: ${section}.${name} ${v} is a prerelease; allowed only when explicitly requested (owner: add-dependency).`);
      for (const r of packageMatches(name, frontendRules)) findings.push(`${rel}: '${name}' requires a concrete need and approval — ${r.reason} (owner: ${r.owner}).`);
    }
  }
}

// Validates one manifest of the active root. Returns true when it is a project file (graph-relevant).
function validateManifest(active, rel, rules, findings) {
  const abs = path.join(active, rel);
  if (!existsSync(abs)) return false;
  let text;
  try {
    text = readText(abs, rel);
  } catch (error) {
    if (!(error instanceof EncodingError)) throw error;
    findings.push(`${error.message}; save it as UTF-8 (or BOM-tagged UTF-16) so it can be validated (owner: ${PCM}).`);
    return false;
  }
  const name = path.posix.basename(rel).toLowerCase();
  checkEffectiveCpm(active, rel, findings);
  if (name.endsWith('.csproj')) { checkCsproj(rel, text, rules, findings); return true; }
  if (name === 'directory.packages.props') checkPackagesProps(rel, text, rules, findings, loadVersionExceptions(active, findings));
  else if (name === 'package.json') checkPackageJson(rel, text, rules, findings, loadVersionExceptions(active, findings));
  return false;
}

// ---------- Per-worktree snapshot of manifest content ----------

function snapshot(active) {
  const files = {};
  const prefixOut = git(active, ['rev-parse', '--show-prefix']);
  if (prefixOut !== null) {
    const prefix = prefixOut.trim();
    const ls = git(active, ['ls-files', '-s', '-z', '--', ...PATHSPECS]);
    const status = git(active, ['status', '--porcelain=v1', '-z', '--untracked-files=all', '--no-renames', '--', ...PATHSPECS]);
    if (ls !== null && status !== null) {
      for (const entry of ls.split('\0').filter(Boolean)) {
        const [meta, file] = entry.split('\t');
        if (MANIFEST.test(file)) files[file] = meta.split(' ')[1];
      }
      for (const entry of status.split('\0').filter(Boolean)) {
        const top = entry.slice(3);
        if (!top.startsWith(prefix)) continue;
        const rel = top.slice(prefix.length);
        if (!MANIFEST.test(rel)) continue;
        const abs = path.join(active, rel);
        if (existsSync(abs) && statSync(abs).isFile()) files[rel] = blobId(readFileSync(abs));
        else delete files[rel];
      }
      const head = git(active, ['rev-parse', '-q', '--verify', 'HEAD']);
      return { mode: 'git', head: head ? head.trim() : null, files };
    }
  }
  // Not a Git working tree: stat-based scan (content is read only for changed files during validation).
  for (const abs of listFiles(active, (f) => MANIFEST.test(toPosix(f)))) {
    const st = statSync(abs);
    files[toPosix(path.relative(active, abs))] = `${st.size}:${st.mtimeMs}`;
  }
  return { mode: 'scan', head: null, files };
}

function stateFile(active) { return path.join(hookStateDir(active), 'manifest-state.json'); }

function loadState(active) {
  try { return JSON.parse(readFileSync(stateFile(active), 'utf8')); } catch { return null; }
}

function saveState(active, snap) {
  mkdirSync(hookStateDir(active), { recursive: true });
  writeFileSync(stateFile(active), JSON.stringify(snap, null, 2));
}

function report(findings, label) {
  if (findings.length === 0) process.exit(0);
  process.stderr.write(`${label}:\n- ${findings.join('\n- ')}\n`);
  process.exit(2);
}

function architectureFindings(active, config, findings) {
  const { violations } = checkArchitecture(active, config);
  for (const v of violations) findings.push(`architecture: ${v}`);
}

function editFlow(input) {
  const filePath = input.tool_input && (input.tool_input.file_path || input.tool_input.notebook_path);
  if (!filePath) process.exit(0);
  const { active, config } = resolveRoots(path.dirname(path.resolve(input.cwd || process.cwd(), filePath)));
  const rel = toRepoRelative(active, path.resolve(input.cwd || process.cwd(), filePath));
  if (!rel) process.exit(0);
  const findings = [];
  if (rel === 'SPECIFICATION.md' || rel === 'CUSTOM_SETTINGS.md') {
    findings.push(`${rel} changed: keep SPECIFICATION.md and CUSTOM_SETTINGS.md consistent (CLAUDE.md § Product inputs) and run the custom-settings workflow to synchronize affected code, validation, configuration, tests, documentation, and frontend.`);
  } else if (MANIFEST.test(rel)) {
    const project = validateManifest(active, rel, packageRules(config), findings);
    if (project) architectureFindings(active, config, findings);
    const state = loadState(active);
    if (state && state.files) {
      const abs = path.join(active, rel);
      if (existsSync(abs)) state.files[rel] = state.mode === 'git' ? blobId(readFileSync(abs)) : `${statSync(abs).size}:${statSync(abs).mtimeMs}`;
      else delete state.files[rel];
      saveState(active, state);
    }
  }
  report(findings, 'Post-edit checks');
}

function shellFlow(input) {
  const { active, config } = resolveRoots(input.cwd);
  const current = snapshot(active);
  const previous = loadState(active);
  const before = previous && previous.mode === current.mode ? previous.files : null;
  const changed = [];
  const removed = [];
  for (const [rel, id] of Object.entries(current.files)) if (!before || before[rel] !== id) changed.push(rel);
  if (before) for (const rel of Object.keys(before)) if (!(rel in current.files)) removed.push(rel);
  if (previous && changed.length === 0 && removed.length === 0) {
    if (previous.head !== current.head) saveState(active, current);
    process.exit(0);
  }

  const rules = packageRules(config);
  const findings = [];
  const added = new Set(before ? changed.filter((r) => !(r in before)) : []);
  let graph = false;
  for (const rel of removed) {
    const moved = [...added].find((a) => current.files[a] === before[rel]);
    const what = /\.csproj$/i.test(rel) ? 'changes the project set/reference graph, a Reserved decision unless it implements the approved layout (project-structure)' : 'removes package configuration the package-management rule relies on';
    findings.push(moved ? `${rel} was moved/renamed to ${moved}: this ${what}.` : `${rel} was removed: this ${what}.`);
    if (/\.csproj$/i.test(rel)) graph = true;
  }
  for (const rel of changed) if (validateManifest(active, rel, rules, findings)) graph = true;
  if (graph) architectureFindings(active, config, findings);
  saveState(active, current);
  const event = input.hook_event_name === 'PostToolUseFailure' ? 'failed' : 'completed';
  report(findings, `Manifest state after ${event} ${input.tool_name || 'shell'} call${previous ? '' : ' (initial validation of this worktree)'}`);
}

function scanFlow() {
  cpmState.budgetMs = 0;
  const { active, config } = resolveRoots(process.cwd());
  const rules = packageRules(config);
  const findings = [];
  for (const abs of listFiles(active, (f) => MANIFEST.test(toPosix(f)))) validateManifest(active, toPosix(path.relative(active, abs)), rules, findings);
  const notRun = findings.filter((f) => f.includes(': NOT_RUN ')).length;
  const notices = findings.filter((f) => f.includes('floats: restore rejects it')).length;
  for (const finding of findings) process.stdout.write(`${finding}\n`);
  process.stdout.write(`post-change-checks --scan: ${findings.length - notRun - notices} finding(s), ${notices} notice(s), ${notRun} not run\n`);
  process.exit(findings.length - notRun - notices > 0 ? 1 : notRun > 0 ? 3 : 0);
}

async function main() {
  if (process.argv.includes('--scan')) scanFlow();
  let input;
  try {
    input = await readStdinJson();
  } catch (error) {
    process.stderr.write(`Post-change checks skipped: ${error.message}\n`);
    process.exit(1);
  }
  if (EDIT_TOOLS.has(input.tool_name) || (input.tool_input && (input.tool_input.file_path || input.tool_input.notebook_path) && !input.tool_input.command)) editFlow(input);
  else shellFlow(input);
}

main().catch((error) => {
  process.stderr.write(`Hook failure (post-change-checks): ${error.message}\n`);
  process.exit(1);
});
