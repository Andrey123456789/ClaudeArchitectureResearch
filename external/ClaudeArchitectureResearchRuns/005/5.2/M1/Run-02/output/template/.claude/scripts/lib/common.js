'use strict';
// Shared helpers for the instruction-system hooks and checks.
// Pure Node.js (no packages); paths are resolved from this file's location so
// the scripts work from any working directory on Windows, macOS, and Linux.

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..', '..');
const SKIP_DIRS = new Set(['node_modules', 'bin', 'obj', 'dist', 'coverage', 'TestResults']);
// Dot-directories (VCS data, IDE state, tool caches) are skipped except the instruction system itself.
const KEEP_DOT_DIRS = new Set(['.claude', '.github']);

function projectRoot() {
  if (!fs.existsSync(path.join(ROOT, 'CLAUDE.md'))) {
    throw new Error(`project root not found: expected CLAUDE.md in ${ROOT}`);
  }
  return ROOT;
}

function toPosix(p) {
  return p.split(path.sep).join('/');
}

// Returns the root-relative POSIX path, or null when the path escapes the project root.
function relativeInsideRoot(p) {
  if (!p) return null;
  const abs = path.resolve(ROOT, String(p));
  const rel = path.relative(ROOT, abs);
  if (rel === '' || rel.startsWith('..') || path.isAbsolute(rel)) return null;
  return toPosix(rel);
}

function absPath(rel) {
  const abs = path.resolve(ROOT, rel);
  const back = path.relative(ROOT, abs);
  if (back.startsWith('..') || path.isAbsolute(back)) {
    throw new Error(`path escapes the project root: ${rel}`);
  }
  return abs;
}

function exists(rel) {
  try {
    return fs.existsSync(absPath(rel));
  } catch {
    return false;
  }
}

function isDirectory(rel) {
  try {
    return fs.statSync(absPath(rel)).isDirectory();
  } catch {
    return false;
  }
}

function readText(rel) {
  const text = fs.readFileSync(absPath(rel), 'utf8');
  return text.charCodeAt(0) === 0xfeff ? text.slice(1) : text;
}

function walk(dirRel) {
  const out = [];
  const start = absPath(dirRel || '.');
  if (!fs.existsSync(start)) return out;
  const stack = [start];
  while (stack.length) {
    const dir = stack.pop();
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (entry.isDirectory()) {
        const skip = SKIP_DIRS.has(entry.name) || (entry.name.startsWith('.') && !KEEP_DOT_DIRS.has(entry.name));
        if (!skip) stack.push(path.join(dir, entry.name));
      } else if (entry.isFile()) {
        out.push(toPosix(path.relative(ROOT, path.join(dir, entry.name))));
      }
    }
  }
  return out.sort();
}

function globToRegExp(glob) {
  let re = '';
  for (let i = 0; i < glob.length; i++) {
    const c = glob[i];
    if (c === '*') {
      if (glob[i + 1] === '*') {
        if (glob[i + 2] === '/') {
          re += '(?:.*/)?';
          i += 2;
        } else {
          re += '.*';
          i += 1;
        }
      } else {
        re += '[^/]*';
      }
    } else if (c === '?') {
      re += '[^/]';
    } else {
      re += c.replace(/[.+^${}()|[\]\\]/g, '\\$&');
    }
  }
  return new RegExp(`^${re}$`);
}

function matchesAny(rel, globs) {
  return (globs || []).some((g) => globToRegExp(g).test(rel));
}

