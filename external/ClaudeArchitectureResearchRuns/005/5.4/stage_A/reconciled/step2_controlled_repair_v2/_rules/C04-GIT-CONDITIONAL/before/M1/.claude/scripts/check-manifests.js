#!/usr/bin/env node
'use strict';
// Dependency-manifest check: NuGet Central Package Management, floating and
// prerelease versions, deprecated or not-by-default packages, test-framework
// mixing, and npm dependency categories.
// Policy owners: .claude/rules/dependencies.md and the add-dependency workflow;
// slot-specific package lists come from the selected capability manifests.
// Checks the repository or worktree that contains the working directory.
// Usage (any directory inside it; file arguments are relative to that directory):
//   node "$(git rev-parse --show-toplevel)/.claude/scripts/check-manifests.js" [file ...]   (default: all manifests)
// Exit codes: 0 = no errors, 1 = errors, 2 = cannot run, 3 = no errors, but the proof of effective
// Central Package Management did not run (report it as NOT RUN, never as passed).

const { spawnSync } = require('child_process');
const path = require('path');
const common = require('./lib/common.js');

const OWNER_RULE = '.claude/rules/dependencies.md';
const OWNER_WORKFLOW = 'add-dependency workflow';

// Embedded (non-slot) package policy.
const DEPRECATED_PACKAGES = new Map([
  ['Microsoft.Extensions.Http.Polly', 'deprecated resilience integration; use the approved Microsoft.Extensions resilience packages'],
  ['Polly.Extensions.Http', 'deprecated resilience integration; use the approved Microsoft.Extensions resilience packages'],
  ['Serilog.Sinks.Elasticsearch', 'deprecated sink package; use Elastic.Serilog.Sinks'],
  ['FluentValidation.AspNetCore', 'legacy automatic-validation integration; do not add it merely to connect validation to the pipeline'],
]);
const EXCEPTION_PACKAGES = new Map([
  ['Polly', 'direct Polly usage is an explicit, documented exception (add-dependency workflow, Choose the Package)'],
]);
const NEUTRAL_DEV_ONLY_NPM = ['typescript', 'eslint', 'prettier', '@playwright/test', 'jest', 'karma'];

const PRERELEASE = /-(alpha|beta|rc|preview|pre|dev|nightly|canary|next)/i;

function finding(level, file, message) {
  return { level, file, message };
}

function moduleData() {
  const modules = common.loadSelectedModules();
  const frame = common.moduleFor(modules, 'architecture');
  const testing = common.moduleFor(modules, 'backend-testing');
  const frontend = common.moduleFor(modules, 'frontend');
  return {
    reservedPackages: frame?.manifest.enforcement?.reservedPackages || [],
    testProjectSuffixes: (frame?.manifest.enforcement?.architecture?.testProjects || []).map((t) => t.suffix),
    testFrameworkPackages: testing?.manifest.enforcement?.testFrameworkPackages || [],
    competingFrameworkPackages: testing?.manifest.enforcement?.competingFrameworkPackages || [],
    notByDefaultPackages: frontend?.manifest.enforcement?.notByDefaultPackages || [],
    devOnlyPackages: [...NEUTRAL_DEV_ONLY_NPM, ...(frontend?.manifest.enforcement?.devOnlyPackages || [])],
  };
}

// Version metadata of an item element: a child <Version> wins over the attribute; a child whose
// content cannot be read counts as a declared, empty version. null when there is none.
function versionOf(item) {
  const child = item.inner ? common.xmlElements(item.inner, 'Version')[0] : undefined;
  if (child) return child.inner ?? '';
  return item.attrs.Version ?? null;
}

// One entry per PackageReference with an Include or Update identity, or that cannot be read
// reliably ({ id: null, problem }); Remove items are not references.
function packageReferences(xml) {
  const refs = [];
  for (const item of common.xmlElements(xml, 'PackageReference')) {
    const id = (item.attrs && (item.attrs.Include || item.attrs.Update)) || null;
    if (!id && !item.problem) continue;
    refs.push({ id, version: id ? versionOf(item) : null, override: id ? item.attrs.VersionOverride ?? null : null, line: item.line, problem: item.problem });
  }
  return refs;
}

function unreadable(type, item) {
  return `${type} at line ${item.line} cannot be read reliably (${item.problem}); the package check is incomplete (${OWNER_RULE}).`;
}

