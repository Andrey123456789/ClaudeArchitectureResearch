// Kind: ENF | Scope: repo/meta | Owns: PostToolUse checks for manifests, product inputs and instruction files | Loads: PostToolUse hook (Write|Edit|MultiEdit)
//
// - package/project manifest edited -> run check-manifests (CPM, versions, gated packages, project references)
// - SPECIFICATION.md / CUSTOM_SETTINGS.md edited -> synchronization reminder pointing to the owners
// - instruction file edited -> run check-instructions (Kind/Scope structure, references, register)

import path from 'node:path';
import { readHookInput, resolveProjectRoot, toProjectRelative, fail, feedback } from './hook-io.mjs';
import { checkManifests, formatFindings as formatManifestFindings } from '../scripts/check-manifests.mjs';
import { checkInstructions, formatFindings as formatInstructionFindings } from '../scripts/check-instructions.mjs';

const HOOK = 'post-edit-checks';

export function isManifest(relativePath) {
  const name = path.posix.basename(relativePath);
  return /\.csproj$/i.test(name) || /^Directory\.(Packages|Build)\.props$/i.test(name) || name === 'package.json';
}

export function isInstructionFile(relativePath) {
  return relativePath === 'CLAUDE.md'
    || relativePath.startsWith('.claude/')
    || relativePath.startsWith('docs/architecture/')
    || relativePath.startsWith('docs/decisions/');
}

export function productInputReminder(relativePath) {
  if (relativePath === 'CUSTOM_SETTINGS.md') {
    return 'CUSTOM_SETTINGS.md changed: run the custom-settings workflow (.claude/skills/custom-settings/SKILL.md) '
      + 'to synchronize every affected surface; approval and conflicts: CLAUDE.md § Product Inputs.';
  }
  if (relativePath === 'SPECIFICATION.md') {
    return 'SPECIFICATION.md changed: check consistency with CUSTOM_SETTINGS.md (CLAUDE.md § Product Inputs) '
      + 'and follow development-workflow § 5 for approved behavior.';
  }
  return null;
}

export function evaluate(root, relativePath) {
  const messages = [];
  if (isManifest(relativePath)) {
    const result = checkManifests(root);
    if (result.findings.length) {
      messages.push(`Manifest check after editing ${relativePath}:\n${formatManifestFindings(result.findings)}`);
    }
  }
  const reminder = productInputReminder(relativePath);
  if (reminder) {
    messages.push(reminder);
  }
  if (isInstructionFile(relativePath)) {
    const result = checkInstructions(root);
    if (result.errors.length) {
      messages.push(`Instruction-structure check after editing ${relativePath}:\n${formatInstructionFindings(result.errors)}\n`
        + 'Procedure: template-maintenance (.claude/skills/template-maintenance/SKILL.md).');
    }
  }
  return messages;
}

const isEntryPoint = process.argv[1] && import.meta.url.endsWith(process.argv[1].split(/[\\/]/).pop());
if (isEntryPoint) {
  const input = await readHookInput(HOOK);
  const filePath = input?.tool_input?.file_path;
  if (typeof filePath !== 'string') {
    fail(HOOK, `tool "${input?.tool_name ?? 'unknown'}" provided no tool_input.file_path`);
  }
  const root = resolveProjectRoot(HOOK, input);
  const relativePath = toProjectRelative(root, filePath);
  if (relativePath === null) {
    process.exit(0); // edited file is outside this project: nothing here applies to it
  }
  const messages = evaluate(root, relativePath);
  if (messages.length) {
    feedback(messages.join('\n\n'));
  }
  process.exit(0);
}
