#!/usr/bin/env node
// Stop: co-change reminder based on the Git working tree of the active project (resolved from the
// hook input cwd, so a linked worktree is checked in its own checkout).
// Never loops: when Claude is already continuing because of this hook (stop_hook_active), it exits.
// Deduplicates by material state: the same reminders for byte-identical relevant files stay silent;
// a further change to an already-modified relevant file can remind again. State is per worktree.
import { readFileSync } from 'node:fs';
import path from 'node:path';
import {
  SetupError, git, headRevision, loadJsonFacet, matchesAny, parseSelection, readHookInput, readState, requireConfigRoot,
  resolveContext, sha256, stateFile, toPosix, writeState,
} from '../scripts/lib/project.mjs';

function output(obj) {
  process.stdout.write(JSON.stringify(obj));
  process.exit(0);
}

// Changed paths relative to the active root (porcelain v1, NUL-separated: renames list PATH then ORIG_PATH).
function changedFiles(root) {
  const prefix = git(root, ['rev-parse', '--show-prefix']);
  const status = git(root, ['status', '--porcelain=v1', '-z', '--untracked-files=all']);
  if (!prefix.ok || !status.ok) return null;
  const base = prefix.stdout.trim();
  const parts = status.stdout.split('\0');
  const files = [];
  for (let i = 0; i < parts.length; i++) {
    const entry = parts[i];
    if (entry.length < 4) continue;
    const code = entry.slice(0, 2);
    files.push(entry.slice(3));
    if (code[0] === 'R' || code[0] === 'C') i++; // skip ORIG_PATH
  }
  return files.filter((f) => f.startsWith(base)).map((f) => f.slice(base.length));
}

function contentHash(root, rel) {
  try { return sha256(readFileSync(path.join(root, rel))); } catch { return 'deleted'; }
}

async function main() {
  const input = await readHookInput();
  if (!input.ok) output({ systemMessage: `Co-change reminder skipped: ${input.error}.` });
  if (input.value.stop_hook_active) process.exit(0);

  const ctx = resolveContext(typeof input.value.cwd === 'string' ? input.value.cwd : process.cwd());
  if (!ctx.activeRoot || !ctx.active.gitTop) {
    output({ systemMessage: 'Co-change reminder skipped: the active project is not a Git working tree or git is unavailable. Check seed, migration, and test co-changes manually (verify workflow).' });
  }
  const files = changedFiles(ctx.activeRoot);
  if (files === null) output({ systemMessage: 'Co-change reminder skipped: git status failed. Check seed, migration, and test co-changes manually (verify workflow).' });
  if (files.length === 0) process.exit(0);

  const configRoot = requireConfigRoot(ctx);
  const selection = parseSelection(configRoot);
  const frame = loadJsonFacet(configRoot, selection, 'architecture', 'check');
  const persistence = loadJsonFacet(configRoot, selection, 'persistence', 'enforcement');
  const roleGlobs = (frame && frame.rolePathGlobs) || {};
  const matching = (globs) => files.filter((f) => matchesAny(f, globs));
  const reminders = [];
  const relevant = new Set();

  if (persistence && persistence.cochange) {
    const c = persistence.cochange;
    const model = matching([...(c.modelRoles || []).flatMap((r) => roleGlobs[r] || []), ...(c.modelPathGlobs || [])]);
    if (model.length) {
      model.forEach((f) => relevant.add(f));
      if (!matching(c.seederPathGlobs).length) reminders.push({ id: 'seed', text: `Domain/persistence model files changed without a seeder change: confirm seeded entities are unaffected or update the seeder (${c.owner}, step A.2).` });
      if (!matching(c.migrationPathGlobs).length) reminders.push({ id: 'migration', text: `Domain/persistence model files changed without a migration: confirm no schema change is needed (${c.owner}, step A.3).` });
    }
  }

  const productionGlobs = Object.entries(roleGlobs).filter(([role]) => role !== 'tests').flatMap(([, globs]) => globs);
  const production = files.filter((f) => f.endsWith('.cs') && matchesAny(f, productionGlobs));
  if (production.length && !matching(roleGlobs.tests || []).length) {
    production.forEach((f) => relevant.add(f));
    reminders.push({ id: 'tests', text: 'Backend production code changed without test changes: confirm existing coverage, bug-fix regression tests, and preservation of behavioral probes (verify workflow, step 4).' });
  }

  const product = files.filter((f) => f === 'SPECIFICATION.md' || f === 'CUSTOM_SETTINGS.md');
  if (product.length) {
    product.forEach((f) => relevant.add(f));
    reminders.push({ id: 'product', text: 'Product sources changed: confirm SPECIFICATION.md and CUSTOM_SETTINGS.md are consistent and synchronized (custom-settings workflow).' });
  }

  if (reminders.length === 0) process.exit(0);

  // Material state: reminder set + HEAD + content of every file that triggered a reminder.
  const material = sha256(JSON.stringify({
    reminders: reminders.map((r) => r.id).sort(),
    head: headRevision(ctx),
    files: [...relevant].sort().map((f) => [f, contentHash(ctx.activeRoot, f)]),
  }));
  const file = stateFile(ctx, 'stop-reminder');
  const previous = readState(file);
  if (previous && previous.material === material) process.exit(0);
  writeState(file, { version: 1, root: toPosix(ctx.activeRoot), material });

  output({
    decision: 'block',
    reason: `Co-change check (reminds once per material state):\n- ${reminders.map((r) => r.text).join('\n- ')}\nIf an item is already handled or not applicable, say so briefly and finish.`,
  });
}

main().catch((error) => {
  const prefix = error instanceof SetupError ? 'Hook setup problem' : 'Hook failure';
  output({ systemMessage: `${prefix} (stop-cochange): ${error.message}` });
});
