// Stop hook: co-change reminders computed from the Git working tree. Blocks the
// stop once per distinct set of reminders (never while stop_hook_active), so it
// cannot create an execution loop. Messages point to owners only.
import fs from 'node:fs';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { TemplateError, resolveRoot, inRoot, loadCapabilities, resolveRoleTokens, globToRegExp } from '../scripts/lib/template.mjs';
import { runInstructionChecks } from '../scripts/check-instructions.mjs';

async function readPayload() {
  let raw = '';
  for await (const chunk of process.stdin) raw += chunk;
  // Windows PowerShell 5.1 prefixes piped input with a UTF-8 byte-order mark.
  try { return JSON.parse(raw.replace(/^﻿/, '') || '{}'); } catch { throw new TemplateError('hook input is not valid JSON'); }
}

function changedFiles(root) {
  const git = spawnSync('git', ['-C', root, 'status', '--porcelain=v1', '-z', '--untracked-files=all'], { encoding: 'utf8', shell: false });
  if (git.error) return { skipped: `Git is not available (${git.error.code ?? git.error.message})` };
  if (git.status !== 0) return { skipped: 'the project is not a Git working tree' };
  // Porcelain paths are relative to the repository root; the project may be a subdirectory.
  const prefix = spawnSync('git', ['-C', root, 'rev-parse', '--show-prefix'], { encoding: 'utf8', shell: false }).stdout.trim();
  const files = [];
  const entries = git.stdout.split('\0').filter(Boolean);
  for (let i = 0; i < entries.length; i++) {
    const status = entries[i].slice(0, 2);
    const file = entries[i].slice(3);
    if (file.startsWith(prefix)) files.push(file.slice(prefix.length));
    if (/[RC]/.test(status)) i++; // skip the rename/copy source path
  }
  return { files: files.filter(f => !f.startsWith('.claude/.cache/')) };
}

function matcher(globs, frame) {
  const res = (globs ?? []).map(g => globToRegExp(resolveRoleTokens(g, frame)));
  return f => res.some(re => re.test(f));
}

export function reminders(root, files) {
  const out = [];
  const { modules } = loadCapabilities(root);
  const frame = modules.architecture?.manifest;
  const coChange = modules.persistence?.manifest?.properties?.coChange ?? {};
  const isModel = matcher(coChange.modelGlobs, frame);
  const isSeeder = matcher(coChange.seederGlobs, frame);
  const isMigration = matcher(coChange.migrationGlobs, frame);
  const isTest = f => /^backend\/[^/]*Tests\//.test(f);
  const isBackendCode = f => /^backend\/.+\.cs$/.test(f) && !isTest(f);

  const model = files.filter(isModel);
  if (model.length && !files.some(isSeeder)) out.push('Domain/persistence model files changed without a development-seeder change: confirm the seeder still matches the model (development-workflow → Change-Specific Obligations).');
  if (model.length && !files.some(isMigration)) out.push('Model or mapping files changed without a schema migration: confirm whether a migration is required (development-workflow → Change-Specific Obligations).');
  if (files.some(isMigration)) out.push('Migration files changed: review each generated migration as source code before committing (development-workflow → Change-Specific Obligations).');
  if (files.some(isBackendCode) && !files.some(isTest)) out.push('Backend production code changed without test changes: confirm regression and behavioral coverage (development-workflow → Change-Specific Obligations; verify → Preserve Behavioral Verification).');
  if (files.includes('CUSTOM_SETTINGS.md')) out.push('CUSTOM_SETTINGS.md changed: run the custom-settings workflow.');
  if (files.includes('SPECIFICATION.md')) out.push('SPECIFICATION.md changed: confirm CUSTOM_SETTINGS.md stays consistent (CLAUDE.md → Product Sources).');
  if (files.some(f => /^(CLAUDE\.md|docs\/[^/]+\.md|\.claude\/)/.test(f))) {
    const result = runInstructionChecks(root);
    if (result.errors.length) out.push(`Instruction-structure errors: run node .claude/scripts/check-instructions.mjs (${result.errors.length} error(s), first: ${result.errors[0]}).`);
  }
  return out;
}

function alreadyShown(root, fingerprint) {
  const dir = inRoot(root, '.claude/.cache');
  const file = inRoot(root, '.claude/.cache/stop-hook.json');
  let previous = null;
  try { previous = JSON.parse(fs.readFileSync(file, 'utf8')).fingerprint; } catch { previous = null; }
  if (previous === fingerprint) return true;
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(file, JSON.stringify({ fingerprint }));
  return false;
}

try {
  const payload = await readPayload();
  if (payload.stop_hook_active) process.exit(0);
  const root = resolveRoot(process.env.CLAUDE_PROJECT_DIR, payload.cwd);
  const changes = changedFiles(root);
  if (changes.skipped) {
    process.stdout.write(JSON.stringify({ systemMessage: `Co-change check skipped: ${changes.skipped}.` }));
    process.exit(0);
  }
  const list = reminders(root, changes.files);
  if (list.length) {
    const fingerprint = crypto.createHash('sha256').update(JSON.stringify([list, [...changes.files].sort()])).digest('hex');
    if (!alreadyShown(root, fingerprint)) {
      process.stdout.write(JSON.stringify({ decision: 'block', reason: ['Before finishing, address or explicitly confirm these co-change checks:', ...list.map(r => `- ${r}`)].join('\n') }));
    }
  }
  process.exit(0);
} catch (e) {
  process.stderr.write(`stop hook failed: ${e instanceof TemplateError ? e.message : e.stack}\n`);
  process.exit(1);
}
