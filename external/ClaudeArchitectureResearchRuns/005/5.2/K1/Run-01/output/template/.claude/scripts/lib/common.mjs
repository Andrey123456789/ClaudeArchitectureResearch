// Kind: ENF | Scope: repo/meta | Capability: — | Loading: imported by .claude/hooks and .claude/scripts | Shared helpers: project root, stdin, globs, manifests, enforcement data
import { readFileSync, existsSync, readdirSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

const SKIPPED_DIRECTORIES = new Set(['node_modules', 'bin', 'obj', '.git', '.vs', 'dist', 'TestResults', 'coverage']);

export class EnforcementError extends Error {}

// The project root is derived from this file's location (.claude/scripts/lib/common.mjs),
// so it does not depend on the shell, the current directory or environment-variable expansion.
export function projectRoot() {
  const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..', '..');
  if (!existsSync(path.join(root, '.claude', 'settings.json'))) {
    throw new EnforcementError(`Project root not recognized: ${root} has no .claude/settings.json.`);
  }
  return root;
}

export function rootFromArgs(argv) {
  const index = argv.indexOf('--root');
  if (index === -1) {
    return projectRoot();
  }
  const value = argv[index + 1];
  if (!value || !existsSync(value) || !statSync(value).isDirectory()) {
    throw new EnforcementError(`--root must name an existing directory (got: ${value ?? 'nothing'}).`);
  }
  return path.resolve(value);
}

export async function readStdinJson() {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  const text = Buffer.concat(chunks).toString('utf8').trim();
  if (text === '') {
    return {};
  }
  try {
    return JSON.parse(text);
  } catch (error) {
    throw new EnforcementError(`Hook input is not valid JSON: ${error.message}`);
  }
}

// Returns a forward-slash path relative to root, or null when the path lies outside root.
export function toRootRelative(root, filePath) {
  if (!filePath) {
    return null;
  }
  const absolute = path.resolve(root, filePath);
  const relative = path.relative(root, absolute);
  if (relative === '' || relative.startsWith('..') || path.isAbsolute(relative)) {
    return null;
  }
  return relative.split(path.sep).join('/');
}

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
    } else {
      pattern += c.replace(/[.+^${}()|[\]\\]/g, '\\$&');
    }
  }
  return new RegExp(`^${pattern}$`, 'i');
}

export function matchesAny(relativePath, globs = []) {
  return globs.some((glob) => globToRegExp(glob).test(relativePath));
}

export function listFiles(root, startDirectory, predicate) {
  const results = [];
  const start = path.join(root, startDirectory);
  if (!existsSync(start)) {
    return results;
  }
  const stack = [start];
  while (stack.length > 0) {
    const current = stack.pop();
    for (const entry of readdirSync(current, { withFileTypes: true })) {
      if (entry.isDirectory()) {
        if (!SKIPPED_DIRECTORIES.has(entry.name)) {
          stack.push(path.join(current, entry.name));
        }
      } else {
        const relative = toRootRelative(root, path.join(current, entry.name));
        if (relative && predicate(relative)) {
          results.push(relative);
        }
      }
    }
  }
  return results.sort();
}

export function readJson(root, relativePath, { required = true } = {}) {
  const absolute = path.join(root, relativePath);
  if (!existsSync(absolute)) {
    if (required) {
      throw new EnforcementError(`Required enforcement data is missing: ${relativePath}.`);
    }
    return null;
  }
  try {
    return JSON.parse(readFileSync(absolute, 'utf8'));
  } catch (error) {
    throw new EnforcementError(`Enforcement data is not valid JSON: ${relativePath} (${error.message}).`);
  }
}

// Non-slot enforcement data plus the enforcement facets of the selected capability modules.
export function loadEnforcement(root) {
  const policy = readJson(root, '.claude/scripts/enforcement.json');
  const architecture = readJson(root, '.claude/scripts/facets/architecture/enforcement.json');
  const persistence = readJson(root, '.claude/scripts/facets/persistence/enforcement.json');
  const frontend = readJson(root, '.claude/scripts/facets/frontend/enforcement.json', { required: false });
  const facets = [architecture, persistence, frontend].filter(Boolean);
  return { policy, architecture, persistence, frontend, facets };
}

function attributes(tag) {
  const result = {};
  for (const match of tag.matchAll(/([A-Za-z_:][\w:.-]*)\s*=\s*"([^"]*)"/g)) {
    result[match[1]] = match[2];
  }
  return result;
}

function elements(text, name) {
  return [...text.matchAll(new RegExp(`<${name}\\b[^>]*>`, 'g'))].map((m) => attributes(m[0]));
}

export function parseProjectFile(text) {
  const projectTag = text.match(/<Project\b[^>]*>/);
  return {
    sdk: projectTag ? attributes(projectTag[0]).Sdk ?? '' : '',
    projectReferences: elements(text, 'ProjectReference').map((a) => a.Include).filter(Boolean),
    packageReferences: elements(text, 'PackageReference').filter((a) => a.Include || a.Update),
    frameworkReferences: elements(text, 'FrameworkReference').map((a) => a.Include).filter(Boolean),
    centralManagement: /<ManagePackageVersionsCentrally>\s*true\s*<\/ManagePackageVersionsCentrally>/i.test(text),
    packageVersions: elements(text, 'PackageVersion').filter((a) => a.Include),
  };
}

export function readText(root, relativePath) {
  return readFileSync(path.join(root, relativePath), 'utf8');
}

// True when the module with this import.meta.url is the script Node was started with.
export function isMainModule(moduleUrl) {
  if (!process.argv[1]) {
    return false;
  }
  const normalize = (p) => (process.platform === 'win32' ? path.resolve(p).toLowerCase() : path.resolve(p));
  return normalize(fileURLToPath(moduleUrl)) === normalize(process.argv[1]);
}

export function stableHash(value) {
  return createHash('sha256').update(value).digest('hex').slice(0, 16);
}

export function formatFindings(title, findings) {
  if (findings.length === 0) {
    return '';
  }
  return `${title}\n${findings.map((f) => `- ${f}`).join('\n')}`;
}
