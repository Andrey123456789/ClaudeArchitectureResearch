// Shared helpers for the instruction-system checkers and hooks.
// Dependency-free Node.js (18+); works the same on Windows, macOS, and Linux.
import fs from 'node:fs';
import path from 'node:path';

export class TemplateError extends Error {}

const ROOT_MARKERS = ['CLAUDE.md', path.join('.claude', 'capabilities')];

// Resolve the project root from explicit input, CLAUDE_PROJECT_DIR, or the
// working directory. Fails clearly instead of guessing.
export function resolveRoot(...hints) {
  const tried = [...hints, process.env.CLAUDE_PROJECT_DIR, process.cwd()].filter(Boolean);
  for (const hint of tried) {
    const root = path.resolve(hint);
    if (ROOT_MARKERS.every(m => fs.existsSync(path.join(root, m)))) return root;
  }
  throw new TemplateError(
    `Project root not found: none of [${tried.join(', ')}] contains CLAUDE.md and .claude/capabilities/. ` +
    'Run from the project root or set CLAUDE_PROJECT_DIR.');
}

export const toPosix = p => p.split(path.sep).join('/');

// Absolute path for a root-relative path; rejects paths that escape the root.
export function inRoot(root, rel) {
  const abs = path.resolve(root, rel);
  const back = path.relative(root, abs);
  if (back.startsWith('..') || path.isAbsolute(back)) throw new TemplateError(`Path escapes the project root: ${rel}`);
  return abs;
}

export function relFromRoot(root, abs) {
  const rel = path.relative(root, path.resolve(abs));
  if (rel.startsWith('..') || path.isAbsolute(rel)) return null;
  return toPosix(rel);
}

export const exists = (root, rel) => fs.existsSync(inRoot(root, rel));
export const readText = (root, rel) => fs.readFileSync(inRoot(root, rel), 'utf8').replace(/\r\n/g, '\n');

const SKIP_DIRS = new Set(['.git', 'node_modules', 'bin', 'obj', '.vs', 'dist', 'TestResults', 'coverage', '.cache']);

// Root-relative POSIX paths of all files below relDir (skipping build/vendor folders).
export function walk(root, relDir = '.') {
  const out = [];
  const start = inRoot(root, relDir);
  if (!fs.existsSync(start)) return out;
  const stack = [start];
  while (stack.length) {
    const dir = stack.pop();
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const abs = path.join(dir, entry.name);
      if (entry.isDirectory()) { if (!SKIP_DIRS.has(entry.name)) stack.push(abs); }
      else if (entry.isFile()) out.push(relFromRoot(root, abs));
    }
  }
  return out.sort();
}

export function splitFrontmatter(text) {
  if (!text.startsWith('---\n')) return { fm: null, body: text };
  const end = text.indexOf('\n---', 4);
  if (end === -1) return { fm: null, body: text };
  return { fm: text.slice(4, end), body: text.slice(end + 4).replace(/^\n+/, '') };
}

