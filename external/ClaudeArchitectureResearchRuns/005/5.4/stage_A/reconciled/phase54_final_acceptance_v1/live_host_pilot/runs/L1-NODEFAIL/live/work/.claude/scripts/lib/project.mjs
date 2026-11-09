// Shared helpers for instruction-system hooks and checks.
// Cross-platform (Node.js >= 18, ESM). No shell expansion: every path is resolved here.
//
// Two roots are kept apart:
// - launcher root: the instruction template these scripts were started from (script location);
// - active root: the project/worktree Claude is working in, resolved from the hook input `cwd` (or the
//   edited file) and Git. Repository state, manifests, architecture checks, and hook state always use the
//   active root; instruction configuration comes from the active root when it carries the template,
//   otherwise from the launcher root.
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const SKIP_DIRS = new Set(['node_modules', 'bin', 'obj', '.git', '.vs', 'dist', 'TestResults', 'coverage']);
const MARKER = path.join('.claude', 'rules', '3-project', 'decisions.md');

export class SetupError extends Error {}
export class InputError extends SetupError {}
export class EncodingError extends SetupError {}

export function toPosix(p) {
  return p.split(path.sep).join('/').replace(/\\/g, '/');
}

// The launcher root is three levels above this file: <root>/.claude/scripts/lib/project.mjs
export function resolveRoot() {
  const here = path.dirname(fileURLToPath(import.meta.url));
  const root = path.resolve(here, '..', '..', '..');
  if (!existsSync(path.join(root, MARKER))) {
    throw new SetupError(`Instruction template incomplete: expected ${toPosix(path.join(root, MARKER))}. Restore .claude/rules/3-project/decisions.md before relying on hooks or checks.`);
  }
  return root;
}

