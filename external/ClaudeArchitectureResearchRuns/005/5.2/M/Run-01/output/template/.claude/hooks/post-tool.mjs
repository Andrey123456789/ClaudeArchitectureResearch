// PostToolUse hook for file edits (Write, Edit, MultiEdit) and shell tools (Bash, PowerShell).
// - Package/project manifest edited, or a dependency command ran -> runs the manifest check
//   and routes to the add-dependency workflow.
// - SPECIFICATION.md or CUSTOM_SETTINGS.md edited -> synchronization reminder.
// - Instruction files edited -> runs the instruction-structure check.
// Feedback goes to Claude through stderr with exit code 2; silence means nothing to report.
// Messages point to the owning rule or workflow; policy text lives there, not here.
// Registered in .claude/settings.json as: node .claude/hooks/post-tool.mjs

import path from 'node:path';
import { SetupError, formatFindings, readStdinJson, resolveProjectRoot, toRepoPath } from '../scripts/lib/repo.mjs';
import { checkManifests } from '../scripts/check-manifests.mjs';
import { checkInstructions } from '../scripts/check-instructions.mjs';
import { findDependencyCommands } from './commands.mjs';

const EDIT_TOOLS = new Set(['Write', 'Edit', 'MultiEdit']);
const SHELL_TOOLS = new Set(['Bash', 'PowerShell']);

function isManifest(repoPath) {
  const name = path.posix.basename(repoPath);
  return name.endsWith('.csproj') || name === 'Directory.Packages.props' ||
    name === 'Directory.Build.props' || name === 'package.json';
}

function isInstructionFile(repoPath) {
  return repoPath === 'CLAUDE.md' || repoPath === 'docs/technology-stack.md' ||
    (repoPath.startsWith('.claude/') && (repoPath.endsWith('.md') || repoPath === '.claude/settings.json'));
}

function manifestReport(root, heading) {
  const { findings } = checkManifests(root);
  const relevant = findings.filter((f) => f.level === 'violation' || f.level === 'warning');
  return relevant.length > 0 ? formatFindings(heading, relevant) : null;
}

async function main() {
  const root = resolveProjectRoot(import.meta.url);
  const input = await readStdinJson();
  const tool = input?.tool_name;
  const toolInput = input?.tool_input ?? {};
  const messages = [];

  if (EDIT_TOOLS.has(tool)) {
    const repoPath = toRepoPath(root, toolInput.file_path);
    if (!repoPath) return;
    if (isManifest(repoPath)) {
      const report = manifestReport(root, `Manifest check after editing ${repoPath}:`);
      if (report) messages.push(`${report}\nDependency changes follow .claude/skills/add-dependency/SKILL.md.`);
    }
    if (repoPath === 'SPECIFICATION.md' || repoPath === 'CUSTOM_SETTINGS.md') {
      messages.push(
        `${repoPath} changed. Keep the product sources consistent and synchronized: CLAUDE.md (Product Sources); ` +
        'settings propagation: .claude/skills/custom-settings/SKILL.md; approved behavior changes: ' +
        '.claude/skills/development-workflow/SKILL.md (Approved product rules).');
    }
    if (isInstructionFile(repoPath)) {
      const { findings } = checkInstructions(root);
      const violations = findings.filter((f) => f.level === 'violation');
      if (violations.length > 0) {
        messages.push(`${formatFindings(`Instruction-structure check after editing ${repoPath}:`, violations)}\n` +
          'Structure owner: .claude/skills/template-maintenance/SKILL.md; map: .claude/MAP.md.');
      }
    }
  } else if (SHELL_TOOLS.has(tool)) {
    const commands = findDependencyCommands(toolInput.command);
    if (commands.length > 0) {
      const list = commands.map((c) => `\`${c.command}\``).join(', ');
      const report = manifestReport(root, 'Manifest check:');
      messages.push(
        `Dependency or project-reference change detected: ${list}. It is governed by ` +
        '.claude/skills/add-dependency/SKILL.md (package changes) and .claude/rules/architecture.md ' +
        '(project references); follow them if not already done.' + (report ? `\n${report}` : '\nManifest check: no findings.'));
    }
  }

  if (messages.length > 0) {
    process.stderr.write(`${messages.join('\n\n')}\n`);
    process.exit(2);
  }
}

main().catch((error) => {
  const message = error instanceof SetupError ? error.message : (error?.stack ?? String(error));
  process.stderr.write(`post-tool hook failed; manifest, product-input, and instruction checks were NOT run: ${message}\n`);
  process.exit(1);
});
