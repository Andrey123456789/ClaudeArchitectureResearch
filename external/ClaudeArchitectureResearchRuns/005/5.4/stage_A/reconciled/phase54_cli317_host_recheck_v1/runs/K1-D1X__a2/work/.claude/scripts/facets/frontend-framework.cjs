// Kind: ENF | Scope: frontend | Capability: frontend/angular | Loading: facet of check-manifests.cjs (manifest hooks, verify)
// Conforms: docs/architecture/decision-register.md, .claude/rules/frontend/dependencies.md
'use strict';

const lib = require('../lib.cjs');

const OWNER_DEC = 'docs/architecture/decision-register.md (frontend: not added by default)';
const OWNER_NPM = '.claude/rules/frontend/dependencies.md';

// Libraries the Angular selection does not add by default (concrete need required).
const NOT_BY_DEFAULT = [/^@ngrx\//, /^axios$/, /^lodash(-es)?$/, /^bootstrap$/, /^@ng-bootstrap\//, /^ngx-bootstrap$/, /^tailwindcss$/];
// Angular build tooling that belongs in devDependencies.
const BUILD_TOOLING = [/^@angular\/cli$/, /^@angular\/build$/, /^@angular-devkit\//, /^@angular\/compiler-cli$/];

function checkPackageJson(ctx, rel, pkg) {
  if (!rel.startsWith('frontend/')) return [];
  const findings = [];
  for (const section of ['dependencies', 'devDependencies']) {
    for (const name of Object.keys(pkg[section] || {})) {
      if (NOT_BY_DEFAULT.some(re => re.test(name))) {
        findings.push(lib.finding('warn', rel, `"${name}" is not added by default; confirm the concrete need`, OWNER_DEC));
      }
    }
  }
  for (const name of Object.keys(pkg.dependencies || {})) {
    if (BUILD_TOOLING.some(re => re.test(name))) {
      findings.push(lib.finding('warn', rel, `build tooling "${name}" is in runtime dependencies`, OWNER_NPM));
    }
  }
  return findings;
}

module.exports = { checkPackageJson };
