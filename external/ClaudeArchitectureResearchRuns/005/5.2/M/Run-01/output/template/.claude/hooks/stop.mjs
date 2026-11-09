// Stop hook: co-change reminders computed from the Git working tree.
// Reminds (once per distinct set of findings per session) about seed data, migrations,
// tests, product inputs, and manifest findings. It never blocks twice in a row
// (`stop_hook_active`), so it cannot create an execution loop.
// Messages point to the owning workflow; policy text lives there, not here.
// Registered in .claude/settings.json as: node .claude/hooks/stop.mjs

import { spawnSync } from 'node:child_process';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { SetupError, formatFindings, readStdinJson, resolveProjectRoot, walkFiles } from '../scripts/lib/repo.mjs';
import { checkManifests } from '../scripts/check-manifests.mjs';

function git(root, args) {
  return spawnSync('git', args, { cwd: root, encoding: 'utf8', windowsHide: true });
}

// Changed and untracked files relative to the project root (which may be a subdirectory
// of the Git working tree).
function changedFiles(root) {
  const prefixResult = git(root, ['rev-parse', '--show-prefix']);
  if (prefixResult.error) return { error: `git is not available (${prefixResult.error.message})` };
  if (prefixResult.status !== 0) return { error: (prefixResult.stderr || 'not a Git working tree').trim() };
  const prefix = prefixResult.stdout.trim();
  const result = git(root, ['status', '--porcelain=v1', '--untracked-files=all', '--', '.']);
  if (result.status !== 0) return { error: (result.stderr || 'git status failed').trim() };
  const files = result.stdout.split(/\r?\n/).filter(Boolean).map((line) => {
    const entry = line.slice(3);
    const renamed = entry.split(' -> ');
    return renamed[renamed.length - 1].replace(/^"|"$/g, '');
  }).filter((f) => f.startsWith(prefix)).map((f) => f.slice(prefix.length));
  return { files };
}

function reminders(root, files) {
  const items = [];
  const backendCs = files.filter((f) => f.startsWith('backend/') && f.endsWith('.cs'));
  const isTest = (f) => /^backend\/[^/]*Tests?\//.test(f);
  const seedChanged = files.some((f) => /\/Seeding\//.test(f));
  const seederExists = walkFiles(root, 'backend').some((f) => /\/Seeding\/.+\.cs$/.test(f));
  const modelChanged = backendCs.some((f) =>
    /^backend\/[^/]+\.Domain\//.test(f) ||
    (/^backend\/[^/]+\.Infrastructure\/Persistence\//.test(f) && !/\/(Seeding|Migrations)\//.test(f)));

  if (modelChanged && seederExists && !seedChanged) {
    items.push('Domain or persistence files changed but the development seeder did not: check .claude/skills/development-workflow/SKILL.md (Seed data).');
  }
  if (backendCs.some((f) => /\/Migrations\//.test(f))) {
    items.push('Migration files changed: review them as source code per .claude/skills/development-workflow/SKILL.md (Migrations).');
  }
  const productionChanged = backendCs.some((f) => !isTest(f) && !/\/Migrations\//.test(f));
  if (productionChanged && !backendCs.some(isTest)) {
    items.push('Backend production code changed without test changes: confirm coverage per .claude/skills/verify/SKILL.md (Preserve Behavioral Verification) and .claude/skills/development-workflow/SKILL.md (Bug fixes).');
  }
  if (files.includes('SPECIFICATION.md') || files.includes('CUSTOM_SETTINGS.md')) {
    items.push('Product inputs changed: confirm synchronization per .claude/skills/custom-settings/SKILL.md and CLAUDE.md (Product Sources).');
  }
  if (files.some((f) => /(\.csproj|Directory\.Packages\.props|package\.json)$/.test(f))) {
    const { findings } = checkManifests(root);
    const violations = findings.filter((f) => f.level === 'violation');
    if (violations.length > 0) items.push(formatFindings('Manifest violations:', violations));
  }
  return items;
}

// Returns true when this exact message was already shown in this session.
function alreadyShown(root, sessionId, message) {
  const key = crypto.createHash('sha256').update(`${root}|${sessionId ?? ''}`).digest('hex').slice(0, 16);
  const stateFile = path.join(os.tmpdir(), `claude-stop-hook-${key}.json`);
  const digest = crypto.createHash('sha256').update(message).digest('hex');
  try {
    const previous = JSON.parse(fs.readFileSync(stateFile, 'utf8'));
    if (previous.digest === digest) return true;
  } catch {
    // No previous state: show the message.
  }
  try {
    fs.writeFileSync(stateFile, JSON.stringify({ digest }));
  } catch {
    // State is a convenience only; failing to store it just repeats the reminder later.
  }
  return false;
}

async function main() {
  const root = resolveProjectRoot(import.meta.url);
  const input = await readStdinJson();
  if (input?.stop_hook_active) return;

  const status = changedFiles(root);
  if (status.error) {
    const note = `Co-change check not run: ${status.error}.`;
    if (!alreadyShown(root, input?.session_id, note)) process.stdout.write(JSON.stringify({ systemMessage: note }));
    return;
  }

  const items = reminders(root, status.files);
  if (items.length === 0) return;
  const reason = `Co-change check before finishing:\n${items.map((i) => `- ${i}`).join('\n')}\n` +
    'Address each item or state why it does not apply, then finish.';
  if (alreadyShown(root, input?.session_id, reason)) return;
  process.stdout.write(JSON.stringify({ decision: 'block', reason }));
}

main().catch((error) => {
  const message = error instanceof SetupError ? error.message : (error?.stack ?? String(error));
  process.stderr.write(`stop hook failed; co-change checks were NOT run: ${message}\n`);
  process.exit(1);
});
