// Shared helpers for instruction-system hooks and checks.
// Cross-platform (Node.js >= 18, ESM). No shell expansion: every path is resolved here.
//
// Two roots are kept apart:
// - launcher root: the instruction template that contains these scripts (located from this file);
// - active root: the project Claude is operating in, resolved from the hook input `cwd` (or the
//   process cwd for manual runs) through Git — a linked worktree or nested directory resolves to its
//   own checkout. Repository state, manifests, and per-worktree hook state always use the active root.
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, readdirSync, renameSync, statSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const MARKER = path.join('.claude', 'rules', '3-project', 'decisions.md');
const SKIP_DIRS = new Set(['node_modules', 'bin', 'obj', 'dist', 'TestResults', 'coverage', 'out', 'artifacts']);

export class SetupError extends Error {}
export class EncodingError extends Error {}

export function toPosix(p) {
  return p.split(path.sep).join('/').replace(/\\/g, '/');
}

export const samePath = (a, b) => (process.platform === 'win32'
  ? path.resolve(a).toLowerCase() === path.resolve(b).toLowerCase()
  : path.resolve(a) === path.resolve(b));

// Repository-relative POSIX path, or null when the path escapes the root.
export function toRepoRelative(root, filePath) {
  if (!filePath || !root) return null;
  const abs = path.resolve(root, filePath);
  const rel = path.relative(root, abs);
  if (rel === '' || rel.startsWith('..') || path.isAbsolute(rel)) return null;
  return toPosix(rel);
}

// Decodes text produced by the supported Windows/Unix tooling: UTF-8 (with or without BOM) and
// BOM-tagged UTF-16LE/UTF-16BE. Anything else fails deterministically with EncodingError.
export function decodeText(buffer, label = 'input') {
  const buf = Buffer.isBuffer(buffer) ? buffer : Buffer.from(buffer);
  const utf16 = (bytes, littleEndian) => {
    if (bytes.length % 2 !== 0) throw new EncodingError(`${label}: malformed UTF-16${littleEndian ? 'LE' : 'BE'} content (odd byte length)`);
    const le = littleEndian ? bytes : Buffer.from(bytes).swap16();
    try { return new TextDecoder('utf-16le', { fatal: true }).decode(le); } catch {
      throw new EncodingError(`${label}: malformed UTF-16${littleEndian ? 'LE' : 'BE'} content`);
    }
  };
  if (buf.length >= 2 && buf[0] === 0xff && buf[1] === 0xfe) return utf16(buf.subarray(2), true);
  if (buf.length >= 2 && buf[0] === 0xfe && buf[1] === 0xff) return utf16(buf.subarray(2), false);
  const body = buf.length >= 3 && buf[0] === 0xef && buf[1] === 0xbb && buf[2] === 0xbf ? buf.subarray(3) : buf;
  if (body.includes(0)) throw new EncodingError(`${label}: contains NUL bytes (UTF-16 without a byte-order mark is not supported; save as UTF-8)`);
  try { return new TextDecoder('utf-8', { fatal: true }).decode(body); } catch {
    throw new EncodingError(`${label}: not valid UTF-8 (save as UTF-8, or UTF-16 with a byte-order mark)`);
  }
}

export function readText(file) {
  return decodeText(readFileSync(file), toPosix(file));
}

export function readJson(file) {
  try { return JSON.parse(readText(file)); } catch (error) {
    if (error instanceof EncodingError) throw new SetupError(error.message);
    throw new SetupError(`${toPosix(file)}: invalid JSON (${error.message})`);
  }
}

// Reads hook input from stdin. Never throws: returns { ok, value } or { ok: false, error }.
export async function readHookInput() {
  const chunks = [];
  try {
    for await (const chunk of process.stdin) chunks.push(chunk);
  } catch (error) {
    return { ok: false, error: `hook input could not be read (${error.message})` };
  }
  let text;
  try { text = decodeText(Buffer.concat(chunks), 'hook input').trim(); } catch (error) {
    return { ok: false, error: error.message };
  }
  if (!text) return { ok: false, error: 'hook input is empty' };
  try {
    const value = JSON.parse(text);
    if (!value || typeof value !== 'object' || Array.isArray(value)) return { ok: false, error: 'hook input is not a JSON object' };
    return { ok: true, value };
  } catch {
    return { ok: false, error: 'hook input is not valid JSON' };
  }
}