function checkPackageId(file, id, data, findings) {
  if (DEPRECATED_PACKAGES.has(id)) {
    findings.push(finding('ERROR', file, `${id}: ${DEPRECATED_PACKAGES.get(id)} (${OWNER_WORKFLOW}).`));
  }
  if (EXCEPTION_PACKAGES.has(id)) {
    findings.push(finding('WARN', file, `${id}: ${EXCEPTION_PACKAGES.get(id)}.`));
  }
  if (data.reservedPackages.includes(id)) {
    findings.push(finding('WARN', file, `${id}: introduces a pattern listed as not adopted; this is a Reserved decision (docs/capabilities/architecture.md, architecture-decision workflow).`));
  }
}

function checkCsproj(file, data, findings) {
  const xml = common.readXml(file);
  const name = path.basename(file, '.csproj');
  const refs = packageReferences(xml);
  for (const ref of refs) {
    if (ref.problem) findings.push(finding('WARN', file, unreadable('PackageReference', ref)));
    if (!ref.id) continue;
    if (ref.version !== null) {
      findings.push(finding('ERROR', file, `PackageReference ${ref.id} declares a version; versions belong in Directory.Packages.props (${OWNER_RULE}, NuGet).`));
    }
    if (ref.override !== null) {
      findings.push(finding('WARN', file, `PackageReference ${ref.id} uses VersionOverride; this needs a concrete, documented reason (${OWNER_RULE}).`));
    }
    checkPackageId(file, ref.id, data, findings);
  }
  const ids = refs.filter((r) => r.id).map((r) => r.id);
  const isTestProject =
    data.testProjectSuffixes.some((s) => name.endsWith(s)) ||
    ids.some((id) => data.testFrameworkPackages.includes(id)) ||
    /<IsTestProject>\s*true\s*<\/IsTestProject>/i.test(xml);
  if (isTestProject) {
    const competing = ids.filter((id) => data.competingFrameworkPackages.includes(id));
    if (competing.length) {
      findings.push(finding('WARN', file, `test project references another test framework (${competing.join(', ')}); a second framework needs a concrete reason (.claude/rules/test-framework.md).`));
    }
  }
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

function loadVersionExceptions(data, findings) {
  const file = 'dependency-version-exceptions.json';
  if (!common.exists(file)) return;
  try {
    const entries = JSON.parse(common.readText(file)).exceptions;
    if (!Array.isArray(entries)) throw new Error('"exceptions" is not a list');
    for (const e of entries) {
      if (validVersionException(e)) data.versionExceptions.push(e);
      else findings.push(finding('ERROR', file, `exception entry ignored: it needs ecosystem, an exact package, version, manifest, requested_by "user", and the request text (${OWNER_WORKFLOW}).`));
    }
  } catch (e) {
    findings.push(finding('ERROR', file, `unreadable exception record (${e.message}); no exception applies (${OWNER_WORKFLOW}).`));
  }
}

function approvedVersionException(data, ecosystem, id, version, rel) {
  const wanted = ecosystem === 'nuget' ? id.toLowerCase() : id;
  return data.versionExceptions.some((e) => e.ecosystem === ecosystem && (ecosystem === 'nuget' ? e.package.toLowerCase() : e.package) === wanted
    && e.version.trim() === String(version).trim() && e.manifest.replace(/\\/g, '/') === String(rel).replace(/\\/g, '/'));
}

function checkPackagesProps(file, data, findings) {
  const xml = common.readXml(file);
  for (const item of common.xmlElements(xml, 'PackageVersion')) {
    if (item.problem) findings.push(finding('WARN', file, unreadable('PackageVersion', item)));
    const id = item.attrs && item.attrs.Include;
    if (!id) continue;
    const version = versionOf(item);
    if (version !== null) {
      if (approvedVersionException(data, 'nuget', id, version, file)) {
        findings.push(finding('WARN', file, `${id}: version "${version}" is an approved exception recorded in dependency-version-exceptions.json.`));
      } else if (version.includes('*') || version.trim() === '') {
        findings.push(finding('ERROR', file, `${id}: floating or empty version "${version}"; select the latest stable compatible version (${OWNER_WORKFLOW}).`));
      } else if (PRERELEASE.test(version)) {
        findings.push(finding('WARN', file, `${id}: prerelease version "${version}" is allowed only when explicitly requested (${OWNER_WORKFLOW}).`));
      }
    }
    checkPackageId(file, id, data, findings);
  }
}

function checkPackageJson(file, data, findings) {
  let pkg;
  try {
    pkg = JSON.parse(common.readText(file));
  } catch (e) {
    findings.push(finding('ERROR', file, `cannot parse package.json: ${e.message}`));
    return;
  }
  const sections = { dependencies: pkg.dependencies || {}, devDependencies: pkg.devDependencies || {} };
  let count = 0;
  for (const [section, deps] of Object.entries(sections)) {
    for (const [id, spec] of Object.entries(deps)) {
      count++;
      const s = String(spec).trim();
      if (approvedVersionException(data, 'npm', id, s, file)) {
        findings.push(finding('WARN', file, `${section}.${id}: version "${s}" is an approved exception recorded in dependency-version-exceptions.json.`));
      } else if (s === '' || s === '*' || s === 'latest' || /^x(\.x)*$/i.test(s)) {
        findings.push(finding('ERROR', file, `${section}.${id}: floating version "${s}"; pin the latest stable compatible version (${OWNER_WORKFLOW}).`));
      } else if (PRERELEASE.test(s)) {
        findings.push(finding('WARN', file, `${section}.${id}: prerelease version "${s}" is allowed only when explicitly requested (${OWNER_WORKFLOW}).`));
      }
      if (section === 'dependencies' && data.devOnlyPackages.includes(id)) {
        findings.push(finding('WARN', file, `${id} is build/test tooling listed in runtime dependencies; use devDependencies unless there is a reason (${OWNER_RULE}, npm).`));
      }
      if (data.notByDefaultPackages.includes(id)) {
        findings.push(finding('WARN', file, `${id} is not part of the frontend baseline; add it only for a concrete requirement (docs/capabilities/frontend.md).`));
      }
    }
  }
  const lock = path.posix.join(path.posix.dirname(file), 'package-lock.json');
  if (count > 0 && !common.exists(lock)) {
    findings.push(finding('WARN', file, `package-lock.json is missing; maintain and commit the lockfile (${OWNER_RULE}, npm).`));
  }
}

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

function isManifest(rel) {
  return /\.csproj$/i.test(rel) || CPM_CHAIN_FILES.has(path.posix.basename(rel)) || /(^|\/)package\.json$/.test(rel);
}

// The projects whose effective state these targets can change: a project itself, or every project below a chain file.
function cpmProjects(targets) {
  const projects = new Set();
  for (const rel of targets) {
    if (!common.exists(rel)) continue;
    if (/\.csproj$/i.test(rel)) projects.add(rel);
    else if (CPM_CHAIN_FILES.has(path.posix.basename(rel))) {
      const dir = path.posix.dirname(rel);
      for (const project of common.walk('.').filter((f) => /\.csproj$/i.test(f))) if (dir === '.' || project.startsWith(`${dir}/`)) projects.add(project);
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

function checkManifests(files) {
  common.projectRoot();
  const data = moduleData();
  const targets = files && files.length ? files : common.walk('.').filter(isManifest);
  const findings = [];
  data.versionExceptions = [];
  loadVersionExceptions(data, findings);
  for (const rel of targets) {
    if (!common.exists(rel)) continue;
    if (/\.csproj$/i.test(rel)) checkCsproj(rel, data, findings);
    else if (/Directory\.Packages\.props$/.test(rel)) checkPackagesProps(rel, data, findings);
    else if (/package\.json$/.test(rel)) checkPackageJson(rel, data, findings);
  }
  checkEffectiveCpm(targets, findings);
  return findings;
}

module.exports = { checkManifests, isManifest, packageReferences };

if (require.main === module) {
  try {
    const files = process.argv.slice(2).map((f) => {
      const rel = common.relativeInsideRoot(f, process.cwd());
      if (!rel) throw new Error(`file outside the project root: ${f}`);
      return rel;
    });
    cpmState.budgetMs = 0;
    const findings = checkManifests(files);
    if (findings.length) console.log(common.formatFindings(findings));
    const errors = findings.filter((f) => f.level === 'ERROR').length;
    const notRun = findings.filter((f) => f.message.startsWith('NOT_RUN')).length;
    console.log(`check-manifests: ${errors} error(s), ${findings.length - errors - notRun} warning(s), ${notRun} not run`);
    process.exit(errors ? 1 : notRun ? 3 : 0);
  } catch (e) {
    console.error(`check-manifests: cannot run: ${e.message}`);
    process.exit(2);
  }
}
