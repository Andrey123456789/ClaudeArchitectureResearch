// Kind: ENF | Scope: repo/meta | Owner: shared repository helpers — active repository/worktree root, Git calls, text decoding, content hashes | Loading: required by .claude/hooks/hook.cjs and the checkers in .claude/scripts/
//
// The active root is the repository or linked worktree being worked on. It is resolved from a starting
// directory (hook input `cwd`, an edited file, or the current directory of a manual run) through Git, never
// from the location of the launched script.
'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { spawnSync } = require('child_process');

function git(cwd, args) {
  const result = spawnSync('git', args, { cwd, encoding: 'utf8', windowsHide: true, maxBuffer: 64 * 1024 * 1024 });
  return { ok: !result.error && result.status === 0, stdout: result.stdout || '', stderr: (result.stderr || '').trim() };
}

function realpathLoose(target) {
  const absolute = path.resolve(String(target));
  try {
    return fs.realpathSync.native(absolute);
  } catch {
    const parent = path.dirname(absolute);
    return parent === absolute ? absolute : path.join(realpathLoose(parent), path.basename(absolute));
  }
}

function nearestDirectory(start) {
  let current = path.resolve(String(start));
  for (;;) {
    try {
      return fs.statSync(current).isDirectory() ? current : path.dirname(current);
    } catch {
      const parent = path.dirname(current);
      if (parent === current) return null;
      current = parent;
    }
  }
}

// Git work tree containing `start` (a linked worktree resolves to itself); otherwise the nearest ancestor that
// holds this instruction system (CLAUDE.md and .claude/); otherwise the starting directory itself.
function resolveRoot(start) {
  const dir = nearestDirectory(start || process.cwd());
  if (!dir) return null;
  const top = git(dir, ['rev-parse', '--show-toplevel']);
  if (top.ok && top.stdout.trim()) return { root: realpathLoose(top.stdout.trim()), git: true };
  for (let current = dir; ;) {
    if (fs.existsSync(path.join(current, 'CLAUDE.md')) && fs.existsSync(path.join(current, '.claude'))) {
      return { root: realpathLoose(current), git: false };
    }
    const parent = path.dirname(current);
    if (parent === current) break;
    current = parent;
  }
  return { root: realpathLoose(dir), git: false };
}

// Repository-relative path with forward slashes, or null when the file lies outside the root.
function toRelative(root, file) {
  const relative = path.relative(root, realpathLoose(path.resolve(root, String(file))));
  if (!relative || relative.startsWith('..') || path.isAbsolute(relative)) return null;
  return relative.split(path.sep).join('/');
}

function utf8(bytes) {
  try {
    return { text: new TextDecoder('utf-8', { fatal: true }).decode(bytes) };
  } catch {
    return { error: 'is not valid UTF-8' };
  }
}

function utf16(bytes, order) {
  if (bytes.length % 2 !== 0) return { error: `is truncated UTF-16${order} (odd byte length)` };
  const littleEndian = order === 'LE' ? bytes : Buffer.from(bytes).swap16();
  try {
    return { text: new TextDecoder('utf-16le', { fatal: true }).decode(littleEndian) };
  } catch {
    return { error: `is not valid UTF-16${order}` };
  }
}

// UTF-8 with or without a byte-order mark, and BOM-tagged UTF-16LE/BE (as written by Windows PowerShell 5.1).
// Returns { text } or { error } — never throws on malformed content.
function decodeText(buffer) {
  const bytes = Buffer.isBuffer(buffer) ? buffer : Buffer.from(String(buffer));
  if (bytes[0] === 0xef && bytes[1] === 0xbb && bytes[2] === 0xbf) return utf8(bytes.subarray(3));
  if (bytes[0] === 0xff && bytes[1] === 0xfe) return utf16(bytes.subarray(2), 'LE');
  if (bytes[0] === 0xfe && bytes[1] === 0xff) return utf16(bytes.subarray(2), 'BE');
  if (bytes.includes(0)) return { error: 'contains NUL bytes (binary, or UTF-16 without a byte-order mark)' };
  return utf8(bytes);
}

function readText(file) {
  let bytes;
  try {
    bytes = fs.readFileSync(file);
  } catch (error) {
    return { error: `cannot be read (${error.code || error.message})` };
  }
  return decodeText(bytes);
}

// Content identity of a file: SHA-1 of its bytes, or null when it does not exist as a file.
function hashFile(file) {
  try {
    return crypto.createHash('sha1').update(fs.readFileSync(file)).digest('hex');
  } catch {
    return null;
  }
}

function hashText(text) {
  return crypto.createHash('sha1').update(String(text)).digest('hex');
}

module.exports = { git, resolveRoot, toRelative, realpathLoose, decodeText, readText, hashFile, hashText };
