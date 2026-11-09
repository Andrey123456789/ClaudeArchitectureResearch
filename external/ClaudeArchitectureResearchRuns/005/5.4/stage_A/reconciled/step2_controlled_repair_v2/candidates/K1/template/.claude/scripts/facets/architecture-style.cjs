// Kind: ENF | Scope: backend | Capability: architecture/clean-architecture | Loading: facet of check-manifests.cjs (manifest hooks, verify)
// Conforms: .claude/rules/backend/architecture-style.md, .claude/rules/backend-tests/test-projects.md
'use strict';

const lib = require('../lib.cjs');

const OWNER_STYLE = '.claude/rules/backend/architecture-style.md';
const OWNER_TESTS = '.claude/rules/backend-tests/test-projects.md';
const LAYERS = ['Domain', 'Application', 'Infrastructure', 'Api'];

// Inward dependency direction of the Clean Architecture frame.
const ALLOWED_PRODUCTION = {
  Domain: [],
  Application: ['Domain'],
  Infrastructure: ['Application', 'Domain'],
  Api: ['Application', 'Infrastructure', 'Domain'],
};

// Typical test-project references: [allowed without remark, allowed but needing a reason].
const TEST_REFERENCES = {
  Domain: [['Domain'], []],
  Application: [['Application', 'Domain'], []],
  Infrastructure: [['Infrastructure'], ['Application', 'Domain']],
  Api: [['Api'], ['Application', 'Infrastructure', 'Domain']],
  Integration: [['Api'], ['Application', 'Infrastructure', 'Domain']],
};

/** Frame role of a backend project, derived from the <Name>.<Layer> convention. */
function roleOf(projectName) {
  if (/\.IntegrationTests$/.test(projectName)) return { kind: 'test', target: 'Integration' };
  const test = /\.(Domain|Application|Infrastructure|Api)\.Tests$/.exec(projectName);
  if (test) return { kind: 'test', target: test[1] };
  if (/\.Tests?$/.test(projectName)) return { kind: 'test', target: null };
  const layer = /\.(Domain|Application|Infrastructure|Api)$/.exec(projectName);
  if (layer) return { kind: 'production', layer: layer[1] };
  return { kind: 'unknown' };
}

function checkProject(ctx, project) {
  if (!project.rel.startsWith('backend/')) return [];
  const findings = [];
  const role = roleOf(project.name);

  if (role.kind === 'unknown') {
    findings.push(lib.finding('warn', project.rel, `project "${project.name}" matches no frame role (${LAYERS.join(', ')}, tests); a new production project is a Reserved decision`, OWNER_STYLE));
    return findings;
  }

  for (const ref of project.projectRefs) {
    const target = roleOf(ref.name);
    if (role.kind === 'production') {
      if (target.kind === 'test') {
        findings.push(lib.finding('error', project.rel, `production project references test project "${ref.name}"`, OWNER_STYLE));
      } else if (target.kind === 'production' && !ALLOWED_PRODUCTION[role.layer].includes(target.layer)) {
        findings.push(lib.finding('error', project.rel, `${role.layer} must not reference ${target.layer} ("${ref.name}")`, OWNER_STYLE));
      }
    } else if (role.kind === 'test') {
      if (target.kind === 'test') {
        findings.push(lib.finding('warn', project.rel, `test project references another test project "${ref.name}"`, OWNER_TESTS));
        continue;
      }
      if (target.kind !== 'production' || !role.target) continue;
      const [typical, justified] = TEST_REFERENCES[role.target];
      if (typical.includes(target.layer)) continue;
      if (justified.includes(target.layer)) {
        findings.push(lib.finding('warn', project.rel, `reference to ${target.layer} is broader than the typical test scope; keep it only if the tests require it`, OWNER_TESTS));
      } else {
        findings.push(lib.finding('error', project.rel, `test project for ${role.target} must not reference ${target.layer} ("${ref.name}")`, OWNER_TESTS));
      }
    }
  }

  if (role.kind === 'production' && (role.layer === 'Domain' || role.layer === 'Application')) {
    if (/Microsoft\.NET\.Sdk\.Web/i.test(project.sdk)) {
      findings.push(lib.finding('error', project.rel, `${role.layer} uses the Web SDK (ASP.NET Core transport types)`, OWNER_STYLE));
    }
    if (project.frameworkRefs.some(f => /^Microsoft\.AspNetCore\.App$/i.test(f))) {
      findings.push(lib.finding('error', project.rel, `${role.layer} references the ASP.NET Core shared framework`, OWNER_STYLE));
    }
    for (const pkg of project.packages) {
      if (/^Microsoft\.AspNetCore\./i.test(pkg.id)) {
        findings.push(lib.finding('error', project.rel, `${role.layer} references ASP.NET Core package "${pkg.id}"`, OWNER_STYLE));
      }
    }
  }
  return findings;
}

module.exports = { roleOf, checkProject };
