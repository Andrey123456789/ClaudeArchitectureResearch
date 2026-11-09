'use strict';
// Stop hook entry point: co-change reminders over the uncommitted change set of
// the active repository or worktree (hook input cwd; see scripts/lib/common.js).
// - persistence model changed without seed-data or migration changes
//   (patterns from the selected persistence manifest);
// - backend production code changed without backend test changes;
// - product sources changed;
// - manifest errors.
// Loop safety: it never re-blocks while stop_hook_active is set, and it does not
// repeat a reminder for an unchanged state. The state identity is a hash of the
// reminders and the current content of every changed file they were derived from,
// stored in the worktree's own Git directory, so a content change re-arms the
// reminder and one worktree never suppresses another.
// Reminders are returned to Claude as hook JSON (see scripts/lib/hook-output.js);
// a hook failure is reported visibly.

const crypto = require('crypto');
const fs = require('fs');
const common = require('../scripts/lib/common.js');
const hook = require('../scripts/lib/hook-output.js');
const { checkManifests, isManifest } = require('../scripts/check-manifests.js');

function sha256(data) {
  return crypto.createHash('sha256').update(data).digest('hex');
}

// Content identity of a changed path: file hash, or a marker for a deleted path or a directory.
function contentIdentity(rel) {
  try {
    const abs = common.absPath(rel);
    const stat = fs.statSync(abs);
    return stat.isDirectory() ? 'directory' : sha256(fs.readFileSync(abs));
  } catch {
    return 'missing';
  }
}

// Returns the reminders and the changed files each reminder was derived from.
function reminders(files) {
  const messages = [];
  const inputs = new Set();
  const modules = common.loadSelectedModules();
  const persistence = common.moduleFor(modules, 'persistence');
  const coChange = persistence && persistence.manifest.enforcement && persistence.manifest.enforcement.coChange;
  if (coChange) {
    const model = files.filter((f) => common.matchesAny(f, coChange.model));
    if (model.length) {
      const companions = Object.entries(coChange.companions || {});
      const missing = companions.filter(([, globs]) => !files.some((f) => common.matchesAny(f, globs))).map(([name]) => name);
      if (missing.length) {
        messages.push(`Persistence model files changed (${model.slice(0, 3).join(', ')}${model.length > 3 ? ', ...' : ''}) without ${missing.join(' or ')} changes: confirm the persistence-change workflow was applied (${coChange.owner}).`);
        model.forEach((f) => inputs.add(f));
        files.filter((f) => companions.some(([, globs]) => common.matchesAny(f, globs))).forEach((f) => inputs.add(f));
      }
    }
  }
  const frame = common.moduleFor(modules, 'architecture');
  const testSuffixes = ((frame && frame.manifest.enforcement.architecture.testProjects) || []).map((t) => t.suffix);
  const isTest = (f) => testSuffixes.some((s) => f.split('/').some((seg) => seg.endsWith(s))) || /Tests\//.test(f);
  const backendCode = files.filter((f) => f.startsWith('backend/') && f.endsWith('.cs'));
  if (backendCode.some((f) => !isTest(f)) && !backendCode.some(isTest)) {
    messages.push('Backend production code changed without test changes: check regression coverage and behavioral-probe preservation (development-workflow, verify).');
    backendCode.forEach((f) => inputs.add(f));
  }
  for (const source of ['CUSTOM_SETTINGS.md', 'SPECIFICATION.md']) {
    if (!files.includes(source)) continue;
    messages.push(
      source === 'CUSTOM_SETTINGS.md'
        ? 'CUSTOM_SETTINGS.md changed: confirm the custom-settings workflow synchronized every affected surface.'
        : 'SPECIFICATION.md changed: confirm it stays consistent with CUSTOM_SETTINGS.md and the implementation (CLAUDE.md, Product Sources).'
    );
    inputs.add(source);
  }
  const manifests = files.filter(isManifest).filter((f) => common.exists(f));
  if (manifests.length) {
    const errors = checkManifests(manifests).filter((f) => f.level === 'ERROR');
    if (errors.length) {
      messages.push(`Manifest errors (.claude/rules/dependencies.md):\n${common.formatFindings(errors)}`);
      manifests.forEach((f) => inputs.add(f));
    }
  }
  return { messages, inputs: [...inputs].sort() };
}

try {
  const input = common.readStdinJson();
  if (input.stop_hook_active) hook.allow();
  common.useActiveRoot(input.cwd || process.cwd());
  const files = common.changedFiles();
  if (!files.length) hook.allow();
  const { messages, inputs } = reminders(files);
  if (!messages.length) hook.allow();
  const fingerprint = sha256(JSON.stringify({ messages, state: inputs.map((f) => [f, contentIdentity(f)]) }));
  const file = common.stateFile('claude-stop-check.json');
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
