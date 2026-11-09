#!/usr/bin/env node
// Owns: PostToolUse reactions to file edits — product-source synchronization
// reminders and manifest checks after project/package manifest changes.
// Scope: common. Loads: PostToolUse hook (Edit|Write|MultiEdit) from .claude/settings.json.

import { basename, relative, resolve } from 'node:path';
import { checkManifests, formatFindings } from '../scripts/check-manifests.mjs';

function readStdin() {
  return new Promise((done) => {
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', (chunk) => (data += chunk));
    process.stdin.on('end', () => done(data));
  });
}

function emit(payload) {
  process.stdout.write(JSON.stringify(payload));
  process.exit(0);
}

function remind(text) {
  emit({ hookSpecificOutput: { hookEventName: 'PostToolUse', additionalContext: text } });
}

let input = {};
try { input = JSON.parse((await readStdin()) || '{}'); } catch { process.exit(0); } // never fail the tool call on bad input
const filePath = String(input?.tool_input?.file_path ?? '');
const name = basename(filePath.replace(/\\/g, '/'));
const root = resolve(process.env.CLAUDE_PROJECT_DIR ?? input?.cwd ?? process.cwd());

if (name === 'SPECIFICATION.md') {
  remind(
    'SPECIFICATION.md changed: check CUSTOM_SETTINGS.md and the implementation for conflicts or drift ' +
      '(CLAUDE.md, Product Sources).',
  );
}

if (name === 'CUSTOM_SETTINGS.md') {
  remind('CUSTOM_SETTINGS.md changed: run the custom-settings workflow (.claude/skills/custom-settings/SKILL.md).');
}

if (/\.csproj$/i.test(name) || name === 'Directory.Packages.props' || name === 'Directory.Build.props' || name === 'package.json') {
  const edited = relative(root, resolve(root, filePath)).split('\\').join('/');
  const findings = checkManifests(root).filter(([file]) => file === edited);
  if (findings.length) {
    emit({
      decision: 'block',
      reason: `Manifest check found ${findings.length} issue(s):\n${formatFindings(findings)}`,
    });
  }
}

process.exit(0);
