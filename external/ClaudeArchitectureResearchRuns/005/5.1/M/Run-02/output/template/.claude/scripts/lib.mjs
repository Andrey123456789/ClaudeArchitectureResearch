// Owner: shared file-walking and reporting helpers for the check scripts and hooks | Scope: repo/meta | Loads: imported by .claude/scripts/*.mjs and .claude/hooks/hooks.mjs | Enforced: n/a (library)

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const SKIPPED_DIRS = new Set([
  '.git', 'node_modules', 'bin', 'obj', 'dist', '.angular', '.vs', '.idea',
  'TestResults', 'coverage', 'artifacts',
]);

/** Canonical absolute path (resolves symlinks and Windows short names when the path exists). */
function canonical(target) {
  try {
    return fs.realpathSync.native(target);
  } catch {
    return path.resolve(target);
  }
}

/** Project root: CLAUDE_PROJECT_DIR when set, otherwise two levels above this file. */
export function projectRoot() {
  if (process.env.CLAUDE_PROJECT_DIR) {
    return canonical(process.env.CLAUDE_PROJECT_DIR);
  }
  return canonical(path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..'));
}

/** Repository-relative path with forward slashes. */
export function rel(root, file) {
  const absolute = path.resolve(root, file);
  const resolved = fs.existsSync(absolute) ? canonical(absolute) : absolute;
  return path.relative(root, resolved).split(path.sep).join('/');
}

/** Recursively lists files under `dir` (skipping build/output folders) that satisfy `filter(relPath)`. */
export function walk(root, dir, filter = () => true) {
  const results = [];
  const start = path.resolve(root, dir);
  if (!fs.existsSync(start)) {
    return results;
  }
  const stack = [start];
  while (stack.length > 0) {
    const current = stack.pop();
    let entries;
    try {
      entries = fs.readdirSync(current, { withFileTypes: true });
    } catch {
      continue;
    }
    for (const entry of entries) {
      const full = path.join(current, entry.name);
      if (entry.isDirectory()) {
        if (!SKIPPED_DIRS.has(entry.name)) {
          stack.push(full);
        }
      } else if (entry.isFile()) {
        const relative = rel(root, full);
        if (filter(relative)) {
          results.push(relative);
        }
      }
    }
  }
  return results.sort();
}

export function readText(root, relative) {
  try {
    return fs.readFileSync(path.resolve(root, relative), 'utf8');
  } catch {
    return null;
  }
}

export function exists(root, relative) {
  return fs.existsSync(path.resolve(root, relative));
}

/** Creates a finding. level: 'error' | 'warning'. */
export function finding(level, file, message, owner) {
  return { level, file, message, owner };
}

export function formatFindings(findings) {
  return findings
    .map((f) => `${f.level.toUpperCase()} ${f.file}: ${f.message}${f.owner ? ` — see ${f.owner}` : ''}`)
    .join('\n');
}

/** Prints findings and sets the exit code (1 when any error exists) for CLI use. */
export function reportCli(title, findings) {
  if (findings.length === 0) {
    console.log(`${title}: no findings.`);
    return;
  }
  console.log(`${title}:\n${formatFindings(findings)}`);
  if (findings.some((f) => f.level === 'error')) {
    process.exitCode = 1;
  }
}

/** True when this module is the process entry point. */
export function isMain(importMetaUrl) {
  return process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(importMetaUrl);
}
