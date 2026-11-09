#!/usr/bin/env node
// Claude Code PostToolUse hook for file edits (Edit, Write, MultiEdit).
//   CUSTOM_SETTINGS.md / SPECIFICATION.md -> synchronization reminder.
//   .csproj, Directory.Packages.props, Directory.Build.props, Directory.Build.targets,
//   package.json -> manifest check
//   (Central Package Management, versions, deprecated packages, project
//   references) and a pointer to the add-dependency workflow.
// The active root for an edit is the checkout or worktree of this repository
// that contains the edited file (a relative file_path is resolved against the
// input "cwd"); a file outside every checkout is not governed and is ignored.
// Registered in .claude/settings.json in exec form:
//   "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/file-change.mjs"]
// Manual test (from the repository root; "cwd" defaults to the current directory):
//   echo '{"hook_event_name":"PostToolUse","tool_input":{"file_path":"CUSTOM_SETTINGS.md"}}' | node .claude/hooks/file-change.mjs

import { dirname, isAbsolute, resolve } from 'node:path';
import { readInput, startDirectory, repoRelative, rememberManifests, postToolBlock, postToolContext, done } from './hook-io.mjs';
import { resolveActiveRepository } from '../scripts/repo-root.mjs';
import { checkManifests, formatResult } from '../scripts/check-manifests.mjs';

const input = readInput();
const toolInput = input.tool_input ?? {};
const filePath = toolInput.file_path;
if (typeof filePath !== 'string' || filePath.trim() === '') done();

const absolute = isAbsolute(filePath) ? filePath : resolve(startDirectory(input), filePath);
const repo = repositoryFrom(dirname(absolute));
const root = repo?.root;
const rel = root && repoRelative(root, absolute);
if (!rel) done(); // not a file of any checkout of this repository
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

const isManifest = name.toLowerCase().endsWith('.csproj') || name === 'Directory.Packages.props' || name === 'Directory.Build.props' || name === 'Directory.Build.targets' || name === 'package.json';
if (!isManifest || rel.split('/').includes('node_modules')) done();

const result = checkManifests(root, [resolve(root, rel)]);
rememberManifests(repo, [resolve(root, rel)]); // a later shell command does not re-report this state
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

// Active repository for the edited file's directory, or null when it belongs to
// no checkout of this repository (the file is then not governed by these rules).
function repositoryFrom(dir) {
  try {
    return resolveActiveRepository(dir);
  } catch {
    return null;
  }
}
