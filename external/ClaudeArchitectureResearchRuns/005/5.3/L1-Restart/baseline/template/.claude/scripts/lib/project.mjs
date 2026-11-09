// Shared helpers for instruction-system hooks and checks.
// Cross-platform (Node.js >= 18, ESM). No shell expansion: every path is resolved here.
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const SKIP_DIRS = new Set(['node_modules', 'bin', 'obj', '.git', '.vs', 'dist', 'TestResults', 'coverage']);

export class SetupError extends Error {}

// The project root is three levels above this file: <root>/.claude/scripts/lib/project.mjs
export function resolveRoot() {
  const here = path.dirname(fileURLToPath(import.meta.url));
  const root = path.resolve(here, '..', '..', '..');
  const marker = path.join(root, '.claude', 'rules', '3-project', 'decisions.md');
  if (!existsSync(marker)) {
    throw new SetupError(`Instruction template incomplete: expected ${toPosix(path.relative(process.cwd(), marker)) || marker}. Restore .claude/rules/3-project/decisions.md before relying on hooks or checks.`);
  }
  return root;
}

export function toPosix(p) {
  return p.split(path.sep).join('/').replace(/\\/g, '/');
}

// Repository-relative POSIX path, or null when the path escapes the root.
export function toRepoRelative(root, filePath) {
  if (!filePath) return null;
  const abs = path.resolve(root, filePath);
  const rel = path.relative(root, abs);
  if (rel === '' || rel.startsWith('..') || path.isAbsolute(rel)) return null;
  return toPosix(rel);
}

export function readText(file) {
  return readFileSync(file, 'utf8');
}

export async function readStdinJson() {
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  const raw = Buffer.concat(chunks).toString('utf8').trim();
  if (!raw) return {};
  try {
    return JSON.parse(raw);
  } catch {
    throw new SetupError('Hook input is not valid JSON.');
  }
}

export function listFiles(dir, predicate = () => true) {
  const out = [];
  if (!existsSync(dir)) return out;
  for (const entry of readdirSync(dir)) {
    if (SKIP_DIRS.has(entry)) continue;
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

// Capability selection record: the table under "## Capability selection" in decisions.md.
export function parseSelection(root) {
  const file = path.join(root, '.claude', 'rules', '3-project', 'decisions.md');
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
