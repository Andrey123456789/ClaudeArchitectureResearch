// Kind: ENF | Scope: repo/meta | Capability: — | Loading: shared helpers for .claude/scripts and .claude/hooks
// Conforms: —
'use strict';

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const IGNORED_DIRS = new Set(['.git', 'node_modules', 'bin', 'obj', 'dist', '.vs', 'TestResults', 'coverage']);

function toPosix(p) {
  return p.split(path.sep).join('/');
}

/** Launcher root: two levels above .claude/scripts or .claude/hooks (locates the implementation only). */
function rootFrom(dirname, levels) {
  const root = path.resolve(dirname, ...Array(levels).fill('..'));
  if (!fs.existsSync(path.join(root, '.claude'))) {
    throw new Error(`Cannot locate the project root from ${dirname}: expected a .claude directory at ${root}`);
  }
  return root;
}

function realpath(p) {
  try {
    return fs.realpathSync.native(p);
  } catch {
    return path.resolve(p);
  }
}

/** Read-only Git call; returns null when Git cannot be started. */
function git(cwd, args, options = {}) {
  const result = spawnSync('git', args, { cwd, encoding: options.encoding || 'utf8', windowsHide: true, maxBuffer: 64 * 1024 * 1024, input: options.input });
  if (result.error) return null;
  return result;
}

function isProjectRoot(dir) {
  return fs.existsSync(path.join(dir, '.claude')) && fs.existsSync(path.join(dir, 'CLAUDE.md'));
}

function nearestExisting(dir) {
  let d = path.resolve(dir);
  while (!fs.existsSync(d)) {
    const parent = path.dirname(d);
    if (parent === d) return d;
    d = parent;
  }
  return d;
}

function gitCommonDir(dir) {
  const r = git(dir, ['rev-parse', '--git-common-dir']);
  return r && r.status === 0 && r.stdout.trim() ? realpath(path.resolve(dir, r.stdout.trim())) : null;
}

/**
 * Active repository/worktree root for a working directory (hook input `cwd`, or process.cwd() for commands):
 * the Git top level containing it (a linked worktree resolves to that worktree, also when it sits inside the
 * main checkout); a nested independent repository resolves to the enclosing project (nearest ancestor with
 * CLAUDE.md and .claude); outside Git, that project root or the directory itself.
 */
function activeRoot(cwd) {
  const start = realpath(nearestExisting(cwd || process.cwd()));
  const top = git(start, ['rev-parse', '--show-toplevel']);
  const gitTop = top && top.status === 0 && top.stdout.trim() ? realpath(top.stdout.trim()) : null;
  if (gitTop && fs.existsSync(path.join(gitTop, '.claude'))) return gitTop;
  let project = null;
  for (let d = start; ; d = path.dirname(d)) {
    if (isProjectRoot(d)) {
      project = d;
      break;
    }
    if (path.dirname(d) === d) break;
  }
  if (gitTop && project && gitCommonDir(gitTop) === gitCommonDir(project)) return gitTop; // worktree of the same repository
  return project || gitTop || start;
}

/** Root inspected by a command-line checker: the repository containing the current directory, else the script's own. */
function commandRoot(scriptDir) {
  const root = activeRoot(process.cwd());
  return fs.existsSync(path.join(root, '.claude')) ? root : rootFrom(scriptDir, 2);
}

/** Resolve a path relative to root; returns null when it escapes the root. */
function relInside(root, filePath) {
  const resolved = path.resolve(root, filePath);
  const abs = fs.existsSync(resolved) ? realpath(resolved) : path.join(realpath(path.dirname(resolved)), path.basename(resolved));
  const rel = path.relative(realpath(root), abs);
  if (rel === '' || rel.startsWith('..') || path.isAbsolute(rel)) return null;
  return toPosix(rel);
}

function exists(root, rel) {
  return fs.existsSync(path.join(root, rel));
}

/**
 * Decode a text file: UTF-8 (BOM optional) and BOM-tagged UTF-16LE/BE. Throws for undecodable input
 * (NUL bytes without a BOM) so that enforcement fails visibly instead of silently skipping the file.
 */
