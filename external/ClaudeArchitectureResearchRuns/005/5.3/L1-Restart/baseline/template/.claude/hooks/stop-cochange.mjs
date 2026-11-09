#!/usr/bin/env node
// Stop: one-time co-change reminder based on the Git working tree.
// Never loops: when Claude is already continuing because of this hook (stop_hook_active), it exits.
import { spawnSync } from 'node:child_process';
import {
  SetupError, loadJsonFacet, matchesAny, parseSelection, readStdinJson, resolveRoot,
} from '../scripts/lib/project.mjs';

function output(obj) {
  process.stdout.write(JSON.stringify(obj));
  process.exit(0);
}

function changedFiles(root) {
  const prefixResult = spawnSync('git', ['-C', root, 'rev-parse', '--show-prefix'], { encoding: 'utf8' });
  const result = spawnSync('git', ['-C', root, 'status', '--porcelain', '--untracked-files=all'], { encoding: 'utf8' });
  if (prefixResult.error || prefixResult.status !== 0 || result.error || result.status !== 0) return null;
  const prefix = prefixResult.stdout.trim();
  // Porcelain paths are relative to the repository top level; make them relative to the project root.
  return result.stdout.split(/\r?\n/).filter(Boolean).map((line) => {
    const entry = line.slice(3).trim().replace(/^"|"$/g, '');
    const arrow = entry.indexOf(' -> ');
    return arrow >= 0 ? entry.slice(arrow + 4) : entry;
  }).filter((f) => f.startsWith(prefix)).map((f) => f.slice(prefix.length));
}

async function main() {
  const input = await readStdinJson();
  if (input.stop_hook_active) process.exit(0);

  const root = resolveRoot();
  const files = changedFiles(root);
  if (files === null) {
    output({ systemMessage: 'Co-change reminder skipped: this project is not a Git working tree or git is unavailable. Check seed, migration, and test co-changes manually (verify workflow).' });
  }
  if (files.length === 0) process.exit(0);

  const selection = parseSelection(root);
  const frame = loadJsonFacet(root, selection, 'architecture', 'check');
  const persistence = loadJsonFacet(root, selection, 'persistence', 'enforcement');
  const roleGlobs = (frame && frame.rolePathGlobs) || {};
  const changed = (globs) => files.some((f) => matchesAny(f, globs));
  const reminders = [];

  if (persistence && persistence.cochange) {
    const c = persistence.cochange;
    const modelGlobs = [...(c.modelRoles || []).flatMap((r) => roleGlobs[r] || []), ...(c.modelPathGlobs || [])];
    if (changed(modelGlobs)) {
      if (!changed(c.seederPathGlobs)) reminders.push(`Domain/persistence model files changed without a seeder change: confirm seeded entities are unaffected or update the seeder (${c.owner}, step A.2).`);
      if (!changed(c.migrationPathGlobs)) reminders.push(`Domain/persistence model files changed without a migration: confirm no schema change is needed (${c.owner}, step A.3).`);
    }
  }

  const productionGlobs = Object.entries(roleGlobs).filter(([role]) => role !== 'tests').flatMap(([, globs]) => globs);
  const productionCode = files.some((f) => f.endsWith('.cs') && matchesAny(f, productionGlobs));
  if (productionCode && !changed(roleGlobs.tests || [])) {
    reminders.push('Backend production code changed without test changes: confirm existing coverage, bug-fix regression tests, and preservation of behavioral probes (verify workflow, step 4).');
  }

  if (files.includes('SPECIFICATION.md') || files.includes('CUSTOM_SETTINGS.md')) {
    reminders.push('Product sources changed: confirm SPECIFICATION.md and CUSTOM_SETTINGS.md are consistent and synchronized (custom-settings workflow).');
  }

  if (reminders.length === 0) process.exit(0);
  output({
    decision: 'block',
    reason: `Co-change check (one-time):\n- ${reminders.join('\n- ')}\nIf an item is already handled or not applicable, say so briefly and finish.`,
  });
}

main().catch((error) => {
  const prefix = error instanceof SetupError ? 'Hook setup problem' : 'Hook failure';
  output({ systemMessage: `${prefix} (stop-cochange): ${error.message}` });
});
