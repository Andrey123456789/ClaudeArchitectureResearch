'use strict';
// Shared helpers for the instruction-system hooks and checks.
// Pure Node.js (no packages); works on Windows, macOS, and Linux.
//
// Two roots:
// - launcher root: the checkout that contains these scripts (located from this
//   file); it is used only to load the scripts;
// - active root: the repository or worktree being worked on, resolved from the
//   hook input `cwd` (hooks call useActiveRoot before any other helper) or from
//   the process working directory (manual runs). Every repository read, path
//   containment check, and Git call uses the active root; there is no silent
//   fallback to the launcher root.

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const LAUNCHER_ROOT = path.resolve(__dirname, '..', '..', '..');
const SKIP_DIRS = new Set(['node_modules', 'bin', 'obj', 'dist', 'coverage', 'TestResults']);
// Dot-directories (VCS data, IDE state, tool caches) are skipped except the instruction system itself.
const KEEP_DOT_DIRS = new Set(['.claude', '.github']);

let activeRoot = null;
// Git directory of the active root's repository or worktree, found with the root (null: none).
let activeGitDir = null;

function isDir(p) {
  try {
    return fs.statSync(p).isDirectory();
  } catch {
    return false;
  }
}

// Absolute path with symlinks, junctions, and short names resolved for its longest existing prefix.
function canonical(p) {
  const abs = path.resolve(p);
  const rest = [];
  let cur = abs;
  for (;;) {
    try {
      return path.join(fs.realpathSync.native(cur), ...rest);
    } catch {
      const parent = path.dirname(cur);
      if (parent === cur) return abs;
      rest.unshift(path.basename(cur));
      cur = parent;
    }
  }
}

function samePath(a, b) {
  return path.relative(a, b) === '';
}

// Git top-level and Git directory of dir (one Git call), or null outside a work tree.
function gitLocation(dir) {
  const r = spawnSync('git', ['rev-parse', '--show-toplevel', '--absolute-git-dir'], { cwd: dir, encoding: 'utf8', windowsHide: true });
  const [top, gitDir] = r.error || r.status !== 0 ? [] : r.stdout.trim().split(/\r?\n/);
  return top && gitDir ? { top: canonical(top), gitDir } : null;
}

function isInstructionRoot(dir) {
  return fs.existsSync(path.join(dir, 'CLAUDE.md')) && isDir(path.join(dir, '.claude'));
}

// The Git top-level of startDir when it holds the instruction system; otherwise the
// nearest enclosing directory (not above the Git top-level) that does.
function locateActiveRoot(startDir) {
  const start = canonical(startDir || process.cwd());
  if (!isDir(start)) throw new Error(`working directory does not exist: ${start}`);
  const repo = gitLocation(start);
  const top = repo && repo.top;
  const gitDir = repo ? repo.gitDir : null;
  if (top && isInstructionRoot(top)) return { root: top, gitDir };
  for (let dir = start; ; dir = path.dirname(dir)) {
    if (isInstructionRoot(dir)) return { root: dir, gitDir };
    if ((top && samePath(dir, top)) || path.dirname(dir) === dir) break;
  }
  throw new Error(`no project root (CLAUDE.md with .claude/) found for working directory ${start}`);
}

function resolveActiveRoot(startDir) {
  return locateActiveRoot(startDir).root;
}

function useActiveRoot(startDir) {
  ({ root: activeRoot, gitDir: activeGitDir } = locateActiveRoot(startDir));
  return activeRoot;
}

function root() {
  return activeRoot || useActiveRoot(process.cwd());
}

function projectRoot() {
  return root();
}

function git(args) {
  const r = spawnSync('git', args, { cwd: root(), encoding: 'utf8', windowsHide: true });
  if (r.error) throw new Error(`git is not available (${r.error.message})`);
  if (r.status !== 0) throw new Error(`git ${args[0]} failed: ${(r.stderr || '').trim()}`);
  return r.stdout;
}

function toPosix(p) {
  return p.split(path.sep).join('/');
}

function escapes(rel) {
  return rel === '..' || rel.startsWith(`..${path.sep}`) || path.isAbsolute(rel);
}