// Minimal front-matter reader: scalar keys, folded/literal blocks, and string lists.
function parseFrontMatter(text) {
  const result = { data: {}, body: text, hasFrontMatter: false };
  if (!text.startsWith('---')) return result;
  const end = text.indexOf('\n---', 3);
  if (end < 0) return result;
  const lines = text.slice(3, end).split(/\r?\n/);
  result.body = text.slice(text.indexOf('\n', end + 1) + 1);
  result.hasFrontMatter = true;
  let key = null;
  for (const line of lines) {
    const keyMatch = /^([A-Za-z][\w-]*):\s*(.*)$/.exec(line);
    if (keyMatch) {
      key = keyMatch[1];
      const value = keyMatch[2].trim();
      result.data[key] = value === '' || value === '>' || value === '|' ? (value === '' ? [] : '') : value;
      continue;
    }
    const itemMatch = /^\s+-\s+(.*)$/.exec(line);
    if (key && itemMatch) {
      if (!Array.isArray(result.data[key])) result.data[key] = [];
      result.data[key].push(itemMatch[1].trim().replace(/^["']|["']$/g, ''));
      continue;
    }
    if (key && /^\s+\S/.test(line) && typeof result.data[key] === 'string') {
      result.data[key] = `${result.data[key]} ${line.trim()}`.trim();
    }
  }
  return result;
}

function firstContentLine(text) {
  const { body } = parseFrontMatter(text);
  for (const line of body.split(/\r?\n/)) {
    if (line.trim() !== '') return line;
  }
  return '';
}

function extractJsonBlock(text) {
  const match = /```json\s*\r?\n([\s\S]*?)\r?\n```/.exec(text);
  if (!match) return null;
  return JSON.parse(match[1]);
}

function headings(text) {
  return text
    .split(/\r?\n/)
    .filter((l) => /^#{1,6}\s/.test(l))
    .map((l) => l.replace(/^#{1,6}\s+/, '').trim());
}

function normalizeHeading(h) {
  return h.replace(/`/g, '').replace(/^\d+\.\s*/, '').replace(/^Step \d+:\s*/i, '').trim().toLowerCase();
}

function slugify(h) {
  return h
    .toLowerCase()
    .replace(/`/g, '')
    .replace(/[^\w\s-]/g, '')
    .trim()
    .replace(/\s/g, '-');
}

function capabilityOf(text) {
  const match = /Capability:\s*([a-z][a-z-]*)\/([a-z][a-z0-9-]*)/.exec(firstContentLine(text));
  return match ? { slot: match[1], implementation: match[2] } : null;
}

const SELECTION_FILE = 'docs/capability-selection.md';

function readSelection() {
  const rows = [];
  const text = readText(SELECTION_FILE);
  for (const line of text.split(/\r?\n/)) {
    if (!line.startsWith('|')) continue;
    const cells = line.split('|').slice(1, -1).map((c) => c.trim());
    if (cells.length < 5 || cells[0] === 'Slot' || /^-+$/.test(cells[0].replace(/[:\s]/g, ''))) continue;
    rows.push({
      slot: cells[0],
      slotType: cells[1],
      status: cells[2],
      implementation: cells[3],
      properties: cells[4],
    });
  }
  return rows;
}

function selectedImplementation(row) {
  if (!row || row.status !== 'selected') return null;
  const impl = row.implementation;
  return impl && impl !== '—' && impl !== '-' ? impl : null;
}

// Loads the manifests of the selected implementations; throws with a clear message on failure.
function loadSelectedModules() {
  const modules = [];
  for (const row of readSelection()) {
    const impl = selectedImplementation(row);
    if (!impl) continue;
    const file = `.claude/capabilities/${row.slot}/${impl}/MODULE.md`;
    if (!exists(file)) throw new Error(`selected implementation has no manifest: ${file}`);
    const manifest = extractJsonBlock(readText(file));
    if (!manifest) throw new Error(`manifest JSON block missing in ${file}`);
    modules.push({ slot: row.slot, implementation: impl, file, manifest, row });
  }
  return modules;
}

function moduleFor(modules, slot) {
  return modules.find((m) => m.slot === slot) || null;
}

function readStdinJson() {
  let raw = '';
  try {
    raw = fs.readFileSync(0, 'utf8');
  } catch {
    raw = '';
  }
  return raw.trim() ? JSON.parse(raw) : {};
}

function formatFindings(findings) {
  return findings.map((f) => `${f.level}: ${f.file ? `${f.file}: ` : ''}${f.message}`).join('\n');
}

module.exports = {
  ROOT,
  projectRoot,
  toPosix,
  relativeInsideRoot,
  absPath,
  exists,
  isDirectory,
  readText,
  walk,
  globToRegExp,
  matchesAny,
  parseFrontMatter,
  firstContentLine,
  extractJsonBlock,
  headings,
  normalizeHeading,
  slugify,
  capabilityOf,
  SELECTION_FILE,
  readSelection,
  selectedImplementation,
  loadSelectedModules,
  moduleFor,
  readStdinJson,
  formatFindings,
};
