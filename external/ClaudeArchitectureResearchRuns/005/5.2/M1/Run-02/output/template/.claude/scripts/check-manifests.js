#!/usr/bin/env node
'use strict';
// Dependency-manifest check: NuGet Central Package Management, floating and
// prerelease versions, deprecated or not-by-default packages, test-framework
// mixing, and npm dependency categories.
// Policy owners: .claude/rules/dependencies.md and the add-dependency workflow;
// slot-specific package lists come from the selected capability manifests.
// Usage: node .claude/scripts/check-manifests.js [file ...]   (default: all manifests)

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

function packageReferences(xml) {
  const refs = [];
  const re = /<PackageReference\b([^>]*?)(\/?)>/g;
  let m;
  while ((m = re.exec(xml))) {
    const attrs = m[1];
    const include = /\b(?:Include|Update)\s*=\s*"([^"]+)"/.exec(attrs)?.[1];
    if (!include) continue;
    let version = /\bVersion\s*=\s*"([^"]*)"/.exec(attrs)?.[1] ?? null;
    const override = /\bVersionOverride\s*=\s*"([^"]*)"/.exec(attrs)?.[1] ?? null;
    if (m[2] !== '/') {
      const close = xml.indexOf('</PackageReference>', re.lastIndex);
      const inner = close > 0 ? xml.slice(re.lastIndex, close) : '';
      const child = /<Version>([^<]*)<\/Version>/.exec(inner)?.[1];
      if (child !== undefined) version = child;
    }
    refs.push({ id: include, version, override });
  }
  return refs;
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
  const xml = common.readText(file);
  const name = path.basename(file, '.csproj');
  const refs = packageReferences(xml);
  for (const ref of refs) {
    if (ref.version !== null) {
      findings.push(finding('ERROR', file, `PackageReference ${ref.id} declares a version; versions belong in Directory.Packages.props (${OWNER_RULE}, NuGet).`));
    }
    if (ref.override !== null) {
      findings.push(finding('WARN', file, `PackageReference ${ref.id} uses VersionOverride; this needs a concrete, documented reason (${OWNER_RULE}).`));
    }
    checkPackageId(file, ref.id, data, findings);
  }
  const ids = refs.map((r) => r.id);
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

function checkPackagesProps(file, data, findings) {
  const xml = common.readText(file);
  if (!/<ManagePackageVersionsCentrally>\s*true\s*<\/ManagePackageVersionsCentrally>/i.test(xml)) {
    findings.push(finding('ERROR', file, `Central Package Management is not enabled (ManagePackageVersionsCentrally=true) (${OWNER_RULE}).`));
  }
  const re = /<PackageVersion\b[^>]*\bInclude\s*=\s*"([^"]+)"[^>]*\bVersion\s*=\s*"([^"]*)"/g;
  let m;
  while ((m = re.exec(xml))) {
    const [, id, version] = m;
    if (version.includes('*') || version.trim() === '') {
      findings.push(finding('ERROR', file, `${id}: floating or empty version "${version}"; select the latest stable compatible version (${OWNER_WORKFLOW}).`));
    } else if (PRERELEASE.test(version)) {
      findings.push(finding('WARN', file, `${id}: prerelease version "${version}" is allowed only when explicitly requested (${OWNER_WORKFLOW}).`));
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
      if (s === '' || s === '*' || s === 'latest' || /^x(\.x)*$/i.test(s)) {
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

function isManifest(rel) {
  return /\.csproj$/i.test(rel) || /(^|\/)Directory\.Packages\.props$/.test(rel) || /(^|\/)package\.json$/.test(rel);
}

function checkManifests(files) {
  common.projectRoot();
  const data = moduleData();
  const targets = files && files.length ? files : common.walk('.').filter(isManifest);
  const findings = [];
  for (const rel of targets) {
    if (!common.exists(rel)) continue;
    if (/\.csproj$/i.test(rel)) checkCsproj(rel, data, findings);
    else if (/Directory\.Packages\.props$/.test(rel)) checkPackagesProps(rel, data, findings);
    else if (/package\.json$/.test(rel)) checkPackageJson(rel, data, findings);
  }
  return findings;
}

module.exports = { checkManifests, isManifest, packageReferences };

if (require.main === module) {
  try {
    const files = process.argv.slice(2).map((f) => {
      const rel = common.relativeInsideRoot(f);
      if (!rel) throw new Error(`file outside the project root: ${f}`);
      return rel;
    });
    const findings = checkManifests(files);
    if (findings.length) console.log(common.formatFindings(findings));
    const errors = findings.filter((f) => f.level === 'ERROR').length;
    console.log(`check-manifests: ${errors} error(s), ${findings.length - errors} warning(s)`);
    process.exit(errors ? 1 : 0);
  } catch (e) {
    console.error(`check-manifests: cannot run: ${e.message}`);
    process.exit(2);
  }
}
