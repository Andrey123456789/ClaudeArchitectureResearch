'use strict';
// Stop hook entry point: co-change reminders over the uncommitted change set.
// - persistence model changed without seed-data or migration changes
//   (patterns from the selected persistence manifest);
// - backend production code changed without backend test changes;
// - product sources changed;
// - manifest errors.
// It never re-blocks while stop_hook_active is set and does not repeat a
// reminder for an unchanged change set, so it cannot create an execution loop.
// Reminders are returned to Claude as hook JSON (see scripts/lib/hook-output.js);
// a hook failure is reported visibly.

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const common = require('../scripts/lib/common.js');
const hook = require('../scripts/lib/hook-output.js');
const { checkManifests, isManifest } = require('../scripts/check-manifests.js');

function git(args) {
  const r = spawnSync('git', args, { cwd: common.ROOT, encoding: 'utf8', windowsHide: true });
  if (r.error) throw new Error(`git is not available (${r.error.message})`);
  if (r.status !== 0) throw new Error(`git ${args[0]} failed: ${(r.stderr || '').trim()}`);
  return r.stdout;
}

function changedFiles() {
  const top = path.resolve(git(['rev-parse', '--show-toplevel']).trim());
  const status = git(['status', '--porcelain=v1', '-z', '--untracked-files=all']);
  const files = [];
  const parts = status.split('\0').filter(Boolean);
  for (let i = 0; i < parts.length; i++) {
    const code = parts[i].slice(0, 2);
    const file = parts[i].slice(3);
    if (code.includes('R') || code.includes('C')) i++;
    const rel = common.relativeInsideRoot(path.join(top, file));
    if (rel) files.push(rel);
  }
  return files.sort();
}

function stateFile() {
  return path.join(git(['rev-parse', '--absolute-git-dir']).trim(), 'claude-stop-check.json');
}

function reminders(files) {
  const messages = [];
  const modules = common.loadSelectedModules();
  const persistence = common.moduleFor(modules, 'persistence');
  const coChange = persistence && persistence.manifest.enforcement && persistence.manifest.enforcement.coChange;
  if (coChange) {
    const model = files.filter((f) => common.matchesAny(f, coChange.model));
    if (model.length) {
      const missing = Object.entries(coChange.companions || {})
        .filter(([, globs]) => !files.some((f) => common.matchesAny(f, globs)))
        .map(([name]) => name);
      if (missing.length) {
        messages.push(`Persistence model files changed (${model.slice(0, 3).join(', ')}${model.length > 3 ? ', ...' : ''}) without ${missing.join(' or ')} changes: confirm the persistence-change workflow was applied (${coChange.owner}).`);
      }
    }
  }
  const frame = common.moduleFor(modules, 'architecture');
  const testSuffixes = ((frame && frame.manifest.enforcement.architecture.testProjects) || []).map((t) => t.suffix);
  const isTest = (f) => testSuffixes.some((s) => f.split('/').some((seg) => seg.endsWith(s))) || /Tests\//.test(f);
  const backendCode = files.filter((f) => f.startsWith('backend/') && f.endsWith('.cs'));
  if (backendCode.some((f) => !isTest(f)) && !backendCode.some(isTest)) {
    messages.push('Backend production code changed without test changes: check regression coverage and behavioral-probe preservation (development-workflow, verify).');
  }
  if (files.includes('CUSTOM_SETTINGS.md')) messages.push('CUSTOM_SETTINGS.md changed: confirm the custom-settings workflow synchronized every affected surface.');
  if (files.includes('SPECIFICATION.md')) messages.push('SPECIFICATION.md changed: confirm it stays consistent with CUSTOM_SETTINGS.md and the implementation (CLAUDE.md, Product Sources).');
  const manifests = files.filter(isManifest).filter((f) => common.exists(f));
  if (manifests.length) {
    const errors = checkManifests(manifests).filter((f) => f.level === 'ERROR');
    if (errors.length) messages.push(`Manifest errors (.claude/rules/dependencies.md):\n${common.formatFindings(errors)}`);
  }
  return messages;
}

try {
  common.projectRoot();
  const input = common.readStdinJson();
  if (input.stop_hook_active) hook.allow();
  const files = changedFiles();
  if (!files.length) hook.allow();
  const messages = reminders(files);
  if (!messages.length) hook.allow();
  const fingerprint = crypto.createHash('sha256').update(JSON.stringify({ files, messages })).digest('hex');
  const file = stateFile();
  let state = {};
  try {
    state = JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch {
    state = {};
  }
  if (state.fingerprint === fingerprint) hook.allow();
  try {
    fs.writeFileSync(file, JSON.stringify({ fingerprint }), 'utf8');
  } catch {
    // Without stored state the reminder may repeat on a later stop; stop_hook_active still prevents a loop.
  }
  hook.block(`Co-change check:\n- ${messages.join('\n- ')}\nAddress these or state why they do not apply, then finish.`);
} catch (e) {
  hook.fail('stop', e, 'the co-change check was not run');
}
