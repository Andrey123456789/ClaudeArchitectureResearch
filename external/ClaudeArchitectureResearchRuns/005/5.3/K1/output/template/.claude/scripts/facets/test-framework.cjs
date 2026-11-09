// Kind: ENF | Scope: backend-tests | Capability: backend-testing/nunit | Loading: facet of check-manifests.cjs (manifest hooks, verify)
// Conforms: .claude/rules/backend-tests/test-framework.md
'use strict';

const lib = require('../lib.cjs');

const OWNER = '.claude/rules/backend-tests/test-framework.md';
// Test frameworks other than NUnit; introducing one needs a concrete reason.
const OTHER_FRAMEWORKS = /^(xunit(\.v3)?|xunit\.core|mstest|mstest\.testframework|mstest\.testadapter|tunit)$/i;

function checkProject(ctx, project) {
  if (ctx.roleOf(project.name).kind !== 'test') return [];
  return project.packages
    .filter(pkg => OTHER_FRAMEWORKS.test(pkg.id))
    .map(pkg => lib.finding('warn', project.rel, `test project uses "${pkg.id}" in addition to or instead of NUnit`, OWNER));
}

function checkCentralPackages(ctx, rel, packages) {
  return packages
    .filter(pkg => OTHER_FRAMEWORKS.test(pkg.id))
    .map(pkg => lib.finding('warn', rel, `central version for additional test framework "${pkg.id}"`, OWNER));
}

module.exports = { checkProject, checkCentralPackages };