// Returns the root-relative POSIX path, or null when the path escapes the active root.
// A relative path is resolved against base (default: the active root).
function relativeInsideRoot(p, base) {
  if (!p) return null;
  const r = root();
  const rel = path.relative(r, canonical(path.resolve(base || r, String(p))));
  if (rel === '' || escapes(rel)) return null;
  return toPosix(rel);
}

function absPath(rel) {
  const r = root();
  const abs = path.resolve(r, rel);
  if (escapes(path.relative(r, abs))) {
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

// XML project files may also be UTF-16 with a byte-order mark (for example written by
// Windows PowerShell 5.1 redirection); MSBuild reads them, so the checks must too.
function readXml(rel) {
  const buf = fs.readFileSync(absPath(rel));
  if (buf[0] === 0xff && buf[1] === 0xfe) return buf.toString('utf16le', 2);
  if (buf[0] === 0xfe && buf[1] === 0xff) return Buffer.from(buf.subarray(2, buf.length - (buf.length % 2))).swap16().toString('utf16le');
  return readText(rel);
}

const XML_NAME = /[A-Za-z_:][\w.:-]*/y;
const XML_MARKUP = [['<!--', '-->'], ['<![CDATA[', ']]>'], ['<?', '?>'], ['<!', '>']];

// The start or end tag at xml[i] ('<'), or null when no tag starts there. Attribute values are
// single- or double-quoted; a start tag that cannot be read has attrs null, and reading resumes
// after its next '>'.
function readTag(xml, i) {
  const close = xml[i + 1] === '/';
  XML_NAME.lastIndex = i + (close ? 2 : 1);
  const name = (XML_NAME.exec(xml) || [])[0];
  if (!name) return null;
  const attrs = Object.create(null);
  const space = /\s*/y;
  let j = XML_NAME.lastIndex;
  const skip = () => {
    space.lastIndex = j;
    space.exec(xml);
    j = space.lastIndex;
  };
  for (;;) {
    skip();
    if (xml[j] === '>') return { name, close, selfClosing: false, attrs: close ? null : attrs, start: i, stop: j + 1 };
    if (!close && xml.startsWith('/>', j)) return { name, close, selfClosing: true, attrs, start: i, stop: j + 2 };
    XML_NAME.lastIndex = j;
    const attr = !close && XML_NAME.exec(xml);
    if (!attr) break;
    j = XML_NAME.lastIndex;
    skip();
    if (xml[j] !== '=') break;
    j++;
    skip();
    const quote = xml[j];
    const end = quote === '"' || quote === "'" ? xml.indexOf(quote, j + 1) : -1;
    if (end < 0) break;
    if (!(attr[0] in attrs)) attrs[attr[0]] = xml.slice(j + 1, end);
    j = end + 1;
  }
  const next = xml.indexOf('>', i + 1);
  return { name, close, selfClosing: false, attrs: null, start: i, stop: next < 0 ? xml.length : next + 1 };
}

// Live elements named `name` in project XML (for example PackageReference). Comments, CDATA
// sections, processing instructions, and declarations do not count, also when an attribute value
// contains their delimiters. Attributes may be in any order, single- or double-quoted, with line
// breaks inside the start tag. Each element is { attrs, inner, line, problem }: attrs maps names to
// values (null when the start tag cannot be read), inner is the content of a non-self-closing
// element, and problem says what could not be read reliably (the checks report it).
function xmlElements(xml, name) {
  const tags = [];
  let unterminated = -1;
  for (let i = xml.indexOf('<'); i >= 0; ) {
    const markup = XML_MARKUP.find(([open]) => xml.startsWith(open, i));
    let stop;
    if (markup) {
      const end = xml.indexOf(markup[1], i + markup[0].length);
      if (end < 0) {
        unterminated = i;
        break;
      }
      stop = end + markup[1].length;
    } else {
      const tag = readTag(xml, i);
      if (tag) tags.push(tag);
      stop = tag ? tag.stop : i + 1;
    }
    i = xml.indexOf('<', stop);
  }
  const lineAt = (index) => xml.slice(0, index).split('\n').length;
  const elements = [];
  tags.forEach((tag, k) => {
    if (tag.close || tag.name !== name) return;
    const element = { attrs: tag.attrs, inner: null, line: lineAt(tag.start), problem: tag.attrs ? null : 'malformed start tag' };
    if (tag.attrs && !tag.selfClosing) {
      for (let j = k + 1, depth = 1; j < tags.length && element.inner === null; j++) {
        if (tags[j].name !== name) continue;
        if (!tags[j].close) depth += tags[j].selfClosing ? 0 : 1;
        else if (--depth === 0) element.inner = xml.slice(tag.stop, tags[j].start);
      }
      if (element.inner === null) element.problem = 'missing end tag';
    }
    elements.push(element);
  });
  if (unterminated >= 0) {
    const hidden = new RegExp(`<${name}\\b`, 'g');
    hidden.lastIndex = unterminated;
    for (let m; (m = hidden.exec(xml)); ) {
      elements.push({ attrs: null, inner: null, line: lineAt(m.index), problem: 'inside an unterminated comment or declaration' });
    }
  }
  return elements;
}

// Nested repositories and worktrees (for example .claude/worktrees/<name>) are separate
// checkouts with their own state and are not walked.
function walk(dirRel) {
  const out = [];
  const r = root();
  const start = absPath(dirRel || '.');
  if (!fs.existsSync(start)) return out;
  const stack = [start];
  while (stack.length) {
    const dir = stack.pop();
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (entry.isDirectory()) {
        const sub = path.join(dir, entry.name);
        const skip =
          SKIP_DIRS.has(entry.name) ||
          (entry.name.startsWith('.') && !KEEP_DOT_DIRS.has(entry.name)) ||
          fs.existsSync(path.join(sub, '.git'));
        if (!skip) stack.push(sub);
      } else if (entry.isFile()) {
        out.push(toPosix(path.relative(r, path.join(dir, entry.name))));
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

// Hook input: one JSON object on stdin. A leading UTF-8 byte-order mark (for example
// from Windows PowerShell 5.1) and surrounding whitespace or line breaks are ignored;
// unreadable, empty, or non-object input is an error (each hook applies its failure policy).
function readStdinJson() {
  const text = fs.readFileSync(0, 'utf8').replace(/^\uFEFF/, '').trim();
  const input = JSON.parse(text);
  if (!input || typeof input !== 'object' || Array.isArray(input)) throw new Error('hook input is not a JSON object');
  return input;
}

// Root-relative paths that Git reports as changed or untracked in the active root,
// optionally limited to the given root-relative paths.
function changedFiles(paths = []) {
  const top = path.resolve(git(['rev-parse', '--show-toplevel']).trim());
  const pathspecs = paths.length ? ['--', ...paths.map((p) => `:(literal)${p}`)] : [];
  const status = git(['status', '--porcelain=v1', '-z', '--untracked-files=all', ...pathspecs]);
  const files = [];
  const parts = status.split('\0').filter(Boolean);
  for (let i = 0; i < parts.length; i++) {
    const code = parts[i].slice(0, 2);
    const file = parts[i].slice(3);
    if (code.includes('R') || code.includes('C')) i++;
    const rel = relativeInsideRoot(path.join(top, file));
    if (rel) files.push(rel);
  }
  return files.sort();
}

// Hook state file in the Git directory of the active repository or worktree (one per worktree).
function stateFile(name) {
  root();
  return path.join(activeGitDir || git(['rev-parse', '--absolute-git-dir']).trim(), name);
}

function formatFindings(findings) {
  return findings.map((f) => `${f.level}: ${f.file ? `${f.file}: ` : ''}${f.message}`).join('\n');
}

module.exports = {
  LAUNCHER_ROOT,
  resolveActiveRoot,
  useActiveRoot,
  root,
  projectRoot,
  git,
  toPosix,
  relativeInsideRoot,
  absPath,
  exists,
  isDirectory,
  readText,
  readXml,
  xmlElements,
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
  changedFiles,
  stateFile,
  formatFindings,
};
