#!/usr/bin/env node
// Stop: co-change reminder based on the active worktree's Git state. Never loops and never repeats itself:
// - when Claude is already continuing because of this hook (stop_hook_active), it exits silently;
// - a reminder is shown once per material state: the fingerprint covers the reminder kinds and the content of
//   every file that triggered them, so an unchanged state stays silent while a further change to the same
//   file can remind again. State is kept per worktree in <active root>/.claude/.hook-state/.
// Advisory only: problems are reported as a system message, never as a blocking error.
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import {
  blobId, git, hookStateDir, loadJsonFacet, matchesAny, parseSelection, readStdinJson, resolveRoots,
} from '../scripts/lib/project.mjs';

function output(obj) {
  process.stdout.write(JSON.stringify(obj));
  process.exit(0);
}

// Changed paths (relative to the active root), or null when the active root is not a Git working tree.
function changedFiles(active) {
  const prefixOut = git(active, ['rev-parse', '--show-prefix']);
  const status = git(active, ['status', '--porcelain=v1', '-z', '--untracked-files=all', '--no-renames', '--', '.']);
  if (prefixOut === null || status === null) return null;
  const prefix = prefixOut.trim();
  return status.split('\0').filter(Boolean).map((e) => e.slice(3)).filter((f) => f.startsWith(prefix)).map((f) => f.slice(prefix.length));
}

function contentId(active, rel) {
  const abs = path.join(active, rel);
  return existsSync(abs) ? blobId(readFileSync(abs)) : 'deleted';
}

async function main() {
  let input;
  try {
    input = await readStdinJson();
  } catch (error) {
    output({ systemMessage: `Co-change reminder skipped: ${error.message}` });
  }
  if (input.stop_hook_active) process.exit(0);

  const { active, config } = resolveRoots(input.cwd);
  const files = changedFiles(active);
  const reminders = [];
  if (files === null) {
    reminders.push({ id: 'no-git', text: 'Co-change reminder unavailable: the active project is not a Git working tree or git is unavailable. Check seed, migration, and test co-changes manually (verify workflow).', files: [] });
  } else if (files.length > 0) {
    const selection = parseSelection(config);
    const frame = loadJsonFacet(config, selection, 'architecture', 'check');
    const persistence = loadJsonFacet(config, selection, 'persistence', 'enforcement');
    const roleGlobs = (frame && frame.rolePathGlobs) || {};
    const touched = (globs) => files.filter((f) => matchesAny(f, globs));

    if (persistence && persistence.cochange) {
      const c = persistence.cochange;
      const model = touched([...(c.modelRoles || []).flatMap((r) => roleGlobs[r] || []), ...(c.modelPathGlobs || [])]).filter((f) => !/\.csproj$/i.test(f));
      if (model.length > 0) {
        if (touched(c.seederPathGlobs).length === 0) reminders.push({ id: 'seed', text: `Domain/persistence model files changed without a seeder change: confirm seeded entities are unaffected or update the seeder (${c.owner}, step A.2).`, files: model });
        if (touched(c.migrationPathGlobs).length === 0) reminders.push({ id: 'migration', text: `Domain/persistence model files changed without a migration: confirm no schema change is needed (${c.owner}, step A.3).`, files: model });
      }
    }
    const productionGlobs = Object.entries(roleGlobs).filter(([role]) => role !== 'tests').flatMap(([, globs]) => globs);
    const production = files.filter((f) => f.endsWith('.cs') && matchesAny(f, productionGlobs));
    if (production.length > 0 && touched(roleGlobs.tests || []).length === 0) {
      reminders.push({ id: 'tests', text: 'Backend production code changed without test changes: confirm existing coverage, bug-fix regression tests, and preservation of behavioral probes (verify workflow, step 4).', files: production });
    }
    const product = files.filter((f) => f === 'SPECIFICATION.md' || f === 'CUSTOM_SETTINGS.md');
    if (product.length > 0) reminders.push({ id: 'product', text: 'Product sources changed: confirm SPECIFICATION.md and CUSTOM_SETTINGS.md are consistent and synchronized (custom-settings workflow).', files: product });
  }
  if (reminders.length === 0) process.exit(0);

  const material = reminders.map((r) => `${r.id}:${[...new Set(r.files)].sort().map((f) => `${f}=${contentId(active, f)}`).join(',')}`).join('|');
  const fingerprint = createHash('sha256').update(material).digest('hex');
  const stateDir = hookStateDir(active);
  const stateFile = path.join(stateDir, 'stop-state.json');
  let state = {};
  try { state = JSON.parse(readFileSync(stateFile, 'utf8')); } catch { state = {}; }
  if (state.fingerprint === fingerprint) process.exit(0);
  mkdirSync(stateDir, { recursive: true });
  writeFileSync(stateFile, JSON.stringify({ fingerprint }, null, 2));

  if (files === null) output({ systemMessage: reminders[0].text });
  output({
    decision: 'block',
    reason: `Co-change check (shown once per change state):\n- ${reminders.map((r) => r.text).join('\n- ')}\nIf an item is already handled or not applicable, say so briefly and finish.`,
  });
}

main().catch((error) => output({ systemMessage: `Hook failure (stop-cochange): ${error.message}` }));
