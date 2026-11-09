// Active repository root resolution shared by the hooks in .claude/hooks/ and
// the checker scripts in this directory. Requires Node.js 18+ and works the same
// on Windows, macOS, and Linux; Git is optional.
//
// Two roots are kept apart:
//   template root - the checkout these files are installed in, found from this
//                   file's location. It only locates the installed hooks and
//                   scripts (settings.json launches them through
//                   ${CLAUDE_PROJECT_DIR}).
//   active root   - the checkout or worktree being worked on, derived from a
//                   start directory: the hook input "cwd" (the edited file's
//                   directory for file events), or the shell's current directory
//                   for a manual run. Manifest, path, and Git-state checks
//                   always use the active root.
//
// Resolution from a start directory:
//   1. Inside a Git working tree of the same repository as the template root
//      (same common Git directory, which includes linked worktrees): that
//      working tree's top level, plus the template root's offset inside its own
//      working tree (normally none).
//   2. Otherwise, inside the template root (no Git, or a nested independent
//      repository such as a submodule): the template root.
//   3. Otherwise no root can be established: an Error explains why, so callers
//      report it instead of silently checking the wrong tree.

import { execFileSync } from 'node:child_process';
import { realpathSync, statSync } from 'node:fs';
import { dirname, isAbsolute, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

export const templateRoot = canonical(resolve(dirname(fileURLToPath(import.meta.url)), '..', '..'));

export function resolveActiveRoot(startDir) {
  return resolveActiveRepository(startDir).root;
}

// { root, top, gitDir }: the active root plus the top level and Git directory
// of the working tree that contains it (both null without Git).
export function resolveActiveRepository(startDir) {
  const start = canonical(startDir);
  if (!isDirectory(start)) throw new Error(`start directory "${start}" does not exist or is not a directory`);

  const startTree = gitWorkTree(start);
  if (startTree && startTree.top === templateRoot) return { root: templateRoot, ...startTree }; // same tree: no offset
  const templateTree = startTree ? gitWorkTree(templateRoot) : null;
  if (startTree && templateTree && sameRepository(startTree, templateTree)) {
    const offset = relative(templateTree.top, templateRoot);
    const root = canonical(resolve(startTree.top, offset));
    if (!isDirectory(root)) {
      throw new Error(`the working tree "${startTree.top}" has no "${offset}" directory for this project`);
    }
    return { root, ...startTree };
  }
  if (isInside(start, templateRoot)) {
    const tree = startTree ? templateTree : gitWorkTree(templateRoot);
    return { root: templateRoot, top: tree?.top ?? null, gitDir: tree?.gitDir ?? null };
  }

  const reason = startTree
    ? `it belongs to a different Git repository ("${startTree.top}")`
    : 'it is not inside a Git working tree of this repository';
  throw new Error(`cannot establish the active repository root from "${start}": ${reason}, ` +
    `and it is outside the project at "${templateRoot}"`);
}

// True when path equals base or lies below it (case-insensitive on Windows).
export function isInside(path, base) {
  const rel = relative(base, path);
  return rel === '' || (!rel.startsWith('..') && !isAbsolute(rel));
}

// Absolute path with symbolic links, junctions, and Windows short names resolved
// when the path exists; otherwise the plain absolute path.
export function canonical(path) {
  const absolute = resolve(path);
  try {
    return realpathSync.native(absolute);
  } catch {
    return absolute;
  }
}

function isDirectory(path) {
  try {
    return statSync(path).isDirectory();
  } catch {
    return false;
  }
}

// { top, gitDir } for the Git working tree containing dir, or null.
function gitWorkTree(dir) {
  const [top, gitDir] = (git(dir, ['rev-parse', '--show-toplevel', '--absolute-git-dir']) ?? '').split(/\r?\n/);
  return top && gitDir ? { top: canonical(top), gitDir: canonical(gitDir) } : null;
}

function sameRepository(a, b) {
  if (a.top === b.top) return true;
  const commonA = commonDir(a.top);
  const commonB = commonDir(b.top);
  return commonA !== null && commonA === commonB;
}

// Run from the working tree top so a relative answer is relative to that top.
function commonDir(top) {
  const common = git(top, ['rev-parse', '--git-common-dir']);
  return common ? canonical(resolve(top, common)) : null;
}

function git(cwd, args) {
  try {
    const output = execFileSync('git', args, {
      cwd,
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
      timeout: 15000,
      windowsHide: true,
    });
    return output.trim() || null;
  } catch {
    return null; // Git missing, not a working tree, or an unusable repository
  }
}
