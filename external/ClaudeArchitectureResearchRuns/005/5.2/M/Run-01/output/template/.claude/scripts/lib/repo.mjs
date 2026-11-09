// Shared helpers for the instruction hooks and check scripts: project-root resolution,
// safe path handling, repository walking, glob matching, and report formatting.
// Cross-platform (Windows, macOS, Linux); Node.js built-ins only.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const SKIPPED_DIRS = new Set([
  '.git', 'node_modules', 'bin', 'obj', 'dist', '.angular', '.vs', '.idea',
  'TestResults', 'coverage', 'artifacts', 'publish',
]);

export class SetupError extends Error {}

function isProjectRoot(dir) {
  return fs.existsSync(path.join(dir, 'CLAUDE.md')) &&
    fs.existsSync(path.join(dir, '.claude', 'settings.json'));
}

// Resolves the project root from the calling module's location (…/.claude/<dir>/file.mjs),
// falling back to CLAUDE_PROJECT_DIR read from the environment. Throws a SetupError with
// an explicit message instead of guessing.
export function resolveProjectRoot(moduleUrl) {
  const tried = [];
  let dir = path.dirname(fileURLToPath(moduleUrl));
  for (;;) {
    tried.push(dir);
    if (isProjectRoot(dir)) return dir;
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  const fromEnv = process.env.CLAUDE_PROJECT_DIR;
  if (fromEnv) {
    const resolved = path.resolve(fromEnv);
    tried.push(resolved);
    if (isProjectRoot(resolved)) return resolved;
  }
  throw new SetupError(
    'Cannot locate the project root (a directory containing CLAUDE.md and .claude/settings.json). ' +
    `Searched: ${tried.join(', ')}`);
}

// Returns the repository-relative POSIX path of `p`, or null when `p` lies outside `root`.
export function toRepoPath(root, p) {
  if (!p || typeof p !== 'string') return null;
  const absolute = path.resolve(root, p);
  const relative = path.relative(root, absolute);
  if (relative === '' || relative.startsWith('..') || path.isAbsolute(relative)) return null;
  return relative.split(path.sep).join('/');
}

export function readText(root, repoPath) {
  const absolute = path.join(root, ...repoPath.split('/'));
  try {
    return fs.readFileSync(absolute, 'utf8');
  } catch {
    return null;
  }
}

export function exists(root, repoPath) {
  return fs.existsSync(path.join(root, ...repoPath.split('/')));
}

// Lists repository files (POSIX relative paths) below `start`, skipping build output,
// dependency folders, and VCS metadata.
export function walkFiles(root, start = '') {
  const results = [];
  const base = start ? path.join(root, ...start.split('/')) : root;
  if (!fs.existsSync(base)) return results;
  const stack = [base];
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
        if (!SKIPPED_DIRS.has(entry.name)) stack.push(full);
      } else if (entry.isFile()) {
        results.push(path.relative(root, full).split(path.sep).join('/'));
      }
    }
  }
  return results.sort();
}

// Converts a gitignore-style glob (as used by rule `paths`) into a RegExp.
// `**/` matches zero or more directories, `/**` at the end matches everything below,
// `*` matches within one path segment, `?` matches one character.
export function globToRegExp(glob) {
  let pattern = '';
  for (let i = 0; i < glob.length; i++) {
    const c = glob[i];
    if (c === '*') {
      if (glob[i + 1] === '*') {
        if (glob[i + 2] === '/') {
          pattern += '(?:.*/)?';
          i += 2;
        } else {
          pattern += '.*';
          i += 1;
        }
      } else {
        pattern += '[^/]*';
      }
    } else if (c === '?') {
      pattern += '[^/]';
    } else if ('\\^$+.()|{}[]'.includes(c)) {
      pattern += `\\${c}`;
    } else {
      pattern += c;
    }
  }
  return new RegExp(`^${pattern}$`);
}

export function matchesGlob(repoPath, glob) {
  return globToRegExp(glob).test(repoPath);
}

// Reads the whole of stdin (hook payload) and parses it as JSON.
export async function readStdinJson() {
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  const text = Buffer.concat(chunks).toString('utf8').trim();
  if (!text) return {};
  try {
    return JSON.parse(text);
  } catch (error) {
    throw new SetupError(`Hook input is not valid JSON: ${error.message}`);
  }
}

export function formatFindings(title, findings) {
  if (findings.length === 0) return '';
  const lines = [title];
  for (const f of findings) {
    const where = f.file ? `${f.file}: ` : '';
    lines.push(`- [${f.level}] ${where}${f.message}${f.owner ? ` -> ${f.owner}` : ''}`);
  }
  return lines.join('\n');
}

export function isMainModule(moduleUrl) {
  if (!process.argv[1]) return false;
  const normalize = (p) => {
    const resolved = path.resolve(p);
    return process.platform === 'win32' ? resolved.toLowerCase() : resolved;
  };
  return normalize(process.argv[1]) === normalize(fileURLToPath(moduleUrl));
}