function decodeText(buffer, label = 'file') {
  if (buffer.length >= 2 && buffer[0] === 0xff && buffer[1] === 0xfe) return buffer.slice(2).toString('utf16le');
  if (buffer.length >= 2 && buffer[0] === 0xfe && buffer[1] === 0xff) {
    const swapped = Buffer.from(buffer.slice(2));
    for (let i = 0; i + 1 < swapped.length; i += 2) [swapped[i], swapped[i + 1]] = [swapped[i + 1], swapped[i]];
    return swapped.toString('utf16le');
  }
  const start = buffer.length >= 3 && buffer[0] === 0xef && buffer[1] === 0xbb && buffer[2] === 0xbf ? 3 : 0;
  const body = buffer.slice(start);
  if (body.includes(0)) throw new Error(`${label}: unsupported text encoding (NUL bytes without a UTF-16 byte-order mark)`);
  return body.toString('utf8');
}

function readText(root, rel) {
  return decodeText(fs.readFileSync(path.join(root, rel)), rel);
}

/** Files below root/startRel, skipping build/tool directories and nested Git roots (other repositories or worktrees). */
function walk(root, startRel = '', filter = () => true) {
  const out = [];
  const start = path.join(root, startRel);
  if (!fs.existsSync(start)) return out;
  const stack = [start];
  while (stack.length) {
    const dir = stack.pop();
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const abs = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        if (!IGNORED_DIRS.has(entry.name) && !fs.existsSync(path.join(abs, '.git'))) stack.push(abs);
      } else {
        const rel = toPosix(path.relative(root, abs));
        if (filter(rel)) out.push(rel);
      }
    }
  }
  return out.sort();
}

/**
 * Minimal element reader for MSBuild files (no external XML dependency): every `<tag>` start tag with its
 * attributes, plus the simple `<Name>value</Name>` children of a paired element. Attribute values may use single
 * or double quotes, in any order and spacing; a quoted `>` does not end the tag. A malformed start tag throws so
 * that enforcement fails visibly instead of silently skipping the element.
 */
function xmlElements(text, tag) {
  const results = [];
  const startRe = new RegExp(`<${tag}(?=[\\s/>])`, 'g');
  const endRe = new RegExp(`</${tag}\\s*>`, 'g');
  const attrRe = /\s*(?:(\/?>)|([^\s=/>"'<]+)\s*=\s*(?:"([^"]*)"|'([^']*)'))/y;
  let m;
  while ((m = startRe.exec(text)) !== null) {
    const attrs = {};
    let close = null;
    attrRe.lastIndex = startRe.lastIndex;
    while (close === null) {
      const a = attrRe.exec(text);
      if (!a) throw new Error(`malformed <${tag}> start tag (attribute values must be quoted): ${text.slice(m.index, m.index + 80).split(/\r?\n/)[0]}`);
      if (a[1]) close = a[1];
      else attrs[a[2]] = a[3] !== undefined ? a[3] : a[4];
    }
    startRe.lastIndex = attrRe.lastIndex;
    let body = '';
    if (close === '>') {
      endRe.lastIndex = attrRe.lastIndex;
      const end = endRe.exec(text);
      if (end) body = text.slice(attrRe.lastIndex, end.index);
    }
    const child = {};
    const childRe = /<([A-Za-z_][\w.-]*)>([^<]*)<\/\1>/g;
    let c;
    while ((c = childRe.exec(body)) !== null) child[c[1]] = c[2].trim();
    results.push({ attrs, child });
  }
  return results;
}

function stripXmlComments(text) {
  return text.replace(/<!--[\s\S]*?-->/g, '');
}

function finding(severity, file, message, owner) {
  return { severity, file, message, owner };
}

function formatFindings(findings) {
  return findings
    .map(f => `[${f.severity}] ${f.file}: ${f.message}${f.owner ? ` -> ${f.owner}` : ''}`)
    .join('\n');
}

module.exports = {
  IGNORED_DIRS,
  toPosix,
  rootFrom,
  realpath,
  git,
  activeRoot,
  commandRoot,
  relInside,
  exists,
  decodeText,
  readText,
  walk,
  xmlElements,
  stripXmlComments,
  finding,
  formatFindings,
};
