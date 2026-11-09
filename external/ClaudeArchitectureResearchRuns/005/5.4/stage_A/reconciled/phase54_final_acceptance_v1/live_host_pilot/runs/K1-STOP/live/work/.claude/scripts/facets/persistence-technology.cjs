// Kind: ENF | Scope: backend | Capability: persistence/ef-core | Loading: facet of check-manifests.cjs and check-cochange.cjs (hooks, verify)
// Conforms: .claude/rules/backend/persistence-technology.md
'use strict';

const lib = require('../lib.cjs');

const OWNER_STD = '.claude/rules/backend/persistence-technology.md';
const OWNER_WF = 'persistence-change workflow';

// Binds the architecture frame: EF Core packages belong to the Infrastructure role only.
function checkProject(ctx, project) {
  const role = ctx.roleOf(project.name);
  if (role.kind !== 'production' || (role.layer !== 'Domain' && role.layer !== 'Application')) return [];
  return project.packages
    .filter(pkg => /^Microsoft\.EntityFrameworkCore(\.|$)/i.test(pkg.id))
    .map(pkg => lib.finding('error', project.rel, `${role.layer} references EF Core package "${pkg.id}"`, OWNER_STD));
}

const isMigration = p => /^backend\/[^/]+\.Infrastructure\/Persistence\/Migrations\//.test(p);
const isSeeder = p => /^backend\/[^/]+\.Infrastructure\/Persistence\/Seeding\//.test(p);
const isModel = p =>
  /^backend\/[^/]+\.Domain\/.+\.cs$/.test(p) ||
  /^backend\/[^/]+\.Infrastructure\/Persistence\/Configurations\/.+\.cs$/.test(p) ||
  /^backend\/[^/]+\.Infrastructure\/Persistence\/[^/]*DbContext\.cs$/.test(p);

/** Seed and migration co-change reminders for the current working-tree changes. */
function cochange(ctx, changes) {
  const paths = changes.map(c => c.path);
  const reminders = [];
  const model = paths.filter(isModel);
  const migrations = paths.filter(isMigration);
  if (model.length && !paths.some(isSeeder)) {
    reminders.push({
      id: 'persistence-seed',
      message: `persistence model changed (${model.slice(0, 3).join(', ')}${model.length > 3 ? ', ...' : ''}) without a development seeder change; confirm whether seeded entities are affected`,
      owner: OWNER_WF,
      paths: model,
    });
  }
  if (model.length && !migrations.length) {
    reminders.push({
      id: 'persistence-migration',
      message: 'persistence model changed without a migration; confirm whether the schema changed',
      owner: OWNER_WF,
      paths: model,
    });
  }
  if (migrations.length) {
    reminders.push({
      id: 'persistence-migration-review',
      message: `migration files changed (${migrations.length}); review them as source code before committing`,
      owner: OWNER_WF,
      paths: migrations,
    });
  }
  return reminders;
}

module.exports = { checkProject, cochange };
