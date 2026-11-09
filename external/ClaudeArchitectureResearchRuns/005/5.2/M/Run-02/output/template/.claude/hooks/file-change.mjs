#!/usr/bin/env node
// Claude Code PostToolUse hook for file edits (Edit, Write, MultiEdit).
//   CUSTOM_SETTINGS.md / SPECIFICATION.md -> synchronization reminder.
//   .csproj, Directory.Packages.props, package.json -> manifest check
//   (Central Package Management, versions, deprecated packages, project
//   references) and a pointer to the add-dependency workflow.
// Configured in .claude/settings.json as: node .claude/hooks/file-change.mjs
// Manual test: echo '{"hook_event_name":"PostToolUse","tool_input":{"file_path":"CUSTOM_SETTINGS.md"}}' | node .claude/hooks/file-change.mjs

import { resolve } from 'node:path';
import { readInput, projectRoot, repoRelative, postToolBlock, postToolContext, done } from './hook-io.mjs';
import { checkManifests, formatResult } from '../scripts/check-manifests.mjs';

const input = readInput();
const toolInput = input.tool_input ?? {};
const filePath = toolInput.file_path;
if (typeof filePath !== 'string' || filePath.trim() === '') done();

const root = projectRoot();
const rel = repoRelative(root, filePath);
if (rel === null) done();
const name = rel.split('/').pop();

if (rel === 'CUSTOM_SETTINGS.md') {
  postToolContext(
    'CUSTOM_SETTINGS.md changed: run the custom-settings workflow to synchronize every affected surface, ' +
    'and confirm it stays consistent with SPECIFICATION.md (CLAUDE.md, Custom Settings).',
  );
}

if (rel === 'SPECIFICATION.md') {
  postToolContext(
    'SPECIFICATION.md changed: confirm it stays consistent with CUSTOM_SETTINGS.md (CLAUDE.md, Custom Settings) ' +
    'and carry approved behavior changes through the development-workflow.',
  );
}

const isManifest = name.toLowerCase().endsWith('.csproj') || name === 'Directory.Packages.props' || name === 'package.json';
if (!isManifest || rel.split('/').includes('node_modules')) done();

const result = checkManifests(root, [resolve(root, rel)]);
const lines = formatResult(result);
if (result.violations.length > 0) {
  postToolBlock(
    `Manifest check failed for ${rel}:\n${lines.join('\n')}\n` +
    'Fix the manifest following the owners named above; dependency changes follow the add-dependency workflow.',
  );
}

const editedText = [toolInput.content, toolInput.new_string, ...(toolInput.edits ?? []).map((e) => e?.new_string)]
  .filter((text) => typeof text === 'string')
  .join('\n');
const touchesDependencies = name === 'Directory.Packages.props' ||
  /PackageReference|PackageVersion|"(dev|optional|peer)?[dD]ependencies"|"[@a-z0-9][^"]*"\s*:\s*"[~^<>=]?\d/.test(editedText);

const parts = [];
if (touchesDependencies) {
  parts.push(`${rel} edited: dependency additions, updates, and removals follow the add-dependency workflow.`);
}
if (lines.length > 0) parts.push(`Manifest notes:\n${lines.join('\n')}`);
if (parts.length > 0) postToolContext(parts.join('\n'));
done();
