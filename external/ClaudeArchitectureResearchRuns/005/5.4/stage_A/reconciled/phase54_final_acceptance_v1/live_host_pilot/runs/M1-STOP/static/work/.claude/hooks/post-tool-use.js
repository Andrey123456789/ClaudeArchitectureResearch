'use strict';
// PostToolUse hook entry point (Write, Edit, MultiEdit, Bash, PowerShell) and
// PostToolUseFailure entry point (Bash, PowerShell: a failed command may still have
// changed files).
// After a change it runs the deterministic checks that apply to the touched
// file: manifests (central package management, versions, deny-list, project
// references), inner-layer namespaces, product-source synchronization
// reminders, and the instruction-structure check. All checks run against the
// active repository or worktree (hook input cwd; see scripts/lib/common.js).
// Shell commands are judged by their effect: the content of every dependency manifest
// and project file is compared with the state recorded after the previous check, kept
// per worktree in its own Git directory. Changed manifests are validated whatever
// command changed them (scripts, partial effects of failed commands, branch switches);
// a worktree without recorded state is validated completely once. Removals and moves
// are always reported, and uncommitted changes that no recognized dependency or
// project-reference command explains are routed to their workflows.
// Findings are returned to Claude as hook JSON (see scripts/lib/hook-output.js);
// a hook failure is reported visibly.

const crypto = require('crypto');
const fs = require('fs');
const common = require('../scripts/lib/common.js');
const out = require('../scripts/lib/hook-output.js');
const { changesManifests } = require('../scripts/lib/dependency-commands.js');
const { checkManifests, isManifest } = require('../scripts/check-manifests.js');
const { checkArchitecture } = require('../scripts/check-architecture.js');
const instructions = require('../scripts/check-instructions.js');

const MAX_LINES = 25;
const MANIFEST_STATE = 'claude-manifest-state.json';
const MANIFEST_TITLE = 'Manifest check (.claude/rules/dependencies.md)';
const ARCHITECTURE_TITLE = 'Architecture check (.claude/rules/architecture.md)';
const isProject = (rel) => /\.csproj$/i.test(rel);

function sha256(data) {
  return crypto.createHash('sha256').update(data).digest('hex');
}

function changedText(toolInput) {
  if (!toolInput) return '';
  if (typeof toolInput.content === 'string') return toolInput.content;
  if (typeof toolInput.new_string === 'string') return toolInput.new_string;
  if (Array.isArray(toolInput.edits)) return toolInput.edits.map((e) => e.new_string || '').join('\n');
  return '';
}

function limit(lines) {
  const shown = lines.slice(0, MAX_LINES);
  if (lines.length > MAX_LINES) shown.push(`... ${lines.length - MAX_LINES} more`);
  return shown;
}

function report(findings, title) {
  const relevant = findings.filter((f) => f.level === 'ERROR' || f.level === 'WARN');
  if (!relevant.length) return [];
  return [`${title}:`, ...limit(common.formatFindings(relevant).split('\n'))];
}

function fileChecks(rel, text) {
  const msgs = [];
  if (isManifest(rel)) {
    msgs.push(...report(checkManifests([rel]), `Manifest check for ${rel} (.claude/rules/dependencies.md)`));
    if (isProject(rel)) msgs.push(...report(checkArchitecture([]).findings, ARCHITECTURE_TITLE));
    if (/PackageReference|PackageVersion|"(?:dev)?[dD]ependencies"/.test(text) || rel.endsWith('package.json')) {
      msgs.push(`Dependency entries changed in ${rel}: confirm the add-dependency workflow was applied (.claude/skills/add-dependency/SKILL.md).`);
    }
  }
  if (rel.startsWith('backend/') && rel.endsWith('.cs')) {
    const errors = checkArchitecture([rel]).findings.filter((f) => f.level === 'ERROR' && f.file.startsWith(rel));
    msgs.push(...report(errors, 'Layer boundary check (.claude/rules/architecture.md)'));
  }
  if (rel === 'SPECIFICATION.md') {
    msgs.push('SPECIFICATION.md changed: keep it consistent with CUSTOM_SETTINGS.md (CLAUDE.md, Product Sources); record approved behavior through the architecture-decision workflow.');
  }
  if (rel === 'CUSTOM_SETTINGS.md') {
    msgs.push('CUSTOM_SETTINGS.md changed: run the custom-settings workflow (.claude/skills/custom-settings/SKILL.md) to synchronize every affected surface.');
  }
  if (instructions.isInstructionPath(rel)) {
    const { findings } = instructions.run();
    msgs.push(...report(findings.filter((f) => f.level === 'ERROR'), 'Instruction-structure check (template-maintenance workflow)'));
  }
  return msgs;
}

// ---------- manifest state (shell commands) ----------

// Recorded state of the active root ({ file: content hash }), or null when there is none.
function readManifestState(file) {
  try {
    const state = JSON.parse(fs.readFileSync(file, 'utf8'));
    return state.root === common.root() && state.files && typeof state.files === 'object' ? state.files : null;
  } catch {
    return null;
  }
}