export function git(cwd, args) {
  const r = spawnSync('git', ['-C', cwd, ...args], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
  if (r.error || r.status !== 0) return null;
  return r.stdout;
}

export function gitToplevel(dir) {
  const out = git(dir, ['rev-parse', '--show-toplevel']);
  return out ? path.resolve(out.trim()) : null;
}

function findTemplateRoot(start, stop) {
  let dir = path.resolve(start);
  for (;;) {
    if (existsSync(path.join(dir, MARKER))) return dir;
    if (stop && path.resolve(dir) === path.resolve(stop)) return null;
    const parent = path.dirname(dir);
    if (parent === dir) return null;
    dir = parent;
  }
}

// Resolves { launcher, active, config, gitTop } from a working directory (hook input `cwd`).
export function resolveRoots(cwdInput) {
  const launcher = resolveRoot();
  let cwd = cwdInput ? path.resolve(cwdInput) : process.cwd();
  while (!existsSync(cwd) && path.dirname(cwd) !== cwd) cwd = path.dirname(cwd);
  const gitTop = gitToplevel(cwd);
  const templateRoot = findTemplateRoot(cwd, gitTop);
  const active = templateRoot || gitTop || cwd;
  return { launcher, active, config: templateRoot || launcher, gitTop, cwd };
}

export function hookStateDir(activeRoot) {
  return path.join(activeRoot, '.claude', '.hook-state');
}

// Repository-relative POSIX path, or null when the path escapes the root.
export function toRepoRelative(root, filePath) {
  if (!filePath) return null;
  const abs = path.resolve(root, filePath);
  const rel = path.relative(root, abs);
  if (rel === '' || rel.startsWith('..') || path.isAbsolute(rel)) return null;
  return toPosix(rel);
}

// ---------- Text decoding (UTF-8 with or without BOM, BOM-tagged UTF-16LE/BE) ----------

function strictUtf8(buf, label) {
  let text;
  try {
    text = new TextDecoder('utf-8', { fatal: true }).decode(buf);
  } catch {
    throw new EncodingError(`${label} cannot be decoded: not valid UTF-8 and no UTF-16 byte-order mark`);
  }
  if (text.includes('\u0000')) throw new EncodingError(`${label} cannot be decoded: contains NUL characters (UTF-16 without a byte-order mark?)`);
  return text;
}

export function decodeText(buf, label = 'content') {
  if (buf.length >= 3 && buf[0] === 0xef && buf[1] === 0xbb && buf[2] === 0xbf) return strictUtf8(buf.subarray(3), label);
  const le = buf.length >= 2 && buf[0] === 0xff && buf[1] === 0xfe;
  const be = buf.length >= 2 && buf[0] === 0xfe && buf[1] === 0xff;
  if (le || be) {
    const body = Buffer.from(buf.subarray(2));
    if (body.length % 2 !== 0) throw new EncodingError(`${label} cannot be decoded: UTF-16 content has an odd byte length`);
    if (be) for (let i = 0; i < body.length; i += 2) { const t = body[i]; body[i] = body[i + 1]; body[i + 1] = t; }
    return body.toString('utf16le');
  }
  return strictUtf8(buf, label);
}

export function readText(file, label) {
  return decodeText(readFileSync(file), label || toPosix(file));
}

// Hook input: JSON object on stdin (UTF-8, UTF-8 BOM, or BOM-tagged UTF-16). Empty or malformed input
// throws InputError; callers decide whether that blocks (critical PreToolUse) or only reports.
export async function readStdinJson() {
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  const buf = Buffer.concat(chunks);
  let raw;
  try {
    raw = decodeText(buf, 'Hook input').trim();
  } catch (error) {
    throw new InputError(error.message);
  }
  if (!raw) throw new InputError('Hook input is empty.');
  let value;
  try {
    value = JSON.parse(raw);
  } catch {
    throw new InputError('Hook input is not valid JSON.');
  }
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new InputError('Hook input is not a JSON object.');
  return value;
}

// Git blob id of file content (matches index ids, so clean and dirty snapshots compare directly).
export function blobId(buf) {
  return createHash('sha1').update(`blob ${buf.length}\0`).update(buf).digest('hex');
}

export function listFiles(dir, predicate = () => true) {
  const out = [];
  if (!existsSync(dir)) return out;
  for (const entry of readdirSync(dir)) {
    if (SKIP_DIRS.has(entry)) continue;
    const full = path.join(dir, entry);
    const stat = statSync(full);
    if (stat.isDirectory()) {
      if (existsSync(path.join(full, '.git'))) continue; // nested repository or linked worktree
      out.push(...listFiles(full, predicate));
    } else if (predicate(full)) out.push(full);
  }
  return out;
}

// Minimal glob support: '**' (any depth), '*' (within a segment), '?' (one char).
export function globToRegExp(glob) {
  let re = '';
  for (let i = 0; i < glob.length; i++) {
    const c = glob[i];
    if (c === '*') {
      if (glob[i + 1] === '*') {
        i++;
        if (glob[i + 1] === '/') { i++; re += '(?:.*/)?'; } else { re += '.*'; }
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

export function matchesAny(relPath, globs = []) {
  return globs.some((g) => globToRegExp(g).test(relPath));
}

// Capability selection record: the table under "## Capability selection" in decisions.md.
export function parseSelection(root) {
  const file = path.join(root, MARKER);
  const text = readText(file);
  const start = text.indexOf('## Capability selection');
  if (start < 0) throw new SetupError('decisions.md has no "## Capability selection" section.');
  const rows = [];
  for (const line of text.slice(start).split(/\r?\n/)) {
    const cells = line.split('|').map((c) => c.trim());
    if (cells.length < 5 || cells[1] === 'Slot' || /^-+$/.test(cells[1])) continue;
    if (!cells[1]) continue;
    const selected = cells[3].replace(/`/g, '');
    rows.push({ slot: cells[1], requirement: cells[2], selected: selected === 'none' ? null : selected });
  }
  return rows;
}

export function selectedImplementation(selection, slot) {
  const row = selection.find((r) => r.slot === slot);
  return row ? row.selected : null;
}

export function facetFile(root, selection, slot, facet, ext) {
  const impl = selectedImplementation(selection, slot);
  if (!impl) return null;
  return path.join(root, '.claude', 'capabilities', slot, impl, `${facet}.${ext}`);
}

// Loads a JSON facet of the selected implementation. A cleared optional slot returns null;
// a selected implementation without the facet is a setup error (fail clearly, never skip silently).
export function loadJsonFacet(root, selection, slot, facet) {
  const file = facetFile(root, selection, slot, facet, 'json');
  if (!file) return null;
  if (!existsSync(file)) {
    throw new SetupError(`Missing facet ${slot}.${facet}: ${toPosix(path.relative(root, file))}`);
  }
  return JSON.parse(readText(file));
}

// Lightweight MSBuild XML reading: comments are ignored; single- and double-quoted attributes are equivalent.
// MSBuild properties ($(...)) are not evaluated; callers report them instead of trusting them.
export function xmlAttr(tag, name) {
  const m = tag.match(new RegExp(`\\b${name}\\s*=\\s*(?:"([^"]*)"|'([^']*)')`, 'i'));
  return m ? (m[1] !== undefined ? m[1] : m[2]) : null;
}

export function xmlElements(text, name) {
  const clean = text.replace(/<!--[\s\S]*?-->/g, '');
  return [...clean.matchAll(new RegExp(`<${name}\\b((?:[^>"']|"[^"]*"|'[^']*')*?)(/>|>([\\s\\S]*?)</${name}\\s*>)`, 'gi'))]
    .map((m) => ({ attrs: m[1], inner: m[3] || '' }));
}

function childText(inner, name) {
  const m = inner.match(new RegExp(`<${name}>\\s*([^<]*?)\\s*</${name}>`, 'i'));
  return m ? m[1] : null;
}

export function parseCsproj(text) {
  const packages = xmlElements(text, 'PackageReference').map((e) => ({
    id: xmlAttr(e.attrs, 'Include') || xmlAttr(e.attrs, 'Update'),
    version: xmlAttr(e.attrs, 'Version') || childText(e.inner, 'Version'),
    versionOverride: xmlAttr(e.attrs, 'VersionOverride') || childText(e.inner, 'VersionOverride'),
  }));
  const projects = xmlElements(text, 'ProjectReference').map((e) => xmlAttr(e.attrs, 'Include')).filter(Boolean);
  const frameworks = xmlElements(text, 'FrameworkReference').map((e) => xmlAttr(e.attrs, 'Include')).filter(Boolean);
  // MSBuild SDKs the project uses: <Project Sdk="A;B/1.0">, <Sdk Name="A" />, <Import Sdk="A" ... />.
  // Version suffixes are dropped; literal values only (properties are not evaluated).
  const sdkList = (value) => String(value || '').split(';').map((s) => s.split('/')[0].trim()).filter(Boolean);
  const sdks = [
    ...xmlElements(text, 'Project').flatMap((e) => sdkList(xmlAttr(e.attrs, 'Sdk'))),
    ...xmlElements(text, 'Sdk').map((e) => xmlAttr(e.attrs, 'Name')).filter(Boolean),
    ...xmlElements(text, 'Import').flatMap((e) => sdkList(xmlAttr(e.attrs, 'Sdk'))),
  ];
  return { packages, projects, frameworks, sdks };
}

export function parsePackagesProps(text) {
  const clean = text.replace(/<!--[\s\S]*?-->/g, '');
  const versions = xmlElements(clean, 'PackageVersion').map((e) => ({
    id: xmlAttr(e.attrs, 'Include') || xmlAttr(e.attrs, 'Update'),
    version: xmlAttr(e.attrs, 'Version') || childText(e.inner, 'Version') || '',
  }));
  return { versions };
}

export function packageMatches(id, rules = []) {
  const lower = (id || '').toLowerCase();
  return rules.filter((r) => (r.id && r.id.toLowerCase() === lower) || (r.prefix && lower.startsWith(r.prefix.toLowerCase())));
}