export function listFiles(dir, predicate = () => true) {
  const out = [];
  if (!existsSync(dir)) return out;
  for (const entry of readdirSync(dir)) {
    if (SKIP_DIRS.has(entry) || entry.startsWith('.')) continue;
    const full = path.join(dir, entry);
    const stat = statSync(full);
    if (stat.isDirectory()) out.push(...listFiles(full, predicate));
    else if (predicate(full)) out.push(full);
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

export function sha256(data) {
  return createHash('sha256').update(data).digest('hex');
}

// Runs git without a shell. Paths are printed verbatim (core.quotepath=off).
export function git(cwd, args) {
  const result = spawnSync('git', ['-c', 'core.quotepath=off', ...args], { cwd, encoding: 'buffer', windowsHide: true, maxBuffer: 64 * 1024 * 1024 });
  if (result.error || result.status !== 0) {
    return { ok: false, stdout: '', stderr: result.error ? result.error.message : decodeLoose(result.stderr) };
  }
  return { ok: true, stdout: decodeLoose(result.stdout) };
}

function decodeLoose(buf) {
  return buf ? Buffer.from(buf).toString('utf8') : '';
}

// The template that contains this script: <root>/.claude/scripts/lib/project.mjs.
export function resolveLauncherRoot() {
  const here = path.dirname(fileURLToPath(import.meta.url));
  const root = path.resolve(here, '..', '..', '..');
  return { root, valid: existsSync(path.join(root, MARKER)) };
}

// Active project root for a directory: the nearest ancestor (inclusive) that contains the instruction
// marker, bounded by the Git top-level; without a marker, the Git top-level itself. Returns null when
// the directory belongs to neither a Git working tree nor an instruction template.
export function resolveActiveRoot(startDir) {
  if (!startDir || !existsSync(startDir)) return null;
  let dir = path.resolve(startDir);
  if (!statSync(dir).isDirectory()) dir = path.dirname(dir);
  const top = git(dir, ['rev-parse', '--show-toplevel']);
  const gitTop = top.ok && top.stdout.trim() ? path.resolve(top.stdout.trim()) : null;
  let root = null;
  for (let cur = dir; ; cur = path.dirname(cur)) {
    if (existsSync(path.join(cur, MARKER))) { root = cur; break; }
    if ((gitTop && samePath(cur, gitTop)) || path.dirname(cur) === cur) break;
  }
  if (!root && !gitTop) return null;
  const activeRoot = root || gitTop;
  let gitDir = null;
  if (gitTop) {
    const g = git(activeRoot, ['rev-parse', '--absolute-git-dir']);
    if (g.ok && g.stdout.trim()) gitDir = path.resolve(g.stdout.trim());
  }
  return { root: activeRoot, gitTop, gitDir, hasInstructions: Boolean(root) };
}

// Hook/check context. Policy data (selection record, facets) comes from the active root when it
// carries the instruction system, otherwise from the launcher root.
export function resolveContext(cwd) {
  const launcher = resolveLauncherRoot();
  const active = resolveActiveRoot(cwd || process.cwd());
  let configRoot = null;
  if (active && active.hasInstructions) configRoot = active.root;
  else if (launcher.valid) configRoot = launcher.root;
  return { launcherRoot: launcher.root, active, activeRoot: active ? active.root : null, configRoot };
}

export function requireConfigRoot(ctx) {
  if (!ctx.configRoot) {
    throw new SetupError(`Instruction template incomplete: ${toPosix(MARKER)} not found in the active project or in ${toPosix(ctx.launcherRoot)}. Restore it before relying on hooks or checks.`);
  }
  return ctx.configRoot;
}

// Per-worktree hook state lives in the worktree's own Git directory (never tracked, never shared
// between worktrees); outside Git it falls back to the git-ignored .claude/.hook-state/.
export function stateFile(ctx, name) {
  const base = ctx.active && ctx.active.gitDir
    ? path.join(ctx.active.gitDir, 'claude-hooks')
    : path.join(ctx.activeRoot || ctx.launcherRoot, '.claude', '.hook-state');
  const scope = ctx.activeRoot ? sha256(path.resolve(ctx.activeRoot).toLowerCase()).slice(0, 12) : 'global';
  return path.join(base, `${name}-${scope}.json`);
}

export function readState(file) {
  if (!existsSync(file)) return null;
  try { return JSON.parse(readFileSync(file, 'utf8')); } catch { return null; }
}

export function writeState(file, value) {
  mkdirSync(path.dirname(file), { recursive: true });
  const tmp = `${file}.${process.pid}.tmp`;
  writeFileSync(tmp, JSON.stringify(value, null, 2));
  renameSync(tmp, file);
}

// Capability selection record: the table under "## Capability selection" in decisions.md.
export function parseSelection(root) {
  const file = path.join(root, MARKER);
  if (!existsSync(file)) throw new SetupError(`Missing ${toPosix(MARKER)} in ${toPosix(root)}.`);
  const text = readText(file);
  const start = text.indexOf('## Capability selection');
  if (start < 0) throw new SetupError('decisions.md has no "## Capability selection" section.');
  const rows = [];
  for (const line of text.slice(start).split(/\r?\n/).slice(1)) {
    if (/^##\s/.test(line)) break;
    const cells = line.split('|').map((c) => c.trim());
    if (cells.length < 5 || cells[1] === 'Slot' || /^-+$/.test(cells[1]) || !cells[1]) continue;
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
  if (!existsSync(file)) throw new SetupError(`Missing facet ${slot}.${facet}: ${toPosix(path.relative(root, file))}`);
  return readJson(file);
}

export function parseCsproj(text) {
  const attr = (tag, name) => {
    const m = tag.match(new RegExp(`\\b${name}\\s*=\\s*"([^"]*)"`, 'i'));
    return m ? m[1] : null;
  };
  const tags = (name) => [...text.matchAll(new RegExp(`<${name}\\b([^>]*?)(/>|>([\\s\\S]*?)</${name}>)`, 'gi'))];
  const packages = tags('PackageReference').map((m) => {
    const inner = m[3] || '';
    const childVersion = inner.match(/<Version>([^<]*)<\/Version>/i);
    return {
      id: attr(m[1], 'Include') || attr(m[1], 'Update'),
      version: attr(m[1], 'Version') || (childVersion ? childVersion[1] : null),
      versionOverride: attr(m[1], 'VersionOverride'),
    };
  });
  const projects = tags('ProjectReference').map((m) => attr(m[1], 'Include')).filter(Boolean);
  const frameworks = tags('FrameworkReference').map((m) => attr(m[1], 'Include')).filter(Boolean);
  return { packages, projects, frameworks };
}

export function packageMatches(id, rules = []) {
  const lower = (id || '').toLowerCase();
  return rules.filter((r) => (r.id && r.id.toLowerCase() === lower) || (r.prefix && lower.startsWith(r.prefix.toLowerCase())));
}

// Package and project manifests whose actual state the hooks validate.
const MANIFEST_NAME = /(^|\/)(Directory\.Packages\.props|Directory\.Build\.props|package\.json|[^/]+\.csproj)$/i;
const MANIFEST_PATHSPECS = [':(glob)**/*.csproj', ':(glob)**/Directory.Packages.props', ':(glob)**/Directory.Build.props', ':(glob)**/package.json'];

export function isManifestPath(rel) {
  return MANIFEST_NAME.test(rel) && !rel.split('/').some((seg) => SKIP_DIRS.has(seg) || seg.startsWith('.'));
}

// Lists present manifest files of the active root (tracked plus untracked, not ignored). Git does not
// descend into nested repositories or linked worktrees; skipped directories are excluded explicitly.
export function listManifests(ctx) {
  const root = ctx.activeRoot;
  let rels;
  if (ctx.active && ctx.active.gitTop) {
    const r = git(root, ['ls-files', '-z', '--cached', '--others', '--exclude-standard', '--', ...MANIFEST_PATHSPECS]);
    if (!r.ok) throw new SetupError(`git ls-files failed in ${toPosix(root)}: ${r.stderr.trim()}`);
    rels = r.stdout.split('\0').filter(Boolean);
  } else {
    rels = walkManifests(root, root);
  }
  return [...new Set(rels.map(toPosix))].filter((rel) => isManifestPath(rel) && existsSync(path.join(root, rel))).sort();
}

function walkManifests(root, dir) {
  const out = [];
  for (const entry of readdirSync(dir)) {
    if (SKIP_DIRS.has(entry) || entry.startsWith('.')) continue;
    const full = path.join(dir, entry);
    const stat = statSync(full);
    if (stat.isDirectory()) {
      if (existsSync(path.join(full, '.git'))) continue; // nested repository or worktree
      out.push(...walkManifests(root, full));
    } else if (MANIFEST_NAME.test(entry)) {
      out.push(toPosix(path.relative(root, full)));
    }
  }
  return out;
}

export function headRevision(ctx) {
  if (!ctx.active || !ctx.active.gitTop) return 'no-git';
  const r = git(ctx.activeRoot, ['rev-parse', '--verify', '-q', 'HEAD']);
  return r.ok && r.stdout.trim() ? r.stdout.trim() : 'unborn';
}

export function snapshotManifests(ctx) {
  const files = {};
  for (const rel of listManifests(ctx)) {
    try { files[rel] = sha256(readFileSync(path.join(ctx.activeRoot, rel))); } catch { /* vanished meanwhile */ }
  }
  return { version: 1, root: path.resolve(ctx.activeRoot), head: headRevision(ctx), files };
}