// Minimal YAML subset used by Claude Code frontmatter: scalars, folded/literal
// blocks (> or |), and block lists.
export function parseFrontmatter(fm) {
  const result = {};
  if (fm === null) return result;
  const lines = fm.split('\n');
  for (let i = 0; i < lines.length; i++) {
    const m = /^([A-Za-z][\w-]*):\s*(.*)$/.exec(lines[i]);
    if (!m) continue;
    const [, key, rest] = m;
    if (rest === '>' || rest === '|') {
      const parts = [];
      while (i + 1 < lines.length && /^\s+\S/.test(lines[i + 1])) parts.push(lines[++i].trim());
      result[key] = parts.join(rest === '>' ? ' ' : '\n');
    } else if (rest === '') {
      const items = [];
      while (i + 1 < lines.length && /^\s+-\s+/.test(lines[i + 1])) items.push(lines[++i].replace(/^\s+-\s+/, '').replace(/^["']|["']$/g, ''));
      result[key] = items;
    } else {
      result[key] = rest.replace(/^["']|["']$/g, '');
    }
  }
  return result;
}

// First non-empty line of the body (the one-line classification header).
export function headerLine(text) {
  const { body } = splitFrontmatter(text);
  return body.split('\n').find(l => l.trim() !== '') ?? '';
}

export function capabilityOf(text) {
  const m = /Capability:\s*([a-z0-9-]+\/[a-z0-9-]+)/.exec(headerLine(text));
  return m ? m[1] : null;
}

// Headings of a Markdown document, ignoring fenced code, with list numbering removed.
export function headings(text) {
  const out = [];
  let fence = false;
  for (const line of text.split('\n')) {
    if (/^(```|~~~)/.test(line)) { fence = !fence; continue; }
    const m = !fence && /^#{1,6}\s+(.*)$/.exec(line);
    if (m) out.push(m[1].replace(/^(\d+\.|Step \d+:)\s*/, '').trim());
  }
  return out;
}

export function extractJsonBlock(text, label) {
  const m = /```json\n([\s\S]*?)\n```/.exec(text);
  if (!m) throw new TemplateError(`${label}: missing \`\`\`json manifest block`);
  try { return JSON.parse(m[1]); } catch (e) { throw new TemplateError(`${label}: invalid JSON manifest block (${e.message})`); }
}

export function globToRegExp(glob) {
  let re = '';
  for (let i = 0; i < glob.length; i++) {
    const c = glob[i];
    if (c === '*' && glob[i + 1] === '*') {
      if (glob[i + 2] === '/') { re += '(?:.*/)?'; i += 2; } else { re += '.*'; i += 1; }
    } else if (c === '*') re += '[^/]*';
    else if (c === '?') re += '[^/]';
    else if (c === '{') { const end = glob.indexOf('}', i); re += '(?:' + glob.slice(i + 1, end).split(',').map(escapeRe).join('|') + ')'; i = end; }
    else re += escapeRe(c);
  }
  return new RegExp('^' + re + '$');
}

export const escapeRe = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

export const SLOTS = ['architecture', 'persistence', 'backend-testing', 'frontend'];
export const SELECTION_FILE = 'docs/capability-selection.md';

// Parse the selection table: | Slot | Status | Selected | Declared properties |
export function loadSelection(root) {
  const text = readText(root, SELECTION_FILE);
  const rows = [];
  for (const line of text.split('\n')) {
    const cells = line.split('|').slice(1, -1).map(c => c.trim());
    if (cells.length < 4 || !/^[a-z][a-z0-9-]*$/.test(cells[0])) continue;
    if (/required|optional/.test(cells[1])) rows.push({ slot: cells[0], status: cells[1], selected: cells[2] });
  }
  return { text, rows };
}

export function loadManifest(root, rel) {
  return extractJsonBlock(readText(root, rel), rel);
}

// Load selection, contracts, and selected modules. Throws on structural errors
// that make further checking meaningless.
export function loadCapabilities(root) {
  const { rows } = loadSelection(root);
  const contracts = {};
  for (const slot of SLOTS) {
    const rel = `.claude/capabilities/${slot}/CONTRACT.md`;
    if (exists(root, rel)) contracts[slot] = loadManifest(root, rel);
  }
  const modules = {};
  for (const row of rows) {
    if (/^none\b/.test(row.selected)) continue;
    const rel = `.claude/capabilities/${row.slot}/${row.selected}/MODULE.md`;
    if (exists(root, rel)) modules[row.slot] = { rel, manifest: loadManifest(root, rel) };
  }
  const allModules = walk(root, '.claude/capabilities')
    .filter(p => /^\.claude\/capabilities\/[^/]+\/[^/]+\/MODULE\.md$/.test(p))
    .map(rel => ({ rel, manifest: loadManifest(root, rel) }));
  return { rows, contracts, modules, allModules };
}

// Replace <role:NAME> tokens with the frame's project directory glob.
export function resolveRoleTokens(pattern, frameManifest) {
  return pattern.replace(/<role:([^>]+)>/g, (_, role) => {
    const layer = (frameManifest?.properties?.layers ?? []).find(l => l.role === role);
    if (!layer) throw new TemplateError(`Role "${role}" is not bound to a project by the architecture frame`);
    return `backend/*${layer.suffix}`;
  });
}

export function termRegExp(term) {
  const start = /^\w/.test(term) ? '\\b' : '';
  const end = /\w$/.test(term) ? '\\b' : '';
  return new RegExp(start + escapeRe(term) + end, 'i');
}

export function report(title, { errors = [], warnings = [], info = [] }) {
  const lines = [`${title}: ${errors.length} error(s), ${warnings.length} warning(s)`];
  for (const e of errors) lines.push(`  ERROR   ${e}`);
  for (const w of warnings) lines.push(`  WARNING ${w}`);
  for (const i of info) lines.push(`  INFO    ${i}`);
  return lines.join('\n');
}