function writeManifestState(file, files) {
  const tmp = `${file}.${process.pid}.tmp`;
  try {
    fs.writeFileSync(tmp, JSON.stringify({ root: common.root(), files }), 'utf8');
    fs.renameSync(tmp, file);
  } catch {
    // Without stored state the next shell command compares with older state and checks again.
    try {
      fs.rmSync(tmp, { force: true });
    } catch {
      // nothing left to clean up
    }
  }
}

function manifestSnapshot() {
  const files = {};
  for (const rel of common.walk('.').filter(isManifest)) {
    try {
      files[rel] = sha256(fs.readFileSync(common.absPath(rel)));
    } catch {
      // removed while the snapshot was taken
    }
  }
  return files;
}

// Manifest changes since the recorded state; null when there is no Git directory to keep state in.
function manifestChanges() {
  let file;
  try {
    file = common.stateFile(MANIFEST_STATE);
  } catch {
    return null;
  }
  const before = readManifestState(file);
  const after = manifestSnapshot();
  const save = () => writeManifestState(file, after);
  if (!before) return { initial: true, changed: Object.keys(after).sort(), added: [], removed: [], moved: [], save };
  const changed = Object.keys(after).filter((f) => before[f] !== after[f]).sort();
  const gone = Object.keys(before).filter((f) => !(f in after)).sort();
  const added = changed.filter((f) => !(f in before));
  const moved = [];
  for (const from of gone) {
    const to = added.find((f) => after[f] === before[from] && !moved.some(([, t]) => t === f));
    if (to) moved.push([from, to]);
  }
  const removed = gone.filter((f) => !moved.some(([m]) => m === f));
  return { initial: false, changed, added, removed, moved, save: changed.length || gone.length ? save : () => {} };
}

// Every removal or move, and uncommitted changes that no recognized command explains
// (changes that leave the files equal to the checked-out revision are only validated).
function changeNotes(delta, recognized) {
  const movedTo = new Set(delta.moved.map(([, to]) => to));
  const candidates = recognized ? [] : delta.changed.filter((f) => !movedTo.has(f));
  const uncommitted = new Set(candidates.length ? common.changedFiles(candidates) : []);
  const lines = [
    ...candidates.filter((f) => uncommitted.has(f)).map((f) => `${delta.added.includes(f) ? 'added' : 'modified'}: ${f}`),
    ...delta.removed.map((f) => `removed: ${f}`),
    ...delta.moved.map(([from, to]) => `moved: ${from} -> ${to}`),
  ];
  if (!lines.length) return [];
  return [
    recognized
      ? 'Dependency manifests or project files removed or moved:'
      : 'Dependency manifests or project files changed without a recognized dependency or project-reference command:',
    ...limit(lines.map((l) => `- ${l}`)),
    'Confirm the owning workflow was applied: dependency entries, add-dependency (.claude/skills/add-dependency/SKILL.md); projects and project references, project-structure (.claude/skills/project-structure/SKILL.md). A branch switch or another change of the checked-out revision needs no workflow.',
  ];
}

function shellChecks(command, tool) {
  const recognized = changesManifests(command, tool);
  const delta = manifestChanges();
  const msgs = [];
  if (recognized) {
    msgs.push(...report(checkManifests([]), MANIFEST_TITLE));
    msgs.push(...report(checkArchitecture([]).findings, ARCHITECTURE_TITLE));
  } else if (delta) {
    const touched = [...delta.changed, ...delta.removed, ...delta.moved.flat()];
    if (delta.changed.length) msgs.push(...report(checkManifests(delta.changed), MANIFEST_TITLE));
    if (touched.some(isProject)) msgs.push(...report(checkArchitecture([]).findings, ARCHITECTURE_TITLE));
  }
  if (delta && !delta.initial) msgs.push(...changeNotes(delta, recognized));
  if (delta) delta.save();
  return msgs;
}

// A manifest edited through Write/Edit was checked above; record it so that the next
// shell command does not report the same change again. Only files the snapshot covers
// are recorded (not, for example, files inside a nested worktree or node_modules).
function recordManifestEdit(rel) {
  let file;
  try {
    file = common.stateFile(MANIFEST_STATE);
  } catch {
    return;
  }
  const files = readManifestState(file);
  if (!files) return;
  const now = manifestSnapshot();
  if (rel in now) files[rel] = now[rel];
  else delete files[rel];
  writeManifestState(file, files);
}

try {
  const input = common.readStdinJson();
  const event = input.hook_event_name || 'PostToolUse';
  const cwd = input.cwd || process.cwd();
  common.useActiveRoot(cwd);
  const tool = input.tool_name || '';
  const toolInput = input.tool_input || {};
  let messages = [];
  if (['Write', 'Edit', 'MultiEdit'].includes(tool)) {
    const rel = common.relativeInsideRoot(toolInput.file_path, cwd);
    if (rel) {
      messages = fileChecks(rel, changedText(toolInput));
      if (isManifest(rel)) recordManifestEdit(rel);
    }
  } else if (['Bash', 'PowerShell'].includes(tool)) {
    messages = shellChecks(toolInput.command, tool);
  }
  if (messages.length && event === 'PostToolUseFailure') out.addContext(event, messages.join('\n'));
  if (messages.length) out.block(messages.join('\n'));
  out.allow();
} catch (e) {
  out.fail('post-tool-use', e, 'post-change checks were not applied');
}
